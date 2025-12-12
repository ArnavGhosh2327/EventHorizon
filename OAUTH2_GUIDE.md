# OAuth2 Integration Guide

## Overview

EventHorizon supports OAuth2 authentication, allowing you to build client applications in any language (Flutter/Dart, PHP, React Native, etc.) that can securely access the API on behalf of users.

## What is OAuth2?

OAuth2 is an industry-standard authorization framework that allows third-party applications to access user data without exposing passwords. This is perfect for:

- **Mobile apps** (Flutter, React Native, Swift, Kotlin)
- **Web applications** (PHP, Node.js, Python, Ruby)
- **Desktop applications** (Electron, Qt, Java)
- **Third-party integrations**

## Quick Start

### 1. Create an OAuth2 Application

**Via Admin Panel:**
1. Log in to http://localhost:8000/admin/
2. Go to **Django OAuth Toolkit → Applications**
3. Click **Add Application**
4. Fill in the details:
   - **Name**: Your app name (e.g., "EventHorizon Flutter App")
   - **Client type**: 
     - Choose **Confidential** for server-side apps (PHP, Node.js backends)
     - Choose **Public** for mobile/desktop apps (Flutter, React Native)
   - **Authorization grant type**: Choose based on your use case:
     - **Authorization code** - Most secure, recommended for most apps
     - **Implicit** - For browser-based SPAs (less secure)
     - **Resource owner password-based** - For trusted first-party apps only
     - **Client credentials** - For server-to-server communication
   - **Redirect URIs**: Your app's callback URL (one per line)
     - For mobile apps: `myapp://oauth/callback`
     - For web apps: `https://yourapp.com/oauth/callback`
     - For local dev: `http://localhost:3000/callback`
   - **Scopes**: Select the permissions your app needs

5. Click **Save**
6. Copy the **Client ID** and **Client Secret** (for confidential apps)

### 2. OAuth2 Endpoints

EventHorizon provides these OAuth2 endpoints:

- **Authorization**: `http://localhost:8000/o/authorize/`
- **Token**: `http://localhost:8000/o/token/`
- **Revoke Token**: `http://localhost:8000/o/revoke_token/`
- **Introspect Token**: `http://localhost:8000/o/introspect/`

## Available Scopes

| Scope | Description |
|-------|-------------|
| `read` | Read access to public events and data |
| `write` | Create and update events |
| `events` | Full access to event management |
| `registrations` | Manage event registrations |
| `profile` | Access user profile information |

## Integration Examples

### Flutter/Dart Example

Using the `oauth2` package:

```dart
import 'package:oauth2/oauth2.dart' as oauth2;

// Configuration
const authorizationEndpoint = Uri.parse('http://localhost:8000/o/authorize/');
const tokenEndpoint = Uri.parse('http://localhost:8000/o/token/');
const clientId = 'YOUR_CLIENT_ID';
const redirectUrl = Uri.parse('myapp://oauth/callback');

// Authorization Code Flow
Future<oauth2.Client> authenticate() async {
  var grant = oauth2.AuthorizationCodeGrant(
    clientId,
    authorizationEndpoint,
    tokenEndpoint,
  );

  // Get the authorization URL
  var authorizationUrl = grant.getAuthorizationUrl(
    redirectUrl,
    scopes: ['read', 'write', 'events', 'registrations'],
  );

  // Redirect user to authorizationUrl
  // After user authorizes, extract code from callback
  
  // Exchange code for token
  var client = await grant.handleAuthorizationResponse(queryParameters);
  
  return client;
}

// Use the client to make API requests
Future<void> fetchEvents(oauth2.Client client) async {
  var response = await client.get(
    Uri.parse('http://localhost:8000/api/events/')
  );
  
  if (response.statusCode == 200) {
    var events = jsonDecode(response.body);
    print('Events: $events');
  }
}

// Create an event
Future<void> createEvent(oauth2.Client client) async {
  var response = await client.post(
    Uri.parse('http://localhost:8000/api/events/'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({
      'title': 'Flutter Meetup',
      'slug': 'flutter-meetup',
      'description': 'Join us for Flutter development!',
      'start_datetime': '2025-07-01T18:00:00Z',
      'end_datetime': '2025-07-01T21:00:00Z',
      'status': 'published',
    }),
  );
  
  if (response.statusCode == 201) {
    print('Event created!');
  }
}
```

### PHP Example

Using `league/oauth2-client`:

