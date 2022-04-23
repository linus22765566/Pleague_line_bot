import requests
from bs4 import BeautifulSoup
import json

def highlight_yt(game_number):    
    # to find hightlight on Youtube
    game_number += 125
    response = requests.get("https://pleagueofficial.com/video")
    allinfo = BeautifulSoup(response.text, "html.parser")
    past_games = allinfo.find(id = "video-"+str(game_number))
    return (past_games['href'])

def livestream_yt(game_number):
    # to find hightlight on Youtube
    game_number += 72
    response = requests.get("https://pleagueofficial.com/game/"+str(game_number))
    allinfo = BeautifulSoup(response.text, "html.parser")
    past_games = allinfo.find("a",class_="colorBB986C btn btn-primary btn-pill fs14 btn-sm mb-1 mr-2 pr-4 pl-4")
    return (past_games['href'])

def update_teams():
    # do crawler first
    response = requests.get("https://pleagueofficial.com/")
    allinfo = BeautifulSoup(response.text, "html.parser")
    teams_in_html = allinfo.find_all("tr", class_="bg-deepgray text-light")
    with open('json/teams_info.json') as f:
        allteams = json.load(f)

    # 爬蟲更新tems_info內資料
    for i in range(len(allteams["teams"])):
        for eachteam in teams_in_html:
            if(allteams["teams"][i]["Team_name"] == eachteam.find("td", class_="font-weight-bold").getText()):
                allteams["teams"][i]["rank"] = eachteam.find("th").getText()
                allteams["teams"][i]["win_or_lose"] = eachteam.find_all("td")[-1].getText()
                break
    # carousel內元素
    all_team_info = []
    for i in range(len(allteams["teams"])):
        with open('json/teams_template.json') as template:
            each_team = json.load(template)
        each_team["hero"]["url"] = allteams["teams"][i]["image"]
        each_team["body"]["contents"][0]["text"] = allteams["teams"][i]["Team_name"]
        each_team["body"]["contents"][2]["contents"][0]["contents"][1]["text"] = allteams["teams"][i]["home"]
        each_team["hero"]["action"]["uri"] = allteams["teams"][i]["official_website"]
        # 聯盟排名
        each_team["body"]["contents"][1]["contents"].append(allteams["others"]["ranking"])
        each_team["body"]["contents"][1]["contents"].append(allteams["others"]["number"+allteams["teams"][i]["rank"]])

        

        # 連勝場數
        if(allteams["teams"][i]["win_or_lose"][0] == 'W'):
                each_team["body"]["contents"][1]["contents"].append(allteams["others"]["winning"])
        else:
            each_team["body"]["contents"][1]["contents"].append(allteams["others"]["losing"])
        each_team["body"]["contents"][1]["contents"].append(allteams["others"]["number"+allteams["teams"][i]["win_or_lose"][2]])
        each_team["body"]["contents"][1]["contents"].append(allteams["others"]["games"])
        
        # 連勝星星數
        for j in range(int(allteams["teams"][i]["win_or_lose"][2])):
            if(allteams["teams"][i]["win_or_lose"][0] == 'W'):
                each_team["body"]["contents"][1]["contents"].append(allteams["others"]["win_start"])
            else:
                each_team["body"]["contents"][1]["contents"].append(allteams["others"]["lose_start"])

        each_team["footer"]["contents"][0]["action"]["uri"] = allteams["teams"][i]["official_website"]
        each_team["footer"]["contents"][1]["action"]["uri"] = allteams["teams"][i]["Youtube_channel"]
        all_team_info.append(each_team)
    return all_team_info
    
