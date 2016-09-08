import sys
import json

stateabbr_dict={"AL":"Alabama","AK":"Alaska","AZ":"Arizona","AR":"Arkansas","CA":"California","CO":"Colorado","CT":"Connecticut","DE":"Delaware","DC":"District of Columbia",
"FL":"Florida","GA":"Georgia","HI":"Hawaii","ID":"Idaho","IL":"Illinois","IN":"Indiana","IA":"Iowa","KS":"Kansas","KY":"Kentucky","LA":"Louisiana","ME":"Maine","MT":"Montana",
"NE":"Nebraska","NV":"Nevada","NH":"New Hampshire","NJ":"New Jersey","NM":"New Mexico","NY":"New York","NC":"North Carolina","ND":"North Dakota","OH":"Ohio","OK":"Oklahoma",
"OR":"Oregon","MD":"Maryland","MA":"Massachusetts","MI":"Michigan","MN":"Minnesota","MS":"Mississippi","MO":"Missouri","PA":"Pennsylvania","RI":"Rhode Island","SC":"South Carolina",
"SD":"South Dakota","TN":"Tennessee","TX":"Texas","UT":"Utah","VT":"Vermont","VA":"Virginia","WA":"Washington","WV":"West Virginia","WI":"Wisconsin","WY":"Wyoming",
"AS":"American Samoa","GU":"Guam","MP":"Northern Mariana Islands","PR":"Puerto Rico","VI":"U.S. Virgin Islands"}
scores={}

def afinnDict():
    sent_file = open(sys.argv[1])
    for line in sent_file:
        term,score=line.split("\t")
        scores[term]=float(score)
    return scores

def main():
    avg_lines={}
    sent_dict={}
    state_dict={}
    final_sent_dict={}
    tweet_file = open(sys.argv[2],encoding="utf-8")
    for line in tweet_file:
        tweetscore=float(0.00)
        tweet=json.loads(line)
        tweetlist=tweet["text"].split()
        location=tweet["user"]["location"]
        if (location is not None):
            location=location.split()
        else:
            continue

        ##checking the state of the location
        for word in location:
            stateabbr=""
            word=word.strip()
            if(word in stateabbr_dict.keys()):  ##Searching for abberviations directly,based on keys
                stateabbr=word
            elif(word in stateabbr_dict.values()):  ## Searching for full state names based on values
                stateabbr={key for key, value in stateabbr_dict.items() if value == word}
                stateabbr="".join(stateabbr)
            else:
                continue;

            ##If stateabbr name in dictionary, append the tweet to the state's existing tweets
            if(stateabbr in state_dict):
                exsttweet=state_dict[stateabbr]
                exsttweet.extend(tweetlist)
                state_dict[stateabbr]=exsttweet
                
            ##If stateabbr name not present in dictionry, add the key and the tweet
            else:
                state_dict[stateabbr]=tweetlist

            ##Adding the total lines to avg_lines dictionary
            if(stateabbr in avg_lines):
                avg_lines[stateabbr]=avg_lines[stateabbr]+1
            else:
               avg_lines[stateabbr]=1

    ##Calculating the sentiment of each states' tweets
    for state in state_dict.keys():
        tweetscore=float(0.00)
        tweetwordlist=state_dict[state]
        for word in tweetwordlist: ##calculating sentiment of each tweet
            word=word.lower()
            wordscore = scores.get(word, 0)
            tweetscore=float(tweetscore+wordscore)
        sent_dict[state]=tweetscore

    ##printing values of sentiment scores for each state
    for state in sorted(sent_dict, key=sent_dict.get, reverse=True):
        avg_score=float(0.0)
        avg_score=float(sent_dict[state]/avg_lines[state])
        final_sent_dict[state]=avg_score

    for state in sorted(final_sent_dict, key=final_sent_dict.get, reverse=True):
        print (final_sent_dict[state], ":" ,state)
    
if __name__ == '__main__':
    scores=afinnDict()
    main()
