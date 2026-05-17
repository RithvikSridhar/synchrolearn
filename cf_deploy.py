import http.client
import json
import tarfile
import io
import os
import time

src = r"C:\Users\rithv\synchrolearn"
os.chdir(src)

# Build tar.gz excluding .git and .github
buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode='w:gz') as tar:
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.github']]
        for file in files:
            filepath = os.path.join(root, file)
            tar.add(filepath)
buf.seek(0)
data = buf.read()
print(f"Archive: {len(data)} bytes")

project_name = "synchrolearn-preview"

# Step 1: Create Cloudflare Pages project
conn = http.client.HTTPSConnection('api.cloudflare.com')
payload = json.dumps({
    "name": project_name,
    "source": {"type:": "drop"},
    "deployment_config": {
        "env": {"var": []}
    }
}).replace('"type:"', '"type":')

headers = {
    'Content-Type': 'application/json',
    'X-Auth-Email': 'rithvik.sridhar93@gmail.com',
    'X-Auth-Key': '${CF_API_KEY}'
}
conn.request('POST', '/client/v4/accounts/${CF_ACCOUNT_ID}/pages/projects', body=payload, headers=headers)
resp = conn.getresponse()
print("Create project:", resp.status, resp.read().decode()[:500])