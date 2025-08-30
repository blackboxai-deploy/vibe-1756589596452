"""
Accessibility and Neurodivergent Support Framework for NeuroDemon

Provides comprehensive accessibility features and accommodations for
neurodivergent users including ADHD, autism, anxiety, OCD, and PTSD support.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger

from app.core.config import get_accessibility_config


class NeurodivergentType(Enum):
    """Types of neurodivergent conditions supported"""
    ADHD = "adhd"
    AUTISM = "autism"
    ANXIETY = "anxiety"
    OCD = "ocd"
    PTSD = "ptsd"
    DYSLEXIA = "dyslexia"
    SENSORY_PROCESSING = "sensory_processing"


class StressLevel(Enum):
    """User stress levels for adaptive interface"""
    LOW = "low"
    NORMAL = "normal"
    ELEVATED = "elevated"
    HIGH = "high"
    CRITICAL = "critical"


class FocusMode(Enum):
    """Focus modes for different attention needs"""
    NORMAL = "normal"
    MINIMAL = "minimal"
    HYPERFOCUS = "hyperfocus"
    BREAK_TIME = "break_time"


@dataclass
class UserAccessibilityProfile:
    """User accessibility profile and preferences"""
    user_id: str
    neurodivergent_types: List[NeurodivergentType]
    theme_preference: str = "calm"
    font_size_preference: str = "medium"
    animation_preference: str = "reduced"
    sound_preference: str = "minimal"
    notification_style: str = "gentle"
    focus_mode: FocusMode = FocusMode.NORMAL
    break_interval: int = 25  # minutes
    stress_monitoring: bool = True
    progress_granularity: str = "detailed"


class AccessibilityMiddleware(BaseHTTPMiddleware):
    """Middleware to apply accessibility features to all responses"""
    
    async def dispatch(self, request: Request, call_next):
        # Get user accessibility preferences
        user_profile = await self._get_user_profile(request)
        
        # Process request with accessibility context
        request.state.accessibility_profile = user_profile
        
        # Call the next middleware/endpoint
        response = await call_next(request)
        
        # Apply accessibility modifications to response
        if user_profile:
            response = self._apply_accessibility_headers(response, user_profile)
        
        return response
    
    async def _get_user_profile(self, request: Request) -> Optional[UserAccessibilityProfile]:
        """Get user accessibility profile from session/database"""
        # In a real implementation, this would fetch from database
        # For now, we'll check for accessibility headers or default profile
        
        user_agent = request.headers.get("user-agent", "").lower()
        
        # Detect screen reader usage
        if "nvda" in user_agent or "jaws" in user_agent or "voiceover" in user_agent:
            return UserAccessibilityProfile(
                user_id="anonymous",
                neurodivergent_types=[],
                theme_preference="high-contrast",
                sound_preference="enhanced"
            )
        
        # Return default accessibility-friendly profile
        return UserAccessibilityProfile(
            user_id="anonymous",
            neurodivergent_types=[NeurodivergentType.ADHD, NeurodivergentType.AUTISM],
            theme_preference="calm"
        )
    
    def _apply_accessibility_headers(self, response: Response, profile: UserAccessibilityProfile) -> Response:
        """Apply accessibility-specific headers"""
        # Add accessibility headers
        response.headers["X-Accessibility-Profile"] = "enabled"
        response.headers["X-Theme-Preference"] = profile.theme_preference
        response.headers["X-Animation-Preference"] = profile.animation_preference
        response.headers["X-Focus-Mode"] = profile.focus_mode.value
        
        return response


class NeurodivergentSupport:
    """
    Comprehensive support system for neurodivergent users
    
    Features:
    - ADHD: Focus management, task breakdown, timer reminders
    - Autism: Predictable workflows, detailed explanations, routine templates
    - Anxiety: Risk assessments, confidence indicators, undo capabilities
    - OCD: Verification checklists, completion confirmations
    - PTSD: Gentle notifications, stress monitoring, break suggestions
    """
    
    def __init__(self):
        self.user_sessions: Dict[str, Dict] = {}
        self.break_timers: Dict[str, datetime] = {}
        self.stress_monitors: Dict[str, List[Dict]] = {}
    
    async def get_adhd_support(self, user_id: str, current_task: str) -> Dict[str, Any]:
        """Provide ADHD-specific support and accommodations"""
        return {
            "task_breakdown": self._break_down_task(current_task),
            "focus_timer": {
                "recommended_duration": 25,  # Pomodoro technique
                "break_duration": 5,
                "long_break_after": 4
            },
            "distraction_management": {
                "minimize_notifications": True,
                "hide_non_essential_ui": True,
                "focus_mode_available": True
            },
            "motivation_techniques": {
                "progress_visualization": True,
                "achievement_badges": True,
                "task_completion_celebrations": True
            },
            "time_management": {
                "estimated_time": self._estimate_task_time(current_task),
                "deadline_reminders": True,
                "time_tracking": True
            }
        }
    
    async def get_autism_support(self, user_id: str, workflow_stage: str) -> Dict[str, Any]:
        """Provide autism-specific support and accommodations"""
        return {
            "predictable_workflow": {
                "clear_steps": True,
                "consistent_navigation": True,
                "no_surprising_changes": True
            },
            "detailed_explanations": {
                "why_this_step": self._explain_workflow_step(workflow_stage),
                "what_happens_next": self._get_next_steps(workflow_stage),
                "expected_outcomes": self._get_expected_outcomes(workflow_stage)
            },
            "routine_templates": {
                "saved_workflows": True,
                "customizable_templates": True,
                "step_by_step_guides": True
            },
            "sensory_considerations": {
                "reduced_visual_clutter": True,
                "consistent_color_scheme": True,
                "minimal_animations": True,
                "optional_audio_cues": True
            }
        }
    
    async def get_anxiety_support(self, user_id: str, risk_level: str) -> Dict[str, Any]:
        """Provide anxiety management support"""
        return {
            "risk_assessment": {
                "safety_indicators": self._get_safety_indicators(risk_level),
                "confidence_meter": self._calculate_confidence_level(risk_level),
                "reversibility_info": True
            },
            "stress_management": {
                "breathing_exercises": True,
                "calming_interface": True,
                "emergency_stop_button": True
            },
            "reassurance_features": {
                "expert_validation": True,
                "peer_support_available": True,
                "legal_compliance_confirmed": True
            },
            "control_options": {
                "undo_capability": True,
                "pause_at_any_time": True,
                "rollback_options": True
            }
        }
    
    async def get_ocd_support(self, user_id: str, task_phase: str) -> Dict[str, Any]:
        """Provide OCD-specific accommodations"""
        return {
            "verification_checklists": self._generate_verification_checklist(task_phase),
            "completion_confirmations": {
                "step_confirmations": True,
                "visual_completion_indicators": True,
                "final_verification_step": True
            },
            "organized_categorization": {
                "clear_file_organization": True,
                "consistent_naming_conventions": True,
                "logical_groupings": True
            },
            "ritual_accommodations": {
                "custom_verification_steps": True,
                "repeated_confirmation_options": True,
                "detailed_audit_trails": True
            }
        }
    
    async def get_ptsd_support(self, user_id: str, current_stress: StressLevel) -> Dict[str, Any]:
        """Provide PTSD-sensitive support"""
        return {
            "gentle_notifications": {
                "soft_alerts": True,
                "gradual_escalation": True,
                "user_controlled_timing": True
            },
            "stress_monitoring": {
                "current_level": current_stress.value,
                "recommended_actions": self._get_stress_recommendations(current_stress),
                "break_suggestions": self._get_break_suggestions(current_stress)
            },
            "trauma_informed_design": {
                "avoid_sudden_changes": True,
                "user_agency_prioritized": True,
                "safe_exit_options": True
            },
            "grounding_techniques": {
                "breathing_exercises": True,
                "mindfulness_prompts": True,
                "reality_anchoring": True
            }
        }
    
    def _break_down_task(self, task: str) -> List[Dict[str, Any]]:
        """Break down complex tasks into ADHD-friendly steps"""
        # Simplified task breakdown - would be more sophisticated in real implementation
        steps = [
            {"step": 1, "description": f"Prepare for {task}", "estimated_time": 5, "difficulty": "easy"},
            {"step": 2, "description": f"Execute {task}", "estimated_time": 20, "difficulty": "medium"},
            {"step": 3, "description": f"Verify {task} completion", "estimated_time": 5, "difficulty": "easy"}
        ]
        return steps
    
    def _estimate_task_time(self, task: str) -> int:
        """Estimate task completion time"""
        # Simplified estimation - would use ML or historical data
        base_time = 30  # minutes
        if "scan" in task.lower():
            return base_time * 2
        elif "report" in task.lower():
            return base_time * 3
        return base_time
    
    def _explain_workflow_step(self, stage: str) -> str:
        """Explain why a workflow step is necessary"""
        explanations = {
            "authorization": "This step ensures we have legal permission to test the target systems",
            "reconnaissance": "This step gathers information about the target to plan our testing approach",
            "scanning": "This step identifies potential entry points and vulnerabilities",
            "exploitation": "This step tests whether identified vulnerabilities can be exploited",
            "reporting": "This step documents our findings for the client"
        }
        return explanations.get(stage, "This step is part of the standard penetration testing methodology")
    
    def _get_next_steps(self, current_stage: str) -> List[str]:
        """Get upcoming steps in the workflow"""
        workflow = ["authorization", "reconnaissance", "scanning", "exploitation", "reporting"]
        try:
            current_index = workflow.index(current_stage)
            return workflow[current_index + 1:current_index + 3]
        except ValueError:
            return []
    
    def _get_expected_outcomes(self, stage: str) -> List[str]:
        """Get expected outcomes for a workflow stage"""
        outcomes = {
            "authorization": ["Signed authorization document", "Scope agreement", "Legal compliance confirmation"],
            "reconnaissance": ["Target system inventory", "Technology stack identification", "Attack surface mapping"],
            "scanning": ["Open ports list", "Service versions", "Potential vulnerabilities"],
            "exploitation": ["Proof of concept", "Impact assessment", "Access level determination"],
            "reporting": ["Executive summary", "Technical findings", "Remediation recommendations"]
        }
        return outcomes.get(stage, [])
    
    def _get_safety_indicators(self, risk_level: str) -> Dict[str, Any]:
        """Generate safety indicators for anxiety management"""
        indicators = {
            "low": {"color": "green", "message": "This activity is considered safe", "confidence": 95},
            "medium": {"color": "yellow", "message": "This activity has minimal risks", "confidence": 80},
            "high": {"color": "orange", "message": "This activity requires caution", "confidence": 60},
            "critical": {"color": "red", "message": "This activity has significant risks", "confidence": 40}
        }
        return indicators.get(risk_level, indicators["medium"])
    
    def _calculate_confidence_level(self, risk_level: str) -> int:
        """Calculate confidence level percentage"""
        confidence_map = {"low": 95, "medium": 80, "high": 60, "critical": 40}
        return confidence_map.get(risk_level, 80)
    
    def _generate_verification_checklist(self, phase: str) -> List[Dict[str, Any]]:
        """Generate OCD-friendly verification checklist"""
        checklists = {
            "pre_scan": [
                {"item": "Authorization document verified", "required": True, "completed": False},
                {"item": "Target systems confirmed", "required": True, "completed": False},
                {"item": "Scanning tools configured", "required": True, "completed": False},
                {"item": "Backup procedures in place", "required": False, "completed": False}
            ],
            "post_scan": [
                {"item": "All results saved", "required": True, "completed": False},
                {"item": "False positives filtered", "required": True, "completed": False},
                {"item": "Critical findings flagged", "required": True, "completed": False},
                {"item": "Scan logs archived", "required": False, "completed": False}
            ]
        }
        return checklists.get(phase, [])
    
    def _get_stress_recommendations(self, stress_level: StressLevel) -> List[str]:
        """Get stress-level appropriate recommendations"""
        recommendations = {
            StressLevel.LOW: ["Continue with current pace", "Consider tackling challenging tasks"],
            StressLevel.NORMAL: ["Maintain regular breaks", "Stay hydrated"],
            StressLevel.ELEVATED: ["Take a 5-minute break", "Practice deep breathing"],
            StressLevel.HIGH: ["Step away for 15 minutes", "Consider postponing non-critical tasks"],
            StressLevel.CRITICAL: ["Stop current activity", "Seek immediate support", "Consider ending session"]
        }
        return recommendations.get(stress_level, recommendations[StressLevel.NORMAL])
    
    def _get_break_suggestions(self, stress_level: StressLevel) -> Dict[str, Any]:
        """Get appropriate break suggestions"""
        if stress_level in [StressLevel.HIGH, StressLevel.CRITICAL]:
            return {
                "duration": 15,
                "activities": ["Walk away from computer", "Deep breathing", "Call support person"],
                "mandatory": True
            }
        elif stress_level == StressLevel.ELEVATED:
            return {
                "duration": 5,
                "activities": ["Stretch", "Drink water", "Look away from screen"],
                "mandatory": False
            }
        else:
            return {
                "duration": 2,
                "activities": ["Blink exercises", "Shoulder rolls"],
                "mandatory": False
            }
    
    async def monitor_stress_level(self, user_id: str, biometric_data: Dict[str, Any] = None) -> StressLevel:
        """Monitor user stress level using biometric and behavioral data"""
        if user_id not in self.stress_monitors:
            self.stress_monitors[user_id] = []
        
        # In a real implementation, this would analyze:
        # - Heart rate variability
        # - Typing patterns
        # - Mouse movement patterns
        # - Task completion rates
        # - Error frequencies
        
        # For now, return a simulated stress level
        current_time = datetime.utcnow()
        session_duration = self._get_session_duration(user_id, current_time)
        
        if session_duration > 120:  # 2 hours
            return StressLevel.ELEVATED
        elif session_duration > 180:  # 3 hours
            return StressLevel.HIGH
        else:
            return StressLevel.NORMAL
    
    def _get_session_duration(self, user_id: str, current_time: datetime) -> int:
        """Get current session duration in minutes"""
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {"start_time": current_time}
            return 0
        
        start_time = self.user_sessions[user_id]["start_time"]
        duration = (current_time - start_time).total_seconds() / 60
        return int(duration)


# Global neurodivergent support instance
neurodivergent_support = NeurodivergentSupport()