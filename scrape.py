import re
import urllib.request

def midExtract(begin, end, search):
    regex = str(begin) + '(.*?)' + str(end)
    regex = re.compile(regex)
    match = regex.search(search)
    content = match.group(1)
    return content

def jsonpToHTML(jsonpData):
    jsonp = str(jsonpData.decode('unicode_escape').encode('ascii','ignore'))
    jsonp = jsonp.replace('\\\\/', "/")
    content = midExtract('":"','"}],', jsonp)
    return content

def retrieve(url, cookie):
    request = urllib.request.Request(url)
    request.add_header("Cookie", cookie)
    return urllib.request.urlopen(request)
