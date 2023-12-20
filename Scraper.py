import os
import pandas as pd
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    # Replace 'your_folder_id_here' with your actual folder ID
    folder_id = '1Qsz5ZAgZNN_cZFC8jufUHVAP3lsvOg20'
    query = f"'{folder_id}' in parents and trashed=false"

    # Call the Drive v3 API
    results = service.files().list(
        q=query, pageSize=1000, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
        return

    file_data = [{"Title": item['name'], "Link": f"https://drive.google.com/uc?id={item['id']}"} for item in items]

    df = pd.DataFrame(file_data)

    # Define the full path for the Excel file
    output_file_path = '/Users/jadrima/Desktop/Yeet/ComputerScience.csv'  # Change this to your desired path

    # Save the DataFrame to an Excel file at the specified path
    df.to_csv(output_file_path, index=False)


    print(f'File list exported to {output_file_path}')

if __name__ == '__main__':
    main()