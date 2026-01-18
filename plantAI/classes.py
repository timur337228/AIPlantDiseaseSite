from pydantic import BaseModel
from typing import List

class Prediction(BaseModel):
    label: str
    confidence: float

class PlantDisplay(BaseModel):
    image_url: str
    predictions: List[Prediction]
    
    @property
    def top_prediction(self) -> Prediction:
        return sorted(self.predictions, key=lambda x: x.confidence, reverse=True)[0]
    

