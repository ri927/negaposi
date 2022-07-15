import tweepy
from tweetObj import TwitterObj
import re
from oseti.osetiPack import oseti
from datetime import datetime 
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import settings

nowdate = datetime.now()

todayDate = (nowdate - relativedelta())
date1 = (nowdate - relativedelta(days = 1))
date2 = (nowdate - relativedelta(days = 2))
date3 = (nowdate - relativedelta(days = 3))
date4 = (nowdate - relativedelta(days = 4))
date5 = (nowdate - relativedelta(days = 5))
date6 = (nowdate - relativedelta(days = 6))
date7 = (nowdate - relativedelta(days = 7))

def isoFormat(date):
    
    isoDate = f'{date}T15:00:00Z'
    
    return isoDate


today = isoFormat(todayDate.strftime('%Y-%m-%d'))
one_day_ago =  isoFormat(date1.strftime('%Y-%m-%d'))
two_days_ago =  isoFormat(date2.strftime('%Y-%m-%d'))
three_days_ago =  isoFormat(date3.strftime('%Y-%m-%d'))
four_days_ago =  isoFormat(date4.strftime('%Y-%m-%d'))
five_days_ago =  isoFormat(date5.strftime('%Y-%m-%d'))
six_days_ago =  isoFormat(date6.strftime('%Y-%m-%d'))
seven_days_ago =  isoFormat(date7.strftime('%Y-%m-%d'))

# API情報を記入
BEARER_TOKEN        = settings.BEARER_TOKEN
API_KEY             = settings.API_KEY
API_SECRET          = settings.API_SECRET
ACCESS_TOKEN        = settings.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = settings.ACCESS_TOKEN_SECRET


# クライアント関数を作成
def ClientInfo():
    client = tweepy.Client(bearer_token    = BEARER_TOKEN,
                           consumer_key    = API_KEY,
                           consumer_secret = API_SECRET,
                           access_token    = ACCESS_TOKEN,
                           access_token_secret = ACCESS_TOKEN_SECRET,
                          )
    
    return client

# 検索用文字列（リツイートは除外する）
searchWord = input("検索ワードを入力>>")
search    = f'{searchWord} lang:ja'  # 検索対象,検索結果は日本語に限定
tweet_max = 100    # 取得したいツイート数(10〜100で設定可能)


def SearchTweets(search,tweet_max , start_time , end_time = today):    

    # 直近のツイート取得
    if end_time == today:
        tweets = ClientInfo().search_recent_tweets(query = search, max_results = tweet_max ,start_time = start_time  )
    
    else:
        tweets = ClientInfo().search_recent_tweets(query = search, max_results = tweet_max ,start_time = start_time , end_time = end_time )

    objList  = [] 
    tweets_data = tweets.data

    # tweet検索結果取得
    #1つのツイートを1つのオブジェクトにしてリストに格納
    if tweets_data != None: 
        for tweet in tweets_data:
            text =  tweet.text
            objList.append(TwitterObj(tweet.id, text.strip()))
    else:
        objList.append('')
        
    return objList

def format_text(text):
    
    text=re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text)
    text=re.sub('RT', "", text)
    text=re.sub('お気に入り', "", text)
    text=re.sub('まとめ', "", text)
    text=re.sub(r'[!-~]', "", text)#半角記号,数字,英字
    text=re.sub(r'[︰-＠]', "", text)#全角記号
    text=re.sub('\n', " ", text)#改行文字

    return text

def osetiPrint(text):
    analyzer = oseti.Analyzer()
    
    #リスト
    return analyzer.count_polarity(text.rstrip())

def negaposiSet(objList = []):
    
    for o in objList:
    
        posiCount = 0;
        neutralCount = 0;
        negaCount = 0;
    
        #ポジティブ度とネガティブ度をオブジェクトにセット
        if type(o) is not TwitterObj:
            index = objList.index(o)
             #空のオブジェクトをセット
            objList[index] = TwitterObj(None, '')
            objList[index].setPosi(0) 
            objList[index].setNeutral(0) 
            objList[index].setNega(0) 
        
        else:
            text = format_text(o.getText())
            
            negaposiList = osetiPrint(text)
            
            negaposi_posi = [p.get('positive') for p in negaposiList]
            negaposi_neutral = [ 1 if neu.get('positive') == 0 and neu.get('negative') == 0 else 0   for neu in negaposiList]
            negaposi_nega = [n.get('negative') for n in negaposiList]
            
            
            for p in negaposi_posi:
                posiCount += int(p)
                
            for neu in negaposi_neutral:
                neutralCount += int(neu)
            
            for n in negaposi_nega:
                negaCount += int(n)
            
            o.setPosi(posiCount)
            o.setNeutral(neutralCount)
            o.setNega(negaCount)

