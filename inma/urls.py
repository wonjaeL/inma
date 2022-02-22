import logging

import git
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.template.defaultfilters import register
from django.urls import path, include, re_path
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import RedirectView
from django.views.static import serve
from rest_framework.routers import DefaultRouter

from inma.apps.courses.views import CourseViewset

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
    context['page'] = page
    context['version'] = git.Repo(search_parent_directories=True).head.object.hexsha
    context['static_url'] = '/static/'
    return render(request, f'page/{page}.html', context)


router = DefaultRouter()
router.register(r'courses', CourseViewset)

#####################
#######  NEW UI
#####################

menus = [
    ('intro', '소개'),
    ('org', '조직도'),
    ('rules', '회칙'),
    ('school-intro', '모교소개'),
]


def main_page(request):
    context = {'hide_aside': True, 'menus': menus}
    return get_page('main', request, context)


def list_page(request):
    context = {}
    return get_page('list', request, context)


def post_page(request):
    context = {}
    return get_page('post', request, context)


def intro_page(request):
    context = {'menus': menus}
    return get_page('intro', request, context)


def org_page(request):
    context = {'menus': menus}
    return get_page('org', request, context)


def rules_page(request):
    context = {'menus': menus}
    return get_page('rules', request, context)


def school_intro_page(request):
    context = {'menus': menus}
    return get_page('school-intro', request, context)


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
    re_path('^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path('^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

    path('v1/', include(router.urls)),

    # new
    path('', include('social_django.urls', namespace='social')),
    path('logout/', main_page, name='logout'),

    path('', main_page, name="main"),
    path('list', list_page, name="list"),
    path('post', post_page, name="post"),
    path('intro', intro_page, name="intro"),
    path('org', org_page, name="org"),
    path('rules', rules_page, name="rules"),
    path('school-intro', school_intro_page, name="school-intro"),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "인마고 동창회 관리자 페이지"
admin.site.site_title = "인마고 동창회 관리자 페이지"
admin.site.index_title = "인마고 동창회 관리자 페이지입니다"
