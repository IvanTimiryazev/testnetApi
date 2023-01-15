FROM python:3.8

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

COPY . /app
RUN chmod +x boot.sh

ENV FLASK_APP testnet.py

EXPOSE 5005

CMD ["./boot.sh"]
