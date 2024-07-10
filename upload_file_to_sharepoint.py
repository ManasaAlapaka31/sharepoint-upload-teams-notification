#!/usr/bin/env python3
from shareplum import Site
from shareplum import Office365
from shareplum.site import Version
from dotenv import load_dotenv
import os
import configparser
from datetime import datetime
import subprocess
import sys
import send_msg_In_teams_channel # Importing Teams file to post msg in Teams channel



def send_mail(file_name: str,sharepoint_name: str, file_link: str,script_name: str,description: str):

    Subject=f"{script_name} | {description}"
    Body=f"The file has been uploaded successfully to the {sharepoint_name} SharePoint."

    full_body = f"{Body}\n\nFile Name: {file_name}\nFile Link: {file_link}"
    
    # Encode the full body to bytes
    body_str_encoded_to_byte = full_body.encode()
    
    # Send the email
    return_stat = subprocess.run([f"mail", f"-s {Subject}", "Alapaka.Manasa@lumen.com"], input=body_str_encoded_to_byte)
    

def upload_file_to_sharepoint(file_path,sharepoint_name,script_name,description, config_file='sp_config.properties', env_file='.env'):

    load_dotenv(env_file)
    config = configparser.ConfigParser()
    config.read(config_file)

    # full_url = config['DEFAULT']['full_url']
    base_site_url = config['DEFAULT']['base_site_url']
    sharepoint_site = config['DEFAULT']['sharepoint_site']
    doc_library = config['DEFAULT']['doc_library']

    username = os.getenv('SP_USERNAME')
    password = os.getenv('SP_PASSWORD')

    site_url = base_site_url

    try:
        # Authenticate with SharePoint
        authcookie = Office365(sharepoint_site, username=username, password=password).GetCookies()
        if authcookie is None:
            print("Failed to authenticate with SharePoint.")
            return
        site = Site(site_url, version=Version.v365, authcookie=authcookie)
        print("Successfully connected to SharePoint site.")

        file_name = os.path.basename(file_path)

        # Check if the file already exists
        folder = site.Folder(doc_library)
        files = [file['Name'] for file in folder.files]
        if file_name in files:
            # If file exists, append a timestamp to the file name
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            name, extension = os.path.splitext(file_name)
            file_name = f"{name}_{timestamp}{extension}"

        # Upload the file
        print(f"Uploading file '{file_name}' to SharePoint...")
        with open(file_path, 'rb') as file_obj:
            folder.upload_file(file_obj, file_name)
        print(f"Uploaded!")
        print("================================================")      
        send_mail(file_name,sharepoint_name, f"'{site_url}/{doc_library}/{file_name}'",script_name,description)
        send_msg_In_teams_channel.send_details_to_teamsChannel(script_name,description, f"'{site_url}/{doc_library}/{file_name}'")
    except Exception as e:
        print(f"Failed to upload file. Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) ==5: 
        upload_file_to_sharepoint(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print("Usage: python3 sharepoint_v1.py <file_path> <sharepoint_name> <script_name> <description>")




