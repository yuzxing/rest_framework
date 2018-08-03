from django.shortcuts import render, HttpResponse
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.views import APIView
from app01 import models
from app01 import serializers as app01_serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
import logging
# 生成一个以当前文件名为名字的 logger实例
logger = logging.getLogger(__name__)
# 生成一个名字为collect的日志实例
collect_logger = logging.getLogger('collect')


# 创建Article的CBV 继承APIView
# class Article(APIView):
#
#     def get(self, request):
#         res = {"code": 0}
#         all_article = models.Article.objects.all()
#         ser_obj = app01_serializers.ArticleHyperLinkedSerializer(all_article, many=True, context={"request": request})
#         res["data"] = ser_obj.data
#         return Response(res)
#
#     def post(self, request):
#         res = {"code": 0}
#         ser_obj = app01_serializers.ArticleSerializer(data=self.request.data)
#         if ser_obj.is_valid():
#             ser_obj.save()
#         else:
#             res["code"] = 1
#             res["error"] = ser_obj.errors
#         return Response(res)


# 创建Article_detail的CBV 继承APIView
# class ArticleDetail(APIView):
#     def get(self, request):
#         pass
#
#
# # 创建评论类的原始方式
# class Comment(APIView):
#
#     def get(self, request):
#         res = {"code": 0}
#         query_set = models.Comment.objects.all()
#         ser_obj = app01_serializers.CommentSerializer(query_set, many=True)
#         res["data"] = ser_obj.data
#         return Response(res)


# 第二种继承方式
# class CommentView(GenericAPIView, ListModelMixin, CreateModelMixin):
#     queryset = models.Comment.objects.all()
#     serializer_class = app01_serializers.CommentSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, args, kwargs)
#
#     def post(self, request, *args, **kwargs):
#         print("你要添加评论....")
#         return self.create(request, *args, **kwargs)
#

# 评论详情页
# class CommentDetailView(GenericAPIView, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin):
#     queryset = models.Comment.objects.all()
#     serializer_class = app01_serializers.CommentSerializer
#
#     def get(self, request, pk):
#         return self.retrieve(request, pk)
#
#     def delete(self, request, pk):
#         return self.destroy(request, pk)
#
#     def perform_destroy(self, instance):
#         print("你要删除了....")
#         instance.delete()
#
#     def put(self, request, pk):
#         return self.update(request, pk)


# 继承 RetrieveUpdateDestroyAPIView 组合类

# class CommentDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = models.Comment.objects.all()
#     serializer_class = app01_serializers.CommentSerializer
#
#
# # 继承 ListCreateAPIView 组合类
# class Comment(ListCreateAPIView):
#     queryset = models.Comment.objects.all()
#     serializer_class = app01_serializers.CommentSerializer


# 终极继承
# class CommentViewSet(ModelViewSet):
#     queryset = models.Comment.objects.all()
#     serializer_class = app01_serializers.CommentSerializer


# class SchoolDetailView(APIView):
#
#     def get(self, request, name):
#         res = {"code": 0}
#         school_obj = models.School.objects.filter(name=name).first()
#         if not school_obj:
#             logger.warning('找不到学校信息...')
#             collect_logger.info(name)
#
#         logger.debug('我来获取名字为{}学校详情'.format(name))
#         logger.info('我来获取名字为{}学校详情'.format(name))
#         ser_obj = app01_serializers.SchoolSerializer(school_obj, context={"request": request})
#         res["data"] = ser_obj.data
#         return Response(res)


class SchoolViewSet(ModelViewSet):
    queryset = models.School.objects.all()
    serializer_class = app01_serializers.SchoolSerializer


class ArticleViewSet(ModelViewSet):
    queryset = models.Article.objects.all()
    serializer_class = app01_serializers.ArticleSerializer


# 自定义测试
class At(APIView):

    def get(self, request):
        print(request.query_params)
        print(request.query_params.get("name"))
        return HttpResponse("GET")

    def post(self, request):
        print(request.data)
        return HttpResponse("POST")

    def put(self, request):
        print(request.data)
        return HttpResponse("put")


# 生成 Token的函数
def get_token_code(username):
    """
    根据用户名和时间戳生成用户登录成功的随机字符串
    :param username: 字符串格式的用户名
    :return: 字符串格式的Token
    """
    import time
    import hashlib
    timestamp = str(time.time())
    m = hashlib.md5(bytes(username, encoding="utf8"))
    m.update(bytes(timestamp, encoding="utf8"))
    return m.hexdigest()


# login函数
class LoginView(APIView):
    """
    登录测试函数
    1，接受用户发过来的(post)的用户名和密码数据
    2，检验用户名和密码是否正确
        --成功返回登录成功(发Token)
        --失败就返回错误信息提示
    """
    def post(self, request):
        res = {"code": 0}
        # 从post里面取数据
        logger.debug(request.data)
        username = request.data.get("username")  # 从data里取数据
        password = request.data.get("password")
        # 去数据库查询
        user_obj = models.UserInfo.objects.filter(
            username=username,
            password=password,
        ).first()
        if user_obj:
            # 登录成功
            # 生成 Token
            token = get_token_code(username)
            # 将token保存
            # 用 user=user_obj这个条件去Token表里查询
            # 如果有记录就更新defaults里面传的参数，没有记录就用defaults里传的参数创建一条数据
            models.Token.objects.update_or_create(defaults={"token": token}, user=user_obj)
            # 将Token返回给用户
            res["token"] = token
        else:
            # 登录失败
            res["code"] = 1
            res["error"] = "用户名或密码错误"
        return Response(res)


from app01.utils.auth import MyAuth
from app01.utils.permission import MyPermission
from app01.utils.throttle import MyThrottle, VisitThrottle


class CommentViewSet(ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = app01_serializers.CommentSerializer
    authentication_classes = [MyAuth, ]
    throttle_classes = [VisitThrottle, ]


































