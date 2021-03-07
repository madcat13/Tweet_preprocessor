######################################################
#Data preprocessor
#Preprocesses Tweets to enable further text analysis
######################################################

#import libraries
from nltk.corpus import stopwords
import pandas as pd
import re

#set view to full text
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

#read csv and set encoding to "utf8"
df = pd.read_csv("/Users/username/Documents/Tweets.csv",encoding = "utf8")
df=astype(str)

#replace apostrophies symbol to match one type
Tweets = Tweets.str.replace("’","'")
Tweets = Tweets.str.replace(" ’","'")
#change to lower case
Tweets = Tweets.str.lower()
#print df length before dropping duplicates
print("before dropping duplicates ", len(df))
#drop duplicates
df = drop_duplicates('Tweets', keep='last')
#print dataframe length after dropping duplicates
print("after duplicate dropping ", len(df))

#function to remove special chars, links and emojis
#keeps apostrphies in words
def rem_chars(x):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z'\t])|(\w+:\/\/\S+)", " ", x).split())
df['Tweets'] = df['Tweets'].apply(lambda x: rem_chars(x))

#function to remove digits
def rem_digits(tweet):
        return ' '.join(re.sub("[0123456789]", ' ', tweet).split())
df['Tweets'] = df['Tweets'].apply(lambda x: rem_digits(x))

#function to remove stopwords
def rem_stopwords(text):
    #manually adjust stopwords to be excluded from nltk stopwords corpus
    combined_stopword = set(stopwords.words('english')) - {'i', 'me', 'my', 'myself', 'we', 'our', 'ours',
                                                              'ourselves', 'you', "you're", "you've", "you'll",
                                                              "you'd", 'your', 'yours', 'yourself', 'yourselves',
                                                              'he', 'him', 'his', 'himself'}
    #add new stopwords to nltk stopwords corpus
    all_stop_words = ["coronavirus","rona","therona","covid",
                      "gt","app","amp","qr"]+ list(combined_stopword)
    cleaned = ' '.join([x for x in text.lower().split() if x not in all_stop_words])
    return cleaned
df['Tweets'] = df['Tweets'].apply(lambda x: rem_stopwords(x))

#function to remove apostrophies(') outside of word boundries
def clean_apos(x):
    x=re.sub(r"(?!\b'\b)'", "", x)
    return "".join(x)
df['Tweets'] = df['Tweets'].apply(lambda x: clean_apos(x))


#set filename path and file name
filename='/Users/username/Documents/Tweets_cleaned.csv'

#save cleaned file as csv, set index to False
df.to_csv(filename, index=False)
