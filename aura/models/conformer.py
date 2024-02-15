# ---INFO-----------------------------------------------------------------------
# Author        Aditya Prakash

# TODO  1. None

# ---DEPENDENCIES---------------------------------------------------------------
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchmetrics
from lightning import LightningModule
import torchmetrics

from einops import rearrange
from einops.layers.torch import Rearrange


# ---PATCH EMBEDDING------------------------------------------------------------
class PatchEmbedding(nn.Module):
    def __init__(
        self,
        n_electrodes,
        hid_channels,
        shallownet_kernel_size=(1, 25),
        shallownet_pool_size=(1, 75),
        shallownet_pool_stride=(1, 15),
        dropout=0.5,
    ):
        super().__init__()

        self.shallownet = nn.Sequential(
            nn.Conv2d(1, hid_channels, shallownet_kernel_size, (1, 1)),
            nn.Conv2d(hid_channels, hid_channels, (n_electrodes, 1), (1, 1)),
            nn.BatchNorm2d(hid_channels),
            nn.ELU(),
            # Pooling acts as slicing to obtain 'patch' along the time dimension
            # as in ViT.
            nn.AvgPool2d(shallownet_pool_size, shallownet_pool_stride),
            nn.Dropout(dropout),
        )
        # Transpose, Conv could enhance fiting ability slightly
        self.projection = nn.Sequential(
            nn.Conv2d(hid_channels, hid_channels, (1, 1), stride=(1, 1)),
            Rearrange("b e (h) (w) -> b (h w) e"),
        )

    def forward(self, x):
        b, _, _, _ = x.shape
        x = self.shallownet(x)
        x = self.projection(x)
        return x


# ---MULTI-HEAD ATTENTION-------------------------------------------------------
class MultiHeadAttention(nn.Module):
    def __init__(self, hid_channels, heads, dropout=0.5):
        super().__init__()
        self.hid_channels = hid_channels
        self.heads = heads
        self.K = nn.Linear(hid_channels, hid_channels)
        self.Q = nn.Linear(hid_channels, hid_channels)
        self.V = nn.Linear(hid_channels, hid_channels)
        self.att_drop = nn.Dropout(dropout)
        self.projection = nn.Linear(hid_channels, hid_channels)

    def forward(self, x, mask=None):
        q = rearrange(self.Q(x), "b n (h d) -> b h n d", h=self.heads)
        k = rearrange(self.K(x), "b n (h d) -> b h n d", h=self.heads)
        v = rearrange(self.V(x), "b n (h d) -> b h n d", h=self.heads)
        energy = torch.einsum("bhqd, bhkd -> bhqk", q, k)
        if mask is not None:
            fill_value = torch.finfo(torch.float32).min
            energy.mask_fill(~mask, fill_value)

        scaling = self.hid_channels ** (1 / 2)
        att = F.softmax(energy / scaling, dim=-1)
        att = self.att_drop(att)
        out = torch.einsum("bhal, bhlv -> bhav ", att, v)
        out = rearrange(out, "b h n d -> b n (h d)")
        out = self.projection(out)
        return out


# ---MISCELLANEOUS--------------------------------------------------------------
class ResidualAdd(nn.Module):
    def __init__(self, fn):
        super().__init__()
        self.fn = fn

    def forward(self, x, **kwargs):
        res = x
        x = self.fn(x, **kwargs)
        x += res
        return x


class FeedForwardBlock(nn.Sequential):
    def __init__(self, hid_channels, expansion=4, dropout=0.5):
        super().__init__(
            nn.Linear(hid_channels, expansion * hid_channels),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(expansion * hid_channels, hid_channels),
        )


class GELU(nn.Module):
    def forward(self, input):
        return input * 0.5 * (1.0 + torch.erf(input / 1.41421))


# ---TRANSFORMER ENCODER--------------------------------------------------------
class TransformerEncoderBlock(nn.Sequential):
    def __init__(
        self, hid_channels, heads, dropout, forward_expansion, forward_dropout
    ):
        super().__init__(
            ResidualAdd(
                nn.Sequential(
                    nn.LayerNorm(hid_channels),
                    MultiHeadAttention(hid_channels, heads, dropout),
                    nn.Dropout(dropout),
                )
            ),
            ResidualAdd(
                nn.Sequential(
                    nn.LayerNorm(hid_channels),
                    FeedForwardBlock(
                        hid_channels,
                        expansion=forward_expansion,
                        dropout=forward_dropout,
                    ),
                    nn.Dropout(dropout),
                )
            ),
        )


class TransformerEncoder(nn.Sequential):
    def __init__(
        self,
        depth,
        hid_channels,
        heads=10,
        dropout=0.5,
        forward_expansion=4,
        forward_dropout=0.5,
    ):
        super().__init__(
            *[
                TransformerEncoderBlock(
                    hid_channels=hid_channels,
                    heads=heads,
                    dropout=dropout,
                    forward_expansion=forward_expansion,
                    forward_dropout=forward_dropout,
                )
                for _ in range(depth)
            ]
        )


