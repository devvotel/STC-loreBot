import mediawiki
import typing
import json
import datetime

def allpages_monkey(self, query: str = "") -> typing.List[str]:
        """Request all pages from mediawiki instance

        Args:
            query (str): Search string to use for pulling pages
            results (int): The number of pages to return
        Returns:
            list: The pages that meet the search query
        Note:
            Could add ability to continue past the limit of 500
            """
        
        query_params = query_builder(query)
        request = self.wiki_request(query_params)
        self._check_error_response(request, query)
        page_titles = [page["title"] for page in request["query"]["allpages"]]
        
        try:
            apcontinue = request["continue"]["apcontinue"]  
        except:
            apcontinue = None
        
        i = 0
        while apcontinue != None:
            query_params = query_builder(query, apcontinue)
            request = self.wiki_request(query_params)
            self._check_error_response(request, query)
            page_titles.extend([page["title"] for page in request["query"]["allpages"]])
            
            try:
                apcontinue = request["continue"]["apcontinue"]  
            except:
                apcontinue = None

        return page_titles

def query_builder(query, apcontinue = None):
    if apcontinue != None:
        query_params = {"list": "allpages", "aplimit": "max", "apfrom": query, "apnamespace" : 0, "apcontinue" : apcontinue}
    else:
        query_params = {"list": "allpages", "aplimit": "max", "apfrom": query, "apnamespace" : 0}
    return query_params

def save_titles(pages: typing.List[str], filename: str):
    with open(filename,"w", encoding='utf-8') as json_file:
        json.dump(pages, json_file, sort_keys=True, indent=4)
    
    
        

mediawiki.MediaWiki.allpages = allpages_monkey

lexicanum = mediawiki.MediaWiki()
lexicanum.set_api_url("https://wh40k.lexicanum.com/mediawiki/api.php")
lexicanum.user_agent = "Saving titles of all the pages for personal project"
lexicanum.rate_limit = True
lexicanum.rate_limit_min_wait = datetime.timedelta(milliseconds=100)
all_pages = lexicanum.allpages()
save_titles(all_pages,'page_titles.json')
