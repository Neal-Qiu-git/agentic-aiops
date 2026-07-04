#!/usr/bin/env python3
"""Upload files to GitHub Pages using GitHub API."""
import base64, json, urllib.request, sys, os

TOKEN = os.environ.get("GITHUB_TOKEN", "").strip() or open(os.path.expanduser("~/.github_token")).read().strip()
REPO = "Neal-Qiu-git/agentic-aiops"
BASE = f"https://api.github.com/repos/{REPO}/contents"

def upload_file(local_path, remote_path, msg):
    with open(local_path, 'rb') as f:
        content = base64.b64encode(f.read()).decode()
    
    # Check if file exists
    url = f"{BASE}/{remote_path}"
    req = urllib.request.Request(url, headers={"Authorization": f"token {TOKEN}"})
    sha = None
    try:
        resp = urllib.request.urlopen(req)
        data = json.loads(resp.read())
        sha = data.get("sha")
    except:
        pass
    
    body = {"message": msg, "content": content, "branch": "main"}
    if sha:
        body["sha"] = sha
    
    data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, method="PUT", headers={
        "Authorization": f"token {TOKEN}",
        "Content-Type": "application/json"
    })
    try:
        resp = urllib.request.urlopen(req)
        result = json.loads(resp.read())
        print(f"✅ {remote_path} -> {result.get('content',{}).get('sha','?')[:12]}")
    except Exception as e:
        print(f"❌ {remote_path}: {e}")
        try:
            print(e.read().decode()[:200])
        except:
            pass

files = [
    ("index.html", "index.html"),
    ("assets/index-B59Sfut8.js", "assets/index-B59Sfut8.js"),
    ("assets/index-Buvu5_Y5.css", "assets/index-Buvu5_Y5.css"),
]

msg = "v4.7.1: fix DeploymentPage + MonitoringPage black screen (type mismatches)"
for local, remote in files:
    upload_file(local, remote, msg)
