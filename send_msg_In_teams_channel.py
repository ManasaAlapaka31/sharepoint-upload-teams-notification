import requests
import json
import configparser
import subprocess
import sys

def send_email(script_name, description, file_link=None):

    Subject=f"{script_name} | {description}"
    if not file_link:
        Body=f"Below Script executed and posted details in Teams channel:\n Script Name: {script_name}\n Description: {description}"
    else:
        Body=f"File has been shared successfully in Teams channel:\nScript Name: {script_name}\n Description: {description}\n File link: {file_link}"

    # Encode the full body to bytes
    body_str_encoded_to_byte = Body.encode()
    # Send the email
    return_stat = subprocess.run([f"mail", f"-s {Subject}", "Alapaka.Manasa@lumen.com"], input=body_str_encoded_to_byte)




def send_details_to_teamsChannel(script_name, description, file_link):

    # Load configuration
    config = configparser.ConfigParser()
    config.read('tch_config.properties')
    webhook_url = config.get('DEFAULT', 'webhook_url') 

    # Default message if none provided
    if not file_link:

        msg=f"Below Script executed\n\n Script: {script_name}\n\n Description: {description}"

    else:
        msg=f"Below script executed and File shared in sharepoint. \n\n Script: {script_name}\n\n Description: {description}\n\n File link: {file_link}"

    payload = {
        "text":msg
    }


   # Headers for the HTTP request
    headers = {
        'Content-Type': 'application/json'
    }

    # Send the POST request
    response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))

    print("Sending message to Teams channel...")

    # Check the response
    if response.status_code == 200:
        print("Completed!")
        print("================================================")    
        send_email(script_name=script_name, description=description, file_link=file_link)
    else:
        print("Failed to send message")

if __name__ == "__main__":
    if len(sys.argv) > 4 or len(sys.argv) < 3:
        print("Usage: python3 teamschannel_v1.py <script_name> <Description> [file_link]")
    else:
        script_name = sys.argv[1]
        description = sys.argv[2]
        file_link = sys.argv[3] if len(sys.argv) == 4 else None
        send_details_to_teamsChannel(script_name=script_name, description=description, file_link=file_link)

