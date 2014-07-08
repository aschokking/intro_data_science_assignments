# -*- coding: utf-8 -*-
"""
Created on Mon Jul  7 20:09:27 2014

@author: alex
"""
import sys
import json
import re

punc = '[\.,!"\'#@:\(\)]' 

def main():
    tweet_file = open(sys.argv[1])
    word_total = 0;
    word_counts = {}
    for line in tweet_file:
        tweet_json = json.loads(line)
        try:
            text = tweet_json['text']
            
            words = text.split()
            for word in words:
                scrubbed_word = (re.sub(punc, '', word.lower())).strip()
                if scrubbed_word not in word_counts:
                    word_counts[scrubbed_word] = 1
                else:
                    word_counts[scrubbed_word] += 1
                word_total += 1
        except:
            """ no op """
             
    for word in word_counts:
        print word + ' ' + str(word_counts[word] / float(word_total))
    
if __name__ == '__main__':
    main()
