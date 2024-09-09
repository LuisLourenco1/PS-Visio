import cv2
from src.object_detector import ObjectDetector

class VideoProcessor:
    """Classe para processar vídeos, aplicando correção de distorção, crop e detecção de objetos."""
    
    def __init__(self, camera_parameters, top_left, bottom_right):
        self.camera_matrix = camera_parameters.camera_matrix
        self.dist_coeffs = camera_parameters.dist_coeffs
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.object_detector = ObjectDetector()

    def undistort_frame(self, frame):
        """Aplica a correção de distorção a um frame."""
        return cv2.undistort(frame, self.camera_matrix, self.dist_coeffs)

    def crop_frame(self, frame):
        """Realiza o crop da região de interesse de um frame."""
        return frame[self.top_left[0]:self.bottom_right[0], self.top_left[1]:self.bottom_right[1]]

    def draw_boxes(self, frame, boxes):
        """Desenha caixas delimitadoras no frame."""
        for box in boxes:
            cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 255, 0), 2)
        return frame

    def process_video(self, input_path, output_path):
        """Processa um vídeo, aplicando correção de distorção, crop e detecção de objetos."""
        cap = cv2.VideoCapture(input_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        print(f"FPS do vídeo de entrada: {fps}")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = None

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            undistorted_frame = self.undistort_frame(frame)
            cropped_frame = self.crop_frame(undistorted_frame)
            boxes = self.object_detector.detect_objects(cropped_frame)
            frame_with_boxes = self.draw_boxes(cropped_frame, boxes)

            if out is None:
                height, width = frame_with_boxes.shape[:2]
                out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

            out.write(frame_with_boxes)

        cap.release()
        if out is not None:
            out.release()