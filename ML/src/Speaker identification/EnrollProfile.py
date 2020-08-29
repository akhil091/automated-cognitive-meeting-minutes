

import IdentificationServiceHttpClientHelper
import GetSubscriptionKey
import sys
import json

def enroll_profile(subscription_key, profile_id, file_path, force_short_audio, name):
    _short_audio -- waive the recommended minimum audio limit needed for enrollment
    