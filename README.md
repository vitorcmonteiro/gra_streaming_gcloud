# Introduction
The goal of this tutorial is to create a data streaming from Twitter. This data is usefull for a broad range of analysis such as Sentiment Analysis[^1], Community Detection[^2], and much more. These analysis are powerful tools that enable companies to visualize potential targets for an advertisement or avoid fraud in digital purchases.

We will go through the setup of a local machine to receive the tweets and then we will setup a Google Cloud instance to avoid costs while tinkering with the setup and code.

# Table of Contents
1. [Tech Stack](#tech-stack)
2. [Create Data Streaming](#create-data-streaming)
3. []

# Streaming data from Twitter

## **Tech Stack**
* Ubuntu 20.04
* VS Code
* Python
    * Tweepy

I'm using a development evironment in WSL 2 (Ubuntu) and the only Python package we will need is called Tweepy.
</br></br>

## **Create Data Streaming (Extract)**
### *Create Twitter Developer Account*
Before we go ahead with the solution itself, you must first ![create a Developer Account](https://developer.twitter.com/en) so that you have access to API keys needed to pull data from Twitter's Servers. This approval may be quick or take a couple days but it is usually instantaneous.

After creating your account, add an app to your account. I named mine as "analytics-gra". This action enables you to grab Consumer Keys and Authentication Tokens.

[create-app]

Generate a **Bearer Token** under Authentication Tokens section and safekeep that information to be used in our code.

[auth-tokens]

Remember that there is a monthly limit of usage. When we connect to Twitter's API and download the data we have a running count that is capped at 2M Tweets per month. </br>

### Connect to Twitter API
With the token in hands we will now connect to Twitter's API and get some tweets from the trending topics. We are able to connect it through Tweepy's class named ``StreamingClient``[^3]

```python
# main.py
import tweepy, sys

bearer_key = '<insert bearer key>'

class Listener(tweepy.StreamingClient):
    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print('Encountered streaming error (', status, ')')
        sys.exit
```

The ``Listener`` class we created overrides the original ``StreamingClient`` class from ``Tweepy``. The ``on_data`` - originally from ``StreamingClient`` - function is called when a tweet is recevieved and we are printing just to see the incoming data and confirm that our connection is working.
</br>

### Add hashtag and print tweets
Now for the next part of the code, let's keep working on ``main.py`` file. The idea is to follow this simple flow:

1. Connect to Twitter;
2. Get rules saved (filters) on our session; 
3. Remove all of them if they exist;
4. List all rules (like a query) we want to stream from;
5. Recursively add rules to the stream and run it.

So we go ahead and edit ``main.py`` to be like the following code (You can refer to the ``main.py`` file in this repository):

```python
import auth, tweepy, sys

bearer_key = '<insert bearer key>'

class Listener(tweepy.StreamingClient):
    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print('Encountered streaming error (', status, ')')
        sys.exit

# 1. Connect to Twitter;
data_stream = Listener(bearer_key)

# 2. Get rules saved (filters) on our session;
data_stream_rules = data_stream.get_rules()

# 3. Remove all of them if they exist;
if data_stream_rules.data is not None:
    for rule in data_stream_rules[0]:
        data_stream.delete_rules(data_stream_rules[0][0].id)

# 4. List all rules (like a query) we want to stream from;
rules = ['#nfldraft', '#candyonhulu']

# 5. Recursively add rules to the stream and run it.
for rules in rule:
    data_stream.add_rules(tweepy.StreamRule(rule))

data_stream.filter()
```

To determine which hashtags I usually use the trending topics just to grab the ones with the highest throughoutput. You should also refer back to Twitter's API documentation to understand what we can do with these rules.

After running this code for a few seconds you should see that you started consuming your Tweet cap and start getting responses in your console:

[first-results]

This means that we are receiveing response from Twitter and we are now able to work on processing the data or transforming it to a more readable format and store it somewhere.

</br></br>

## Process streaming data (Transform)

## Visualize streaming data

## Google Cloud
### Overview
### Create Compute Engine (Extract)
### Pub/Sub Topic (Transform)
### Create Bucket (Transform)
### Create DataFlow (Transform)
### Visualize with Bokeh


Create Data Streaming
data streaming (compute engine or local)</br>
    Local</br>
    GCloud</br>
process streaming data with dataflow</br>
    Create Service Account</br>
    Create Pub/Sub Topic</br>
        Create Pub/Sub Topic</br>
        Save Pub/Sub Subscription Name</br>
    Create Bucket</br>
    Create DataFlow</br>

visualize with bokeh</br>

https://medium.com/google-cloud/apache-spark-and-jupyter-notebooks-made-easy-with-dataproc-component-gateway-fa91d48d6a5a</br>
https://medium.com/datareply/realtime-streaming-data-pipeline-using-google-cloud-platform-and-bokeh-9dd0cfae647a (Doesn't explain how to build your first pipeline from Twitter)</br>
https://medium.com/google-cloud/twitter-analytics-part-1-801c9d494487 (Missing the streaming.py code)</br>
https://medium.com/google-cloud/twitter-analytics-part-2-f282c49c6de7 (Dependant on part 1)</br>
https://datatonic.com/insights/real-time-streaming-predictions-using-google-cloud-dataflow-and-google-cloud-machine-learning/</br>
https://www.storybench.org/how-to-collect-tweets-from-the-twitter-streaming-api-using-python/</br>
https://pythonprogramming.net/twitter-stream-sentiment-analysis-python/</br>

Cookbook of Tweepy: https://dev.to/twitterdev/a-comprehensive-guide-for-using-the-twitter-api-v2-using-tweepy-in-python-15d9</br>

[^1]: ![Twitter Sentiment Analysis in Real-Time](https://monkeylearn.com/blog/sentiment-analysis-of-twitter/)</br>
[^2]: ![Generating A Twitter Ego-Network & Detecting Communities](https://towardsdatascience.com/generating-twitter-ego-networks-detecting-ego-communities-93897883d255)</br>
[^3]: ![Tweepy Documentation](https://docs.tweepy.org/en/stable/)
