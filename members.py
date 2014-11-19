import urllib.request
from bs4 import BeautifulSoup
import re
from pymongo import MongoClient

# FB Setup
tag = 'fbProfileBrowserListContainer'
groupId = "{insert group}"
cookieText = "{insert cookie}"

client = MongoClient()
coll = client[groupId].members
count = 0

def handleAdd(obj):
    user = dict()
    user['name'] = obj.a.text
    for d in obj.findAll("div"):
        if "fsl" in d["class"]:
            url = d.a["data-hovercard"]
            userid = midRegex('id=(.*?)&extraget', url)
            user['url'] = d.a['href']
            user['userid'] = userid
        if "_17tq" in d["class"]:
            user['occupation']= d.text
        if "fsm" in d["class"]:
            user['joined'] = float(d.abbr['data-utime'])
            if d.text.startswith("Added by"):
                user['addedby'] = d.abbr.previousSibling[9:-1]
    coll.insert(user)
    print (user['name'])

def retrieve(url):
    request = urllib.request.Request(url)
    request.add_header("Cookie", cookieText)
    return urllib.request.urlopen(request)

def midRegex(regex, search):
    regex = re.compile(regex)
    match = regex.search(search)
    content = match.group(1)
    return content

def nextPage(url):
    url = "https://www.facebook.com" + url + "&__a=1"
    jsonpData = retrieve(url).read()
    jsonp = str(jsonpData.decode('unicode_escape').encode('ascii','ignore'))
    jsonp = jsonp.replace('\\\\/', "/")
    content = midRegex('":"(.*?)"}],', jsonp)
    soup = BeautifulSoup(content)
    processContainer(soup)

def processContainer(container):
    data = container.findAll("div", {"class": "clearfix"})
    for cell in data:
        item = cell.div
        if "uiMorePager" in cell['class']:
            nextPage(item.a['href'])
        else:
            handleAdd(item)

# get initial page content
groupUrl = "https://www.facebook.com/groups/" + groupId + "/members/"
response = retrieve(groupUrl)

# get FB content comment blocks
bTag = tag.encode("utf-8")
for line in response.readlines():
    if bTag in line:
        hiddenContent = str(line)
        break

# extract from comment
content = midRegex('<!--(.*?)-->', hiddenContent)

# parse DOM
soup = BeautifulSoup(content)
encapTag = soup.findAll("div", {"class": tag})[0]
processContainer(encapTag)
