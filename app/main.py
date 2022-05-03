import auth, tweepy, sys

bearer_key = 'AAAAAAAAAAAAAAAAAAAAADgqWQEAAAAAETWv2Lzb4gljDernmxGs2vAz1dk%3DmyNEMtDFfZxLq8HVDOXZh6M8putog8CpsZ6HADTrCkAIeKo4FR'

class Listener(tweepy.StreamingClient):
    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print('Encountered streaming error (', status, ')')
        sys.exit

data_stream = Listener(bearer_key)
data_stream.add_rules(tweepy.StreamRule('#nfldraft'))
print(data_stream.get_rules())
data_stream.filter()

#session.add_rules(tweepy.StreamRule('nfldraft is:retweet'))

# with open('out.csv', 'w', encoding='utf-8') as f:
#     f.write('date,user,is_retweet,is_quote,text,quoted_text\n')

# hashtags = {'covid', 'nfldraft'}

# for hashtag in hashtags:
#     counts = client.get_recent_tweets_count(query=f'{hashtag} -is:retweet', granularity='day')
#     for count in counts.data:
#         print(hashtag + ' = ' + str(count['tweet_count']))
