import requests
from rest_framework import status
from rest_framework.response import Response
from main.models import Profile
import logging

logger = logging.getLogger(__name__)

GENDERIZE_API_URL = "https://api.genderize.io"
AGIFY_API_URL = "https://api.agify.io"
NATIONALIZE_API_URL = "https://api.nationalize.io"


def fetch_external_apis_response(name:str):
    # renamed from test_api
    params = {'name':name}
    genderize_res = requests.get(GENDERIZE_API_URL,params=params)
    agify_res = requests.get(AGIFY_API_URL,params=params)
    nationalize_res = requests.get(NATIONALIZE_API_URL,params=params)
    genderize_data = genderize_res.json()
    agify_data = agify_res.json()
    nationalize_data = nationalize_res.json()
    return [genderize_data,agify_data,nationalize_data]

def validate_name(name:str)->tuple:
    """
    This function returns a tuple of length 2.
    elements: 
    """
    if name.strip() == '':
        return False, Response({
            'status': 'error',
            'message': 'Missing or empty name'
            }, status=status.HTTP_400_BAD_REQUEST)
    if name.isalpha() == False:
        return False, Response({
            'status': 'error',
            'message': 'Invalid type'
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return True, None

def  get_or_create_profile(name:str)->tuple:
    '''
    This fuction returns a tuple with length 4. 
    (profile,is_new,error_message,is_error)
    if is_error is True, then profile would be None;
    else profile would contain data and error_message would be None.
    is_new is only True if a new profile was created.
    '''

    if Profile.objects.filter(name=name).exists():
        return Profile.objects.get(name=name),False,None,False
    else:
        profile, error_message, is_error = process_request(name)
        return  profile, True, error_message, is_error # This returns: profile,is_new, error_message, is_error

def process_request(name:str)->tuple:
    '''
    This fuction returns a tuple with length 3. 
    (profile,error_message,is_error)
    if is_error is True, then profile would be None;
    else profile would contain data and error_message would be None.
    '''
    try:
        data1,data2,data3 = fetch_external_apis_response(name)
        failed_apis = '' # a string of the external api names that returned an invalid response
        # genderize API
        gender = data1.get('gender')
        gender_probability = data1.get('probability')
        sample_size = data1.get('count')
        if gender == None or sample_size == 0:
            failed_api = 'Genderize'
            return None, {
                    'status': 'error',
                    'message': f'{failed_api} returned an invalid response'
                    }, True


        # agify API
        age = data2.get('age')
        if age == None:
            failed_api = 'Agify'
            return None, {
                    'status': 'error',
                    'message': f'{failed_api} returned an invalid response'
                    }, True

        else:
            age_group = 'child' if (age>=0 and age<=12) else 'teenager' if (age>=13 and age<=19) else 'adult' if (age>=20 and age<=59) else 'senior' if (age>=60) else 'merlin'
        # nationalize API
        if data3['country'] == []:
            failed_api = 'Nationalize'
            return None, {
                    'status': 'error',
                    'message': f'{failed_api} returned an invalid response'
                    }, True

        else:
            country = max(data3['country'],key=lambda x:x['probability'])
            country_id = country.get('country_id')
            country_probability = country.get('probability')

        profile = Profile.objects.create(
            name = name,
            gender = gender,
            gender_probability = gender_probability,
            sample_size = sample_size,
            age=age,
            age_group = age_group,
            country_id = country_id,
            country_probability=country_probability
        )

        return profile,None,False

        
    except Exception as err:
        logger.error(f"server failure: {err}")
        return None,{
            'status': 'error',
            'message': 'server failure'
        }, True
