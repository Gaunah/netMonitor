import argparse
import csv
import os
import signal
import time
from datetime import datetime
from queue import Empty, Queue
from threading import Event, Thread

import speedtest
from pythonping import ping

# Configuration parameters
DEFAULT_PING_DESTINATION = "1.1.1.1"
DEFAULT_PING_SLEEP_DURATION = 5  # seconds
DEFAULT_SPEEDTEST_SLEEP_DURATION = 3600  # seconds
DEFAULT_FILENAME = "network_data.csv"

queue = Queue()
stop_event = Event()


def signal_handler(signum, frame):
    print("Caught signal. Stopping threads...")
    stop_event.set()


def internet_speed():
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = float("{:.2f}".format(st.download() / 10**6))
    upload_speed = float("{:.2f}".format(st.upload() / 10**6))
    print(f"Download Speed: {download_speed} Mbps, Upload Speed: {upload_speed} Mbps")
    return download_speed, upload_speed


def ping_test(destination):
    response_list = ping(destination, count=2, timeout=1)
    avg = float("{:.2f}".format(response_list.rtt_avg_ms))
    print(f"Ping: {avg} ms")
    return avg


def sleep_with_check(seconds):
    for _ in range(seconds):
        if stop_event.is_set():
            return
        time.sleep(1)


def ping_loop(destination, sleep_duration):
    while not stop_event.is_set():
        try:
            ping_avg = ping_test(destination)
        except Exception as e:
            print(f"Exception during ping test: {e}")
            ping_avg = "NA"
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        data = {
            "timestamp": timestamp,
            "ping_avg": ping_avg,
            "download_speed": "NA",
            "upload_speed": "NA",
        }
        queue.put(data)
        sleep_with_check(sleep_duration)


def speedtest_loop(sleep_duration):
    while not stop_event.is_set():
        try:
            download_speed, upload_speed = internet_speed()
        except Exception as e:
            print(f"Exception during speed test: {e}")
            download_speed, upload_speed = "NA", "NA"
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        data = {
            "timestamp": timestamp,
            "ping_avg": "NA",
            "download_speed": download_speed,
            "upload_speed": upload_speed,
        }
        queue.put(data)
        sleep_with_check(sleep_duration)


def write_to_csv_loop(filename):
    file_exists = os.path.isfile(filename)
    with open(filename, "a", newline="") as csvfile:
        headers = ["timestamp", "ping_avg", "download_speed", "upload_speed"]
        writer = csv.DictWriter(
            csvfile, delimiter=",", lineterminator="\n", fieldnames=headers
        )
        if not file_exists:
            writer.writeheader()
        while not stop_event.is_set():
            try:
                data = queue.get(timeout=1)
                writer.writerow(data)
                csvfile.flush()
            except Empty:
                continue


def main(ping_destination, ping_interval, speedtest_interval, filename):
    print(
        f"Start network test with:\n\tPing destination: {ping_destination}\n\tPing interval: {ping_interval}\n\tSpeedtest interval: {speedtest_interval}\n\tWriting to: {filename}\n"
    )
    try:
        signal.signal(signal.SIGINT, signal_handler)
        ping_thread = Thread(target=ping_loop, args=(ping_destination, ping_interval))
        speedtest_thread = Thread(target=speedtest_loop, args=(speedtest_interval,))
        writer_thread = Thread(target=write_to_csv_loop, args=(filename,))
        ping_thread.start()
        speedtest_thread.start()
        writer_thread.start()
        while not stop_event.is_set():
            time.sleep(0.1)
    except Exception as e:
        print(f"Caught exception. Stopping threads...\n{e}")
        stop_event.set()
        ping_thread.join()
        speedtest_thread.join()
        writer_thread.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run internet speed and ping tests.")
    parser.add_argument(
        "-d",
        "--ping-destination",
        default=DEFAULT_PING_DESTINATION,
        help="The destination for ping tests.",
    )
    parser.add_argument(
        "-p",
        "--ping-interval",
        type=int,
        default=DEFAULT_PING_SLEEP_DURATION,
        help="The sleep duration between ping tests in seconds.",
    )
    parser.add_argument(
        "-s",
        "--speedtest-interval",
        type=int,
        default=DEFAULT_SPEEDTEST_SLEEP_DURATION,
        help="The sleep duration between speed tests in seconds.",
    )
    parser.add_argument(
        "-f",
        "--filename",
        default=DEFAULT_FILENAME,
        help="The name of the output file.",
    )
    args = parser.parse_args()
    main(
        args.ping_destination,
        args.ping_interval,
        args.speedtest_interval,
        args.filename,
    )
