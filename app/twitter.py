import auth, tweepy, sys

class Listener(tweepy.StreamingClient):
    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print('Encountered streaming error (', status, ')')
        sys.exit