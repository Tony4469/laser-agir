FROM continuumio/miniconda3:latest
RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  build-essential checkinstall curl wget bzip2

WORKDIR /app

RUN pip install flask flask_restful gunicorn requests rq faiss transliterate

RUN conda install faiss-cpu -c pytorch
RUN conda install pytorch-cpu torchvision-cpu -c pytorch

COPY . /app

CMD gunicorn laser-agir:app --log-level debug

ENV LASER_AGIR /app