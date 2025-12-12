# Multi-Factor Authentication (MFA) Guide

## Overview

EventHorizon supports **Time-based One-Time Password (TOTP)** Multi-Factor Authentication using authenticator apps like:
- Google Authenticator
- Microsoft Authenticator
- Authy
- 1Password
- Bitwarden
- Any TOTP-compatible app

## Why Use MFA?

Multi-Factor Authentication adds an extra layer of security to your account by requiring:
1. **Something you know** (your password)
2. **Something you have** (your phone with the authenticator app)

This means even if someone gets your password, they can't access your account without the second factor.

## Setup Guide

### Step 1: Enable MFA

**API Request:**
```bash
POST /api/users/mfa/enable/
Authorization: Token YOUR_TOKEN
```

**Response:**
```json
{
  "message": "Scan this QR code with your authenticator app",
  "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
  "secret": "JBSWY3DPEHPK3PXP",
  "device_id": 1,
  "instructions": [
    "1. Open your authenticator app",
    "2. Scan the QR code or enter the secret manually",
    "3. Enter the 6-digit code from your app to confirm"
  ]
}
```

### Step 2: Scan QR Code

1. Open your authenticator app (Google Authenticator, Microsoft Authenticator, etc.)
2. Tap "Add Account" or "+" button
3. Choose "Scan QR Code"
4. Scan the QR code from the API response
5. The app will add "EventHorizon (username)" to your accounts

**Alternative: Manual Entry**
If you can't scan the QR code:
1. In your authenticator app, choose "Enter a setup key" or "Manual entry"
2. Enter the `secret` value from the API response
3. Set account name to "EventHorizon"
4. Choose "Time-based" type

### Step 3: Confirm Setup

Get the 6-digit code from your authenticator app and confirm:

**API Request:**
```bash
POST /api/users/mfa/confirm/
Authorization: Token YOUR_TOKEN
Content-Type: application/json

{
  "token": "123456"
}
```

**Response:**
```json
{
  "message": "MFA enabled successfully! You will now need to enter a code from your authenticator app when logging in.",
  "mfa_enabled": true
}
```

## Using MFA

### Check MFA Status

```bash
GET /api/users/mfa/status/
Authorization: Token YOUR_TOKEN
```

**Response:**
```json
{
  "mfa_enabled": true,
  "device_count": 1
}
```

### Verify OTP Code

When logging in or performing sensitive operations:

```bash
POST /api/users/mfa/verify/
Authorization: Token YOUR_TOKEN
Content-Type: application/json

{
  "token": "123456"
}
```

**Response (Success):**
```json
{
  "message": "Token verified successfully",
  "verified": true
}
```

**Response (Failure):**
```json
{
  "error": "Invalid token"
}
```

## Backup Codes

Backup codes allow you to access your account if you lose your phone or authenticator app.

### Generate Backup Codes

```bash
GET /api/users/mfa/backup_codes/
Authorization: Token YOUR_TOKEN
```

**Response:**
```json
{
  "message": "Backup codes generated. Save these codes in a safe place!",
  "backup_codes": [
    "a1b2c3d4",
    "e5f6g7h8",
    "i9j0k1l2",
    "m3n4o5p6",
    "q7r8s9t0",
    "u1v2w3x4",
    "y5z6a7b8",
    "c9d0e1f2",
    "g3h4i5j6",
    "k7l8m9n0"
  ],
  "warning": "Each code can only be used once. Generate new codes if you run out."
}
```

**Important:**
- Save these codes in a secure place (password manager, safe, etc.)
- Each code works only once
- You can use them instead of the authenticator code if needed
- Generate new codes if you run low

## Disable MFA

To disable MFA, you need to provide your password for security:

```bash
POST /api/users/mfa/disable/
Authorization: Token YOUR_TOKEN
Content-Type: application/json

{
  "password": "your_password"
}
```

**Response:**
```json
{
  "message": "MFA disabled successfully",
  "mfa_enabled": false,
  "devices_removed": 1
}
```

## Integration Examples

### Web Application (JavaScript)

