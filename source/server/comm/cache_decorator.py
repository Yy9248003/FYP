"""
API响应缓存装饰器
用于缓存频繁查询的API响应，提升性能
"""
from functools import wraps
import hashlib
import json

from django.core.cache import cache
from django.http import JsonResponse


def _get_user_cache_identity(request):
    """获取请求对应的用户缓存标识，防止跨用户缓存污染。"""
    user = getattr(request, 'user', None)
    if not user:
        return 'anonymous'

    if getattr(user, 'is_authenticated', False):
        user_id = getattr(user, 'id', None)
        if user_id is not None:
            return f'user:{user_id}'
        return f'user:{getattr(user, "username", "unknown")}'

    return 'anonymous'


def _safe_json_response_data(response):
    """从JsonResponse中安全解析JSON数据，失败时返回None。"""
    if not hasattr(response, 'content'):
        return None

    try:
        return json.loads(response.content.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError, AttributeError):
        return None

def cache_api_response(timeout=300, key_prefix='api_cache'):
    """
    API响应缓存装饰器
    
    Args:
        timeout: 缓存过期时间（秒），默认5分钟
        key_prefix: 缓存键前缀
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # 生成缓存键
            # 基于请求路径、方法和参数
            cache_key_parts = [
                key_prefix,
                request.path,
                request.method,
                _get_user_cache_identity(request),
            ]
            
            # 添加GET参数
            if request.GET:
                cache_key_parts.append(json.dumps(dict(request.GET), sort_keys=True))
            
            # 添加POST参数（仅用于GET请求的缓存，POST请求不缓存）
            if request.method == 'GET' and request.POST:
                cache_key_parts.append(json.dumps(dict(request.POST), sort_keys=True))
            
            cache_key = hashlib.md5('|'.join(cache_key_parts).encode()).hexdigest()
            full_cache_key = f"{key_prefix}:{cache_key}"
            
            # 尝试从缓存获取
            cached_response = cache.get(full_cache_key)
            if cached_response is not None:
                return JsonResponse(cached_response)
            
            # 执行视图函数
            response = view_func(request, *args, **kwargs)
            
            # 只缓存成功的GET请求
            if request.method == 'GET' and hasattr(response, 'content'):
                response_data = _safe_json_response_data(response)
                # 只缓存成功的响应
                if isinstance(response_data, dict) and response_data.get('code') == 0:
                    cache.set(full_cache_key, response_data, timeout)
            
            return response
        
        return wrapper
    return decorator


def cache_query_result(timeout=300, key_func=None):
    """
    查询结果缓存装饰器
    
    Args:
        timeout: 缓存过期时间（秒）
        key_func: 生成缓存键的函数，接收request参数
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # 生成缓存键
            if key_func:
                cache_key = key_func(request)
            else:
                cache_key = (
                    f"query_cache:{request.path}:{request.method}:"
                    f"{_get_user_cache_identity(request)}"
                )
                if request.GET:
                    cache_key += f":{json.dumps(dict(request.GET), sort_keys=True)}"
            
            # 尝试从缓存获取
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                from app.comm.BaseView import BaseView
                return BaseView.successData(cached_result)
            
            # 执行视图函数
            response = view_func(request, *args, **kwargs)
            
            # 缓存结果（只缓存GET请求的成功响应）
            if request.method == 'GET':
                response_data = _safe_json_response_data(response)
                if isinstance(response_data, dict) and response_data.get('code') == 0:
                    cache.set(cache_key, response_data.get('data'), timeout)
            
            return response
        
        return wrapper
    return decorator
