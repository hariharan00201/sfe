import Google
from googleapiclient.http import MediaFileUpload

def addblogs(filename,filetype):
    CLIENT_SECRET_FILE = 'client_secret_file.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES =['https://www.googleapis.com/auth/drive']

    service = Google.Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    folder_id = '1bGQQARcvjmrTK17-4pHaVBp1aTTC6qOX'
    filename = filename
    mime_type = filetype
    file_metadata = {
        'name' : filename,
        'parents':[folder_id]
    }
    media = MediaFileUpload('./gfolder/'+filename,mimetype=mime_type)
    service.files().create(
        body = file_metadata,
        media_body = media,
        fields = 'id'
    ).execute()
