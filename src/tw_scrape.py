import GetOldTweets3 as got
import pandas as pd

#set search variables
#keyword = "#NFL"
oldest_date = "2018-01-01"    
newest_date = "2020-07-01"
keywords = ["#entrepreneurship", "#business", "#portmanteau", "#hyphen", "#Hemingway"]
number_tweets = 100         #per keyword

#get old tweets
tweetCriteria_list = []
for keyword in keywords:
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(keyword)\
                                                .setSince(oldest_date)\
                                                .setUntil(newest_date)\
                                                .setLang('en')\
                                                .setMaxTweets(number_tweets)
    tweetCriteria_list.append(tweetCriteria)
    
#create twitter info for each keyword
tweet_dict = {}
for criteria, keyword in zip(tweetCriteria_list, keywords):
    tweets = got.manager.TweetManager.getTweets(criteria)
    tweet_dict[keyword] = tweets
    
#create df
tweet_df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in tweet_dict.items() ]))
tweet_df['tweet_count'] = tweet_df.index
tweet_df = pd.melt(tweet_df, id_vars=["tweet_count"], var_name='Keyword', value_name='got_criteria')
tweet_df = tweet_df.dropna()

#extract twitter information
#get_twitter_info()

tweet_df["tweet_text"] = tweet_df["got_criteria"].apply(lambda x: x.text)
tweet_df["date"] = tweet_df["got_criteria"].apply(lambda x: x.date)
tweet_df["hashtags"] = tweet_df["got_criteria"].apply(lambda x: x.hashtags)
tweet_df["link"] = tweet_df["got_criteria"].apply(lambda x: x.permalink)
tweet_df = tweet_df.drop("got_criteria", 1)
tweet_df.head()

#export
tweet_df.to_csv("Twitter_data.csv")
