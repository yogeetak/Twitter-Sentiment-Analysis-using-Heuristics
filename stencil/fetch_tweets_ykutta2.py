import argparse
import oauth2 as oauth
import urllib.request as urllib
import json
import sys
import csv

# See Assignment 1 instructions for how to get these credentials
access_token_key = "3362112166-ndLh7zeQfs1RAzSlYt6XAukcBKspReVlfA2mzQO"
access_token_secret = "mh6yHShSYfc7biXzH6R6hbQw9RxPRt0Kccydul7zNnlr7"

consumer_key = "cgFdGq2gEnKfHsdUan9Eexe9C"
consumer_secret = "kUKqH4awMY3PEm5JE05kGIUWSn4Vj5b9sFxYLO2ONQOLQ5BV2K"

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
    req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

    req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

    headers = req.to_header()

    if http_method == "POST":
        encoded_post_data = req.to_postdata()
    else:
        encoded_post_data = None
        url = req.to_url()

    opener = urllib.OpenerDirector()
    opener.add_handler(http_handler)
    opener.add_handler(https_handler)

    response = opener.open(url, encoded_post_data)

    return response

def fetch_samples():
    url = "https://stream.twitter.com/1.1/statuses/sample.json?language=en"
    parameters = []
    response = twitterreq(url, "GET", parameters)
    for line in response:
        print (line.strip().decode('utf-8'))

def fetch_by_terms(term):
    url = "https://api.twitter.com/1.1/search/tweets.json"
    parameters = [("q", term)]
    response = twitterreq(url, "GET", parameters)
    print (response.readline())

def fetch_by_user_names(user_name_file):
    #write the csv header row
    writer = csv.writer(sys.stdout)
    writer.writerow(["user_name","tweet"])
    with open(user_name_file) as sn_file:
        reader=sn_file.readlines()
        for row in reader:
            url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
            parameters = [("screen_name", row),("count","100")]
            response = twitterreq(url, "GET", parameters).read().decode('utf-8')
            line_obj=json.loads(response)
            for tweet in line_obj:
                outtweets=[row.strip(),tweet['text']]
                writer.writerow(outtweets)
                
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', required=True, help='Enter the command')
    parser.add_argument('-term', help='Enter the search term')
    parser.add_argument('-file', help='Enter the user name file')
    opts = parser.parse_args()
    if opts.c == "fetch_samples":
        fetch_samples()
    elif opts.c == "fetch_by_terms":
        term = opts.term
        print (term)
        fetch_by_terms(term)
    elif opts.c == "fetch_by_user_names":
        user_name_file = opts.file
        fetch_by_user_names(user_name_file)
    else:
        raise Exception("Unrecognized command")
