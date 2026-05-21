import time


class RequestTimingMiddleware:
    """中间件 1：记录请求处理时间"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        duration = time.time() - start
        print(f'⏱️ [{request.method}] {request.path} → {duration:.3f}s')
        return response


class RequestCountMiddleware:
    """中间件 2：统计请求次数（演示用，真实项目用监控工具）"""
    request_count = 0

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        RequestCountMiddleware.request_count += 1
        print(f'📊 请求 #{RequestCountMiddleware.request_count}')
        response = self.get_response(request)
        return response


class SimpleLogMiddleware:
    """中间件 3：记录所有请求到控制台"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 预处理
        print(f'→ 收到请求: {request.method} {request.path}')

        response = self.get_response(request)

        # 后处理
        print(f'← 返回响应: {response.status_code}')
        return response