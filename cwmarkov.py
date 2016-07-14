import os
import sys 
from random import choice
import twitter

input_path = sys.argv[1]


def open_and_read_file(file_path):
    """Takes file path as string; returns text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """
    # making a variable called contents and setting it equal to opening the file, 
    # reading over the file and making it all into one big string
    contents = open(file_path).read()
    return contents


def make_chains(text_string):
    """Takes input text as string; returns _dictionary_ of markov chacd neins.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> make_chains("hi there mary hi there juanita")
        {('hi', 'there'): ['mary', 'juanita'], ('there', 'mary'): ['hi'], ('mary', 'hi': ['there']}

    """
    # Creating an empty dictionary
    chains = {}

    # Splitting the long string from our file on the whitespace
    words = text_string.split()
    
    # Iterating through the words for the whole string, except the last two words
    for i in range(len(words)-2):
        # Creating a bigram variable that is a tuple of a word and the following word
        bigram = (words[i], words[i+1])
        # If the tuples are in the dictionary, append the third word to the values list

        if bigram in chains:
            chains[bigram].append(words[i+2])

        # If the tuples are not in the dictionary, add the tuple as a key, and the third
        # word to the values list
        else:
            chains[bigram] = [words[i+2]]
    
    # singled out the last bigram 
    last_bigram = (words[-2], words[-1])
    #append nothing to the list if last bigram in dictionary     
    if last_bigram in chains:
        chains[last_bigram].append(None)
    #if the last bigram is not in the dictionary 
    else:
        chains[last_bigram] = [None]

        
    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""

    
    # get the keys from the dict and randomize
    random_bigram = choice(chains.keys())
    # text is starting with the first random bigram
    text = random_bigram[0] + " " + random_bigram[1] 

    while len(text) < 140:
        # we want the next word to be a random value from available values list for 
        #the corresponding key 
        next_word = choice(chains[random_bigram])
        # if the next word is None, then break the while loop
        if not next_word:
            break
        # adding the next word to our text
        text = text + " " + next_word
        # updates the random_bigram variable to be the second word of the original bigram
        # plus the next word
        random_bigram = (random_bigram[1], next_word)    

    return text 


def tweet(new_text):
    """This tweets the text created in previous function."""

    #this connects our python script to twitter API using our info from secrets.sh
    api = twitter.Api(consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
                  consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
                  access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
                  access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    #print api.VerifyCredentials()
    # print new_text
    
    # posts our new_text as a status on twitter using their API method 
    status = api.PostUpdate(new_text)

    print status.text

# input_path = "green-eggs.txt"

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain
chains = make_chains(input_text)
# print chains

# Produce random text
random_text = make_text(chains)

tweet(random_text)