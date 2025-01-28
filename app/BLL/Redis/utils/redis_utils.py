import redis
import simplejson

CHANNELS = ['routes_share.update', 'request_route.update', 'notification.update', 'user.update', 'schedule_managements.update', 'roadmap_request.update']
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

redis_client.set('users', simplejson.dumps(obj=[]))