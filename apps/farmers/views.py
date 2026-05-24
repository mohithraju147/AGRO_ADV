from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Farmer
from .serializers import FarmerSerializer

class FarmerViewSet(viewsets.ModelViewSet):
    queryset         = Farmer.objects.all()
    serializer_class = FarmerSerializer

    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        mobile = request.data.get('mobile', '').strip()
        if not mobile:
            return Response({'success': False, 'error': 'Mobile number is required'}, status=status.HTTP_400_BAD_REQUEST)
        if Farmer.objects.filter(mobile=mobile).exists():
            return Response({'success': False, 'error': 'Mobile number already registered. Please login.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = FarmerSerializer(data=request.data)
        if serializer.is_valid():
            farmer = serializer.save()
            return Response({'success': True, 'message': f'Welcome {farmer.name}! Profile created successfully.', 'farmer': FarmerSerializer(farmer).data, 'farmer_id': farmer.id}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        mobile = request.data.get('mobile', '').strip()
        if not mobile:
            return Response({'success': False, 'error': 'Mobile number is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            farmer = Farmer.objects.get(mobile=mobile)
            return Response({'success': True, 'message': f'Welcome back, {farmer.name}!', 'farmer': FarmerSerializer(farmer).data, 'farmer_id': farmer.id}, status=status.HTTP_200_OK)
        except Farmer.DoesNotExist:
            return Response({'success': False, 'error': 'No profile found with this mobile number. Please register first.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], url_path='profile')
    def profile(self, request):
        mobile = request.query_params.get('mobile', '').strip()
        if not mobile:
            return Response({'success': False, 'error': 'Mobile number is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            farmer = Farmer.objects.get(mobile=mobile)
            return Response({'success': True, 'farmer': FarmerSerializer(farmer).data})
        except Farmer.DoesNotExist:
            return Response({'success': False, 'error': 'Farmer not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'], url_path='check_mobile')
    def check_mobile(self, request):
        mobile = request.data.get('mobile', '').strip()
        exists = Farmer.objects.filter(mobile=mobile).exists()
        return Response({'exists': exists, 'message': 'Mobile registered' if exists else 'Mobile not registered'})

    @action(detail=False, methods=['put', 'patch'], url_path='update_profile')
    def update_profile(self, request):
        mobile = request.data.get('mobile', '').strip()
        if not mobile:
            return Response({'success': False, 'error': 'Mobile number is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            farmer = Farmer.objects.get(mobile=mobile)
            serializer = FarmerSerializer(farmer, data=request.data, partial=(request.method == 'PATCH'))
            if serializer.is_valid():
                serializer.save()
                return Response({'success': True, 'message': 'Profile updated successfully.', 'farmer': serializer.data})
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Farmer.DoesNotExist:
            return Response({'success': False, 'error': 'Farmer not found'}, status=status.HTTP_404_NOT_FOUND)
