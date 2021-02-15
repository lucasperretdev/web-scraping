import requests
import time
import sys
import random
import re
from bs4 import BeautifulSoup
import pandas as pd

# Pour rotation des proxies et user-agent
# list of proxies
https_proxy = [{"https": "ADD YOUR PROXY"},
               {"https": "ADD YOUR PROXY"}, {"https": "ADD YOUR PROXY"}]
# list of headers
headers = ({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
            'referer': 'https://www.google.com/'},
           {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66',
            'referer': 'https://www.bing.com/'},
           {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
            'referer': 'https://www.google.com/'},
           {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
            'referer': 'https://www.bing.com/'},
           )

# https://fr.trustpilot.com/review/www.adidas.com for instance www.adidas.com
company = 'TARGET COMPANY'
page_number = 1


def geturl(url, i, y):
    r = requests.get(url, proxies=https_proxy[i], headers=headers[y])
    return r


# Initialisation d'un dataframe
data_dict = {"date": [],
             "rating": [],
             "username": [],
             "nb_review_user": [],
             "is_verified": [],
             "company": [],
             "text": []}
df = pd.DataFrame(data_dict)

while True:
    url = f'https://fr.trustpilot.com/review/{company}?page={page_number}'
    # try a http request using a random proxy until there is a response.
    for nb_try in range(10):
        try:
            i = random.randint(0, len(https_proxy)-1)
            y = random.randint(0, len(headers)-1)
            page = geturl(url, i, y)
        except:
            continue
        if page.history == 403:
            continue
        else:
            break

    # Le programme s'arrete à la première redirection rencontrée
    if page.history == []:
        print(f'The page number {page_number} is being crawled...', end='\r')

        # réinitialisation du df
        data_dict = {"date": [],
                     "rating": [],
                     "username": [],
                     "nb_review_user": [],
                     "is_verified": [],
                     "company": [],
                     "text": []}

        soup = BeautifulSoup(page.content, 'html.parser')
        content_div = soup.findAll(class_='review-card')

        for i, div in enumerate(content_div):
            rating = div.find(class_='star-rating').find('img')['alt'][0]
            date_raw = div.find(
                class_='review-content-header__dates').find('script')
            regextest = '(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{2}:\d{2})|(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)'
            try:
                date = re.search(regextest, str(date_raw)).group(0)
            except:
                date = 0
            username = div.find(
                class_='consumer-information__name').text.strip()
            nb_review_tp = div.find(
                class_='consumer-information__review-count').span.text.split()[0]
            is_verified = div.find(
                class_='review-content-header__review-labels')
            if len(is_verified) > 2:
                is_verified = True
            else:
                is_verified = False
            text = div.find(class_="link link--large link--dark").text.strip()

            data_dict['date'].append(date)
            data_dict['rating'].append(rating)
            data_dict['username'].append(username)
            data_dict['nb_review_user'].append(nb_review_tp)
            data_dict['is_verified'].append(is_verified)
            data_dict['company'].append(company)
            data_dict['text'].append(text)

        page_df = pd.DataFrame(data_dict)
        df = pd.concat([df, page_df]).reset_index(drop=True)

    else:  # Une fois arrivé à la dernière page. Sauvegarde le fichier.
        df.to_csv(f'{company}-reviews.csv')
        break

    page_number += 1
    time.sleep(random.randint(0, 3))

print("Done !")
