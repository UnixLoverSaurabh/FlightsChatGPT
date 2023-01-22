import redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)


def get_next_message():
    message = redis_client.brpop('messages', timeout=0)
    if message:
        return message[1].decode()
    else:
        return None
