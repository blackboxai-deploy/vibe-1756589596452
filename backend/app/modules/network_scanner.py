"""
Network Discovery and Enumeration Module for NeuroDemon

Provides comprehensive network scanning capabilities with nmap integration,
intelligent target discovery, and neurodivergent-friendly progress reporting.
"""

import asyncio
import subprocess
import json
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from enum import Enum
from dataclasses import dataclass
import ipaddress
import socket
from loguru import logger

from app.core.config import settings
from app.ai.service import ai_service


class ScanType(Enum):
    """Types of network scans available"""
    PING_SWEEP = "ping_sweep"
    PORT_SCAN = "port_scan"
    SERVICE_DETECTION = "service_detection"
    OS_DETECTION = "os_detection"
    VULNERABILITY_SCAN = "vulnerability_scan"
    STEALTH_SCAN = "stealth_scan"
    UDP_SCAN = "udp_scan"
    COMPREHENSIVE = "comprehensive"


class ScanIntensity(Enum):
    """Scan intensity levels for different scenarios"""
    LIGHT = "light"        # Minimal, stealthy scanning
    NORMAL = "normal"      # Standard scanning approach
    AGGRESSIVE = "aggressive"  # Comprehensive but noisy
    INSANE = "insane"      # Maximum detail, very noisy


@dataclass
class ScanTarget:
    """Structure for scan targets"""
    target: str
    target_type: str  # ip, hostname, network, url
    ports: Optional[List[int]] = None
    exclude_ports: Optional[List[int]] = None
    description: str = ""


@dataclass
class ScanResult:
    """Structure for scan results"""
    target: str
    scan_type: ScanType
    status: str
    start_time: datetime
    end_time: Optional[datetime]
    results: Dict[str, Any]
    raw_output: str
    errors: List[str]


