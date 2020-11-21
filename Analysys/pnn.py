import torch
import torch.nn as nn
import torch.nn.functional as F

class Stalin3000_anal_probe(nn.Module):
    def __init__(self, n):
        # вызов конструктора предка
        super(Stalin3000_anal_probe, self).__init__()
        self.insider = nn.Linear(n, 4*n)
        self.hl1 = nn.Linear(4*n, 2*n)
        self.hl2 = nn.Linear(2*n, 4*n)
        self.hl3 = nn.Linear(4*n, int(1.5*n))
        self.hl4 = nn.Linear(int(1.5*n), n)
        self.outsider = nn.Linear(n, 1)
        self.dropout = nn.Dropout()
        self.bnf1 = nn.BatchNorm1d(num_features=4*n, eps=1e-07, momentum=0.1, affine=True, track_running_stats=True)
        self.bnf2 = nn.BatchNorm1d(num_features=2*n, eps=1e-07, momentum=0.1, affine=True, track_running_stats=True)
        self.bnf3 = nn.BatchNorm1d(num_features=2 * n, eps=1e-07, momentum=0.1, affine=True, track_running_stats=True)
        self.block1 = nn.Sequential()

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x