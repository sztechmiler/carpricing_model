import requests
import os
import time
import random
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self, namesAndLinks):
        self.namesAndLinks = namesAndLinks

        for voivodship, otomoto_link in otomoto_voivodlinks.items():
            iterateThrouthOtomotoLink(voivodship, otomoto_link)
        cwd = os.getcwd()

    def iterateThrouthOtomotoLink(self, voivod, link):
        for x in range(1, 501):  # ma być od 1 do 501
            currentItemPath = cwd + "/{voivod}/{pageIndex}/".format(voivod=voivod, pageIndex=str(x))
            os.makedirs(currentItemPath, exist_ok=True)
            url = link + "{pageIndex}".format(pageIndex=str(x))
            info = GetPageAsJson(url)
            goOn = extractLinksFromVoivodHTML(info, currentItemPath, x)
            f = open(currentItemPath + str(x) + ".txt", "w+")
            f.write(info)
            f.close()
            sleepTime = random.randint(0, 10) / 10
            print(x)
            time.sleep(sleepTime)
            if (not goOn):
                break


    def GetPageAsJson(url):

        headers = {
            'User-Agent': "presonal_agent",
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            # 'Postman-Token': "be12394c-b5b2-4019-bf14-fe93b9a321a0,6505331a-24d4-4dab-9397-6c92fc638bb8",
            # 'Host': "www.otomoto.pl",
            'Accept-Encoding': "gzip, deflate",
            'Cookie': "laquesis=cars-13642@b#cars-13878@a#cars-13986@b#cars-14044@a#cars-14109@b#cars-14358@b#cars-14585@b#cars-14588@a; laquesisff=cars-12084#cars-12514#cars-12578#cars-12764#cars-12788#cars-12801#cars-12892#cars-13116; lqstatus=1575404586; _abck=FB43BE5DA2BAAC4A32AFF7233F79B239~-1~YAAQFx0SAnyniHpuAQAA4fVbzQIBS8L81M8bApMZPEyA1KNCRCBNOPNc6ExPyyd9DYxki1sF/tLCi1Z+CEWuqVC5iwWAhiNQaSq6IacF6XEuSpiJpg/2dWCWhcpXddOYY1k18W6d+k9jhb2tfYzUhiyaI3V8G0o1onuLVw3SBV2qiNTZam4Uo5fVYX3u0sa2TnhmxmbopyYyGekEQXKwpyLP2yzQdTYTVov8s984RmwogteL8lj3y2z6xP/jL8Xd55EdD/Nq/HUGMO3UNGmLAvuyJJggJQe7PCMMR8c9Af3cxm2HFT7o24dS~-1~-1~-1",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }
        r = requests.get(url, headers=headers)

        # return requests.request("GET", url, headers=headers)
        return r.text

    def extractOffer(offer_link, folder, i):
        offer_html = GetPageAsJson(offer_link)
        os.makedirs(folder + "offers/", exist_ok=True)
        f = open(folder + "offers/" + str(i) + ".txt", "w+")
        f.write(offer_html)
        f.close()
        sleepTime = random.randint(0, 10) / 10
        time.sleep(sleepTime)

    def extractLinksFromVoivodHTML(voivodHTML, itemFolder, index):
        soup = BeautifulSoup(voivodHTML, 'html.parser')
        fa = open(itemFolder + str(index) + "links.txt", "a+")
        i = 1
        for link in soup.find_all('a', class_='offer-title__link'):
            link_txt = link.get('href')
            fa.write(link_txt)
            extractOffer(link_txt, itemFolder, i)
            i = i + 1
            fa.write("\n")
        fa.close()
        if (soup.find('link', {'rel': 'next'}) == None):
            return False
        else:
            return True

    # Commented out function -> now we will find other "relecvant links"


    # TODO: scrap for all voivodships up to 500 => ready!
    # TODO: extract lists of links there with some unique identifier => ready!

    # TODO: run through all links 16 x ~1500 = ~24 000 websites and queries.... hmmm :-) around 10%

if __name__ == '__main__':
    otomoto_voivodlinks_done = {
        "mazowieckie": "https://www.otomoto.pl/osobowe/mazowieckie/?page=",
        "slaskie": "https://www.otomoto.pl/osobowe/slaskie/??page=",
        "wielkopolskie": "https://www.otomoto.pl/osobowe/wielkopolskie/?page=",
        "malopolskie": "https://www.otomoto.pl/osobowe/malopolskie/?page=",
        "dolnoslaskie": "https://www.otomoto.pl/osobowe/dolnoslaskie/?page=",
        "pomorskie": "https://www.otomoto.pl/osobowe/pomorskie/?page=",
        "lodzkie": "https://www.otomoto.pl/osobowe/lodzkie/?page=",
        "kujawsko-pomorskie": "https://www.otomoto.pl/osobowe/kujawsko-pomorskie/?page=",
        "lubelskie": "https://www.otomoto.pl/osobowe/lubelskie/?page=",
        "zachodniopomorskie": "https://www.otomoto.pl/osobowe/zachodniopomorskie/?page=",
        "podkarpackie": "https://www.otomoto.pl/osobowe/podkarpackie/?page=",
        "swietokrzyskie": "https://www.otomoto.pl/osobowe/swietokrzyskie/?page=",
        "lubuskie": "https://www.otomoto.pl/osobowe/lubuskie/?page=",
        "warminsko-mazurskie": "https://www.otomoto.pl/osobowe/warminsko-mazurskie/?page=",
        "podlaskie": "https://www.otomoto.pl/osobowe/podlaskie/?page=",
        "opolskie": "https://www.otomoto.pl/osobowe/opolskie/?page="
    }

    otomoto_voivodlinks = {
        "lubuskie": "https://www.otomoto.pl/osobowe/lubuskie/?page=",
    }

    otomotoScraper = Scraper(otomoto_voivodlinks)



