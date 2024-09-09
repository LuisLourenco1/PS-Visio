# Use a imagem base oficial do Python
FROM python:3.9-slim

# Instale as dependências do sistema necessárias para o OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo de dependências para o contêiner
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código para o contêiner
COPY src/ ./src/
COPY input_videos/ ./input_videos/
COPY output_videos/ ./output_videos/

# Adicione o diretório de trabalho ao PYTHONPATH
ENV PYTHONPATH=/app

# Defina o comando padrão para rodar o script principal
CMD ["python", "src/main.py"]