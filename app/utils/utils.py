from functools import wraps
import asyncio
import logging
import time
import hashlib

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def async_route(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        logger.debug(f"Starting async handler for {f.__name__}")
        start_time = time.time()
        try:
            result = asyncio.run(f(*args, **kwargs))
            logger.debug(f"Completed {f.__name__} in {time.time() - start_time:.2f}s")
            return result
        except Exception as e:
            logger.error(f"Error in {f.__name__}: {str(e)}")
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
    


