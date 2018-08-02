from app01 import models
from rest_framework import serializers
from rest_framework.validators import ValidationError


# 序列化评论的类
class CommentSerializer(serializers.ModelSerializer):

    def validate_content(self, value):
        if "草" in value:
            raise ValidationError("不符合社会主义核心价值观")
        else:
            return value

    class Meta:
        model = models.Comment
        fields = "__all__"
        extra_kwargs = {
            "content": {
                "error_messages": {
                    "required": "内容不能为空"
                }
            },
            "article": {
                "error_messages": {
                    "required": "文章不能为空"
                }
            }
        }


# 序列化文章的类
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = "__all__"


# 文章的超链接序列化
class ArticleHyperLinkedSerializer(serializers.HyperlinkedModelSerializer):
    school = serializers.HyperlinkedIdentityField(view_name="school_detail", lookup_url_kwarg="pk")

    class Meta:
        model = models.Article
        fields = ["id", "title", "type", "school"]


# 学校的序列化
class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.School
        fields = "__all__"





















