#AUTOGENERATED! DO NOT EDIT! File to edit: dev/97_utils_test.ipynb (unless otherwise specified).

__all__ = ['synth_dbunch', 'RegModel', 'synth_learner']

#Cell
from .test import *
from .data.all import *
from .optimizer import *
from .learner import *
from torch.utils.data import TensorDataset

#Cell
from torch.utils.data import TensorDataset

def synth_dbunch(a=2, b=3, bs=16, n_train=10, n_valid=2, cuda=False):
    def get_data(n):
        x = torch.randn(bs*n, 1)
        return TensorDataset(x, a*x + b + 0.1*torch.randn(bs*n, 1))
    train_ds = get_data(n_train)
    valid_ds = get_data(n_valid)
    tfms = Cuda() if cuda else None
    train_dl = TfmdDL(train_ds, bs=bs, shuffle=True, after_batch=tfms, num_workers=0)
    valid_dl = TfmdDL(valid_ds, bs=bs, after_batch=tfms, num_workers=0)
    return DataBunch(train_dl, valid_dl)

#Cell
class RegModel(Module):
    def __init__(self): self.a,self.b = nn.Parameter(torch.randn(1)),nn.Parameter(torch.randn(1))
    def forward(self, x): return x*self.a + self.b

#Cell
@delegates(Learner.__init__)
def synth_learner(n_trn=10, n_val=2, cuda=False, lr=1e-3, data=None, **kwargs):
    if data is None: data = synth_dbunch(n_train=n_trn,n_valid=n_val, cuda=cuda)
    return Learner(data, RegModel(), lr=lr, loss_func=MSELossFlat(),
                   opt_func=partial(SGD, mom=0.9), **kwargs)