from bs4 import BeautifulSoup
import scrape
import urllib
class Thread:
    @staticmethod
    def buildThread(threadData):
        thread = dict()
        author = dict()
        meta = threadData("div", {"class": "_3dp"})[0]

        # get author data
        authorData = meta("a")[0]
        author["name"] = authorData.text
        author["id"] = scrape.midExtract("id=", "&", authorData["data-hovercard"])
        author["url"] = authorData["href"]

        postInfo = meta("a", {"class": "_5pcq"})[0]
        thread["date"] = int(postInfo.abbr['data-utime'])
        thread["id"] = postInfo["href"].split("/")[-2]

        # get post body
        postText = str()
        for p in threadData("p"):
            if len(postText) != 0:
                postText += '\n'
            postText += p.text

        thread["body"] = postText
        thread["author"] = author
        return thread

    def __init__(self, groupId, cookieText):
        self.cookieText = cookieText
        self.groupId = groupId

    def retrieve(self, url):
        return scrape.retrieve(url, self.cookieText)

    def processPage(self, content):
        soup = BeautifulSoup(content)
        encapTag = soup.findAll("div", {"class": "mbm"})
        for tag in encapTag:
            thread = Thread.buildThread(tag)
            self.handler(thread)

    def nextPage(self, content):
        data = scrape.midExtract('GroupEntstreamPagelet",', ', {"target_id"', content)
        if data is False:
            return
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
