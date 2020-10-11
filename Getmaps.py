import requests
import pandas as pd
from tqdm import tqdm

API_KEY = '10392f3efda753a7f33b6db3fe5acbcbd9c13fee'


def savecsv(maplist):
    maplist.to_csv("maplist.csv")


def getmapinfo(start, end):
    beatmaplist = pd.DataFrame([], columns=["Beatmap_id", "Title", "Star Rating"])
    for mapid in tqdm(range(start, end + 1)):
        url_map = f'https://osu.ppy.sh/api/get_beatmaps?k={API_KEY}&b={mapid}&m=2&a=1'
        try:
            resp = requests.get(url_map)
        except requests.exceptions.ConnectionError:
            print("No Internet\n")
            return -1
        data = resp.json()
        # print(data)
        if not data:  # No this beatmap or not a ctb map
            continue
        mapinfo = data[0]
        if not mapinfo["approved"] == '1' and not mapinfo["approved"] == '2':  # Not a ranked beatmap
            continue
        beatmap = {
            "Beatmap_id": mapinfo['beatmap_id'],
            "Title": f"{mapinfo['title']}[{mapinfo['version']}]",
            "Star Rating": mapinfo['difficultyrating']
        }
        havefc = getscoreinfo(mapid)
        if havefc == -1:
            print(f'An error occured while getting score from {mapid}\n')
            return -1
        elif havefc == 1:
            continue
        else:
            beatmaplist = beatmaplist.append(pd.DataFrame(beatmap, index=[0]), ignore_index=True)
    print("Update succeded\n")
    savecsv(beatmaplist)
    return 0


def getscoreinfo(mapid):
    url_score = f'https://osu.ppy.sh/api/get_scores?k={API_KEY}&b={mapid}&m=2&a=1'
    try:
        resp = requests.get(url_score)
    except requests.exceptions.ConnectionError:
        print("No Internet\n")
        return -1  # Error
    data = resp.json()
    # print(data)
    for i in range(data.__len__()):
        if data[i]['perfect'] == '1':
            return 1  # FC
    return 0  # Not FC


if __name__ == "__main__":
    getmapinfo(int(input()), int(input()))
