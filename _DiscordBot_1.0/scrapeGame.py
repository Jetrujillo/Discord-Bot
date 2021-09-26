import unicodedata
import game
import requests
import lxml
import re
import game
import cdkey
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

steamURLPattern = '.*http(s)?\:\/\/store\.steampowered\.com\/app\/\d+\/'

def parseSteamURL(URL):
    req = requests.get(URL)
    src = req.content
    soup = BeautifulSoup(src, 'lxml')

    gameFeatures = soup.find_all('div', class_ = 'game_area_details_specs')
    #for item in gameFeatures:
    #    print(item.text)
    gameFeaturesClean = []
    for item in gameFeatures:
        gameFeaturesClean.append(item.text)

    gameDetails = soup.find_all('div', id = 'genresAndManufacturer')
    #gameDetails_refined = gameDetails[0]
    newGD = (gameDetails[0].text).split('\n')
    encgameTitle = (newGD[1].split(": ")[1]).encode("ascii", "ignore")
    gameTitle = encgameTitle.decode()
    gameGenre = newGD[2].split(": ")[1]
    #print(gameTitle)
    #print(gameGenre)

    gameDescription = (soup.find('div', class_ = 'game_description_snippet')).text.strip()

    gamePurchases = soup.find_all('div', class_ = 'game_area_purchase_game')
    gamePurchasesClean = []

    for item in gamePurchases:
        newGP = item.text.strip()
        newnewGP = (newGP.replace('\t', '')).replace('\r', '')
        newnewnewGP = newnewGP.split('\n')
        purchaseTitle = newnewnewGP[0]
        price = ''
        for match in newnewnewGP:
            if "$" in match:
                result = re.findall(r"(\$\d+\.\d{2})", match)
                #print(f'match: {result}')
                print(len(result))
                print (result)
                if len(result) <= 1:
                    price = result[0]
                else:
                    price = result[1]
                #print(price)
        exportItems = []
        if price=='':
            price = '$0.00'
        exportItems.append(f'{purchaseTitle}: {price}')
        #print(purchaseTitle)
        #print(price)
        for option in exportItems:
            gamePurchasesClean.append(option)

    gameSentiment = soup.find_all('div', class_ = 'user_reviews_summary_row')
    trueSentiment = []
    for x in gameSentiment:
        cleanx = x.text
        newnewGS = (cleanx.replace('\t', '')).replace('\r', '')
        newnewnewGS = newnewGS.split('\n')
        cleaned = []
        for y in newnewnewGS:
            if y != '':
                cleaned.append(y)
        preresult = ' '.join(cleaned[1:])
        result = unicodedata.normalize("NFKD", preresult)
        if "All Time" in result:
            x = result.split(" All")
            y = (x[0]).replace("%", "% positive")
            trueSentiment.append(y)
        #print(result)
    gameSentimentClean = trueSentiment[0]
    #print(gameSentimentClean)
    return game.Game(gameTitle, gameGenre, gameSentimentClean, gameDescription, gameFeaturesClean, gamePurchasesClean, URL)

def parseCDKey(URL):
    req = requests.get(URL)
    src = req.content
    soup = BeautifulSoup(src, 'lxml')

    cdkNam = ''
    cdkPla = ''
    cdkReg = ''
    cdkAva = ''
    cdkDel = ''
    cdkPri = ''
    cdkURL = URL

    nameDiv = soup.find('h1', class_='page-title')
    cdkNam = nameDiv.text

    for data in soup.find_all('div', class_='product-attributes primary'):
        cdkeyValue = data.find_all(class_='value')
        cdkeyType = data.find_all(class_='type')
        cleanValues = []
        cleanTypes = []
        pairs = []
        for x in cdkeyValue:
            cleanValues.append(x.text)
        for x in cdkeyType:
            cleanTypes.append(x.text)
        counter = 0
        for x in cleanValues:
            pairs.append(f'{cleanTypes[counter]}: {x}')
            counter = counter + 1
        #print(pairs)
        cdkPla = pairs[0]
        cdkReg = pairs[1]
        cdkAva = pairs[2]
        try:
            cdkDel = pairs[3]
        except:
            print(f'Out of stock, no delivery method.')
        else:
            cdkDel = 'N/A'
    priceDiv = soup.find_all('div', class_='product-info-price')
    #print(priceDiv[0].text)
    for p in priceDiv:
        result = re.search(r"(.\d+\.\d{2})", p.text)
        price = result[0]
        cdkPri = price
    return cdkey.Cdkey(cdkNam, cdkPla, cdkReg, cdkAva, cdkDel, cdkPri, cdkURL)


def lookUpCDKeys(URL):
    cdKeyURL = 'https://www.cdkeys.com/?q='
    if re.match(steamURLPattern,URL):
        parseSteam = re.split(steamURLPattern, URL)
        steamTitle = (parseSteam[2].split('/'))[0]
        #print(steamTitle)
        newURL = f'{cdKeyURL}{steamTitle}'

        #selenium stuff
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1420,1080')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(newURL)

        #soup stuff
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        offeringDivs = soup.find_all('div', class_='result ais-hits--loaded')

        hrefs = []
        for div in offeringDivs:
            foundhref = div.find('a')['href']
            hrefs.append(foundhref)

        #lookup hrefs in another function and leverage cdkey class
        results = []
        for href in hrefs:
            results.append(parseCDKey(href))
        return results

# Use for troubleshooting stuff
#steamURL = 'https://store.steampowered.com/app/527230/For_The_King/'
#cdkeyURL = 'https://www.cdkeys.com/pc/time-cards/titanfall-2-pc-nitro-scorch-pack-dlc-origin-cd-key'
#x = parseSteamURL(steamURL)
#print(x.__dict__)
#lookUpCDKeys(steamURL)
#parseCDKey(cdkeyURL)

