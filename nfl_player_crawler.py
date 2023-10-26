import json
import requests
from bs4 import BeautifulSoup 

def crawl_nfl_roster(url, teams):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}
    players = {}
    for team in teams:
        resp = requests.get(url + team, headers=headers)

        #http_respone 200 means OK status 
        if resp.status_code==200: 
            print("Successfully opened the web page")
        else:
             print("Failed opened the web page")
             return

        soup = BeautifulSoup(resp.text,'html.parser')

        offense = soup.find("div",{"class":"ResponsiveTable Offense"})

        name = ""
        for i, oPlayer in enumerate(offense.findAll("td")):
                if i == 0:
                        continue
                mod = i % 8
                match mod:
                        case 0:
                            continue
                        case 1:
                            num = ""
                            if oPlayer.text[-2].isnumeric():
                                num =  oPlayer.text[-2:]
                            else:
                                num =  oPlayer.text[-1:]
                            name = oPlayer.text[:-len(num)]
                            if name in players.keys():
                                 name = name + " " + team.split("/")[0].upper()
                            players[name] = {}
                            players[name]["num"] = num
                            players[name]["team"] = team.split("/")[0]
                        case 2:
                            players[name]["pos"] = oPlayer.text
                        case 3:
                            players[name]["age"] = oPlayer.text
                        case 4:
                            players[name]["height"] = oPlayer.text
                        case 5:
                            players[name]["weight"] = oPlayer.text 
                        case 6:
                            players[name]["exp"] = oPlayer.text
                        case 7:
                            players[name]["college"] = oPlayer.text

        defense = soup.find("div",{"class":"ResponsiveTable Defense"})

        for i, dPlayer in enumerate(defense.findAll("td")): 
                if i == 0:
                        continue
                mod = i % 8
                match mod:
                        case 0:
                            continue
                        case 1:
                            num = ""
                            if dPlayer.text[-2].isnumeric():
                                num =  dPlayer.text[-2:]
                            else:
                                num =  dPlayer.text[-1:]
                            name = dPlayer.text[:-len(num)]
                            if name in players.keys():
                                  name = name + " " + team.split("/")[0].upper()
                            players[name] = {}
                            players[name]["num"] = num
                            players[name]["team"] = team.split("/")[0]
                        case 2:
                            players[name]["pos"] = dPlayer.text
                        case 3:
                            players[name]["age"] = dPlayer.text
                        case 4:
                            players[name]["height"] = dPlayer.text
                        case 5:
                            players[name]["weight"] = dPlayer.text 
                        case 6:
                            players[name]["exp"] = dPlayer.text
                        case 7:
                            players[name]["college"] = dPlayer.text
    with open("nfl_players.json", "w") as outfile: 
        json.dump(players, outfile, indent = 4)

nfl_teams = [
     "buf/buffalo-bills",
     "mia/miami-dolphins",
     "ne/new-england-patriots",
     "nyj/new-york-jets",
     "kc/kansas-city-chiefs",
     "den/denver-broncos",
     "lv/las-vegas-raiders",
     "lac/los-angeles-chargers",
     "bal/baltimore-ravens",
     "cin/cincinnati-bengals",
     "cle/cleveland-browns",
     "pit/pittsburgh-steelers",
     "hou/houston-texans",
     "ind/indianapolis-colts",
     "jax/jacksonville-jaguars",
     "ten/tennessee-titans",
     "dal/dallas-cowboys",
     "nyg/new-york-giants",
     "phi/philadelphia-eagles",
     "wsh/washington-commanders",
     "ari/arizona-cardinals",
     "lar/los-angeles-rams",
     "sf/san-francisco-49ers",
     "sea/seattle-seahawks",
     "chi/chicago-bears",
     "det/detroit-lions",
     "gb/green-bay-packers",
     "min/minnesota-vikings",
     "atl/atlanta-falcons",
     "car/carolina-panthers",
     "no/new-orleans-saints",
     "tb/tampa-bay-buccaneers"
]

crawl_nfl_roster("https://www.espn.com/nfl/team/roster/_/name/", nfl_teams)