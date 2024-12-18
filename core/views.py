from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .zmq_client import send_command

class ExecuteCommandAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            command = request.data  # DRF parses JSON automatically
            response = send_command(command)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"status": "error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
