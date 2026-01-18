from django.shortcuts import render
from .forms import PlantForm
from .models import PlantInfo
from gradio_client import Client, handle_file
from PIL import Image
from .classes import PlantDisplay, Prediction

def normalize_plant_data(plant_data: dict) -> PlantDisplay:
    image_path = plant_data["image_path"]
    image_url = image_path.replace("\\", "/")
    if "media" in image_url:
        image_url = "/" + image_url.split("media")[-1].lstrip("/\\")
    
    return PlantDisplay(
        image_url=image_url,
        predictions=[Prediction(**pred) for pred in plant_data['prediction']],
    )
    
    

    

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
    sorted_conf = sorted(
        [{'label': item['label'], 'confidence': item['confidence'] * 100} 
            for item in confidences],
        key=lambda x: x['confidence'],
        reverse=True
    )
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
            else:
                if "temporary_plants" not in request.session:
                    request.session["temporary_plants"] = []
                request.session.setdefault("temporary_plants", []).append({
                    "image_path": plant.image.path,
                    "prediction": predicts,
                })
                plant.delete()
                request.session.modified = True
            return render(request, "plantAI/see_plant.html", {"plant": plant})
    else:
        form = PlantForm()
    return render(request, "plantAI/add_plant.html", {"form": form})


def get_my_preds(request):
    if request.user.is_authenticated:
        plants = PlantInfo.objects.filter(user=request.user).order_by("-created_at")
    else:
        plants = request.session.get("temporary_plants", [])
        plants = [normalize_plant_data(plant) for plant in plants]
        plants = list(reversed(plants))
            
    return render(request, "plantAI/get_my_preds.html", {"plants": plants}) 