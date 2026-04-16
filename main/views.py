from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from main.models import Profile
from main.serializers import ProfileSerializer


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    http_method_names = ['get','POST','DELETE','HEAD','OPTIONS']

    def create(self,request):
        ...