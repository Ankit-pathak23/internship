# views.py

from rest_framework import generics
from django.shortcuts import get_object_or_404
from .models import Device, TemperatureReading, HumidityReading
from .serializer import DeviceSerializer, TemperatureReadingSerializer, HumidityReadingSerializer
from rest_framework.decorators import api_view,permission_classes, authentication_classes
import requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils import timezone
from django.shortcuts import render
from rest_framework import permissions
from django.template import loader
from django.http import HttpResponse
@api_view(['POST', 'GET'])
@permission_classes([])
def manageDevices(request):
    if request.method == 'POST':
        return createDevice(request)
    elif request.method == 'GET':
        return getDevices()

def createDevice(request):
        data=request.data
        print(data)
        try:
            device=Device.objects.create(
                name=data['name'],
            )

            serializer=DeviceSerializer(device)
            return Response(serializer.data)
        except:
            message={'detail':"Devices is not cretaed"}
            return Response(message,status=status.HTTP_400_BAD_REQUEST)
def getDevices():
        try:
            device=Device.objects.all()
            serializer=DeviceSerializer(device,many=True)
            return Response(serializer.data)
        except:
            return Response({"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'DELETE'])
@permission_classes([])
def DeviceDetailOrDeleteView(request,pk):
    if request.method == 'DELETE':
        return deleteTheDevice(pk)
    elif request.method == 'GET':
        return getTheDevice(pk)
def getTheDevice(pk):
        try:
            device = Device.objects.get(uid=pk)
            # You can serialize the device object if needed
            # serializer = YourDeviceSerializer(device)
            # return Response(serializer.data)
            serializer=DeviceSerializer(device)
            return Response(serializer.data)
        except Device.DoesNotExist:
            return Response({"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def deleteTheDevice(pk):
    try:
        device = Device.objects.get(uid=pk)
        device.delete()
        message={"Device deleted successfull"}
        return Response(message,status=status.HTTP_204_NO_CONTENT)
    except Device.DoesNotExist:
        return Response({"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   
@api_view(['GET'])
@permission_classes([])
def ReadingListView(request, device_uid, parameter):
    start_on = request.GET.get('start_on')
    end_on = request.GET.get('end_on')

    try:
        reading_model = TemperatureReading if parameter == 'temperature' else HumidityReading
        reading_serializer = TemperatureReadingSerializer if parameter == 'temperature' else HumidityReadingSerializer

        device = Device.objects.get(uid=device_uid)

        # Convert start_on and end_on to aware datetime objects
        start_on_aware = timezone.make_aware(timezone.datetime.strptime(start_on, '%Y-%m-%dT%H:%M:%S'))
        end_on_aware = timezone.make_aware(timezone.datetime.strptime(end_on, '%Y-%m-%dT%H:%M:%S'))

        queryset = reading_model.objects.filter(device=device, timestamp__range=[start_on_aware, end_on_aware])
        instances = queryset.all()

        serializer = reading_serializer(instances, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class CustomDjangoModelPermissionsOrAnonReadOnly(permissions.DjangoModelPermissionsOrAnonReadOnly):
    def _queryset(self, view):
        queryset = getattr(view, 'queryset', None)

        if queryset is None:
            queryset = getattr(view, 'get_queryset', None)

        if queryset is None:
            raise AssertionError(
                "Cannot apply DjangoModelPermissionsOrAnonReadOnly "
                "on a view that does not set `.queryset` or have a `.get_queryset()` method."
            )

        return queryset()
    
# class DeviceGraphView(APIView):
#     permission_classes = [CustomDjangoModelPermissionsOrAnonReadOnly]
#     # queryset = TemperatureReading.objects.all() # This line defines the queryset
#     def get_queryset(self):
#         return TemperatureReading.objects.all()

#     def get(self, request, *args, **kwargs):
#         device_uid = self.request.query_params.get('device_uid')
        
#         # Filter the queryset based on the device_uid
#         temperature_readings = self.get_queryset().filter(device_uid=device_uid)
#         humidity_readings = HumidityReading.objects.filter(device_uid=device_uid)
#         humidity_readings = HumidityReading.objects.filter(device_uid=device_uid).order_by('timestamp')
        
#         temperature_serializer = TemperatureReadingSerializer(temperature_readings, many=True)
#         humidity_serializer = HumidityReadingSerializer(humidity_readings, many=True)
        
#         temperature_data = temperature_serializer.data
#         humidity_data = humidity_serializer.data

#         return render(request, 'graph/device_graph.html', {'temperature_readings': temperature_data, 'humidity_readings': humidity_data})

def DeviceGraphView(request):
    device_uid=request.GET.get("device_uid")
    # template=loader.get_template('graph/device_graph.html')
    
    try:
        temperatures = TemperatureReading.objects.filter(device=device_uid).order_by('timestamp')
        humidities = HumidityReading.objects.filter(device=device_uid).order_by('timestamp')
        temperature_serializer=TemperatureReadingSerializer(temperatures,many=True)
        humidity_serializer=HumidityReadingSerializer(humidities,many=True)
        temperature_data=temperature_serializer.data
        humidity_data=humidity_serializer.data
        
        # Extract temperatures
        temperatures_dataes = [float(entry['temperature']) for entry in temperature_data]

        # Extract humidities
        humidities_dataes = [float(entry['humidity']) for entry in humidity_data]
        print(temperatures_dataes)
        print(humidities_dataes)
        return render(request,'graph/device_graph.html',{'temperature_readings': temperatures_dataes, 'humidity_readings': humidities_dataes})
                # return HttpResponse(temperature_data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)