from rest_framework import generics, status
from rest_framework.response import Response
from my_app.models import Worker, CheckIn
from .serializers import WorkerSerializer, CheckInSerializer


class WorkerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer


class WorkerRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    lookup_field = "telegram_id"


class CheckInListCreateAPIView(generics.ListCreateAPIView):
    queryset = CheckIn.objects.all()
    serializer_class = CheckInSerializer

    def create(self, request, *args, **kwargs):
        telegram_id = request.data.get("telegram_id")
        try:
            worker = Worker.objects.get(telegram_id=telegram_id)
        except Worker.DoesNotExist:
            return Response({"detail": "Worker not found"}, status=status.HTTP_404_NOT_FOUND)

        video_file = request.FILES.get("video")

        checkin = CheckIn.objects.create(
            worker=worker,
            latitude=request.data.get("latitude"),
            longitude=request.data.get("longitude"),
            location_name=request.data.get("location_name"),
            video=video_file
        )

        serializer = self.get_serializer(checkin)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CheckInRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CheckIn.objects.all()
    serializer_class = CheckInSerializer
    lookup_field = "id"
