#!/bin/bash
# This script sets up a .desktop file to autostart the live dictation tool on login.

set -e

AUTOSTART_DIR="$HOME/.config/autostart"
DESKTOP_FILE="$AUTOSTART_DIR/live-dictation.desktop"
PROJECT_DIR="/home/phaedrus/AiSpace/whisper"

# Create the autostart directory if it doesn't exist
mkdir -p "$AUTOSTART_DIR"

# Create the .desktop file
cat > "$DESKTOP_FILE" << EOL
[Desktop Entry]
Type=Application
Name=Live Dictation
Comment=Whisper-based real-time dictation service
Exec=$PROJECT_DIR/venv/bin/python $PROJECT_DIR/live_dictation.py --model base.en
Terminal=false
StartupNotify=false
EOL

# Make the .desktop file executable (often required)
chmod +x "$DESKTOP_FILE"

echo "Successfully created $DESKTOP_FILE"
echo ""
echo "The live dictation script will now automatically start the next time you log in."
echo "To disable it, you can delete that file or use your desktop's 'Startup Applications' manager."
echo ""
echo "To start it immediately for this session without logging out, you can run:"
echo "nohup /home/phaedrus/AiSpace/whisper/venv/bin/python /home/phaedrus/AiSpace/whisper/live_dictation.py --model base.en > /dev/null 2>&1 &"

