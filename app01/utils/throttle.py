"""
自定义的访问限制类
"""
from rest_framework.throttling import BaseThrottle, SimpleRateThrottle
import time

D = {}


class MyThrottle(BaseThrottle):

    def allow_request(self, request, view):
        """
       返回True就放行， 返回False表示被限制了
        """
        # 1 获取当前的访问IP
        ip = request.META.get("REMOTE_ADDR")
        print("这是自定义限制类中的allow_request")
        print(ip)
        # 2 获取当前的时间
        now = time.time()
        # 判断当前ip是否由访问记录
        if ip not in D:
            D[ip] = []  # 初始化一个空的访问历史列表
        # 高端操作
        history = D[ip]
        while history and now - history[-1] > 10:
            history.pop()
        # 判断最近一分钟的访问次数是否超过了阈值 （3次）
        if len(history) >= 3:
            return False
        else:
            # 把这一次的访问时间加到访问历史列表的第一位
            D[ip].insert(0, now)
            return True


class VisitThrottle(SimpleRateThrottle):
    scope = "xxx"

    def get_cache_key(self, request, view):
        return self.get_ident(request)  # 求当前访问的IP