```javascript
class MFAManager {
  constructor(apiToken) {
    this.baseUrl = 'http://localhost:8000/api/users/mfa';
    this.headers = {
      'Authorization': `Token ${apiToken}`,
      'Content-Type': 'application/json'
    };
  }

  async enableMFA() {
    const response = await fetch(`${this.baseUrl}/enable/`, {
      method: 'POST',
      headers: this.headers
    });
    
    const data = await response.json();
    
    if (response.ok) {
      // Display QR code
      document.getElementById('qr-code').src = data.qr_code;
      document.getElementById('secret').textContent = data.secret;
      return data;
    }
    
    throw new Error(data.error || 'Failed to enable MFA');
  }

  async confirmMFA(token) {
    const response = await fetch(`${this.baseUrl}/confirm/`, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify({ token })
    });
    
    const data = await response.json();
    
    if (response.ok) {
      alert('MFA enabled successfully!');
      return data;
    }
    
    throw new Error(data.error || 'Invalid token');
  }

  async verifyToken(token) {
    const response = await fetch(`${this.baseUrl}/verify/`, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify({ token })
    });
    
    return response.ok;
  }

  async getBackupCodes() {
    const response = await fetch(`${this.baseUrl}/backup_codes/`, {
      headers: this.headers
    });
    
    const data = await response.json();
    
    if (response.ok) {
      return data.backup_codes;
    }
    
    throw new Error(data.error || 'Failed to generate backup codes');
  }

  async disableMFA(password) {
    const response = await fetch(`${this.baseUrl}/disable/`, {
      method: 'POST',
      headers: this.headers,
      body: JSON.stringify({ password })
    });
    
    const data = await response.json();
    
    if (response.ok) {
      alert('MFA disabled successfully');
      return data;
    }
    
    throw new Error(data.error || 'Failed to disable MFA');
  }
}

// Usage
const mfa = new MFAManager('your-api-token');

// Enable MFA
const setupData = await mfa.enableMFA();
// Show QR code to user

// User scans QR and enters code
const userCode = document.getElementById('otp-input').value;
await mfa.confirmMFA(userCode);

// Later, verify OTP during login
const isValid = await mfa.verifyToken('123456');
```

### Flutter/Dart Example

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class MFAService {
  final String baseUrl = 'http://localhost:8000/api/users/mfa';
  final String token;

  MFAService(this.token);

  Map<String, String> get headers => {
    'Authorization': 'Token $token',
    'Content-Type': 'application/json',
  };

  Future<Map<String, dynamic>> enableMFA() async {
    final response = await http.post(
      Uri.parse('$baseUrl/enable/'),
      headers: headers,
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }

    throw Exception('Failed to enable MFA');
  }

  Future<bool> confirmMFA(String otpCode) async {
    final response = await http.post(
      Uri.parse('$baseUrl/confirm/'),
      headers: headers,
      body: jsonEncode({'token': otpCode}),
    );

    return response.statusCode == 200;
  }

  Future<bool> verifyToken(String otpCode) async {
    final response = await http.post(
      Uri.parse('$baseUrl/verify/'),
      headers: headers,
      body: jsonEncode({'token': otpCode}),
    );

    return response.statusCode == 200;
  }

  Future<List<String>> getBackupCodes() async {
    final response = await http.get(
      Uri.parse('$baseUrl/backup_codes/'),
      headers: headers,
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return List<String>.from(data['backup_codes']);
    }

    throw Exception('Failed to get backup codes');
  }

  Future<bool> disableMFA(String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/disable/'),
      headers: headers,
      body: jsonEncode({'password': password}),
    );

    return response.statusCode == 200;
  }
}

// Usage in a Flutter widget
class MFASetupScreen extends StatefulWidget {
  @override
  _MFASetupScreenState createState() => _MFASetupScreenState();
}

class _MFASetupScreenState extends State<MFASetupScreen> {
  final mfaService = MFAService('your-token');
  String? qrCodeData;
  String? secret;

  Future<void> setupMFA() async {
    try {
      final data = await mfaService.enableMFA();
      setState(() {
        qrCodeData = data['qr_code'];
        secret = data['secret'];
      });
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to setup MFA: $e')),
      );
    }
  }

  Future<void> confirmSetup(String otpCode) async {
    try {
      final success = await mfaService.confirmMFA(otpCode);
      if (success) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('MFA enabled successfully!')),
        );
        Navigator.pop(context);
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Invalid code')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Setup MFA')),
      body: Column(
        children: [
          if (qrCodeData != null)
            Image.memory(
              base64Decode(qrCodeData!.split(',')[1]),
              width: 200,
              height: 200,
            ),
          if (secret != null)
            Text('Secret: $secret'),
          TextField(
            decoration: InputDecoration(labelText: 'Enter 6-digit code'),
            keyboardType: TextInputType.number,
            onSubmitted: confirmSetup,
          ),
          ElevatedButton(
            onPressed: setupMFA,
            child: Text('Start Setup'),
          ),
        ],
      ),
    );
  }
}
```

### PHP Example

```php
<?php

class MFAService {
    private $baseUrl = 'http://localhost:8000/api/users/mfa';
    private $token;

    public function __construct($token) {
        $this->token = $token;
    }

    private function getHeaders() {
        return [
            'Authorization: Token ' . $this->token,
            'Content-Type: application/json'
        ];
    }

