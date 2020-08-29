

class IdentificationResponse:
   

    _IDENTIFIED_PROFILE_ID = 'identifiedProfileId'
    _CONFIDENCE = 'confidence'

    def __init__(self, response):
        
        self._identified_profile_id = response.get(self._IDENTIFIED_PROFILE_ID, None)
        self._confidence = response.get(self._CONFIDENCE, None)

    def get_identified_profile_id(self):
        
        return self._identified_profile_id

    def get_confidence(self):
        
        return self._confidence
