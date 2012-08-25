import os
import redis
import argparse
import json

conn = redis.Redis()
def job(a, b):
    print a + b
class Worker():
    def __init__(self, queue):
        self.queue = queue
        self.pid = os.getpid()
        self.hostname = os.uname()[1]
        self.id = '%s-%s' % (self.hostname, self.pid)

    def register(self):
        print 'Registering: %s' % self.id
        conn.sadd('%s:workers' % self.queue, self.id)
        conn.zadd('%s:leaderboard' % self.queue, self.id, 0)

    def deregister(self):
        conn.srem('%s:workers', self.queue, self.id)

    def success_stat(self):
        #queue stats
        conn.incr('%s:success' % self.queue)
        #worker stats
        worker_score = conn.incr('%s:success' % self.id)
        #leaderboard
        conn.zadd('%s:leaderboard' % self.queue, self.id, worker_score)

    def failure(self):
        conn.incr('%s:failures' % self.queue)

    def check_commands(self):
        print 'Checking commands: %s:commands' % self.id
        command = conn.lpop('%s:commands' % self.id)
        if command and command == 'stop':
            print 'Stopping...'
            return False
        return True

    def work(self):
        self.register()
        while self.check_commands():
            print 'Listening...'
            message = conn.blpop(self.queue, 5)
            if message:
                print 'Message %s received on worker %s' % (message, self.id)
                content = message[1]
                kwargs = json.loads(content)
                job(**kwargs)
                self.success_stat()
        self.deregister()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("queue")
    args = parser.parse_args()
    worker = Worker(args.queue)
    worker.work()
