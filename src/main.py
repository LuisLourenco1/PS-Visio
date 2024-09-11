import cv2
from src.camera_parameters import CameraParameters
from src.video_file_handler import VideoFileHandler
from src.video_processor import VideoProcessor

def main():
    input_folder = "input_videos"
    output_folder = "output_videos"
    top_left = (128, 288)
    bottom_right = (800, 928)

    print("Carregando parâmetros da câmera...")
    camera_parameters = CameraParameters()

    print("Inicializando manipulador de arquivos de vídeo...")
    video_handler = VideoFileHandler(input_folder, output_folder)

    video_files = video_handler.get_video_files()
    print(f"Arquivos de vídeo encontrados: {video_files}")

    for video_file in video_files:
        input_path, output_path = video_handler.get_input_output_paths(video_file)
        print(f"Processando vídeo: {video_file}")

        # Abra o vídeo para obter a largura e altura
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            print(f"Erro ao abrir o vídeo: {input_path}")
            continue
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()

        # Calcule as coordenadas da ROI
        # ((128, 50), (320, 475))
        detection_roi = ((width // 10, 50), (width // 4, height-485))
        print(f"ROI selecionada: {detection_roi}")

        # Inicialize o processador de vídeo com a ROI calculada
        video_processor = VideoProcessor(camera_parameters, top_left, bottom_right, detection_roi)
        video_processor.process_video(input_path, output_path)

    print("Processamento concluído.")

if __name__ == "__main__":
    main()