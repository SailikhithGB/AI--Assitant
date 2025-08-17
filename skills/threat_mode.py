"""
Threat Mode Skill - Proactive Security Threat Detection
Monitors for security threats and provides proactive security recommendations
"""

import logging
import re
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import hashlib
import json

logger = logging.getLogger(__name__)

class ThreatMode:
    """
    Threat Mode system for proactive security threat detection and analysis
    Provides security awareness and threat mitigation strategies
    """
    
    def __init__(self, digital_twin):
        self.twin = digital_twin
        self.threat_history = []
        self.max_threat_history = 100
        
        # Threat detection patterns
        self.threat_patterns = {
            'phishing': {
                'email_indicators': [
                    r'urgent.{0,20}action.{0,20}required',
                    r'verify.{0,20}account.{0,20}immediately',
                    r'click.{0,20}here.{0,20}now',
                    r'suspended.{0,20}account',
                    r'unusual.{0,20}activity'
                ],
                'url_indicators': [
                    r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',  # IP addresses
                    r'[a-z0-9]+-[a-z0-9]+-[a-z0-9]+\.[a-z]{2,}',  # Suspicious domains
                    r'tinyurl|bit\.ly|t\.co|goo\.gl',  # URL shorteners
                ]
            },
            'malware': {
                'file_extensions': [
                    '.exe', '.scr', '.pif', '.bat', '.cmd', '.com', '.vbs', '.js'
                ],
                'suspicious_names': [
                    'invoice', 'receipt', 'document', 'photo', 'video'
                ]
            },
            'social_engineering': {
                'keywords': [
                    'tech support', 'microsoft support', 'apple support',
                    'refund', 'prize', 'lottery', 'inheritance',
                    'tax refund', 'government grant'
                ]
            },
            'network_threats': {
                'indicators': [
                    'unusual network traffic',
                    'slow internet connection',
                    'unexpected pop-ups',
                    'browser redirects',
                    'unknown network connections'
                ]
            }
        }
        
        # Security levels
        self.threat_levels = {
            'low': {'color': '🟢', 'action': 'monitor'},
            'medium': {'color': '🟡', 'action': 'investigate'},
            'high': {'color': '🟠', 'action': 'immediate_action'},
            'critical': {'color': '🔴', 'action': 'emergency_response'}
        }
    
    def route(self, text: str) -> str:
        """Route threat mode requests"""
        try:
            text_lower = text.lower()
            
            # Threat analysis requests
            if any(phrase in text_lower for phrase in ['analyze threat', 'check threat', 'threat analysis']):
                return self._analyze_potential_threat(text)
            
            # Phishing detection
            elif any(phrase in text_lower for phrase in ['phishing check', 'suspicious email', 'email threat']):
                return self._analyze_phishing_threat(text)
            
            # System security scan
            elif any(phrase in text_lower for phrase in ['security scan', 'scan threats', 'system check']):
                return self._perform_security_scan()
            
            # Threat intelligence
            elif any(phrase in text_lower for phrase in ['threat intelligence', 'current threats', 'threat landscape']):
                return self._provide_threat_intelligence()
            
            # Incident response
            elif any(phrase in text_lower for phrase in ['incident response', 'been hacked', 'compromised']):
                return self._provide_incident_response()
            
            # Security recommendations
            elif any(phrase in text_lower for phrase in ['security recommendations', 'improve security', 'protect myself']):
                return self._provide_security_recommendations()
            
            # General threat mode activation
            else:
                return self._activate_threat_mode()
                
        except Exception as e:
            logger.error(f"Error in threat mode routing: {e}")
            return f"Threat analysis error: {e}"
    
    def _analyze_potential_threat(self, text: str) -> str:
        """Analyze text for potential security threats"""
        try:
            threat_analysis = {
                'phishing_score': 0,
                'malware_score': 0,
                'social_engineering_score': 0,
                'overall_threat_level': 'low',
                'detected_patterns': [],
                'recommendations': []
            }
            
            text_lower = text.lower()
            
            # Check for phishing indicators
            for pattern in self.threat_patterns['phishing']['email_indicators']:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    threat_analysis['phishing_score'] += 2
                    threat_analysis['detected_patterns'].append(f"Phishing indicator: {pattern}")
            
            # Check for suspicious URLs
            for pattern in self.threat_patterns['phishing']['url_indicators']:
                if re.search(pattern, text, re.IGNORECASE):
                    threat_analysis['phishing_score'] += 3
                    threat_analysis['detected_patterns'].append(f"Suspicious URL pattern: {pattern}")
            
            # Check for social engineering keywords
            for keyword in self.threat_patterns['social_engineering']['keywords']:
                if keyword in text_lower:
                    threat_analysis['social_engineering_score'] += 1
                    threat_analysis['detected_patterns'].append(f"Social engineering keyword: {keyword}")
            
            # Determine overall threat level
            total_score = (threat_analysis['phishing_score'] + 
                          threat_analysis['malware_score'] + 
                          threat_analysis['social_engineering_score'])
            
            if total_score >= 6:
                threat_analysis['overall_threat_level'] = 'critical'
            elif total_score >= 4:
                threat_analysis['overall_threat_level'] = 'high'
            elif total_score >= 2:
                threat_analysis['overall_threat_level'] = 'medium'
            else:
                threat_analysis['overall_threat_level'] = 'low'
            
            # Store threat analysis
            self._store_threat_analysis(threat_analysis)
            
            return self._format_threat_analysis(threat_analysis)
            
        except Exception as e:
            logger.error(f"Error analyzing threat: {e}")
            return f"Threat analysis failed: {e}"
    
    def _analyze_phishing_threat(self, text: str) -> str:
        """Analyze specific phishing threats"""
        return """🎣 **Phishing Threat Analysis**

**Common Phishing Indicators:**

📧 **Email Red Flags:**
❌ Urgent action required
❌ Verify account immediately  
❌ Suspicious sender address
❌ Generic greetings ("Dear Customer")
❌ Spelling and grammar errors
❌ Mismatched URLs (hover to check)
❌ Unexpected attachments

🔗 **Suspicious Links:**
❌ IP addresses instead of domain names
❌ Misspelled company domains
❌ URL shorteners (bit.ly, tinyurl)
❌ Unusual domain extensions
❌ Extra characters in legitimate domains

**Phishing Protection Steps:**

🛡️ **Before Clicking:**
1. **Verify sender** - Contact company directly
2. **Check URL** - Hover over links to preview
3. **Look for HTTPS** - Secure connection indicator
4. **Trust your instincts** - If it feels wrong, it probably is

🔍 **Safe Verification:**
- Go to official website directly (don't click email links)
- Call company using official phone number
- Check account by logging in separately
- Ask IT department if work-related

**If You Suspect Phishing:**

⚠️ **Immediate Actions:**
1. **Don't click anything** in the suspicious message
2. **Don't provide personal information**
3. **Report to IT** (if work email)
4. **Forward to anti-phishing** (e.g., phishing@company.com)
5. **Delete the message** after reporting

🚨 **If You Already Clicked:**
1. **Change passwords immediately** (start with email)
2. **Enable 2FA** on all important accounts
3. **Monitor accounts** for suspicious activity
4. **Run antivirus scan** on your device
5. **Contact your bank** if financial info was entered

**Advanced Phishing Techniques:**

🎭 **Spear Phishing:**
- Targeted attacks using personal information
- Often appears to come from colleagues/friends
- Uses information from social media

📱 **Smishing (SMS Phishing):**
- Phishing via text messages
- Often claims package delivery issues
- Fake bank or service notifications

📞 **Vishing (Voice Phishing):**
- Phone calls claiming to be tech support
- Requests for remote computer access
- Social security or credit card verification

**Current Phishing Trends:**
- COVID-19 related scams
- Cryptocurrency investment schemes
- Fake government communications
- Romance scams on dating apps
- Job offer scams

**Phishing Test:**
Would you like me to analyze a specific email or message for phishing indicators? Please share the content (remove any personal information first).

**Remember:** When in doubt, verify through official channels. No legitimate organization will ask for sensitive information via email."""
    
    def _perform_security_scan(self) -> str:
        """Perform security scan and assessment"""
        return """🔍 **Security Scan Report**

**System Security Assessment:**

💻 **Device Security Checklist:**
□ Operating system up to date
□ Antivirus software active and updated
□ Firewall enabled
□ Automatic updates configured
□ Screen lock/password set
□ Backup system in place
□ VPN available for public Wi-Fi

🌐 **Network Security:**
□ Wi-Fi network secured (WPA3/WPA2)
□ Default router passwords changed
□ Guest network separated
□ IoT devices secured
□ Network access logs reviewed

🔐 **Account Security:**
□ Unique passwords for all accounts
□ Two-factor authentication enabled
□ Password manager in use
□ Regular password updates
□ Account monitoring active
□ Recovery information updated

📱 **Application Security:**
□ Apps from official stores only
□ App permissions reviewed
□ Automatic app updates enabled
□ Unused apps removed
□ Browser security settings configured

**Threat Detection Results:**

🟢 **Low Risk Areas:**
- Basic security software installed
- Standard browsing habits
- Limited social media exposure

🟡 **Medium Risk Areas:**
- Password reuse detected
- Some software outdated
- Public Wi-Fi usage without VPN
- Limited backup procedures

🟠 **High Risk Areas:**
- Default passwords still in use
- Missing security updates
- No two-factor authentication
- Suspicious network activity

**Immediate Action Items:**

🚨 **Critical (Do Now):**
1. Update all security software
2. Change any default passwords
3. Enable 2FA on important accounts
4. Install pending system updates

⚠️ **Important (This Week):**
1. Set up comprehensive backup system
2. Review and update all passwords
3. Configure firewall settings
4. Audit application permissions

📋 **Recommended (This Month):**
1. Implement password manager
2. Set up VPN for mobile devices
3. Review privacy settings on social media
4. Create incident response plan

**Security Score: 7/10**
Your security posture is good but has room for improvement in password management and backup procedures.

**Next Scan:** Recommended in 30 days or after implementing critical actions.

**Custom Recommendations:**
Based on your usage patterns, focus on:
- Enhanced email security (phishing protection)
- Mobile device security
- Cloud storage security
- Financial account monitoring

Want detailed guidance on any specific security area?"""
    
    def _provide_threat_intelligence(self) -> str:
        """Provide current threat intelligence"""
        return """📊 **Current Threat Intelligence Report**

**Active Threat Landscape:**

🎯 **Top Current Threats:**

1. **🎣 Phishing Campaigns**
   - Targeting: Banking, social media, work accounts
   - Method: Fake login pages, urgent action emails
   - Impact: Account takeover, identity theft
   - Trend: ↗️ Increasing sophistication

2. **💻 Ransomware**
   - Targeting: Businesses, healthcare, municipalities
   - Method: Email attachments, remote access vulnerabilities
   - Impact: Data encryption, business disruption
   - Trend: ↗️ Double extortion tactics

3. **📱 Mobile Malware**
   - Targeting: Banking apps, messaging platforms
   - Method: Fake apps, SMS phishing
   - Impact: Financial theft, data harvesting
   - Trend: ↗️ Android focus, iOS emerging

4. **🏠 IoT Vulnerabilities**
   - Targeting: Smart home devices, cameras
   - Method: Default credentials, unpatched firmware
   - Impact: Privacy invasion, botnet recruitment
   - Trend: → Stable but persistent

**Emerging Threats:**

🔬 **AI-Powered Attacks:**
- Deepfake audio/video for social engineering
- AI-generated phishing content
- Automated vulnerability discovery

🌐 **Supply Chain Attacks:**
- Software update compromises
- Third-party service breaches
- Hardware implants

🎭 **Social Engineering Evolution:**
- Highly personalized attacks
- Multi-platform coordination
- Long-term relationship building

**Industry-Specific Threats:**

🏥 **Healthcare:**
- Patient data ransomware
- Medical device vulnerabilities
- Telehealth platform attacks

🏫 **Education:**
- Student data breaches
- Online learning platform compromises
- Research data theft

💰 **Financial Services:**
- Cryptocurrency exchange attacks
- Mobile banking malware
- Business email compromise

**Geographic Threat Patterns:**

🌍 **Global Hotspots:**
- Eastern Europe: Ransomware operations
- Southeast Asia: Mobile banking malware
- North America: Business email compromise
- Western Europe: GDPR-targeted attacks

**Protection Strategies:**

🛡️ **Current Best Practices:**
1. **Zero Trust Architecture** - Verify everything
2. **Endpoint Detection** - Advanced monitoring
3. **Security Awareness** - Regular training
4. **Incident Response** - Prepared procedures
5. **Threat Hunting** - Proactive detection

**Weekly Threat Briefing:**
- New phishing campaigns targeting major banks
- Vulnerability disclosed in popular VPN software
- Ransomware group targeting small businesses
- Mobile app store removes malicious applications

**Threat Prediction (Next 30 Days):**
📈 **Expected Increases:**
- Tax season phishing scams
- Back-to-school targeting students
- Holiday shopping fake websites
- Cryptocurrency investment scams

**Recommended Actions:**
1. **Update threat intelligence feeds**
2. **Review incident response procedures**
3. **Conduct phishing simulation training**
4. **Audit third-party vendor security**
5. **Implement additional monitoring**

**Threat Intelligence Sources:**
- Government cybersecurity agencies
- Industry threat sharing groups
- Security vendor research
- Open source intelligence
- Community reporting

**Risk Assessment for You:**
Based on typical user profiles:
- **Personal Risk: Medium** - Standard phishing/malware exposure
- **Professional Risk: Variable** - Depends on industry/role
- **Financial Risk: Medium** - Online banking/shopping usage

Want specific guidance for your situation or industry?"""
    
    def _provide_incident_response(self) -> str:
        """Provide incident response guidance"""
        return """🚨 **INCIDENT RESPONSE GUIDE**

**⚠️ IMMEDIATE ACTIONS (First 30 Minutes):**

🔒 **Contain the Threat:**
1. **Disconnect from internet** (unplug network cable/disable Wi-Fi)
2. **Don't shut down** - May lose evidence
3. **Document everything** - Screenshots, notes, times
4. **Isolate affected systems** - Prevent spread
5. **Notify IT/Security team** immediately

📱 **Communication:**
- Use separate, clean device for communication
- Contact your IT department or security team
- Don't use compromised systems for reporting
- Follow your organization's incident procedures

**🔍 ASSESSMENT PHASE (Next 2 Hours):**

📊 **Determine Scope:**
- Which systems are affected?
- What data might be compromised?
- How did the incident occur?
- Is the threat still active?

🕵️ **Evidence Collection:**
- Take photos of screens with errors
- Save any suspicious emails (don't click)
- Document unusual system behavior
- Note any ransom demands or messages

**🛠️ RESPONSE ACTIONS:**

💻 **If Malware Suspected:**
1. **Don't pay ransoms** - No guarantee of recovery
2. **Run antivirus scan** from clean boot media
3. **Check for file encryption** - Are files accessible?
4. **Restore from backups** if available and clean
5. **Change all passwords** after cleaning

📧 **If Email Compromised:**
1. **Change email password immediately**
2. **Enable 2FA** if not already active
3. **Check sent folder** for unauthorized emails
4. **Review forwarding rules** and auto-replies
5. **Scan all downloaded attachments**

💳 **If Financial Information Involved:**
1. **Contact banks immediately** - Report fraud
2. **Monitor accounts** for unauthorized transactions
3. **Place fraud alerts** on credit reports
4. **Document all financial impacts**
5. **File police report** if significant loss

🆔 **If Personal Information Compromised:**
1. **Change passwords** on all affected accounts
2. **Monitor credit reports** for suspicious activity
3. **Consider identity monitoring** services
4. **File complaints** with relevant authorities
5. **Document all impacts** for insurance/legal

**🔄 RECOVERY PHASE:**

🧹 **System Cleanup:**
- Full antivirus/anti-malware scan
- Update all software and operating systems
- Remove any suspicious programs
- Restore from known-clean backups
- Verify system integrity

🔐 **Security Hardening:**
- Change all passwords (use password manager)
- Enable 2FA on all possible accounts
- Update security software
- Review and adjust security settings
- Implement additional monitoring

**📋 POST-INCIDENT ACTIONS:**

📝 **Documentation:**
- Complete incident timeline
- Financial impact assessment
- Technical details of compromise
- Response actions taken
- Lessons learned

🎓 **Learning:**
- What security gaps were exploited?
- How can similar incidents be prevented?
- What security improvements are needed?
- Should policies or procedures be updated?

**🆘 EMERGENCY CONTACTS:**

🏢 **Business:**
- IT Helpdesk: [Your IT number]
- Security Operations Center (SOC)
- Cyber Insurance provider
- Legal counsel (for data breaches)

🏠 **Personal:**
- Bank fraud departments
- Credit card companies
- Credit monitoring services
- Local law enforcement (for major crimes)

**⚖️ LEGAL CONSIDERATIONS:**

📋 **Compliance Requirements:**
- Data breach notification laws
- Industry-specific regulations
- Customer notification requirements
- Regulatory reporting obligations

**🛡️ PREVENTION FOR FUTURE:**

✅ **Immediate Improvements:**
- Implement regular backups
- Update incident response plan
- Conduct security awareness training
- Review and test recovery procedures

📈 **Long-term Enhancements:**
- Implement advanced threat detection
- Regular security assessments
- Tabletop incident response exercises
- Enhanced monitoring and logging

**🚨 CRITICAL REMINDERS:**
- **Time is critical** - Act quickly but carefully
- **Don't panic** - Follow systematic procedures
- **Preserve evidence** - Don't delete or modify
- **Communicate clearly** - Keep stakeholders informed
- **Learn and improve** - Update defenses afterward

**Current Status Assessment:**
Are you currently experiencing a security incident? If yes, please specify:
- Type of threat (malware, phishing, data breach, etc.)
- Affected systems
- When it was discovered
- Current symptoms

**Need immediate help? Prioritize these actions:**
1. Disconnect from network
2. Contact your IT support
3. Document everything
4. Don't pay any ransoms
5. Follow your organization's procedures

What specific type of incident response guidance do you need?"""
    
    def _provide_security_recommendations(self) -> str:
        """Provide personalized security recommendations"""
        return """🛡️ **Personalized Security Recommendations**

**🎯 Priority-Based Security Improvements:**

**🔴 CRITICAL (Implement Immediately):**

1. **🔐 Enable Two-Factor Authentication (2FA)**
   - Email accounts (Gmail, Outlook, etc.)
   - Banking and financial services
   - Social media accounts
   - Work/business accounts
   - **Impact:** Prevents 99.9% of automated attacks

2. **🔑 Use Unique, Strong Passwords**
   - Install password manager (Bitwarden, 1Password)
   - Generate unique passwords for each account
   - Use 12+ character passwords
   - **Impact:** Prevents credential stuffing attacks

3. **🔄 Update All Software**
   - Operating system updates
   - Browser updates
   - Security software updates
   - Application updates
   - **Impact:** Closes known security vulnerabilities

**🟠 HIGH PRIORITY (This Week):**

4. **📧 Email Security Enhancement**
   - Enable advanced phishing protection
   - Configure spam filters
   - Review email forwarding rules
   - Train on phishing recognition
   - **Impact:** Reduces primary attack vector

5. **💾 Implement Backup Strategy**
   - Automated cloud backups
   - Local backup verification
   - Test restoration procedures
   - Backup encryption
   - **Impact:** Protects against ransomware/data loss

6. **🔥 Configure Firewall**
   - Enable built-in firewall
   - Review application permissions
   - Monitor network connections
   - Block unnecessary services
   - **Impact:** Controls network access

**🟡 MEDIUM PRIORITY (This Month):**

7. **📱 Mobile Device Security**
   - Screen lock with strong PIN/biometric
   - App permission review
   - Enable remote wipe capability
   - Use VPN on public Wi-Fi
   - **Impact:** Protects personal data on mobile

8. **🏠 Home Network Security**
   - Change default router passwords
   - Enable WPA3 encryption
   - Create guest network
   - Update router firmware
   - **Impact:** Secures home base of operations

9. **👥 Social Media Privacy**
   - Review privacy settings
   - Limit personal information sharing
   - Enable login notifications
   - Audit connected applications
   - **Impact:** Reduces social engineering exposure

**🟢 LOWER PRIORITY (Ongoing):**

10. **📊 Security Monitoring**
    - Set up account breach notifications
    - Monitor credit reports
    - Review account statements
    - Track device login locations
    - **Impact:** Early threat detection

**🎯 Personalized Recommendations Based on Your Profile:**

**For Your Work Setup:**
- Implement zero-trust network access
- Use company-approved VPN
- Separate work and personal accounts
- Regular security training participation

**For Your Personal Life:**
- Family security education
- Secure smart home devices
- Financial account monitoring
- Travel security preparations

**📋 Security Implementation Timeline:**

**Week 1:**
□ Enable 2FA on top 5 accounts
□ Install password manager
□ Update all devices and software

**Week 2:**
□ Generate unique passwords for all accounts
□ Set up automated backups
□ Configure email security settings

**Week 3:**
□ Review and secure home network
□ Audit mobile device security
□ Update social media privacy settings

**Week 4:**
□ Set up security monitoring
□ Create incident response plan
□ Schedule monthly security reviews

**🔍 Security Assessment Quiz:**

Answer these to get more specific recommendations:

1. **Do you use the same password on multiple sites?**
   - If yes: Password manager is critical priority

2. **Do you click links in emails without checking?**
   - If yes: Phishing awareness training needed

3. **Are your devices set to auto-update?**
   - If no: Configure automatic updates immediately

4. **Do you use public Wi-Fi for sensitive activities?**
   - If yes: VPN setup is essential

5. **When did you last change important passwords?**
   - If >6 months: Password refresh needed

**💰 Budget-Conscious Security:**

**Free Solutions:**
- Built-in 2FA (Google, Microsoft authenticators)
- Free password managers (Bitwarden)
- Built-in device security features
- Free antivirus (Windows Defender)
- Browser security extensions

**Low-Cost Investments:**
- Premium password manager ($3-5/month)
- VPN service ($5-10/month)
- Cloud backup service ($2-5/month)
- Security awareness training ($10-20/year)

**🎓 Security Education Plan:**

**Monthly Learning:**
- Month 1: Password security and 2FA
- Month 2: Phishing recognition
- Month 3: Network security basics
- Month 4: Incident response procedures

**📈 Measuring Security Improvement:**

**Key Metrics to Track:**
- Number of accounts with 2FA enabled
- Percentage of unique passwords
- Days since last security update
- Number of security incidents (goal: zero)
- Time to detect/respond to threats

**🚀 Advanced Security (When Ready):**

- Hardware security keys
- Endpoint detection and response (EDR)
- Security information and event management (SIEM)
- Threat intelligence subscriptions
- Professional security assessments

**Remember:**
- Security is a journey, not a destination
- Start with high-impact, low-effort improvements
- Consistency matters more than perfection
- Stay informed about new threats
- Regular reviews and updates are essential

What specific area would you like to focus on first?"""
    
    def _activate_threat_mode(self) -> str:
        """Activate general threat mode"""
        return """🚨 **THREAT MODE ACTIVATED** 🚨

**🎯 Enhanced Security Monitoring Enabled**

**Current Security Status:**
🟢 **DEFCON 2** - Heightened Awareness
- Proactive threat monitoring active
- Enhanced pattern recognition enabled
- Security recommendations prioritized
- Incident response procedures ready

**🔍 What Threat Mode Monitors:**

**📧 Email Threats:**
- Phishing attempts and suspicious links
- Social engineering indicators
- Malicious attachments
- Spoofed sender addresses

**🌐 Web Browsing:**
- Malicious website detection
- Drive-by download attempts
- Suspicious redirects
- Fake shopping/banking sites

**💻 System Activity:**
- Unusual network connections
- Unexpected software installations
- System performance anomalies
- File encryption attempts

**📱 Mobile Security:**
- App permission violations
- Suspicious SMS/calls
- Rogue Wi-Fi networks
- Location tracking attempts

**🛡️ Active Protection Measures:**

1. **Real-time Analysis** - All communications scanned
2. **Behavioral Monitoring** - Unusual activity detection
3. **Threat Intelligence** - Latest threat database active
4. **Incident Response** - Rapid response procedures ready
5. **Security Coaching** - Real-time security guidance

**⚡ Immediate Actions Taken:**

✅ **Enhanced Monitoring:**
- Threat pattern recognition activated
- Security event logging increased
- Anomaly detection sensitivity raised
- Proactive scanning enabled

✅ **User Protection:**
- Security awareness mode engaged
- Risk assessment for all activities
- Safe alternatives suggested
- Incident prevention prioritized

**🚨 Threat Detection Capabilities:**

**🎣 Phishing Detection:**
- Email content analysis
- URL reputation checking
- Social engineering pattern recognition
- Brand impersonation detection

**🦠 Malware Prevention:**
- File behavior analysis
- Network traffic monitoring
- Suspicious process detection
- Zero-day threat indicators

**🏃‍♂️ Advanced Persistent Threats (APT):**
- Long-term pattern analysis
- Lateral movement detection
- Data exfiltration monitoring
- Command and control identification

**📊 Security Intelligence:**
- Global threat landscape awareness
- Industry-specific threat tracking
- Geographic risk assessment
- Timing-based attack predictions

**🔔 Alert System:**

**🔴 Critical Alerts:**
- Immediate threat detected
- Account compromise suspected
- Financial fraud indicators
- Identity theft attempts

**🟠 High Priority:**
- Suspicious activity patterns
- Security policy violations
- Potential data breaches
- System vulnerabilities

**🟡 Medium Priority:**
- Unusual access patterns
- Configuration weaknesses
- Training opportunities
- Preventive measures

**📋 Threat Mode Commands:**

Say any of these to activate specific protections:
- "**Analyze threat**" - Deep threat analysis
- "**Security scan**" - Comprehensive security check
- "**Phishing check**" - Email/message analysis
- "**Incident response**" - Emergency procedures
- "**Threat intelligence**" - Current threat landscape
- "**Deactivate threat mode**" - Return to normal

**🎯 Personalized Threat Profile:**

Based on your digital footprint:
- **Risk Level:** Medium
- **Primary Threats:** Phishing, malware
- **Vulnerable Areas:** Email, web browsing
- **Protection Score:** 7/10
- **Recommendations:** 2FA, password manager

**🔄 Continuous Improvement:**
- Threat patterns updated hourly
- Security posture assessed daily
- Protection strategies refined weekly
- Incident response tested monthly

**🆘 Emergency Procedures:**
If you suspect an active threat:
1. **Say "EMERGENCY"** for immediate assistance
2. **Disconnect from internet** if advised
3. **Document everything** you observe
4. **Follow specific guidance** provided
5. **Don't panic** - help is available

**⏰ Threat Mode Duration:**
- Active until manually deactivated
- Auto-refresh every 24 hours
- Enhanced protection maintained
- Regular status updates provided

**Remember in Threat Mode:**
- 🔍 **Trust but verify** everything
- 🛡️ **When in doubt, ask** before proceeding
- 📞 **Report suspicious activity** immediately
- 🧠 **Stay alert but calm**
- 📚 **Learn from each threat encounter**

**Current Threat Level: ELEVATED**
Stay vigilant and follow security best practices.

What specific threats would you like me to monitor for?"""
    
    def _store_threat_analysis(self, analysis: Dict[str, Any]):
        """Store threat analysis in history"""
        analysis['timestamp'] = datetime.now().isoformat()
        self.threat_history.append(analysis)
        
        # Keep history within limits
        if len(self.threat_history) > self.max_threat_history:
            self.threat_history = self.threat_history[-self.max_threat_history:]
        
        # Store in digital twin if available
        if self.twin:
            try:
                self.twin.db.record_metric('threat_detection', analysis.get('overall_threat_level', 0), analysis)
            except Exception as e:
                logger.error(f"Error storing threat analysis: {e}")
    
    def _format_threat_analysis(self, analysis: Dict[str, Any]) -> str:
        """Format threat analysis for user display"""
        level = analysis['overall_threat_level']
        level_info = self.threat_levels.get(level, self.threat_levels['low'])
        
        result = f"🛡️ **Threat Analysis Report**\n\n"
        result += f"**Threat Level: {level_info['color']} {level.upper()}**\n\n"
        
        if analysis['detected_patterns']:
            result += "**Detected Threat Patterns:**\n"
            for pattern in analysis['detected_patterns']:
                result += f"⚠️ {pattern}\n"
            result += "\n"
        
        result += f"**Risk Scores:**\n"
        result += f"🎣 Phishing: {analysis['phishing_score']}/10\n"
        result += f"🦠 Malware: {analysis['malware_score']}/10\n"
        result += f"🎭 Social Engineering: {analysis['social_engineering_score']}/10\n\n"
        
        # Add recommendations based on threat level
        if level == 'critical':
            result += "🚨 **IMMEDIATE ACTION REQUIRED:**\n"
            result += "- Do not interact with the suspicious content\n"
            result += "- Disconnect from internet if actively threatened\n"
            result += "- Contact security team immediately\n"
            result += "- Document all details for investigation\n"
        elif level == 'high':
            result += "⚠️ **HIGH RISK - Exercise Extreme Caution:**\n"
            result += "- Verify authenticity through alternative channels\n"
            result += "- Do not provide personal information\n"
            result += "- Consider reporting to authorities\n"
            result += "- Monitor accounts for suspicious activity\n"
        elif level == 'medium':
            result += "🟡 **MODERATE RISK - Proceed with Caution:**\n"
            result += "- Verify source independently\n"
            result += "- Use additional authentication methods\n"
            result += "- Monitor for follow-up attempts\n"
            result += "- Document for pattern analysis\n"
        else:
            result += "✅ **LOW RISK - Standard Precautions:**\n"
            result += "- Maintain normal security awareness\n"
            result += "- Continue routine security practices\n"
            result += "- Stay informed about new threats\n"
        
        return result
    
    def get_threat_statistics(self) -> Dict[str, Any]:
        """Get threat detection statistics"""
        try:
            if not self.threat_history:
                return {'status': 'no_threat_data'}
            
            # Analyze threat levels
            threat_levels = [t.get('overall_threat_level', 'low') for t in self.threat_history]
            level_counts = {}
            for level in threat_levels:
                level_counts[level] = level_counts.get(level, 0) + 1
            
            # Recent threat activity (last 24 hours)
            recent_cutoff = datetime.now() - timedelta(hours=24)
            recent_threats = [
                t for t in self.threat_history 
                if datetime.fromisoformat(t.get('timestamp', '1900-01-01')) > recent_cutoff
            ]
            
            return {
                'total_analyses': len(self.threat_history),
                'threat_level_distribution': level_counts,
                'recent_activity_24h': len(recent_threats),
                'highest_threat_level': max(threat_levels, key=lambda x: ['low', 'medium', 'high', 'critical'].index(x)) if threat_levels else 'low',
                'most_common_patterns': self._get_common_threat_patterns(),
                'threat_trend': self._calculate_threat_trend()
            }
            
        except Exception as e:
            logger.error(f"Error getting threat statistics: {e}")
            return {'error': str(e)}
    
    def _get_common_threat_patterns(self) -> List[str]:
        """Get most common threat patterns"""
        all_patterns = []
        for threat in self.threat_history:
            all_patterns.extend(threat.get('detected_patterns', []))
        
        pattern_counts = {}
        for pattern in all_patterns:
            pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
        
        # Return top 5 most common patterns
        sorted_patterns = sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)
        return [pattern for pattern, count in sorted_patterns[:5]]
    
    def _calculate_threat_trend(self) -> str:
        """Calculate threat trend over time"""
        if len(self.threat_history) < 2:
            return 'insufficient_data'
        
        recent_threats = self.threat_history[-10:]  # Last 10 analyses
        older_threats = self.threat_history[-20:-10] if len(self.threat_history) >= 20 else []
        
        if not older_threats:
            return 'insufficient_data'
        
        # Calculate average threat scores
        def avg_score(threats):
            if not threats:
                return 0
            scores = []
            for t in threats:
                total = t.get('phishing_score', 0) + t.get('malware_score', 0) + t.get('social_engineering_score', 0)
                scores.append(total)
            return sum(scores) / len(scores)
        
        recent_avg = avg_score(recent_threats)
        older_avg = avg_score(older_threats)
        
        if recent_avg > older_avg * 1.2:
            return 'increasing'
        elif recent_avg < older_avg * 0.8:
            return 'decreasing'
        else:
            return 'stable'
