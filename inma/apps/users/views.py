import json
import logging

from django.contrib import auth
from django.contrib.auth import logout
from django.http import JsonResponse
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action

from .models import Profile, User
from .serializers import UserSerializer

logger = logging.getLogger(__name__)


def social_user(backend, uid, user=None, *args, **kwargs):
    provider = backend.name
    social = backend.strategy.storage.user.get_social_auth(provider, uid)
    if social:
        logout(backend.strategy.request)
    return {'social': social,
            'user': user,
            'is_new': user is None,
            'new_association': False}


kakao = {
    'access_token': 'E6GplCyEzAdukgRvHUbVBnzQbqlaKftbWE2v8Ao9dVsAAAF_NMcGcQ', 'token_type': 'bearer',
    'refresh_token': 'WrpvbaMhxCUjdZTbgJ_hLfhNw--iHzGdmeL4kgo9dVsAAAF_NMcGbw', 'expires_in': 21599,
    'scope': 'age_range birthday profile_image profile_nickname', 'refresh_token_expires_in': 5183999,
    'id': 2066317606,
    'connected_at': '2022-01-05T12:39:14Z', 'properties': {'nickname': '원재',
                                                           'profile_image': 'http://k.kakaocdn.net/dn/hnOLs/btrmXFarEGQ/1K2VAjdxntOrHmWaJAii6k/img_640x640.jpg',
                                                           'thumbnail_image': 'http://k.kakaocdn.net/dn/hnOLs/btrmXFarEGQ/1K2VAjdxntOrHmWaJAii6k/img_110x110.jpg'},
    'kakao_account': {'profile_nickname_needs_agreement': False, 'profile_image_needs_agreement': False,
                      'profile': {'nickname': '원재',
                                  'thumbnail_image_url': 'http://k.kakaocdn.net/dn/ploki/btrt0Nyl63n/KKvMcUtEddPkMFng36knek/img_110x110.jpg',
                                  'profile_image_url': 'http://k.kakaocdn.net/dn/ploki/btrt0Nyl63n/KKvMcUtEddPkMFng36knek/img_640x640.jpg',
                                  'is_default_image': False}, 'has_age_range': True,
                      'age_range_needs_agreement': False,
                      'age_range': '20~29', 'has_birthday': True, 'birthday_needs_agreement': False,
                      'birthday': '0926',
                      'birthday_type': 'SOLAR'}
}

naver = {
    'access_token': 'AAAAOqvV0uiJ7q1Wp0Nv2amPdU4YwrLFsaV5J3_YLpNT-7LfvjHAd1xuu8vgwQYnVrMfCh9Uc1gklw8Oqefh9CuwIGQ',
    'refresh_token': 'Wy0IGUqye9R4PtUmC6WlJipmiinkisTzlYrzVHiihodT7JzeG8RWpFhWhPYb8sgzrXwiiKAKRrrnOISyZK2fZ6Xii6yPrRvmk8aCLbyWvipMwtbbczzqkcfQ9jIzCXn2YqZ5NK3',
    'token_type': 'bearer', 'expires_in': '3600', 'id': 'WS7Gh9-kQgDrjzXichXeK6YPQ2v0yLaSmBdU4NUEpSM',
    'email': 'dnjswo0926@naver.com', 'username': '이원재', 'nickname': '', 'gender': 'M', 'age': '20-29',
    'birthday': '09-26', 'profile_image': 'https://ssl.pstatic.net/static/pwe/address/img_profile.png'
}


def update_user_social_data(strategy, *args, **kwargs):
    response = kwargs['response']
    backend = kwargs['backend']
    user = kwargs['user']

    profile = Profile.objects.filter(user=user).first()
    if not profile:
        profile = Profile(user=user)

    if backend.name == 'kakao':
        profile_image = response.get('properties', {}).get('thumbnail_image')
        name = response.get('properties', {}).get('nickname')
    if backend.name == 'naver':
        profile_image = response.get('profile_image')
        name = response.get('username')

    if not profile.profile:
        profile.profile = profile_image
    if not profile.name:
        profile.name = name
    profile.save()


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['patch'])
    def mypage(self, request, *ars, **kwargs):
        params = request.data

        name = params.get('name')
        profile_image = params.get('profile')
        phone = params.get('phone')
        grade = params.get('grade')
        department = params.get('department')
        marketing = params.get('marketing', True)

        def error_response(type, message):
            return JsonResponse({
                'type': type, 'message': message
            }, status=status.HTTP_400_BAD_REQUEST)

        if not name:
            return error_response('name', '이름을 입력해주세요.')
        if not phone:
            return error_response('phone', '전화번호 입력해주세요.')
        if not grade:
            return error_response('grade', '기수를 선택해주세요.')
        if not department:
            return error_response('department', '학과를 선택해주세요.')

        user = request.user
        profile = Profile.objects.filter(user=user).first()
        if not profile:
            profile = Profile(user=user)

        profile.name = name
        profile.profile = profile_image
        profile.phone = phone
        profile.grade = grade
        profile.department = department
        profile.save()

        return JsonResponse({'message': '저장되었습니다.'}, status=status.HTTP_200_OK)
