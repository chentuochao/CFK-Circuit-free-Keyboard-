import random

from torch.utils.data import DataLoader

from soundboard.ml.data.dataset import KeyboardDataset
from soundboard.ml.params import BATCH_SIZE, WORKER_NUM

VAL_RATIO = 0.1 # VAL_RATIO is the proportion of the testing data


class DataSplitter:
    train_loader: DataLoader
    val_loader: DataLoader

    def __init__(self, all_data):
        random.shuffle(all_data)
        shuffled_data = all_data
        val_start = 0
        val_end = int(VAL_RATIO * len(shuffled_data))
        train_start = val_end
        train_end = len(shuffled_data)
        val_data = shuffled_data[val_start: val_end]
        train_data = shuffled_data[train_start: train_end]
        self.train_loader = DataLoader(
            KeyboardDataset(train_data),
            batch_size=BATCH_SIZE,
            shuffle=True,
            num_workers=WORKER_NUM
        )
        self.test_loader = DataLoader(
            KeyboardDataset(val_data),
            batch_size=BATCH_SIZE,
            shuffle=True,
            num_workers=WORKER_NUM
        )
        self.user_names = 'c'