def update_past_games():
    response = requests.get("https://pleagueofficial.com/schedule-regular-season")
    allinfo = BeautifulSoup(response.text, "html.parser")
    past_four_game = allinfo.find_all("div",class_="before-today")[-4:]
    past_gmaes_info = []
    for a_game in past_four_game:
        with open('json/games_past_template.json') as template:
            each_team = json.load(template)
        
        # 客/主場照片
        each_team["header"]["contents"][0]["url"] = a_game.find_all("img",class_="w105")[0]['src']
        each_team["header"]["contents"][2]["url"] = a_game.find_all("img",class_="w105")[1]['src']
        # 客/主場比數
        each_team["hero"]["contents"][0]["text"] = a_game.find_all("h6",class_="fs20")[0].getText()
        each_team["hero"]["contents"][2]["text"] = a_game.find_all("h6",class_="fs20")[1].getText()
        # G__ & 在哪打比賽
        each_team["body"]["contents"][0]["contents"][0]["text"] = a_game.find("h5",class_="fs14 mb-2").getText()
        each_team["body"]["contents"][0]["contents"][1]["text"] = a_game.find("h5",class_="fs12 mb-0").getText()
        game_number = a_game.find("h5",class_="fs14 mb-2").getText().replace("G","")

        # 進場人數
        each_team["body"]["contents"][1]["contents"][1]["text"] = a_game.find("div",class_="mt-3 mb-md-0 mb-3 fs12 text-center PC_only").getText()

        # 日期
        each_team["body"]["contents"][2]["contents"][0]["text"] = (a_game.find("div",class_="col-lg-1 col-12 text-center align-self-center match_row_datetime").getText()).replace('\n',' ')
        # 數據網址
        each_team["footer"]["contents"][1]["action"]["uri"] = 'https://pleagueofficial.com/game/'+str(int(game_number)+72)
        # 賽事精華
        each_team["footer"]["contents"][0]["action"]["uri"] = highlight_yt(int(game_number))
    
        past_gmaes_info.append(each_team)
    return past_gmaes_info

def update_future_games():
    response = requests.get("https://pleagueofficial.com/schedule-regular-season")
    allinfo = BeautifulSoup(response.text, "html.parser")
    future_four_game = allinfo.find_all("div",class_="is-future",limit = 4)
    future_gmaes_info = []
    for a_game in future_four_game:
        with open('json/games_future_template.json') as template:
            each_team = json.load(template)
        
        # 客/主場照片
        each_team["header"]["contents"][0]["url"] = a_game.find_all("img",class_="w105")[0]['src']
        each_team["header"]["contents"][2]["url"] = a_game.find_all("img",class_="w105")[1]['src']
        # 客/主場比數
        each_team["hero"]["contents"][0]["text"] = a_game.find_all("h6",class_="fs20")[0].getText()
        each_team["hero"]["contents"][2]["text"] = a_game.find_all("h6",class_="fs20")[1].getText()
        # G__ & 在哪打比賽
        each_team["body"]["contents"][0]["contents"][0]["text"] = a_game.find("h5",class_="fs14 mb-2").getText()
        each_team["body"]["contents"][0]["contents"][1]["text"] = a_game.find("h5",class_="fs12 mb-0").getText()
        game_number = a_game.find("h5",class_="fs14 mb-2").getText().replace("G","")

        # 進場人數
        each_team["body"]["contents"][1]["contents"][1]["text"] = a_game.find("div",class_="mt-3 mb-md-0 mb-3 fs12 text-center PC_only").getText()

        # 日期
        each_team["body"]["contents"][2]["contents"][0]["text"] = (a_game.find("div",class_="col-lg-1 col-12 text-center align-self-center match_row_datetime").getText()).replace('\n',' ')
        # 購票網址
        each_team["footer"]["contents"][1]["action"]["uri"] = 'https://pleagueofficial.com'+a_game.find_all("a",class_="fs12 mt-md-2 my-0 py-0 d-md-block d-inline mr-2")[1]['href']
        # 直播網址
        each_team["footer"]["contents"][0]["action"]["uri"] = livestream_yt(int(game_number))
    
        future_gmaes_info.append(each_team)
    return future_gmaes_info

def main():
    print('hello! I\'m main')
if __name__ == '__main__':
    main()
