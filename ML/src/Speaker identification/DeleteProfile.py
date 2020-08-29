

import IdentificationServiceHttpClientHelper
import GetSubscriptionKey
import sys


def delete_profile(subscription_key, profile_id):
		
		helper = IdentificationServiceHttpClientHelper.IdentificationServiceHttpClientHelper(
        subscription_key)
		helper.delete_profile(profile_id)

		print('Profile {0} has been successfully deleted.'.format(profile_id))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python DeleteProfile.py <profile_id> ')
        print('\t<profile_id> the ID for a profile to delete from the sevice')
        sys.exit('Error: Incorrect usage.')

    subscription_key = GetSubscriptionKey.get_subscription_key()

    delete_profile(subscription_key, sys.argv[1])

