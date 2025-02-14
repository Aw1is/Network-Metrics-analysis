import os
import pandas as pd
import matplotlib.pyplot as plt

METRICS_RESULTS = "network_metrics.csv"
OUTPUT_FOLDER = "network_graphs"

# ✅ Ensure output folder exists
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# ✅ Load latest CSV data
try:
    data = pd.read_csv(METRICS_RESULTS)
    data.fillna(0, inplace=True)  # ✅ Fill missing values
    print("✅ Data loaded successfully.")
except Exception as e:
    print(f"❌ Error loading CSV: {e}")
    exit()

# ✅ Convert timestamp dynamically (fixing your error)
data["Timestamp"] = pd.to_datetime(data["Timestamp"], format="mixed", errors="coerce")

# ✅ Generate graphs for each device
for ip in data["IP"].unique():
    device_data = data[data["IP"] == ip]

    plt.figure(figsize=(12, 6))

    # ✅ Multiple metrics in one graph with better visuals
    plt.plot(device_data["Timestamp"], device_data["Latency (ms)"], marker="o", linestyle="-", label="Latency (ms)", color="b")
    plt.plot(device_data["Timestamp"], device_data["Jitter (ms)"], marker="s", linestyle="--", label="Jitter (ms)", color="g")
    plt.plot(device_data["Timestamp"], device_data["Throughput (Mbps)"], marker="D", linestyle=":", label="Throughput (Mbps)", color="r")
    plt.plot(device_data["Timestamp"], device_data["Bandwidth (Mbps)"], marker="x", linestyle="-.", label="Bandwidth (Mbps)", color="m")

    plt.xlabel("Timestamp", fontsize=12)
    plt.ylabel("Metrics", fontsize=12)
    plt.title(f"Network Metrics for {ip}", fontsize=14, fontweight="bold")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True, linestyle="--", linewidth=0.5)

    # ✅ Save graph
    graph_file = f"{OUTPUT_FOLDER}/{ip.replace('.', '_')}.png"
    plt.savefig(graph_file, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"✅ Saved graph for {ip}: {graph_file}")

print("\n🎉 All network graphs generated successfully! Check the `network_graphs` folder.")