def showNegaPosi(objList = []):
    negaposiSet(objList)
    total = 0
    total_positive = 0
    total_neutral = 0
    total_negative = 0

    for tw in objList:
        total_positive += int(tw.getPosi())
        total_neutral += int(tw.getNeutral())
        total_negative += int(tw.getNega())

    total = total_positive + total_neutral + total_negative 

    posirate = 0 if total_positive == 0 else int((total_positive / total) * 100)
    neutralrate = 0 if total_neutral == 0 else int((total_neutral / total) * 100)
    negarate =  0 if total_negative == 0 else int((total_negative / total) * 100)

    print("ポジティブ度 = {}%".format(posirate))
    print("ニュートラル度 = {}%".format(neutralrate))
    print("ネガティブ度 = {}%".format(negarate))
    print("")

def calcPositive(objList):
    negaposiSet(objList)
    total = 0
    total_positive = 0
    total_neutral = 0
    total_negative = 0

    for tw in objList:
        total_positive += int(tw.getPosi())
        total_neutral += int(tw.getNeutral())
        total_negative += int(tw.getNega())
        

    total = total_positive + total_neutral + total_negative

    posirate = 0 if total_positive == 0 else int((total_positive / total) * 100)
    
    return posirate

def calcNeutral(objList):
    
    negaposiSet(objList)
    
    total = 0
    total_positive = 0
    total_neutral = 0
    total_negative = 0

    for tw in objList:
        total_positive += int(tw.getPosi())
        total_negative += int(tw.getNega())

    total = total_positive + total_neutral + total_negative

    neutralrate = 0 if total_neutral == 0 else int((total_neutral / total) * 100)
    
    return neutralrate

def calcNegative(objList):
    
    negaposiSet(objList)
    
    total = 0
    total_positive = 0
    total_neutral = 0
    total_negative = 0

    for tw in objList:
        total_positive += int(tw.getPosi())
        total_neutral += int(tw.getNeutral())
        total_negative += int(tw.getNega())

    total = total_positive + total_neutral + total_negative
    
    negarate =  0 if total_negative == 0 else int((total_negative / total) * 100)
    
    return negarate


#日付ごとにツイートを検索
todayTweetList = SearchTweets(search, tweet_max , one_day_ago , today)
oneDayAgoTweetList = SearchTweets(search, tweet_max , two_days_ago , one_day_ago)
twoDaysAgoTweetList = SearchTweets(search, tweet_max , three_days_ago , two_days_ago)
threeDaysAgoTweetList = SearchTweets(search, tweet_max , four_days_ago , three_days_ago)
fourDaysAgoTweetList = SearchTweets(search, tweet_max , five_days_ago , four_days_ago)
fiveDaysAgoTweetList = SearchTweets(search, tweet_max , six_days_ago , five_days_ago)
sixDaysAgoTweetList = SearchTweets(search, tweet_max , seven_days_ago , six_days_ago)

print(todayDate.strftime('%Y/%m/%d'))
showNegaPosi(todayTweetList)

print(date1.strftime('%Y/%m/%d'))
showNegaPosi(oneDayAgoTweetList)

print(date2.strftime('%Y/%m/%d'))
showNegaPosi(twoDaysAgoTweetList)

print(date3.strftime('%Y/%m/%d'))
showNegaPosi(threeDaysAgoTweetList)

print(date4.strftime('%Y/%m/%d'))
showNegaPosi(fourDaysAgoTweetList)

print(date5.strftime('%Y/%m/%d'))
showNegaPosi(fiveDaysAgoTweetList)

print(date6.strftime('%Y/%m/%d'))
showNegaPosi(sixDaysAgoTweetList)

#X軸のデータ
dateData = [date6.strftime('%m/%d'),date5.strftime('%m/%d'),date4.strftime('%m/%d'),date3.strftime('%m/%d'),date2.strftime('%m/%d'),date1.strftime('%m/%d'),todayDate.strftime('%m/%d')]

#Y軸のデータ
posiData = [calcPositive(sixDaysAgoTweetList), calcPositive(fiveDaysAgoTweetList),calcPositive(fourDaysAgoTweetList), calcPositive(threeDaysAgoTweetList),calcPositive(twoDaysAgoTweetList), calcPositive(oneDayAgoTweetList), calcPositive(todayTweetList)]
negaData = [calcNegative(sixDaysAgoTweetList), calcNegative(fiveDaysAgoTweetList),calcNegative(fourDaysAgoTweetList), calcNegative(threeDaysAgoTweetList),calcNegative(twoDaysAgoTweetList), calcNegative(oneDayAgoTweetList), calcNegative(todayTweetList)]

#グラフで表示するデータ
plt.plot(dateData, posiData, marker = 'o',color = 'red',label = 'positiveRate')
plt.plot(dateData, negaData, marker = 'x', color = 'blue', label = 'negativeRate')

plt.title(f'{searchWord}の検索結果', fontname="MS Gothic")
plt.ylim(0,100)
plt.xlabel("date", style ="italic" , size = "xx-large")
plt.ylabel("rate(%)", style ="italic" , size = "xx-large")
plt.legend(loc = 'upper right')
plt.show()
    
