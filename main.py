import yfinance as yf
import datetime
import os, time
import urllib.request
import json
import random
from termcolor import colored

def get_headlines():
    titles = []
    coins = ['bitcoin','litecoin','ethereum','dogecoin']
    for coin in coins:
        api_key = ''
        if api_key == '': return ["None"]
        url = "https://newsdata.io/api/1/news?apikey=" + api_key + "&q=" + coin + "&language=en"
        page = urllib.request.urlopen(url)
        for line in page.readlines():
            #print(line)
            y = json.loads(line)
            for result in y['results']:
                field = 'content'
                if result[field] == None: continue
                result[field] = result[field].replace("U.S.", "US").replace("U.S", "US")
                first_sentences = ''
                max_sentences = 3
                max_len = 300
                for i in range(max_sentences):
                    if i >= len(result[field].split('.')): break
                    if len(first_sentences) > max_len: break
                    first_sentences += result[field].split('.')[i] + '.'
                #if result[field] is not None and len(result[field].split('.')) > 2: first_sentences = result[field].split('.')[0] + '. ' + result[field].split('.')[1]
                if '>' in first_sentences: first_sentences = first_sentences.split('>')[1].split('<')[0]
                titles.append(result['title'] + "\n\n" + first_sentences)
    return titles


titles = get_headlines()
last_got_titles = time.time()
coins = ['BTC', 'ETH', 'LTC', 'DOGE']
#coins = ['BTC']
cont = True
while cont:
    closes_all = {'BTC': 17227.63, # average buy prices
                  'ETH': 1278,
                  'LTC': 70.10,
                  'DOGE': 0.06819}
    held = {'BTC': 0.01201,
            'ETH': 0.03747,
            'LTC': 0.4624,
            'DOGE': 320.91}
    gbp_held = {'BTC': 0,
            'ETH': 0,
            'LTC': 0,
            'DOGE': 0}
    current_prices = {'BTC': 0,
            'ETH': 0,
            'LTC': 0,
            'DOGE': 0}
    prices_all_ago = {'BTC': 0,
            'ETH': 0,
            'LTC': 0,
            'DOGE': 0}
    totheld_gbp_5min_ago = 0
    totheld_gbp_1hr_ago = 0
    totheld_gbp_24hr_ago = 0
    totheld_gbp_all_ago = 0
    totheld_gbp = 0
    for coin in coins:
        pair = coin + '-GBP'
        data = yf.download(tickers=pair, period='48h', interval='1m')
        got_5min = False
        timestamp_5min_ago = 0
        close_5min_ago = 0
        got_1hr = False
        close_1hr_ago = 0
        timestamp_1hr_ago = 0
        got_24hr = False
        close_24hr_ago = 0
        timestamp_24hr_ago = 0
        close_all_ago = closes_all[coin] * held[coin]
        prices_all_ago[coin] = closes_all[coin]
        totheld_gbp_all_ago += close_all_ago
        #print(data)
        for index, row in data.iterrows():
            date = str(index)
            date = date.split('+')[0]
            close = round(float(row['Close']),2)
          #  print(date)
            datenow = str(datetime.datetime.utcnow()).split('.')[0]
            unixstamp = time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").timetuple())
            currentstamp = time.mktime(datetime.datetime.strptime(datenow, "%Y-%m-%d %H:%M:%S").timetuple())
            age = currentstamp - unixstamp
          #  print(date, age)
            if not got_5min and age < 5 * 60:
                got_5min = True
                timestamp_5min_ago = unixstamp
                close_5min_ago = close
            if not got_1hr and age < 60 * 60:
                got_1hr = True
                timestamp_1hr_ago = unixstamp
                close_1hr_ago = close
            if not got_24hr and age < 24 * 60 * 60:
                got_24hr = True
                timestamp_24hr_ago = unixstamp
                close_24hr_ago = close
            currentprice = close
        current_prices[coin] = currentprice
        gbp_held[coin] = currentprice * held[coin]
        totheld_gbp += gbp_held[coin]
        totheld_gbp_5min_ago += close_5min_ago * held[coin]
        totheld_gbp_1hr_ago += close_1hr_ago * held[coin]
        totheld_gbp_24hr_ago += close_24hr_ago * held[coin]
    os.system("cls")
    #print(":::", totheld_gbp, totheld_gbp_5min_ago)
    increase_5min = totheld_gbp - totheld_gbp_5min_ago
    increase_percent_5min = increase_5min / totheld_gbp_5min_ago * 100
    increase_1hr = totheld_gbp - totheld_gbp_1hr_ago
    increase_percent_1hr = increase_1hr / totheld_gbp_1hr_ago * 100
    increase_24hr = totheld_gbp - totheld_gbp_24hr_ago
    increase_percent_24hr = increase_24hr / totheld_gbp_24hr_ago * 100
    increase_all = totheld_gbp - totheld_gbp_all_ago
    increase_percent_all = increase_all / totheld_gbp_all_ago * 100
    sign_5min = "+"
    if increase_5min < 0: sign_5min = ""
    sign_1hr = "+"
    if increase_1hr < 0: sign_1hr = ""
    sign_24hr = "+"
    if increase_24hr < 0: sign_24hr = ""
    sign_all = "+"
    if increase_all < 0: sign_all = ""
    sign_percent_5min = "+"
    if increase_percent_5min < 0: sign_percent_5min = ""
    sign_percent_1hr = "+"
    if increase_percent_1hr < 0: sign_percent_1hr = ""
    sign_percent_24hr = "+"
    if increase_percent_24hr < 0: sign_percent_24hr = ""
    sign_percent_all = "+"
    if increase_all < 0: sign_percent_all = ""
    a = " "

    # BTC

    btc_usd_price = round(current_prices['BTC'] * 1.22,2)
    btc_gbp_price = round(current_prices['BTC'],2)
    btc_increase = current_prices['BTC'] * held['BTC'] - prices_all_ago['BTC'] * held['BTC']
    btc_increase_percent = btc_increase / (prices_all_ago['BTC'] * held['BTC']) * 100
    btc_increase_percent = round(btc_increase_percent,2)
    btc_sign = "+"
    if btc_increase < 0: btc_sign = ""
    btc_usd_str = "$" + str(btc_usd_price)
    btc_gbp_str = "£" + str(btc_gbp_price)
    btc_swing_sign = "+"
    if btc_increase_percent < 0: btc_swing_sign = ""
    btc_swing_str = btc_swing_sign + str(round(btc_increase_percent,2)) + "%"

    btc_held_str = "£" + str(round(held['BTC'] * current_prices['BTC'],2)) + " (" + btc_sign + "£" + str(round(btc_increase,2)) + ")"
    buf1 = " "*(19 - len(str(btc_gbp_str)))
    buf2 = " "*(21 - len(str(btc_usd_str)))
    buf3 = " "*(13 - len(str(btc_swing_str)))
    print(a*8+"Price"+a*14+"Price USD"+a*12+"Swing"+a*8+"Held")
    colour = 'green'
    if btc_increase == 0: colour = 'white'
    elif btc_increase < 0: colour = 'red'
    print(colored("BTC" + " "*5 + str(btc_gbp_str) + buf1 + str(btc_usd_str) + buf2 + btc_swing_str + buf3 + btc_held_str, colour))

    # ETH

    eth_usd_price = round(current_prices['ETH'] * 1.22,2)
    eth_gbp_price = round(current_prices['ETH'],2)
    eth_increase = current_prices['ETH'] * held['ETH'] - prices_all_ago['ETH'] * held['ETH']
    eth_increase_percent = eth_increase / (prices_all_ago['ETH'] * held['ETH']) * 100
    eth_increase_percent = round(eth_increase_percent,2)
    eth_sign = "+"
    if eth_increase < 0: eth_sign = ""
    eth_usd_str = "$" + str(eth_usd_price)
    eth_gbp_str = "£" + str(eth_gbp_price)
    eth_swing_sign = "+"
    if eth_increase_percent < 0: eth_swing_sign = ""
    eth_swing_str = eth_swing_sign + str(round(eth_increase_percent,2)) + "%"

    eth_held_str = "£" + str(round(held['ETH'] * current_prices['ETH'],2)) + " (" + eth_sign + "£" + str(round(eth_increase,2)) + ")"
    buf1 = " "*(19 - len(str(eth_gbp_str)))
    buf2 = " "*(21 - len(str(eth_usd_str)))
    buf3 = " "*(13 - len(str(eth_swing_str)))
    colour = 'green'
    if eth_increase == 0: colour = 'white'
    elif eth_increase < 0: colour = 'red'
    print(colored("ETH" + " "*5 + str(eth_gbp_str) + buf1 + str(eth_usd_str) + buf2 + eth_swing_str + buf3 + eth_held_str, colour))

    # LTC

    ltc_usd_price = round(current_prices['LTC'] * 1.22,2)
    ltc_gbp_price = round(current_prices['LTC'],2)
    ltc_increase = current_prices['LTC'] * held['LTC'] - prices_all_ago['LTC'] * held['LTC']
    ltc_increase_percent = ltc_increase / (prices_all_ago['LTC'] * held['LTC']) * 100
    ltc_increase_percent = round(ltc_increase_percent,2)
    ltc_sign = "+"
    if ltc_increase < 0: ltc_sign = ""
    ltc_usd_str = "$" + str(ltc_usd_price)
    ltc_gbp_str = "£" + str(ltc_gbp_price)
    ltc_swing_sign = "+"
    if ltc_increase_percent < 0: ltc_swing_sign = ""
    ltc_swing_str = ltc_swing_sign + str(round(ltc_increase_percent,2)) + "%"

    ltc_held_str = "£" + str(round(held['LTC'] * current_prices['LTC'],2)) + " (" + ltc_sign + "£" + str(round(ltc_increase,2)) + ")"
    buf1 = " "*(19 - len(str(ltc_gbp_str)))
    buf2 = " "*(21 - len(str(ltc_usd_str)))
    buf3 = " "*(13 - len(str(ltc_swing_str)))
    colour = 'green'
    if ltc_increase == 0: colour = 'white'
    elif ltc_increase < 0: colour = 'red'
    print(colored("LTC" + " "*5 + str(ltc_gbp_str) + buf1 + str(ltc_usd_str) + buf2 + ltc_swing_str + buf3 + ltc_held_str, colour))

    # DOGE

    doge_usd_price = round(current_prices['DOGE'] * 1.22,4)
    doge_gbp_price = round(current_prices['DOGE'],4)
    doge_increase = current_prices['DOGE'] * held['DOGE'] - prices_all_ago['DOGE'] * held['DOGE']
    doge_increase_percent = doge_increase / (prices_all_ago['DOGE'] * held['DOGE']) * 100
    doge_increase_percent = round(doge_increase_percent,2)
    doge_sign = "+"
    if doge_increase < 0: doge_sign = ""
    doge_usd_str = "$" + str(doge_usd_price)
    doge_gbp_str = "£" + str(doge_gbp_price)
    doge_swing_sign = "+"
    if doge_increase_percent < 0: doge_swing_sign = ""
    doge_swing_str = doge_swing_sign + str(round(doge_increase_percent,2)) + "%"

    doge_held_str = "£" + str(round(held['DOGE'] * current_prices['DOGE'],2)) + " (" + doge_sign + "£" + str(round(doge_increase,2)) + ")"
    buf1 = " "*(19 - len(str(doge_gbp_str)))
    buf2 = " "*(21 - len(str(doge_usd_str)))
    buf3 = " "*(13 - len(str(doge_swing_str)))
    colour = 'green'
    if doge_increase == 0: colour = 'white'
    elif doge_increase < 0: colour = 'red'
    print(colored("DOGE" + " "*4 + str(doge_gbp_str) + buf1 + str(doge_usd_str) + buf2 + doge_swing_str + buf3 + doge_held_str, colour))

    print("---")
    colour = 'green'
    if increase_5min == 0: colour = 'white'
    elif increase_5min < 0: colour = 'red'
    print(colored("5 min: " + sign_5min + "£{:.2f}".format(increase_5min) + " " + "(" + sign_percent_5min + "{:.2f}".format(increase_percent_5min) + "%)", colour))
    colour = 'green'
    if increase_1hr == 0: colour = 'white'
    elif increase_1hr < 0: colour = 'red'
    print(colored("1 hr: " + sign_1hr + "£{:.2f}".format(increase_1hr) + " " + "(" + sign_percent_1hr + "{:.2f}".format(increase_percent_1hr) + "%)", colour))
    colour = 'green'
    if increase_24hr == 0: colour = 'white'
    elif increase_24hr < 0: colour = 'red'
    print(colored("24 hr: " + sign_24hr + "£{:.2f}".format(increase_24hr) + " " + "(" + sign_percent_24hr + "{:.2f}".format(increase_percent_24hr) + "%)", colour))
    colour = 'green'
    if increase_all == 0: colour = 'white'
    elif increase_all < 0: colour = 'red'
    print(colored("All: " + sign_all + "£{:.2f}".format(increase_all) + " " + "(" + sign_percent_all + "{:.2f}".format(increase_percent_all) + "%)", colour));
    print(colored("Total: £" + str(round(totheld_gbp,2)), colour))
    print("")
    headline = random.choice(titles)
    print("News: " + headline)
    since_titles_duration = time.time() - last_got_titles
    if since_titles_duration >= 60 * 60:
        last_got_titles = time.time()
        titles = get_headlines()
    time.sleep(30)
    #print(unixstamp)
        #print(row['Datetime'], float(row['Close']))