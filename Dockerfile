FROM python:slim
WORKDIR /usr/src/saline_bot
COPY ./source .

RUN pip install -r requirements.txt
CMD ["python", "bot.py"]