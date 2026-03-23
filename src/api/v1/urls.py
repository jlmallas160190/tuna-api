from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .core.views import TranslationListView, UserMenuView
from .login.views import LoginView
from .medical_appointments.views import MedicalSpecialityViewSet
from .users.views import UserCreateView, UserDetailView, UserListView

router = DefaultRouter()
router.register(
    r"medical-specialities", MedicalSpecialityViewSet, basename="speciality"
)

urlpatterns = [
    path("", include(router.urls)),
    path("i18n/", include("django.conf.urls.i18n")),
    path("login/", LoginView.as_view(), name="auth"),
    path("api/token/", TokenObtainPairView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view()),
    path("register/", UserCreateView.as_view(), name="user-register"),
    path("menus/", UserMenuView.as_view(), name="user-menus"),
    path("users", UserListView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("translations/", TranslationListView.as_view(), name="translation-list"),
]
