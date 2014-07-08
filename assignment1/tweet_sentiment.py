import sys
import json
import re

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    term_scores = {}
    phrase_scores = {}
    for line in sent_file:
        term, score = line.split("\t")
        if ' ' in term:
            phrase_scores[term] = int(score)    
        else:
            term_scores[term] = int(score)
        
    tweet_texts = []
    for line in tweet_file:
        tweet_json = json.loads(line)
        try:
            tweet_texts.append(tweet_json['text'])
        except:
            """ no op """
            
    tweet_scores = []        
    for text in tweet_texts:
        score = 0        
        
        # first pass, look for multi-word phrases and sub/score them
        for phrase, phrase_score in phrase_scores.iteritems():
            if phrase in text.lower():
                score += phrase_score
                text = text.replace(phrase, 'AAAAA')

        # second pass, look for single words to score        
        words = text.split()
        for word in words:
            scrubbed_word = re.sub('[\.,!]', ' ', word.lower())
            try:
                score += term_scores[scrubbed_word]
            except KeyError:
                """ no op """
        tweet_scores.append(score)

    for i in range(len(tweet_scores)):
        print(tweet_scores[i])
    #for score in tweet_scores:
     #   print(score)

if __name__ == '__main__':
    main()
