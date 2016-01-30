# This script queries reddit directly, putting a phrase into the search function,
# and finding acceptable question and answer matches
import praw
import string
import re

# Reddit requires a user agent, which should have identifying information of some sort
# (typically Reddit username, sometimes github account)
user_agent = "RedditResponder https://github.com/leahrnh/RedditResponder"
r = praw.Reddit(user_agent=user_agent)


# take a list of tuples, return top n
# not currently using this method
def take_top(candidates, newCandidate, n):
    candidates += newCandidate
    candidates.sort(reverse=True)
    return candidates[:n]


#Test possible answers for acceptability, based on length, profanity, and encoding issues
def get_answer(comments):
    badwords = re.compile('.*(\sanal\s|fuck|cunt|penis|vagina|nsfw|\sfap\s|nigger|\srape\s|rapist|\sblow\sjob\s|cunnilingus|\sgive\shead\s|masturbat|porn|orgasm|fetish|blowjob|pussy|\sslut\s|\sclit\s|\shorny\s|\scock\s|jizz|\scum\s)')
    for comment in comments:
        acceptable = True
        reject_reason = "unknown"
        #        try:
        text = comment.body
        text = text.split('\n')
        text = text[0]
        #print("Trying new comment:\n"+text)
        if len(text.split()) > 15 or len(text.split()) < 2:
            acceptable = False
            reject_reason = "length"
        if badwords.match(text):
            acceptable = False
            reject_reason = "profanity"
        try:
            x = str(text)
        except:
            acceptable = False
            reject_reason="encoding"
        if acceptable:
            #print("found an answer")
            return text.split()
        else:
            pass
            #print("Rejected. Reason: " + reject_reason)
#        except:
#            print("Couldn't read comment")
#            pass


# lowercase the sentence and get rid of tags and punctuation
def clean(sentence):
    # some questions starting with a tag, ex. [Serious]. Get rid of that tag.
    tag = re.compile('^\[[^\]]+\]')
    sentence = sentence.lower()
    sentence = tag.sub('', sentence)
    sentence = sentence.translate(string.maketrans("",""), string.punctuation)
    return sentence


# returns a score for a comparison between a submission and an input, using a frequency-based metric
def get_score(submission, user_input, idf_dict):
    try:
        candidate = clean(str(submission.title))
    except:
        return 0, ''
    user_input = user_input.translate(string.maketrans("",""), string.punctuation)
    user_input_string = user_input.split()
    candidate_string = candidate.split()
    possible = 0
    actual = 0
    for token in user_input_string:
        # this section sets a weight even if the token is not in the idf_dict
        if token in idf_dict:
            weight = idf_dict[token]
        else:
            weight = 10

        if token != '':
            possible += weight
            if token in candidate_string:
                actual += weight
    for token in candidate_string:
        # this section sets a weight even if the token is not in the idf_dict
        if token in idf_dict:
            weight = idf_dict[token]
        else:
            weight = 10

        if token != '':
            possible += weight
            if token in user_input_string:
                actual += weight
    score = actual / possible
    # print("Candidate submission: ")
    # print(candidate)
    # print("score: " + str(score))
    return score, candidate


# Given an input sentence, search Reddit using that sentence, and return a list of submissions.
# Calculate the score of each submission using a frequency-based calculation.
# If it's the best submission so far, find an associated answer that is deemed acceptable
def find_candidate(user_input, resource):
    idf_dict = resource['idf_dict']
    # change 'limit=50' to test a different number of possible submissions.
    # The reason this number is so high is that I'm throwing out everything that's not a self-submission, which can be most of them
    submissions = r.search(user_input, limit=50)
    chosen = (-30, '', '')
    for submission in submissions:
        if submission.domain[:4] == 'self':
            score, candidate = get_score(submission, user_input, idf_dict)
            if score > chosen[0]:
            # Needs work: getting comments for each potential answer is significantly slowing things down. Would be better to make a list of top candidates, and then try comments from each of them (maybe 3-5) so as not to go through comments in everything as i go along. If the first one worked, I wouldn't even have to try the second.
                comments = submission.comments
                answer = get_answer(comments)
                if answer != None:
                    # print("Best question match so far: " + str(score) + " " + candidate)
                    chosen = (score, candidate, answer)
                else:
                    pass
                    # print("Couldn't find an answer")
    # print("question match: " + chosen[1])
    # print("score: " + str(chosen[0]))
    return chosen[0], chosen[2]
