FROM python:3.11.0

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /app

#install the linux packages, since these are the dependencies of some python packages
RUN  apk update \
	&& apk add --no-cache \
    gcc \
	&& pip install --upgrade pip

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ ./

# CMD ["sh", "entrypoint.sh"]