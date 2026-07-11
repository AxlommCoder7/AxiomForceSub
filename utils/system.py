#AxiomForceSub --by OwnerAxiom
import psutil
import platform
import time

START_TIME = time.time()


def uptime():

    seconds = int(time.time() - START_TIME)

    hours = seconds // 3600

    minutes = (seconds % 3600) // 60

    seconds = seconds % 60

    return f"{hours}h {minutes}m {seconds}s"


def ram():

    return round(
        psutil.virtual_memory().percent,
        2
    )


def cpu():

    return psutil.cpu_percent()


def system():

    return platform.system()
