from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.api.User.views_user import UserViewSet, Login, Logout
from core.api.Client.views_client import ClientViewSet
from core.api.Company.views_company import *
from core.api.Games.views_games import *
router = DefaultRouter()

router.register(r'UsersApi', UserViewSet, basename='UsersApi')
router.register(r'Client', ClientViewSet, basename='Client')
router.register(r'Company', CompanyViewSet, basename='Company')
router.register(r'Games', GameViewSet, basename='games')

urlpatterns = [
    path('', include(router.urls), name="ViewApi"),
    path('Login/', Login.as_view(), name="Login"),
    path('Logout/', Logout.as_view(), name="Logout"),
]