import redis
import time
conn = redis.Redis()
begin = time.time()
for i in range(1000000):
    conn.set('key%s' % i, "test key")
print time.time()
end = time.time()
print '%s number of seconds to insert 1million records' end-begin
print '%s operations per second' % 1000000.0/(end-begin)
print conn.info()['used_memory_human']
