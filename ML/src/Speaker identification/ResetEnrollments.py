

import IdentificationServiceHttpClientHelper
import GetSubscriptionKey
import sys

def reset_enrollments(subscription_key, profile_id):
   

    helper = IdentificationServiceHttpClientHelper.IdentificationServiceHttpClientHelper(
        subscription_key)

    helper.reset_enrollments(profile_id)

    print('Profile {0} has been successfully reset.'.format(profile_id))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python ResetEnrollments.py <subscription_key> <profile_id> ')
        print('\t<profile_id> the ID for a profile to reset its enrollments')
        sys.exit('Error: Incorrect usage.')

    subscription_key = GetSubscriptionKey.get_subscription_key()

    reset_enrollments(subscription_key, sys.argv[1])

