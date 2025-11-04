import mediawiki
import datetime
import json
import os.path

lexicanum = mediawiki.MediaWiki()
lexicanum.set_api_url("https://wh40k.lexicanum.com/mediawiki/api.php")
lexicanum.user_agent = "Downloading the plaintext of pages for a personal project :)"
lexicanum.rate_limit = True
lexicanum.rate_limit_min_wait = datetime.timedelta(milliseconds=500)

abs_path = os.path.abspath(__file__)
home_dir = os.path.dirname(abs_path)
articles_path = home_dir + '/articles_kb/'

with open("page_titles.json","r", encoding="utf-8") as jsonFile:
    pages = json.load(jsonFile)

for article in pages:
    curr = lexicanum.page(article)
    if ((os.path.isfile(articles_path + str(curr.pageid) +".txt") == False) and curr.content.strip() != ""):
        print("Saving", curr.pageid)
        with open(articles_path+curr.pageid + ".txt", "w", encoding='utf-8') as curr_file:
            curr_file.write(curr.content)
        with open(home_dir+'/processed_article_ids.txt', "a", encoding='utf-8') as processed_files:
            processed_files.write(curr.pageid + ",\n")
            
    else:
        print (curr.pageid, "was already saved or the article is empty.")