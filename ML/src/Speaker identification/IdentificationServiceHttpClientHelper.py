
import http.client
import urllib.parse
import json
import time
from contextlib import closing
import IdentificationProfile
import IdentificationResponse
import EnrollmentResponse
import ProfileCreationResponse
import logging

class IdentificationServiceHttpClientHelper:
   
    _STATUS_OK = 200
    _STATUS_ACCEPTED = 202
    _BASE_URI = 'westus.api.cognitive.microsoft.com'
    _IDENTIFICATION_PROFILES_URI = '/spid/v1.0/identificationProfiles'
    _IDENTIFICATION_URI = '/spid/v1.0/identify'
    _SUBSCRIPTION_KEY_HEADER = 'Ocp-Apim-Subscription-Key'
    _CONTENT_TYPE_HEADER = 'Content-Type'
    _JSON_CONTENT_HEADER_VALUE = 'application/json'
    _STREAM_CONTENT_HEADER_VALUE = 'application/octet-stream'
    _SHORT_AUDIO_PARAMETER_NAME = 'shortAudio'
    _OPERATION_LOCATION_HEADER = 'Operation-Location'
    _OPERATION_STATUS_FIELD_NAME = 'status'
    _OPERATION_PROC_RES_FIELD_NAME = 'processingResult'
    _OPERATION_MESSAGE_FIELD_NAME = 'message'
    _OPERATION_STATUS_SUCCEEDED = 'succeeded'
    _OPERATION_STATUS_FAILED = 'failed'
    _OPERATION_STATUS_UPDATE_DELAY = 5

    def __init__(self, subscription_key):
       
        self._subscription_key = subscription_key

    def get_all_profiles(self):
        
        try:
            # Send the request
            res, message = self._send_request(
                'GET',
                self._BASE_URI,
                self._IDENTIFICATION_PROFILES_URI,
                self._JSON_CONTENT_HEADER_VALUE)

            if res.status == self._STATUS_OK:
                # Parse the response body
                profiles_raw = json.loads(message)
                return [IdentificationProfile.IdentificationProfile(profiles_raw[i])
                        for i in range(0, len(profiles_raw))]
            else:
                reason = res.reason if not message else message
                raise Exception('Error getting all profiles: ' + reason)
        except:
            logging.error('Error getting all profiles.')
            raise

    def get_profile(self, profile_id):
       
        try:
            # Prepare the request
            request_url = '{0}/{1}'.format(
                self._IDENTIFICATION_PROFILES_URI,
                profile_id)

            # Send the request
            res, message = self._send_request(
                'GET',
                self._BASE_URI,
                request_url,
                self._JSON_CONTENT_HEADER_VALUE)

            if res.status == self._STATUS_OK:
                # Parse the response body
                profile_raw = json.loads(message)
                return IdentificationProfile.IdentificationProfile(profile_raw)
            else:
                reason = res.reason if not message else message
                raise Exception('Error getting profile: ' + reason)
        except:
            logging.error('Error getting profile.')
            raise

    def create_profile(self, locale):
       
        try:
           
            body = json.dumps({'locale': '{0}'.format(locale)})

            
            res, message = self._send_request(
                'POST',
                self._BASE_URI,
                self._IDENTIFICATION_PROFILES_URI,
                self._JSON_CONTENT_HEADER_VALUE,
                body)

            if res.status == self._STATUS_OK:
                
                return ProfileCreationResponse.ProfileCreationResponse(json.loads(message))
            else:
                reason = res.reason if not message else message
                raise Exception('Error creating profile: ' + reason)
        except:
            logging.error('Error creating profile.')
            raise

    def delete_profile(self, profile_id):
        """ Deletes a profile from the server

      
        """
        try:
           
            request_url = '{0}/{1}'.format(
                self._IDENTIFICATION_PROFILES_URI,
                profile_id)

            
            res, message = self._send_request(
                'DELETE',
                self._BASE_URI,
                request_url,
                self._JSON_CONTENT_HEADER_VALUE)

            if res.status != self._STATUS_OK:
                reason = res.reason if not message else message
                raise Exception('Error deleting profile: ' + reason)
        except:
            logging.error('Error deleting profile')
            raise

    def reset_enrollments(self, profile_id):
        
        try:
            
            request_url = '{0}/{1}/reset'.format(
                self._IDENTIFICATION_PROFILES_URI,
                profile_id)

            
            res, message = self._send_request(
                'POST',
                self._BASE_URI,
                request_url,
                self._JSON_CONTENT_HEADER_VALUE)

            if res.status != self._STATUS_OK:
                reason = res.reason if not message else message
                raise Exception('Error resetting profile: ' + reason)
        except:
            logging.error('Error resetting profile')
            raise

    def enroll_profile(self, profile_id, file_path, force_short_audio = False):
        
        try:
           
            request_url = '{0}/{1}/enroll?{2}={3}'.format(
                self._IDENTIFICATION_PROFILES_URI,
                urllib.parse.quote(profile_id),
                self._SHORT_AUDIO_PARAMETER_NAME,
                force_short_audio)

            
            with open(file_path, 'rb') as body:
               
                res, message = self._send_request(
                    'POST',
                    self._BASE_URI,
                    request_url,
                    self._STREAM_CONTENT_HEADER_VALUE,
                    body)

            if res.status == self._STATUS_OK:
                
                return EnrollmentResponse.EnrollmentResponse(json.loads(message))
            elif res.status == self._STATUS_ACCEPTED:
                operation_url = res.getheader(self._OPERATION_LOCATION_HEADER)

                return EnrollmentResponse.EnrollmentResponse(
                    self._poll_operation(operation_url))
            else:
                reason = res.reason if not message else message
                raise Exception('Error enrolling profile: ' + reason)
        except:
            logging.error('Error enrolling profile.')
            raise

    def identify_file(self, file_path, test_profile_ids, force_short_audio = False):
        
        try:
            
            if len(test_profile_ids) < 1:
                raise Exception('Error identifying file: no test profile IDs are provided.')
            test_profile_ids_str = ','.join(test_profile_ids)
            request_url = '{0}?identificationProfileIds={1}&{2}={3}'.format(
                self._IDENTIFICATION_URI,
                urllib.parse.quote(test_profile_ids_str),
                self._SHORT_AUDIO_PARAMETER_NAME,
                force_short_audio)

            
            with open(file_path, 'rb') as body:
               
                res, message = self._send_request(
                    'POST',
                    self._BASE_URI,
                    request_url,
                    self._STREAM_CONTENT_HEADER_VALUE,
                    body)

            if res.status == self._STATUS_OK:
                
                return IdentificationResponse.IdentificationResponse(json.loads(message))
            elif res.status == self._STATUS_ACCEPTED:
                operation_url = res.getheader(self._OPERATION_LOCATION_HEADER)

                return IdentificationResponse.IdentificationResponse(
                    self._poll_operation(operation_url))
            else:
                reason = res.reason if not message else message
                raise Exception('Error identifying file: ' + reason)
        except:
            logging.error('Error identifying file.')
            raise

    def _poll_operation(self, operation_url):
        
        try:
            
            parsed_url = urllib.parse.urlparse(operation_url)

            while True:
                
                res, message = self._send_request(
                    'GET',
                    parsed_url.netloc,
                    parsed_url.path,
                    self._JSON_CONTENT_HEADER_VALUE)

                if res.status != self._STATUS_OK:
                    reason = res.reason if not message else message
                    raise Exception('Operation Error: ' + reason)

                operation_response = json.loads(message)

                if operation_response[self._OPERATION_STATUS_FIELD_NAME] == \
                        self._OPERATION_STATUS_SUCCEEDED:
                    return operation_response[self._OPERATION_PROC_RES_FIELD_NAME]
                elif operation_response[self._OPERATION_STATUS_FIELD_NAME] == \
                        self._OPERATION_STATUS_FAILED:
                    raise Exception('Operation Error: ' +
                                    operation_response[self._OPERATION_MESSAGE_FIELD_NAME])
                else:
                    time.sleep(self._OPERATION_STATUS_UPDATE_DELAY)
        except:
            logging.error('Error polling the operation status.')
            raise

    def _send_request(self, method, base_url, request_url, content_type_value, body=None):
        
        try:
           
            headers = {self._CONTENT_TYPE_HEADER: content_type_value,
                       self._SUBSCRIPTION_KEY_HEADER: self._subscription_key}

            
            with closing(http.client.HTTPSConnection(base_url)) as conn:
                
                conn.request(method, request_url, body, headers)
                res = conn.getresponse()
                message = res.read().decode('utf-8')

                return res, message
        except:
            logging.error('Error sending the request.')
            raise
