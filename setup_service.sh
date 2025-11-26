#!/bin/bash
# This script sets up the systemd user service for the live dictation tool.

set -e

SERVICE_DIR="$HOME/.config/systemd/user"
SERVICE_FILE="$SERVICE_DIR/live-dictation.service"
PROJECT_DIR="/home/phaedrus/AiSpace/whisper"

# Create the systemd user directory if it doesn't exist
mkdir -p "$SERVICE_DIR"

# Create the service file
cat > "$SERVICE_FILE" << EOL
[Unit]
Description=Live Dictation Service using Whisper
After=graphical-session.target

[Service]
ExecStart=$PROJECT_DIR/venv/bin/python $PROJECT_DIR/live_dictation.py --model base.en
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
EOL

echo "Successfully created $SERVICE_FILE"
echo ""
echo "To enable and start the service, run the following commands:"
echo "systemctl --user daemon-reload"
echo "systemctl --user enable --now live-dictation"
echo ""
echo "To check the status, run:"
echo "systemctl --user status live-dictation"
echo ""
echo "To view logs, run:"
echo "journalctl --user -u live-dictation -f"
