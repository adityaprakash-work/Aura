# ---INFO-----------------------------------------------------------------------
# Author(s)     Aditya Prakash
#               Uthamkumar M.

# TODO  1. -
#       2. -

# ---DEPENDENCIES---------------------------------------------------------------
import torch
import torch.nn as nn
import torch.nn.functional as F
import lightning as L
import torchmetrics
from einops.layers.torch import Rearrange
from .modules import Ensure4d, MaxNormLinear, CausalConv1d


# ---CONV BLOCKS----------------------------------------------------------------
class _ConvBlock(nn.Module):
    def __init__(
        self,
        n_channels,
        n_filters=16,
        kernel_size_1=64,
        kernel_size_2=16,
        pool_size_1=8,
        pool_size_2=7,
        depth_mult=2,
        dropout=0.3,
    ):
        super().__init__()
        self.conv1 = nn.Conv2d(
            in_channels=1,
            out_channels=n_filters,
            kernel_size=(kernel_size_1, 1),
            padding="same",
            bias=False,
        )
        self.bn1 = nn.BatchNorm2d(num_features=n_filters, eps=1e-4)
        n_depth_kernels = n_filters * depth_mult
        self.conv2 = nn.Conv2d(
            in_channels=n_filters,
            out_channels=n_depth_kernels,
            groups=n_filters,
            kernel_size=(1, n_channels),
            padding="valid",
            bias=False,
        )
        self.bn2 = nn.BatchNorm2d(num_features=n_depth_kernels, eps=1e-4)
        self.activation2 = nn.ELU()
        self.pool2 = nn.AvgPool2d(kernel_size=(pool_size_1, 1))
        self.drop2 = nn.Dropout2d(dropout)
        self.conv3 = nn.Conv2d(
            in_channels=n_depth_kernels,
            out_channels=n_depth_kernels,
            kernel_size=(kernel_size_2, 1),
            padding="same",
            bias=False,
        )
        self.bn3 = nn.BatchNorm2d(num_features=n_depth_kernels, eps=1e-4)
        self.activation3 = nn.ELU()
        self.pool3 = nn.AvgPool2d(kernel_size=(pool_size_2, 1))
        self.drop3 = nn.Dropout2d(dropout)

    def forward(self, X):
        # --Temporal convolution
        # shape: (batch_size, 1, T, C)
        X = self.conv1(X)
        X = self.bn1(X)
        # shape: (batch_size, F1, T, C)

        # --Depthwise channels convolution
        X = self.conv2(X)
        X = self.bn2(X)
        X = self.activation2(X)
        # shape: (batch_size, F1*D, T, 1)
        X = self.pool2(X)
        X = self.drop2(X)
        # shape: (batch_size, F1*D, T/P1, 1)

        # --Spatial convolution
        X = self.conv3(X)
        X = self.bn3(X)
        X = self.activation3(X)
        # shape: (batch_size, F1*D, T/P1, 1)
        X = self.pool3(X)
        X = self.drop3(X)
        # shape: (batch_size, F1*D, T/(P1*P2), 1)

        return X


# ---ATTENTION BLOCKS-----------------------------------------------------------
class _AttentionBlock(nn.Module):
    def __init__(
        self,
        in_shape=32,
        head_dim=8,
        num_heads=2,
        dropout=0.5,
    ):
        super().__init__()
        self.in_shape = in_shape
        self.head_dim = head_dim
        self.num_heads = num_heads
        self.dimshuffle = Rearrange("batch C T -> batch T C")
        self.ln = nn.LayerNorm(normalized_shape=in_shape, eps=1e-6)
        self.mha = _MHA(
            input_dim=in_shape,
            head_dim=head_dim,
            output_dim=in_shape,
            num_heads=num_heads,
            dropout=dropout,
        )
        self.drop = nn.Dropout(0.3)

    def forward(self, X):
        # shape: (batch_size, F2, Tw)
        X = self.dimshuffle(X)
        # shape: (batch_size, Tw, F2)
        out = self.ln(X)
        # --Self attention
        out = self.mha(out, out, out)
        # shape: (batch_size, Tw, F2)
        # --Skip connection
        out = X + self.drop(out)
        # shape: (batch_size, F2, Tw)
        return self.dimshuffle(out)


