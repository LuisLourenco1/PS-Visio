from abc import ABC, abstractmethod

class BaseObjectDetector(ABC):
    """Classe base abstrata para detecção de objetos."""

    @abstractmethod
    def detect_objects(self, frame):
        """Método abstrato para detectar objetos em um frame."""
        pass
