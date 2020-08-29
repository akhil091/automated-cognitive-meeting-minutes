
import IdentificationServiceHttpClientHelper
import GetSubscriptionKey
import sys
import json

def identify_file(subscription_key, map_file, file_path, force_short_audio, profile_ids):
    
    helper = IdentificationServiceHttpClientHelper.IdentificationServiceHttpClientHelper(
        subscription_key)

    identification_response = helper.identify_file(
        file_path, profile_ids,
        force_short_audio.lower() == "true")

    print('Identified Speaker = {0}'.format(map_file.get(identification_response.get_identified_profile_id(),"Unknown")))
    print('Confidence = {0}'.format(identification_response.get_confidence()))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Usage: python IdentifyFile.py <identification_file_path>'
              ' <profile_ids>...')
        print('\t<identification_file_path> is the audio file path for identification')
        print('\t<force_short_audio> True/False waives the recommended minimum audio limit needed '
              'for enrollment')
        
        sys.exit('Error: Incorrect Usage.')

    subscription_key = GetSubscriptionKey.get_subscription_key()

    with open('./Identification/mapping.json') as f:
        data = json.load(f)

        group_ids = list(data.keys())

    identify_file(subscription_key, data, sys.argv[1], sys.argv[2], group_ids)
