import redis
import argparse

conn = redis.Redis()
#show leaderboard
def stats(queue):
    #queue stats
    print '%s jobs have been run from %s' % (conn.get('%s:success' % queue), queue)
    #leaders
    leaders = conn.zrange('%s:leaderboard' % queue, 0, 10, desc=True, withscores=True)
    print 'Leaders'
    for item in leaders:
        print '%s %s' % (item[0], item[1])

parser = argparse.ArgumentParser()
parser.add_argument("queue", default="test")
args = parser.parse_args()
stats(args.queue)
