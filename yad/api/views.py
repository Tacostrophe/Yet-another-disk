from datetime import datetime, timedelta

from .models import Item
from . import serializers
from rest_framework import generics, status
from rest_framework.serializers import ValidationError


class ImportsView(generics.CreateAPIView):
    '''Импортирует элементы файловой системы.'''
    queryset = Item.objects.all()
    serializer_class = serializers.ImportsSerializer

    def create(self, request, *args, **kwargs):
        date = request.data.get('updateDate')
        for item in request.data['items']:
            item['date'] = date
        response = super().create(request, *args, **kwargs)
        response.status_code = status.HTTP_200_OK
        return response


class DeleteView(generics.DestroyAPIView):
    '''Удалить элемент по идентификатору.'''
    queryset = Item.objects.all()
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        date = request.query_params.get('date')
        if date is None:
            raise ValidationError('date parameter is required')
        response = super().destroy(request, *args, **kwargs)
        response.status_code = status.HTTP_200_OK
        return response


class NodesView(generics.RetrieveAPIView):
    '''Получить информацию об элементе по идентификатору.'''
    queryset = Item.objects.all()
    serializer_class = serializers.NodesSerializer
    lookup_field = 'id'


class UpdatesView(generics.ListAPIView):
    '''Получение списка файлов, которые были обновлены
       за последние 24 часа включительно [date - 24h, date]
       от времени переданном в запросе.'''
    serializer_class = serializers.ItemRepresentSerializer

    def get_queryset(self):
        date = self.request.query_params.get('date')
        if date is None:
            raise ValidationError('date parameter is required')
        date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
        queryset = Item.objects.filter(
            date__lte=date,
            date__gte=date - timedelta(hours=24)
        )
        return queryset
