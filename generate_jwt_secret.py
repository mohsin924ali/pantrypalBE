#!/usr/bin/env python3
"""
JWT Secret Key Generator for PentryPal Backend
Generates secure JWT secret keys for production deployment
"""

import secrets
import base64
import os

def generate_jwt_secret():
    """Generate a secure JWT secret key"""
    # Generate 64 bytes of random data
    random_bytes = secrets.token_bytes(64)
    
    # Convert to URL-safe base64 string
    jwt_secret = base64.urlsafe_b64encode(random_bytes).decode('utf-8')
    
    return jwt_secret

def main():
    """Main function to generate and display JWT secret"""
    print("🔐 PentryPal JWT Secret Key Generator")
    print("=" * 50)
    
    # Generate the secret
    secret = generate_jwt_secret()
    
    print(f"Generated JWT Secret Key:")
    print(f"JWT_SECRET_KEY={secret}")
    print()
    
    print("📋 For Railway Deployment:")
    print("1. Copy the JWT_SECRET_KEY value above")
    print("2. Go to your Railway project dashboard")
    print("3. Navigate to your service → Variables")
    print("4. Add new variable: JWT_SECRET_KEY")
    print("5. Paste the generated value")
    print()
    
    print("⚠️  Security Notes:")
    print("- Keep this secret key secure and private")
    print("- Never commit it to version control")
    print("- Use different keys for different environments")
    print("- If compromised, generate a new key immediately")
    print()
    
    print("✅ Your JWT secret key is ready for Railway deployment!")

if __name__ == "__main__":
    main()
