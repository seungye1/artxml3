import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, date


main_url = "https://sagittarius.com/archive/{}"
df = pd.DataFrame(columns=['start_date', 'end_date', 'sign', 'horoscope'])

i = 0
page = 1
while page <= 113:
    try:
        main_req = requests.get(main_url.format(page))
        main_soup = BeautifulSoup(main_req.text, 'lxml')
        h5s = main_soup.find('div', class_="bg-main-gradient").find_all('h5')
        for h5 in h5s:
            print(i)
            if i == 0:
                i += 1
                continue
            try:

                url = h5.find('a').get('href')
                req = requests.get(url)
                soup = BeautifulSoup(req.text, 'lxml')
                horoscopes = soup.find('ul', class_="horoscope-list").find_all('li')
                # print(horoscopes)
                sign = [h.find('a').get('name') for h in horoscopes]
                day = soup.find('div', class_="bg-main-gradient").\
                    find('h3').text.replace("Free Horoscope for ", '')
                day = datetime.strptime(day, "%B %d, %Y")
                days = [day for x in range(len(sign))]
                daily = [str(h.find('div', class_='text').find('p').text.replace(
                         "Ask 1 free question to a Psychic", '').
                    encode('ascii', 'ignore')) for h in horoscopes]
                df = df.append(pd.DataFrame({"start_date": days, "end_date": days,
                                             "sign": sign, "horoscope": daily},
                               columns=df.columns))
                i += len(sign)
            except:
                continue
        df.to_csv('daily2.csv')
    except:
        page += 1
        continue
    
    

df.to_csv('daily2.csv')
