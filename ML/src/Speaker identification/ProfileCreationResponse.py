

class ProfileCreationResponse:
    
    _PROFILE_ID = 'identificationProfileId'

    def __init__(self, response):
       
        self._profile_id = response.get(self._PROFILE_ID, None)

    def get_profile_id(self):
        
        return self._profile_id
