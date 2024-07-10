This repository contains scripts for uploading files to SharePoint and sending notifications to a Teams channel.

## Configuration

### Environment Variables
Create a `.env` file in the root directory with the following variables:
- `SP_USERNAME`: Your SharePoint username.
- `SP_PASSWORD`: Your SharePoint password.

### Property Files
The `sp_config.properties` file should contain the SharePoint site URL configuration:
- `sharepoint_site`
- `base_site_url`
- `doc_library`
The `tch_config.properties` file should contain Teams channel configuration:
- `webhook_url`: The webhook URL for your Teams channel.


## Usage

### Uploading Files to SharePoint
Run the `upload_file_to_sharepoint.py` script with the necessary parameters to upload files to SharePoint.

### Sending Messages to Teams Channel
Run the `send_msg_In_teams_channel.py` script to send a notification message to the specified Teams channel.

## Dependencies
Ensure you have the following Python packages installed:
- `shareplum`
- `python-dotenv`
- `requests`

You can install them using pip:
pip install shareplum python-dotenv requests
