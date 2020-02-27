import math
from typing import List
import torch
import torch.nn as nn


class MyNet(nn.Module):
    def __init__(self, input_dim, output_dim, key_length, output_num):
        super(MyNet, self).__init__()
        self.n = input_dim
        self.m = output_num
        self.kernel1_size = 7
        self.kernel2_size = 5
        self.length = math.ceil(math.ceil(key_length / self.kernel1_size) / self.kernel2_size) 

        # the first convolutional layer
        self.conv1 = nn.Sequential(
            nn.Conv1d(
                in_channels=input_dim,
                out_channels=input_dim * 2,
                kernel_size=self.kernel1_size,
                padding=(self.kernel1_size - 1) // 2
            ),
            nn.BatchNorm1d(input_dim * 2)
        )
        # the second convolutional layer
        self.conv2 = nn.Sequential(
            nn.Conv1d(
                in_channels=input_dim * 2,
                out_channels=input_dim * 4,
                kernel_size=self.kernel1_size,
                padding=(self.kernel1_size - 1) // 2
            ),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=self.kernel1_size, ceil_mode=True),
            nn.BatchNorm1d(input_dim * 4)
        )
        # the third convolutional layer
        self.conv3 = nn.Sequential(
            nn.Conv1d(
                in_channels=input_dim * 4,
                out_channels=input_dim * 8,
                kernel_size=self.kernel2_size,
                padding=(self.kernel2_size - 1) // 2
            ),
            nn.ReLU(),
            nn.BatchNorm1d(input_dim * 8)
        )
        # the forth convolutional layer
        self.conv4 = nn.Sequential(
            nn.Conv1d(
                in_channels=input_dim * 8,
                out_channels=input_dim * 16,
                kernel_size=self.kernel2_size,
                padding=(self.kernel2_size - 1) // 2
            ),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=self.kernel2_size, ceil_mode=True),
            nn.BatchNorm1d(input_dim * 16),
        )
        # the dropout layer
        self.dropout = nn.Dropout(p=0.5)
        assert input_dim * 16 == output_dim
        # the full connected layer
        self.full_connect = nn.Sequential(
            nn.Linear(self.length * output_dim, self.m),
            nn.ReLU(),
            nn.BatchNorm1d(self.m)
        )

    # connect the above layers
    def forward(self, input: torch.Tensor):
        x = input
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.conv4(x)
        x = self.dropout(x)
        x = self.full_connect(x.view(x.shape[0], -1))
        #print(x.shape)
        return x

    def process_lengths(self, lengths: List[int]):
        return [math.ceil(math.ceil(length / self.kernel1_size) / self.kernel2_size) for length in lengths]
