"""
AI Integration Service for NeuroDemon

Provides intelligent guidance, automated analysis, and natural language
interaction for penetration testing activities.
"""

import asyncio
import json
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum
import httpx
from loguru import logger

from app.core.config import settings, get_ai_headers


class AIModelType(Enum):
    """AI model types for different tasks"""
    CHAT = "chat"
    IMAGE_GENERATION = "image"
    VIDEO_GENERATION = "video"
    CODE_ANALYSIS = "code"


class ConfidenceLevel(Enum):
    """AI confidence levels for recommendations"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class AIService:
    """
    Comprehensive AI service for penetration testing guidance
    
    Features:
    - Natural language query processing
    - Automated tool selection
    - Intelligent report generation
    - Context-aware suggestions
    - Neurodivergent-friendly explanations
    - Risk assessment assistance
    """
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=settings.AI_TIMEOUT)
        self.conversation_history: Dict[str, List[Dict]] = {}
        self.system_prompts = self._initialize_system_prompts()
    
    def _initialize_system_prompts(self) -> Dict[str, str]:
        """Initialize system prompts for different AI tasks"""
        return {
            "pentesting_guide": """
            You are NeuroAI, an expert penetration testing assistant designed to be neurodivergent-friendly.
            
            Your core principles:
            - Provide clear, step-by-step explanations
            - Break down complex tasks into manageable steps
            - Use consistent terminology and structure
            - Include confidence levels for all recommendations
            - Prioritize safety and legal compliance
            - Accommodate different learning and processing styles
            
            For ADHD users: Use bullet points, highlight key actions, provide time estimates
            For autism users: Be precise, avoid ambiguity, explain reasoning behind recommendations
            For anxiety management: Include risk assessments, provide reassurance about safety
            For OCD accommodations: Include verification steps and completion confirmations
            
            Always start responses with a brief summary, then provide detailed steps.
            Include warnings for potentially risky activities.
            Suggest breaks and focus management techniques when appropriate.
            """,
            
            "vulnerability_analysis": """
            You are a cybersecurity vulnerability analyst specializing in clear, actionable reporting.
            
            Analyze vulnerabilities with:
            - Clear severity ratings (Critical/High/Medium/Low)
            - Step-by-step remediation instructions
            - Business impact explanations
            - Technical details appropriate for the audience
            - Timelines for fixes
            - Verification steps
            
            Present findings in a structured, easy-to-follow format.
            Use neurodivergent-friendly language: clear, direct, well-organized.
            """,
            
            "tool_selection": """
            You are a penetration testing tool recommendation engine.
            
            Consider:
            - Target system characteristics
            - User skill level and preferences
            - Legal and ethical constraints
            - Time and resource limitations
            - Neurodivergent accessibility needs
            
            Recommend tools with:
            - Clear justification for selection
            - Setup and usage instructions
            - Expected outcomes
            - Safety considerations
            - Alternative options
            """,
            
            "report_generation": """
            You are an expert technical writer specializing in cybersecurity reports.
            
            Create reports that are:
            - Executive summary friendly
            - Technically accurate
            - Actionable and clear
            - Neurodivergent accessible
            - Legally compliant
            
            Structure reports with clear sections, visual hierarchy, and logical flow.
            Include both technical details and business impact.
            """
        }
    
    async def query_ai(
        self,
        message: str,
        context: str = "pentesting_guide",
        user_id: str = None,
        conversation_id: str = None,
        include_history: bool = True
    ) -> Dict[str, Any]:
        """
        Send query to AI service with context preservation
        
        Args:
            message: User's question or request
            context: Context type for system prompt selection
            user_id: User identifier for personalization
            conversation_id: Conversation identifier for history
            include_history: Whether to include conversation history
            
        Returns:
            AI response with metadata
        """
        try:
            logger.info(f"🤖 Processing AI query: {message[:100]}...")
            
            # Prepare conversation history
            history = []
            if include_history and conversation_id:
                history = self.conversation_history.get(conversation_id, [])
            
            # Build messages
            messages = [
                {"role": "system", "content": self.system_prompts.get(context, self.system_prompts["pentesting_guide"])}
            ]
            
            # Add conversation history
            messages.extend(history[-10:])  # Keep last 10 messages for context
            
            # Add current message
            messages.append({"role": "user", "content": message})
            
            # Prepare request
            request_data = {
                "model": settings.AI_DEFAULT_MODEL,
                "messages": messages,
                "max_tokens": settings.AI_MAX_TOKENS,
                "temperature": 0.3,  # Lower temperature for more consistent responses
                "top_p": 0.9
            }
            
            # Make API call
            response = await self.client.post(
                settings.AI_API_ENDPOINT,
                headers=get_ai_headers(),
                json=request_data
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Extract AI response
            ai_response = result["choices"][0]["message"]["content"]
            
            # Update conversation history
            if conversation_id:
                if conversation_id not in self.conversation_history:
                    self.conversation_history[conversation_id] = []
                
                self.conversation_history[conversation_id].extend([
                    {"role": "user", "content": message},
                    {"role": "assistant", "content": ai_response}
                ])
            
            # Analyze response for confidence and key information
            analysis = self._analyze_response(ai_response)
            
            return {
                "response": ai_response,
                "confidence": analysis["confidence"],
                "key_points": analysis["key_points"],
                "warnings": analysis["warnings"],
                "next_steps": analysis["next_steps"],
                "context": context,
                "timestamp": datetime.utcnow(),
                "conversation_id": conversation_id,
                "token_usage": result.get("usage", {}),
                "model_used": settings.AI_DEFAULT_MODEL
            }
            
        except httpx.HTTPStatusError as e:
            logger.error(f"❌ AI API error: {e.response.status_code} - {e.response.text}")
            return {
                "error": f"AI service error: {e.response.status_code}",
                "response": "I'm currently experiencing technical difficulties. Please try again or contact support.",
                "confidence": ConfidenceLevel.LOW.value
            }
        except Exception as e:
            logger.error(f"❌ AI service error: {str(e)}")
            return {
                "error": f"Unexpected error: {str(e)}",
                "response": "I encountered an unexpected error. Please try rephrasing your question.",
                "confidence": ConfidenceLevel.LOW.value
            }
    
    def _analyze_response(self, response: str) -> Dict[str, Any]:
        """Analyze AI response for metadata extraction"""
        analysis = {
            "confidence": ConfidenceLevel.MEDIUM.value,
            "key_points": [],
            "warnings": [],
            "next_steps": []
        }
        
        response_lower = response.lower()
        
        # Detect confidence indicators
        high_confidence_indicators = ["definitely", "certainly", "always", "proven", "established"]
        low_confidence_indicators = ["might", "possibly", "unclear", "depends", "varies"]
        
        if any(indicator in response_lower for indicator in high_confidence_indicators):
            analysis["confidence"] = ConfidenceLevel.HIGH.value
        elif any(indicator in response_lower for indicator in low_confidence_indicators):
            analysis["confidence"] = ConfidenceLevel.LOW.value
        
        # Extract warnings
        warning_indicators = ["warning", "caution", "danger", "risk", "careful", "legal"]
        for line in response.split('\n'):
            if any(indicator in line.lower() for indicator in warning_indicators):
                analysis["warnings"].append(line.strip())
        
        # Extract key points (lines starting with bullet points or numbers)
        for line in response.split('\n'):
            line = line.strip()
            if line.startswith(('•', '-', '*')) or (line and line[0].isdigit() and '.' in line[:3]):
                analysis["key_points"].append(line)
        
        # Extract next steps
        next_step_indicators = ["next", "then", "after", "following", "step"]
        for line in response.split('\n'):
            if any(indicator in line.lower() for indicator in next_step_indicators):
                analysis["next_steps"].append(line.strip())
        
        return analysis
    
    async def recommend_tools(
        self,
        target_info: Dict[str, Any],
        objectives: List[str],
        user_preferences: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Recommend penetration testing tools based on context
        
        Args:
            target_info: Information about target systems
            objectives: Testing objectives
            user_preferences: User skill level and preferences
            
        Returns:
            Tool recommendations with explanations
        """
        if user_preferences is None:
            user_preferences = {}
            
        context_message = f"""
        Target Information:
        - Systems: {target_info.get('systems', [])}
        - Services: {target_info.get('services', [])}
        - OS: {target_info.get('operating_systems', [])}
        - Network: {target_info.get('network_info', {})}
        
        Objectives: {', '.join(objectives)}
        
        User Preferences:
        - Skill Level: {user_preferences.get('skill_level', 'intermediate')}
        - Preferred Tools: {user_preferences.get('preferred_tools', [])}
        - Time Constraints: {user_preferences.get('time_limit', 'none')}
        
        Please recommend appropriate penetration testing tools for these requirements.
        Include setup instructions and safety considerations.
        """
        
        return await self.query_ai(
            message=context_message,
            context="tool_selection"
        )
    
    async def analyze_vulnerabilities(
        self,
        scan_results: List[Dict[str, Any]],
        context_info: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Analyze vulnerability scan results with AI
        
        Args:
            scan_results: Raw scan results from tools
            context_info: Additional context about the environment
            
        Returns:
            AI analysis of vulnerabilities
        """
        if context_info is None:
            context_info = {}
            
        # Format scan results for AI analysis
        formatted_results = []
        for result in scan_results[:50]:  # Limit to prevent token overflow
            formatted_results.append({
                "host": result.get("host", "unknown"),
                "port": result.get("port", "unknown"),
                "service": result.get("service", "unknown"),
                "vulnerability": result.get("vulnerability", "unknown"),
                "severity": result.get("severity", "unknown"),
                "description": result.get("description", "")[:200]  # Truncate long descriptions
            })
        
        analysis_message = f"""
        Vulnerability Scan Results Analysis:
        
        Context:
        - Environment: {context_info.get('environment', 'unknown')}
        - Business Type: {context_info.get('business_type', 'unknown')}
        - Criticality: {context_info.get('criticality', 'unknown')}
        
        Scan Results ({len(formatted_results)} items):
        {json.dumps(formatted_results, indent=2)}
        
        Please analyze these vulnerabilities and provide:
        1. Risk prioritization
        2. Business impact assessment
        3. Remediation recommendations
        4. Timeline for fixes
        5. Compensating controls if immediate fixes aren't possible
        """
        
        return await self.query_ai(
            message=analysis_message,
            context="vulnerability_analysis"
        )
    
    async def generate_report(
        self,
        findings: List[Dict[str, Any]],
        report_type: str = "executive",
        target_audience: str = "technical"
    ) -> Dict[str, Any]:
        """
        Generate comprehensive penetration testing report
        
        Args:
            findings: List of security findings
            report_type: Type of report (executive, technical, compliance)
            target_audience: Target audience (executive, technical, mixed)
            
        Returns:
            Generated report with structured sections
        """
        # Format findings for report generation
        formatted_findings = []
        for finding in findings:
            formatted_findings.append({
                "title": finding.get("title", "Unknown Finding"),
                "severity": finding.get("severity", "Medium"),
                "description": finding.get("description", ""),
                "impact": finding.get("impact", ""),
                "remediation": finding.get("remediation", ""),
                "affected_systems": finding.get("affected_systems", [])
            })
        
        report_message = f"""
        Generate a {report_type} penetration testing report for {target_audience} audience.
        
        Findings Summary:
        - Total Findings: {len(formatted_findings)}
        - Critical: {sum(1 for f in formatted_findings if f['severity'] == 'Critical')}
        - High: {sum(1 for f in formatted_findings if f['severity'] == 'High')}
        - Medium: {sum(1 for f in formatted_findings if f['severity'] == 'Medium')}
        - Low: {sum(1 for f in formatted_findings if f['severity'] == 'Low')}
        
        Detailed Findings:
        {json.dumps(formatted_findings, indent=2)}
        
        Please generate a comprehensive report with:
        1. Executive Summary
        2. Risk Assessment
        3. Detailed Findings
        4. Recommendations
        5. Next Steps
        
        Format for {target_audience} audience with appropriate technical depth.
        """
        
        return await self.query_ai(
            message=report_message,
            context="report_generation"
        )
    
    async def get_neurodivergent_guidance(
        self,
        user_profile: Dict[str, Any],
        current_task: str,
        stress_level: str = "normal"
    ) -> Dict[str, Any]:
        """
        Provide neurodivergent-specific guidance and support
        
        Args:
            user_profile: User's neurodivergent profile and preferences
            current_task: Current penetration testing task
            stress_level: Current stress level (low, normal, high, critical)
            
        Returns:
            Personalized guidance and recommendations
        """
        guidance_message = f"""
        Provide neurodivergent-friendly guidance for the current situation:
        
        User Profile:
        - Neurodivergent traits: {user_profile.get('traits', [])}
        - Preferred communication style: {user_profile.get('communication_style', 'direct')}
        - Stress management needs: {user_profile.get('stress_management', [])}
        - Focus management preferences: {user_profile.get('focus_preferences', [])}
        
        Current Situation:
        - Task: {current_task}
        - Stress Level: {stress_level}
        - Time of day: {datetime.now().strftime('%H:%M')}
        
        Please provide:
        1. Task breakdown and organization
        2. Stress management suggestions
        3. Focus techniques
        4. Break recommendations
        5. Motivation and encouragement
        
        Adapt your response style to the user's neurodivergent needs.
        """
        
        return await self.query_ai(
            message=guidance_message,
            context="pentesting_guide"
        )
    
    async def cleanup(self):
        """Cleanup resources"""
        if hasattr(self, 'client'):
            await self.client.aclose()


# Global AI service instance
ai_service = AIService()