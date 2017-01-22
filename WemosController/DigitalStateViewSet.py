"""defines D1Mini ViewSet"""
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from WemosController.serializerclasses import DigitalStateSerializer
from WemosController.serializerclasses import D1MiniCommandSerializer
from Base.models import D1Mini, DigitalState


# ViewSets define the view behavior.
class DigitalStateViewSet(viewsets.GenericViewSet):
    """defines views for each of the http verbs"""
    queryset = DigitalState.objects.all()
    """Assign queryset for all views"""

    def list(self, request):
        """return a list of DigitalStates"""

        if 'device' in request.query_params:
            miniset = D1Mini.objects.all()
            miniset = miniset.filter(id=request.query_params['device'])
            if len(miniset) != 1:
                return Response(status=status.HTTP_204_NO_CONTENT)
            queryset = self.queryset.filter(device=miniset[0])
        else:
            queryset = self.queryset
        serializer_class = DigitalStateSerializer(
            queryset,
            many=True,
            context={'request': request})
        return Response(serializer_class.data)


    def retrieve(self, request):
        pk=None
        pin_id=None
        """handle get with a pk identifier"""
        miniset = D1Mini.objects.all().filter(pk=pk)
        stateset = DigitalState.objects.all()
        state = get_object_or_404(stateset, device=miniset[0], pin_id=pin_id)
        serializer_class = DigitalStateSerializer(state, context={'request': request})
        return Response(serializer_class.data)
