AUTHENTICATION_BACKENDS = {
    'social_core.backends.naver.NaverOAuth2',
    'social_core.backends.kakao.KakaoOAuth2',
    'django.contrib.auth.backends.ModelBackend'
}

SOCIAL_AUTH_KAKAO_KEY = '6839bd1616511a0069058429cc2045e9'
SOCIAL_AUTH_KAKAO_SECRET = '6839bd1616511a0069058429cc2045e9'

SOCIAL_AUTH_NAVER_KEY = 'VCH1Wv9IOMl9Us9x8KH2'
SOCIAL_AUTH_NAVER_SECRET = 'B5fs3iiIXU'

SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'inma.apps.users.views.social_user',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'inma.apps.users.views.update_user_social_data'
)

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
