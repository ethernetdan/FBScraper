import re

def midRegex(regex, search):
    regex = re.compile(regex)
    match = regex.search(search)
    content = match.group(1)
    return content

def jsonpToHTML(jsonpData):
    jsonp = str(jsonpData.decode('unicode_escape').encode('ascii','ignore'))
    jsonp = jsonp.replace('\\\\/', "/")
    content = midRegex('":"(.*?)"}],', jsonp)
    return content