    public function enableMFA() {
        $ch = curl_init($this->baseUrl . '/enable/');
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, $this->getHeaders());
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        
        $response = curl_exec($ch);
        curl_close($ch);
        
        return json_decode($response, true);
    }

    public function confirmMFA($token) {
        $ch = curl_init($this->baseUrl . '/confirm/');
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode(['token' => $token]));
        curl_setopt($ch, CURLOPT_HTTPHEADER, $this->getHeaders());
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        
        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        
        return $httpCode === 200;
    }

    public function verifyToken($token) {
        $ch = curl_init($this->baseUrl . '/verify/');
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode(['token' => $token]));
        curl_setopt($ch, CURLOPT_HTTPHEADER, $this->getHeaders());
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        
        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        
        return $httpCode === 200;
    }

    public function getBackupCodes() {
        $ch = curl_init($this->baseUrl . '/backup_codes/');
        curl_setopt($ch, CURLOPT_HTTPHEADER, $this->getHeaders());
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        
        $response = curl_exec($ch);
        curl_close($ch);
        
        $data = json_decode($response, true);
        return $data['backup_codes'] ?? [];
    }

    public function disableMFA($password) {
        $ch = curl_init($this->baseUrl . '/disable/');
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode(['password' => $password]));
        curl_setopt($ch, CURLOPT_HTTPHEADER, $this->getHeaders());
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        
        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        
        return $httpCode === 200;
    }
}

// Usage
$mfa = new MFAService($_SESSION['api_token']);

// Enable MFA
$setupData = $mfa->enableMFA();
echo '<img src="' . $setupData['qr_code'] . '" />';
echo '<p>Secret: ' . $setupData['secret'] . '</p>';

// Confirm with user's code
if (isset($_POST['otp_code'])) {
    if ($mfa->confirmMFA($_POST['otp_code'])) {
        echo 'MFA enabled successfully!';
    } else {
        echo 'Invalid code, please try again';
    }
}

// Later, verify during login
if ($mfa->verifyToken($_POST['login_otp'])) {
    // OTP valid, proceed with login
    $_SESSION['authenticated'] = true;
}
```

## Security Best Practices

1. **Save Backup Codes Securely**
   - Store them in a password manager
   - Print and keep in a safe place
   - Never share them with anyone

2. **Use a Reliable Authenticator App**
   - Google Authenticator
   - Microsoft Authenticator
   - Authy (supports cloud backup)
   - 1Password or Bitwarden (if you use these password managers)

3. **Don't Lose Your Device**
   - Before removing authenticator app, disable MFA first
   - Or make sure you have backup codes

4. **Re-enable MFA After Disabling**
   - You'll get a new QR code and secret
   - The old codes will stop working

5. **Protect Your Password**
   - MFA is only effective if your password is also strong
   - Use a unique password for EventHorizon

## Troubleshooting

### "Invalid token" Error

**Common causes:**
1. **Time sync issue** - Make sure your device's time is accurate
   - Solution: Enable automatic time sync on your device
2. **Wrong code** - 6-digit codes change every 30 seconds
   - Solution: Wait for the next code and try again
3. **Old device** - Using QR code from a previous setup attempt
   - Solution: Start fresh by calling `/enable/` again

### Lost Phone / Authenticator App

**Solutions:**
1. Use one of your backup codes to log in
2. Generate new backup codes after logging in
3. Set up MFA again with a new device

### Can't Scan QR Code

**Solution:**
Use manual entry:
1. Copy the `secret` value from the API response
2. In your authenticator app, choose "Enter a setup key"
3. Paste the secret
4. Choose "Time-based" type

### MFA Not Working After Setup

**Checklist:**
1. Did you confirm the setup? (call `/confirm/` endpoint)
2. Is your device's time synchronized?
3. Are you using the correct account in your authenticator app?
4. Try using a backup code to verify the system is working

## API Reference Summary

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/users/mfa/status/` | GET | Check if MFA is enabled | Yes |
| `/api/users/mfa/enable/` | POST | Start MFA setup, get QR code | Yes |
| `/api/users/mfa/confirm/` | POST | Confirm MFA setup with OTP | Yes |
| `/api/users/mfa/verify/` | POST | Verify OTP code | Yes |
| `/api/users/mfa/disable/` | POST | Disable MFA (requires password) | Yes |
| `/api/users/mfa/backup_codes/` | GET | Generate backup codes | Yes |

## Next Steps

After setting up MFA:
1. Save your backup codes securely
2. Test login with MFA to ensure it works
3. Consider enforcing MFA for all organizers
4. Educate users about the security benefits

For implementation help, see:
- API.md for general API documentation
- OAUTH2_GUIDE.md for OAuth2 integration
- USER_GUIDE.md for user workflows
