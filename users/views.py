from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.util import random_hex
import qrcode
import qrcode.image.svg
from io import BytesIO
import base64
from .models import UserProfile
from .serializers import UserProfileSerializer, UserRegistrationSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    """API endpoint for user profiles"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Users can only view their own profile"""
        return UserProfile.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get', 'put', 'patch'])
    def me(self, request):
        """Get or update current user's profile"""
        # Ensure profile exists (should be created by signal, but just in case)
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        if request.method == 'GET':
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        
        elif request.method in ['PUT', 'PATCH']:
            partial = request.method == 'PATCH'
            serializer = self.get_serializer(profile, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class UserRegistrationViewSet(viewsets.GenericViewSet):
    """API endpoint for user registration"""
    serializer_class = UserRegistrationSerializer
    
    def create(self, request):
        """Register a new user"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"message": "User created successfully", "username": user.username},
            status=status.HTTP_201_CREATED
        )


class MFAViewSet(viewsets.GenericViewSet):
    """API endpoint for Multi-Factor Authentication management"""
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def status(self, request):
        """Check if user has MFA enabled"""
        devices = TOTPDevice.objects.filter(user=request.user, confirmed=True)
        return Response({
            'mfa_enabled': devices.exists(),
            'device_count': devices.count()
        })
    
    @action(detail=False, methods=['post'])
    def enable(self, request):
        """Enable MFA and get QR code for authenticator app"""
        # Check if user already has a confirmed device
        existing_device = TOTPDevice.objects.filter(user=request.user, confirmed=True).first()
        if existing_device:
            return Response(
                {'error': 'MFA is already enabled. Disable it first to set up a new device.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Delete any unconfirmed devices
        TOTPDevice.objects.filter(user=request.user, confirmed=False).delete()
        
        # Create new TOTP device
        device = TOTPDevice.objects.create(
            user=request.user,
            name=f'{request.user.username}-totp',
            confirmed=False
        )
        
        # Generate provisioning URI for QR code
        # Format: otpauth://totp/EventHorizon:username?secret=SECRET&issuer=EventHorizon
        url = device.config_url
        
        # Generate QR code as SVG
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        # Convert to base64 PNG
        img = qr.make_image(fill_color="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        qr_code_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        return Response({
            'message': 'Scan this QR code with your authenticator app (Google Authenticator, Microsoft Authenticator, Authy, etc.)',
            'qr_code': f'data:image/png;base64,{qr_code_base64}',
            'secret': device.key,  # Manual entry fallback
            'device_id': device.id,
            'instructions': [
                '1. Open your authenticator app',
                '2. Scan the QR code or enter the secret manually',
                '3. Enter the 6-digit code from your app to confirm',
            ]
        })
    
    @action(detail=False, methods=['post'])
    def confirm(self, request):
        """Confirm MFA setup by verifying OTP code"""
        token = request.data.get('token')
        
        if not token:
            return Response(
                {'error': 'Token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get unconfirmed device
        device = TOTPDevice.objects.filter(
            user=request.user,
            confirmed=False
        ).first()
        
        if not device:
            return Response(
                {'error': 'No pending MFA setup found. Please start the setup process first.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify the token
        if device.verify_token(token):
            device.confirmed = True
            device.save()
            return Response({
                'message': 'MFA enabled successfully! You will now need to enter a code from your authenticator app when logging in.',
                'mfa_enabled': True
            })
        else:
            return Response(
                {'error': 'Invalid token. Please try again.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['post'])
    def verify(self, request):
        """Verify OTP code for login"""
        token = request.data.get('token')
        
        if not token:
            return Response(
                {'error': 'Token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get confirmed device
        device = TOTPDevice.objects.filter(
            user=request.user,
            confirmed=True
        ).first()
        
        if not device:
            return Response(
                {'error': 'MFA is not enabled for this account'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify the token
        if device.verify_token(token):
            return Response({
                'message': 'Token verified successfully',
                'verified': True
            })
        else:
            return Response(
                {'error': 'Invalid token'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['post'])
    def disable(self, request):
        """Disable MFA (requires password confirmation)"""
        password = request.data.get('password')
        
        if not password:
            return Response(
                {'error': 'Password is required to disable MFA'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify password
        if not request.user.check_password(password):
            return Response(
                {'error': 'Invalid password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Delete all TOTP devices for this user
        deleted_count = TOTPDevice.objects.filter(user=request.user).delete()[0]
        
        return Response({
            'message': 'MFA disabled successfully',
            'mfa_enabled': False,
            'devices_removed': deleted_count
        })
    
    @action(detail=False, methods=['get'])
    def backup_codes(self, request):
        """Generate backup codes for account recovery"""
        from django_otp.plugins.otp_static.models import StaticDevice, StaticToken
        
        # Check if MFA is enabled
        totp_device = TOTPDevice.objects.filter(user=request.user, confirmed=True).first()
        if not totp_device:
            return Response(
                {'error': 'MFA must be enabled before generating backup codes'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get or create static device for backup codes
        static_device, created = StaticDevice.objects.get_or_create(
            user=request.user,
            name=f'{request.user.username}-backup'
        )
        
        # Clear existing tokens
        StaticToken.objects.filter(device=static_device).delete()
        
        # Generate 10 backup codes
        backup_codes = []
        for _ in range(10):
            token = StaticToken.random_token()
            StaticToken.objects.create(device=static_device, token=token)
            backup_codes.append(token)
        
        return Response({
            'message': 'Backup codes generated. Save these codes in a safe place!',
            'backup_codes': backup_codes,
            'warning': 'Each code can only be used once. Generate new codes if you run out.'
        })

