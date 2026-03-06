"""
统一错误处理模块
提供统一的错误处理装饰器和工具函数
"""
import logging
from functools import wraps
from django.core.cache import cache
from comm.BaseView import BaseView

logger = logging.getLogger('app.views')


def handle_exceptions(func):
    """
    统一异常处理装饰器
    自动捕获异常并返回统一的错误响应
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            logger.warning(f"参数错误 in {func.__name__}: {str(e)}")
            return BaseView.warn(f'参数错误: {str(e)}')
        except Exception as e:
            # 动态导入models避免循环导入
            from app import models
            if hasattr(models, 'Users') and isinstance(e, models.Users.DoesNotExist):
                logger.warning(f"用户不存在 in {func.__name__}")
                return BaseView.error('用户不存在')
            elif hasattr(models, 'DoesNotExist') and isinstance(e, models.DoesNotExist):
                logger.warning(f"数据不存在 in {func.__name__}: {str(e)}")
                return BaseView.error('数据不存在')
            else:
                logger.error(f"系统错误 in {func.__name__}: {str(e)}", exc_info=True)
                return BaseView.error('系统错误，请稍后重试')
    return wrapper


def validate_required_fields(request, fields, method='POST'):
    """
    验证必需字段
    
    Args:
        request: Django请求对象
        fields: 必需字段列表
        method: 请求方法 ('POST' 或 'GET')
        
    Returns:
        tuple: (is_valid, missing_field) - (是否有效, 缺失的字段名)
    """
    data = request.POST if method == 'POST' else request.GET
    
    for field in fields:
        if not data.get(field):
            return False, field
    
    return True, None


def validate_user_token(request):
    """
    验证用户token并返回用户对象
    
    Args:
        request: Django请求对象
        
    Returns:
        tuple: (is_valid, user) - (是否有效, 用户对象或None)
    """
    from app import models
    
    token = request.POST.get('token') or request.GET.get('token')
    if not token:
        return False, None
    
    user_id = cache.get(token)
    if not user_id:
        return False, None
    
    try:
        user = models.Users.objects.filter(id=user_id).first()
        if not user:
            return False, None
        return True, user
    except Exception:
        return False, None


def sanitize_input(text, max_length=None, allowed_chars=None):
    """
    清理输入文本
    
    Args:
        text: 输入文本
        max_length: 最大长度
        allowed_chars: 允许的字符（正则表达式）
        
    Returns:
        str: 清理后的文本
    """
    if not text:
        return ''
    
    import re
    
    # 移除危险字符
    if allowed_chars:
        text = re.sub(f'[^{allowed_chars}]', '', text)
    
    # 限制长度
    if max_length:
        text = text[:max_length]
    
    return text.strip()
