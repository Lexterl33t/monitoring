import os
import re
import platform


def get_local_ip_and_mac_address():
    """Function for get local ip and mac address (linux or windows os).

    Returns:
        tuple (str): local ip and mac address.
        none: if the os number is not recognized.
    """
    if platform.system() == "Windows":
        command = os.popen("ipconfig /all").read()
        local_ip = re.search(r"(IPv4 Address)(\D+)(\d{1,3})(\.\d{1,3}){3}", command)
        local_ip = re.search(r"(\d{1,3})(\.\d{1,3}){3}", local_ip.group())
        mac_address = re.search(r"(Physical Address)(\D+)(\w{2})([-]\w{2}){5}", command)
        mac_address = re.search(r"\w{2}([-]\w{2}){5}", mac_address.group())
        return local_ip.group(), mac_address.group()
    elif platform.system() == "Linux":
        command = os.popen("ifconfig").read()
        local_ip = re.search(r"(inet)(\D+)(\d{1,3})(\.\d{1,3}){3}", command)
        local_ip = re.search(r"(\d{1,3})(\.\d{1,3}){3}", local_ip.group())
        mac_address = re.search(r"(ether)(\D+)(\w{2})([:]\w{2}){5}", command)
        mac_address = re.search(r"\w{2}([:]\w{2}){5}", mac_address.group())
        return local_ip.group(), mac_address.group()
    else:
        return
