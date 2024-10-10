from flask import Flask, render_template, request, jsonify
import boto3
import subprocess
import os
# import backend.ec2 as ec2
# import backend.emailing as emailapi 
# from flask import Flask, render_template, request, redirect, url_for
from twilio.rest import Client
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
import cv2
from instapy import InstaPy


# Initialize Flask app
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/bulkmail')
def bulkmail():
    return render_template('bulkmail.html')

@app.route('/bulkmail_send', methods=['POST'])
def send_bulk_email():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Invalid request data'}), 400

    smtp_server = data.get('smtp_server')
    smtp_port = data.get('smtp_port')
    smtp_user = data.get('smtp_user')
    smtp_password = data.get('smtp_password')
    from_email = data.get('from_email')
    to_emails = data.get('to_emails')
    subject = data.get('subject')
    body = data.get('body')

    if not all([smtp_server, smtp_port, smtp_user, smtp_password, from_email, to_emails, subject, body]):
        return jsonify({'message': 'Missing required fields'}), 400

    to_emails = [email.strip() for email in to_emails.split(',')]

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)

        for email in to_emails:
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            server.sendmail(from_email, email, msg.as_string())

        server.quit()
        return jsonify({'message': 'Emails sent successfully'})
    except Exception as e:
        print("Error sending email:", str(e))
        return jsonify({'message': 'Error sending email'}), 500

@app.route('/ec2')
def ec2():
    return render_template('ec2.html')


@app.route('/ec2/instance_launch')
def ec2_instance_launch():
    aws_access_key_id=request.json['aws_access_key_id']
    aws_secret_access_key=request.json['aws_secret_access_key']
    region_name=request.json['region_name']
    instance_type=request.json['instance_type']
    image_id=request.json['image_id']
    
    try:
        ec2.instance_launch(aws_access_key_id, aws_secret_access_key, region_name, instance_type, image_id)
        return jsonify({'status': 'success', 'message': 'EC2 instance successfully launched'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message':str(e)}), 500


@app.route('/docker')
def docker():
    return render_template('docker.html')

@app.route("/pull", methods=['post'])
def pull():
    img=request.form['docker']
    cmd=f'docker pull {img}'
    status,output = subprocess.getstatusoutput(cmd)
    if status == 0:
        image_name = output.split('/')[-1]
        return image_name
    else:
        return("image downloded failed")

@app.route("/images", methods=['post'])
def get_images():
    status,output = subprocess.getstatusoutput('docker images')
    if status == 0:
        img = re.sub(r'(SIZE|MB|kB)', r'\1\n', output)
        return img
    else:
        return("image downloded failed")




@app.route('/emailing')
def emailing():
    return render_template('emailing.html')

@app.route('/emailing/send_email')
def eamiling_send():
    to=request.json['']
    message=request.json['']
    message = emailapi.send_email(to, message)
    print(message)


@app.route('/googles')
def googles():
    return render_template('googles.html')

# Google Custom Search API credentials
API_KEY = "YOUR_API_KEY"
SEARCH_ENGINE_ID = "YOUR_SEARCH_ENGINE_ID"

@app.route('/googles', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Query is required'})

    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}"
    response = request.get(url)
    data = response.json()

    results = []
    for result in data['items']:
        results.append({
            'title': result['title'],
            'link': result['link'],
            'snippet': result['snippet']
        })

    return jsonify({'results': results})   

@app.route('/insta')
def insta():
    return render_template('insta.html')

def post_on_instagram(username, password, photo_path, caption):
    session = InstaPy(username=username, password=password)
    session.login()
    session.upload_photo(photo_path, caption=caption)
    session.logout()
    return True, "Post uploaded successfully"

@app.route('/insta/post_on_instagram', methods=['POST'])
def insta_post():
    if request.is_json:
        username = request.json['username']
        password = request.json['password']
        photo_path = request.json['photo_path']
        caption = request.json['caption']
    else:
        username = request.form['username']
        password = request.form['password']
        photo = request.files['photo']
        caption = request.form['caption']
        photo_path = f"temp_{photo.filename}"
        photo.save(photo_path)

    try:
        success, response_message = post_on_instagram(username, password, photo_path, caption)
        import os
        os.remove(photo_path)
        return jsonify({'status': 'success', 'message': response_message}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    


@app.route('/s3')
def s3():
    return render_template('s3.html')

@app.route('/create_bucket', methods=['POST'])
def create_bucket():
    data = request.get_json()
    aws_access_key = data['aws_access_key']
    aws_secret_key = data['aws_secret_key']
    bucket_name = data['bucket_name']
    region = data['region']

    # Create an S3 client
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key,
                             aws_secret_access_key=aws_secret_key,
                             region_name=region)

    # Create the S3 bucket
    try:
        s3.create_bucket(Bucket=bucket_name)
        return jsonify({'message': f"Bucket '{bucket_name}' created successfully!"})
    except Exception as e:
        return jsonify({'error': f"Error creating bucket: {e}"})

@app.route('/upload_file', methods=['POST'])
def upload_file():
    data = request.get_json()
    aws_access_key = data['aws_access_key']
    aws_secret_key = data['aws_secret_key']
    bucket_name = data['bucket_name']
    file_name = data['file_name']
    file_content = data['file_content']
    region = data['region']

    # Create an S3 client
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key,
                             aws_secret_access_key=aws_secret_key,
                             region_name=region)

    # Upload the file to the S3 bucket
    try:
        s3.put_object(Body=file_content, Bucket=bucket_name, Key=file_name)
        return jsonify({'message': f"File '{file_name}' uploaded successfully!"})
    except Exception as e:
        return jsonify({'error': f"Error uploading file: {e}"})


@app.route('/sms')
def sms_get():
    return render_template('sms.html')

account_sid = " " #enter ur credentials
auth_token = ' '# enter ur credentials
number = '+14692146692'

@app.route("/sms", methods=['post'])
def sms_post():
    msg=request.form['msg']
    no="+91"+request.form['to']
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    body=msg,

	    from_=number,

	    to=no

	)
    return(f"Message sent with SID: {message.sid}")

