# RootMe API 

URL: [https://root-me-api.hackademint.org](https://root-me-api.hackademint.org) \
BOT Discord: [link](https://discordapp.com/api/oauth2/authorize?client_id=523372231561314304&permissions=0&scope=bot)

## Description

[Root-Me](https://www.root-me.org/?lang=en) is a french platform that is the fast, easy, and affordable way to train your hacking skills. This website provides hundreds of challenges to train yourself in different and not simulated environments, offering you a way to learn a lot of hacking technics. \
It also provides dozens of virtual environments, accessible with a few clicks, to give you a realistic learning environment, without any limitation.

The purpose of this project is to provide an API to use 
[Root-Me](https://www.root-me.org/?lang=en) data, provide a discord bot fetching events and data from this API and to build a distributed system thanks to workers using [redis streams and consumer groups](https://redis.io/topics/streams-intro).

## How does it works ? 

When a client is making a request on the API, the server is checking if there is an existing data in an associated [redis key](https://redis.io/commands/getset). If not, the server is sending a task to workers through the appropriate [redis stream](https://redis.io/topics/streams-intro). If there is existing data, the API is checking if the last update is not too old (depends on `UPDATE_TIMEOUT` in [constants.py](https://github.com/zteeed/Root-Me-API/blob/master/api/api/constants.py)) and ask the workers for updates if necessary.

The form of the data is:

```
{
    'body': data,
    'last_update': timestamp_isoformat
}
```

The workers are permanently reading the streams, which are in the same [consumer group](https://redis.io/topics/streams-intro). You might read this script: [init.py](https://github.com/zteeed/Root-Me-API/blob/master/api/init.py).

When a worker receive a task, it makes HTTPS request to [Root-Me](https://www.root-me.org/?lang=en) website and parse the result into JSON format inside [redis keys](https://redis.io/commands/getset).

![](./images/schema.png)

## Before install

You need to create a discord bot here: [https://discordapp.com/developers/applications/](https://discordapp.com/developers/applications/), get a token and replace it in `./bot_discord/bot/constants.py`.


## Simple configuration (1 worker)

### Install

```bash
 docker-compose up -d
```

## Advanced configuration (1+ workers)

### Install

```bash
 docker-compose up -d
```

## [API]

Some endpoints need a valid RootMe username you can extract from the URL of your profile. \
Here is an example with https://www.root-me.org/zTeeed-115405 --> zTeeed-115405


- [https://root-me-api.hackademint.org/](https://root-me-api.hackademint.org/)
- [https://root-me-api.hackademint.org/v2](https://root-me-api.hackademint.org/v2)
- [https://root-me-api.hackademint.org/v2/challenges](https://root-me-api.hackademint.org/v2/challenges)
- [https://root-me-api.hackademint.org/v2/zTeeed-115405](https://root-me-api.hackademint.org/v2/zTeeed-115405)
- [https://root-me-api.hackademint.org/v2/zTeeed-115405/profile](https://root-me-api.hackademint.org/v2/zTeeed-115405/profile)
- [https://root-me-api.hackademint.org/v2/zTeeed-115405/contributions](https://root-me-api.hackademint.org/v2/zTeeed-115405/contributions)
- [https://root-me-api.hackademint.org/v2/zTeeed-115405/details](https://root-me-api.hackademint.org/v2/zTeeed-115405/details)
- [https://root-me-api.hackademint.org/v2/zTeeed-115405/ctf](https://root-me-api.hackademint.org/v2/zTeeed-115405/ctf)
- [https://root-me-api.hackademint.org/v2/zTeeed-115405/stats](https://root-me-api.hackademint.org/v2/zTeeed-115405/stats)

## [Discord Bot]


### Features

### events

Display new challenges solved by users from team.

![](./images/discord_event.png)

### help

Display available commands.

![](./images/discord_help.png)

### add_user/remove_user \<username\>

Add a user to team / Remove a user from team.

Extract the username from the RootMe profile link. \
Example with [https://www.root-me.org/zTeeed-115405?inc=info](https://www.root-me.org/zTeeed-115405?inc=info)

![](./images/discord_add_remove_user.png)

### scoreboard

Show team scoreboard.

![](./images/discord_scoreboard.png)

### categories

Show list of categories.

![](./images/discord_categories.png)

### category

Show list of challenges from a category.

![](./images/discord_category_cracking.png)

### today (\<username\>) 

Show challenges solved grouped by users for last day.

![](./images/discord_today.png)

### week (\<username\>) 

Show challenges solved grouped by users for last week.

![](./images/discord_week.png)

### who_solved \<challenge\>

Show who solved a specific challenge.

![](./images/discord_who_solved.png)

### diff \<username1\> \<username2\>
  
Show difference of solved challenges between two users.

![](./images/discord_diff1.png)

![](./images/discord_diff2.png)

### diff_with \<username\> 

Show difference of solved challenges between a user and all team.

### flush       

Flush all data from bot channel excepted events
