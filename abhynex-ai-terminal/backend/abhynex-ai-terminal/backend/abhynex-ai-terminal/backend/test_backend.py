import requests
import json

def test_root():
    try:
        res = requests.get('http://localhost:8000/')
        print(f'Root: {res.json()}')
    except Exception as e:
        print(f'Root failed: {e}')

if __name__ == '__main__':
    # This is just a placeholder for manual testing or CI
    print('Backend test script ready.')