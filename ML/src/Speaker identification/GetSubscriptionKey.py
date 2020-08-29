
import os, sys

def get_subscription_key():
    subscription_key = os.environ.get("WHO_SAID_WHAT_KEY")

    if subscription_key is None:
        print("Cannot find Subscription Key")
        sys.exit()

    return subscription_key