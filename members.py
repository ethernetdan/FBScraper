from bs4 import BeautifulSoup
import scrape

class Member:
    @staticmethod
    def buildUser(obj):
        user = dict()
        user['name'] = obj.a.text
        for d in obj.findAll("div"):
            if "fsl" in d["class"]:
                url = d.a["data-hovercard"]
                userid = scrape.midExtract('id=', '&', url)
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
        return scrape.retrieve(url, self.cookieText)

    def nextPage(self, url):
        url = "https://www.facebook.com" + url + "&__a=1"
        jsonpData = self.retrieve(url).read()
        content = scrape.jsonpToHTML(jsonpData)
        content = scrape.midExtract('":"','"}],', content)
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
        response = self.retrieve(groupUrl).readlines()

        # get FB content comment blocks
        hiddenContent = scrape.lineSearch(tag, response)

        # extract from comment
        content = scrape.midExtract('<!--', '-->', hiddenContent)

        # parse DOM
        soup = BeautifulSoup(content)
        encapTag = soup.findAll("div", {"class": tag})[0]
        self.processContainer(encapTag)
