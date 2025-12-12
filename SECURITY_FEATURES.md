# Security Features

## OAuth2 Authentication

EventHorizon provides full OAuth2 support for building secure client applications.

### Quick Setup

1. **Create OAuth2 Application** (Admin Panel)
   - Go to `/admin/oauth2_provider/application/`
   - Click "Add Application"
   - Configure client type and grant type
   - Add redirect URIs

2. **Use OAuth2 in Your App**
   ```bash
   # Get authorization code
   GET /o/authorize/?response_type=code&client_id=YOUR_ID&redirect_uri=YOUR_URI
   
   # Exchange for token
   POST /o/token/
   {
     "grant_type": "authorization_code",
     "code": "AUTH_CODE",
     "client_id": "YOUR_ID",
     "client_secret": "YOUR_SECRET"
   }
   
   # Use access token
   GET /api/events/
   Authorization: Bearer ACCESS_TOKEN
   ```

See **OAUTH2_GUIDE.md** for complete documentation with examples for:
- Flutter/Dart
- PHP
- Python
- JavaScript/React Native

## Multi-Factor Authentication (MFA)

TOTP-based two-factor authentication for enhanced account security.

### Quick Setup

1. **Enable MFA**
   ```bash
   POST /api/users/mfa/enable/
   Authorization: Token YOUR_TOKEN
   ```
   
   Response includes QR code to scan with authenticator app.

2. **Confirm Setup**
   ```bash
   POST /api/users/mfa/confirm/
   {
     "token": "123456"
   }
   ```

3. **Verify OTP During Login**
   ```bash
   POST /api/users/mfa/verify/
   {
     "token": "123456"
   }
   ```

### Supported Authenticator Apps

- Google Authenticator
- Microsoft Authenticator
- Authy
- 1Password
- Bitwarden
- Any TOTP-compatible app

### Backup Codes

Generate one-time backup codes for account recovery:

```bash
GET /api/users/mfa/backup_codes/
Authorization: Token YOUR_TOKEN
```

Returns 10 one-time codes. Save securely!

See **MFA_GUIDE.md** for complete documentation with integration examples.

## Security Best Practices

### For API Developers

1. **Use OAuth2** for client applications instead of storing user passwords
2. **Implement token refresh** to maintain sessions
3. **Use HTTPS** in production (OAuth2/MFA require secure connections)
4. **Validate redirect URIs** to prevent authorization code interception
5. **Use PKCE** for mobile apps (public clients)

### For Users

1. **Enable MFA** for important accounts (organizers, admins)
2. **Save backup codes** securely
3. **Use strong passwords** (MFA is second factor, not replacement)
4. **Review authorized apps** regularly in admin panel

### For Organizers

1. **Require MFA** for team members with event management access
2. **Use OAuth2** for custom integrations
3. **Audit access tokens** periodically
4. **Revoke tokens** for unused apps

## API Endpoints Summary

### OAuth2
- `GET /o/authorize/` - Authorization endpoint
- `POST /o/token/` - Token endpoint
- `POST /o/revoke_token/` - Revoke access token
- `GET /o/introspect/` - Token introspection

### MFA
- `GET /api/users/mfa/status/` - Check if MFA enabled
- `POST /api/users/mfa/enable/` - Start MFA setup
- `POST /api/users/mfa/confirm/` - Confirm setup with OTP
- `POST /api/users/mfa/verify/` - Verify OTP code
- `POST /api/users/mfa/disable/` - Disable MFA
- `GET /api/users/mfa/backup_codes/` - Generate backup codes

## Configuration

### OAuth2 Settings (settings.py)

```python
OAUTH2_PROVIDER = {
    'SCOPES': {
        'read': 'Read access',
        'write': 'Write access',
        'events': 'Event management',
        'registrations': 'Registration management',
        'profile': 'Profile access',
    },
    'ACCESS_TOKEN_EXPIRE_SECONDS': 36000,  # 10 hours
    'REFRESH_TOKEN_EXPIRE_SECONDS': 2592000,  # 30 days
}
```

### MFA Settings

MFA uses django-otp with TOTP (Time-based One-Time Password):
- 30-second time windows
- 6-digit codes
- SHA-1 algorithm (standard)
- Compatible with all major authenticator apps

## Common Use Cases

### Mobile App (Flutter)
1. Implement OAuth2 authorization code flow
2. Store tokens securely (flutter_secure_storage)
3. Offer MFA enrollment in app settings
4. Support biometric authentication for token access

### Web Application (PHP/Node.js)
1. Use OAuth2 for user authentication
2. Implement MFA challenge after password verification
3. Store tokens server-side
4. Provide backup code download

### Third-Party Integration
1. Create OAuth2 application in admin
2. Request appropriate scopes
3. Use access tokens for API calls
4. Handle token expiration/refresh

## Troubleshooting

### OAuth2 Issues

**"Invalid redirect URI"**
- Exact match required (including trailing slash)
- Register all redirect URIs in application settings

**"Invalid client"**
- Check client ID and secret
- Ensure application is active

### MFA Issues

**"Invalid token"**
- Check device time synchronization
- Wait for next code (30-second window)
- Try backup codes if authenticator unavailable

**Lost authenticator app**
- Use backup codes to login
- Disable MFA with password
- Re-enable with new device

## Next Steps

1. Read **OAUTH2_GUIDE.md** for OAuth2 implementation
2. Read **MFA_GUIDE.md** for MFA implementation
3. Test OAuth2 flow with Postman or curl
4. Enable MFA for your account
5. Create OAuth2 application for your client