# ---TCN RESIDUAL BLOCKS--------------------------------------------------------
class _TCNResidualBlock(nn.Module):

    def __init__(
        self,
        in_channels,
        kernel_size=4,
        n_filters=32,
        dropout=0.3,
        activation=nn.ELU(),
        dilation=1,
    ):
        super().__init__()
        self.activation = activation
        self.dilation = dilation
        self.dropout = dropout
        self.n_filters = n_filters
        self.kernel_size = kernel_size
        self.in_channels = in_channels
        self.conv1 = CausalConv1d(
            in_channels=in_channels,
            out_channels=n_filters,
            kernel_size=kernel_size,
            dilation=dilation,
        )
        nn.init.kaiming_uniform_(self.conv1.weight)
        self.bn1 = nn.BatchNorm1d(n_filters)
        self.drop1 = nn.Dropout(dropout)
        self.conv2 = CausalConv1d(
            in_channels=n_filters,
            out_channels=n_filters,
            kernel_size=kernel_size,
            dilation=dilation,
        )
        nn.init.kaiming_uniform_(self.conv2.weight)
        self.bn2 = nn.BatchNorm1d(n_filters)
        self.drop2 = nn.Dropout(dropout)
        if in_channels != n_filters:
            self.reshaping_conv = nn.Conv1d(
                n_filters,
                kernel_size=1,
                padding="same",
            )
        else:
            self.reshaping_conv = nn.Identity()

    def forward(self, X):
        # shape: (batch_size, F2, Tw)
        # --Double dilated convolutions
        out = self.conv1(X)
        out = self.bn1(out)
        out = self.activation(out)
        out = self.drop1(out)

        out = self.conv2(out)
        out = self.bn2(out)
        out = self.activation(out)
        out = self.drop2(out)

        out = self.reshaping_conv(out)

        # --Residual connection
        out = X + out

        return self.activation(out)


# ---MHA------------------------------------------------------------------------
class _MHA(nn.Module):
    def __init__(
        self,
        input_dim: int,
        head_dim: int,
        output_dim: int,
        num_heads: int,
        dropout: float = 0.0,
    ):
        super(_MHA, self).__init__()
        self.input_dim = input_dim
        self.head_dim = head_dim
        self.embed_dim = head_dim * num_heads

        self.fc_q = nn.Linear(input_dim, self.embed_dim)
        self.fc_k = nn.Linear(input_dim, self.embed_dim)
        self.fc_v = nn.Linear(input_dim, self.embed_dim)

        self.fc_o = nn.Linear(self.embed_dim, output_dim)
        self.dropout = nn.Dropout(dropout)

    def forward(
        self, Q: torch.Tensor, K: torch.Tensor, V: torch.Tensor
    ) -> torch.Tensor:
        assert Q.shape[-1] == K.shape[-1] == V.shape[-1] == self.input_dim

        batch_size, _, _ = Q.shape
        Q = self.fc_q(Q)  # (B, S, D)
        K, V = self.fc_k(K), self.fc_v(V)  # (B, S, D)

        Q_ = torch.cat(Q.split(self.head_dim, -1), 0)  # (B', S, D')
        K_ = torch.cat(K.split(self.head_dim, -1), 0)  # (B', S, D')
        V_ = torch.cat(V.split(self.head_dim, -1), 0)  # (B', S, D')

        W = torch.softmax(
            Q_.bmm(K_.transpose(-2, -1)) / (self.head_dim**0.5), -1  # (B', D', S)
        )  # (B', N, M)

        H = torch.cat(
            (W.bmm(V_)).split(  # (B', S, S)  # (B', S, D')
                batch_size, 0
            ),  # [(B, S, D')] * num_heads
            -1,
        )  # (B, S, D)
        out = self.fc_o(H)

        return self.dropout(out)


