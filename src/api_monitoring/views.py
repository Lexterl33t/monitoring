import json
import platform
import psutil
from psutil._common import bytes2human
import datetime
import getdata
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.utils import timezone
from api_monitoring.models import Cpu, Ram, Disks
from django.core.exceptions import ValidationError
import re
from django.db import connection
# Create your views here.

class System_information(View):

    def get(self, request):
        addresses = getdata.get_local_ip_and_mac_address()
        system_data = {
            "os_name": platform.system(),
            "os_version": platform.version(),
            "user": platform.node(),
            "cpu_architecture": platform.machine(),
            "local_ip": addresses[0],
            "mac_address": addresses[1],
            "boot_time": datetime.datetime.fromtimestamp(psutil.boot_time())
        }
        return JsonResponse(system_data)

@method_decorator(csrf_exempt, name='dispatch')
class Cpu_information(View):

    def get(self, request):

        hardware_data = {
            "total_cores": psutil.cpu_count(),
            "physical_cores": psutil.cpu_count(logical=False),
            "max_frequency": psutil.cpu_freq().max,
            "current_frequency": psutil.cpu_freq().current,
            "percent_used": psutil.cpu_percent()
        }
        return JsonResponse(hardware_data)


    def post(self, request):
        if request.content_type != "application/json":
            return JsonResponse({"Error": "Please, use json application."})
        data = json.loads(request.body)
        data.update({"date": timezone.localtime(timezone.now())})
        print(data)
        try:
            Cpu.objects.create(**data)
        except TypeError:
            return JsonResponse({"Error": "Bad argument."}, status=400)
        except ValueError:
            return JsonResponse({"Error": "Bad argument."}, status=400)
        return JsonResponse({"Success": "Create with successful."}, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class Memory_information(View):

    def get(self, request):
        convert_mb = lambda x: round(x / 1024**3, 2)
        ram = psutil.virtual_memory()
        swap = psutil.swap_memory()
        hardware_data = {
            "virtual_memory": {
                "size": convert_mb(ram.total),
                "available": convert_mb(ram.available),
                "used": convert_mb(ram.used),
                "percent_used": ram.percent
                },
            "swap_memory": {
                "size": convert_mb(swap.total),
                "free": convert_mb(swap.free),
                "used": convert_mb(swap.used),
                "percent_used": swap.percent
            }
        }
        return JsonResponse(hardware_data)

    def post(self, request):
        response = verify(Ram(), request)
        return JsonResponse(response[0], status=response[1])

@method_decorator(csrf_exempt, name='dispatch')
class Disk_information(View):
    def get(self, request):
        convert_mb = lambda x: round(x / 1024**3, 2)
        hardware_data = {"disks": []}
        disks = psutil.disk_partitions()
        for disk in disks:
            disk_usage = psutil.disk_usage(disk.mountpoint)
            if convert_mb(disk_usage.total) < 2:
                continue
            disk_data = {
                "path": disk.device,
                "type": disk.fstype,
                "size": convert_mb(disk_usage.total),
                "used": convert_mb(disk_usage.used),
                "free": convert_mb(disk_usage.free),
                "percent_used": disk_usage.percent,
                "disk_total_write": convert_mb(psutil.disk_io_counters().write_bytes)
            }
            hardware_data.get("disks").append(disk_data)
        return JsonResponse(hardware_data)

    def post(self, request):
        response = verify(Disks(), request)
        return JsonResponse(response[0], status=response[1])


def verify(model, request):

    # Deserialize json request
    if request.content_type != "application/json":
        return [{"Error": "Please, use json type."}, 400]
    try:
        data = json.loads(request.body)
    except json.decoder.JSONDecodeError:
        return [{"Error": "Invalid JSON."}, 400]

    data.update({"date": timezone.localtime(timezone.now())})

    # Set attribute of model object
    for key, value in data.items():
        # Verify if they aren't html tag
        if re.search(r"(([<]{1}).+([>]{1})){1}", str(value)) is not None:
            return [{"Error": f"Please, edit value of : {key}."}, 400]
        setattr(model, key, value)
    try:
        model.full_clean()
    except ValidationError as error:
        error_return = [{"Error": "Bad argument. For more information, please visit our documentation."}, 400]
        for key, value in dict(error).items():
            error_return[0].update({key: value[0]})
        return error_return
    model.save()
    return [{"Success": "Create with successful."}, 200]



