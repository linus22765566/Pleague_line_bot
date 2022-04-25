# Pleague_line_bot
This is a linebot using line-bot-sdk & beautifulsoup to get latest information of P+ league.
Cause I'm P+ fans, so all the function is designed for my daily need.
Also, if you want, just clone the project, then request a PR, contributor is welcome!! :)

below is bot's QR code

![QR_code](https://user-images.githubusercontent.com/71446199/164895289-32140182-9ada-4d1f-9793-0dbf0c5d4ce2.png)


## how it work
### in json folder:
Here's template of all flex message used by bot.
Because different template is used in different function, and they are too long to be init in app_core.py.
So I just seperate them in a folder, to read them when needed.

### in app_core.py:
Here's the main part of the bot. Dealing with the request from line user, init the bot with token here, and reply message is also write in method here.

### in update_game_info.py:
Here's all of the function implement, including getting videos url of different games, getting scoreboard of games, and also teams information here.

### in img folder:
Just image used in bot richmenu. Not related to coding.
