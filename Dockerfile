FROM python:3.10.12-alpine3.18
RUN pip install requests && pip install telebot && pip install bs4
WORKDIR /usr/src/tbridgebot/
COPY . /usr/src/tbridgebot/
ARG BOT_API_KEY
ENV BOT_API_KEY=${BOT_API_KEY}
CMD python bot.py $BOT_API_KEY