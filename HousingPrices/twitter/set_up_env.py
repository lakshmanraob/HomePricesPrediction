import json
from pathlib import Path

script_location = Path(__file__).absolute().parent
print(script_location)
with open(script_location / 'settings.json', encoding='utf-8') as setting_file:
    data = json.loads(setting_file.read())

print(data['access_token'])
