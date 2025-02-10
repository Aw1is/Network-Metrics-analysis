# Network-Metrics-analysis
**📡 Network Performance &amp; Anomaly Detection**   A real-time network monitoring tool that discovers devices, measures latency, jitter, throughput, bandwidth, and more. Generates visual insights with bar graphs. Integrates iPerf3 for bandwidth tests. Easy setup with troubleshooting guide. Check **README.md** for details! 🚀

# **📌 Network Performance and Anomaly Detection - User Guide** ✨🔍📊  
_A Comprehensive Guide to Setting Up, Running, and Troubleshooting the Project_ 🚀💡🔧

---

## **📚 Table of Contents** 📖✅📝
1. [Introduction](#introduction)  
2. [Installation and Setup](#installation-and-setup)  
   - Install Required Dependencies  
   - Create and Activate a Virtual Environment  
3. [Running the Project](#running-the-project)  
   - Step 1: Network Discovery  
   - Step 2: Network Metrics Collection  
   - Step 3: Data Visualization  
4. [Automating the Process](#automating-the-process)  
5. [Troubleshooting](#troubleshooting)  
6. [Expected Constants & Default Values](#expected-constants--default-values)  
7. [Conclusion](#conclusion)  

---

## **📌 Introduction** 🌐📡📊
This project provides a **real-time network monitoring solution** that performs the following key tasks:  

✔ **Discovers devices** on the local network 🔎📡💻  
✔ **Measures network performance** (latency, jitter, throughput, bandwidth, etc.) 📈📉📊  
✔ **Generates visual insights** through graphs 📊📌🔍  

---

## **📌 Installation and Setup** 🛠️📥💾  

### **1️⃣ Install Required Dependencies** 📦🔧💻  
Run the following command to install system dependencies:  
```bash
sudo apt update && sudo apt install iperf3 nmap traceroute python3-pip -y
```

### **2️⃣ Create and Activate a Virtual Environment** 🔄📂🐍  
Navigate to the project directory and create a **Python virtual environment**:  
```bash
cd ~/Network_matric
python3 -m venv venv
source venv/bin/activate
```

### **3️⃣ Install Python Libraries** 📚🐍💡  
Once inside the virtual environment, install required Python packages:  
```bash
pip install pandas numpy matplotlib seaborn scapy
```

---

## **📌 Running the Project** 🚀📊📡  

### **🔹 Step 1: Network Discovery** 🔎🌍📶  
The **network discovery script** scans the network for active devices and logs them into `discovered_devices.csv`.  

#### **✅ Run the script:** 🖥️📌🚀  
```bash
sudo python3 network_discovery.py
```

#### **📌 Expected Output:** 📊✅📡  
```
👉 Detected Network Subnet: 192.168.1.0/24
🔍 Scanning network...
📌 [Discovered Devices]
IP Address       MAC Address          Device Name       Type
================================================================
192.168.1.1      00:1A:2B:3C:4D:5E    Router           Network Device
192.168.1.10     AC:DE:48:00:11:22    Laptop           Personal Computer
192.168.1.15     BC:2E:F3:44:55:66    Smartphone       Mobile Device

✅ Discovery results saved in `discovered_devices.csv`.
```

#### **⚠️ Troubleshooting (If No Devices Are Found):** 🛠️❗🔍  
- Ensure you are **connected to the network**. 📶✅🔄  
- Run the following command to check for active devices manually:  
  ```bash
  sudo nmap -sn 192.168.1.0/24
  ```  

---

### **🔹 Step 2: Network Metrics Collection** 📡📊📋  
The **network metrics script** collects various network statistics, including:  
✔ **Latency (ms)** ⏳📉📡  
✔ **Jitter (ms)** 📉📊⚡  
✔ **Throughput (Mbps)** 📶🚀📊  
✔ **Bandwidth (Mbps)** 🌍📈📡  
✔ **Delay (ms)** 🕒⏳📊  
✔ **Hop Count** 📍🔗🛠️  

#### **✅ Start iPerf3 Server (Before Running Tests)** 🖥️📡⚙️  
In a separate terminal, run:  
```bash
iperf3 -s
```
_(Keep this terminal open while running network tests.)_ 🏗️🔍✅  

#### **✅ Run the network metrics script:** 📡📊✅  
```bash
python3 network_metrics.py
```

#### **📌 Expected Output:** 📡📊💾  
```
👉 Using column `IP` for device discovery.

💠 Running tests for 192.168.1.1...
📊 192.168.1.1 | 🥒 Latency: 5.2 ms | 📉 Jitter: 1.1 ms | ⏳ Delay: 4 ms
💀 Throughput: 100 Mbps | 📶 Bandwidth: 95 Mbps | 🛠️ Hops: 2

📅 All network tests completed.
```

#### **⚠️ If iPerf3 Bandwidth Shows 1 Mbps:** 🚨📉🔧  
- Ensure the **iperf3 server is running** on the **target device**:  
  ```bash
  iperf3 -s
  ```  
- If testing on a **remote machine**, ensure **port 5201** is open. 🌍📶🔓  

---

### **🔹 Step 3: Data Visualization** 📊📡🖥️  
After collecting network metrics, visualize them using **bar graphs**. 📉📊✅  

#### **✅ Run the visualization script:** 📊🖥️🔍  
```bash
python3 network_visualization.py
```

#### **📌 Expected Output:** 📡📊✅  
```
👉 Data loaded successfully.
👉 Saved graph for 192.168.1.1: network_graphs/192_168_1_1.png
👉 Saved graph for 192.168.1.10: network_graphs/192_168_1_10.png

📚 All network graphs generated successfully!
```

📂 **Graph files will be available in `network_graphs/`** 📊📂📌  

---

## **📌 Troubleshooting** 🛠️❗📌  

| **Issue** | **Possible Cause** | **Solution** |
|------------|------------------|--------------|
| ❌ No devices found | Not connected to the network | Run `sudo nmap -sn 192.168.1.0/24` |
| ❌ iPerf3 bandwidth shows 1 Mbps | iPerf3 server not running | Start it with `iperf3 -s` |
| ❌ Old data in visualization | Data not updated | Delete old metrics & rerun: `rm network_metrics.csv` |

---

## **📌 Conclusion** 🎯📊🌍  
This project provides a **real-time network monitoring solution** by **discovering devices, measuring network performance, and generating graphs**. 📈📡📊  

💡 **Now you're ready to monitor your network like a pro!** 🚀✅📶  

---

