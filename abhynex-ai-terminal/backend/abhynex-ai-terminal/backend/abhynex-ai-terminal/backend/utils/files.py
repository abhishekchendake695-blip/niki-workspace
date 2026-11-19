import os
import shutil

class FileManager:
    def list_files(self, path='.'):
        return os.listdir(path)

    def read_file(self, path):
        with open(path, 'r') as f:
            return f.read()

    def write_file(self, path, content):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)

    def delete_path(self, path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)