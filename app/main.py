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
data_stream_rules = data_stream.get_rules()

# If the stream returns any rule, remove all of them before adding new ones
if data_stream_rules.data is not None:
    for rule in data_stream_rules[0]:
        data_stream.delete_rules(data_stream_rules[0][0].id)

rules = ['#nfldraft', '#candyonhulu']

# Add all the hashtags requested
for rules in rule:
    data_stream.add_rules(tweepy.StreamRule(rule))

data_stream.filter()
