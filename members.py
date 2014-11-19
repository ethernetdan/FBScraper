import urllib.request
from bs4 import BeautifulSoup
import re

# FB Setup
tag = 'fbProfileBrowserListContainer'
groupId = "{insert group}"
cookieText = "{insert cookie}"

def handleAdd(obj):
    print (obj.a.text)

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

# extract from content
content = midRegex('<!--(.*?)-->', hiddenContent)

# parse DOM
soup = BeautifulSoup(content)
encapTag = soup.findAll("div", {"class": tag})[0]
processContainer(encapTag)