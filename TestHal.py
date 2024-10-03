#!/usr/bin/env python3

from hal import FanatecDeviceMonitor

def main():
    monitor = FanatecDeviceMonitor()
    monitor.start_monitoring()

if __name__ == "__main__":
    main()