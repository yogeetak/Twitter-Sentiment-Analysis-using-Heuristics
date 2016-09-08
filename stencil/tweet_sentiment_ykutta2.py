import sys
import json

scores={}
##Method to get the sentiment scores
def afinnDict():
    sent_file = open(sys.argv[1])
    for line in sent_file:
        term,score=line.split("\t")
        scores[term]=float(score)
    return scores

def main():
    sent_dict={}
    tweet_file= open(sys.argv[2],encoding="utf-8")
    for line in tweet_file:
        tweetscore=float(0.00)
        tweet=json.loads(line)
        tweetwordlist=tweet["text"].lower().split()
        for word in tweetwordlist:
            wordscore = scores.get(word, 0)
            tweetscore=float(tweetscore+wordscore)

        ##Storing sentiment values for each tweet in a dictionary    
        sent_dict[tweet["text"]]=tweetscore
        
    ##Retriving the 10 most high sentiment score tweets
    for tweet in sorted(sent_dict, key=sent_dict.get, reverse=True)[:10]:
        print (sent_dict[tweet], ":" ,tweet)

    tempdict={}
    for tweet in sorted(sent_dict, key=sent_dict.get, reverse=False)[:10]:
        a=sent_dict[tweet]
        tempdict[tweet]=a
        
    ##Retriving the 10 most Low sentiment score tweets
    for key in sorted(tempdict, key=tempdict.get , reverse=False):
        print(tempdict[key], ":" ,key)
  
if __name__ == '__main__':
    scores=afinnDict()
    main()

