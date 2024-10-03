#!/usr/bin/env python3

from hal import FanatecDeviceMonitor

def main():
    monitor = FanatecDeviceMonitor()
    monitor.start()

    try:
        # Main application logic can continue here
        while True:
            pass  # Replace with your application logic
    except KeyboardInterrupt:
        # Handle cleanup on exit
        monitor.stop()
        print("Device monitoring stopped.")

if __name__ == "__main__":
    main()