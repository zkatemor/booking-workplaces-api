from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView

from booking_workplaces_api.auth import BasicAuthentication, IsAuthenticated
from booking_workplaces_api.models import Workplace
from booking_workplaces_api.serializer import WorkplaceSerializer


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
            workplace.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Workplace.DoesNotExist as e:
            return JsonResponse({"error": "Not found workplace"}, status=404)
