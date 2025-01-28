from functools import wraps
import asyncio
import logging
import time
import hashlib
from datetime import datetime


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def async_route(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            result = asyncio.run(f(*args, **kwargs))
            return result
        except Exception as e:
            raise
    return wrapper


class Helper():
    @staticmethod
    def generate_hash_md5(*args: str):
        hash_object = hashlib.md5()
        for data in args:
            hash_object.update(data.encode())
        
        return hash_object.hexdigest()
    
    @staticmethod
    def sorted_combine_id_to_str(*args: int):
        id_tuple_sorted = sorted(args)
        return f'{id_tuple_sorted}'.replace('(', '[').replace(')', ']')
    
    @staticmethod
    def convert_datetime_iso(datetime_str: str) -> datetime:
        timestamp_ms = int(datetime_str) / 1000
        dt = datetime.fromtimestamp(timestamp_ms)

        return dt
    


