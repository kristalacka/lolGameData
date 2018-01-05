import requests, json, datetime

#records the initial game data
def record_data(game, date):
    with open('data.json', 'r') as f:
        data = json.load(f)
    try:
        data[date].append(game)
    except KeyError:
        data.update({date: [game]})
    return data

#logs the summoner info and prints it out
def sum_info(sum_ids, endpoint, api_key, data, date):
    path_to_sum0 = '/lol/summoner/v3/summoners/'
    path_to_league = '/lol/league/v3/positions/by-summoner/'
    number = 'team 1'
    for team, sums in sum_ids.items():
        for i in sums:
            summoner = requests.get('%s%s%s?api_key=%s'%(endpoint, path_to_sum0, i, api_key)).json()
            league_info = requests.get('%s%s%s?api_key=%s'%(endpoint, path_to_league, i, api_key)).json()
            info = summoner.copy()
            try:
                info.update(league_info[0])
            except IndexError:
                pass
            try:
                data[date][len(data[date])-1][number].append(info)
            except KeyError:
                data[date][len(data[date])-1][number] = [info]
            try:
                print('%s:\t%s\t%s/%s\t%s %s'%(summoner['name'], summoner['summonerLevel'], league_info[0]['wins'], league_info[0]['losses'], league_info[0]['tier'], league_info[0]['rank']))
            except IndexError:
                print('%s:\t%s\tno league info'%(summoner['name'], summoner['summonerLevel']))
        number = 'team 2'
        print('\n')
    return data

#saves the final game data to the file
def save(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)  
    input()

def main():
    with open('config.ini', 'r') as f:
        api_key = f.read()
    endpoint = 'https://eun1.api.riotgames.com'
    path_to_sum = '/lol/summoner/v3/summoners/by-name/'
    sum_name = 'BoxofJuice'
    summoner = requests.get('%s%s%s?api_key=%s'%(endpoint, path_to_sum, sum_name, api_key)).json()
    sum_id = summoner['id'] #gets the summoner id for the game search
    path_to_game = '/lol/spectator/v3/active-games/by-summoner/%s'%sum_id
    game = requests.get('%s%s?api_key=%s'%(endpoint, path_to_game, api_key)).json()
    participants = game['participants'] #get list of players' summoner IDs
    sum_ids = {}
    for i in participants:
        try:
            sum_ids[i['teamId']].append(i['summonerId'])
        except KeyError:
            sum_ids[i['teamId']] = [i['summonerId']]
    now = datetime.datetime.now()
    date = str(now)[:10]
    data = record_data(game, date)
    data = sum_info(sum_ids, endpoint, api_key, data, date)
    save(data)

main()
