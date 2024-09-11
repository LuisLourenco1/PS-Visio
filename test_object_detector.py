import pytest
import cv2
import numpy as np
from src.object_detector import ObjectDetector

@pytest.fixture
def sample_frame():
    """Cria um frame de exemplo para os testes."""
    return np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

@pytest.fixture
def object_detector():
    """Cria uma instância do ObjectDetector."""
    return ObjectDetector()

def test_detect_objects(object_detector, sample_frame):
    """Testa a detecção de objetos."""
    boxes = object_detector.detect_objects(sample_frame)
    assert isinstance(boxes, list), "A saída deve ser uma lista."
    for box in boxes:
        assert len(box) == 4, "Cada caixa deve ter 4 coordenadas."

def test_initialize_trackers(object_detector, sample_frame):
    """Testa a inicialização dos rastreadores."""
    boxes = [[100, 100, 200, 200], [300, 300, 400, 400]]
    object_detector.initialize_trackers(sample_frame, boxes)
    assert len(object_detector.trackers) == len(boxes), "O número de rastreadores deve ser igual ao número de caixas."

def test_update_trackers(object_detector, sample_frame):
    """Testa a atualização dos rastreadores."""
    boxes = [[100, 100, 200, 200], [300, 300, 400, 400]]
    object_detector.initialize_trackers(sample_frame, boxes)
    tracked_boxes = object_detector.update_trackers(sample_frame, frame_count=1, fps=30)
    assert isinstance(tracked_boxes, list), "A saída deve ser uma lista."
    for box in tracked_boxes:
        assert len(box) == 4, "Cada caixa rastreada deve ter 4 coordenadas."