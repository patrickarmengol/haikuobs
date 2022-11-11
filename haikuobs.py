# TODO: get usernames
# TODO: scan for any haikus instead of just checking if full text is valid haiku
# TODO: botify to post tweets of found haikus in tweets

from syllablecount import count_syllables
from string import punctuation
import tweepy
import json

def get_twitter_client():
    with open('apikeys.json') as f:
        keys = json.load(f)
    return tweepy.Client(bearer_token=keys['bearer_token']) if keys else None

def search_tweets(client: tweepy.Client, keyword: str):
    results = client.search_recent_tweets(keyword, max_results=100)
    return results.data

def detect_haiku(text):
    words = text.replace('-', ' ').lower().split()

    line_flags = (5, 7, 5)
    lines = [[], [], []]
    li = 0
    sc = 0
    cur_phrase = []
    for word in words:
        if li > 2:
            #print('too many words; not a haiku')
            return ''
        cur_phrase.append(word)
        word = word.strip(punctuation)
        if word.endswith('\'s'):
            word = word[:-2]
        sc += count_syllables(word)
        if sc == line_flags[li]:
            lines[li] = cur_phrase
            cur_phrase = []
            sc = 0
            li += 1
        elif sc > line_flags[li]:
            #print('syllables don\'t match up to line breaks; not a haiku')
            return ''
    if not all(lines):
        #print('not enough words; not a haiku')
        return ''
    
    haiku = '\n'.join([' '.join(line) for line in lines])
    return haiku


def main():
    # tests = [
    #     'this is a short test to see if the script works or fails miserably',               # valid
    #     'this is a different test to see if invalid text passes',                           # syllables don't match up
    #     'the quick brown fox jumps over the lazy dog and then takes a shit',                # not enough words
    #     'the quick brown fox jumps over the lazy dog and then takes a shit on the lawn',    # too many words
    #     'first five syllables. then seven more syllables. finally five more!',              # punctuation
    #     'john\'s fox took a shit on my neighbor\'s yard again. hello there, neighbor!',     # apostraphes
    #     '''
    #     this is a multi line test.
    #     i wonder if it works.
    #     i do hope so...
    #     '''
    # ]
    # for test in tests:
    #     print(detect_haiku(test))
    
    client = get_twitter_client()

    while True:
        keyword = input('keyword to search: ')
        if keyword == '':
            break
        tweets = search_tweets(client, keyword)
        for tweet in tweets:
            #print(tweet.id)
            #print(tweet.text)
            hk = detect_haiku(tweet.text)
            if hk:
                print('-------------------------------------------------')
                print('++++++++++++++++++ haiku found ++++++++++++++++++')
                print(hk)
                print('-------------------------------------------------')

    print('bye')



if __name__ == '__main__':
    main()

