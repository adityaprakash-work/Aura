# ---INFO-----------------------------------------------------------------------
# Author(s)     Aditya Prakash
#               Uthamkumar M.

# TODO  1. -
#       2. -

# ---DEPENDENCIES---------------------------------------------------------------
import torch
import torch.nn as nn
import torch.nn.functional as F

class Ensure4d(nn.Module):
    def forward(self, x):
        while len(x.shape) < 4:
            x = x.unsqueeze(-1)
        return x
    
class CausalConv1d(nn.Conv1d):
    def __init__(
        self,
        in_channels,
        out_channels,
        kernel_size,
        dilation=1,
        **kwargs,
    ):
        assert "padding" not in kwargs, (
            "The padding parameter is controlled internally by "
            f"{type(self).__name__} class. You should not try to override this"
            " parameter."
        )

        super().__init__(
            in_channels=in_channels,
            out_channels=out_channels,
            kernel_size=kernel_size,
            dilation=dilation,
            padding=(kernel_size - 1) * dilation,
            **kwargs,
        )

    def forward(self, X):
        out = super().forward(X)
        return out[..., : -self.padding[0]]


class MaxNormLinear(nn.Linear):
    def __init__(
        self, in_features, out_features, bias=True, max_norm_val=2, eps=1e-5, **kwargs,
    ):
        super().__init__(
            in_features=in_features, out_features=out_features, bias=bias, **kwargs,
        )
        self._max_norm_val = max_norm_val
        self._eps = eps

    def forward(self, X):
        self._max_norm()
        return super().forward(X)

    def _max_norm(self):
        with torch.no_grad():
            norm = self.weight.norm(2, dim=0, keepdim=True).clamp(
                min=self._max_norm_val / 2
            )
            desired = torch.clamp(norm, max=self._max_norm_val)
            self.weight *= desired / (self._eps + norm)
