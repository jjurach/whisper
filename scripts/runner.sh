#!/bin/bash

# ==============================================================================
# runner.sh - Manages the live_dictation.py process
#
# USAGE:
#   ./runner.sh [COMMAND]
#
# COMMANDS:
#   start     Starts the live_dictation.py process in the background if it
#             is not already running.
#   stop      Stops the running live_dictation.py process.
#   restart   Stops the process (if running) and then starts it again.
#   status    Checks if the process is currently running and reports its PID.
#
# LOGGING:
#   All output (stdout and stderr) from the live_dictation.py script is
#   appended to the log file located at: ./whisper.log
#
# PID FILE:
#   The script uses a PID file to keep track of the running process:
#   ./whisper.pid
# ==============================================================================

# --- Configuration ---
cd "$(dirname "$0")" # Ensure we are in the script's directory
TMP_DIR="tmp"
LOG_FILE="$TMP_DIR/whisper.log"
PID_FILE="$TMP_DIR/whisper.pid"
VENV_PYTHON="venv/bin/python"
SCRIPT_PATH="live_dictation.py"
SCRIPT_ARGS="--model small.en"

# Create tmp directory if it doesn't exist
mkdir -p $TMP_DIR

# --- Functions ---

# Function to check if the process is running
is_running() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        # Check if a process with that PID exists
        if ps -p $PID > /dev/null; then
            return 0 # 0 is success (true in shell)
        fi
    fi
    return 1 # 1 is failure (false in shell)
}

do_start() {
    if is_running; then
        echo "Process is already running with PID $(cat "$PID_FILE")."
        return
    fi

    echo "Starting process..."
    # Set the PyTorch memory management environment variable and start the script.
    export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
    # Start the python script in the background using nohup
    # and redirect all output to the log file.
    nohup $VENV_PYTHON $SCRIPT_PATH $SCRIPT_ARGS >> "$LOG_FILE" 2>&1 &
    
    # Capture the PID of the last backgrounded process
    PID=$!
    
    # Write the PID to the pidfile
    echo $PID > "$PID_FILE"
    
    echo "Process started with PID $PID. Output is logged to $LOG_FILE."
}

do_stop() {
    if ! is_running; then
        echo "Process is not running."
        # Clean up stale pidfile if it exists
        if [ -f "$PID_FILE" ]; then
            rm "$PID_FILE"
        fi
        return
    fi

    PID=$(cat "$PID_FILE")
    echo "Stopping process with PID $PID..."
    
    # Kill the process
    kill $PID
    
    # Wait a moment and check if the process has stopped
    sleep 1
    if is_running; then
        echo "Process did not stop gracefully. Forcing..."
        kill -9 $PID
    fi
    
    # Remove the pidfile
    rm "$PID_FILE"
    echo "Process stopped."
}

do_status() {
    if is_running; then
        echo "Process is running with PID $(cat "$PID_FILE")."
    else
        echo "Process is not running."
    fi
}


# --- Main Logic ---
COMMAND=$1

if [ -z "$COMMAND" ]; then
    echo "Usage: $0 {start|stop|restart|status}"
    exit 1
fi

case "$COMMAND" in
    start)
        do_start
        ;;
    stop)
        do_stop
        ;;
    restart)
        echo "Restarting process..."
        do_stop
        sleep 1
        do_start
        ;;
    status)
        do_status
        ;;
    *)
        echo "Invalid command: $COMMAND"
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac

exit 0
