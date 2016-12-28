"""defines D1Mini ViewSet"""
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response

from WemosController.serializerclasses import UserSerializer
from WemosController.serializerclasses import D1MiniSerializer

from Base.models import D1Mini


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    """User ViewSet may be unusued or may be used in permissions"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


# ViewSets define the view behavior.
class D1MiniViewSet(viewsets.GenericViewSet):
    """defines views for each of the http verbs"""
    # serializer_class = D1MiniSerializer
    queryset = D1Mini.objects.all()
    """Assign queryset for all views"""

    def list(self, request):
        """return a list of all D1Minis"""
        serializer_class = D1MiniSerializer(
            self.queryset,
            many=True,
            context={'request': request})
        return Response(serializer_class.data)

    def create(self, request):
        """Creates a new D1Mini,
            stores it in the db,
            returns the resulting object"""
        data = request.data
        mini = self.get_mini(mac_id=data["mac_id"])
        if not mini:
            mini = D1Mini.create(mac_id=data["mac_id"])
            mini.save()
        serialized_mini = self.get_serialized_mini(
            mac_id=data['mac_id'],
            request=request)
        return Response(serialized_mini)

    def get_mini(self, mac_id=None, pk=None):
        """return a filtered queryset"""
        if mac_id is not None:
            mini = self.queryset.filter(mac_id=mac_id)
        else:
            mini = self.queryset.filter(pk=pk)
        return mini

    def get_serialized_mini(self, request, mac_id=None, pk=None):
        """returns a serialized mini object matching either mac_id or pk"""
        if mac_id is None:
            result = self.queryset.filter(pk=pk)
        else:
            result = self.queryset.filter(mac_id=mac_id)
        serializer_class = D1MiniSerializer(result,
                                            many=True,
                                            context={'request': request})
        return serializer_class.data

    def retrieve(self, request, pk=None):
        """handle get with a pk identifier"""
        mini = get_object_or_404(self.queryset, pk=pk)
        serializer_class = D1MiniSerializer(mini, context={'request': request})
        return Response(serializer_class.data)

    def update(self, request, pk=None):
        """handle put request"""
        data = request.data
        mini = self.get_mini(self, pk=pk)
        if data['has_dht'] is not None:
            mini.has_dht = data['has_dht']
            mini.save()
        return Response(status=200)

    def partial_update(self, request, pk=None):
        """handle patch request"""
        mini = get_object_or_404(self.queryset, pk=pk)
        serializer_class = D1MiniSerializer(mini, context={'request': request})
        return Response(serializer_class.data, status=200)

    def destroy(self, pk=None):
        """handle delete request"""
        mini = self.getmini(self, pk=pk)
        if mini:
            mini.delete()
        return Response(status=200)
