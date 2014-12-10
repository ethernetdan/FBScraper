import re
import urllib.request

def midExtract(begin, end, search):
    regex = str(begin) + '(.*?)' + str(end)
    regex = re.compile(regex)
    match = regex.search(search)
    if match is None:
        return False
    content = match.group(1)
    return content

def jsonpToHTML(jsonpData):
    jsonp = str(jsonpData.decode('unicode_escape').encode('ascii','ignore'))
    jsonp = jsonp.replace('\\\\/', "/")
    return jsonp

def retrieve(url, cookie):
    request = urllib.request.Request(url)
    request.add_header("Cookie", cookie)
    return urllib.request.urlopen(request)

def lineSearch(key, lines):
    hiddenContent = str()
    bKey = key.encode("utf-8")
    for line in lines:
        if bKey in line:
            hiddenContent = str(line)
            break
    return hiddenContent
