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


class ZWaveView(APIView):
    """defines views for each of the http verbs"""

    def auth(self, session=None):
        """turns on to an optional level"""
        if session == None:
            session = requests.Session()

        # get creds from database
        keys = KeyStore.objects.all()
        user_key = keys.filter(key_name="ZWaveUser")
        user = user_key[0].key_value
        password_key = keys.filter(key_name="ZWavePass")
        password = password_key[0].key_value
        auth_token = keys.filter(key_name="ZWaveAuthToken")

        if True or len(auth_token) == 0 or auth_token[0].key_value == '':

            url = "http://192.168.2.18/api/tokenauth"
            payload = "{\"username\":\"%s\", \"password\": \"%s\"}" % (
                user, password)
            headers = {
                'accept': "application/json",
                'x-http-method-override': "POST",
                'cache-control': "no-cache",
            }

            response = session.post(url, data=payload, headers=headers)
            auth_token_string = json.loads(
                response.content.decode("utf-8"))['responseObject']
            if len(auth_token) == 0:
                new_token = KeyStore.create(
                    key_name="ZWaveAuthToken", key_value=auth_token_string)
                new_token.save()
            else:
                """this won't happen right now
                we will need it when we have to invalidate old tokens"""
                auth_token[0].key_value = auth_token_string
                auth_token[0].save()
            return (user, password, auth_token[0].key_value)
        else:
            return (user, password, auth_token[0].key_value)

    @api_view(['GET'])
    @renderer_classes((JSONRenderer,))
    @permission_classes((permissions.AllowAny,))
    def statusDirect(self, pk):
        """returns the status"""
        session = requests.Session()
        (user_name, password, auth_token_string) = ZWaveView.auth(self, session)
        session.auth = (user_name, password)

        url = "http://192.168.2.18/api/device/%s/" % pk
        headers = {
            'Authorization': ("Token %s" % auth_token_string),
            'Accept': "application/json"
        }
        session.headers.update(headers)

        response = session.request("GET", url)

        message = json.loads(response.text)
        return Response(message)

    @api_view(['GET'])
    @renderer_classes((JSONRenderer,))
    @permission_classes((permissions.AllowAny,))
    def status(self, pk=None):
        """returns the status"""
        session = requests.Session()
        auth_details = ZWaveView.auth(self, session)
        user_name = auth_details[0]
        password = auth_details[1]

        url = "https://192.168.2.18:3101/getDeviceLevel/%s" % pk
        print(url)

        headers = {
            'Accept': "application/json",
            'Content-Type': "application/json",
            'cache-control': "no-cache",
        }

        session.headers.update(headers)
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth(
            user_name, password), verify=False)

        session.close()

        message = json.loads(response.text)
        return Response(message)

    @api_view(['PUT'])
    @renderer_classes((JSONRenderer,))
    @permission_classes((permissions.AllowAny,))
    def turn_off(self, device_code):
        """turns on to an optional level"""
        session = requests.Session()
        (user_name, password, auth_token_string) = ZWaveView.auth(self, session)
        session.auth = (user_name, password)

        url = "https://192.168.2.18:3101/setDeviceLevel"

        payload = "{\"nodeId\": \"%s\", \"deviceLevel\": \"0\"}" % device_code

        headers = {
            'accept': "application/json",
            'x-http-method-override': "POST",
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "c259a9f5-bb74-fea6-d3c9-a05a6b513e78"
        }

        response = session.post(
            url, data=payload, headers=headers, verify=False)

        message = json.loads(response.text)
        return Response(message)

    @api_view(['PUT'])
    @renderer_classes((JSONRenderer,))
    @permission_classes((permissions.AllowAny,))
    def turn_on(self, device_code, on_level=99):
        """turns on to an optional level"""
        session = requests.Session()
        (user_name, password, auth_token_string) = ZWaveView.auth(self, session)
        session.auth = (user_name, password)

        url = "https://192.168.2.18:3101/setDeviceLevel"

        payload = "{\"nodeId\": \"%s\", \"deviceLevel\": \"%d\"}" % (
            device_code, int(on_level))

        headers = {
            'accept': "application/json",
            'content-type': "application/json",
            'cache-control': "no-cache",
            'postman-token': "c259a9f5-bb74-fea6-d3c9-a05a6b513e78"
        }

        response = session.post(
            url, data=payload, headers=headers, verify=False)

        message = json.loads(response.text)

        if message["message"] == 'Failed':
            return Response(status=500)
        else:
            return Response(message)
