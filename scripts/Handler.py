import subprocess
import signal
import sys

# Paths to the scripts
script1 = "measure.py"
script2 = "lightManager.py"

# Function to handle KeyboardInterrupt
def handle_interrupt(processes):
    print("\nKeyboardInterrupt detected! Stopping child processes...")
    for process in processes:
        process.send_signal(signal.SIGINT)  # Send KeyboardInterrupt to child process
    for process in processes:
        process.wait()  # Wait for processes to exit
    print("All child processes stopped. Exiting.")
    sys.exit(0)

def main():
    # Start the scripts as subprocesses
    processes = [
        subprocess.Popen(["python3", script1]),
        subprocess.Popen(["python3", script2])
    ]

    try:
        print("Scripts are running. Press Ctrl+C to stop.")
        for process in processes:
            process.wait()  # Wait for processes (blocks the main script)

    except KeyboardInterrupt:
        handle_interrupt(processes)

if __name__ == "__main__":
    main()