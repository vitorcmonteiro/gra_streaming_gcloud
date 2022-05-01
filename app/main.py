import tweepy

# API Key wOsjtdD5xNwLvAjjYEYi5o80a
# API Key Secret foxzypMH9johyIu16KDXWsGeglEc7k4iAFKyTJ8UusgLRtWvlj
# Access Token 1451977262283247617-YRXscvI59Ln9Y5wHmRdO9KtD4Heix8
# Access Token Secret 3vxJl6PT9n6uBHIypqUM2lpIdiYMICr5MCKZznbe3xvWU

client = tweepy.Client('AAAAAAAAAAAAAAAAAAAAADgqWQEAAAAAETWv2Lzb4gljDernmxGs2vAz1dk%3DmyNEMtDFfZxLq8HVDOXZh6M8putog8CpsZ6HADTrCkAIeKo4FR')
hashtags = {'covid', 'nfldraft'}

for hashtag in hashtags:
    counts = client.get_recent_tweets_count(query=f'{hashtag} -is:retweet', granularity='day')
    for count in counts.data:
        print(hashtag + ' = ' + str(count['tweet_count']))
