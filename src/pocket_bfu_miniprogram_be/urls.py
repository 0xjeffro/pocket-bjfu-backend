"""pocket_bfu_miniprogram_be URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import refresh_jwt_token

from apps.users.views import WxLogin, JwLogin, GetAccessToken, UserInfo, ZsbLogin
from apps.changyonglianjie.views import ChangYongLianJieAddPriority

from apps.xiaoli.views import XiaoLiViewSet
from apps.changyonglianjie.views import ChangYongLianJieViewSet
from apps.jiaowuchu.views import JiaoWuChuNewsViewSet
from apps.content.views import ContentViewSet, MyContentViewSet
from apps.comment.views import CommentViewSet
from apps.operate.views import LikeToContentViewSet, FavToContentViewSet, LikeToCommentViewSet, MyFavViewSet, \
    ReportToContentViewSet
from apps.behaviortracking.views import CaptureScreenTrackingViewSet

from apps.sunnyrun.views import SunnyRun
from apps.chengji.views import ChengJi, PaiMing
from apps.qiniuyun.views import QiNiuView

from apps.ad.views import GetAd
from apps.notice.views import GetNotice
from apps.globalvar.views import GlobalVarViewSet

from apps.kechengbiao.views import KeChengBiao
from apps.kongjiaoshi.views import KongJiaoShi
from django.conf import settings

from django.views.static import serve
from .settings import STATIC_ROOT
from django.views.generic.base import RedirectView


router = DefaultRouter()
router.register(r'xiaoLi', XiaoLiViewSet, basename='xiaoLi')
router.register(r'changYongLianJie', ChangYongLianJieViewSet, basename='changYongLianJie')
router.register(r'jiaoWuChuNews', JiaoWuChuNewsViewSet, basename='jiaoWuChuNews')
router.register(r'content', ContentViewSet, basename='content')
router.register(r'myContent', MyContentViewSet, basename='myContent')
router.register(r'comment', CommentViewSet, basename='comment')
router.register(r'likeToContent', LikeToContentViewSet, basename='likeToContent')
router.register(r'likeToComment', LikeToCommentViewSet, basename='likeToComment')
router.register(r'reportToContent', ReportToContentViewSet, basename='reportToContent')
router.register(r'favToContent', FavToContentViewSet, basename='favToContent')
router.register(r'myFav', MyFavViewSet, basename='myFav')
router.register(r'captureScreen', CaptureScreenTrackingViewSet, basename='captureScreen')
router.register(r'globalVar', GlobalVarViewSet, basename='globalVar')

urlpatterns = [
    path('bfu_admin/', admin.site.urls),
    # url(r'^api-auth/', include('rest_framework.urls')),
    # url(r'^docs/', include_docs_urls(title='口袋北林')),
    url(r'^', include(router.urls)),
    url(r'^getAccessToken', GetAccessToken.as_view(), name='getAccessToken'),
    url(r'^wxLogin', WxLogin.as_view(), name='wxLogin'),
    url(r'^jwLogin', JwLogin.as_view(), name='jxLogin'),
    url(r'^zsbLogin', ZsbLogin.as_view(), name='zsbLogin'),
    url(r'^changYongLianJieAddPriority', ChangYongLianJieAddPriority.as_view(), name='changYongLianJieAddPriority'),
    url(r'^sunnyRun', SunnyRun.as_view(), name='sunnyRun'),
    url(r'^chengJi', ChengJi.as_view(), name='chengJi'),
    url(r'^paiMing', PaiMing.as_view(), name='paiMing'),
    url(r'^keChengBiao', KeChengBiao.as_view(), name='keChengBiao'),
    url(r'^kongJiaoShi', KongJiaoShi.as_view(), name='kongJiaoShi'),
    url(r'^getUserInfo', UserInfo.as_view(), name='getUserInfo'),
    url(r'^uploadToken', QiNiuView.as_view(), name='uploadToken'),
    url(r'^ad', GetAd.as_view(), name='getAd'),
    url(r'^notice', GetNotice.as_view(), name='getNotice'),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    #re_path(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
    path('favicon.ico', RedirectView.as_view(url='/static/admin/simplepro/images/favicon.ico')),
]

if settings.DEBUG:
    urlpatterns.append(url(r'^api-auth/', include('rest_framework.urls')))
    urlpatterns.append(url(r'^docs/', include_docs_urls(title='口袋北林')))
    urlpatterns.append(url(r'^', include(router.urls)))
