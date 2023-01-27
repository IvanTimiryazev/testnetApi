FROM python:3.8

WORKDIR /app

RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app
RUN chmod a+x boot.sh

ENV FLASK_APP testnet.py

EXPOSE 5005
ENTRYPOINT ["./boot.sh"]
