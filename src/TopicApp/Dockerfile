FROM python:3.7.3

RUN pip install --upgrade pip

RUN pip install git+https://github.com/MaartenGr/BERTopic

COPY requirements.txt .

RUN pip install -U pip \
    && pip install --user -r requirements.txt

WORKDIR /app

COPY app .

EXPOSE 5002
CMD [ "python", "app.py" ]