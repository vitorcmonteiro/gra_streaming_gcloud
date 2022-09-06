import os
from google.cloud.pubsublite.cloudpubsub import SubscriberClient
from google.cloud.pubsublite.types import CloudZone, CloudRegion, SubscriptionPath, FlowControlSettings, MessageMetadata
from google.cloud.pubsublite import PubSubMessage

# Google Cloud Settings
cloud_region = 'us-east1'
zone_id = 'b'
project_number = '920873209776'
subscription_id = 'twitter-subscription'
timeout = 90

#Credentials folder, change it to match yours.
credentials = '/home/vitorcmonteiro/repos/gra_streaming_gcloud/credentials'

# Load credentials from files
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f'{credentials}/gra-346616-4dff1bef0aff.json'

# Google Cloud configurations required to connect
location = CloudZone(CloudRegion(cloud_region), zone_id)
subscription_path = SubscriptionPath(project_number, location, subscription_id)
per_partition_flow_control_settings = FlowControlSettings(
    messages_outstanding = 1000,
    bytes_outstanding = 10 * 1024 * 1024,
)

# Main functioned called when object SubscriberClient is called
# It is responsible for all transformations and flow of the Subscription.
def callback(message: PubSubMessage):
    message_data = message.data.decode('utf-8')
    metadata = MessageMetadata.decode(message.message_id)
    print(
        f'Received {message_data} of ordering key {message.ordering_key} with id {metadata}.'
    )
    message.ack()

# This code part controls the flow of the Subscriber itself, if we didn't specify that print in the callback function, we would
# just see a froze "Linestening for messages on...".
with SubscriberClient() as subscriber_client:
    streaming_pull_future = subscriber_client.subscribe(
        subscription_path,
        callback=callback,
        per_partition_flow_control_settings=per_partition_flow_control_settings,
    )

    print(f'Listening for messages on {str(subscription_path)}...')

    try:
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError or KeyboardInterrupt:
        streaming_pull_future.cancel()
        assert streaming_pull_future.done()