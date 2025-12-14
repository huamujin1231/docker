import redis
import json
from flask import current_app

class RedisClient:
    _instance = None
    
    def __init__(self):
        self.client = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def init_app(self, app):
        try:
            # 优先使用REDIS_URL（Docker环境）
            if 'REDIS_URL' in app.config and app.config['REDIS_URL']:
                self.client = redis.from_url(app.config['REDIS_URL'], decode_responses=True)
            else:
                # 回退到单独配置
                self.client = redis.Redis(
                    host=app.config.get('REDIS_HOST', '127.0.0.1'),
                    port=app.config.get('REDIS_PORT', 6379),
                    db=app.config.get('REDIS_DB', 0),
                    decode_responses=True
                )
        except Exception as e:
            print(f'Redis初始化失败: {e}')
            self.client = None
    
    def cache_product(self, product_id, data, expire=300):
        if not self.client:
            return
        try:
            key = f'product:{product_id}'
            self.client.setex(key, expire, json.dumps(data))
        except:
            pass
    
    def get_product(self, product_id):
        if not self.client:
            return None
        try:
            key = f'product:{product_id}'
            data = self.client.get(key)
            return json.loads(data) if data else None
        except:
            return None
    
    def delete_product(self, product_id):
        if not self.client:
            return
        try:
            key = f'product:{product_id}'
            self.client.delete(key)
        except:
            pass
    
    def cache_cart_count(self, user_id, count):
        if not self.client:
            return
        try:
            key = f'cart_count:{user_id}'
            self.client.setex(key, 600, count)
        except:
            pass
    
    def get_cart_count(self, user_id):
        if not self.client:
            return None
        try:
            key = f'cart_count:{user_id}'
            return self.client.get(key)
        except:
            return None
    
    def clear_all_products(self):
        if not self.client:
            return
        try:
            for key in self.client.scan_iter('product:*'):
                self.client.delete(key)
        except:
            pass
    
    def clear_all_carts(self):
        if not self.client:
            return
        try:
            for key in self.client.scan_iter('cart_count:*'):
                self.client.delete(key)
        except:
            pass
    
    def clear_all_cache(self):
        if not self.client:
            return
        try:
            self.client.flushdb()
        except:
            pass

redis_client = RedisClient.get_instance()
