import os

class VideoFileHandler:
    """Classe para gerenciar a leitura e escrita de arquivos de vídeo."""
    
    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.ensure_output_folder_exists()

    def ensure_output_folder_exists(self):
        """Garante que a pasta de saída exista."""
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def get_video_files(self):
        """Obtém a lista de arquivos de vídeo na pasta de entrada."""
        return [f for f in os.listdir(self.input_folder) if f.endswith(('.mp4', '.avi', '.mov'))]

    def get_input_output_paths(self, video_file):
        """Obtém os caminhos de entrada e saída para um arquivo de vídeo."""
        input_path = os.path.join(self.input_folder, video_file)
        output_path = os.path.join(self.output_folder, video_file)
        return input_path, output_path
