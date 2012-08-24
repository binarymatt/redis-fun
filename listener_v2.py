import redis
import subprocess

conn = redis.Redis()
pubsub = conn.pubsub()
print 'Listening...'

def play_wat():
    audio_file = "wat.wav"
    subprocess.call(["afplay", audio_file])

def handle_message(message):
    if message['type'] == "message":
        if message['data'] == ".quit":
            pubsub.unsubscribe()
        elif message['data'] == "WAT":
            play_wat()
        else:
            print message['data']

pubsub.subscribe('chat')
for msg in pubsub.listen():
    if msg['type'] == "unsubscribe":
        print 'disconnecting'
        break
    handle_message(msg)



