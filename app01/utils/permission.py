"""
自定义的权限类
"""
from rest_framework.permissions import BasePermission


class MyPermission(BasePermission):
    message = "没有权限,请注册"

    def has_permission(self, request, view):
        """
        判断该用户有没有权限
        判断是不是VIP用户
        如果是VIP用户就返回True
        如果是普通用户就返回False
        """
        print("我要进行自定义的权限判断....")
        return True

    def has_object_permission(self, request, view, obj):
        """
        判断当前评论用户的作者是不是你当前的用户
        只有评论的作者才能删除自己的评论
        """
        print("这是在自定义权限类中has_object_permission")
        print(obj.id)
        if request.method in ["PUT", "DELETE"]:
            if obj.user == request.user:
                # 当前要删除的评论的作者就是当前登录的用户
                return True
            else:
                return False
        else:
            return True
