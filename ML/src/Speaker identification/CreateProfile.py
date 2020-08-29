

import IdentificationServiceHttpClientHelper
import GetSubscriptionKey
import sys

def create_profile(subscription_key, locale):
    
    helper = IdentificationServiceHttpClientHelper.IdentificationServiceHttpClientHelper(
        subscription_key)

    creation_response = helper.create_profile(locale)

    print('{0}'.format(creation_response.get_profile_id()))

if __name__ == "__main__":

    subscription_key = GetSubscriptionKey.get_subscription_key()

    create_profile(subscription_key, 'en-us')
