import cv2
from src.object_detector import ObjectDetector

class VideoProcessor:
    """Classe para processar vídeos, aplicando correção de distorção, crop, detecção e rastreamento de objetos."""

    def __init__(self, camera_parameters, top_left, bottom_right, detection_roi=None):
        self.camera_parameters = camera_parameters
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.object_detector = ObjectDetector()
        self.attendance_times = {}
        self.detection_roi = detection_roi
        if detection_roi:
            self.object_detector.set_roi(detection_roi[0], detection_roi[1])

    def undistort_frame(self, frame):
        """Aplica correção de distorção no frame."""
        return cv2.undistort(frame, self.camera_parameters.camera_matrix, self.camera_parameters.dist_coeffs)

    def crop_frame(self, frame):
        """Recorta o frame."""
        return frame[self.top_left[0]:self.bottom_right[0], self.top_left[1]:self.bottom_right[1]]

    def resize_frame(self, frame, size=(640, 480)):
        """Redimensiona o frame."""
        return cv2.resize(frame, size)

    def draw_boxes(self, frame, boxes):
        """Desenha caixas delimitadoras no frame."""
        return self.object_detector.draw_boxes(frame, boxes)

    def draw_roi(self, frame):
        """Desenha a ROI no frame."""
        if self.detection_roi:
            top_left, bottom_right = self.detection_roi
            cv2.rectangle(frame, top_left, bottom_right, (255, 0, 0), 2)
        return frame

    def process_video(self, input_path, output_path):
        """Processa um vídeo, aplicando correção de distorção, crop, detecção e rastreamento de objetos."""
        cap = cv2.VideoCapture(input_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = None

        frame_count = 0
        initialized = False
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            undistorted_frame = self.undistort_frame(frame)
            cropped_frame = self.crop_frame(undistorted_frame)
            resized_frame = self.resize_frame(cropped_frame)

            # Recorte o frame com base na ROI
            if self.detection_roi:
                roi_top_left, roi_bottom_right = self.detection_roi
                roi_frame = resized_frame[roi_top_left[1]:roi_bottom_right[1], roi_top_left[0]:roi_bottom_right[0]]
            else:
                roi_frame = resized_frame

            if not initialized:
                boxes = self.object_detector.detect_objects(roi_frame)
                self.object_detector.initialize_trackers(roi_frame, boxes)
                initialized = True
            else:
                tracked_boxes = self.object_detector.update_trackers(roi_frame, frame_count, fps)
                frame_with_boxes = self.draw_boxes(roi_frame, tracked_boxes)
                frame_with_roi = self.draw_roi(resized_frame)  # Desenha a ROI no frame original redimensionado
                if out is None:
                    height, width = frame_with_roi.shape[:2]
                    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
                out.write(frame_with_roi)

        cap.release()
        if out is not None:
            out.release()

        # Calcular o tempo de atendimento
        for person_id, times in self.object_detector.attendance_times.items():
            attendance_time = times[-1] - times[0]
            print(f"Pessoa {person_id} foi atendida por {attendance_time:.2f} segundos.")