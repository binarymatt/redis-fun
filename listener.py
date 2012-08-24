import redis

conn = redis.Redis()
pubsub = conn.pubsub()
print 'Listening...'

def handle_message(message):
    if message['type'] == "message":
        if message['data'] == ".quit":
            pubsub.unsubscribe()
        else:
            print message['data']

pubsub.subscribe('chat')
for msg in pubsub.listen():
    if msg['type'] == "unsubscribe":
        print 'disconnecting'
        break
    handle_message(msg)
