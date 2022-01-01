import tweepy
import credentials

client = tweepy.Client(bearer_token= credentials.bearer_token)

query = 'covid OR covid19'



reponse = client.search_recent_tweets(query=query, max_results=100)

print(reponse)
