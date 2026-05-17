import http.client
import json
import tarfile
import io
import os
import ssl

src = r"C:\Users\rithv\synchrolearn"
os.chdir(src)

# Build tar.gz
buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode='w:gz') as tar:
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.github']]
        for file in files:
            filepath = os.path.join(root, file)
            tar.add(filepath)
buf.seek(0)
data = buf.read()
print(f"Archive: {len(data)} bytes, SHA256: {hash(data)}")

# Try tiiny.host API (free, no auth for small files)
import urllib.parse

conn = http.client.HTTPSConnection('api.tiiny.host')
boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
body = b'--' + boundary.encode() + b'\r\n'
body += b'Content-Disposition: form-data; name="file"; filename="site.tar.gz"\r\n'
body += b'Content-Type: application/gzip\r\n\r\n'
body += data
body += b'\r\n--' + boundary.encode() + b'--\r\n'

headers = {
    'Content-Type': f'multipart/form-data; boundary={boundary}',
    'Content-Length': str(len(body))
}
conn.request('POST', '/api/v1/site/upload', body=body, headers=headers)
resp = conn.getresponse()
print(f"Status: {resp.status}")
print(resp.read().decode()[:1000])