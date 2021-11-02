FROM python:3.8.3
ENV WORKSPACE=/mnt/www/api
RUN mkdir -p ${WORKSPACE}
ADD . ${WORKSPACE}
WORKDIR ${WORKSPACE}
EXPOSE 80

RUN apt-get update \
    && apt-get install -y \   
    python3-dev \
    libffi-dev \
    build-essential \
    && rm -rf /etc/apt/sources.list.d/*
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

ENTRYPOINT ["python", "./src/index.py"]