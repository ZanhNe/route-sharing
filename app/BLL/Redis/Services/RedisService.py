from app.BLL.Redis.Interfaces.IRedisService import IRedisService
from app.Socket.handlers.Interfaces.ISocketHandler import ISocketHandler
from typing import List
from redis import Redis
import time
import simplejson

class RedisService(IRedisService):

    def __init__(self, redis_client: Redis, socket_handler: ISocketHandler):
        self.redis_client = redis_client
        self.socket_handler = socket_handler

    def set_value(self, key, value):
        self.redis_client.set(name=key, value=value)
    
    def get_value(self, key):
        return self.redis_client.get(name=key)
    
    def start_subsrcibe(self, channels: List[str]):
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe(*channels)

        print("Subscribe channel")

        while True:
            message = pubsub.get_message(ignore_subscribe_messages=True)
            if (not message):
                time.sleep(0.1)
            else:
                try:
                    data = simplejson.loads(message['data'])
                    if ('send_to' in data):
                        self.socket_handler.handlers[message['channel']](data['payload'], self.redis_client.get(f'user_sid:{data['send_to']}'))
                    else:
                        self.socket_handler.handlers[message['channel']](data['payload'])
                except Exception as e:
                    print(e)        