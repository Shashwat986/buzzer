import sentiment as st
import json
import urllib

cache = {}

def search(client, term):
    response = client.api.search.tweets.get(q=term, count=50)
    return response.data.statuses

def getDirectConnections(statuses, term):
    directConnections = []
    for status in statuses:
        if term in status.user.name:
            continue
        if status.user.location:    
            url = "http://dev.virtualearth.net/REST/v1/Locations?query="+urllib.quote(status.user.location.encode('ascii','ignore'))+"&output=json&key=Ar31XPc8UKrmZMDPsEVNjdAcz4yyfLtrqAkSKrNnd-RQVpFUqz4xZH1UqqTOraQI"
            r=st.connect(url)
            try:
                d = json.loads(r)
            except:
                d=r
        try:
            lt = d['resourceSets'][0]['resources'][0]['point']['coordinates'][0]
        except: lt = ""

        try:
            lng = d['resourceSets'][0]['resources'][0]['point']['coordinates'][1]
        except:
            lng = ""
        
        dConn = dict(text=status.text, name=status.user.name, lat=lt, long=lng, location=status.user.location, userid=status.user.id_str, sentiment=st.sentiment(status.text, term), weight=status.user.followers_count)
        directConnections.append(dConn)
    return directConnections

def getFollowers(client, userid):
    count = 0
    idlist = ""
    ids = client.api.followers.ids.get(user_id=userid).data.ids
    for id in ids:
        if count == 100:
            break
        idlist = idlist + ',' + str(id)
        count+=1
    response = client.api.users.lookup.get(user_id=idlist)
    return response.data

def extractLocations(users):
    return [ i.location for i in users if i.location != ""]
    
def getSecondaryFollowerLocations(client, users) :
    locations = {}
    count = 0
    for user in users:
        if count == 20:
            break
        followers = getFollowers(client, user['userid'])
        x = extractLocations(followers)
        locations[user['userid']] = x
        count += 1
    return locations

def getDirectInfo(client, term):
    if 'direct'+term in cache:
        return cache['direct'+term]
        
    results = search(client, term)
    dConns = getDirectConnections(results, term)
    dConns = sorted(dConns, key = lambda ky: ky['weight'], reverse=True) 
    cache['direct'+term] = dConns
    return dConns

def getSecondaryInfo(client, term):
    if 'sec'+term in cache:
        return cache['sec'+term]    
    
    dConns = getDirectInfo(client, term)
    locations = getSecondaryFollowerLocations(client, dConns)
    dloc = {}
    for k, val in locations.iteritems():
        vv=[]
        for i in dConns:
            if i['userid']==k:
                v1,v2 = i['lat'], i['long']
                break
        for elem in val:
            url = "http://dev.virtualearth.net/REST/v1/Locations?query="+urllib.quote(elem.encode('ascii','ignore'))+"&output=json&key=Ar31XPc8UKrmZMDPsEVNjdAcz4yyfLtrqAkSKrNnd-RQVpFUqz4xZH1UqqTOraQI"
            r = st.connect(url)
            try:
                d = json.loads(r)
            except:
                d=r
        try:
            lt = d['resourceSets'][0]['resources'][0]['point']['coordinates'][0]
        except: lt = ""
        try:
            lng = d['resourceSets'][0]['resources'][0]['point']['coordinates'][1]
        except: lng = ""

        vv.append([lt,lng])

        dloc[str(v1,v2)]=vv

    cache['sec'+term] = dloc
    return dloc
    
def getInfo(client, term):
    results = search(client, term)
    dConns = getDirectConnections(results, term)
    return dConns


