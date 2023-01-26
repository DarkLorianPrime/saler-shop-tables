from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import ViewSet

from apps.balance.responses import Messages


class SuccessPayViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.POST.get("balance").isdigit():
            return Response({"error": Messages.BALANCE_NOT_INTEGER})

        request.user.balance += int(request.POST.get("balance"))
        request.user.save()
        return Response({"response": "ok"}, status=HTTP_201_CREATED)


class BalanceViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({"response": request.user.balance})
