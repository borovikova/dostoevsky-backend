FROM python:3
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app
EXPOSE 8000

RUN mkdir -p /vol/web/static

RUN adduser user
RUN chown -R user:user /vol
RUN chmod -R 755 /vol/web/
USER user