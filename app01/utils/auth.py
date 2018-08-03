"""
自定义的认证类都放在这里
"""
from rest_framework.authentication import BaseAuthentication
from app01 import models
from rest_framework.exceptions import AuthenticationFailed
import logging
logger = logging.getLogger(__name__)


class MyAuth(BaseAuthentication):

    def authenticate(self, request):
        logger.debug(request.method)
        if request.method in ["POST", "PUT", "DELETE"]:
            token = request.data.get("token")
            # 取数据库中查询有没有这个token
            token_obj = models.Token.objects.filter(token=token).first()
            if token_obj:
                return token_obj.user, token
            else:
                raise AuthenticationFailed("无效的token")
        else:
            return None, None