# ---CLASSIFICATION HEAD--------------------------------------------------------
class ClassificationHead(nn.Sequential):
    def __init__(
        self,
        in_channels: int,
        out_units: int,
        hid_channels: int = 32,
        dropout: float = 0.5,
    ):
        super().__init__()
        if out_units == 1:
            activation = nn.Sigmoid()
        else:
            activation = nn.Softmax(dim=-1)
        self.fc = nn.Sequential(
            nn.Linear(in_channels, hid_channels * 8),
            nn.ELU(),
            nn.Dropout(dropout),
            nn.Linear(hid_channels * 8, hid_channels),
            nn.ELU(),
            nn.Dropout(dropout),
            nn.Linear(hid_channels, out_units),
            activation,
        )

    def forward(self, x):
        x = x.contiguous().view(x.size(0), -1)
        x = self.fc(x)
        return x


# ---CONFORMER------------------------------------------------------------------
class Conformer(nn.Module):
    def __init__(
        self,
        n_electrodes=62,
        sampling_rate=200,
        num_samples=500,
        embed_dropout=0.5,
        shallownet_kernel_size=(1, 25),
        shallownet_pool_size=(1, 75),
        shallownet_pool_stride=(1, 15),
        hid_channels=40,
        depth=6,
        heads=10,
        dropout=0.5,
        forward_expansion=4,
        forward_dropout=0.5,
        cls_channels=32,
        cls_dropout=0.5,
        out_units=2,
    ):
        super().__init__()
        self.n_electrodes = n_electrodes
        self.sampling_rate = sampling_rate
        self.num_samples = num_samples
        self.embed_dropout = embed_dropout
        self.shallownet_kernel_size = shallownet_kernel_size
        self.shallownet_pool_size = shallownet_pool_size
        self.shallownet_pool_stride = shallownet_pool_stride
        self.hid_channels = hid_channels
        self.depth = depth
        self.heads = heads
        self.dropout = dropout
        self.forward_expansion = forward_expansion
        self.forward_dropout = forward_dropout
        self.cls_channels = cls_channels
        self.cls_dropout = cls_dropout
        self.out_units = out_units

        self.embd = PatchEmbedding(
            n_electrodes,
            hid_channels,
            shallownet_kernel_size,
            shallownet_pool_size,
            shallownet_pool_stride,
            embed_dropout,
        )
        self.encoder = TransformerEncoder(
            depth,
            hid_channels,
            heads=heads,
            dropout=dropout,
            forward_expansion=forward_expansion,
            forward_dropout=forward_dropout,
        )
        self.cls = ClassificationHead(
            in_channels=self.feature_dim(),
            out_units=out_units,
            hid_channels=cls_channels,
            dropout=cls_dropout,
        )

    def feature_dim(self):
        with torch.no_grad():
            mx = torch.zeros(1, 1, self.n_electrodes, self.num_samples)

            mx = self.embd(mx)
            mx = self.encoder(mx)
            mx = mx.flatten(start_dim=1)

            return mx.shape[1]

    def forward(self, x):
        x = self.embd(x)
        x = self.encoder(x)
        x = x.flatten(start_dim=1)
        x = self.cls(x)
        return x


# ---LIGHTNING CONFORMER--------------------------------------------------------
class LightningConformer(LightningModule):
    def __init__(
        self,
        n_electrodes=62,
        sampling_rate=200,
        num_samples=500,
        embed_dropout=0.5,
        shallownet_kernel_size=(1, 25),
        shallownet_pool_size=(1, 75),
        shallownet_pool_stride=(1, 15),
        hid_channels=40,
        depth=6,
        heads=10,
        dropout=0.5,
        forward_expansion=4,
        forward_dropout=0.5,
        cls_channels=32,
        cls_dropout=0.5,
        out_units=1,
        lr=1e-3,
        weight_decay=1e-4,
    ):
        super().__init__()
        self.save_hyperparameters()
        self.model = Conformer(
            n_electrodes=n_electrodes,
            sampling_rate=sampling_rate,
            num_samples=num_samples,
            embed_dropout=embed_dropout,
            shallownet_kernel_size=shallownet_kernel_size,
            shallownet_pool_size=shallownet_pool_size,
            shallownet_pool_stride=shallownet_pool_stride,
            hid_channels=hid_channels,
            depth=depth,
            heads=heads,
            dropout=dropout,
            forward_expansion=forward_expansion,
            forward_dropout=forward_dropout,
            cls_channels=cls_channels,
            cls_dropout=cls_dropout,
            out_units=out_units,
        )
        if out_units == 1:
            self.loss_fn = F.binary_cross_entropy
            task = "binary"
        else:
            self.loss_fn = F.cross_entropy
            task = "multiclass"
        self.train_acc = torchmetrics.Accuracy(task=task, num_classes=out_units)
        self.valid_acc = torchmetrics.Accuracy(task=task, num_classes=out_units)

        self.example_input_array = torch.zeros(1, 1, n_electrodes, num_samples)

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self.model(x)
        loss = self.loss_fn(y_hat, y)
        accu = self.train_acc(y_hat, y)
        self.log("train_loss", loss, on_step=True, on_epoch=False)
        self.log("train_accu", accu, on_step=True, on_epoch=False)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self.model(x)
        loss = self.loss_fn(y_hat, y)
        accu = self.valid_acc(y_hat, y)
        self.log("valid_loss", loss, on_step=False, on_epoch=True)
        self.log("valid_accu", accu, on_step=False, on_epoch=True)

    def configure_optimizers(self):
        optimizer = torch.optim.AdamW(
            self.parameters(),
            lr=self.hparams.lr,
            weight_decay=self.hparams.weight_decay,
        )
        return optimizer
