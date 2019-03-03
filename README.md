# RootMe API 

URL: [https://root-me-api.hackademint.org](https://root-me-api.hackademint.org)

## Self deployment

```bash
 docker-compose up 
```

## List of endpoints

Some endpoints need a valid RootMe username you can extract from the URL of your profile. \
Here is an example with https://www.root-me.org/zTeeed-115405 --> zTeeed-115405


- [https://root-me-api.hackademint.org/](https://root-me-api.hackademint.org/)
- [https://root-me-api.hackademint.org/v1](https://root-me-api.hackademint.org/v1)
- [https://root-me-api.hackademint.org/v1/challenges](https://root-me-api.hackademint.org/v1/challenges)
- [https://root-me-api.hackademint.org/v1/zTeeed-115405](https://root-me-api.hackademint.org/v1/zTeeed-115405)
- [https://root-me-api.hackademint.org/v1/zTeeed-115405/profile](https://root-me-api.hackademint.org/v1/zTeeed-115405/profile)
- [https://root-me-api.hackademint.org/v1/zTeeed-115405/contributions](https://root-me-api.hackademint.org/v1/zTeeed-115405/contributions)
- [https://root-me-api.hackademint.org/v1/zTeeed-115405/details](https://root-me-api.hackademint.org/v1/zTeeed-115405/details)
- [https://root-me-api.hackademint.org/v1/zTeeed-115405/ctf](https://root-me-api.hackademint.org/v1/zTeeed-115405/ctf)
- [https://root-me-api.hackademint.org/v1/zTeeed-115405/stats](https://root-me-api.hackademint.org/v1/zTeeed-115405/stats)

## Discord Bot

### Install

You need to create a discord bot here: [https://discordapp.com/developers/applications/](https://discordapp.com/developers/applications/), get a token and replace it in ./bot_discord/bot/constants.py (you can use the public url api or your own instance)

```bash
cd ./bot_discord
apt install python3.5 python3.5-pip
pip3 install -r requirements.txt
python3.5 main.py
```


### Features