```php
<?php
require 'vendor/autoload.php';

use League\OAuth2\Client\Provider\GenericProvider;

$provider = new GenericProvider([
    'clientId'                => 'YOUR_CLIENT_ID',
    'clientSecret'            => 'YOUR_CLIENT_SECRET',
    'redirectUri'             => 'https://yourapp.com/callback',
    'urlAuthorize'            => 'http://localhost:8000/o/authorize/',
    'urlAccessToken'          => 'http://localhost:8000/o/token/',
    'urlResourceOwnerDetails' => 'http://localhost:8000/api/users/profiles/me/',
    'scopes'                  => 'read write events registrations'
]);

// Step 1: Get authorization URL
if (!isset($_GET['code'])) {
    $authorizationUrl = $provider->getAuthorizationUrl();
    $_SESSION['oauth2state'] = $provider->getState();
    header('Location: ' . $authorizationUrl);
    exit;
}

// Step 2: Get access token
elseif (empty($_GET['state']) || ($_GET['state'] !== $_SESSION['oauth2state'])) {
    unset($_SESSION['oauth2state']);
    exit('Invalid state');
} else {
    try {
        $accessToken = $provider->getAccessToken('authorization_code', [
            'code' => $_GET['code']
        ]);

        // Use the token to make API requests
        $request = $provider->getAuthenticatedRequest(
            'GET',
            'http://localhost:8000/api/events/',
            $accessToken
        );
        
        $response = $provider->getParsedResponse($request);
        print_r($response);
        
        // Create an event
        $request = $provider->getAuthenticatedRequest(
            'POST',
            'http://localhost:8000/api/events/',
            $accessToken,
            [
                'body' => json_encode([
                    'title' => 'PHP Workshop',
                    'slug' => 'php-workshop',
                    'description' => 'Learn modern PHP',
                    'start_datetime' => '2025-07-15T14:00:00Z',
                    'end_datetime' => '2025-07-15T17:00:00Z',
                    'status' => 'published',
                ])
            ]
        );
        
    } catch (\League\OAuth2\Client\Provider\Exception\IdentityProviderException $e) {
        exit($e->getMessage());
    }
}
```

### React Native / JavaScript Example

Using `react-native-app-auth`:

```javascript
import { authorize } from 'react-native-app-auth';

const config = {
  clientId: 'YOUR_CLIENT_ID',
  redirectUrl: 'myapp://oauth/callback',
  scopes: ['read', 'write', 'events', 'registrations'],
  serviceConfiguration: {
    authorizationEndpoint: 'http://localhost:8000/o/authorize/',
    tokenEndpoint: 'http://localhost:8000/o/token/',
    revocationEndpoint: 'http://localhost:8000/o/revoke_token/',
  },
};

// Authenticate
async function login() {
  try {
    const result = await authorize(config);
    const { accessToken, refreshToken, accessTokenExpirationDate } = result;
    
    // Store tokens securely
    await SecureStore.setItemAsync('accessToken', accessToken);
    
    return accessToken;
  } catch (error) {
    console.error('Authentication failed', error);
  }
}

// Use token to fetch events
async function fetchEvents(accessToken) {
  const response = await fetch('http://localhost:8000/api/events/', {
    headers: {
      'Authorization': `Bearer ${accessToken}`,
    },
  });
  
  const events = await response.json();
  return events;
}

// Create event
async function createEvent(accessToken, eventData) {
  const response = await fetch('http://localhost:8000/api/events/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(eventData),
  });
  
  return await response.json();
}
```

### Python Example

Using `requests-oauthlib`:

```python
from requests_oauthlib import OAuth2Session

client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
redirect_uri = 'http://localhost:8080/callback'

authorization_base_url = 'http://localhost:8000/o/authorize/'
token_url = 'http://localhost:8000/o/token/'

# Step 1: Get authorization URL
oauth = OAuth2Session(
    client_id, 
    redirect_uri=redirect_uri,
    scope=['read', 'write', 'events', 'registrations']
)
authorization_url, state = oauth.authorization_url(authorization_base_url)

print(f'Please go to {authorization_url} and authorize access.')

# Step 2: Get access token
authorization_response = input('Enter the full callback URL: ')
token = oauth.fetch_token(
    token_url,
    authorization_response=authorization_response,
    client_secret=client_secret
)

# Step 3: Use token to make requests
events = oauth.get('http://localhost:8000/api/events/')
print(events.json())

# Create event
new_event = oauth.post(
    'http://localhost:8000/api/events/',
    json={
        'title': 'Python Workshop',
        'slug': 'python-workshop',
        'description': 'Learn Python best practices',
        'start_datetime': '2025-08-01T10:00:00Z',
        'end_datetime': '2025-08-01T13:00:00Z',
        'status': 'published',
    }
)
print(new_event.json())
```

## Authorization Grant Types

### 1. Authorization Code (Recommended)

**Best for:** Server-side web apps, mobile apps

**Flow:**
1. App redirects user to `/o/authorize/`
2. User logs in and authorizes
3. User redirected back with authorization code
4. App exchanges code for access token at `/o/token/`
5. App uses access token to access API

**Security:** Most secure, tokens not exposed to browser

### 2. Implicit Grant

**Best for:** Browser-based SPAs (less secure than Authorization Code)

**Flow:**
1. App redirects user to `/o/authorize/`
2. User logs in and authorizes
3. Access token returned directly in URL fragment

**Security:** Less secure, tokens exposed in browser

### 3. Resource Owner Password Credentials

**Best for:** First-party trusted apps only

**Flow:**
1. App collects username/password directly
2. App sends credentials to `/o/token/`
3. Receives access token

