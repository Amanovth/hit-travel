from django.urls import path, include

from .views import *

urlpatterns = [
    path('auth/register', RegisterAPIView.as_view(), name='register'),
    path('auth/verify-email', VerifyEmailAPIView.as_view(), name='verify-email'),
    path('auth/re-send', SendAgainCodeAPIView.as_view(), name='send-code-again'),
    path('auth/login', LoginAPIView.as_view(), name='login'),
    path('auth/logout', LogoutAPIView.as_view(), name='logout'),
    path('auth/password-reset/request', PasswordResetRequestAPIView.as_view(), name='password-reset-request'),
    path('auth/password-reset/<str:token>', PasswordResetUpdateAPIView.as_view(), name='password-reset-update'),
    path('auth/new-password', SetNewPasswordAPIView.as_view(), name='set-new-password'),
    path('profile/update-photo', UpdateProfilePhotoAPIView.as_view(), name='Update profile photo'),
    path('profile/remove-photo', RemoveProfilePhotoAPIView.as_view(), name='Remove profile photo'),
    path('favorite/<int:tour_id>', AddRemoveFavoriteView.as_view(), name='add-remove-favorite'),
    path('profile/personal', ProfileInfoAPIView.as_view(), name='Profile information'),
    path('profile/favorites', FavoriteToursAPIView.as_view(), name='Favorite Tours')
]