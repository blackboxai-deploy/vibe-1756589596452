"""
NeuroDemon - AI-Powered Neurodivergent-Friendly Penetration Testing Application
Main FastAPI application entry point
"""

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
import uvicorn
import logging
from loguru import logger

from app.core.config import settings
from app.core.database import init_db
from app.core.legal import LegalFramework
from app.api.routes import api_router
from app.core.auth import verify_token
from app.core.accessibility import AccessibilityMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("🧠 NeuroDemon starting up...")
    
    # Initialize database
    await init_db()
    
    # Initialize legal framework
    legal_framework = LegalFramework()
    await legal_framework.initialize()
    
    # Initialize AI services
    logger.info("🤖 Initializing AI services...")
    
    logger.info("✅ NeuroDemon startup complete!")
    
    yield
    
    # Shutdown
    logger.info("🔽 NeuroDemon shutting down...")


# Create FastAPI application with neurodivergent-friendly features
app = FastAPI(
    title="NeuroDemon API",
    description="""
    🧠 **NeuroDemon** - AI-Powered Neurodivergent-Friendly Penetration Testing Application
    
    **⚠️ LEGAL NOTICE**: FOR AUTHORIZED PENETRATION TESTING ONLY
    Unauthorized use may result in criminal prosecution.
    
    ## Features
    
    ### 🔒 Legal & Ethical Framework
    - Mandatory target authorization verification
    - Comprehensive activity logging
    - Digital signature verification
    - Compliance reporting
    
    ### 🧠 Neurodivergent-Friendly Design
    - ADHD-friendly: Focus mode, task breakdowns, timers
    - Autism-friendly: Predictable workflows, detailed docs
    - Anxiety management: Risk assessments, undo capabilities
    - OCD accommodations: Verification checklists
    - PTSD considerations: Gentle notifications, stress monitoring
    
    ### 🤖 AI Integration
    - Natural language pentesting guidance
    - Automated tool selection
    - Intelligent report generation
    - Context-aware suggestions
    
    ### 🛡️ Core Pentesting Modules
    - Network Discovery & Enumeration
    - Port Scanning & Service Detection
    - Vulnerability Assessment
    - Web Application Testing
    - Wireless Security Testing
    - Cloud Security Testing (AWS, Azure, GCP)
    - Mobile Application Testing
    - API Security Testing
    
    **Made with ❤️ for the neurodivergent cybersecurity community**
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/api/redoc" if settings.ENVIRONMENT == "development" else None,
)

# Security middleware
security = HTTPBearer()

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=settings.ALLOWED_HOSTS
)

# Add accessibility middleware for neurodivergent users
app.add_middleware(AccessibilityMiddleware)


@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    """Add security headers to all responses"""
    response = await call_next(request)
    
    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    
    return response


@app.get("/")
async def root():
    """Root endpoint with legal disclaimer"""
    return {
        "application": "NeuroDemon",
        "version": "1.0.0",
        "description": "AI-Powered Neurodivergent-Friendly Penetration Testing Application",
        "legal_notice": "⚠️ FOR AUTHORIZED PENETRATION TESTING ONLY - Unauthorized use may result in criminal prosecution",
        "features": {
            "neurodivergent_friendly": True,
            "ai_powered": True,
            "legal_compliant": True,
            "accessible": True
        },
        "documentation": "/api/docs",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "application": "NeuroDemon",
        "version": "1.0.0",
        "timestamp": "2024-01-01T00:00:00Z"
    }


@app.get("/legal/disclaimer")
async def legal_disclaimer():
    """Legal disclaimer and terms of use"""
    return {
        "disclaimer": """
        ⚠️ IMPORTANT LEGAL NOTICE ⚠️
        
        FOR AUTHORIZED PENETRATION TESTING ONLY
        
        This application is designed exclusively for authorized security testing
        and penetration testing activities. Users must:
        
        1. Obtain explicit written authorization before testing any systems
        2. Comply with all applicable laws and regulations
        3. Use this tool only for legitimate security assessment purposes
        4. Maintain confidentiality of all discovered vulnerabilities
        5. Report findings responsibly through proper channels
        
        UNAUTHORIZED USE IS STRICTLY PROHIBITED and may result in:
        - Criminal prosecution under computer fraud and abuse laws
        - Civil liability for damages
        - Professional sanctions and loss of credentials
        - Permanent ban from using this application
        
        By using this application, you acknowledge that you understand and agree
        to these terms and accept full responsibility for your actions.
        """,
        "acceptance_required": True,
        "version": "1.0",
        "last_updated": "2024-01-01"
    }


# Include API routers
app.include_router(api_router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development",
        log_level="info"
    )