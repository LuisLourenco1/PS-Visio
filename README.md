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

### Bônus

#### Questão 1

**1. Estimativa do custo diário de processamento**

a) Calcular a quantidade total de frames
* 100 horas de vídeo por dia, com 15 FPS
* Total de frames = 100 horas x 3600 segundos por hora x 15 FPS = **5.400.000 frames por dia**

b) Calcular o tempo necessário para processar esses frames
* O modelo processa 250 FPS utilizando a GPU
* Tempo necessário para processar: 5.400.000 frames / 250 FPS = 21.600 segundos
* Convertendo para horas: 21.600 / 3600 = **6 horas**

c) Estimar o custo da GPU
* O tempo necessário para processar os 5.400.000 frames é de 6 horas
* Custo da GPU (NVIDIA Tesla T4) por 6 horas = 6 x R$1.00 = **R$6.00**

d) Estimar o custo de CPU e RAM
* Vamos assumir que o processamento também utiliza 1 CPU e 4GB de RAM, que são estimativas comuns em cenários de processamento com GPU
* Custo de 1 CPU por 6 horas = 6 x R$0.10 = **R$0.60**
* Custo de 4GB de RAM por 6 horas = 6 x 4 x R$0.01 = **R$0.24**

**Custo total diário:**
* GPU: R$6.00
* CPU: R$0.60
* RAM: R$0.24

**Custo total diário = R$6.00 + R$0.60 + R$0.24 = R$6.84**

**2. Alterações para reduzir o custo**

Para reduzir o custo de processamento, algumas estratégias podem ser consideradas:

* Reduzir a resolução ou taxa de quadros dos vídeos de entrada: Processar vídeos com uma menor resolução ou reduzir a taxa de quadros (FPS) pode diminuir o número de frames processados e, consequentemente, o tempo necessário para processar
* Utilizar GPUs de menor custo ou otimizadas para IA: Se o modelo de detecção puder ser acelerado por GPUs com menor custo por hora (como a NVIDIA A100 ou outras opções), é possível reduzir o custo
* Batch processing (processamento em lotes): Dependendo do modelo, processar vários frames em lote em vez de um por vez pode melhorar a eficiência, aproveitando melhor a capacidade da GPU e diminuindo o tempo de uso
* Utilizar um pipeline de pré-processamento eficiente: Se houver tarefas que possam ser realizadas sem o uso da GPU, mover esses passos para um pipeline em CPU pode reduzir a carga da GPU

**3. Estimativa do novo custo diário**

Vamos supor que, com otimizações como a redução da taxa de quadros para 10 FPS (ainda garantindo a qualidade necessária para detecção) e melhorias no pipeline, conseguimos reduzir o total de frames processados por dia

a) Novo cálculo com 10 FPS
* 100 horas de vídeo por dia, agora com 10 FPS
* Total de frames = 100 horas x 3600 segundos por hora x 10 FPS = **3.600.000 frames por dia**

b) Calcular o novo tempo necessário para processar os frames
* O modelo processa 250 FPS utilizando a GPU
* Tempo necessário para processar = 3.600.000 frames / 250 FPS = 14.400 segundos
* Convertendo para horas: 14.400 / 3600 = **4 horas**

c) Estimar o novo custo de GPU, CPU e RAM
* GPU: 4 horas de utilização = 4 x R$1.00 = R$4.00
* CPU: 4 horas de utilização = 4 x R$0.10 = R$0.40
* RAM (4GB): 4 horas de utilização = 4 x 4 x R$0.01 = R$0.16

**Novo custo total diário:**
* GPU: R$4.00
* CPU: R$0.40
* RAM: R$0.16

**Novo custo total diário = R$4.00 + R$0.40 + R$0.16 = R$4.56**

**Conclusão**
* Custo original: R$6.84 por dia.
* Novo custo após otimizações: R$4.56 por dia.

**Redução de 33% do valor**


#### Questão 2

Foram implementados testes unitários, utilizando PyTest, em uma região crítica do projeto que é a de Detecção de Objetos

Para rodar os testes, basta rodar no terminal:
```bash
pytest test_object_detector.py
```
