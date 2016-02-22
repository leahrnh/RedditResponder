#!/usr/bin/env python
###########################################################################
##                                                                       ##
##                  Language Technologies Institute                      ##
##                     Carnegie Mellon University                        ##
##                         Copyright (c) 2012                            ##
##                        All Rights Reserved.                           ##
##                                                                       ##
##  Permission is hereby granted, free of charge, to use and distribute  ##
##  this software and its documentation without restriction, including   ##
##  without limitation the rights to use, copy, modify, merge, publish,  ##
##  distribute, sublicense, and/or sell copies of this work, and to      ##
##  permit persons to whom this work is furnished to do so, subject to   ##
##  the following conditions:                                            ##
##   1. The code must retain the above copyright notice, this list of    ##
##      conditions and the following disclaimer.                         ##
##   2. Any modifications must be clearly marked as such.                ##
##   3. Original authors' names are not deleted.                         ##
##   4. The authors' names are not used to endorse or promote products   ##
##      derived from this software without specific prior written        ##
##      permission.                                                      ##
##                                                                       ##
##  CARNEGIE MELLON UNIVERSITY AND THE CONTRIBUTORS TO THIS WORK         ##
##  DISCLAIM ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING      ##
##  ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT   ##
##  SHALL CARNEGIE MELLON UNIVERSITY NOR THE CONTRIBUTORS BE LIABLE      ##
##  FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES    ##
##  WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN   ##
##  AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION,          ##
##  ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF       ##
##  THIS SOFTWARE.                                                       ##
##                                                                       ##
###########################################################################
##  Author: Aasish Pappu (aasish@cs.cmu.edu)                             ##
##  Date  : November 2012                                                ##
###########################################################################
## Description: Example python backend module for olympus applications   ##
###########################################################################

###########################################################################
##               RedditResponder Modifications                           ##
## Author: Leah Nicolich-Henkin (leah.nh@cs.cmu.edu)                     ##
## Date  : January 2016                                                  ##
##                                                                       ##
## Working off TickTock 'galbackend' version from January 2015           ##
##      with notable additions by @yipeiw                                ##
## Deleted nearly the entirety of the code, retaining structure of       ##
## methods previously used for debugging                                 ##
## and resource structure/initialization                                 ##
##                                                                       ##
###########################################################################


# LNH: uses the Loader to create idf_dict, which is used for comparing candidates
import Loader
import RedditQuery


# @yipeiw
resource = {}
# listfile = 'reddit_corpus.list' # file listing all corpus files to be used as a database
idf_file = 'idf_dict.csv' # file listing words and idf values


def init_resource():
    global resource
    resource = Loader.load_language_resource(idf_file)


# @yipeiw
# LNH: instead of using Control/Understand/Retrieval to find a response from the database,
# call RedditQuery, which queries Reddit directly
def get_response(user_input):
    global database, resource
    relevance, answer = RedditQuery.find_candidate(user_input, resource)
    # print("answer is: " + str(answer))
    output = " ".join(answer)
    return output
