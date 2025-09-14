# Railway Deployment Guide

This guide explains how to deploy the PentryPal backend to Railway.app.

## Prerequisites

1. A Railway.app account
2. Your project code pushed to a GitHub repository
3. Basic understanding of environment variables

## Deployment Steps

### 1. Create a New Railway Project

1. Go to [Railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Connect your GitHub account and select this repository

### 2. Add Required Services

Your application needs these services:

#### PostgreSQL Database
1. In your Railway project, click "New Service"
2. Select "Database" → "PostgreSQL"
3. Railway will automatically create a PostgreSQL instance

#### Redis (Optional but Recommended)
1. Click "New Service" → "Database" → "Redis"
2. This enables full WebSocket functionality

### 3. Generate JWT Secret Key

**IMPORTANT**: You must generate a secure JWT secret key for production. Here are several ways to do it:

#### Method 1: Using Python (Recommended)
```bash
python3 -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(64))"
```

#### Method 2: Using OpenSSL
```bash
openssl rand -base64 64
```

#### Method 3: Online Generator
Visit: https://generate-secret.vercel.app/64

**Example generated key:**
```
JWT_SECRET_KEY=XE-_Pziv1GyFAHmILR15eMgb-_aAYzsZ-alfKKiqpg82jtBLSDezg3nGV0xcEqfLYUjk7Ao2PBVCA_Fr-1arMQ
```

### 4. Configure Environment Variables

In your Railway project dashboard, go to your main service and set these variables:

#### Required Variables
```bash
# Database (automatically set by Railway PostgreSQL service)
DATABASE_URL=${{Postgres.DATABASE_URL}}

# Redis (automatically set by Railway Redis service)
REDIS_URL=${{Redis.REDIS_URL}}

# JWT Security (IMPORTANT: Generate a secure key - see below)
JWT_SECRET_KEY=your-super-secure-jwt-key-change-this-now

# API Configuration
DEBUG=false
PROJECT_NAME=PentryPal API
PROJECT_VERSION=1.0.0

# CORS Origins (for native mobile apps, use "*" to allow all origins)
BACKEND_CORS_ORIGINS=["*"]
```

#### Optional Variables
```bash
# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60

# File Uploads
MAX_FILE_SIZE_MB=10

# WebSocket
WEBSOCKET_HEARTBEAT_INTERVAL=30

# JWT Token Expiry
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 5. Deploy

1. Railway will automatically deploy when you push to your connected branch
2. Monitor the deployment in the Railway dashboard
3. Check logs for any errors

### 6. Run Database Migrations

After the first deployment, you need to run database migrations:

1. Go to your service in Railway dashboard
2. Open the "Deployments" tab
3. Click on the latest deployment
4. Open the "Console" tab
5. Run: `alembic upgrade head`

Alternatively, the migrations will run automatically if you're using the Procfile.

### 7. Verify Deployment

1. Check your service URL in Railway dashboard
2. Visit `https://your-service-url.railway.app/health` - should return `{"status": "healthy"}`
3. Visit `https://your-service-url.railway.app/api/v1/docs` for API documentation

## Native Mobile App Configuration

### CORS for Mobile Apps
Since your frontend is a native mobile app, CORS restrictions are different:

- **Native apps don't enforce CORS** like web browsers do
- **Use `"*"` for CORS origins** to allow all requests
- **This is safe for mobile apps** as they don't have the same security model as web browsers

### Environment Variables for Mobile Apps
```bash
# For native mobile apps
BACKEND_CORS_ORIGINS=["*"]
```

### Mobile App API Integration
Your mobile app can connect directly to:
```
https://your-service-url.railway.app/api/v1/
```

## Important Security Notes

1. **JWT_SECRET_KEY**: Generate a strong, unique secret key for production
2. **CORS Origins**: For native mobile apps, using `"*"` is acceptable and recommended
3. **Database**: Railway PostgreSQL is automatically secured
4. **Environment Variables**: Never commit sensitive data to your repository
5. **Mobile Security**: Rely on JWT tokens and API authentication, not CORS

## File Upload Configuration

For file uploads (user avatars), Railway provides ephemeral storage. For production, consider:

1. Using Railway's persistent volumes (if available)
2. Integrating with cloud storage (AWS S3, Cloudinary, etc.)
3. The current setup works but uploaded files may not persist across deployments

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Ensure DATABASE_URL is properly set to `${{Postgres.DATABASE_URL}}`
   - Check if PostgreSQL service is running

2. **Redis Connection Errors**
   - WebSocket features will be limited without Redis
   - Ensure REDIS_URL is set to `${{Redis.REDIS_URL}}`

3. **CORS Errors**
   - Update BACKEND_CORS_ORIGINS with your frontend URL
   - Ensure the format is a JSON array string

4. **Port Issues**
   - Railway automatically sets the PORT environment variable
   - The application is configured to use this automatically

### Viewing Logs

1. Go to your Railway project dashboard
2. Click on your service
3. Go to the "Deployments" tab
4. Click on a deployment to view logs

## WebSocket Connection

WebSocket endpoint for real-time features:
```
wss://your-service-url.railway.app/api/v1/realtime/ws/<jwt_token>
```

## API Documentation

Once deployed, your API documentation will be available at:
```
https://your-service-url.railway.app/api/v1/docs
```

## Support

If you encounter issues:
1. Check Railway's documentation: https://docs.railway.app
2. Review application logs in Railway dashboard
3. Ensure all environment variables are properly set
