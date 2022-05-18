import json
import pandas as pd

tweets_data_path = '/home/vitorcmonteiro/repos/gra_streaming_gcloud/app/twitter_data.txt'
tweets_data = []
tweets_file = open(tweets_data_path, 'r')

for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue

tweets = pd.DataFrame()
tweets['text'] = list(map(lambda tweet: tweet['data']['text'], tweets_data))
tweets['matching_rule_id'] = list(map(lambda tweet: tweet['matching_rules'][0]['id'], tweets_data))

print(tweets.head())