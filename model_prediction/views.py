from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import torch
from torchvision import transforms, models
from PIL import Image
from .models import ResnetModel
import torch.nn as nn


def dashboard(request):
    return render(request, template_name='model_prediction/diagnose.html')


# Load the saved model
model = models.resnet101(pretrained=False)  # Assuming ResNet-101

# Modify the final fully connected layer for the number of classes in your dataset
num_classes = 8  # Adjust this based on the number of classes in your dataset
model.fc = torch.nn.Linear(model.fc.in_features, num_classes)

# Load the saved model state dictionary
checkpoint_path = r'D:\Sample\SkinLife\model_prediction\static\model_prediction\highacc.pth'
checkpoint = torch.load(checkpoint_path, map_location=torch.device('cpu'))
model.load_state_dict(checkpoint['model_state_dict'])

# Set the model to evaluation mode
model.eval()

# Define the transformation for the input image
transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])
def model_predictor(request):
    if request.method == 'POST':
        image_file = request.FILES.get('image')

        if image_file:
            # Load and preprocess the input image
            image = Image.open(image_file)
            image_tensor = transform(image).unsqueeze(0)  # Add batch dimension

            # Move the model to the same device as the input tensor
            device = torch.device('cpu')  # Use CPU for inference
            model.to(device)
            image_tensor = image_tensor.to(device)

            # Use the model to predict the class
            with torch.no_grad():
                output = model(image_tensor)
                probabilities = torch.softmax(output, dim=1)[0]  # Convert to probabilities
                predicted_class = torch.argmax(output, dim=1).item()

            return render(request, 'model_prediction/result.html', {'result': predicted_class})

    return render(request, 'model_prediction/diagnose.html')