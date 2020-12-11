import torch
import torch.nn as nn
import torch.nn.functional as F

import dataset
import musictheory
import output

REBUILD_DATASET, CONVERT_DATASET = True, True

if REBUILD_DATASET:
    dataset.build()
if CONVERT_DATASET:
    dataset.convert()
data = dataset.load()


class jamnet(nn.Module):
    def __init__(self):
        super().__init__()
        # Layers

    def forward(self):
        pass
