import torch
import torchvision
import torch.nn as nn
from torch import optim
import torch.nn.functional as F
import torchvision.transforms as transforms
from torch.utils.data import DataLoader,Dataset
import matplotlib.pyplot as plt
import torchvision.utils
import numpy as np
import random
import sys

train_batch_size = 32        
train_number_epochs = 50     
	
class SiameseNetworkDataset(Dataset):
    
    def __init__(self, data_folder):
        self.data_folder = data_folder
        self.data_files = [f for f in os.listdir(data_folder) if f.endswith('.txt')]
        self.texts = []
        self.load_texts()

    def load_texts(self):
        for file_name in self.data_files:
            with open(os.path.join(self.data_folder, file_name), 'r', encoding='utf-8') as file:
                self.texts.extend(file.readlines())

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        return text

    
transform = transforms.Compose([transforms.Resize((100,100)), 
                                transforms.ToTensor()])
siamese_dataset = SiameseNetworkDataset(codeDataset=sys.argv[1],
                                        transform=transform,
                                        should_invert=False)

train_dataloader = DataLoader(siamese_dataset,
                            shuffle=True,
                            batch_size=train_batch_size)
							

