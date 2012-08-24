import redis
import argparse
conn = redis.Redis()
parser = argparse.ArgumentParser()
parser.add_argument("message")
args = parser.parse_args()

conn.publish('chat', args.message)
