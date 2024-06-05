import psutil
import logging
import threading
from time import sleep
import argparse as ap

logging.basicConfig(filename='system_health.log', level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

def get_arguments():
    parser = ap.ArgumentParser(description='System Health Monitoring Script')
    parser.add_argument('-ci', '--cpu_interval', type=int, default=5, help='Interval for CPU usage check in seconds')
    parser.add_argument('-mi', '--memory_interval', type=int, default=5, help='Interval for memory usage check in seconds')
    parser.add_argument('-di', '--disk_interval', type=int, default=5, help='Interval for disk usage check in seconds')
    parser.add_argument('-ri', '--process_interval', type=int, default=5, help='Interval for running processes check in seconds')
    parser.add_argument('-il', '--ignore_list', nargs='+', default=["snap"], help='List of mount points to ignore for disk usage check')
    return parser.parse_args()

def check_cpu_usage(threshold=80, interval=10):
    """ Check CPU usage every 'interval' seconds. """
    while True:
        cpu_usage = psutil.cpu_percent(interval=interval)
        if cpu_usage > threshold:
            logging.warning(f"CPU usage is at {cpu_usage}%!")
            print(f"CPU usage is at {cpu_usage}%!")
        sleep(interval-1)

def check_memory_usage(threshold=80, interval=10):
    """ Check memory usage every 'interval' seconds. """
    while True:
        memory = psutil.virtual_memory()
        memory_usage = (memory.used / memory.total) * 100
        if memory_usage > threshold:
            logging.warning(f"Memory usage is at {memory_usage:.2f}%!")
            print(f"Memory usage is at {memory_usage:.2f}%!")
        sleep(interval)

def check_disk_usage(threshold=80, ignore_list=None, interval=1800):
    """ Check disk usage every 'interval' seconds. """
    if ignore_list is None:
        ignore_list = []
    while True:
        partitions = psutil.disk_partitions()
        for partition in partitions:
            if any(keyword in partition.mountpoint for keyword in ignore_list):
                continue
            usage = psutil.disk_usage(partition.mountpoint)
            disk_usage = (usage.used / usage.total) * 100
            if disk_usage > threshold:
                logging.warning(f"Disk usage on {partition.mountpoint} is at {disk_usage:.2f}%!")
                print(f"Disk usage on {partition.mountpoint} is at {disk_usage:.2f}%!")
        sleep(interval)

def check_running_processes(threshold=100, interval=15):
    """ Check running processes every 'interval' seconds. """
    while True:
        processes = psutil.pids()
        if len(processes) > threshold:
            logging.warning(f"There are {len(processes)} running processes!")
            print(f"There are {len(processes)} running processes!")
        sleep(interval)

def main():
    args = get_arguments()
    threads = [
        threading.Thread(target=check_cpu_usage, args=(10, args.cpu_interval)),
        threading.Thread(target=check_memory_usage, args=(1, args.memory_interval)),
        threading.Thread(target=check_disk_usage, args=(1, args.ignore_list, args.disk_interval)),
        threading.Thread(target=check_running_processes, args=(100, args.process_interval))
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
