# RootMe API 

URL: [https://root-me-api.hackademint.org](https://root-me-api.hackademint.org)

## Self deployment

### Using docker

```bash
 docker-compose up
```
### Alternative

- Install python3, python3-pip, install the dependencies `pip3 install -r api/requirements.txt`
- Launch the api `python3 api/main.py`
- Install varnish ([https://varnish-cache.org/releases/](https://varnish-cache.org/releases/) and replace the default config file in /etc/varnish/default.vcl by the file in varnish/config.vcl (update host to '0.0.0.0' and the port to the port where your flask API is running). Then you can use your application with varnish HTTP cache by making HTTP requests on port 6081.


> Varnish Cache is a web application accelerator also known as a caching
> HTTP reverse proxy. You install it in front of any server that speaks
> HTTP and configure it to cache the contents. Varnish Cache is really,
> really fast. It typically speeds up delivery with a factor of 300 -
> 1000x, depending on your architecture.


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

- today       (\<username\>) 
> Return challenges solved grouped by users for last day.
- week        (\<username\>) 
> Return challenges solved grouped by users for last week.
- add_user    \<username\> 
> Add a user to team into database.
- scoreboard  
> Show list of users from team.
- remove_user \<username\> 
> Remove a user from team in database.
- categories  
> Show list of categories.
- category    \<category\> 
> Show list of challenges from a category.
- who_solved  \<challenge\> 
> Return who solved a specific challenge.
- diff        \<username1\> \<username2\> 
> Return difference of solved challenges between two users.
- diff_with   \<username\> 
> Return difference of solved challenges between a user and all team.
- flush       
> Flush all data from bot channel excepted events
