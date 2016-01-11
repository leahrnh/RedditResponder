#!/usr/bin/etc python

import nltk
from collections import defaultdict
import json
import os.path as path
import math

#LNH: this section is no longer being used meaningful and could probably be altered/removed
def LoadLanguageResource(database):
        print("Loading language resources...")
        WeightRules=defaultdict(int)
        nounlist = ['NN', 'NNS', 'NNP', 'NNPS']
        for noun in nounlist:
                WeightRules[noun] = 3
        WeightRules['VBP'] = 1
        idf_dict = LoadFreqs(database)
        stop_dict=defaultdict(bool)
        for word in nltk.corpus.stopwords.words('english'):
                stop_dict[word] = True
        resource = {}
        resource['rules'] = WeightRules
        resource['stop_words'] = stop_dict
        resource['idf_dict'] = idf_dict
        return resource

def LoadData(datalist):
	database = {}
	for datafile in datalist:
		f = open(datafile)
		line = f.readline()
		f.close()
		raw_data = json.loads(str(line.strip()))
		database = PushData(raw_data, database)
	return database

def PushData(data, database):
	last = len(database.keys())
	for pair in data:
		database[last] = pair['question'].split()
		last += 1
		database[last] = pair['answer'].split()		
		last += 1
	return database

def LoadDataPair(datalist):
        print("Loading data...")
        database = {}
        database['Q'] = {}
        database['A'] = {}

        for datafile in datalist:
                f = open(datafile)
                line = f.readline()
                f.close()
                raw_data = json.loads(str(line.strip()))
                database = PushDataPair(raw_data, database)
        return database

def PushDataPair(data, database):
        last = len(database['Q'].keys())
        for pair in data:
                database['Q'][last] = pair['question'].split()
                database['A'][last] = pair['answer'].split()
                last += 1
        return database

def LoadTemplate(filelist):
	Library = {}
	for filepath in filelist:
		name = path.splitext(path.basename(filepath))[0]	
		Library[name] = [line.strip() for line in open(filepath)]
	return Library

def LoadTopic(topicfile):
	return [line.strip() for line in open(topicfile)]

#LNH: Create a dictionary where key=word in database and value=idf of the word. This is part of resource
#This takes some on startup, but otherwise doesn't effect how fast the program runs. Speed could be improved by doing this processing once and then reading from a file.
#This could also be improved by lowercasing and removing punctuation from everything. That would solve problems later on when an input word is lowercased, but all or most examples in the database are not.
def LoadFreqs(database):
        #freq_dict measures the number of "documents" or phrases in the database that include the target word
        freq_dict = {}
        numDocs = 0
        for idx, utter in database['Q'].items():
                numDocs += 1
                for token in set(utter):
                    if token in freq_dict:
                            freq_dict[token] += 1
                    else:
                            freq_dict[token] = 1
        for idx, utter in database['A'].items():
                numDocs += 1
                for token in set(utter):
                    if token in freq_dict:
                            freq_dict[token] += 1
                    else:
                            freq_dict[token] = 1
        print("Created freq_dict")
        #idf_dict implements inverse document frequency for each word
        idf_dict = {}
        for word in freq_dict:
             idf_dict[word] = math.log(float(numDocs) / float(freq_dict[word]))
        return idf_dict

