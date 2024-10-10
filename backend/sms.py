from flask import Flask, request, jsonify
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from flask_cors import CORS




@app.route("/send_sms", methods=['POST'])
def send_sms():
    # Get the JSON data from the request
    data = request.json
    recipient_phone_number = data.get('recipient')
    message_body = data.get('message')

    # Validate the request data
    if not recipient_phone_number or not message_body:
        return jsonify({"status": "error", "message": "Recipient phone number and message body are required"}), 400

    # Initialize the Twilio client
    client = Client(account_sid, auth_token)

    try:
        # Send the SMS using Twilio's API
        message = client.messages.create(
            body=message_body,
            from_=twilio_phone_number,
            to=recipient_phone_number
        )

        # Check if the message was successfully sent
        if message.sid:
            return jsonify({"status": "success", "message": "SMS sent successfully"}), 200
        else:
            return jsonify({"status": "error", "message": "SMS not sent due to an unknown error"}), 500

    except TwilioRestException as e:
        # Handle specific Twilio API exceptions
        return jsonify({"status": "error", "message": f"Twilio error: {str(e)}"}), 500

    except Exception as e:
        # Handle any other exceptions
        return jsonify({"status": "error", "message": f"SMS NOT SENT! Error: {str(e)}"}), 500


from twilio.rest import Client

# Define your Twilio account credentials
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
number = 'your_twilio_number'

@app.route('/sms', methods=['GET'])
def sms_get():
    return render_template('sms.html')

@app.route('/sms', methods=['POST'])
def sms_post():
    msg = request.form['msg']
    no = "+91" + request.form['to']
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=msg,
        from_=number,
        to=no
    )
    return f"Message sent with SID: {message.sid}"