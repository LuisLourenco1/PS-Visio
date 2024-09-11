## Processo Seletivo Visio

Este projeto é um sistema de processamento de vídeo que aplica correção de distorção, recorte, detecção e rastreamento de objetos em vídeos. Ele utiliza modelos de detecção de objetos baseados em redes neurais e algoritmos de rastreamento para identificar e seguir objetos em frames de vídeo.

### Funcionalidades

* **Correção de Distorção:** Corrige a distorção da lente da câmera.
* **Recorte de Frame:** Recorta a área de interesse do frame.
* **Redimensionamento de Frame:** Redimensiona o frame para uma dimensão específica.
* **Detecção de Objetos:** Detecta objetos em frames de vídeo usando um modelo de detecção de objetos.
* **Rastreamento de Objetos:** Rastreia objetos detectados ao longo dos frames.
* **Cálculo do Tempo de Atendimento:** Calcula o tempo total de atendimento de um cliente nos vídeos.

### Requisitos

* Python 3.9 ou superior
* Docker e Docker Compose

### Instalação e Uso

1. Clone o repositório:
```bash
git clone https://github.com/LuisLourenco1/PS-Visio.git
cd PS-Visio
```

2. Construa e suba o contêiner Docker
```bash
docker-compose build --no-cache
docker-compose up
```

3. Veja os vídeos de saída na pasta output_videos
