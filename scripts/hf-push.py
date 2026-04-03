import os
import subprocess

def git_push_to_hf():
    """
    Bypasses the Hugging Face API entirely and uses standard Git
    by injecting the HF_TOKEN into the remote URL. 
    This avoids the 404 preupload bugs on new spaces and ensures
    a perfect delta push.
    """
    token = os.getenv("HF_TOKEN")
    if not token and os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                if "HF_TOKEN=" in line and not line.startswith("#"):
                    token = line.split("=", 1)[1].strip().strip('"\'')
    
    if not token:
        print("❌ HF_TOKEN not found in .env")
        return

    print("🔄 Initializing secure Git injection to Hugging Face Space...")

    # The secure URL with the injected token
    remote_url = f"https://doubas:{token}@huggingface.co/spaces/doubas/paperclip"
    
    # Run the Git sequence
    commands = [
        ["git", "remote", "remove", "hf"],
        ["git", "remote", "add", "hf", remote_url],
        ["git", "add", "."],
        ["git", "commit", "-m", "🚀 Deploy latest Paperclip bits (Persistence & Sandbox fixes)"],
        ["git", "push", "hf", "HEAD:main", "--force"]
    ]

    print("📦 Packing delta and pushing...")
    
    success = True
    for cmd in commands:
        # Check=False because remove might fail if it doesn't exist, commit might fail if no changes
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # If the push fails specifically, we want to know
        if "push" in cmd and result.returncode != 0:
            print("\n❌ Git Push Failed:")
            print(result.stderr.replace(token, "[HIDDEN_TOKEN]"))
            success = False

    if success:
        print("\n✅ SUCCESS! Code securely pushed to Hugging Face Space.")
        print("🔗 View progress at: https://huggingface.co/spaces/doubas/paperclip")
    
    # Cleanup to ensure the token isn't sticking around in the git config
    subprocess.run(["git", "remote", "remove", "hf"], capture_output=True)

if __name__ == "__main__":
    git_push_to_hf()
