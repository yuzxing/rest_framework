import os

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "study_drf.settings")
    import django
    django.setup()

    from app01 import models
    import datetime

    article_list = models.Article.objects.all()
    for i in article_list:
        i.create_time = datetime.datetime.now()
        i.save()
    # query_set = models.Article.objects.all().values("id", "title", "create_time", "type", "school__name")
    # print(query_set)
    # obj = models.Article.objects.first()
    # ret = obj.type
    # print(ret)
    # ret = obj.get_type_display()
    # print(ret)

