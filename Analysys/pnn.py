import torch
import torch.nn as nn
import torch.nn.functional as F

class Stalin3000_anal_probe(nn.Module):
    def __init__(self, n):
        # вызов конструктора предка
        super(Stalin3000_anal_probe, self).__init__()
        self.n = n
        self.insider = nn.Linear(n, n+2)
        self.hl1 = nn.Linear(n+2, n+2)
        self.hl2 = nn.Linear(n+2, int(n/2))
        self.outsider = nn.Linear(int(n/2), 1)
        # self.bnf2 = nn.BatchNorm1d(num_features=4*n, eps=1e-07, momentum=0.1, affine=True, track_running_stats=True)
        # self.bnf1 = nn.BatchNorm1d(num_features=2*n, eps=1e-07, momentum=0.1, affine=True, track_running_stats=True)
        # self.bnf3 = nn.BatchNorm1d(num_features=int(1.5*n), eps=1e-07, momentum=0.1, affine=True, track_running_stats=True)

    def forward(self, x):
        # for _ in range(self.n // 3):
        x = F.dropout(F.relu(self.insider(x)), p=0.5)
        # for _ in range(self.n//2):
        x = F.dropout(F.relu(self.hl1(x)), p=0.5)
        x = F.dropout(F.relu(self.hl2(x)), p=0.5)
        x = F.dropout(F.relu(self.outsider(x)), p=0.5)
        return x