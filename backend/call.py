import os
from twilio.rest import Client

# Function to make a call
def make_call(to_number):
    account_sid = " "#enter your credentials
    auth_token =" "#enter your credentials
    client = Client(account_sid, auth_token)

    try:
        call = client.calls.create(
            from_="+14692146692",  # Your Twilio number
            to=to_number,  # User-provided number
            url="http://demo.twilio.com/docs/voice.xml",
        )
        print(f"Call initiated with SID: {call.sid}")
    except Exception as e:
        print(f"Failed to make call: {e}")

if __name__ == "__main__":
    # Example usage (replace this with user input in your application)
    user_number = input("Enter the phone number you want to call (in format +<country_code><number>): ")
    make_call(user_number)
