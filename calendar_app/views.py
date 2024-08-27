from datetime import datetime, timezone
from rest_framework import status


from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from .models import Event
from .serializers import EventSerializer


class AddEventView(CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        timestamp = self.request.data.get('start_at')
        if timestamp:
            start_at = datetime.fromtimestamp(int(timestamp), tz=timezone.utc)
            serializer.save(start_at=start_at)
        else:
            serializer.save()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'id': response.data['id']}, status=status.HTTP_201_CREATED)


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
        events_to_remove = Event.objects.filter(start_at__gte=start_at, id=id)
        return events_to_remove


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
