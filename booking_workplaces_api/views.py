import dateutil.parser
from django.db.models import Q

from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView

from booking_workplaces_api.auth import BasicAuthentication, IsAuthenticated
from booking_workplaces_api.models import Workplace, BookingWorkplace
from booking_workplaces_api.serializer import WorkplaceSerializer, BookingSerializer


class WorkplaceView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        if not data.get("name"):
            return JsonResponse({"error": "name is required"}, status=422)

        name = data.get("name")

        workplace = Workplace(name=name)
        workplace.save()

        serializer = WorkplaceSerializer(workplace)

        return JsonResponse({"result": serializer.data}, status=201)

    def get(self, request):
        data = request.query_params

        if data.get("datetime_from") or data.get("datetime_to"):
            if not data.get("datetime_from") or not data.get("datetime_to"):
                return JsonResponse({"error": "The time period is not fully indicated."}, status=422)
            else:
                datetime_from = dateutil.parser.parse(data.get("datetime_from"))
                datetime_to = dateutil.parser.parse(data.get("datetime_to"))

                booking = BookingWorkplace.objects.filter(Q(datetime_to__range=(datetime_from, datetime_to)) |
                                                          Q(datetime_from__range=(datetime_from, datetime_to)))

                workplaces = Workplace.objects.exclude(pk__in=set(list(booking.values_list('workplace', flat=True))))
                serializer = [WorkplaceSerializer(i).data for i in workplaces]
                return JsonResponse({"result": serializer}, status=200)
        else:
            workplaces = Workplace.objects.all()
            serializer = [WorkplaceSerializer(i).data for i in workplaces]
            return JsonResponse({"result": serializer})


class WorkplaceIndexView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            workplace = Workplace.objects.get(id=pk)
            serializer = WorkplaceSerializer(workplace)
            return JsonResponse({"result": serializer.data})
        except Workplace.DoesNotExist as e:
            return JsonResponse({"error": "Not found workplace"}, status=404)

    def put(self, request, pk):
        try:
            workplace = Workplace.objects.get(id=pk)

            data = request.data

            if not data.get("name"):
                return JsonResponse({"error": "name is required"}, status=422)

            name = data.get("name")
            workplace.name = name
            workplace.save()

            serializer = WorkplaceSerializer(workplace)
            return JsonResponse({"result": serializer.data}, status=201)
        except Workplace.DoesNotExist as e:
            return JsonResponse({"error": "Not found workplace"}, status=404)

    def delete(self, request, pk):
        try:
            workplace = Workplace.objects.get(id=pk)
            workplace.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Workplace.DoesNotExist as e:
            return JsonResponse({"error": "Not found workplace"}, status=404)


class BookingView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        data = request.data

        if not data.get("description"):
            return JsonResponse({"error": "description is required"}, status=422)

        if not data.get("datetime_from"):
            return JsonResponse({"error": "datetime_from is required"}, status=422)

        if not data.get("datetime_to"):
            return JsonResponse({"error": "datetime_to is required"}, status=422)

        if Workplace.objects.filter(pk=pk).exists():
            description = data.get("description")
            datetime_from = dateutil.parser.parse(data.get("datetime_from"))
            datetime_to = dateutil.parser.parse(data.get("datetime_to"))

            # check if datetime is valid
            if timezone.now() <= datetime_from < datetime_to:
                booking = BookingWorkplace.objects.filter(Q(datetime_to__range=(datetime_from, datetime_to)) |
                                                          Q(datetime_from__range=(datetime_from, datetime_to)))

                workplace_ids = set(list(booking.values_list('workplace', flat=True)))
                # check if workplace is not free
                if pk in workplace_ids:
                    return JsonResponse({"error": "The workplace is occupied at the selected time."}, status=422)
                else:

                    booking = BookingWorkplace(description=description, workplace_id=pk,
                                               datetime_from=datetime_from, datetime_to=datetime_to)
                    booking.save()

                    serializer = BookingSerializer(booking)

                    return JsonResponse({"result": serializer.data}, status=201)
            else:
                return JsonResponse({"error": "Datetime is not valid"}, status=422)
        else:
            return JsonResponse({"error": "Not found workplace"}, status=404)

    def get(self, request, pk):
        if Workplace.objects.filter(pk=pk).exists():
            booking = BookingWorkplace.objects.filter(workplace_id=pk)

            serializer = [BookingSerializer(i).data for i in booking]
            return JsonResponse({"result": serializer}, status=200)
        else:
            return JsonResponse({"error": "Not found workplace"}, status=404)
