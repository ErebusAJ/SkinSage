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
model = models.resnet101(pretrained=False)
num_classes = 19  # Adjust based on your number of classes
model.fc = nn.Linear(model.fc.in_features, num_classes)

model_path = r'D:/SkinDisease/SkinLife/model_prediction/static/model_prediction/resnet101_newmodel.pth'
checkpoint = torch.load(model_path, map_location=torch.device('cpu'))
model.load_state_dict(checkpoint)

# Set the model to evaluation mode
model.eval()

# Move the model to CPU
device = torch.device('cpu')
model.to(device)

# Define the image transformations
img_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])


def model_predictor(request):
    if request.method == 'POST':
        image_file = request.FILES.get('image')

        if image_file:
            image = Image.open(image_file)
            input_tensor = img_transforms(image).unsqueeze(0).to(device)

            # Load your ResNet model
            model = ResnetModel(num_classes=19)  # Replace YourModel with your actual ResNet model
            model.eval()

            with torch.no_grad():
                output = model(input_tensor)
                probabilities = torch.softmax(output, dim=1)[0]  # Get class probabilities
                predicted_class = torch.argmax(probabilities).item()
                print(predicted_class)

            return render(request, 'model_prediction/result.html',  {'result': predicted_class})


