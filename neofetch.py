import climage
import platform
import cpuinfo
import os
import tkinter
import psutil
import ctypes
import subprocess
from ctypes import windll

platform_system = platform.system()
platform_release = platform.release()
platform_version = platform.version()

cpu_info = cpuinfo.get_cpu_info()

windll.shcore.SetProcessDpiAwareness(2)
monitor_width = windll.user32.GetSystemMetrics(0)
monitor_height = windll.user32.GetSystemMetrics(1)

computer_uptime = windll.kernel32.GetTickCount64()

gpu_info = subprocess.check_output("wmic path Win32_VideoController get name")
gpu_info = gpu_info.decode()

mobo_info = subprocess.check_output("wmic path win32_baseboard get product")
mobo_info = mobo_info.decode()

def get_memory_info():
    mem = psutil.virtual_memory()
    total_mem = mem.total / (1024 ** 3)
    available_mem = mem.available / (1024 ** 3)
    percentage_mem = (total_mem - available_mem) / total_mem * 100

    return total_mem, available_mem, percentage_mem

total_mem, available_mem, percentage_mem = get_memory_info()

# psutil.disk_partitions brings back a list (sdiskpart) - tells us the mountpoint for each drive we have 
# we want to then have a loop happening whereby it checks the mountpoint from sdiskpart each time, sees if there is a disk drive, calculate the used / total : percent of the drive, then moves forward in the loop to check the next drive
# once its checked all the drives - we want the loop to break

greatwave = os.path.join(os.path.dirname(__file__), 'greatwave.jpg')

output = climage.convert(greatwave, is_unicode = True, width=50,)

split_image = output.split(sep = "\n")
counter = 0

info_text = [ 
         f"\x1b[38;2;74;163;29mRens system info :-)\x1b[0m",
         f"\x1b[38;2;235;171;54mOS:\x1b[0m {platform_system} {platform_release}, {platform_version}",
         f"\x1b[38;2;235;171;54mCPU:\x1b[0m {cpu_info["brand_raw"]}",
         f"\x1b[38;2;235;171;54mArchitecture:\x1b[0m {cpu_info["arch"]}",
         f"\x1b[38;2;235;171;54mGPU:\x1b[0m {gpu_info.rstrip().lstrip("Name").lstrip()}",
         f"\x1b[38;2;235;171;54mMotherboard:\x1b[0m {mobo_info.rstrip().lstrip("Product").lstrip()}",
         f"\x1b[38;2;235;171;54mAvailable Memory:\x1b[0m {available_mem:.2f} / Total Memory: {total_mem:.2f} : {percentage_mem:.2f}%",
         f"\x1b[38;2;235;171;54mDisk info:\x1b[0m')"
]

for disk_part in psutil.disk_partitions():
    used_disk = (psutil.disk_usage(disk_part.mountpoint).used) / 1024 / 1024 / 1024
    total_disk = (psutil.disk_usage(disk_part.mountpoint).total) / 1024 / 1024 / 1024
    percent_disk = (psutil.disk_usage(disk_part.mountpoint).percent)
    info_text.append(f"   {disk_part.mountpoint} {used_disk:.2f} / {total_disk:.2f} : {percent_disk}% ")
    
info_text.append(f"\x1b[38;2;235;171;54mResolution:\x1b[0m {monitor_width} x {monitor_height} ")
info_text.append(f"\x1b[38;2;235;171;54mUptime:\x1b[0m {computer_uptime / 1000 / 60 / 60: .2f} hours")

length_info_text = len(info_text)
length_split_image = len(split_image)

if length_info_text > length_split_image:
    for i in range(length_split_image):
        split_image[i] = split_image[i] + ' ' + info_text[i]
    for f in range(length_split_image, length_info_text):
        split_image.append(info_text[f])
else:
    for i in range(length_info_text):
        split_image[i] = split_image[i] + ' ' + info_text[i]
     
for entry in split_image:
    print(entry)