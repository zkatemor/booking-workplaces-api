from django.http import JsonResponse

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

        return JsonResponse({"result": serializer.data})

    def get(self, request):
        workplaces = Workplace.objects.all()
        serializer = [WorkplaceSerializer(i).data for i in workplaces]
        return JsonResponse({"result": serializer})