@app.route('/whatsapp')
def whatsapp():
    return render_template('whatsapp.html')
@app.route("/whatsapp", methods=['post'])
def wth():
    client = Client(account_sid, auth_token)
    account_sid = 'your_account_sid'
    auth_token = 'your_auth_token'
    message = client.messages.create(
    from_='whatsapp:+14692146692',
    body=request.form['body'],
    to='whatsapp:+91'+request.form['to']
)
    return (f"Message sent with SID: {message.sid}")

    
@app.route('/call')
def call_page():
    return render_template('call.html')

@app.route("/call_now", methods=['POST'])
def call_now():
    # Get the phone number from the form
    no = '+91' + request.form['to']  # Ensure you get the number from the form input9++++++++++++++++++++++++++++++++++++++++++++++++
    
    # Twilio credentials from environment variables
    account_sid = " "#enter ur credentials
    auth_token = " "#enter ur credentials

    if not account_sid or not auth_token:
        return "Twilio credentials not set", 500  # Early return to handle missing credentials

    client = Client(account_sid, auth_token)
    
    try:
        # Create a call using Twilio API
        call = client.calls.create(
            from_='+14692146692',  # Replace with your Twilio number
            to=no,
            url="http://demo.twilio.com/docs/voice.xml"
        )
        
        # Return the call SID or a confirmation message
        return f"Call initiated with SID: {call.sid}"
    
    except Exception as e:
        # Print the error to console and return error message
        print(f"Error: {e}")
        return f"Failed to initiate call: {str(e)}", 500


@app.route('/livestream')
def livestream():
    return render_template('livestream.html')

@app.route('/liveStream', methods=['POST'])
def liveStream():
    stream = request.get_json()
    cap = cv2.VideoCapture(stream)
    while True:
        ret, frame = cap.read()
        if not ret:
            break;
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return jsonify({'status': 'frame processed'})



##if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    app.run()
if __name__ == "__main__":
    app.run(debug=True)