# ---ATCNET---------------------------------------------------------------------
class ATCNet(nn.Module):
    def __init__(
        self,
        n_chans=None,
        n_outputs=None,
        input_window_seconds=10,
        sfreq=125.0,
        conv_block_n_filters=16,
        conv_block_kernel_size_1=64,
        conv_block_kernel_size_2=16,
        conv_block_pool_size_1=8,
        conv_block_pool_size_2=7,
        conv_block_depth_mult=2,
        conv_block_dropout=0.3,
        n_windows=5,
        att_head_dim=8,
        att_num_heads=2,
        att_dropout=0.5,
        tcn_depth=2,
        tcn_kernel_size=4,
        tcn_n_filters=32,
        tcn_dropout=0.3,
        tcn_activation=nn.ELU(),
        concat=False,
        max_norm_const=0.25,
    ):
        super().__init__()
        self.n_chans = n_chans
        self.n_outputs = n_outputs
        self.input_window_seconds = input_window_seconds
        self.sfreq = sfreq
        self.conv_block_n_filters = conv_block_n_filters
        self.conv_block_kernel_size_1 = conv_block_kernel_size_1
        self.conv_block_kernel_size_2 = conv_block_kernel_size_2
        self.conv_block_pool_size_1 = conv_block_pool_size_1
        self.conv_block_pool_size_2 = conv_block_pool_size_2
        self.conv_block_depth_mult = conv_block_depth_mult
        self.conv_block_dropout = conv_block_dropout
        self.n_windows = n_windows
        self.att_head_dim = att_head_dim
        self.att_num_heads = att_num_heads
        self.att_dropout = att_dropout
        self.tcn_depth = tcn_depth
        self.tcn_kernel_size = tcn_kernel_size
        self.tcn_n_filters = tcn_n_filters
        self.tcn_dropout = tcn_dropout
        self.tcn_activation = tcn_activation
        self.concat = concat
        self.max_norm_const = max_norm_const

        map = dict()
        for w in range(self.n_windows):
            map[f"max_norm_linears.[{w}].weight"] = f"final_layer.[{w}].weight"
            map[f"max_norm_linears.[{w}].bias"] = f"final_layer.[{w}].bias"
        self.mapping = map

        # Check later if we want to keep the Ensure4d. Not sure if we can
        # remove it or replace it with eipsum.
        self.ensuredims = Ensure4d()
        self.dimshuffle = Rearrange("batch C T 1 -> batch 1 T C")

        self.conv_block = _ConvBlock(
            n_channels=self.n_chans,  # input shape: (batch_size, 1, T, C)
            n_filters=conv_block_n_filters,
            kernel_size_1=conv_block_kernel_size_1,
            kernel_size_2=conv_block_kernel_size_2,
            pool_size_1=conv_block_pool_size_1,
            pool_size_2=conv_block_pool_size_2,
            depth_mult=conv_block_depth_mult,
            dropout=conv_block_dropout,
        )

        self.F2 = int(conv_block_depth_mult * conv_block_n_filters)
        self.Tc = int(
            self.input_window_seconds
            * self.sfreq
            / (conv_block_pool_size_1 * conv_block_pool_size_2)
        )
        self.Tw = self.Tc - self.n_windows + 1

        self.attention_blocks = nn.ModuleList(
            [
                _AttentionBlock(
                    in_shape=self.F2,
                    head_dim=self.att_head_dim,
                    num_heads=att_num_heads,
                    dropout=att_dropout,
                )
                for _ in range(self.n_windows)
            ]
        )

        self.temporal_conv_nets = nn.ModuleList(
            [
                nn.Sequential(
                    *[
                        _TCNResidualBlock(
                            in_channels=self.F2,
                            kernel_size=tcn_kernel_size,
                            n_filters=tcn_n_filters,
                            dropout=tcn_dropout,
                            activation=tcn_activation,
                            dilation=2**i,
                        )
                        for i in range(tcn_depth)
                    ]
                )
                for _ in range(self.n_windows)
            ]
        )

        if self.concat:
            self.final_layer = nn.ModuleList(
                [
                    MaxNormLinear(
                        in_features=self.F2 * self.n_windows,
                        out_features=self.n_outputs,
                        max_norm_val=self.max_norm_const,
                    )
                ]
            )
        else:
            self.final_layer = nn.ModuleList(
                [
                    MaxNormLinear(
                        in_features=self.F2,
                        out_features=self.n_outputs,
                        max_norm_val=self.max_norm_const,
                    )
                    for _ in range(self.n_windows)
                ]
            )

        self.out_fun = nn.Softmax(dim=1)

    def forward(self, X):
        # shape: (batch_size, C, T)
        X = self.ensuredims(X)
        # shape: (batch_size, C, T, 1)
        X = self.dimshuffle(X)
        # shape: (batch_size, 1, T, C)

        # --Sliding window
        conv_feat = self.conv_block(X)
        # shape: (batch_size, F2, Tc, 1)
        conv_feat = conv_feat.view(-1, self.F2, self.Tc)
        # shape: (batch_size, F2, Tc)

        # --Sliding window
        sw_concat = []  # to store sliding window outputs
        for w in range(self.n_windows):
            conv_feat_w = conv_feat[..., w : w + self.Tw]
            # shape: (batch_size, F2, Tw)
            # --Attention block
            att_feat = self.attention_blocks[w](conv_feat_w)
            # shape: (batch_size, F2, Tw)
            # --Temporal convolutional network (TCN)
            tcn_feat = self.temporal_conv_nets[w](att_feat)[..., -1]
            # shape: (batch_size, F2)
            # Outputs of sliding window can be either averaged after being
            # mapped by dense layer or concatenated then mapped by a dense
            # layer
            if not self.concat:
                tcn_feat = self.final_layer[w](tcn_feat)
            sw_concat.append(tcn_feat)

        # --Aggregation and prediction
        if self.concat:
            sw_concat = torch.cat(sw_concat, dim=1)
            sw_concat = self.final_layer[0](sw_concat)
        else:
            if len(sw_concat) > 1:  # more than one window
                sw_concat = torch.stack(sw_concat, dim=0)
                sw_concat = torch.mean(sw_concat, dim=0)
            else:  # one window (# windows = 1)
                sw_concat = sw_concat[0]

        return self.out_fun(sw_concat)


