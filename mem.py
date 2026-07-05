import psutil

ram = psutil.virtual_memory()
total_ram = ram.total / (1024.0**3)
used_ram = ram.used / (1024.0**3)
free_ram = ram.available / (1024.0**3)
ram_usage_percent = ram.percent
print(int(used_ram * 100))
