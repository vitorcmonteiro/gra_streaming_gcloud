import tweepy, sys, os
from google.cloud.pubsublite.cloudpubsub import PublisherClient
from google.cloud.pubsublite.types import CloudRegion, CloudZone, MessageMetadata, TopicPath

# Google Cloud Settings
cloud_region = 'us-east1'
zone_id = 'b'
project_number = '920873209776'
topic_id = 'tweets'

# Twitter stream limits
tweet_count = 0
num_tweets = 10

#Credentials folder, change it to match yours.
credentials = '/home/vitorcmonteiro/repos/gra_streaming_gcloud/credentials'

# Load credentials from files
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f'{credentials}/gra-346616-cdedbe380d9a.json'
bearer_key = open(f'{credentials}/twitter', 'r').readline()

location = CloudZone(CloudRegion(cloud_region), zone_id)
topic_path = TopicPath(project_number, location, topic_id)

class Listener(tweepy.StreamingClient):
    def on_data(self, data):
        global tweet_count
        global num_tweets

        if tweet_count < num_tweets:
            with PublisherClient() as publisher_client:
                api_future = publisher_client.publish(topic_path, data)
                message_id = api_future.result()
                message_metadata = MessageMetadata.decode(message_id)
                print(
                    f"Published a message to {topic_path} with partition {message_metadata.partition.value} and offset {message_metadata.cursor.offset}."
                )
            print(data.decode('utf-8'))
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

rules = ['#NationalRescueDogDay -is:retweet', '#StreamingDay -is:retweet']

# Add all the hashtags requested
for rule in rules:
    data_stream.add_rules(tweepy.StreamRule(rule))

data_stream.filter()
