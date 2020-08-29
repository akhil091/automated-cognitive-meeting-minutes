
import IdentificationServiceHttpClientHelper
import GetSubscriptionKey
import sys

def print_all_profiles(subscription_key):
    
    helper = IdentificationServiceHttpClientHelper.IdentificationServiceHttpClientHelper(
        subscription_key)

    profiles = helper.get_all_profiles()

    print('Profile ID, Locale, Enrollment Speech Time, Remaining Enrollment Speech Time,'
          ' Created Date Time, Last Action Date Time, Enrollment Status')
    for profile in profiles:
        print('{0}, {1}, {2}, {3}, {4}, {5}, {6}'.format(
            profile.get_profile_id(),
            profile.get_locale(),
            profile.get_enrollment_speech_time(),
            profile.get_remaining_enrollment_time(),
            profile.get_created_date_time(),
            profile.get_last_action_date_time(),
            profile.get_enrollment_status()))

if __name__ == "__main__":
    subscription_key = GetSubscriptionKey.get_subscription_key()

    print_all_profiles(subscription_key)
