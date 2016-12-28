"""defines D1Mini ViewSet"""
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import list_route
from WemosController.serializerclasses import D1MiniReadingSerializer
from Base.models import D1MiniReading, D1Mini


# ViewSets define the view behavior.
class D1MiniReadingViewSet(viewsets.GenericViewSet):
    """defines views for each of the http verbs"""
    queryset = D1MiniReading.objects.all()
    """Assign queryset for all views"""

    def list(self, request):
        """return a list of all Readings"""

        if request.query_params['device'] is not None:
            miniset = D1Mini.objects.all()
            miniset = miniset.filter(pk=request.query_params['device'])
            if len(miniset) == 1:
                mini = miniset[0]
                self.queryset = mini.d1minireading_set
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)

        serializer_class = D1MiniReadingSerializer(
            self.queryset,
            many=True,
            context={'request': request})
        return Response(serializer_class.data)

    @list_route()
    def humidity(self, request):
        """return a list of all Readings"""

        if request.query_params['device'] is not None:
            miniset = D1Mini.objects.all()
            miniset = miniset.filter(pk=request.query_params['device'])
            if len(miniset) == 1:
                mini = miniset[0]
                self.queryset = mini.d1minireading_set.humidity_readings_for_mini(
                    mini)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)

        serializer_class = D1MiniReadingSerializer(
            self.queryset,
            many=True,
            context={'request': request})
        return Response(serializer_class.data)

    @list_route()
    def temperature(self, request):
        """return a list of all Readings"""

        if request.query_params['device'] is not None:
            miniset = D1Mini.objects.all()
            miniset = miniset.filter(pk=request.query_params['device'])
            if len(miniset) == 1:
                mini = miniset[0]
                if request.query_params['reading_unit'] is not None:
                    self.queryset = mini.d1minireading_set.temp_readings_for_mini(
                        mini, request.query_params['reading_unit'])
                else:
                    self.queryset = mini.d1minireading_set.temp_readings_for_mini(
                        mini, 2)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)

        serializer_class = D1MiniReadingSerializer(
            self.queryset,
            many=True,
            context={'request': request})
        return Response(serializer_class.data)

    @list_route()
    def felt_air(self, request):
        """return a list of all Readings"""

        if request.query_params['device'] is not None:
            miniset = D1Mini.objects.all()
            miniset = miniset.filter(pk=request.query_params['device'])
            if len(miniset) == 1:
                mini = miniset[0]
                if request.query_params['reading_unit'] is not None:
                    self.queryset = mini.d1minireading_set.temp_readings_for_mini(
                        mini, request.query_params['reading_unit'])
                else:
                    self.queryset = mini.d1minireading_set.temp_readings_for_mini(
                        mini, 2)
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)

        serializer_class = D1MiniReadingSerializer(
            self.queryset,
            many=True,
            context={'request': request})
        return Response(serializer_class.data)

    def create(self, request):
        """Creates a new D1MiniReading,
            stores it in the db,
            returns the resulting object"""
        data = request.data

        # lookup the mini by url or pk
        miniset = D1Mini.objects.all()

        new_objects = []
        if isinstance(data, list):
            for d in data:
                mini = miniset.filter(pk=d['device'])

                if len(mini) != 1:
                    return Response(data="no device found for id {0}".format(data['device']),
                                    status=status.HTTP_400_BAD_REQUEST)

                mini_reading = self.save_mini_reading(mini[0], d['reading_type'], d[
                    'reading_value'], d['reading_unit'])
                new_objects.append(mini_reading)
        else:
            mini = miniset.filter(pk=data['device'])

            if len(mini) != 1:
                return Response(data="no device found for id {0}".format(data['device']),
                                status=status.HTTP_400_BAD_REQUEST)

            mini_reading = self.save_mini_reading(mini[0], data['reading_type'], data[
                'reading_value'], data['reading_unit'])
            new_objects.append(mini_reading)

        serializer_class = D1MiniReadingSerializer(
            new_objects,
            many=len(new_objects) > 1,
            context={'request': request})
        return Response(serializer_class.data)

    @staticmethod
    def save_mini_reading(device, reading_type, reading_value, reading_unit):
        """create a new D1Mini object and save it to the db"""

        # it is only valid to have type=0,unit=0; type=1, unit in (1,2),
        # type=2,unit in (3,4)
        if reading_type == 0 and reading_unit != 0:
            raise ValueError(
                '''A reading_type of Humidity is only valid with a reading_unit
                 of percent''')
        elif reading_type == 1 and reading_unit not in (1, 2):
            raise ValueError(
                '''A reading_type of Temperature is only valid with a reading_unit
                 of Fahrenheit or Celcius''')
        elif reading_type == 2 and reading_unit not in (3, 4):
            raise ValueError(
                '''A reading_type of Heat Index is only valid with a reading_unit
                 of Felt Air F or Felt Air C''')
        mini_reading = D1MiniReading.create(device=device,
                                            reading_type=reading_type,
                                            reading_value=reading_value,
                                            reading_unit=reading_unit)
        mini_reading.save()
        return mini_reading

    def retrieve(self, request, pk=None):
        """handle get with a pk identifier"""
        mini = get_object_or_404(self.queryset, pk=pk)
        serializer_class = D1MiniReadingSerializer(
            mini, context={'request': request})
        return Response(serializer_class.data)
