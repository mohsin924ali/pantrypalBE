"""
Application configuration settings
"""
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import validator
import os


class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "PentryPal API"
    PROJECT_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Railway Environment Detection
    RAILWAY_ENVIRONMENT: Optional[str] = None
    PORT: int = 8000
    
    # Database Configuration
    DATABASE_URL: Optional[str] = None
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = "pentrypal_db"
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = "password"
    
    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict) -> str:
        if isinstance(v, str) and v:
            # If URL is provided and starts with postgres://, convert to postgresql://
            if v.startswith("postgres://"):
                return v.replace("postgres://", "postgresql://", 1)
            return v
        return f"postgresql://{values.get('DATABASE_USER')}:{values.get('DATABASE_PASSWORD')}@{values.get('DATABASE_HOST')}:{values.get('DATABASE_PORT')}/{values.get('DATABASE_NAME')}"
    
    # JWT Configuration
    JWT_SECRET_KEY: str = "your-super-secret-jwt-key-change-this-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS Configuration
    # For native mobile apps, CORS is less restrictive
    BACKEND_CORS_ORIGINS: str = "*"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.RAILWAY_ENVIRONMENT is not None or not self.DEBUG
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert CORS origins string to list for FastAPI CORS middleware"""
        if self.BACKEND_CORS_ORIGINS == "*":
            return ["*"]
        elif "," in self.BACKEND_CORS_ORIGINS:
            return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",") if origin.strip()]
        else:
            return [self.BACKEND_CORS_ORIGINS] if self.BACKEND_CORS_ORIGINS else ["*"]
    
    
    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # File Upload Configuration
    MAX_FILE_SIZE_MB: int = 10
    UPLOAD_DIR: str = "uploads/"
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # WebSocket Configuration
    WEBSOCKET_HEARTBEAT_INTERVAL: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()
