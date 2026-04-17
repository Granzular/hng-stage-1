from django.urls import path
from main import views
from rest_framework.routers import DefaultRouter

app_name = 'main'

router = DefaultRouter(trailing_slash=False)
router.register(r'profiles',views.ProfileViewSet,basename='create-list-profile')
router.register(r'profiles/<pk>',views.ProfileViewSet,basename='detail-delete-profile')
urlpatterns = router.urls
