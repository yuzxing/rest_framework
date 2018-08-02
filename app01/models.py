from django.db import models


# 文章表
class Article(models.Model):
    title = models.CharField(max_length=32, unique=True, error_messages={"unique": "文章标题不能重复"})
    # 文章发布时间
    # auto_now每次更新的时候会把当前时间保存
    create_time = models.DateField(auto_now_add=True)
    # auto_now_add 第一次创建的时候把当前时间保存
    update_time = models.DateField(auto_now=True)
    # 文章的类型
    type = models.SmallIntegerField(
        choices=((1, "原创"), (2, "转载")),
        default=1
    )
    # 来源
    school = models.ForeignKey(to='School', on_delete=models.CASCADE)
    # 标签
    tag = models.ManyToManyField(to='Tag')


# 文章来源表
class School(models.Model):
    name = models.CharField(max_length=16)


# 文章标签表
class Tag(models.Model):
    name = models.CharField(max_length=16)


# 评论表
class Comment(models.Model):
    content = models.CharField(max_length=128)
    article = models.ForeignKey(to='Article', on_delete=models.CASCADE)

