import urllib.request
from bs4 import BeautifulSoup
import re

class Member:
    @staticmethod
    def buildUser(obj):
        user = dict()
        user['name'] = obj.a.text
        for d in obj.findAll("div"):
            if "fsl" in d["class"]:
                url = d.a["data-hovercard"]
                userid = Member.midRegex('id=(.*?)&extraget', url)
                user['url'] = d.a['href']
                user['userid'] = userid
            if "_17tq" in d["class"]:
                user['occupation']= d.text
            if "fsm" in d["class"]:
                user['joined'] = float(d.abbr['data-utime'])
                if d.text.startswith("Added by"):
                    user['addedby'] = d.abbr.previousSibling[9:-1]
        print(user['name'])
        return user

    def retrieve(self, url):
        request = urllib.request.Request(url)
        request.add_header("Cookie", self.cookieText)
        return urllib.request.urlopen(request)

    @staticmethod
    def midRegex(regex, search):
        regex = re.compile(regex)
        match = regex.search(search)
        content = match.group(1)
        return content

    def nextPage(self, url):
        url = "https://www.facebook.com" + url + "&__a=1"
        jsonpData = self.retrieve(url).read()
        jsonp = str(jsonpData.decode('unicode_escape').encode('ascii','ignore'))
        jsonp = jsonp.replace('\\\\/', "/")
        content = Member.midRegex('":"(.*?)"}],', jsonp)
        soup = BeautifulSoup(content)
        self.processContainer(soup)

    def processContainer(self, container):
        data = container.findAll("div", {"class": "clearfix"})
        for cell in data:
            item = cell.div
            if "uiMorePager" in cell['class']:
                self.nextPage(item.a['href'])
            else:
                user = self.buildUser(item)
                self.handler(user)


    def __init__(self, groupId, cookieText):
        self.cookieText = cookieText
        self.groupId = groupId

    def getDict(self):
        self.data = dict()
        def simpleAdd(user):
            self.data[user['userid']] = user
        self.get(simpleAdd)
        return self.data

    def get(self, func):
        self.handler = func
        tag = 'fbProfileBrowserListContainer'
        # get initial page content
        groupUrl = "https://www.facebook.com/groups/" + self.groupId + "/members/"
        response = self.retrieve(groupUrl)

        # get FB content comment blocks
        bTag = tag.encode("utf-8")
        for line in response.readlines():
            if bTag in line:
                hiddenContent = str(line)
                break

        # extract from comment
        content = Member.midRegex('<!--(.*?)-->', hiddenContent)

        # parse DOM
        soup = BeautifulSoup(content)
        encapTag = soup.findAll("div", {"class": tag})[0]
        self.processContainer(encapTag)
        return self.data
