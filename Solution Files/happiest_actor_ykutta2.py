import sys
import csv

scores={}
def afinnDict():
    sent_file = open(sys.argv[1])
    for line in sent_file:
        term,score=line.split("\t")
        scores[term]=float(score)
    return scores

def main():
    mydict={}
    sent_dict={}
    avg_lines={}
    final_senti_score={}
    actorname=""
    csv_file = open(sys.argv[2])
    file_reader = csv.reader(csv_file)
    for row in file_reader:
        actorname=row[0].strip()
        if(actorname=="user_name"):
            continue
        tweetlist=row[1].strip().split()

        ##If actor name in dictionary, append the tweet to the actor's existing tweets
        if(actorname in mydict): 
            exsttweet=mydict[actorname]
            exsttweet.extend(tweetlist)
            mydict[actorname]=exsttweet
            
        ##If actor name not present in dictionry, add the key and the tweet
        else:
            mydict[actorname]=tweetlist
            
        ##Adding the total lines to avg_lines dictionary
        if(actorname in avg_lines):
            avg_lines[actorname]=avg_lines[actorname]+1
        else:
           avg_lines[actorname]=1
    
    ##Calculating the sentiment of each actors' tweets
    for actor in mydict.keys():
        tweetscore=float(0.00)
        tweetwordlist=mydict[actor]
        for word in tweetwordlist: ##calculating sentiment of each tweet
            word=word.lower()
            wordscore = scores.get(word, 0)
            tweetscore=float(tweetscore+wordscore)
        sent_dict[actor]=tweetscore

    ##printing values of sentiment scores for each actor
    for actor in sorted(sent_dict, key=sent_dict.get, reverse=True):
        avg_score=float(0.0)
        avg_score=float(sent_dict[actor]/avg_lines[actor])
        final_senti_score[actor]=avg_score

    for actor in sorted(final_senti_score, key=final_senti_score.get, reverse=True):
        print (final_senti_score[actor], ":" ,actor)
    
if __name__ == '__main__':
    scores=afinnDict()
    main()
