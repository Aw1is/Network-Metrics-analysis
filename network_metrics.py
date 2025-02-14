import os
import pandas as pd
import datetime
import subprocess
import re

DISCOVERY_RESULTS = "discovered_devices.csv"
METRICS_RESULTS = "network_metrics.csv"

PING_TIMEOUT = 3
IPERF_TIMEOUT = 5
TRACEROUTE_TIMEOUT = 10

# Devices where you have `iperf3 -s` running
IPERF_DEVICES = {"192.168.1.68"}  # Example: add your own IPs

def ensure_metrics_file():
    if not os.path.exists(METRICS_RESULTS):
        df = pd.DataFrame(columns=["Timestamp", "IP", "Latency (ms)", "Jitter (ms)", "Delay (ms)",
                                   "Throughput (Mbps)", "Bandwidth (Mbps)", "Hop Count"])
        df.to_csv(METRICS_RESULTS, index=False)
        print(f"✅ Created `{METRICS_RESULTS}` successfully.")

def get_discovered_devices():
    if not os.path.exists(DISCOVERY_RESULTS):
        print("❌ Discovery results not found. Testing with default 8.8.8.8")
        return ["8.8.8.8"]

    df = pd.read_csv(DISCOVERY_RESULTS)
    possible_columns = ["IP", "IP Address", "IP_Address"]
    for col in possible_columns:
        if col in df.columns:
            return df[col].dropna().tolist()

    print("❌ No valid IP column in discovery results. Using default 8.8.8.8")
    return ["8.8.8.8"]

def run_ping(target):
    try:
        result = subprocess.run(["ping", "-c", "4", "-W", str(PING_TIMEOUT), target], capture_output=True, text=True, timeout=PING_TIMEOUT + 2)
        latencies = [float(line.split("time=")[-1].split()[0]) for line in result.stdout.splitlines() if "time=" in line]

        if not latencies:
            return None, None

        jitter = max(latencies) - min(latencies)
        avg_latency = sum(latencies) / len(latencies)

        return avg_latency, jitter
    except Exception as e:
        print(f"⚠️ Ping failed for {target}: {e}")
        return None, None

def run_iperf(target):
    try:
        result = subprocess.run(["iperf3", "-c", target, "-J", "-t", str(IPERF_TIMEOUT)],
                                capture_output=True, text=True, timeout=IPERF_TIMEOUT + 2)

        match_bandwidth = re.search(r'"bits_per_second":\s*([\d.]+)', result.stdout)

        if match_bandwidth:
            throughput = float(match_bandwidth.group(1)) / 1e6
            return throughput, throughput

        return None, None

    except Exception as e:
        print(f"⚠️ iPerf3 error for {target}: {e}")
        return None, None

def run_speedtest():
    try:
        import speedtest
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1e6
        return download_speed, download_speed
    except Exception as e:
        print(f"⚠️ Speedtest failed: {e}")
        return None, None

def run_traceroute(target):
    try:
        result = subprocess.run(["traceroute", target], capture_output=True, text=True, timeout=TRACEROUTE_TIMEOUT)
        hops = len([line for line in result.stdout.splitlines() if line.strip()]) - 1
        delay = hops * 2
        return hops, delay
    except Exception as e:
        return None, None

def run_network_tests():
    ensure_metrics_file()
    devices = get_discovered_devices()
    results = []

    for index, device in enumerate(devices, 1):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n🚀 [{index}/{len(devices)}] Testing {device} at {timestamp}...")

        latency, jitter = run_ping(device)

        throughput, bandwidth = None, None
        if device in IPERF_DEVICES:
            throughput, bandwidth = run_iperf(device)

        elif device in {"8.8.8.8", "1.1.1.1"}:
            print(f"🌐 Running Speedtest for public IP {device}...")
            throughput, bandwidth = run_speedtest()

        hops, delay = run_traceroute(device)

        latency = latency if latency is not None else 0
        jitter = jitter if jitter is not None else 0
        delay = delay if delay is not None else 0
        throughput = throughput if throughput is not None else 0
        bandwidth = bandwidth if bandwidth is not None else 0
        hops = hops if hops is not None else 0

        print(f"📊 {device} | 🕒 Latency: {latency:.2f} ms | 📉 Jitter: {jitter:.2f} ms | ⏳ Delay: {delay} ms")
        print(f"🚀 Throughput: {throughput:.2f} Mbps | 📶 Bandwidth: {bandwidth:.2f} Mbps | 🛤 Hops: {hops}")

        results.append([timestamp, device, latency, jitter, delay, throughput, bandwidth, hops])

    df = pd.DataFrame(results, columns=["Timestamp", "IP", "Latency (ms)", "Jitter (ms)", "Delay (ms)",
                                        "Throughput (Mbps)", "Bandwidth (Mbps)", "Hop Count"])
    df.to_csv(METRICS_RESULTS, mode="a", header=False, index=False)

    print("\n✅ All network tests completed and results saved.")

if __name__ == "__main__":
    run_network_tests()

