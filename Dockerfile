FROM continuumio/miniconda3:latest
RUN apt-get update -y
RUN apt-get install -y build-essential checkinstall curl

# Adding wget and bzip2
RUN apt-get install -y wget bzip2

# RUN apt-get install -y libreadline-gplv2-dev libncursesw5-dev libssl-dev \
#     libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev
# RUN apt-get install -y apt-utils python3.6 python3-pip python3-dev
VOLUME /app

# WORKDIR /tmp

# RUN curl -O https://repo.continuum.io/archive/Anaconda3-5.0.1-Linux-x86_64.sh
# RUN bash Anaconda3-5.0.1-Linux-x86_64.sh -b
# RUN rm Anaconda3-5.0.1-Linux-x86_64.sh
# ENV PATH /home/ubuntu/anaconda3/bin:$PATH
# RUN which anaconda3

WORKDIR /app
# Updating Anaconda packages
RUN conda update conda
RUN conda update --all

RUN alias python=python3
RUN alias pip=pip3
RUN python --version
RUN pip --version
RUN pip install flask flask_restful gunicorn requests rq faiss

RUN conda install faiss-cpu -c pytorch
RUN conda install pytorch-cpu torchvision-cpu -c pytorch

# COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "laser-agir.py" ]