from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from main.serializers import ProfileSerializer
from main.models import Profile
from main.utils import fetch_external_apis_response, validate_name, get_or_create_profile


class ProfileViewSet(ModelViewSet):

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    http_method_names = ['head','get','post','delete']

    def create(self,request):
        name = request.data.get('name') or ''
        valid, response = validate_name(name)
        
        if valid == False:
            return response
        else:
            profile,is_new,error_message, is_error = get_or_create_profile(name)
            if is_error:
                return Response(error_message,status=status.HTTP_502_BAD_GATEWAY)
