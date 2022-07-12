from django.urls import path
from auth.views import CreateTokenView, LogoutView, RegisterView, \
    UserProfileAPIView

urlpatterns = [
    path('token/', CreateTokenView.as_view(), name='token'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me', UserProfileAPIView.as_view(), name='me'),
]