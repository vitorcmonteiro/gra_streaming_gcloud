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
    * Tweepy (pip install tweepy)
    * Pandas (pip install pandas)
    * Matplotlib (pip install matplotlib)

I'm using a development evironment in WSL 2 (Ubuntu) and the only Python package we will need is called Tweepy.

This is an example of the infrastructure that we are creating at Google Cloud[^3].

![Infrastructure](https://user-images.githubusercontent.com/22838513/169104325-907363f7-6626-4c75-8de2-bdf73f58fc52.png)

</br></br>

## **Create Data Streaming (Extract)**
### *Create Twitter Developer Account*
Before we go ahead with the solution itself, you must first ![create a Developer Account](https://developer.twitter.com/en) so that you have access to API keys needed to pull data from Twitter's Servers. This approval may be quick or take a couple days but it is usually instantaneous.

After creating your account, add an app to your account. I named mine as "analytics-gra". This action enables you to grab Consumer Keys and Authentication Tokens.

![Developer Dashboard](https://user-images.githubusercontent.com/22838513/167897083-d429c517-5c41-4981-82c1-6408483caf66.png)

Generate a **Bearer Token** under Authentication Tokens section and safekeep that information to be used in our code.

![Authentication tokens](https://user-images.githubusercontent.com/22838513/167897153-7998ee7c-9274-46dd-9caa-765b13dee034.png)

Remember that there is a monthly limit of usage. When we connect to Twitter's API and download the data we have a running count that is capped at 2M Tweets per month. </br>

### *Connect to Twitter API*
With the token in hands we will now connect to Twitter's API and get some tweets from the trending topics. We are able to connect it through Tweepy's class named ``StreamingClient``[^4].

Remember to install tweepy package (``pip install tweepy``) in your environment.

```python
# main.py
import tweepy, sys

bearer_key = '<insert bearer key>'

# Variables used to close connection when the desired number of tweets is achieved
tweet_count = 0
num_tweets = 10

class Listener(tweepy.StreamingClient):
    def on_data(self, data):
        global tweet_count
        global num_tweets
        global stream

        if tweet_count < num_tweets:
            print(data)
            tweet_count += 1
            return True
        else:
            stream.disconnect()

    def on_error(self, status):
        print('Encountered streaming error (', status, ')')
        sys.exit
```

The ``Listener`` class we created overrides the original ``StreamingClient`` class from ``Tweepy``. The ``on_data`` - originally from ``StreamingClient`` - function is called when a tweet is recevieved and we are printing just to see the incoming data and confirm that our connection is working.
</br>

### Add hashtag and print tweets
Now for the next part of the code, let's keep working on ``main.py`` file. The idea is to follow these steps:

1. Connect to Twitter;
2. Get rules saved (filters) on our session; 
3. Remove all of them if they exist;
4. List all rules (like a query) we want to stream from;
5. Recursively add rules to the stream and run it.

So we go ahead and add to ``main.py`` below the new ``Class`` we created the following code (You can refer to the ``main.py`` file in this repository):

```python
# main.py

# 1. Connect to Twitter;
data_stream = Listener(bearer_key)

# 2. Get rules saved (filters) on our session;
data_stream_rules = data_stream.get_rules()

# 3. Remove all of them if they exist;
if data_stream_rules.data is not None:
    for rule in data_stream_rules[0]:
        data_stream.delete_rules(data_stream_rules[0][0].id)

# 4. List all rules (like a query) we want to stream from;
rules = ['#ufcvegas54', '#creatorclash']

# 5. Recursively add rules to the stream and run it.
for rules in rule:
    data_stream.add_rules(tweepy.StreamRule(rule))

data_stream.filter()
```

To determine which hashtags I usually use the trending topics just to grab the ones with the highest throughoutput. You should also refer back to Twitter's API documentation to understand what we can do with these rules.

After running this code for a few seconds you should see that you started consuming your Tweet cap and start getting responses in your console:

![Results](https://user-images.githubusercontent.com/22838513/167897299-da686def-1e07-4dd6-a350-b6e7010b3565.png)

This means that we are receiveing response from Twitter and we are now able to work on processing the data or transforming it to a more readable format and store it somewhere. We will get into details of data structure in the next section.

If you want to write these responses to a file just run this command ``python3 main.py > twitter_data.txt`` and this will save the entire response to the txt file. You can customize which fields should be included in the response but we will go through it in the following sections.

Now commit your changes to a GitHub repository that you can manage Access Keys so that we can pull these files into our VM - that we will create below.
</br></br>

## Process streaming data (Transform)
To read data both locally and on Google Cloud we will use ``Pandas`` so remember to install it aswell (``pip install pandas``) before proceeding.

Create a file called ``analysis.py`` to read the text file we created and then show it as a table that we can transform with ``Pandas``.

```python
# analysis.py

import json
import pandas as pd

tweets_data_path = '<complete path to your file>'
tweets_data = []
tweets_file = open(tweets_data_path, 'r') # Open txt file in read-only

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
```

![Twitter stream results in pandas](https://user-images.githubusercontent.com/22838513/169099262-ef6eb95f-8a4a-40ea-879f-88fbc8fdcfc4.png)


We didn't visualize anything at this point (Like a chart) because we will do that in Google Cloud using Bokeh. So we just showed here that we are able to read incoming data as a table in Pandas. </br></br>


# Migrating to Google Cloud
We will now migrate our local solution to [!Google Cloud](https://cloud.google.com/) so please create your account before proceding. Before we begin we should follow a few configuration steps. These are very similar to AWS' IAM account and access key creation.

## **Before we begin**
The following steps should be completed before going forward, except for the step 5 which we will go through in details[^5]:

1. Create a [!Google Cloud project](https://cloud.google.com/resource-manager/docs/creating-managing-projects) </br>
2. [!Enable the Pub/Sub Lite API](https://console.cloud.google.com/flows/enableapi?apiid=pubsublite.googleapis.com) </br>
3. Create a service account </br>
4. Create a service account key </br>
5. Set environment variable GOOGLE_APPLICATION_CREDENTIALS </br></br>

### **Create service account**
When creating the service account, add two different roles that you can see below:

![Project owner](https://user-images.githubusercontent.com/22838513/169102045-5e56343a-bb03-415c-9c16-d72ad4015a1a.png)

![PubSub admin](https://user-images.githubusercontent.com/22838513/169102117-547c60ef-1779-4f18-97b8-41e95d967447.png)

Now create the account and you should see something similar to the image below:

![Service account created](https://user-images.githubusercontent.com/22838513/169103716-3995a5b4-4864-4d26-942f-365bc49f4acc.png)

### **Create a service account key**
After creating the service account, click on the account email and browse to the Keys tab. Create a new key. It will generate a JSON file and you may save it in somewhere you will remember.

![Creat key](https://user-images.githubusercontent.com/22838513/169103992-4d4e6f60-a538-401c-90ba-10ff36a39729.png)

You can use this key locally or in the Cloud as it is your key to the services. The process is the same for both, just make sure you are in the correct terminal of the machine you want to install these keys. Since we are working with Google Cloud, we will add this key to our cloud VM below. </br></br>

### **Create Compute Engine (Extract)**
This service is used to create Cloud Virtual Machines that will run our app (code) while the machine is running.  It is possible to launch them automatically but to control the costs I decided to launch it manually.

It will authenticate and pull tweets from Twitter using the code we create before (main.py). The first step is to enter the Compute Engine console by searching "Compute Engine" in Google Cloud's search.

![Search for Compute Engine](https://user-images.githubusercontent.com/22838513/169104039-ff42326e-12d4-45dc-a015-eaa1fe422528.png)

Create a new instance of the e2-micro type (Least expensive) and under Boot disk **change the Boot disk type to "Standard persistent disk"**, this should decrease the costs of running the machine. You can see the specs below for quick reference, but I have only changed the machine type and the rest is standard.

![VM configuration](https://user-images.githubusercontent.com/22838513/169104096-4ce72de6-6c3a-43af-97b0-c458923f3875.png)

![Standard disk](https://user-images.githubusercontent.com/22838513/169104214-46b73b48-6d08-49aa-a47a-32da547bb93b.png)

Remember to stop the machine after you are done because it is paid by the hour that it is running - unlike AWS that would account for only when used.

Wait until your machine is running and you may now SSH into your recently created VM.

![ssh](https://user-images.githubusercontent.com/22838513/169130964-e1c424aa-6382-49d6-b7f1-6d85592b0899.png)

### **Setting up Credentials**
Going back to our "Before we begin" section, we will now setup the credentials we have created before. These credentials could be installed in both local or Cloud settings like I mentioned before, just repeat the same steps on your Virtual Machine and you will be able to acomplish the same task within Cloud.

In your Linux Terminal create the following evironment variable with the full path for the JSON file you have downloaded from Google Cloud after creating your service account.

```Console
$ export GOOGLE_APPLICATION_CREDENTIALS="KEY_PATH"
```

Double check if the value is correct with:

```Console
$ echo $GOOGLE_APPLICATION_CREDENTIALS
```

### Installing tools and packages
Now with access to a VM, we will need to install pip and other tools in order to run our code successfully[^6]. Follow the steps included in that link (Installing Python section) and then install the Python the following packages: ``tweepy``, ``matplotlib``, and ``pandas``.

```
$ pip install tweepy
```

```Console
$ pip install matplotlib
```

```Console
$ pip install pandas
```

From the console that opened we can now download our project files from GitHub, so please create one repository for you and upload your project files.

If the ``git`` command is not found, run this first ``sudo apt-get install git`` to install Git. Then create any folder you want to store your project and run the following:

- ``git init`` - to start a repository at that folder </br>
- ``git pull <repository address>`` - and this should pull all the files from the repository you stored your files </br>
(remember to create your personal access token[^7] and use it as your password) </br></br>

### Create Pub/Sub Lite Reservation
Pub/Sub is a message queue app that enables asynchronous integration between aplications [^8]. It will manage the streaming data from Twitter and continuously transmit data down the stream we will create. There's also a service called Pub/Sub Lite that is specifically built for lower cost and that's the one we are using since we don't need high throughput and reliability.

In our case we will use Pub/Sub Lite Reservations since we don't require high reliability due to this being a test.

### Create Bucket (Transform)
### Create DataFlow (Transform)
### Visualize with Bokeh


# References
[^1]: ![Twitter Sentiment Analysis in Real-Time](https://monkeylearn.com/blog/sentiment-analysis-of-twitter/) </br>
[^2]: ![Generating A Twitter Ego-Network & Detecting Communities](https://towardsdatascience.com/generating-twitter-ego-networks-detecting-ego-communities-93897883d255) </br>
[^3]: ![Realtime Streaming Data Pipeline using Google Cloud Platform and Bokeh](https://medium.com/datareply/realtime-streaming-data-pipeline-using-google-cloud-platform-and-bokeh-9dd0cfae647a) </br>
[^4]: ![Tweepy Documentation](https://docs.tweepy.org/en/stable/) </br>
[^5]: ![Before you begin](https://cloud.google.com/pubsub/lite/docs/publish-receive-messages-console#before-you-begin) </br>
[^6]: ![Setting up a Python development environment](https://cloud.google.com/python/docs/setup#installing_python) </br>
[^7]: ![Creating a personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) </br>
[^8]: ![What is Pub/Sub?](https://cloud.google.com/pubsub/docs/overview) </br>

# Additional Resources
https://medium.com/datareply/realtime-streaming-data-pipeline-using-google-cloud-platform-and-bokeh-9dd0cfae647a (Doesn't explain how to build your first pipeline from Twitter)</br>
https://medium.com/google-cloud/twitter-analytics-part-1-801c9d494487 </br>
https://medium.com/google-cloud/twitter-analytics-part-2-f282c49c6de7 </br>
https://datatonic.com/insights/real-time-streaming-predictions-using-google-cloud-dataflow-and-google-cloud-machine-learning/</br>
https://www.storybench.org/how-to-collect-tweets-from-the-twitter-streaming-api-using-python/</br>
https://pythonprogramming.net/twitter-stream-sentiment-analysis-python/</br>
https://z-ai.medium.com/downloading-data-from-twitter-using-the-streaming-api-3ac6766ba96c</br>
https://developer.twitter.com/en/docs/twitter-api/data-dictionary/introduction</br>

1. [!Tweepy Cookbook](https://dev.to/twitterdev/a-comprehensive-guide-for-using-the-twitter-api-v2-using-tweepy-in-python-15d9) </br>
2. [!Stream messages from Pub/Sub by using Dataflow](https://cloud.google.com/pubsub/docs/stream-messages-dataflow) </br>
3. [!Setting up a GCP Pub/Sub Integration with Python](http://www.theappliedarchitect.com/setting-up-gcp-pub-sub-integration-with-python/) </br>
4. [!Apache Spark and Jupyter Notebooks made easy with Dataproc component gateway](https://medium.com/google-cloud/apache-spark-and-jupyter-notebooks-made-easy-with-dataproc-component-gateway-fa91d48d6a5a) </br>
5. [!Publish and receive messages in Pub/Sub Lite by using the Cloud console](https://cloud.google.com/pubsub/lite/docs/publish-receive-messages-console) </br>
