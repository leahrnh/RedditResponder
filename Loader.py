#!/usr/bin/etc python

import json
import math
import csv


def load_language_resource(idf_file):
        print("Loading language resources...")
        idf_dict = load_freqs(idf_file)
        resource = {'idf_dict': idf_dict}
        return resource


def load_data_pair(datalist):
        print("Loading data...")
        database = {'Q': {}, 'A': {}}

        for datafile in datalist:
                f = open(datafile)
                line = f.readline()
                f.close()
                raw_data = json.loads(str(line.strip()))
                database = push_data_pair(raw_data, database)
        return database


def push_data_pair(data, database):
        last = len(database['Q'].keys())
        for pair in data:
                database['Q'][last] = pair['question'].split()
                database['A'][last] = pair['answer'].split()
                last += 1
        return database


def load_freqs(idf_file):
        idf_dict = {}
        with open(idf_file, 'rb') as csvfile:
                reader = csv.reader(csvfile, delimiter=",", quotechar='|')
                for line in reader:
                        word = line[0]
                        weight = float(line[1])
                        idf_dict[word] = weight
        return idf_dict


# Read a database and create a  dictionary where key=word in database and value=idf of the word.
# This was used to create idf_dict.csv and could be reinserted to be used with another database
#
# This could be improved by lowercasing and removing punctuation from everything.
# That would solve problems later on when an input word is lowercased, but all or most examples in the database are not.
def create_idf_file(database):
        # freq_dict measures the number of "documents" or phrases in the database that include the target word
        freq_dict = {}
        num_docs = 0
        for idx, utter in database['Q'].items():
                num_docs += 1
                for token in set(utter):
                    if token in freq_dict:
                            freq_dict[token] += 1
                    else:
                            freq_dict[token] = 1
        for idx, utter in database['A'].items():
                num_docs += 1
                for token in set(utter):
                    if token in freq_dict:
                            freq_dict[token] += 1
                    else:
                            freq_dict[token] = 1
        print("Created freq_dict")
        # idf_dict implements inverse document frequency for each word
        idf_dict = {}
        for word in freq_dict:
            idf_dict[word] = math.log(float(num_docs) / float(freq_dict[word]))

        with open('idf_dict.csv', 'wb') as csvfile:
            idf_writer = csv.writer(csvfile, delimiter=',', quotechar='|')
            for word in idf_dict:
                idf_writer.writerow([word.encode('utf-8'), idf_dict[word]])

        return idf_dict

