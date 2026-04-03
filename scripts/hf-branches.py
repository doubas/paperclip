import os
from huggingface_hub import list_repo_refs

token = None
if os.path.exists(".env"):
    with open(".env") as f:
        for line in f:
            if "HF_TOKEN=" in line and not line.startswith("#"):
                token = line.split("=", 1)[1].strip().strip('"\'')

try:
    refs = list_repo_refs(repo_id="doubas/paperclip", repo_type="space", token=token)
    branches = [ref.name for ref in refs.branches]
    print(f"BRANCHES FOUND: {branches}")
except Exception as e:
    print(f"ERROR: {e}")
