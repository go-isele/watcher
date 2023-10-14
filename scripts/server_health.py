import psutil
import json


def get_system_metrics():
    # Get CPU usage
    cpu_usage = psutil.cpu_percent(interval=1)

    # Get memory usage
    memory = psutil.virtual_memory()
    total_memory = memory.total
    used_memory = memory.used

    # Get disk usage
    disk = psutil.disk_usage('/')
    total_disk_space = disk.total
    used_disk_space = disk.used

    # Get network usage
    network = psutil.net_io_counters()
    sent_bytes = network.bytes_sent
    received_bytes = network.bytes_recv

    # Get swap memory usage
    swap = psutil.swap_memory()
    total_swap = swap.total
    used_swap = swap.used

    # Get processes consuming highest resources
    processes = []
    for process in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            process_info = process.as_dict()
            processes.append({
                'pid': process_info['pid'],
                'name': process_info['name'],
                'cpu_percent': process_info['cpu_percent'],
                'memory_percent': process_info['memory_percent']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # Sort processes by CPU usage
    processes.sort(key=lambda x: x['cpu_percent'], reverse=True)

    # Prepare the metrics as a dictionary
    metrics = {
        'cpu_usage_percent': cpu_usage,
        'memory_usage_percent': (used_memory / total_memory) * 100,
        'swap_usage_percent': (used_swap / total_swap) * 100,
        'disk_usage_percent': (used_disk_space / total_disk_space) * 100,
        'network_sent_bytes': sent_bytes,
        'network_received_bytes': received_bytes,
        'top_processes': processes[:5],  # Get top 5 processes consuming CPU

    }

    # Format the percentage and fraction values
    for key, value in metrics.items():
        if isinstance(value, float):
            metrics[key] = "{:.2f}%".format(value)

    return metrics


