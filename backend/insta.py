from instagrapi import Client

def post_on_instagram(username, password, photo_path, caption):
    try:
        client = Client()
        client.login(username, password)
        media = client.photo_upload(photo_path, caption=caption)
        media_id = media.pk
        return True, f"Photo uploaded successfully! Media ID: {media_id}"
    except Exception as e:
        return False, str(e)

username = input("Enter Instagram username: ")
password = input("Enter Instagram password: ")
photo_path = input("Enter photo path: ")
caption = input("Enter caption: ")

success, response_message = post_on_instagram(username, password, photo_path, caption)

if success:
    print(response_message)
else:
    print("Error:", response_message)