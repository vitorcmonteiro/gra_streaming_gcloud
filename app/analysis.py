# batch_analysis.py

import json
import pandas as pd

tweets_data_path = '/home/vitorcmonteiro/repos/gra_streaming_gcloud/app/twitter_data.txt'
tweets_data = []
tweets_file = open(tweets_data_path, 'r').read().splitlines() # Open txt file in read-only

# Consolidate each txt line into a single json
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue

# Create Pandas DataFrame and map data to its columns
tweets = pd.DataFrame()
tweets['text'] = list(map(lambda tweet: tweet['data']['text'], tweets_data))

# For this data, I wanted to gather what rule we used to get that tweet so you need to 
# evaluate the txt file data structure and you will see that this id comes from that structure (['matching_rules'][0]['id'])
tweets['matching_rule_id'] = list(map(lambda tweet: tweet['matching_rules'][0]['id'], tweets_data)) 

print(tweets.head())