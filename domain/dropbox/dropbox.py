import dropbox
from dropbox.files import FolderMetadata, FileMetadata
import core.config as config
import requests
import core.tools as t

def get_dropbox_obj():
    return dropbox.Dropbox(get_fresh_access_token())

def read_dropbox_file(file_path: str) -> str:
    try:
        metadata, response = get_dropbox_obj().files_download(file_path)
        return response.content.decode('utf-8')
    except Exception as e:
        return f"Error reading file: {str(e)}"


def list_dropbox_directory(folder_path: str) -> list:
    try:
        if folder_path == "/":
            folder_path = ""

        response = get_dropbox_obj().files_list_folder(folder_path)
        items = []

        for entry in response.entries:
            if isinstance(entry, FolderMetadata):
                items.append({"name": entry.name, "type": "folder", "path": entry.path_display})
            elif isinstance(entry, FileMetadata):
                items.append({"name": entry.name, "type": "file", "path": entry.path_display})

        return items
    except Exception as e:
        return f"Error listing directory: {str(e)}"

@t.memoize(ttl=60*60)
def get_fresh_access_token():
    response = requests.post(
        "https://api.dropbox.com/oauth2/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": config.read_encrypted_flag('dropbox_refresh_token'),
            "client_id": config.read_encrypted_flag('dropbox_app_key'),
            "client_secret": config.read_encrypted_flag('dropbox_app_secret'),
        },
    )
    if response.status_code == 200:
        return response.json().get("access_token")
    raise Exception(f"Failed to refresh token: {response.text}")