

class EnrollmentResponse:
    

    _TOTAL_SPEECH_TIME = 'enrollmentSpeechTime'
    _REMAINING_SPEECH_TIME = 'remainingEnrollmentSpeechTime'
    _SPEECH_TIME = 'speechTime'
    _ENROLLMENT_STATUS = 'enrollmentStatus'

    def __init__(self, response):
       
        self._total_speech_time = response.get(self._TOTAL_SPEECH_TIME, None)
        self._remaining_speech_time = response.get(self._REMAINING_SPEECH_TIME, None)
        self._speech_time = response.get(self._SPEECH_TIME, None)
        self._enrollment_status = response.get(self._ENROLLMENT_STATUS, None)

    def get_total_speech_time(self):
        
        return self._total_speech_time

    def get_remaining_speech_time(self):
        
        return self._remaining_speech_time

    def get_speech_time(self):
        
        return self._speech_time

    def get_enrollment_status(self):
        
        return self._enrollment_status
