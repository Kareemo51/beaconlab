from datetime import datetime
import os
from collections import Counter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "logs", "beacons.log")

def read_beacon_times():
    times = []

    with open(LOG_FILE, "r") as f:
        for line in f:
            if line.startswith("["):
                timestamp = line.split("]")[0].strip("[")
                dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                times.append(dt)

    return times

def calculate_intervals(times):
    intervals = []

    for i in range(1, len(times)):
        delta = (times[i] - times[i - 1]).total_seconds()
        intervals.append(delta)

    return intervals

def detect_regular_beaconing(intervals):
    if len(intervals) < 3:
        print("Not enough data yet.")
        return

    rounded = [round(x) for x in intervals]
    counts = Counter(rounded)

    most_common_interval, count = counts.most_common(1)[0]
    percentage = (count / len(rounded)) * 100

    print(f"Most common interval: {most_common_interval} seconds")
    print(f"Match rate: {percentage:.2f}%")

    if percentage >= 80:
        print(f"ALERT: Mostly regular beaconing detected around {most_common_interval} seconds.")
    else:
        print("No strong regular beaconing pattern detected.")

def main():
    times = read_beacon_times()
    intervals = calculate_intervals(times)

    print("Intervals:", intervals)
    detect_regular_beaconing(intervals)

if __name__ == "__main__":
    main()