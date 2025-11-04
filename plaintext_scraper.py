import mediawiki
import datetime
import json

lexicanum = mediawiki.MediaWiki()
lexicanum.set_api_url("https://wh40k.lexicanum.com/mediawiki/api.php")
lexicanum.user_agent = "Saving titles of all the pages for personal project"
lexicanum.rate_limit = True
lexicanum.rate_limit_min_wait = datetime.timedelta(seconds=1)

with open("page_titles.json","r", encoding="utf-8") as jsonFile:
    pages = json.load(jsonFile)

for i in range (5):
    curr = lexicanum.page(pages[i])
    print(curr.content)