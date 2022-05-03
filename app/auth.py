import tweepy

# API Key wOsjtdD5xNwLvAjjYEYi5o80a
# API Key Secret foxzypMH9johyIu16KDXWsGeglEc7k4iAFKyTJ8UusgLRtWvlj
# Access Token 1451977262283247617-YRXscvI59Ln9Y5wHmRdO9KtD4Heix8
# Access Token Secret 3vxJl6PT9n6uBHIypqUM2lpIdiYMICr5MCKZznbe3xvWU

bearer_key = 'AAAAAAAAAAAAAAAAAAAAADgqWQEAAAAAETWv2Lzb4gljDernmxGs2vAz1dk%3DmyNEMtDFfZxLq8HVDOXZh6M8putog8CpsZ6HADTrCkAIeKo4FR'

def Batch():
    auth = tweepy.Client(bearer_token=bearer_key)
    return auth

def Stream():
    auth = tweepy.StreamingClient(bearer_token=bearer_key)
    return auth