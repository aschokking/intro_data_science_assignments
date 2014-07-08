import sys
import json
import re

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    
    word_scores = {}    
    
    term_scores = {}
    phrase_scores = {}

    punc = '[\.,!"\'#@:\(\)]' 
    
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
            if tweet_json['lang'] == 'en':
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
                text = text.replace(phrase, '@@')

        # second pass, look for single words to score        
        words = text.split()
        for word in words:
            scrubbed_word = re.sub(punc, '', word.lower())
            try:
                score += term_scores[scrubbed_word]
                text = text.replace(word, '@@')
            except KeyError:
                """ no op """
        tweet_scores.append(score)

        #third pass, take remaining words and add them to the new words dict        
        words = text.split()
        for word in words:
            scrubbed_word = (re.sub(punc, '', word.lower())).strip()
            if scrubbed_word not in word_scores:
                word_scores[scrubbed_word] = {'count': 1, 'total' : score}
            else:
                word_scores[scrubbed_word]['count'] += 1
                word_scores[scrubbed_word]['total'] += score

    for word, data in word_scores.iteritems():
        if len(word.split()) == 1:
            print(word + ' ' + str(data['total'] / float(data['count']))
    
if __name__ == '__main__':
    main()
