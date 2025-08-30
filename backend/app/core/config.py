"""
Configuration settings for NeuroDemon application
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import secrets
import os


class Settings(BaseSettings):
    """Application settings with security-first defaults"""
    
    # Application
    APP_NAME: str = "NeuroDemon"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS and Security
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://neurodemon:secure_password@localhost/neurodemon"
    DATABASE_ECHO: bool = False
    
    # Redis (for caching and session management)
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # AI Integration
    AI_API_ENDPOINT: str = "https://oi-server.onrender.com/chat/completions"
    AI_CUSTOMER_ID: str = "cus_SxqlmLh4W5utbp"
    AI_AUTHORIZATION: str = "Bearer xxx"
    AI_DEFAULT_MODEL: str = "openrouter/anthropic/claude-sonnet-4"
    AI_TIMEOUT: int = 300  # 5 minutes
    AI_MAX_TOKENS: int = 4096
    
    # Image Generation
    IMAGE_GEN_MODEL: str = "replicate/black-forest-labs/flux-1.1-pro"
    IMAGE_GEN_TIMEOUT: int = 300  # 5 minutes
    
    # Video Generation  
    VIDEO_GEN_MODEL: str = "replicate/google/veo-3"
    VIDEO_GEN_TIMEOUT: int = 900  # 15 minutes
    
    # Pentesting Tools Configuration
    NMAP_TIMEOUT: int = 300
    NMAP_MAX_PORTS: int = 65535
    SCAN_RATE_LIMIT: int = 100  # requests per minute
    MAX_CONCURRENT_SCANS: int = 10
    
    # Legal & Compliance
    REQUIRE_AUTHORIZATION: bool = True
    LOG_ALL_ACTIVITIES: bool = True
    LEGAL_DISCLAIMER_VERSION: str = "1.0"
    DIGITAL_SIGNATURE_REQUIRED: bool = True
    
    # Accessibility & Neurodivergent Features
    DEFAULT_THEME: str = "calm"  # calm, focus, high-contrast, minimal
    ENABLE_FOCUS_MODE: bool = True
    TIMER_REMINDERS: bool = True
    PROGRESS_INDICATORS: bool = True
    STRESS_MONITORING: bool = True
    
    # File Upload & Storage
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    ALLOWED_FILE_TYPES: List[str] = [".pdf", ".docx", ".txt", ".png", ".jpg", ".jpeg"]
    UPLOAD_PATH: str = "uploads/"
    REPORT_PATH: str = "reports/"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "neurodemon.log"
    LOG_ROTATION: str = "10 MB"
    LOG_RETENTION: str = "30 days"
    
    # Performance & Scaling
    WORKER_PROCESSES: int = 4
    MAX_CONNECTIONS: int = 1000
    CONNECTION_TIMEOUT: int = 30
    
    # Monitoring & Health Checks
    HEALTH_CHECK_INTERVAL: int = 60  # seconds
    METRICS_ENABLED: bool = True
    SENTRY_DSN: Optional[str] = None
    
    # Development Settings
    RELOAD_ON_CHANGE: bool = False
    PROFILING_ENABLED: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()


# Validation functions
def validate_ai_config() -> bool:
    """Validate AI service configuration"""
    required_fields = [
        settings.AI_API_ENDPOINT,
        settings.AI_CUSTOMER_ID,
        settings.AI_AUTHORIZATION,
        settings.AI_DEFAULT_MODEL
    ]
    return all(field for field in required_fields)


def validate_database_config() -> bool:
    """Validate database configuration"""
    return bool(settings.DATABASE_URL and settings.DATABASE_URL.startswith("postgresql"))


def get_ai_headers() -> dict:
    """Get standardized AI API headers"""
    return {
        "CustomerId": settings.AI_CUSTOMER_ID,
        "Content-Type": "application/json",
        "Authorization": settings.AI_AUTHORIZATION
    }


def get_security_config() -> dict:
    """Get security configuration for JWT and encryption"""
    return {
        "secret_key": settings.SECRET_KEY,
        "algorithm": settings.ALGORITHM,
        "access_token_expire_minutes": settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        "refresh_token_expire_days": settings.REFRESH_TOKEN_EXPIRE_DAYS
    }


def get_accessibility_config() -> dict:
    """Get accessibility and neurodivergent support configuration"""
    return {
        "default_theme": settings.DEFAULT_THEME,
        "enable_focus_mode": settings.ENABLE_FOCUS_MODE,
        "timer_reminders": settings.TIMER_REMINDERS,
        "progress_indicators": settings.PROGRESS_INDICATORS,
        "stress_monitoring": settings.STRESS_MONITORING
    }


def get_legal_config() -> dict:
    """Get legal and compliance configuration"""
    return {
        "require_authorization": settings.REQUIRE_AUTHORIZATION,
        "log_all_activities": settings.LOG_ALL_ACTIVITIES,
        "legal_disclaimer_version": settings.LEGAL_DISCLAIMER_VERSION,
        "digital_signature_required": settings.DIGITAL_SIGNATURE_REQUIRED
    }