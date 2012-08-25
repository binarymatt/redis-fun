import redis
import argparse

conn = redis.Redis()
parser = argparse.ArgumentParser()
parser.add_argument("queue")
args = parser.parse_args()
#get all workers for queue
workers = conn.smembers('%s:workers' % args.queue)
for worker in workers:
    print worker
    conn.lpush('%s:commands' % worker, 'stop')