class NetworkScanner:
    """
    Comprehensive network scanning engine with neurodivergent-friendly features
    
    Features:
    - Multiple scan types and techniques
    - Progress tracking with detailed feedback
    - AI-powered result analysis
    - Rate limiting and safety controls
    - Pause/resume functionality
    - Clear explanations for each scan type
    """
    
    def __init__(self):
        self.active_scans: Dict[str, Dict] = {}
        self.scan_history: List[ScanResult] = []
        self.rate_limiter = RateLimiter(settings.SCAN_RATE_LIMIT)
        
    async def ping_sweep(
        self, 
        network: str, 
        progress_callback: Callable = None,
        user_preferences: Dict[str, Any] = None
    ) -> ScanResult:
        """
        Perform ping sweep to discover live hosts
        
        Args:
            network: Network to scan (e.g., "192.168.1.0/24")
            progress_callback: Callback for progress updates
            user_preferences: User preferences for neurodivergent accommodations
            
        Returns:
            Scan results with discovered hosts
        """
        scan_id = f"ping_sweep_{datetime.now().isoformat()}"
        logger.info(f"🔍 Starting ping sweep of {network}")
        
        # Validate network
        try:
            net = ipaddress.ip_network(network, strict=False)
        except ValueError as e:
            logger.error(f"❌ Invalid network format: {network}")
            return ScanResult(
                target=network,
                scan_type=ScanType.PING_SWEEP,
                status="error",
                start_time=datetime.utcnow(),
                end_time=datetime.utcnow(),
                results={},
                raw_output="",
                errors=[f"Invalid network format: {str(e)}"]
            )
        
        scan_result = ScanResult(
            target=network,
            scan_type=ScanType.PING_SWEEP,
            status="running",
            start_time=datetime.utcnow(),
            end_time=None,
            results={"hosts": []},
            raw_output="",
            errors=[]
        )
        
        self.active_scans[scan_id] = {
            "result": scan_result,
            "paused": False,
            "cancelled": False
        }
        
        try:
            # Build nmap command
            nmap_command = [
                "nmap",
                "-sn",  # Ping sweep only
                "-T4",  # Aggressive timing
                "--max-retries", "1",
                "--host-timeout", "5s",
                str(network)
            ]
            
            # Add stealth options if requested
            if user_preferences and user_preferences.get("stealth_mode", False):
                nmap_command.extend(["-T2", "--max-retries", "0"])
            
            # Execute scan with progress tracking
            if progress_callback:
                await progress_callback(0, f"Starting ping sweep of {network}...")
            
            process = await asyncio.create_subprocess_exec(
                *nmap_command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode().strip()
                logger.error(f"❌ Nmap error: {error_msg}")
                scan_result.status = "error"
                scan_result.errors.append(error_msg)
            else:
                # Parse nmap output
                raw_output = stdout.decode()
                scan_result.raw_output = raw_output
                
                # Extract discovered hosts
                hosts = self._parse_ping_sweep_results(raw_output)
                scan_result.results["hosts"] = hosts
                scan_result.status = "completed"
                
                logger.info(f"✅ Ping sweep completed: {len(hosts)} hosts discovered")
                
                if progress_callback:
                    await progress_callback(100, f"Completed: {len(hosts)} hosts discovered")
        
        except Exception as e:
            logger.error(f"❌ Ping sweep failed: {str(e)}")
            scan_result.status = "error"
            scan_result.errors.append(str(e))
        
        finally:
            scan_result.end_time = datetime.utcnow()
            self.scan_history.append(scan_result)
            if scan_id in self.active_scans:
                del self.active_scans[scan_id]
        
        return scan_result
    
    async def port_scan(
        self,
        targets: List[ScanTarget],
        scan_type: str = "tcp_connect",
        intensity: ScanIntensity = ScanIntensity.NORMAL,
        progress_callback: Callable = None,
        user_preferences: Dict[str, Any] = None
    ) -> List[ScanResult]:
        """
        Perform port scanning on specified targets
        
        Args:
            targets: List of targets to scan
            scan_type: Type of port scan (tcp_connect, syn, udp, etc.)
            intensity: Scan intensity level
            progress_callback: Callback for progress updates
            user_preferences: User preferences for accommodations
            
        Returns:
            List of scan results for each target
        """
        scan_id = f"port_scan_{datetime.now().isoformat()}"
        logger.info(f"🔍 Starting port scan of {len(targets)} targets")
        
        results = []
        total_targets = len(targets)
        
        for i, target in enumerate(targets):
            if progress_callback:
                progress = int((i / total_targets) * 100)
                await progress_callback(progress, f"Scanning {target.target}...")
            
            # Check for pause/cancel requests
            if scan_id in self.active_scans:
                if self.active_scans[scan_id].get("cancelled", False):
                    logger.info("🛑 Port scan cancelled by user")
                    break
                
                while self.active_scans[scan_id].get("paused", False):
                    await asyncio.sleep(1)
            
            # Rate limiting
            await self.rate_limiter.wait()
            
            scan_result = await self._scan_single_target(target, scan_type, intensity)
            results.append(scan_result)
            
            # Provide neurodivergent-friendly updates
            if user_preferences and user_preferences.get("detailed_feedback", True):
                open_ports = len([p for p in scan_result.results.get("ports", []) if p.get("state") == "open"])
                logger.info(f"📊 {target.target}: {open_ports} open ports found")
        
        if progress_callback:
            await progress_callback(100, f"Port scanning completed: {len(results)} targets scanned")
        
        return results
    
    async def _scan_single_target(
        self,
        target: ScanTarget,
        scan_type: str,
        intensity: ScanIntensity
    ) -> ScanResult:
        """Scan a single target"""
        start_time = datetime.utcnow()
        
        try:
            # Build nmap command based on scan type and intensity
            nmap_command = self._build_nmap_command(target, scan_type, intensity)
            
            # Execute scan
            process = await asyncio.create_subprocess_exec(
                *nmap_command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode().strip()
                return ScanResult(
                    target=target.target,
                    scan_type=ScanType.PORT_SCAN,
                    status="error",
                    start_time=start_time,
                    end_time=datetime.utcnow(),
                    results={},
                    raw_output="",
                    errors=[error_msg]
                )
            
            # Parse results
            raw_output = stdout.decode()
            parsed_results = self._parse_port_scan_results(raw_output)
            
            return ScanResult(
                target=target.target,
                scan_type=ScanType.PORT_SCAN,
                status="completed",
                start_time=start_time,
                end_time=datetime.utcnow(),
                results=parsed_results,
                raw_output=raw_output,
                errors=[]
            )
            
        except Exception as e:
            logger.error(f"❌ Scan failed for {target.target}: {str(e)}")
            return ScanResult(
                target=target.target,
                scan_type=ScanType.PORT_SCAN,
                status="error",
                start_time=start_time,
                end_time=datetime.utcnow(),
                results={},
                raw_output="",
                errors=[str(e)]
            )
    
    def _build_nmap_command(
        self, 
        target: ScanTarget, 
        scan_type: str, 
        intensity: ScanIntensity
    ) -> List[str]:
        """Build nmap command based on parameters"""
        command = ["nmap"]
        
        # Scan type options
        scan_type_map = {
            "tcp_connect": ["-sT"],
            "tcp_syn": ["-sS"],
            "udp": ["-sU"],
            "stealth": ["-sS", "-f"],  # Fragmented packets
            "version": ["-sV"],
            "os": ["-O"],
            "comprehensive": ["-sS", "-sV", "-O", "-A"]
        }
        
        command.extend(scan_type_map.get(scan_type, ["-sT"]))
        
        # Intensity options
        intensity_map = {
            ScanIntensity.LIGHT: ["-T1", "--max-retries", "1"],
            ScanIntensity.NORMAL: ["-T3", "--max-retries", "2"],
            ScanIntensity.AGGRESSIVE: ["-T4", "--max-retries", "3"],
            ScanIntensity.INSANE: ["-T5", "--max-retries", "5"]
        }
        
        command.extend(intensity_map.get(intensity, intensity_map[ScanIntensity.NORMAL]))
        
        # Port specification
        if target.ports:
            ports_str = ",".join(map(str, target.ports))
            command.extend(["-p", ports_str])
        
        # Output format
        command.extend(["-oX", "-"])  # XML output to stdout
        
        # Target
        command.append(target.target)
        
        return command
    
    def _parse_ping_sweep_results(self, nmap_output: str) -> List[Dict[str, Any]]:
        """Parse ping sweep results from nmap output"""
        hosts = []
        
        for line in nmap_output.split('\n'):
            if "Nmap scan report for" in line:
                # Extract host information
                parts = line.split()
                if len(parts) >= 5:
                    hostname = parts[4]
                    ip = parts[5].strip('()')
                    hosts.append({
                        "ip": ip,
                        "hostname": hostname if hostname != ip else None,
                        "status": "up"
                    })
                else:
                    # Just IP address
                    ip = parts[4]
                    hosts.append({
                        "ip": ip,
                        "hostname": None,
                        "status": "up"
                    })
        
        return hosts
    
    def _parse_port_scan_results(self, xml_output: str) -> Dict[str, Any]:
        """Parse port scan results from nmap XML output"""
        try:
            root = ET.fromstring(xml_output)
            results = {
                "ports": [],
                "host_info": {},
                "services": []
            }
            
            for host in root.findall("host"):
                # Host information
                for address in host.findall("address"):
                    if address.get("addrtype") == "ipv4":
                        results["host_info"]["ip"] = address.get("addr")
                
                # Port information
                for ports in host.findall("ports"):
                    for port in ports.findall("port"):
                        port_info = {
                            "port": int(port.get("portid")),
                            "protocol": port.get("protocol"),
                            "state": port.find("state").get("state"),
                            "service": None,
                            "version": None
                        }
                        
                        # Service information
                        service = port.find("service")
                        if service is not None:
                            port_info["service"] = service.get("name")
                            port_info["version"] = service.get("version")
                            port_info["product"] = service.get("product")
                        
                        results["ports"].append(port_info)
                        
                        # Add to services list
                        if port_info["service"]:
                            results["services"].append({
                                "port": port_info["port"],
                                "service": port_info["service"],
                                "version": port_info["version"],
                                "product": port_info["product"]
                            })
            
            return results
            
        except ET.ParseError as e:
            logger.error(f"❌ Failed to parse nmap XML output: {str(e)}")
            # Fallback to text parsing
            return self._parse_port_scan_text(xml_output)
    
    def _parse_port_scan_text(self, text_output: str) -> Dict[str, Any]:
        """Fallback text parsing for port scan results"""
        results = {"ports": [], "host_info": {}, "services": []}
        
        lines = text_output.split('\n')
        for line in lines:
            line = line.strip()
            
            # Extract open ports
            if "/tcp" in line and ("open" in line or "filtered" in line):
                parts = line.split()
                if len(parts) >= 2:
                    port_proto = parts[0]
                    port_num = port_proto.split('/')[0]
                    state = parts[1]
                    service = parts[2] if len(parts) > 2 else "unknown"
                    
                    port_info = {
                        "port": int(port_num),
                        "protocol": "tcp",
                        "state": state,
                        "service": service,
                        "version": None
                    }
                    
                    results["ports"].append(port_info)
                    if service != "unknown":
                        results["services"].append({
                            "port": int(port_num),
                            "service": service,
                            "version": None,
                            "product": None
                        })
        
        return results
    
    async def analyze_scan_results(
        self, 
        scan_results: List[ScanResult],
        user_context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Use AI to analyze scan results and provide intelligent insights
        
        Args:
            scan_results: List of scan results to analyze
            user_context: Additional context about user and environment
            
        Returns:
            AI analysis with recommendations and insights
        """
        logger.info(f"🤖 Analyzing {len(scan_results)} scan results with AI")
        
        # Prepare data for AI analysis
        analysis_data = {
            "total_targets": len(scan_results),
            "successful_scans": len([r for r in scan_results if r.status == "completed"]),
            "failed_scans": len([r for r in scan_results if r.status == "error"]),
            "findings_summary": {}
        }
        
        all_ports = []
        all_services = []
        
        for result in scan_results:
            if result.status == "completed" and "ports" in result.results:
                for port in result.results["ports"]:
                    if port.get("state") == "open":
                        all_ports.append({
                            "target": result.target,
                            "port": port["port"],
                            "service": port.get("service", "unknown"),
                            "protocol": port.get("protocol", "tcp")
                        })
                        
                        if port.get("service") and port["service"] != "unknown":
                            all_services.append(port["service"])
        
        analysis_data["open_ports"] = len(all_ports)
        analysis_data["unique_services"] = len(set(all_services))
        analysis_data["common_services"] = list(set(all_services))
        
        # Get AI analysis
        ai_query = f"""
        Analyze these network scan results and provide insights:
        
        Scan Summary:
        - Total targets scanned: {analysis_data['total_targets']}
        - Successful scans: {analysis_data['successful_scans']}
        - Failed scans: {analysis_data['failed_scans']}
        - Total open ports found: {analysis_data['open_ports']}
        - Unique services identified: {analysis_data['unique_services']}
        - Common services: {', '.join(analysis_data['common_services'][:10])}
        
        Top findings:
        {json.dumps(all_ports[:20], indent=2)}
        
        Please provide:
        1. Risk assessment of discovered services
        2. Recommended next steps for penetration testing
        3. Potential security concerns
        4. Prioritized targets for further investigation
        5. ADHD-friendly task breakdown for follow-up actions
        """
        
        ai_response = await ai_service.query_ai(
            message=ai_query,
            context="vulnerability_analysis"
        )
        
        return {
            "scan_summary": analysis_data,
            "ai_analysis": ai_response,
            "recommended_actions": self._generate_recommended_actions(all_ports, all_services),
            "risk_assessment": self._assess_scan_risks(all_ports, all_services)
        }
    
    def _generate_recommended_actions(
        self, 
        open_ports: List[Dict], 
        services: List[str]
    ) -> List[Dict[str, Any]]:
        """Generate recommended follow-up actions"""
        actions = []
        
        # High-risk service detection
        high_risk_services = ["ftp", "telnet", "ssh", "smtp", "http", "https", "smb", "rdp"]
        found_high_risk = [s for s in services if s in high_risk_services]
        
        if found_high_risk:
            actions.append({
                "priority": "high",
                "action": "Service Enumeration",
                "description": f"Perform detailed enumeration of high-risk services: {', '.join(found_high_risk)}",
                "estimated_time": 30,
                "difficulty": "medium",
                "tools": ["nmap", "enum4linux", "nikto"]
            })
        
        # Web services
        web_ports = [p for p in open_ports if p["port"] in [80, 443, 8080, 8443]]
        if web_ports:
            actions.append({
                "priority": "medium",
                "action": "Web Application Testing",
                "description": f"Test web applications on {len(web_ports)} ports",
                "estimated_time": 60,
                "difficulty": "medium",
                "tools": ["burp suite", "nikto", "dirb"]
            })
        
        # Database services
        db_services = ["mysql", "postgresql", "mssql", "oracle"]
        found_db = [s for s in services if s in db_services]
        if found_db:
            actions.append({
                "priority": "high",
                "action": "Database Assessment",
                "description": f"Assess database security: {', '.join(found_db)}",
                "estimated_time": 45,
                "difficulty": "advanced",
                "tools": ["sqlmap", "nmap"]
            })
        
        return sorted(actions, key=lambda x: {"high": 3, "medium": 2, "low": 1}[x["priority"]], reverse=True)
    
    def _assess_scan_risks(
        self, 
        open_ports: List[Dict], 
        services: List[str]
    ) -> Dict[str, Any]:
        """Assess security risks from scan results"""
        risk_score = 0
        risk_factors = []
        
        # High-risk ports
        high_risk_ports = [21, 23, 135, 139, 445, 1433, 3389]
        found_high_risk_ports = [p for p in open_ports if p["port"] in high_risk_ports]
        
        if found_high_risk_ports:
            risk_score += len(found_high_risk_ports) * 20
            risk_factors.append(f"{len(found_high_risk_ports)} high-risk ports detected")
        
        # Excessive open ports
        if len(open_ports) > 50:
            risk_score += 30
            risk_factors.append("Large attack surface (50+ open ports)")
        
        # Unencrypted services
        unencrypted_services = ["ftp", "telnet", "http", "smtp"]
        found_unencrypted = [s for s in services if s in unencrypted_services]
        if found_unencrypted:
            risk_score += len(found_unencrypted) * 15
            risk_factors.append(f"Unencrypted services: {', '.join(found_unencrypted)}")
        
        # Determine overall risk level
        if risk_score >= 100:
            risk_level = "critical"
        elif risk_score >= 70:
            risk_level = "high"
        elif risk_score >= 40:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        return {
            "risk_level": risk_level,
            "risk_score": min(risk_score, 100),
            "risk_factors": risk_factors,
            "total_open_ports": len(open_ports),
            "unique_services": len(set(services))
        }
    
    async def pause_scan(self, scan_id: str) -> bool:
        """Pause an active scan"""
        if scan_id in self.active_scans:
            self.active_scans[scan_id]["paused"] = True
            logger.info(f"⏸️ Scan {scan_id} paused")
            return True
        return False
    
    async def resume_scan(self, scan_id: str) -> bool:
        """Resume a paused scan"""
        if scan_id in self.active_scans:
            self.active_scans[scan_id]["paused"] = False
            logger.info(f"▶️ Scan {scan_id} resumed")
            return True
        return False
    
    async def cancel_scan(self, scan_id: str) -> bool:
        """Cancel an active scan"""
        if scan_id in self.active_scans:
            self.active_scans[scan_id]["cancelled"] = True
            logger.info(f"🛑 Scan {scan_id} cancelled")
            return True
        return False


class RateLimiter:
    """Simple rate limiter for scan requests"""
    
    def __init__(self, requests_per_minute: int):
        self.requests_per_minute = requests_per_minute
        self.request_times = []
    
    async def wait(self):
        """Wait if necessary to respect rate limits"""
        now = datetime.utcnow()
        
        # Remove old requests (older than 1 minute)
        cutoff = now - timedelta(minutes=1)
        self.request_times = [t for t in self.request_times if t > cutoff]
        
        # Check if we need to wait
        if len(self.request_times) >= self.requests_per_minute:
            # Calculate wait time
            oldest_request = min(self.request_times)
            wait_until = oldest_request + timedelta(minutes=1)
            wait_seconds = (wait_until - now).total_seconds()
            
            if wait_seconds > 0:
                logger.info(f"⏳ Rate limiting: waiting {wait_seconds:.1f} seconds")
                await asyncio.sleep(wait_seconds)
        
        # Record this request
        self.request_times.append(now)


# Global network scanner instance
network_scanner = NetworkScanner()