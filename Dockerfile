FROM python:3.6-slim 
 
RUN apt-get update && apt-get install -y build-essential cmake git libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1 wget && rm -rf /var/lib/apt/lists/* 
 
WORKDIR /app 
 
RUN git clone https://github.com/terryli710/COVID_19_Rapid_Triage_Risk_Predictor.git . 
 
RUN pip install --no-cache-dir PyWavelets==1.1.1 
 
RUN pip install --no-cache-dir SimpleITK==2.0.2 numpy==1.19.5 pandas==1.1.0 scikit-learn==0.23.2 joblib==0.16.0 lightgbm==2.3.1 matplotlib==3.3.4 scipy==1.5.4 pillow==8.3.2 tqdm pykwalify==1.8.0 
 
RUN pip install --no-cache-dir pyradiomics==3.0.1 
 
RUN pip install torch==1.7.1+cpu torchvision==0.8.2+cpu -f https://download.pytorch.org/whl/torch_stable.html 
 
RUN mkdir -p /app/data /app/results /app/batch_scripts 
 
ENV PYTHONPATH=/app:$PYTHONPATH 
 
CMD ["bash"] 
