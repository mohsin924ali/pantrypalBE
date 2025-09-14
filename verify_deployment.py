#!/usr/bin/env python3
"""
Deployment verification script for PentryPal backend
Run this script to verify your deployment configuration
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath: str, description: str) -> bool:
    """Check if a file exists"""
    if Path(filepath).exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} (MISSING)")
        return False

def check_env_example() -> bool:
    """Check if env.example has all required variables"""
    required_vars = [
        "DATABASE_URL",
        "REDIS_URL", 
        "JWT_SECRET_KEY",
        "DEBUG",
        "BACKEND_CORS_ORIGINS"
    ]
    
    if not Path("env.example").exists():
        print("❌ env.example file missing")
        return False
    
    with open("env.example", "r") as f:
        content = f.read()
    
    missing_vars = []
    for var in required_vars:
        if var not in content:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ env.example missing variables: {', '.join(missing_vars)}")
        return False
    else:
        print("✅ env.example contains all required variables")
        return True

def main():
    """Main verification function"""
    print("🔍 Verifying Railway deployment configuration...\n")
    
    checks = []
    
    # Check required files
    checks.append(check_file_exists("Dockerfile", "Dockerfile"))
    checks.append(check_file_exists("requirements.txt", "Requirements file"))
    checks.append(check_file_exists("railway.json", "Railway config"))
    checks.append(check_file_exists("Procfile", "Procfile"))
    checks.append(check_file_exists(".railwayignore", "Railway ignore file"))
    checks.append(check_file_exists("RAILWAY_DEPLOYMENT.md", "Deployment guide"))
    checks.append(check_file_exists("app/main.py", "Main application"))
    checks.append(check_file_exists("alembic.ini", "Alembic config"))
    
    # Check environment example
    checks.append(check_env_example())
    
    # Summary
    passed = sum(checks)
    total = len(checks)
    
    print(f"\n📊 Verification Summary: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 All checks passed! Your project is ready for Railway deployment.")
        print("\n📝 Next steps:")
        print("1. Push your code to GitHub")
        print("2. Create a new Railway project")
        print("3. Add PostgreSQL and Redis services")
        print("4. Set environment variables (see RAILWAY_DEPLOYMENT.md)")
        print("5. Deploy and run database migrations")
    else:
        print("⚠️  Some checks failed. Please fix the issues above before deploying.")
        sys.exit(1)

if __name__ == "__main__":
    main()
