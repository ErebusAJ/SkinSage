from django.db import models
import torch.nn as nn
import torchvision.models as model


class ResnetModel(nn.Module):
    def __init__(self, num_classes):
        super(ResnetModel, self).__init__()
        # Define your ResNet model architecture
        self.resnet = model.resnet101(pretrained=False)
        # Modify the classifier layer for your specific task
        self.resnet.fc = nn.Linear(self.resnet.fc.in_features, num_classes)

    def forward(self, x):
        return self.resnet(x)
