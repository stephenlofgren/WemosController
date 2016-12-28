"""defines D1Mini ViewSet"""
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from WemosController.serializerclasses import D1MiniEventSerializer
from Base.models import D1MiniCommand, D1Mini


# ViewSets define the view behavior.
class D1MiniEventViewSet(viewsets.GenericViewSet):
    """defines views for each of the http verbs"""
    queryset = D1MiniCommand.objects.all()
    """Assign queryset for all views"""

    def list(self, request):
        """return a list of all D1Minis"""

        if request.query_params['device'] is not None:
            miniset = D1Mini.objects.all()
            miniset = miniset.filter(pk=request.query_params['device'])
            if len(miniset) == 1:
                mini = miniset[0]
                self.queryset = mini.d1minicommand_set
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)

        if request.query_params['acknowledged'] is not None:
            self.queryset = self.queryset.filter(
                acknowledged=bool(request.query_params['acknowledged']))
        serializer_class = D1MiniEventSerializer(
            self.queryset,
            many=True,
            context={'request': request})
        return Response(serializer_class.data)

    def create(self, request):
        """Creates a new D1MiniCommand,
            stores it in the db,
            returns the resulting object"""
        data = request.data

        # lookup the mini by url or pk
        miniset = D1Mini.objects.all()
        mini = miniset.filter(pk=data['device'])

        if len(mini) != 1:
            return Response(data="no device found for id {0}".format(data['device']),
                            status=status.HTTP_400_BAD_REQUEST)

        mini_command = self.save_mini_command(mini[0], data['pin_id'], data[
            'pin_mode'], data['pin_level'], data['acknowledged'])
        serializer_class = D1MiniEventSerializer(
            mini_command,
            many=False,
            context={'request': request})
        return Response(serializer_class.data)

    @staticmethod
    def save_mini_command(device, pin_id, pin_mode, pin_level, acknowledged):
        """create a new D1Mini object and save it to the db"""

        mini = D1MiniCommand.create(device=device,
                                    pin_id=pin_id,
                                    pin_mode=pin_mode,
                                    pin_level=pin_level,
                                    acknowledged=acknowledged)
        mini.save()
        return mini

    def retrieve(self, request, pk=None):
        """handle get with a pk identifier"""
        mini = get_object_or_404(self.queryset, pk=pk)
        serializer_class = D1MiniEventSerializer(mini, context={'request': request})
        return Response(serializer_class.data)

    def update(self, request, pk=None):
        """handle put request"""
        data = request.data
        mini = get_object_or_404(self.queryset, pk=pk)
        if mini is not None:
            if data['acknowledged'] is not None:
                mini.acknowledged = bool(data['acknowledged'])
                mini.save()
        serializer_class = D1MiniEventSerializer(
            mini, context={'request': request})
        return Response(serializer_class.data)
