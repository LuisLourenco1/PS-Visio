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
    
    print("Inicializando processador de vídeo...")
    video_processor = VideoProcessor(camera_parameters, top_left, bottom_right)

    video_files = video_handler.get_video_files()
    print(f"Arquivos de vídeo encontrados: {video_files}")

    for video_file in video_files:
        input_path, output_path = video_handler.get_input_output_paths(video_file)
        print(f"Processando vídeo: {video_file}")
        video_processor.process_video(input_path, output_path)

    print("Processamento concluído.")

if __name__ == "__main__":
    main()