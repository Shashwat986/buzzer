from birdy.twitter import AppClient

CONSUMER_KEY = 'lZc5Z5qGNZJTi8n5329g'
CONSUMER_SECRET = 'enRXRLMs8i2xYKMkmgxjFckXqOvcPV9bZ2JMaXRoGI'

def login():
    client = AppClient(CONSUMER_KEY, CONSUMER_SECRET)
    access_token = client.get_access_token()
    return client

