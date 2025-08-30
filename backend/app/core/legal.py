"""
Legal Framework for NeuroDemon - Ensuring Ethical and Compliant Penetration Testing

This module provides comprehensive legal compliance, authorization verification,
and audit trail functionality to ensure all penetration testing activities
are conducted within legal boundaries.
"""

from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from enum import Enum
import hashlib
import json
import uuid
from dataclasses import dataclass

from cryptography.fernet import Fernet
from loguru import logger

from app.core.config import settings


class LegalStatus(Enum):
    """Legal status enumeration for authorization tracking"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"
    REVOKED = "revoked"


class RiskLevel(Enum):
    """Risk assessment levels for pentesting activities"""
    LOW = "low"
    MEDIUM = "medium" 
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class AuthorizationDocument:
    """Structure for authorization documents"""
    document_id: str
    client_name: str
    client_email: str
    target_systems: List[str]
    authorized_activities: List[str]
    start_date: datetime
    end_date: datetime
    signature_hash: str
    digital_signature: Optional[str] = None
    risk_assessment: RiskLevel = RiskLevel.MEDIUM
    special_conditions: List[str] = None


@dataclass 
class JurisdictionInfo:
    """Legal jurisdiction information"""
    country: str
    state_province: Optional[str]
    applicable_laws: List[str]
    compliance_requirements: List[str]
    legal_contact: Optional[str] = None


class LegalFramework:
    """
    Comprehensive legal framework for ethical penetration testing
    
    Features:
    - Authorization document verification
    - Digital signature validation
    - Audit trail management
    - Compliance monitoring
    - Risk assessment
    - Jurisdiction-specific guidance
    """
    
    def __init__(self):
        self.encryption_key = self._generate_encryption_key()
        self.cipher_suite = Fernet(self.encryption_key)
        self.audit_logs: List[Dict] = []
        self.jurisdictions: Dict[str, JurisdictionInfo] = {}
        self._initialize_jurisdictions()
    
    async def initialize(self):
        """Initialize the legal framework"""
        logger.info("🏛️ Initializing Legal Framework...")
        
        # Load jurisdiction data
        await self._load_jurisdictions()
        
        # Initialize audit logging
        await self._initialize_audit_logging()
        
        # Validate legal configuration
        if settings.REQUIRE_AUTHORIZATION:
            logger.info("✅ Authorization requirement enabled")
        
        if settings.DIGITAL_SIGNATURE_REQUIRED:
            logger.info("✅ Digital signature requirement enabled")
        
        logger.info("✅ Legal Framework initialized successfully")
    
    def _generate_encryption_key(self) -> bytes:
        """Generate encryption key for sensitive data"""
        return Fernet.generate_key()
    
    def _initialize_jurisdictions(self):
        """Initialize jurisdiction-specific legal information"""
        self.jurisdictions = {
            "US": JurisdictionInfo(
                country="United States",
                state_province=None,
                applicable_laws=[
                    "Computer Fraud and Abuse Act (CFAA)",
                    "Digital Millennium Copyright Act (DMCA)",
                    "State-specific cybercrime laws"
                ],
                compliance_requirements=[
                    "Written authorization required",
                    "Scope limitations must be respected", 
                    "Data protection regulations apply"
                ]
            ),
            "EU": JurisdictionInfo(
                country="European Union",
                state_province=None,
                applicable_laws=[
                    "General Data Protection Regulation (GDPR)",
                    "NIS2 Directive",
                    "Cybersecurity Act",
                    "Country-specific cybercrime laws"
                ],
                compliance_requirements=[
                    "GDPR compliance mandatory",
                    "Data Protection Impact Assessment may be required",
                    "Right to be forgotten must be respected"
                ]
            ),
            "UK": JurisdictionInfo(
                country="United Kingdom", 
                state_province=None,
                applicable_laws=[
                    "Computer Misuse Act 1990",
                    "Data Protection Act 2018",
                    "UK GDPR"
                ],
                compliance_requirements=[
                    "Explicit consent required",
                    "ICO registration may be required",
                    "Lawful basis for processing must be established"
                ]
            )
        }
    
    async def _load_jurisdictions(self):
        """Load additional jurisdiction data from database"""
        # Implementation for loading jurisdiction data from database
        pass
    
    async def _initialize_audit_logging(self):
        """Initialize comprehensive audit logging system"""
        logger.info("📝 Initializing audit logging system...")
        
        # Create audit log entry for system startup
        await self.log_activity(
            activity_type="system_startup",
            description="Legal Framework initialized",
            user_id="system",
            risk_level=RiskLevel.LOW,
            metadata={"version": settings.VERSION}
        )
    
    async def verify_authorization(
        self, 
        document: AuthorizationDocument, 
        user_id: str
    ) -> Dict[str, Any]:
        """
        Verify authorization document and digital signatures
        
        Args:
            document: Authorization document to verify
            user_id: ID of user requesting authorization
            
        Returns:
            Verification result with status and details
        """
        logger.info(f"🔍 Verifying authorization for user {user_id}")
        
        verification_result = {
            "status": LegalStatus.PENDING,
            "document_id": document.document_id,
            "verified_at": datetime.now(timezone.utc),
            "verifications": {},
            "issues": [],
            "risk_assessment": document.risk_assessment.value
        }
        
        try:
            # 1. Verify document completeness
            completeness_check = self._verify_document_completeness(document)
            verification_result["verifications"]["completeness"] = completeness_check
            
            # 2. Verify digital signature if present
            if document.digital_signature:
                signature_check = await self._verify_digital_signature(document)
                verification_result["verifications"]["digital_signature"] = signature_check
            elif settings.DIGITAL_SIGNATURE_REQUIRED:
                verification_result["issues"].append("Digital signature required but not provided")
            
            # 3. Verify authorization scope
            scope_check = self._verify_authorization_scope(document)
            verification_result["verifications"]["scope"] = scope_check
            
            # 4. Check date validity
            date_check = self._verify_dates(document)
            verification_result["verifications"]["dates"] = date_check
            
            # 5. Risk assessment
            risk_check = self._assess_risk(document)
            verification_result["verifications"]["risk_assessment"] = risk_check
            
            # Determine overall status
            if all(check.get("valid", False) for check in verification_result["verifications"].values()):
                if not verification_result["issues"]:
                    verification_result["status"] = LegalStatus.APPROVED
                else:
                    verification_result["status"] = LegalStatus.REJECTED
            else:
                verification_result["status"] = LegalStatus.REJECTED
            
            # Log verification attempt
            await self.log_activity(
                activity_type="authorization_verification",
                description=f"Authorization verification completed: {verification_result['status'].value}",
                user_id=user_id,
                risk_level=document.risk_assessment,
                metadata={
                    "document_id": document.document_id,
                    "client": document.client_name,
                    "targets": len(document.target_systems),
                    "verification_result": verification_result["status"].value
                }
            )
            
            return verification_result
            
        except Exception as e:
            logger.error(f"❌ Authorization verification failed: {str(e)}")
            verification_result["status"] = LegalStatus.REJECTED
            verification_result["issues"].append(f"Verification error: {str(e)}")
            
            await self.log_activity(
                activity_type="authorization_error",
                description=f"Authorization verification failed: {str(e)}",
                user_id=user_id,
                risk_level=RiskLevel.HIGH,
                metadata={"error": str(e), "document_id": document.document_id}
            )
            
            return verification_result
    
    def _verify_document_completeness(self, document: AuthorizationDocument) -> Dict[str, Any]:
        """Verify that all required document fields are present"""
        required_fields = [
            "document_id", "client_name", "client_email", 
            "target_systems", "authorized_activities",
            "start_date", "end_date", "signature_hash"
        ]
        
        missing_fields = []
        for field in required_fields:
            if not getattr(document, field, None):
                missing_fields.append(field)
        
        return {
            "valid": len(missing_fields) == 0,
            "missing_fields": missing_fields,
            "checked_at": datetime.now(timezone.utc)
        }
    
    async def _verify_digital_signature(self, document: AuthorizationDocument) -> Dict[str, Any]:
        """Verify digital signature of authorization document"""
        try:
            # Implementation would verify actual digital signature
            # For now, we'll do a basic hash verification
            computed_hash = self._compute_document_hash(document)
            signature_valid = computed_hash == document.signature_hash
            
            return {
                "valid": signature_valid,
                "signature_hash": document.signature_hash,
                "computed_hash": computed_hash,
                "verified_at": datetime.now(timezone.utc)
            }
        except Exception as e:
            return {
                "valid": False,
                "error": str(e),
                "verified_at": datetime.now(timezone.utc)
            }
    
    def _compute_document_hash(self, document: AuthorizationDocument) -> str:
        """Compute hash of document for integrity verification"""
        document_data = {
            "client_name": document.client_name,
            "client_email": document.client_email,
            "target_systems": sorted(document.target_systems),
            "authorized_activities": sorted(document.authorized_activities),
            "start_date": document.start_date.isoformat(),
            "end_date": document.end_date.isoformat()
        }
        
        document_string = json.dumps(document_data, sort_keys=True)
        return hashlib.sha256(document_string.encode()).hexdigest()
    
    def _verify_authorization_scope(self, document: AuthorizationDocument) -> Dict[str, Any]:
        """Verify that authorization scope is reasonable and specific"""
        issues = []
        
        # Check target systems
        if not document.target_systems:
            issues.append("No target systems specified")
        elif len(document.target_systems) > 100:
            issues.append("Too many target systems (>100)")
        
        # Check authorized activities
        if not document.authorized_activities:
            issues.append("No authorized activities specified")
        
        # Check for overly broad authorizations
        broad_activities = ["full access", "any activity", "unrestricted"]
        if any(activity.lower() in broad_activities for activity in document.authorized_activities):
            issues.append("Authorization scope too broad")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "target_count": len(document.target_systems),
            "activity_count": len(document.authorized_activities)
        }
    
    def _verify_dates(self, document: AuthorizationDocument) -> Dict[str, Any]:
        """Verify authorization date validity"""
        now = datetime.now(timezone.utc)
        issues = []
        
        # Check if start date is too far in the past
        if (now - document.start_date).days > 30:
            issues.append("Start date more than 30 days in the past")
        
        # Check if end date has passed
        if document.end_date < now:
            issues.append("Authorization has expired")
        
        # Check if date range is reasonable
        duration = (document.end_date - document.start_date).days
        if duration > 365:
            issues.append("Authorization period too long (>1 year)")
        elif duration < 1:
            issues.append("Authorization period too short (<1 day)")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "duration_days": duration
        }
    
    def _assess_risk(self, document: AuthorizationDocument) -> Dict[str, Any]:
        """Assess risk level of proposed penetration testing activities"""
        risk_factors = []
        
        # Check for high-risk activities
        high_risk_activities = [
            "exploitation", "privilege escalation", "lateral movement",
            "data exfiltration", "denial of service", "social engineering"
        ]
        
        for activity in document.authorized_activities:
            if any(risk_term in activity.lower() for risk_term in high_risk_activities):
                risk_factors.append(f"High-risk activity: {activity}")
        
        # Check target system count
        if len(document.target_systems) > 50:
            risk_factors.append("Large number of target systems")
        
        # Determine overall risk level
        if len(risk_factors) >= 3 or document.risk_assessment == RiskLevel.CRITICAL:
            overall_risk = RiskLevel.HIGH
        elif len(risk_factors) >= 1 or document.risk_assessment == RiskLevel.HIGH:
            overall_risk = RiskLevel.MEDIUM
        else:
            overall_risk = RiskLevel.LOW
        
        return {
            "valid": True,
            "risk_level": overall_risk.value,
            "risk_factors": risk_factors,
            "assessment_date": datetime.now(timezone.utc)
        }
    
    async def log_activity(
        self,
        activity_type: str,
        description: str,
        user_id: str,
        risk_level: RiskLevel,
        metadata: Dict[str, Any] = None
    ):
        """Log activity for audit trail"""
        log_entry = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc),
            "activity_type": activity_type,
            "description": description,
            "user_id": user_id,
            "risk_level": risk_level.value,
            "metadata": metadata or {},
            "ip_address": None,  # Would be populated from request context
            "user_agent": None   # Would be populated from request context
        }
        
        # Encrypt sensitive data
        if metadata and any(key in str(metadata) for key in ["password", "token", "key"]):
            log_entry["metadata"] = self._encrypt_sensitive_data(metadata)
        
        self.audit_logs.append(log_entry)
        
        # Log to structured logging system
        logger.info(
            f"🔍 {activity_type}: {description}",
            extra={
                "user_id": user_id,
                "risk_level": risk_level.value,
                "metadata": metadata
            }
        )
    
    def _encrypt_sensitive_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Encrypt sensitive data in audit logs"""
        encrypted_data = {}
        sensitive_keys = ["password", "token", "key", "secret", "credential"]
        
        for key, value in data.items():
            if any(sensitive in key.lower() for sensitive in sensitive_keys):
                encrypted_data[key] = self.cipher_suite.encrypt(str(value).encode()).decode()
            else:
                encrypted_data[key] = value
        
        return encrypted_data
    
    async def get_jurisdiction_info(self, country_code: str) -> Optional[JurisdictionInfo]:
        """Get jurisdiction-specific legal information"""
        return self.jurisdictions.get(country_code.upper())
    
    async def generate_compliance_report(
        self, 
        user_id: str, 
        start_date: datetime, 
        end_date: datetime
    ) -> Dict[str, Any]:
        """Generate compliance report for audit purposes"""
        relevant_logs = [
            log for log in self.audit_logs
            if start_date <= log["timestamp"] <= end_date
            and log["user_id"] == user_id
        ]
        
        return {
            "report_id": str(uuid.uuid4()),
            "generated_at": datetime.now(timezone.utc),
            "period_start": start_date,
            "period_end": end_date,
            "user_id": user_id,
            "total_activities": len(relevant_logs),
            "activities_by_type": self._categorize_activities(relevant_logs),
            "risk_summary": self._summarize_risks(relevant_logs),
            "compliance_status": "compliant",  # Would be determined by analysis
            "recommendations": []
        }
    
    def _categorize_activities(self, logs: List[Dict]) -> Dict[str, int]:
        """Categorize activities for reporting"""
        categories = {}
        for log in logs:
            activity_type = log["activity_type"]
            categories[activity_type] = categories.get(activity_type, 0) + 1
        return categories
    
    def _summarize_risks(self, logs: List[Dict]) -> Dict[str, Any]:
        """Summarize risk levels for reporting"""
        risk_counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        
        for log in logs:
            risk_level = log["risk_level"]
            risk_counts[risk_level] = risk_counts.get(risk_level, 0) + 1
        
        return {
            "risk_distribution": risk_counts,
            "total_high_risk": risk_counts["high"] + risk_counts["critical"],
            "risk_percentage": {
                level: (count / len(logs)) * 100 if logs else 0
                for level, count in risk_counts.items()
            }
        }