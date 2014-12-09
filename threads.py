from bs4 import BeautifulSoup
import scrape
import urllib

class Thread:
    def __init__(self, groupId, cookieText):
        self.cookieText = cookieText
        self.groupId = groupId

    def retrieve(self, url):
        return scrape.retrieve(url, self.cookieText)

    def processPage(self, content):
        soup = BeautifulSoup(content)
        encapTag = soup.findAll("div", {"class": "mbm"})
        for tag in encapTag:
            post = tag("span", {"class": "fwb"})[0]
            text = post.a.text
            for p in tag("p"):
                text += '\n'+ p.text
            print(text)

    def nextPage(self, content):
        data = scrape.midExtract('GroupEntstreamPagelet",', ', {"target_id"', content)
        data = urllib.parse.quote(data)
        url = "https://www.facebook.com/ajax/pagelet/generic.php/GroupEntstreamPagelet?data=" + data + "&__a=1"
        response = self.retrieve(url).read()
        response = scrape.jsonpToHTML(response)
        pageContent = scrape.midExtract('"payload":"', '","', response)
        self.processPage(pageContent)
        self.nextPage(response)

    def getDict(self):
        self.data = dict()
        def simpleAdd(thread):
            self.data[thread['id']] = thread
        self.get(simpleAdd)
        return self.data

    def get(self, func):
        self.handler = func

        # get content
        groupUrl = "https://www.facebook.com/groups/" + self.groupId + "/"
        response = self.retrieve(groupUrl).readlines()

        # get initial page load content
        hiddenContent = scrape.lineSearch('RECENT ACTIVITY', response)
        aboveFoldContent = scrape.midExtract('<!--', '-->', hiddenContent)
        self.processPage(aboveFoldContent)

        hiddenPager = scrape.lineSearch('GroupEntstreamPagelet', response)
        hiddenPager = hiddenPager.replace('\\\\', '')
        self.nextPage(hiddenPager)
