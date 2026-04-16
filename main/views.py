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

    def retrieve(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        try:
            profile = Profile.objects.get(id=pk)
            return Response({
                    "status":"success",
                    "data": {
                        "id":profile.id,
                        "name":profile.name,
                        "gender":profile.gender,
                        "gender_probability":profile.gender_probability,
                        "sample_size":profile.sample_size,
                        "age":profile.age,
                        "age_group":profile.age_group,
                        "country_id":profile.country_id,
                        "country_probability":profile.country_probability,
                        "created_at":profile.created_at
                    }}, status=status.HTTP_200_OK)
        except Profile.DoesNotExist as err:
            return Response({
                "status":"error",
                "message":"Profile not found"
                }, status=status.HTTP_404_NOT_FOUND)


    def list(self,request,*args,**kwargs):
        q_gender = request.query_params.get("gender")
        q_country_id = request.query_params.get("country_id")
        q_age_group = request.query_params.get("age_group")
        query = {}
        if q_gender:
            query["gender__iexact"] = q_gender
        if q_country_id:
            query["country_id__iexact"] = q_country_id
        if q_age_group:
            query["age_group__iexact"] = q_age_group

        queryset = Profile.objects.only("id","name","gender","age","age_group","country_id").filter(**query)
        data = [{
            "id": item.id,
            "name": item.name,
            "gender": item.gender,
            "age": item.age,
            "age_group": item.age_group,
            "country_id": item.country_id
            } for item in queryset]

        return Response({
            "status": "success",
            "count": len(data),
            "data": data
            }, status=status.HTTP_200_OK)


    def create(self,request):
        name = request.data.get('name') or ''
        valid, response = validate_name(name)
        
        if valid == False:
            return response
        else:
            profile,is_new,error_message, is_error = get_or_create_profile(name)
            if is_error:
                return Response(error_message,status=status.HTTP_502_BAD_GATEWAY)
            elif is_new:
                 return Response({
                    "status":"success",
                    "data": {
                        "id":profile.id,
                        "name":profile.name,
                        "gender":profile.gender,
                        "gender_probability":profile.gender_probability,
                        "sample_size":profile.sample_size,
                        "age":profile.age,
                        "age_group":profile.age_group,
                        "country_id":profile.country_id,
                        "country_probability":profile.country_probability,
                        "created_at":profile.created_at
                    }}, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "status":"success",
                    "message":"Profile already exists",
                    "data": {
                        "id":profile.id,
                        "name":profile.name,
                        "gender":profile.gender,
                        "gender_probability":profile.gender_probability,
                        "sample_size":profile.sample_size,
                        "age":profile.age,
                        "age_group":profile.age_group,
                        "country_id":profile.country_id,
                        "country_probability":profile.country_probability,
                        "created_at":profile.created_at
                    }}, status=status.HTTP_200_OK)



    def destroy(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        
        if Profile.objects.filter(id=pk).exists():
            Profile.objects.get(id=pk).delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({
                "status": "error",
                "message": "Profile not found",
                }, status=status.HTTP_404_NOT_FOUND)
