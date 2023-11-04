from django.urls import path, include
from apps.users.api.views import LoginView, LogoutView, VerifyTokenView
from apps.users.api.router import router

app_name = 'users_app'

urlpatterns = [
    # path('',include(router.urls)),
    path('user/login',LoginView.as_view(),name='token_obtain_pair'),
    path('user/logout',LogoutView.as_view(),name='logout'),
    path('user/verify-token', VerifyTokenView.as_view(), name='verify-token'),

]