import tweepy, sys

bearer_key = 'AAAAAAAAAAAAAAAAAAAAADgqWQEAAAAAETWv2Lzb4gljDernmxGs2vAz1dk%3DmyNEMtDFfZxLq8HVDOXZh6M8putog8CpsZ6HADTrCkAIeKo4FR'

tweet_count = 0
num_tweets = 10

class Listener(tweepy.StreamingClient):
    def on_data(self, data):
        global tweet_count
        global num_tweets

        if tweet_count < num_tweets:
            print(data)
            tweet_count += 1
            return True
        else:
            self.disconnect()

    def on_error(self, status):
        print('Encountered streaming error (', status, ')')
        sys.exit

data_stream = Listener(bearer_key)
data_stream_rules = data_stream.get_rules()

# If the stream returns any rule, remove all of them before adding new ones
if data_stream_rules.data is not None:
    for rule in data_stream_rules[0]:
        data_stream.delete_rules(data_stream_rules[0][0].id)

rules = ['#ufcvegas54', '#creatorclash']

# Add all the hashtags requested
for rule in rules:
    data_stream.add_rules(tweepy.StreamRule(rule))

data_stream.filter()
