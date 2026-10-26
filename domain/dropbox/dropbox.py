import dropbox
from dropbox.files import FolderMetadata, FileMetadata
import core.config as config

DROPBOX_ACCESS_TOKEN = config.read_encrypted_flag('dropbox_access_token')
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

def read_dropbox_file(file_path: str) -> str:
    try:
        metadata, response = dbx.files_download(file_path)
        return response.content.decode('utf-8')
    except Exception as e:
        return f"Error reading file: {str(e)}"


def list_dropbox_directory(folder_path: str) -> list:
    try:
        if folder_path == "/":
            folder_path = ""

        response = dbx.files_list_folder(folder_path)
        items = []

        for entry in response.entries:
            if isinstance(entry, FolderMetadata):
                items.append({"name": entry.name, "type": "folder", "path": entry.path_display})
            elif isinstance(entry, FileMetadata):
                items.append({"name": entry.name, "type": "file", "path": entry.path_display})

        return items
    except Exception as e:
        return f"Error listing directory: {str(e)}"