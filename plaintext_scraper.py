import mediawiki
import datetime
import json

lexicanum = mediawiki.MediaWiki()
lexicanum.set_api_url("https://wh40k.lexicanum.com/mediawiki/api.php")
lexicanum.user_agent = "Downloading the plaintext of pages for a personal project"
lexicanum.rate_limit = True
lexicanum.rate_limit_min_wait = datetime.timedelta(milliseconds=500)

with open("page_titles.json","r", encoding="utf-8") as jsonFile:
    pages = json.load(jsonFile)

print("START")
for i in range (5):
    curr = lexicanum.page(pages[i])
    print(curr.content)