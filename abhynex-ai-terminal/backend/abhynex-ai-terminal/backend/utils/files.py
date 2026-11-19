import os
import shutil
from typing import List, Dict

def list_files(path: str = '.') -> List[Dict]:
    items = []
    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        items.append({
            'name': item,
            'is_dir': os.path.isdir(full_path),
            'size': os.path.getsize(full_path) if os.path.isfile(full_path) else 0
        })
    return items

def read_file(path: str) -> str:
    with open(path, 'r') as f:
        return f.read()

def write_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)

def delete_path(path: str):
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)