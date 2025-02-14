import scapy.all as scapy
import socket
import subprocess
import re
import os
import datetime
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

DISCOVERY_RESULTS = "discovered_devices.csv"
DEVICE_LIMIT = 30


def get_local_ip():
    """Returns the local IP address of the machine on the primary interface."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print(f"❌ Failed to get local IP: {e}")
        return "127.0.0.1"


def get_network_range():
    """Dynamically fetch network subnet range from `ip route`."""
    try:
        result = subprocess.run(["ip", "route", "show"], capture_output=True, text=True)
        matches = re.findall(r'(\d+\.\d+\.\d+\.\d+/\d+)', result.stdout)
        for subnet in matches:
            if not subnet.startswith(("172.17", "172.18")):  # Skip Docker or virtual networks
                return subnet
        return "192.168.1.0/24"  # Fallback
    except Exception as e:
        print(f"⚠️ Failed to detect network range: {e}")
        return "192.168.1.0/24"


def get_mac_from_arp(ip):
    """Fetch MAC address from ARP table."""
    try:
        result = subprocess.run(["arp", "-n", ip], capture_output=True, text=True)
        match = re.search(r"(([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2})", result.stdout)
        return match.group(0) if match else "Unknown"
    except Exception as e:
        print(f"⚠️ Failed to get MAC for {ip}: {e}")
        return "Unknown"


def scan_arp(network):
    """Perform ARP scan using Scapy. Needs sudo."""
    devices = []
    try:
        arp_request = scapy.ARP(pdst=network)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        answered_list = scapy.srp(broadcast / arp_request, timeout=2, verbose=False)[0]

        for _, received in answered_list:
            devices.append({
                "IP": received.psrc,
                "MAC": received.hwsrc,
                "Device": "Unknown",
                "Type": "Unknown"
            })
        print(f"✅ ARP Scan detected {len(devices)} devices.")
    except Exception as e:
        print(f"❌ ARP Scan failed: {e}")

    return devices


def scan_nmap(network):
    """Perform a fast Nmap ping scan."""
    devices = []
    try:
        result = subprocess.run(
            ["nmap", "-sn", "-n", "--host-timeout", "500ms", "--max-retries", "1", network],
            capture_output=True, text=True
        )
        ip_addresses = re.findall(r"Nmap scan report for ([\d.]+)", result.stdout)

        for ip in ip_addresses:
            mac = get_mac_from_arp(ip)
            devices.append({
                "IP": ip,
                "MAC": mac,
                "Device": "Unknown",
                "Type": "Unknown"
            })
        print(f"✅ Nmap Scan detected {len(devices)} devices.")
    except Exception as e:
        print(f"❌ Nmap Scan failed: {e}")

    return devices


def scan_network():
    """Runs network discovery combining ARP & Nmap."""
    network = get_network_range()
    local_ip = get_local_ip()

    print(f"\n🔍 Scanning network: {network}")
    print(f"🖥️ Local IP detected: {local_ip}")

    with ThreadPoolExecutor(max_workers=2) as executor:
        arp_devices_future = executor.submit(scan_arp, network)
        nmap_devices_future = executor.submit(scan_nmap, network)

        arp_devices = arp_devices_future.result()
        nmap_devices = nmap_devices_future.result()

    # Merge and remove duplicates (prefer ARP results if overlap)
    discovered_devices = {device["IP"]: device for device in (arp_devices + nmap_devices)}.values()
    discovered_devices = list(discovered_devices)[:DEVICE_LIMIT]

    # Add local machine if not discovered already
    if local_ip not in [d["IP"] for d in discovered_devices]:
        discovered_devices.append({
            "IP": local_ip,
            "MAC": "Local Machine",
            "Device": socket.gethostname(),
            "Type": "This Machine"
        })

    # ✅ Display results in terminal
    print("\n📋 [Discovered Devices]")
    print("IP Address\t\tMAC Address\t\tDevice Name\t\tType")
    print("=" * 80)
    for device in discovered_devices:
        print(f"{device['IP']}\t{device['MAC']}\t{device['Device']}\t{device['Type']}")

    # ✅ Save results to CSV
    df = pd.DataFrame(discovered_devices)
    df["Timestamp"] = datetime.datetime.now()
    df.to_csv(DISCOVERY_RESULTS, index=False)

    print(f"\n✅ Discovery results saved in `{DISCOVERY_RESULTS}`.")
    return discovered_devices


if __name__ == "__main__":
    scan_network()

