import threads
import members
import json

cookieText = "{cookie here}"
groupId = "{groupId here}"

threads = threads.Thread(groupId, cookieText)
data = threads.getDict()
threadJson = json.dumps(data, indent=4, sort_keys=True)

members = members.Member(groupId, cookieText)
data = members.getDict()
memberJson = json.dumps(data, indent=4, sort_keys=True)

with open('members.json', 'w') as outfile:
    outfile.write(memberJson)

with open('threads.json', 'w') as outfile:
        outfile.write(threadJson)
