# Google SSO Integration Guide

## Overview
FarmTrack now supports Google OAuth 2.0 authentication for both login and registration.

## Setup

### 1. Google Cloud Console Configuration

Your Google OAuth credentials are already configured in the `.env` files:
- **Client ID**: `44569555873-cbhlf86mh1q2i6q5mipberg5si6kbk70.apps.googleusercontent.com`
- **Client Secret**: `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`

Make sure in your Google Cloud Console (https://console.cloud.google.com/apis/credentials):
- **Authorized JavaScript origins**: `http://localhost:3000`
- **Authorized redirect URIs**: 
  - `http://localhost:3000/api/auth/callback/google`
  - `http://localhost:3000`

### 2. Environment Variables

**Frontend** (`FrontEnd/.env`):
```bash
GOOGLE_CLIENT_ID="44569555873-cbhlf86mh1q2i6q5mipberg5si6kbk70.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET="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"
NEXTAUTH_SECRET="R1m5ZWduXhZj30KWn5k2s+ruT1J7bKKdkD+DikIiM34="
NEXTAUTH_URL="http://localhost:3000"
```

**Backend** (`BackEnd/.env`):
```bash
GOOGLE_CLIENT_ID=44569555873-cbhlf86mh1q2i6q5mipberg5si6kbk70.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=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
```

## How It Works

### Login Flow
1. User clicks "Login with Google" on `/login` page
2. User is redirected to Google's OAuth consent screen
3. After approval, Google redirects back with an ID token
4. Frontend sends the Google token to backend `/api/v1/auth/google-auth`
5. Backend verifies the token with Google's servers
6. If valid, backend:
   - Finds existing user by email OR
   - Creates new user with info from Google
   - Returns JWT access token
7. Frontend stores JWT and redirects to dashboard

### Registration Flow
1. User clicks "Sign up with Google" on `/register` page
2. User can select their role (Farmer, Processor, Regulator) before signing in
3. Same flow as login, but role is sent to backend
4. New users are created with the selected role

### Sign Out Flow
1. User clicks "Sign Out" in dropdown menu
2. Clears localStorage tokens
3. Signs out from Google session (if SSO was used)
4. Redirects to `/login`

## Backend Endpoints

### `/api/v1/auth/google-auth` (POST)
Verify Google OAuth token and return JWT.

**Request Body:**
```json
{
  "token": "google-id-token-from-frontend",
  "role": "farmer"  // Optional, defaults to "farmer"
}
```

**Response:**
```json
{
  "access_token": "jwt-token",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "user123",
    "role": "farmer",
    "email": "user@gmail.com",
    "full_name": "John Doe"
  }
}
```

## Frontend Implementation

### Login Form (`LoginForm.vue`)
- Uses `useAuth()` from `@sidebase/nuxt-auth`
- Watches for session changes
- Sends Google token to backend for verification
- Stores backend JWT for API calls

### Register Form (`RegisterForm.vue`)
- Same flow as login
- Allows role selection before Google sign-in
- Role is passed to backend during registration

### Auth Management (`useAuthManagement.ts`)
- Handles sign out for both credential and SSO auth
- Clears tokens and redirects appropriately

## Security Features

1. **Token Verification**: Backend verifies Google tokens with Google's servers
2. **Audience Check**: Ensures token is for your app
3. **Email Requirement**: Users must have email from Google
4. **Unique Usernames**: Auto-generates unique usernames from email
5. **JWT Tokens**: Backend issues its own JWT for API authentication
6. **Role-Based Access**: Users can select role during registration

## User Experience

### For New Users:
- Click "Sign up with Google" or "Login with Google"
- Select role (Farmer/Processor/Regulator) on register page
- Approve Google consent screen
- Automatically logged in and redirected to dashboard

### For Existing Users:
- Click "Login with Google"
- Automatically matched by email
- Logged in with existing account

### Mixed Authentication:
- Users can use Google SSO or traditional credentials
- Backend identifies users by email
- Same JWT authentication for all API calls

## Troubleshooting

### "Invalid token audience" error
- Check that `GOOGLE_CLIENT_ID` matches in both frontend and backend `.env` files
- Verify the token is coming from your Google Cloud project

### Google consent screen not appearing
- Check authorized redirect URIs in Google Cloud Console
- Ensure `NEXTAUTH_URL` is correct in frontend `.env`

### User created with wrong role
- Ensure role is selected before clicking Google sign-up
- Default role is "farmer" if not specified

## Dependencies

**Backend:**
- `google-auth` - Google authentication library
- `google-auth-oauthlib` - OAuth library
- `google-auth-httplib2` - HTTP transport

**Frontend:**
- `@sidebase/nuxt-auth` - Nuxt auth module
- `@auth/core` - Auth.js core
- Configured in `nuxt.config.ts`

## Testing

1. **Test Login**: Navigate to http://localhost:3000/login
2. **Test Register**: Navigate to http://localhost:3000/register
3. **Test Sign Out**: Click user avatar → Sign Out
4. **Test API Auth**: Check Network tab - all API calls should have `Authorization: Bearer <token>` header
