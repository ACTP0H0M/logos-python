import string
import random

VERBOSE = False
ROBOT_KEYWORDS = ("robot", "ai", "artificial intelligence", "machine", "bot", "chatbot")
CLEVER_KEYWORDS = ("clever", "smart", "intelligent")
STUPID_KEYWORDS = ("stupid", "imbecile", "dumb", "idiot")
HAPPY_RESPONSE = ("I'm glad to hear that!", "That is great!", "Nice!")
SORRY_RESPONSE = ("Sorry to hear that... How can I help you?", "That is very sad. Can I help you?")
THANKS = ("Thank you very much!", "I'm flattered!", "You really think so? Thank you!")
GOOD_MOOD_PHRASES = ("I'm fine, thanks!", "I'm fine", "I'm great", "Good", "I'm ok", "I'm alright")
GOOD_MOOD_KEYWORDS = ("fine", "super", "great", "good", "wonderful", "amazing", "happy", "ok", "alright")
BAD_MOOD_PHRASES = ("I'm sad", "I don't feel very well", "I'm depressed")
BAD_MOOD_KEYWORDS = ("sad", "depressed", "tired", "bored", "exhausted", "bad", "unhappy")

# to extract punctuation
translator=str.maketrans('','',string.punctuation)

def jaccardIndex (set1, set2):
    global VERBOSE
    '''Intersection / (set1 + set2 - intersection)'''
    common = []
    for x in range(len(set1)):
        for y in range(len(set2)):
            if set1[x] == set2[y]:
                common.append(set1[x])
    ans = len(common) / (len(set1) + len(set2) - len(common))
    if VERBOSE:
        print("DEBUG: Jaccard Index = " + str(ans))
    return ans

def similarityIndex (set1, set2):
    global VERBOSE
    '''n-grams'''
    gram1 = []
    gram2 = []
    for x in range(len(set1)):
        if x <= len(set1) - 2:
            pair = [set1[x], set1[x + 1]]
            gram1.append(pair)
    for y in range(len(set2)):
        if y <= len(set2) - 2:
            combo = [set2[y], set2[y + 1]]
            gram2.append(combo)
    common = 0
    for z in range(len(gram1)):
        for u in range(len(gram2)):
            if gram1[z] == gram2[u]:
                common = common + 1
    try:
        ans = common / (len(gram1) + len(gram2) - common)
    except ZeroDivisionError:
        ans = 0
    if VERBOSE:
        print("DEBUG: n-Gram Index = " + str(ans))
    return ans

def isQuestion (sentence):
    if "?" in sentence:
        return True
    else:
        return False

def isPositiveMood (sentence):
    global VERBOSE
    if VERBOSE:
        print("DEBUG: Checking for good mood...")
    wrds = words(sentence)
    for i in range(len(wrds)):
        word = wrds[i]
        if word in GOOD_MOOD_KEYWORDS:
            for phrase in GOOD_MOOD_PHRASES:
                if similarityIndex(wrds, words(phrase)) >= 0.4:
                    return True
            return False
        if word in BAD_MOOD_KEYWORDS and wrds[i - 1] == "not":
            return True
    return False

def isNegativeMood (sentence):
    global VERBOSE
    if VERBOSE:
        print("DEBUG: Checking for bad mood...")
        wrds = words(sentence)
    for word in wrds:
        if word in BAD_MOOD_KEYWORDS:
            for phrase in BAD_MOOD_PHRASES:
                if similarityIndex(wrds, words(phrase)) >= 0.4:
                    return True
    return False

def containsRobotReference (sentence):
    for word in words(sentence):
        if word in ROBOT_KEYWORDS:
            return True
    return False

def containsDirectYou (sentence):
    for word in words(sentence):
        if word == "you":
            return True
    return False

def containsCompliment (sentence):
    for word in words(sentence):
        if word in CLEVER_KEYWORDS:
            return True
    return False

def containsFrustration (sentence):
    for word in words(sentence):
        if word in STUPID_KEYWORDS:
            return True
    return False

def findFirstIndex (word, wrds):
    for i in range(len(wrds)):
        if wrds[i] == word:
            return i
    return -1

def randomHappyResponse():
    return random.choice(HAPPY_RESPONSE)

def randomSorryResponse():
    return random.choice(SORRY_RESPONSE)

def randomThanks():
    return random.choice(THANKS)

def words(sentence):
    global VERBOSE
    '''Returns lowercase words without punctuation for a given sentence'''
    wrds = sentence.split(" ")
    if VERBOSE:
        print(wrds)
    for i in range(len(wrds)):
        if not "'" in wrds[i]:
            wrds[i] = wrds[i].translate(translator).lower()
    return wrds
