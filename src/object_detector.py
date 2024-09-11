import cv2
import torch
import PIL
from torchvision.models.detection import retinanet_resnet50_fpn_v2, RetinaNet_ResNet50_FPN_V2_Weights
from torchvision.transforms import functional as F
from src.base_object_detector import BaseObjectDetector

class ObjectDetector(BaseObjectDetector):
    """Classe para detecção de objetos usando RetinaNet com backbone ResNet-50-FPN V2."""

    def __init__(self, threshold=0.41, nms_threshold=0.4):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        weights = RetinaNet_ResNet50_FPN_V2_Weights.COCO_V1
        self.preprocessing = weights.transforms()
        self.model = retinanet_resnet50_fpn_v2(weights=weights).to(self.device)
        self.model.eval()
        self.threshold = threshold
        self.nms_threshold = nms_threshold
        self.trackers = []
        self.attendance_times = {}
        self.roi = None

    def set_roi(self, top_left, bottom_right):
        """Define a área de interesse (ROI) para a detecção de objetos."""
        self.roi = (top_left, bottom_right)

    def detect_objects(self, frame):
        """Detecta objetos em um frame."""
        # Converte o frame para o formato PIL
        img = PIL.Image.fromarray(frame)

        # Pré-processa o frame
        img = self.preprocessing(img)

        # Converte o frame para tensor e move para a GPU
        frame_tensor = img.unsqueeze(0).to(self.device)

        # Realiza a inferência
        with torch.no_grad():
            predictions = self.model(frame_tensor)

        # Move as predições de volta para a CPU
        predictions = [{k: v.to('cpu') for k, v in t.items()} for t in predictions]

        # Filtra as detecções com base no limiar de confiança
        pred_classes = [pred for pred in predictions[0]['labels'].numpy()]
        pred_scores = [score for score in predictions[0]['scores'].numpy()]
        pred_boxes = [box for box in predictions[0]['boxes'].numpy()]

        filtered_boxes = [box for box, score in zip(pred_boxes, pred_scores) if score >= self.threshold]
        filtered_scores = [score for score in pred_scores if score >= self.threshold]

        # Aplicar NMS
        if filtered_boxes:
            indices = cv2.dnn.NMSBoxes(
                bboxes=[list(map(int, box)) for box in filtered_boxes],
                scores=filtered_scores,
                score_threshold=self.threshold,
                nms_threshold=self.nms_threshold
            )
            indices = indices.flatten() if len(indices) > 0 else []
            filtered_boxes = [filtered_boxes[i] for i in indices]

        return filtered_boxes

    def initialize_trackers(self, frame, boxes):
        """Inicializa os rastreadores CSRT para os objetos detectados."""
        self.trackers = []
        for i, box in enumerate(boxes):
            tracker = cv2.TrackerCSRT_create() if hasattr(cv2, 'TrackerCSRT_create') else cv2.TrackerCSRT_create()
            bbox = (int(box[0]), int(box[1]), int(box[2] - box[0]), int(box[3] - box[1]))
            tracker.init(frame, bbox)
            self.trackers.append(tracker)
            self.attendance_times[i] = [0]  # Inicializa o tempo de atendimento para cada objeto

    def update_trackers(self, frame, frame_count, fps):
        """Atualiza a posição dos objetos rastreados em cada frame."""
        tracked_boxes = []
        for i, tracker in enumerate(self.trackers):
            success, bbox = tracker.update(frame)
            if success:
                x, y, w, h = [int(v) for v in bbox]
                tracked_boxes.append([x, y, x + w, y + h])
                # Atualiza o tempo de atendimento
                self.attendance_times[i].append(frame_count / fps)
        return tracked_boxes

    def draw_boxes(self, frame, boxes):
        """Desenha caixas delimitadoras no frame e exibe o tempo de atendimento."""
        for i, box in enumerate(boxes):
            cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 255, 0), 2)
            if i in self.attendance_times:
                # Calcula o tempo de atendimento
                attendance_time = self.attendance_times[i][-1] - self.attendance_times[i][0]
                # Exibe o tempo de atendimento
                cv2.putText(frame, f'Tempo: {attendance_time:.2f}s', (int(box[0]), int(box[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        return frame