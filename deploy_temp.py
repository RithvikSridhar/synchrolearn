import http.client
import tarfile
import io
import os

src = r"C:\Users\rithv\synchrolearn"
os.chdir(src)

buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode='w:gz') as tar:
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.github']]
        for file in files:
            filepath = os.path.join(root, file)
            tar.add(filepath)
buf.seek(0)
data = buf.read()
print(f"Archive size: {len(data)} bytes")

conn = http.client.HTTPSConnection('api.netlify.com')
headers = {
    'Content-Type': 'application/tar+gzip',
    'Content-Length': str(len(data))
}
conn.request('POST', '/api/v1/sites', body=data, headers=headers)
resp = conn.getresponse()
result = resp.read().decode()
print(f"Status: {resp.status}")
print(result[:2000])