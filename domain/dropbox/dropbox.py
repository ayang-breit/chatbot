import dropbox

DROPBOX_ACCESS_TOKEN = 'your_dropbox_token'
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

def read_dropbox_file(file_path: str) -> str:
    try:
        metadata, response = dbx.files_download(file_path)
        return response.content.decode('utf-8')
    except Exception as e:
        return f"Error reading file: {str(e)}"