from typing import List, Tuple

import numpy as np
import torch.utils.data


class KeyboardDataset(torch.utils.data.Dataset):

    def __init__(self, data: List[Tuple[np.array, int]]):
        self.data = data
    def __getitem__(self, index):
        # noinspection PyArgumentList
        input_arr = self.data[index][0].astype(np.float32)
        # noinspection PyArgumentList
        output_arr = self.data[index][1]
        return input_arr, output_arr

    def __len__(self):
        return len(self.data)
