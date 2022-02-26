import logging

import git
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template.defaultfilters import register
from django.urls import path, include, re_path
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import RedirectView
from django.views.static import serve
from rest_framework.routers import DefaultRouter

from inma.apps.users.views import UserViewset

logger = logging.getLogger(__name__)


@register.filter(name='dict_key')
def dict_key(d, k):
    return d[k]


@register.filter(name='div')
def div(a, b):
    return a / b


@register.filter(name='mul')
def mul(a, b):
    return a * b


@csrf_exempt
def get_page(page, request, context=None):
    if not context:
        context = {}
    context['menu_title'] = ['동문회 소개', '동문회비', '동문회 소식', '커뮤니티'][context.get('menu_index', 0)]
    context['page'] = page
    context['version'] = git.Repo(search_parent_directories=True).head.object.hexsha
    context['static_url'] = '/static/'

    if 'mypage' not in request.path and request.user.is_authenticated and (
            not request.user.profile or not request.user.profile.grade):
        return redirect('/mypage?is_first')
    return render(request, f'page/{page}.html', context)


router = DefaultRouter()
router.register(r'users', UserViewset)

#####################
#######  NEW UI
#####################

menu1 = [
    ('intro', '소개'),
    ('org', '조직도'),
    ('rules', '회칙'),
    ('school-intro', '모교소개'),
]
menu2 = [
    ('pricing', '회비 안내'),
    # ('payment', '후원금 납부'),
]
menu3 = [
    ('notice', '공지사항'),
    ('bulletin', '회보'),
    ('news', '교우 소식'),
]
menu4 = [
    # ('inc-info', '기업정보 공유'),
    # ('job-info', '채용정보 공유'),
    # ('grade', '기수별 모임'),
    # ('small', '소모임'),
    ('free-board', '자유게시판'),
    ('executive-board', '임원게시판'),
]
menus = [menu1, menu2, menu3, menu4]


def main_page(request):
    context = {'hide_aside': True, 'menus': menus}
    return get_page('main', request, context)


def intro_page(request):
    context = {'menus': menus, 'aside': menu1, 'menu_index': 0}
    return get_page('intro', request, context)


def org_page(request):
    context = {'menus': menus, 'aside': menu1, 'menu_index': 0}
    return get_page('org', request, context)


def rules_page(request):
    context = {'menus': menus, 'aside': menu1, 'menu_index': 0}
    return get_page('rules', request, context)


def school_intro_page(request):
    context = {'menus': menus, 'aside': menu1, 'menu_index': 0}
    return get_page('school-intro', request, context)


def pricing_page(request):
    context = {'menus': menus, 'aside': menu2, 'menu_index': 1}
    return get_page('pricing', request, context)


def notice_page(request):
    context = {'menus': menus, 'aside': menu3, 'menu_index': 2}
    return get_page('notice', request, context)


def post_page(request):
    context = {'menus': menus, 'aside': menu3, 'menu_index': 2}
    return get_page('post', request, context)


def bulletin_page(request):
    context = {'menus': menus, 'aside': menu3, 'menu_index': 2}
    return get_page('bulletin', request, context)


def news_page(request):
    context = {'menus': menus, 'aside': menu3, 'menu_index': 2}
    return get_page('news', request, context)


@login_required
def free_board_page(request):
    context = {'menus': menus, 'aside': menu4, 'menu_index': 3}
    return get_page('free-board', request, context)


@login_required
def executive_board_page(request):
    context = {'menus': menus, 'aside': menu4, 'menu_index': 3}
    return get_page('executive-board', request, context)


def sign_in_page(request):
    from django.contrib import auth
    auth.logout(request)
    return get_page('sign-in', request)


def sign_up_page(request):
    return get_page('sign-up', request)


def mypage(request):
    context = {'menus': menus, 'is_first': 'is_first' in request.GET}
    return get_page('mypage', request, context)


def logout_page(request):
    from django.contrib import auth
    auth.logout(request)
    return main_page(request)


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
    re_path('^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path('^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

    path('api/', include(router.urls)),

    # new
    path('', include('social_django.urls', namespace='social')),
    path('logout/', logout_page, name='logout'),

    path('', main_page, name="main"),
    path('intro', intro_page, name="intro"),
    path('org', org_page, name="org"),
    path('rules', rules_page, name="rules"),
    path('school-intro', school_intro_page, name="school-intro"),
    path('pricing', pricing_page, name="pricing"),

    path('post', post_page, name="post"),

    path('notice', notice_page, name="notice"),
    path('bulletin', bulletin_page, name="bulletin"),
    path('news', news_page, name="news"),
    path('free-board', free_board_page, name="free-board"),
    path('executive-board', executive_board_page, name="executive-board"),

    path('sign-in', sign_in_page, name="sign-in"),
    path('sign-up', sign_up_page, name="sign-up"),
    path('mypage', mypage, name="mypage"),

    path('ckeditor/', include('ckeditor_uploader.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "인마고 동창회 관리자 페이지"
admin.site.site_title = "인마고 동창회 관리자 페이지"
admin.site.index_title = "인마고 동창회 관리자 페이지입니다"
