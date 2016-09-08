import sys
import json

stopwordlist=[]
def stopwords():
    with open(sys.argv[1],"r") as stop_word_file:
        stopwordlist=stop_word_file.read().split()
        return stopwordlist
        
def main():
    completewordlist=[]
    file_obj= open(sys.argv[2],encoding="utf-8")
    for line in file_obj:
        tweet=json.loads(line)
        tweetlist=tweet["text"].lower().split()
        
        ##removing the stop words from the tweet
        resultwords  = [word for word in tweetlist if word.lower() not in stopwordlist]
        completewordlist.extend(resultwords)

    ##Creating a Dictionary of Unique Words and their fequency count
    uniqwordset=set(completewordlist)
    frequency={}
    for word in uniqwordset:        
        frequency[word]=completewordlist.count(word)/(float)(len(completewordlist))

    ##Getting top 30 frequencies
    for word in sorted(frequency, key=frequency.get, reverse=True):
        print (word, frequency[word])


if __name__ == '__main__':
    stopwordlist=stopwords()
    main()

    ##References:
    ##http://digitalhistoryhacks.blogspot.com/2006/08/easy-pieces-in-python-word-frequencies.html
    ##http://stackoverflow.com/questions/20510768/python-count-frequency-of-words-in-a-list    
