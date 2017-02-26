"""defines X10View"""
import json
import os
import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework import permissions

from requests.auth import HTTPBasicAuth


from Base.models import KeyStore


class HomeAssistantView(APIView):
    """defines views for each of the http verbs"""

    @api_view(['GET'])
    @renderer_classes((JSONRenderer,))
    @permission_classes((permissions.AllowAny,))
    def status(self, pk=None):

        url = "http://192.168.2.17:8123/api/states/%s" % pk
        headers = {
            'accept': "application/json",
            'content-type': "text/json",
            'x-ha-access': "esp8266Fun",
            'Accept': "application/json"
        }

        response = requests.request("GET", url, headers=headers)

        message = json.loads(response.text)
        return Response(message)

    @api_view(['PUT'])
    @renderer_classes((JSONRenderer,))
    @permission_classes((permissions.AllowAny,))
    def turn_off(self, device_code=None):
        payload = {"entity_id": device_code}

        url = "http://192.168.2.17:8123/api/services/light/turn_off"
        headers = {
            'accept': "application/json",
            'content-type': "text/json",
            'x-ha-access': "esp8266Fun",
            'Accept': "application/json"
        }

        response = requests.request(
            "POST", url, headers=headers, data=json.dumps(payload))

        message = json.loads(response.text)
        return Response(message)

    @api_view(['PUT'])
    @renderer_classes((JSONRenderer,))
    @permission_classes((permissions.AllowAny,))
    def turn_on(self, device_code, on_level=255):
        payload = {"entity_id": device_code, "brightness": on_level}

        url = "http://192.168.2.17:8123/api/services/light/turn_on"
        headers = {
            'accept': "application/json",
            'content-type': "text/json",
            'x-ha-access': "esp8266Fun",
            'Accept': "application/json"
        }

        response = requests.request(
            "POST", url, headers=headers, data=json.dumps(payload))

        message = json.loads(response.text)
        return Response(message)
