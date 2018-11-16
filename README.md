# Spoorbot

Telegram bot which, at a given time, notifies you of any possible delays
for a journey with the Dutch Railways (NS).

You need a [Telegram Bot](https://core.telegram.org/bots) and
[NS API](https://www.ns.nl/en/travel-information/ns-api) credentials.

Runs in Docker and is configured using a YAML file.

## Example `config.yml`
```yaml
journeys:
  - from: Ut
    to: Amf
    cron: "0 8 * * mon,tue,wed,thu"
  - from: Amf
    to: Ut
    cron: "0 17 * * mon,tue,wed,thu"
```

Will notify you for journeys from Utrecht Centraal to Amersfoort, every
Monday to Thursday at 8AM, and from Amersfoort to Utrecht
Centraal, every day at 5PM.

For all station codes see
https://en.wikipedia.org/wiki/Railway_stations_in_the_Netherlands

## Example `docker run`
```bash
docker run --rm -d \
-e NS_LOGIN=ns_api_login \
-e NS_PASSWORD=ns_api_password \
-e TELEGRAM_TOKEN=bot_token \
-e TELEGRAM_CHAT_ID=bot_chat_id \
-v /path/to/config.yml:/app/config.yml \
-v /etc/timezone:/etc/timezone \
milanb/spoorbot
```

Initiate a conversation with your Telegram bot, then visit
https://api.telegram.org/bot{token}/getUpdates to find your
`TELEGRAM_CHAT_ID`.