# ---ATCNET-LIGHTNING-----------------------------------------------------------
class LightningATCNet(L.LightningModule):
    def __init__(self, *model_args, **model_kwargs):
        super().__init__()
        self.save_hyperparameters()
        self.model = ATCNet(*model_args, **model_kwargs)
        self.loss = nn.CrossEntropyLoss()
        self.accuracy = torchmetrics.Accuracy(
            task="multiclass", num_classes=self.model.n_outputs
        )
        self.example_input_array = torch.rand(
            1, 
            self.model.n_chans,
            int(self.model.input_window_seconds * self.model.sfreq),
        )

    def forward(self, X):
        return self.model(X)

    def training_step(self, batch, batch_idx):
        X, y = batch
        y = y.float()
        y_hat = self.model(X)
        loss = self.loss(y_hat, y)
        y_hat = torch.argmax(y_hat, dim=1)
        y = torch.argmax(y, dim=1)
        accu = self.accuracy(y_hat, y)
        self.log("train_loss", loss, on_step=True, on_epoch=True, prog_bar=True)
        self.log("train_acc", accu, on_step=True, on_epoch=True, prog_bar=True)
        return loss

    def validation_step(self, batch, batch_idx):
        X, y = batch
        y = y.float()
        y_hat = self.model(X)
        loss = self.loss(y_hat, y)
        y_hat = torch.argmax(y_hat, dim=1)
        y = torch.argmax(y, dim=1)
        accu = self.accuracy(y_hat, y)
        self.log("val_loss", loss, on_step=True, on_epoch=True, prog_bar=True)
        self.log("val_acc", accu, on_step=True, on_epoch=True, prog_bar=True)
        return loss

    def test_step(self, batch, batch_idx):
        X, y = batch
        y = y.float()
        y = torch.argmax(y, dim=1)
        y_hat = self.model(X)
        y_hat = torch.argmax(y_hat, dim=1)
        accu = self.accuracy(y_hat, y)
        self.log("test_acc", accu, on_step=True, on_epoch=True, prog_bar=True)
        return accu

    def configure_optimizers(self):
        optimizer = torch.optim.AdamW(
            self.model.parameters(),
            lr=0.001,
            weight_decay=0.004,
        )
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer,
            T_max=10,
            eta_min=1e-4,
        )
        return {
            "optimizer": optimizer,
            "lr_scheduler": {
                "scheduler": scheduler,
                "interval": "step",
            },
        }
