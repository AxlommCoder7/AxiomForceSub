import os
import platform
import socket
import time
from datetime import timedelta

import psutil

START_TIME = time.time()


# =====================================================
# Platform
# =====================================================

def system():

    return platform.system()


def release():

    return platform.release()


def machine():

    return platform.machine()


def processor():

    cpu = platform.processor()

    if cpu:

        return cpu

    return "Unknown"


def python_version():

    return platform.python_version()


def hostname():

    return socket.gethostname()


# =====================================================
# CPU
# =====================================================

def cpu():

    return psutil.cpu_percent(interval=1)


def cpu_count():

    return psutil.cpu_count()


def cpu_physical():

    return psutil.cpu_count(logical=False)


def cpu_freq():

    try:

        freq = psutil.cpu_freq()

        return round(freq.current, 2)

    except:

        return 0


# =====================================================
# RAM
# =====================================================

def ram():

    return round(
        psutil.virtual_memory().percent,
        2
    )


def ram_total():

    return round(
        psutil.virtual_memory().total / (1024 ** 3),
        2
    )


def ram_used():

    return round(
        psutil.virtual_memory().used / (1024 ** 3),
        2
    )


def ram_free():

    return round(
        psutil.virtual_memory().available / (1024 ** 3),
        2
    )


# =====================================================
# Disk
# =====================================================

def disk():

    return round(
        psutil.disk_usage("/").percent,
        2
    )


def disk_total():

    return round(
        psutil.disk_usage("/").total / (1024 ** 3),
        2
    )


def disk_used():

    return round(
        psutil.disk_usage("/").used / (1024 ** 3),
        2
    )


def disk_free():

    return round(
        psutil.disk_usage("/").free / (1024 ** 3),
        2
    )


# =====================================================
# Network
# =====================================================

def network_sent():

    return round(
        psutil.net_io_counters().bytes_sent / (1024 ** 2),
        2
    )


def network_recv():

    return round(
        psutil.net_io_counters().bytes_recv / (1024 ** 2),
        2
    )


# =====================================================
# Boot
# =====================================================

def boot_time():

    return datetime_from_timestamp(
        psutil.boot_time()
    )


def datetime_from_timestamp(ts):

    return time.strftime(
        "%d-%m-%Y %H:%M:%S",
        time.localtime(ts)
    )


# =====================================================
# Uptime
# =====================================================

def uptime():

    seconds = int(
        time.time() - START_TIME
    )

    return str(
        timedelta(seconds=seconds)
    )


# =====================================================
# Full Report
# =====================================================

def report():

    return f"""
🖥 System : {system()}
📦 Release : {release()}
💻 Machine : {machine()}

🐍 Python : {python_version()}

⚙ CPU : {cpu()} %
⚙ Cores : {cpu_count()}
⚙ Physical : {cpu_physical()}
⚙ Frequency : {cpu_freq()} MHz

🧠 RAM : {ram()} %
🧠 Used : {ram_used()} GB
🧠 Free : {ram_free()} GB
🧠 Total : {ram_total()} GB

💾 Disk : {disk()} %
💾 Used : {disk_used()} GB
💾 Free : {disk_free()} GB
💾 Total : {disk_total()} GB

📤 Upload : {network_sent()} MB
📥 Download : {network_recv()} MB

⏳ Uptime : {uptime()}

🌐 Host : {hostname()}
"""
