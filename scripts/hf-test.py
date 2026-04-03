import os
from huggingface_hub import HfApi

token = None
if os.path.exists(".env"):
    with open(".env") as f:
        for line in f:
            if "HF_TOKEN=" in line and not line.startswith("#"):
                try:
                    token = line.split("=", 1)[1].strip().strip('"\'')
                except:
                    pass

api = HfApi()

print("Testing access across repo types...")

for r_type in ["model", "space", "dataset"]:
    try:
        info = api.repo_info(repo_id="doubas/paperclip", repo_type=r_type, token=token)
        print(f"✅ FOUND AS: {r_type.upper()}")
    except Exception as e:
        print(f"❌ NOT {r_type.upper()}: {e}")
