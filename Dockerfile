FROM python:3.11.0

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /app

#install the linux packages, since these are the dependencies of some python packages
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/* 

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ ./

# CMD ["sh", "entrypoint.sh"]