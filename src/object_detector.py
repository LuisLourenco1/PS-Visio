import cv2
import torch
from torchvision.models.detection import retinanet_resnet50_fpn_v2, RetinaNet_ResNet50_FPN_V2_Weights
from torchvision.transforms import functional as F
from src.base_object_detector import BaseObjectDetector

class ObjectDetector(BaseObjectDetector):
    """Classe para detecção de objetos usando RetinaNet com backbone ResNet-50-FPN V2."""
    
    def __init__(self, threshold=0.5):
        weights = RetinaNet_ResNet50_FPN_V2_Weights.COCO_V1
        self.model = retinanet_resnet50_fpn_v2(weights=weights)
        self.model.eval()
        self.threshold = threshold

    def detect_objects(self, frame):
        """Detecta objetos em um frame."""
        # Converte o frame de BGR para RGB usando OpenCV
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Converte o frame para tensor
        frame_tensor = F.to_tensor(frame_rgb).unsqueeze(0)
        
        # Realiza a inferência
        with torch.no_grad():
            predictions = self.model(frame_tensor)
        
        # Filtra as detecções com base no limiar de confiança
        pred_classes = [pred for pred in predictions[0]['labels'].cpu().numpy()]
        pred_scores = [score for score in predictions[0]['scores'].cpu().numpy()]
        pred_boxes = [box for box in predictions[0]['boxes'].cpu().numpy()]

        filtered_boxes = [box for box, score in zip(pred_boxes, pred_scores) if score >= self.threshold]
        
        return filtered_boxes
