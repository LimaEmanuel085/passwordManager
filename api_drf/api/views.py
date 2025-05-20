from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import bcrypt

class HashPasswordView(APIView):
    def post(self, request):
        password = request.data.get('password')
        if not password:
            return Response({'error': 'Password is required'}, status=400)
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return Response({
            'password': password,
            'hashed_password': hashed.decode()
        }, status=201)
    
class VerifyPasswordView(APIView):
    def post(self, request):
        password = request.data.get('password')
        hashed = request.data.get('hashed_password')
        if not password or not hashed:
            return Response({'error': 'Password and hashed password are required'}, status=400)
        valid = bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        return Response({'valid': valid}, status=201)
