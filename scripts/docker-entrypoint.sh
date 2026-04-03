#!/bin/sh
set -e

# --- PERSISTENCE LAYER ---
echo "Provisioning persistent storage on /data..."
mkdir -p /data/.gemini
mkdir -p /data/instances/default/workspaces
mkdir -p /data/instances/default/companies
mkdir -p /data/storage

# Link .gemini to home for project persistence
if [ ! -L "/home/node/.gemini" ]; then
    rm -rf "/home/node/.gemini"
    ln -s /data/.gemini "/home/node/.gemini"
fi

# Link instances to local folder for config persistence if needed
# (Paperclip often looks in current_dir/instances)
if [ ! -L "/home/node/app/instances" ]; then
    # Only link if not existing
    ln -s /data/instances /home/node/app/instances || true
fi

# --- AGENT PROVISIONING ---
# Ensure the CEO agent path exists to prevent ENOENT crashes
CEO_COMPANY_ID="465e25ff-f9c4-4c65-9411-67fe8b966451"
CEO_AGENT_ID="6f030d76-657d-49a3-9c06-b74afcf4c3ef"
AGENT_INSTR_DIR="/data/instances/default/companies/$CEO_COMPANY_ID/agents/$CEO_AGENT_ID/instructions"

mkdir -p "$AGENT_INSTR_DIR"
if [ ! -f "$AGENT_INSTR_DIR/AGENTS.md" ]; then
    echo "Seeding missing AGENTS.md for CEO..."
    cat > "$AGENT_INSTR_DIR/AGENTS.md" <<EOF
# CEO Agent Instructions
You are the CEO of doubasco. Your goal is to coordinate operations and ensure project success.
EOF
fi

# --- USER PERMISSIONS ---
if [ "$(id -u)" = "0" ]; then
    PUID=${USER_UID:-1000}
    PGID=${USER_GID:-1000}
    changed=0
    if [ "$(id -u node)" -ne "$PUID" ]; then
        usermod -o -u "$PUID" node
        changed=1
    fi
    if [ "$(id -g node)" -ne "$PGID" ]; then
        groupmod -o -g "$PGID" node
        usermod -g "$PGID" node
        changed=1
    fi
    if [ "$changed" = "1" ]; then
        chown -R node:node /data
    fi

    if [ "$PAPERCLIP_MIGRATION_AUTO_APPLY" = "true" ]; then
        echo "Synchronizing administrator state..."
        gosu node pnpm paperclipai auth bootstrap-ceo --base-url "https://doubas-paperclip.hf.space"
    fi
    exec gosu node "$@"
else
    if [ "$PAPERCLIP_MIGRATION_AUTO_APPLY" = "true" ]; then
        echo "Synchronizing administrator state..."
        pnpm paperclipai auth bootstrap-ceo --base-url "https://doubas-paperclip.hf.space"
    fi
    exec "$@"
fi
