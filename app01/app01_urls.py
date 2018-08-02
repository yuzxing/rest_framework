from rest_framework.routers import DefaultRouter
from django.conf.urls import url
from app01 import views

urlpatterns = [
    # url(r'^article/', views.Article.as_view()),
    # url(r'^article/(?P<pk>\d+)', views.ArticleDetail.as_view(), name="article_detail"),
    # url(r'^school/(?P<name>\d+)', views.SchoolDetailView.as_view(), name="school_detail"),
    # url(r'comment/$', views.CommentView.as_view()),
    # url(r'^comment/(?P<pk>\d+)/$', views.CommentDetailView.as_view()),
    # url(r'comment/$', views.CommentViewSet.as_view({
    #     "get": "list",
    #     "post": "create"
    # })),
    # url(r'^comment/(?P<pk>\d+)/$', views.CommentViewSet.as_view({
    #     "get": "retrieve",
    #     "put": "update",
    #     "delete": "destroy"
    # })),

]
router = DefaultRouter()
router.register(r"comment", views.CommentViewSet)
router.register(r"school", views.SchoolViewSet)
router.register(r"article", views.ArticleViewSet)
urlpatterns += router.urls
