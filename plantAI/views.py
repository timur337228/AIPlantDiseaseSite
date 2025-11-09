from django.shortcuts import render
from .forms import PlantForm
from gradio_client import Client, handle_file
from PIL import Image


def resize_image(file):
    img = Image.open(file)
    img.thumbnail((256, 256))
    img.save(file)

def get_out_model(img_path):
    client = Client("TimurMixx/PlantDisease")
    resize_image(img_path)
    predicts = client.predict(
        img=handle_file(img_path),
        api_name="/predict",
    )
    confidences = predicts['confidences']
    sorted_conf = sorted(confidences, key=lambda x: x['confidence'], reverse=True)
    return sorted_conf

def predict_plant(request):
    if request.method == "POST":
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            plant = form.save()
            predicts = get_out_model(plant.image.path)
            plant.prediction=predicts
            if request.user.is_authenticated:
                plant.user = request.user
                plant.save()
            return render(request, "plantAI/see_plant.html", {"plant": plant})
    else:
        form = PlantForm()
    return render(request, "plantAI/add_plant.html", {"form": form})