import datetime as dt
import os
import pickle
from typing import List, Optional, Dict
import sys
import numpy as np
import torch
import torch.nn as nn
from tensorboardX import SummaryWriter
from torch.utils.data import DataLoader

from soundboard.ml.data.data_splitter import DataSplitter
from soundboard.ml.network.mynetwork import MyNet
from soundboard.ml.params import BATCH_MIN, USER_ITER, VAL_ITER, TEST_ITER, BATCH_SIZE

eps = 1e-8

SAVE_FILE_NAME = "save.pickle"

def append_to(array: Optional[np.array], new_array: torch.Tensor):
    new_array_np = new_array.cpu().detach().numpy()
    if len(new_array_np.shape) <= 1:
        new_array_np = np.array([new_array_np])
    if array is None:
        return new_array_np
    else:
        return np.concatenate((array, new_array_np), axis=0)


class KeyboardTrainer:
    writer: SummaryWriter
    output_dir: str
    writer_dir: str
    model: torch.nn.Module
    # noinspection PyUnresolvedReferences
    optimizer: torch.optim.Optimizer

    def __init__(self, data_splitter: DataSplitter, device, max_step=10000000):
        self.data_splitter = data_splitter
        self.max_step = max_step
        self.criterion = nn.CrossEntropyLoss()
        self.n_iter = 0
        self.device = device
        self.user_names = self.data_splitter.user_names
        self.current_user_id = 0
        self.last_loss = None
        self.cached_scalar = {}

    @property
    def current_user_name(self):
        return self.user_names[self.current_user_id]

    def save_model(self, user_name: str):  # save the training status and model
        filename = f"modelTrained_{user_name}_{self.n_iter}_{self.last_loss}.pickle"
        print(f"Creating checkpoint: {filename}")
        filepath = os.path.join(self.output_dir, filename)
        torch.save({'epoch': self.n_iter,                 # the number of training iter
                    'model_state_dict': self.model.state_dict(),  # the parameter of nerual network
                    'optimizer_state_dict': self.optimizer.state_dict(),  # the status of optimizer
                    'loss': self.last_loss}, filepath)    # the current loss
        print(user_name, self.n_iter)
        self.save_files[user_name][self.n_iter] = filepath
        self.save_to(os.path.join(self.output_dir, "save.pickle"))

    def load_model(self, user_name: str) -> bool:  # load the model and training status
        min_iter = -1
        checkpoint_path = None
        if user_name in self.save_files:
            for n_iter, iter_checkpoint_path in self.save_files[user_name].items():
                if n_iter > min_iter:
                    min_iter = n_iter
                    checkpoint_path = iter_checkpoint_path
        else:
            self.save_files[user_name] = dict()
        if checkpoint_path is None:   # if there are no existing model, initialize a new model
            print('There is no exiting mode!')
            self.n_iter = 0
            # noinspection PyUnresolvedReferences
            self.model = MyNet(4, 64, 2048, 26).to(self.device)
            self.optimizer = torch.optim.Adam(params=self.model.parameters(), lr=0.0001, weight_decay=1e-4)
            return False
        # if there are an existing model, load the training status and model parameter
        print(f"checkpoint file: {checkpoint_path}")
        with open(checkpoint_path, "rb") as model_file:
            checkpoint = torch.load(model_file)
        self.n_iter = checkpoint['epoch']
        self.model = MyNet(4, 64, 2048, 26).to(self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer = torch.optim.Adam(params=self.model.parameters(), lr=0.0001, weight_decay=1e-4)
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        return True

    def save_to(self, file_dir):   # save the information of configuration
        save_file_content = {
            "current_user_id": self.current_user_id,
            "user_names": self.user_names,
            "save_files": self.save_files,
            "output_dir": self.output_dir,
            "writer_dir": self.writer_dir,
        }
        with open(file_dir, "wb") as save_file:
            pickle.dump(save_file_content, save_file)

    def load_from(self, file_dir):  # load the information of configuration
        with open(file_dir, "rb") as save_file:
            save_file_content = pickle.load(save_file)
        self.current_user_id = save_file_content["current_user_id"]
        self.user_names = save_file_content["user_names"]
        self.save_files = save_file_content["save_files"]
        self.output_dir = save_file_content["output_dir"]
        self.writer_dir = save_file_content["writer_dir"]

    def train_iter(self, myinput: torch.Tensor, myoutput: torch.Tensor): # specific steps for training during each iter
        self.model.train()
        output = self.model(myinput)
        loss = self.criterion(output, myoutput)
        #self.add_scalar('train/loss', loss.detach().cpu().numpy())
        self.optimizer.zero_grad()
        loss.backward()

    # the main function during training
    def train(self, resume_from: Optional[str]):
        torch.autograd.set_detect_anomaly(True)   
        if sys.platform[0] == 'w': #windows
            output_parent_dir = r'.//checkpoints'
            run_dir = r'.//runs//'
        else:    #linux
            output_parent_dir = "./checkpoints"
            run_dir = "./runs/"
        if resume_from is None:    # train a new models
            current_datetime = dt.datetime.now().strftime("%Y%m%dT%H%M%S")
            self.output_dir = os.path.join(output_parent_dir, current_datetime)
            self.writer_dir = os.path.join(run_dir, current_datetime)
            print(self.writer_dir)
            if not os.path.isdir(self.output_dir):
                os.mkdir(self.output_dir)
            self.save_files = dict() 
        else:     # Continue to train the models you've already trained
            save_file_dir = os.path.join(output_parent_dir, resume_from)
            save_file_path = os.path.join(save_file_dir, SAVE_FILE_NAME)
            self.load_from(save_file_path) # load the trained model
        
        self.load_model(self.current_user_name)  # initialize the NN model
        train_loader = self.data_splitter.train_loader
        
        start_iter = self.n_iter   
        self.writer = SummaryWriter(log_dir=self.writer_dir)  # initialize 'writer' for visualization
        print(f"User {self.current_user_name} iter {self.n_iter}-{self.n_iter + USER_ITER}")
        print(f"iter: ...", end='')

        # begin traning ................
        while self.n_iter - start_iter < USER_ITER:  
            print(f"\riter: {self.n_iter}", end='')
            for i, (input, target) in enumerate(train_loader):
                myinput = input.cuda()  # cuda() will load the data from CPU to GPU
                myoutput = target.cuda()
                self.train_iter(myinput, myoutput) 
            self.n_iter += 1
            self.eval()   # after each training iter, we will test the model with the testing data
        self.save_model(self.current_user_name)

    def add_scalar(self, tag: str, value: float):   # this function work with SummaryWriter for visualization
        if tag not in self.cached_scalar:
            self.cached_scalar[tag] = {}
        if self.n_iter not in self.cached_scalar[tag]:
            self.cached_scalar[tag][self.n_iter] = {}
        self.cached_scalar[tag][self.n_iter][self.current_user_name] = value
        self.writer.add_scalar(f"{tag}_{self.current_user_name}", value, self.n_iter)

    def eval(self, checkpoint=True):  # evaluate our model 
        self.model.eval()
        loss_array: Optional[List[float]] = None
        rate_array: Optional[List[float]] = None
        data_loader = self.data_splitter.test_loader
        prefix = "test/" 
        for i, (input, target) in enumerate(data_loader):
            myinput = input.cuda()
            myoutput = target.cuda()
            output = self.model(myinput)
            loss = self.criterion(output, myoutput)
            #print(type(output),output.shape)
            max_val, max_index = output.max(1)
            correct_rate = (max_index[:] == myoutput[:]).float().mean()
            loss_array = append_to(loss_array, loss)
            rate_array = append_to(rate_array, correct_rate)
        avg_loss = np.average(loss_array)
        self.add_scalar(prefix + 'avg_loss', avg_loss)
        avg_rate = np.average(rate_array)
        self.add_scalar(prefix + 'avg_rate', avg_rate)
        print("   average loss:",  avg_loss, "average correct_rate:", avg_rate)
        if checkpoint:
            self.last_loss = avg_loss
        return avg_loss

    def close(self, path):
        print('(Visualize the training result) Please type:')
        print('tensorboard --logdir ' + self.writer_dir)
        self.writer.export_scalars_to_json(path)
        self.writer.close()