**Security:** Only use for your own apps, not third-party

### 4. Client Credentials

**Best for:** Server-to-server, machine-to-machine

**Flow:**
1. App sends client ID and secret to `/o/token/`
2. Receives access token

**Security:** No user involved, app-level access only

## Testing OAuth2 Flow

### Using curl

**1. Get authorization code (paste URL in browser):**
```bash
http://localhost:8000/o/authorize/?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost:8080/callback&scope=read%20write%20events
```

**2. Exchange code for token:**
```bash
curl -X POST http://localhost:8000/o/token/ \
  -d "grant_type=authorization_code" \
  -d "code=AUTHORIZATION_CODE" \
  -d "redirect_uri=http://localhost:8080/callback" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET"
```

Response:
```json
{
  "access_token": "abc123...",
  "token_type": "Bearer",
  "expires_in": 36000,
  "refresh_token": "xyz789...",
  "scope": "read write events"
}
```

**3. Use access token:**
```bash
curl -H "Authorization: Bearer abc123..." \
  http://localhost:8000/api/events/
```

**4. Refresh token:**
```bash
curl -X POST http://localhost:8000/o/token/ \
  -d "grant_type=refresh_token" \
  -d "refresh_token=xyz789..." \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET"
```

## Mobile App Deep Linking

For mobile apps, configure custom URL schemes:

**Flutter (iOS - Info.plist):**
```xml
<key>CFBundleURLTypes</key>
<array>
  <dict>
    <key>CFBundleURLSchemes</key>
    <array>
      <string>eventhorizon</string>
    </array>
  </dict>
</array>
```

**Flutter (Android - AndroidManifest.xml):**
```xml
<intent-filter>
  <action android:name="android.intent.action.VIEW" />
  <category android:name="android.intent.category.DEFAULT" />
  <category android:name="android.intent.category.BROWSABLE" />
  <data
    android:scheme="eventhorizon"
    android:host="oauth" />
</intent-filter>
```

Then use redirect URI: `eventhorizon://oauth/callback`

## Security Best Practices

1. **Store tokens securely**
   - Mobile: Use secure storage (Keychain on iOS, Keystore on Android)
   - Web: Use HttpOnly cookies or secure session storage
   - Never store in localStorage or plain cookies

2. **Use HTTPS in production**
   - Always use HTTPS for authorization and token endpoints
   - Only use HTTP for local development

3. **Validate redirect URIs**
   - Register exact redirect URIs in OAuth2 application
   - Never use wildcards in production

4. **Implement token refresh**
   - Access tokens expire after 10 hours
   - Use refresh tokens to get new access tokens
   - Implement automatic token refresh in your app

5. **Use appropriate grant types**
   - Authorization Code for most apps
   - PKCE extension for mobile apps (highly recommended)
   - Avoid Implicit grant (deprecated)

6. **Limit scopes**
   - Only request scopes your app needs
   - Users can see what permissions you're requesting

## Troubleshooting

### "Invalid redirect URI"
- Make sure redirect URI in your request exactly matches one registered in the OAuth2 application
- Check for trailing slashes, http vs https

### "Invalid client"
- Verify client ID is correct
- For confidential clients, verify client secret

### "Access token expired"
- Use refresh token to get new access token
- Implement automatic token refresh

### CORS errors (web apps)
- Configure CORS settings in Django for your domain
- Or use server-side proxy for API calls

## Advanced: PKCE for Mobile Apps

PKCE (Proof Key for Code Exchange) adds security for public clients:

```dart
// Flutter example with PKCE
import 'dart:convert';
import 'dart:math';
import 'package:crypto/crypto.dart';

String generateCodeVerifier() {
  var random = Random.secure();
  var values = List<int>.generate(32, (i) => random.nextInt(256));
  return base64Url.encode(values).replaceAll('=', '');
}

String generateCodeChallenge(String verifier) {
  var bytes = utf8.encode(verifier);
  var digest = sha256.convert(bytes);
  return base64Url.encode(digest.bytes).replaceAll('=', '');
}

// Store verifier
final codeVerifier = generateCodeVerifier();
final codeChallenge = generateCodeChallenge(codeVerifier);

// Add to authorization URL
final authUrl = Uri.parse('http://localhost:8000/o/authorize/').replace(
  queryParameters: {
    'response_type': 'code',
    'client_id': clientId,
    'redirect_uri': redirectUri,
    'scope': 'read write events',
    'code_challenge': codeChallenge,
    'code_challenge_method': 'S256',
  },
);

// When exchanging code for token, include verifier
final tokenResponse = await http.post(
  Uri.parse('http://localhost:8000/o/token/'),
  body: {
    'grant_type': 'authorization_code',
    'code': authCode,
    'redirect_uri': redirectUri,
    'client_id': clientId,
    'code_verifier': codeVerifier,
  },
);
```

## Need Help?

- Check Django OAuth Toolkit docs: https://django-oauth-toolkit.readthedocs.io/
- OAuth2 spec: https://oauth.net/2/
- Open an issue on GitHub for EventHorizon-specific questions
