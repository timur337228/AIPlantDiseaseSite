from torchvision import datasets, transforms
import gradio as gr
import pickle
import torch
from PIL import Image
from torchvision import transforms

classes = [
    "Яблоня — парша яблони", "Яблоня — чёрная гниль", "Яблоня — кедрово-яблочная ржавчина", "Яблоня — здоровое растение",
    "Черника — здоровое растение",
    "Вишня (включая кислую) — мучнистая роса", "Вишня (включая кислую) — здоровое растение",
    "Кукуруза — церкоспороз (серая пятнистость листьев)", "Кукуруза — обыкновенная ржавчина", "Кукуруза — северный гельминтоспориоз (северная пятнистость листьев)", "Кукуруза — здоровое растение",
    "Виноград — чёрная гниль", "Виноград — эска (чёрная корь)", "Виноград — пятнистость листьев (изариопсис)", "Виноград — здоровое растение",
    "Апельсин — хлороз цитрусовых (Хуанлунбин, озеленение цитрусовых)",
    "Персик — бактериальная пятнистость", "Персик — здоровое растение",
    "Сладкий перец — бактериальная пятнистость", "Сладкий перец — здоровое растение",
    "Картофель — ранняя фитофтора (альтернариоз)", "Картофель — поздняя фитофтора", "Картофель — здоровое растение",
    "Малина — здоровое растение",
    "Соя — здоровое растение",
    "Кабачок — мучнистая роса",
    "Клубника — ожог листьев", "Клубника — здоровое растение",p
    "Томат — бактериальная пятнистость", "Томат — ранняя фитофтора (альтернариоз)", "Томат — поздняя фитофтора", "Томат — листовая плесень",
    "Томат — септориоз листьев", "Томат — паутинный клещ (двухпятнистый)", "Томат — мишеневидная пятнистость", "Томат — вирус жёлтой курчавости листьев",
    "Томат — вирус табачной мозаики", "Томат — здоровое растение"
]

import torch.nn as nn

    
model = torch.load("efficientnet_leaf.pth", map_location="cpu", weights_only=False)
model.eval()

mean = [0.485, 0.456, 0.406]
std  = [0.229, 0.224, 0.225]

transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(mean, std)
])
def predict_image(img: Image.Image):
    x = transform(img).unsqueeze(0)

    with torch.no_grad():
        logits = model(x)
        probs = torch.softmax(logits, dim=1)[0]
        pred = {cls: prob for cls, prob in zip(classes, probs)}
        return pred

    return pred

image = gr.Image(type="pil")
label = gr.Label(num_top_classes=5)
demo = gr.Interface(fn=predict_image, inputs=image, outputs=label)
demo.launch()