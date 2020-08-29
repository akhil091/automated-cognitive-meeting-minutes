

import IdentificationServiceHttpClientHelper
import GetSubscriptionKey
import sys


def get_profile(subscription_key, profile_id):
    
    helper = IdentificationServiceHttpClientHelper.IdentificationServiceHttpClientHelper(
        subscription_key)

    profile = helper.get_profile(profile_id)

    print('Profile ID = {0}\nLocale = {1}\nEnrollments Speech Time = {2}\nRemaining Enrollment Time = {3}\nCreated = {4}\nLast Action = {5}\nEnrollment Status = {6}\n'.format(
        profile._profile_id,
        profile._locale,
        profile._enrollment_speech_time,
        profile._remaining_enrollment_time,
        profile._created_date_time,
        profile._last_action_date_time,
        profile._enrollment_status))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python DeleteProfile.py <profile_id> ')
        print('\t<profile_id> the ID for a profile to delete from the sevice')
        sys.exit('Error: Incorrect usage.')

    subscription_key = GetSubscriptionKey.get_subscription_key()

    get_profile(subscription_key, sys.argv[1])

