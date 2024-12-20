import requests
from bs4 import BeautifulSoup

class AskQuery:
    def __init__(self,Query:str) -> None:
        self.Query = Query
        self.iud = 'c10f7632-42e9-4501-ba7c-e972e1a94ebe'
        self.session = requests.Session()

    def req(self):
        req1 = self.session.get(f'https://es.ask.com/web?l=dir&qo=homepageSearchBox&ueid={self.iud}&q={self.Query}')
        return BeautifulSoup(req1.text, "html.parser")

def urlsave(newreq):
    newuls = newreq.find_all('a', {'class': 'PartialSearchResults-item-title-link result-link'})
    uls = []
    for save in newuls:
        href = save.get("href")
        if href:
            uls.append(href)
    return uls



