"""服务层与通用装饰器测试。"""

import json
from types import SimpleNamespace

from django.core.cache import cache
from django.http import JsonResponse, HttpResponse
from django.test import RequestFactory, SimpleTestCase

from comm.cache_decorator import cache_api_response


class CacheDecoratorTestCase(SimpleTestCase):
    """验证缓存装饰器的关键行为。"""

    def setUp(self):
        self.factory = RequestFactory()
        cache.clear()

    def tearDown(self):
        cache.clear()

    def test_cache_isolated_by_authenticated_user(self):
        """同一路径请求应按用户隔离缓存，避免跨用户数据污染。"""
        counter = {'value': 0}

        @cache_api_response(timeout=60, key_prefix='test_api')
        def sample_view(request):
            counter['value'] += 1
            return JsonResponse({'code': 0, 'data': {'counter': counter['value']}})

        req_user_1_a = self.factory.get('/api/mock/info/', {'q': 'same'})
        req_user_1_a.user = SimpleNamespace(is_authenticated=True, id='u1', username='user1')

        req_user_2 = self.factory.get('/api/mock/info/', {'q': 'same'})
        req_user_2.user = SimpleNamespace(is_authenticated=True, id='u2', username='user2')

        req_user_1_b = self.factory.get('/api/mock/info/', {'q': 'same'})
        req_user_1_b.user = SimpleNamespace(is_authenticated=True, id='u1', username='user1')

        response_1 = sample_view(req_user_1_a)
        response_2 = sample_view(req_user_2)
        response_3 = sample_view(req_user_1_b)

        data_1 = json.loads(response_1.content)
        data_2 = json.loads(response_2.content)
        data_3 = json.loads(response_3.content)

        self.assertEqual(data_1['data']['counter'], 1)
        self.assertEqual(data_2['data']['counter'], 2)
        self.assertEqual(data_3['data']['counter'], 1)
        self.assertEqual(counter['value'], 2)

    def test_invalid_json_response_is_not_cached(self):
        """非JSON响应内容不应进入缓存，且不应抛异常。"""
        counter = {'value': 0}

        @cache_api_response(timeout=60, key_prefix='test_non_json')
        def invalid_json_view(request):
            counter['value'] += 1
            return HttpResponse('not-json-response', content_type='text/plain')

        request = self.factory.get('/api/mock/non-json/')
        request.user = SimpleNamespace(is_authenticated=False)

        invalid_json_view(request)
        invalid_json_view(request)

        self.assertEqual(counter['value'], 2)
