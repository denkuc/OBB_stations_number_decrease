import json
import pandas as pd
import urllib.request
import codecs

reader = codecs.getreader("utf-8")

def get_json_url(lat,long,type):
    url='https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+str(lat)+','+str(long)+'&radius=100&type='+type+'_station&key=AIzaSyBQ2TfoexH2vrMQRievma4LrnBtVxeZCXQ'

    return str(url)

def if_na(x):
    if x == None: value="nA"
    else: value=x
    return value

file = pd.read_csv('sample10stations.csv')
sample=pd.DataFrame(file)
bus_name=[]
bus_type=[]
train_name=[]
train_type=[]
links=[]
sum1=0
station_types=['bus','train']
for index, row in sample.iterrows():
        #json_file = urllib.request.urlopen('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=47.590078999999996,8.565846&radius=100&type=bus_station&key=AIzaSyBQ2TfoexH2vrMQRievma4LrnBtVxeZCXQ')
    BND = []
    BTD = []
    TND = []
    TTD = []
    for type in station_types:
        json_url = get_json_url(row['latitude'], row['longitude'], type)
        json_pandas = pd.get_json(json_url)
        json_file = urllib.request.urlopen(json_url)
        json_array = json.load(reader(json_file))
        results = json_array["results"]
        links.append(results)
        for i in results:
            if type == 'bus':
                BTD.append(i["types"])
                BND.append(i["name"])
            elif type == 'train':
                TND.append(i["name"])
                TTD.append(i["types"])
    bus_name.append(BND)
    bus_type.append(BTD)
    train_name.append(TND)
    train_type.append(TTD)

sample["bus_name"]=bus_name
sample["bus_type"]=bus_type
sample["train_name"]=train_name
sample["train_type"]=train_type


sample.to_csv('export.csv',index=False,encoding='utf-16',sep='$')