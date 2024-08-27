from datetime import datetime, timezone
from rest_framework import status, serializers
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Event
from .serializers import EventSerializer





class AddEventView(CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        start_at = self.request.data.get('start_at')
        if start_at:
            try:
                # Пытаемся разобрать дату в формате ISO 8601
                start_at = datetime.fromisoformat(start_at.replace("Z", "+00:00"))
            except ValueError:
                # Если формат неправильный, возвращаем ошибку
                start_at = None

        if not start_at:
            # Если start_at не был корректно разобран, возвращаем ошибку
            raise serializers.ValidationError({"start_at": "Неправильный формат даты"})

        serializer.save(start_at=start_at)


class RemoveEventView(DestroyAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        id = self.kwargs.get('id')
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')

        if not id or not year or not month or not day:
            return Event.objects.none() 

        start_at = datetime(year=int(year), month=int(month), day=int(day), tzinfo=timezone.utc)
        return Event.objects.filter(start_at=start_at, id=id)


class RemoveNextEventsView(DestroyAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        id = self.kwargs.get('id')
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')

        if not id or not year or not month or not day:
            return Event.objects.none() 

        start_at = datetime(year=int(year), month=int(month), day=int(day), tzinfo=timezone.utc)
        return Event.objects.filter(start_at__gte=start_at, id=id)


class UpdateEventView(UpdateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        id = self.kwargs.get('id')
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')

        if not id or not year or not month or not day:
            return Event.objects.none()

        start_at = datetime(year=int(year), month=int(month), day=int(day), tzinfo=timezone.utc)
        return Event.objects.filter(start_at=start_at, id=id)


class EventsByDateView(ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')

        if not year or not month or not day:
            return Event.objects.none() 

        start_at = datetime(year=int(year), month=int(month), day=int(day), tzinfo=timezone.utc)
        return Event.objects.filter(start_at__date=start_at.date())