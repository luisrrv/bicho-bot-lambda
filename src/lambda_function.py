import tweepy
from google_images_search import GoogleImagesSearch
import requests
import random
import os
from dotenv import load_dotenv
import time
import datetime
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[0]

def lambda_handler(event, context):
    # Load environment variables
    load_dotenv()
    CONSUMER_KEY = os.getenv('CONSUMER_KEY')
    CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
    ACCESS_SECRET = os.getenv('ACCESS_SECRET')
    GOOGLE_API_KEY= os.getenv('GOOGLE_API_KEY')
    GOOGLE_API_CX= os.getenv('GOOGLE_API_CX')

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    gis = GoogleImagesSearch(GOOGLE_API_KEY, GOOGLE_API_CX)

    # Check time to decide what to do
    hour = datetime.datetime.now().hour +9
    minute = datetime.datetime.now().minute

    if (hour==9 or hour==12 or hour==21) and (minute < 2):

        search_terms = ["el bicho gritando siuuu","cr7 tomando jugo", "El bicho memes 2023", "cristiano ronaldo mi comandante", "el bicho gif"]
        search_term = random.choice(search_terms)
        gis.search(search_params={'q': search_term, 'num': 20})
        img_url = gis.results()[random.randint(0, 9)].url

        text_tweets = [
            "SIUUUUUU!"
            "Quizás me odian porque soy muy bueno.",
            "Tu amor me hace fuerte, tu odio me hace imparable.",
            "Quizás me odian porque soy muy bueno.",
            "Yo sé que al que le gusta el fútbol, le gusto yo.",
            "¿Por qué mentir? No voy a ser un hipócrita y decir lo opuesto a lo que pienso, como hacen otros.",
            "Demasiada humildad es un defecto.",
            "Nunca he escondido el hecho de que es mi intención ser el mejor.",
            "Què hace una belleza como tú en un lugar tan sucio como mi mente?",
            "No soy Cristobal Colón, pero sí hay 1492 razones para quererte.",
            "Un iPhone to te puede quitar lo barrio, pero un barrio sí te puede quitar el iPhone.",
            "De día me gustaria jugar con Messi... Y de noche con el bicho. -Kylian Mbappe",
            "Muchas gracias afición esto es para vosotros, SIIIIUUUUUUUU!",
            "Si no sueltas tu pasado, con qué mano vas a agarrarme esta?",
            "Quieres ser el siii de mi uuuuu?",
            "Si Dios no exiscte por qué el bicho se llama Cristiano Ronaldo y no Ateo Ronaldo?",
        ]

        if (search_term == 'cr7 tomando jugo'):
            tweet = [random.choice(text_tweets), img_url]
        else:
            tweet = ["",img_url]

        # download image
        filename = 'temp.jpg'
        request = requests.get(tweet[1], stream=True)
        if request.status_code == 200:
            with open(filename, 'wb') as image:
                for chunk in request:
                    image.write(chunk)

            media = api.media_upload(filename)
            api.update_status(status=tweet[0], media_ids=[media.media_id])
            os.remove(filename)
        else:
            print("Unable to download image")

    else:
        print("Hour:", hour)
        print("Minute:", minute)

        #Search keyword 
        search = 'CR7 OR Ronaldo OR TeamCRonaldo OR TimelineCR7'
        #Maximum limit of tweets to be interacted with
        maxNumberOfTweets = 15

        #To keep track of tweets published
        count = 0

        print("Retweet Bot Started!")

        for tweet in tweepy.Cursor(api.search_tweets, search).items(maxNumberOfTweets):
            try:
                # for each status, overwrite that status by the same status, but from a different endpoint.
                status = api.get_status(tweet.id, tweet_mode='extended')
                if status.retweeted == False and status.favorited == False:
                    print("###############################################################")
                    print("Found tweet by @" + tweet.user.screen_name)
                    tweet.favorite()
                    print("Liked tweet")
                    tweet.retweet()
                    print("Retweeted tweet")
                    print("###############################################################")

                    #Random wait time
                    timeToWait = random.randint(10, 60)
                    print("Waiting for "+ str(timeToWait) + " seconds")
                    for remaining in range(timeToWait, -1, -1):
                        sys.stdout.write("\r")
                        sys.stdout.write("{:2d} seconds remaining.".format(remaining))
                        sys.stdout.flush()
                        time.sleep(1)
                    sys.stdout.write("\rOnwards to next tweet!\n")
            except tweepy.errors.TweepyException as e:
                print(str(e))

