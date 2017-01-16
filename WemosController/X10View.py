"""defines X10View"""
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework import permissions

from requests import get
from requests import post


# ViewS ets define the view behavior.
class X10View(APIView):
    """defines views for each of the http verbs"""

    @api_view(['GET'])
    @renderer_classes((JSONRenderer,))
    @permission_classes((permissions.AllowAny,))
    def status(self, pk=None):
        """returns the status"""
        resp = get('http://192.168.2.18:3000/status')
        message = json.loads(resp.text)
        if pk is not None and message["message"] is not None:
            message["message"] = message["message"][int(pk) - 1]
        return Response(message)

    @api_view(['PUT'])
    @renderer_classes((JSONRenderer,))
    @permission_classes((permissions.AllowAny,))
    def turn_on(self, house_code, device_code, dim_level=22):
        """turns on to an optional level"""
        if int(dim_level) < 22:
            payload = {"HouseCode": house_code,
                       "DeviceCode": device_code, "dimValue": dim_level}
            resp = post('http://192.168.2.18:3000/dim', data=payload)
        else:
            payload = {"HouseCode": house_code, "DeviceCode": device_code}
            resp = post('http://192.168.2.18:3000/turnOn', data=payload)
        message = json.loads(resp.text)
        return Response(message)

    @api_view(['PUT'])
    @renderer_classes((JSONRenderer,))
    @permission_classes((permissions.AllowAny,))
    def turn_off(self, house_code, device_code):
        """turns on to an optional level"""
        payload = {"HouseCode": house_code, "DeviceCode": device_code}
        resp = post('http://192.168.2.18:3000/turnOff', data=payload)
        message = json.loads(resp.text)
        return Response(message)

#    def turnOn(self, request):
#        payload = dict(HouseCode='A', DeviceCode='value2')
#        h4 = post('http://192.168.2.18/turnOn:3000', data=payload)
#        return Response(h4.text)
