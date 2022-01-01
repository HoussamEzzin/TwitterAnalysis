import tweepy
from tweepy import Stream
from platform import python_version
import requests
from tweepy import OAuthHandler
import socket
import json
import credentials
'''
we import socket module to create a communication channel between 
our local machine and the Twitter API

'''


class TweetsListener(Stream):
    def __init__(self,csocket,consumer_key,consumer_secret, 
                 acces_token, acces_secret):
        self.access_token = acces_token
        self.access_token_secret = acces_secret
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.client_socket = csocket
        self.running = False
        self.session = None
        self.thread = None
        self.user_agent = (
            f"Python/{python_version()} "
            f"Requests/{requests.__version__} "
            f"Tweepy/{tweepy.__version__}"
        )
        self.chunk_size = 521
        self.daemon = False
        self.max_retries = 5
        self.proxies = {"https": None} if None else {}
        self.verify = True
        
        
    
    def on_data(self,data):
        try:
            msg = json.loads( data )
            print('new message')
            #if tweet is longer than 140 chars
            if "extended_tweet" in msg:
                self.client_socket\
                    .send(str(msg['extended_tweet']['full_text']+"t_end")\
                    .encode('utf-8'))
                print(msg['extended_tweet']['full_text'])
            else:
                self.client_socket\
                    .send(str(msg['text']+"t_end")\
                    .encode('utf-8'))
                print(msg['text'])
            return True
        except BaseException as e:
            print('Error on_data: %s' % str(e))
        return True
    def on_error(self,status):
        print(status)
        return True

#function to get data from twitter
def get_data(c_socket, keyword):
    print('Start getting data from Twitter')
    #authentication based on credentials file
    # auth = OAuthHandler(credentials.consumer_key,credentials.consumer_secret)
    # auth.set_access_token(credentials.access_token,credentials.access_secret)
    
    # twitter_stream = Stream(auth, TweetsListener(c_socket))
    twitter_stream = TweetsListener(c_socket,credentials.consumer_key,
                                    credentials.consumer_secret,
                                    credentials.access_token,
                                    credentials.access_secret)
    
    twitter_stream.filter(track= keyword, languages=["en"])
    
# start streaming

if __name__ == "__main__":
    
    s = socket.socket()
    host = "0.0.0.0"
    port = 5555
    s.bind((host,port))
    print('socket is ready')
    s.listen(4)
    print('socket is listening')
    
    c_socket, addr = s.accept()
    print('Received request from: '+ str(addr))
    get_data(c_socket, keyword=['piano'])



