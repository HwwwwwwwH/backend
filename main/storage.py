import os
from django.core.files.storage import FileSystemStorage
from backend.settings import MEDIA_ROOT


class FileStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(MEDIA_ROOT, name))
        return name