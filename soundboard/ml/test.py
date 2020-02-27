import pickle
import random
import sys
sys.path.append("C:/Users/chent/Desktop/Machine_learning") #please change the path of dir "soundboard" in your computer

import torch.utils.data
from torch.utils.data import DataLoader
import seaborn as sns
import matplotlib.pyplot as plt

from soundboard.ml.network.mynetwork import MyNet   # initialize the structure of CNN
from soundboard.ml.trainer.trainer import KeyboardTrainer
from soundboard.ml.data.data_splitter import DataSplitter


if __name__ == "__main__":
    random.seed(24)
    mode = sys.argv[1]
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    #device = torch.device("cuda:1")
    my_os = sys.platform
    if my_os[0] == 'w': #windows
        data_path = r'processed_data//sliced_data.pkl'
    else: #linux
        data_path = './processed_data/sliced_data.pkl'
    with open(data_path, "rb") as data_file:       # load the saved preprocessed data
        all_data = pickle.load(data_file)
        print(str(len(all_data))+' data of keystroke is loading')
    data_splitter = DataSplitter(all_data)         # turn the preprocessed data to the dataloader for the training

    if mode == "train":
        trainer = KeyboardTrainer(
            data_splitter,
            device
        )
        trainer.train(None)                       # begin training
        trainer.close("./train.json")
