import redis
import json
import argparse

conn = redis.Redis()
def push(queue, a, b):
    message = {'a': a, 'b': b}
    conn.rpush(queue, json.dumps(message))

parser = argparse.ArgumentParser()
parser.add_argument("a", type=int)
parser.add_argument("b", type=int)
parser.add_argument("--queue", default="test")
args = parser.parse_args()
push(args.queue, args.a, args.b)
