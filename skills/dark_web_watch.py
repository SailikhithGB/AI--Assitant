"""
Dark Web Watch Skill - Security Monitoring and Breach Detection
Monitors for security breaches and provides security awareness
"""

import logging
import hashlib
import re
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import requests

logger = logging.getLogger(__name__)

class DarkWebWatch:
    """
    Dark Web Watch system for monitoring security breaches and threats
    Uses HaveIBeenPwned API and provides security awareness
    """
    
    def __init__(self):
        from config import HAVEIBEENPWNED_API_KEY
        self.api_key = HAVEIBEENPWNED_API_KEY
        self.hibp_base_url = "https://haveibeenpwned.com/api/v3"
        
        # Common breach indicators
        self.security_keywords = [
            'password', 'breach', 'hack', 'compromise', 'leak', 'exposed', 
            'stolen', 'malware', 'phishing', 'scam', 'virus'
        ]
        
    def route(self, text: str) -> str:
        """Route dark web watch requests"""
        try:
            text_lower = text.lower()
            
            # Check for email breach inquiry
            if any(phrase in text_lower for phrase in ['check email', 'email breach', 'been pwned', 'email compromised']):
                return self._handle_email_check_request(text)
            
            # Check for general security inquiry
            elif any(phrase in text_lower for phrase in ['security status', 'am i safe', 'security check']):
                return self._provide_security_overview()
            
            # Check for specific breach information
            elif any(phrase in text_lower for phrase in ['latest breaches', 'recent breaches', 'new breaches']):
                return self._get_recent_breaches()
            
            # Security tips request
            elif any(phrase in text_lower for phrase in ['security tips', 'stay safe', 'protect myself']):
                return self._provide_security_tips()
            
            # Password security
            elif any(phrase in text_lower for phrase in ['password security', 'strong password', 'password help']):
                return self._provide_password_guidance()
            
            # General dark web awareness
            else:
                return self._provide_general_awareness()
                
        except Exception as e:
            logger.error(f"Error in dark web watch routing: {e}")
            return f"I encountered an error while checking security information: {e}"
    
    def _handle_email_check_request(self, text: str) -> str:
        """Handle email breach checking requests"""
        # Extract email from text if provided
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        
        if emails:
            email = emails[0]
            return self._check_email_breaches(email)
        else:
            return """🔒 **Email Breach Check**

To check if your email has been in any known data breaches, I would need your email address. However, for privacy reasons, I recommend:

1. **Visit HaveIBeenPwned.com directly** - This is the most secure way to check
2. **Never share your email in chat logs** - Protect your privacy
3. **Use the official website** - https://haveibeenpwned.com

If you want to check multiple emails or get notifications about future breaches, you can:
- Subscribe to notifications on the official site
- Use a password manager that includes breach monitoring
- Set up email aliases for different services

**What to do if you find breaches:**
- Change passwords for affected accounts immediately
- Enable two-factor authentication where possible
- Monitor your accounts for suspicious activity"""
    
    def _check_email_breaches(self, email: str) -> str:
        """Check specific email for breaches using HaveIBeenPwned API"""
        if not self.api_key:
            return """🔒 **Email Breach Check**

I don't have access to the HaveIBeenPwned API right now. For the most secure and up-to-date breach check:

**Visit https://haveibeenpwned.com directly**

This is the official and most trusted way to check if your email has been compromised in known data breaches.

**Why check directly:**
- Most current data
- Secure connection
- No third-party involvement
- Official source"""
        
        try:
            headers = {
                'hibp-api-key': self.api_key,
                'User-Agent': 'Nova-AI-Assistant'
            }
            
            # Check breaches
            response = requests.get(
                f"{self.hibp_base_url}/breachedaccount/{email}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                breaches = response.json()
                return self._format_breach_results(email, breaches)
            elif response.status_code == 404:
                return f"✅ **Good news!** The email address has not been found in any known data breaches."
            else:
                return f"⚠️ Unable to check breach status (Status: {response.status_code}). Please try again later or check directly at haveibeenpwned.com."
                
        except requests.RequestException as e:
            logger.error(f"Error checking email breaches: {e}")
            return "⚠️ Unable to connect to breach database. Please check your internet connection or try again later."
        except Exception as e:
            logger.error(f"Unexpected error in breach check: {e}")
            return f"⚠️ An unexpected error occurred: {e}"
    
    def _format_breach_results(self, email: str, breaches: List[Dict]) -> str:
        """Format breach results for user"""
        if not breaches:
            return "✅ **Good news!** No breaches found for this email address."
        
        result = f"⚠️ **{len(breaches)} breach(es) found** for this email address:\n\n"
        
        # Sort breaches by date (most recent first)
        breaches.sort(key=lambda x: x.get('BreachDate', ''), reverse=True)
        
        for i, breach in enumerate(breaches[:5], 1):  # Show top 5 most recent
            name = breach.get('Name', 'Unknown')
            date = breach.get('BreachDate', 'Unknown date')
            description = breach.get('Description', 'No description available')
            
            # Clean up description (remove HTML tags)
            clean_description = re.sub('<[^<]+?>', '', description)
            if len(clean_description) > 150:
                clean_description = clean_description[:150] + "..."
            
            result += f"**{i}. {name}** ({date})\n"
            result += f"   {clean_description}\n\n"
        
        if len(breaches) > 5:
            result += f"... and {len(breaches) - 5} more breach(es).\n\n"
        
        result += """**🛡️ What to do now:**
1. **Change passwords** for any affected accounts immediately
2. **Enable 2FA** (two-factor authentication) where possible
3. **Monitor accounts** for suspicious activity
4. **Use unique passwords** for each account
5. **Consider a password manager** for better security

**Stay vigilant** and regularly check for new breaches at haveibeenpwned.com"""
        
        return result
    
    def _provide_security_overview(self) -> str:
        """Provide general security overview"""
        return """🛡️ **Security Status Overview**

**Current Threat Landscape:**
- Data breaches are increasingly common
- Cybercriminals target personal information
- Password reuse is a major vulnerability
- Phishing attacks are becoming more sophisticated

**Your Security Checklist:**
✅ Use unique, strong passwords for each account
✅ Enable two-factor authentication (2FA)
✅ Keep software and apps updated
✅ Be cautious with email links and attachments
✅ Regularly monitor your accounts
✅ Use a reputable password manager
✅ Back up important data

**Red Flags to Watch For:**
🚩 Unexpected password reset emails
🚩 Unknown login notifications
🚩 Suspicious account activity
🚩 Emails asking for personal information
🚩 Unexpected charges or transactions

**Need Help?**
- Ask me to check for recent breaches
- Request security tips for specific situations
- Get guidance on password security
- Learn about protecting your privacy online"""
    
    def _get_recent_breaches(self) -> str:
        """Get information about recent breaches"""
        try:
            if not self.api_key:
                return """📊 **Recent Data Breaches**

I don't have real-time access to breach data, but here's what you should know:

**Stay Informed:**
- Visit https://haveibeenpwned.com for the latest breach information
- Follow security news sources like Krebs on Security
- Enable breach notifications for your email addresses

**Common Recent Breach Types:**
- Social media platforms
- E-commerce websites
- Health care systems
- Educational institutions
- Gaming platforms

**Protection Strategy:**
- Assume any service you use might be breached
- Use unique passwords for every account
- Enable 2FA wherever possible
- Monitor your accounts regularly"""
            
            headers = {
                'hibp-api-key': self.api_key,
                'User-Agent': 'Nova-AI-Assistant'
            }
            
            # Get all breaches (recent ones will be at the top)
            response = requests.get(
                f"{self.hibp_base_url}/breaches",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                breaches = response.json()
                return self._format_recent_breaches(breaches)
            else:
                return "⚠️ Unable to fetch recent breach data. Please check haveibeenpwned.com for the latest information."
                
        except Exception as e:
            logger.error(f"Error getting recent breaches: {e}")
            return "⚠️ Unable to fetch breach information. Please check haveibeenpwned.com for updates."
    
    def _format_recent_breaches(self, breaches: List[Dict]) -> str:
        """Format recent breaches information"""
        # Filter and sort recent breaches (last 6 months)
        six_months_ago = datetime.now() - timedelta(days=180)
        
        recent_breaches = []
        for breach in breaches:
            breach_date_str = breach.get('BreachDate')
            if breach_date_str:
                try:
                    breach_date = datetime.strptime(breach_date_str, '%Y-%m-%d')
                    if breach_date > six_months_ago:
                        recent_breaches.append(breach)
                except ValueError:
                    continue
        
        if not recent_breaches:
            return "✅ **No major breaches reported in the last 6 months.**\n\nHowever, stay vigilant as new breaches are discovered regularly."
        
        # Sort by date (most recent first)
        recent_breaches.sort(key=lambda x: x.get('BreachDate', ''), reverse=True)
        
        result = f"📊 **Recent Data Breaches ({len(recent_breaches)} in last 6 months):**\n\n"
        
        for breach in recent_breaches[:10]:  # Show top 10
            name = breach.get('Name', 'Unknown')
            date = breach.get('BreachDate', 'Unknown')
            pwn_count = breach.get('PwnCount', 0)
            
            result += f"**{name}** - {date}\n"
            result += f"   📈 {pwn_count:,} accounts affected\n"
            
            # Add data types if available
            data_classes = breach.get('DataClasses', [])
            if data_classes:
                result += f"   📋 Data: {', '.join(data_classes[:3])}\n"
            result += "\n"
        
        result += """**🛡️ Stay Protected:**
- Check if your accounts were affected at haveibeenpwned.com
- Change passwords for any compromised accounts
- Monitor your accounts for suspicious activity
- Use unique passwords and enable 2FA"""
        
        return result
    
    def _provide_security_tips(self) -> str:
        """Provide comprehensive security tips"""
        return """🛡️ **Essential Security Tips**

**Password Security:**
🔐 Use unique passwords for every account
🔐 Make passwords at least 12 characters long
🔐 Include uppercase, lowercase, numbers, and symbols
🔐 Consider using passphrases (4+ random words)
🔐 Use a password manager to generate and store passwords

**Two-Factor Authentication (2FA):**
📱 Enable 2FA on all important accounts
📱 Use authenticator apps over SMS when possible
📱 Keep backup codes in a safe place
📱 Consider hardware security keys for highest security

**Email Security:**
📧 Be suspicious of unexpected emails
📧 Don't click links from unknown senders
📧 Verify requests for personal information
📧 Check sender addresses carefully
📧 Use separate emails for different purposes

**Device Security:**
💻 Keep software and apps updated
💻 Use device lock screens
💻 Enable automatic updates
💻 Install antivirus software
💻 Avoid public Wi-Fi for sensitive activities

**Financial Security:**
💳 Monitor bank and credit card statements
💳 Set up account alerts
💳 Freeze your credit when not needed
💳 Use secure payment methods online
💳 Check credit reports regularly

**Privacy Protection:**
🔒 Review privacy settings on social media
🔒 Limit personal information sharing
🔒 Use VPN for public Wi-Fi
🔒 Be cautious about app permissions
🔒 Regularly clean up old accounts"""
    
    def _provide_password_guidance(self) -> str:
        """Provide specific password security guidance"""
        return """🔐 **Password Security Guide**

**Creating Strong Passwords:**

**Method 1: Passphrases**
- Use 4+ random words: `Coffee#Mountain$River!Dance`
- Easy to remember, hard to crack
- Add numbers and symbols between words

**Method 2: Character Substitution**
- Start with a phrase: "I love pizza and movies"
- Transform: `IL0v3P1zz4&M0v!es`
- Replace letters with numbers/symbols

**Method 3: Password Patterns**
- Create a base: `MySecure!`
- Add site identifier: `MySecure!FB23` (Facebook)
- Change the identifier for each site

**Password Don'ts:**
❌ Don't reuse passwords across sites
❌ Avoid personal information (birthdays, names)
❌ Don't use dictionary words
❌ Avoid simple patterns (123456, qwerty)
❌ Don't share passwords with others

**Password Managers:**
✅ Generate unique passwords automatically
✅ Store passwords securely
✅ Sync across devices
✅ Popular options: Bitwarden, 1Password, LastPass

**Testing Password Strength:**
- Most password managers include strength meters
- Check if your passwords have been breached
- Aim for "Very Strong" or equivalent ratings

**Emergency Planning:**
- Keep master password written down securely
- Share emergency access with trusted person
- Have backup authentication methods
- Know how to recover accounts if locked out

**Quick Security Check:**
1. Are you using unique passwords? (Most important!)
2. Do you have 2FA enabled on important accounts?
3. When did you last update your passwords?
4. Are you using a password manager?

Need help with any specific aspect of password security?"""
    
    def _provide_general_awareness(self) -> str:
        """Provide general dark web awareness"""
        return """🕵️ **Dark Web & Security Awareness**

**What is the Dark Web?**
The dark web is a part of the internet that requires special software to access. While it has legitimate uses, it's also where cybercriminals often sell stolen data.

**How Your Data Gets There:**
📊 **Data Breaches** - Companies get hacked and data is stolen
🎣 **Phishing** - Criminals trick people into giving up information
💻 **Malware** - Software that steals data from infected devices
🏪 **Insider Threats** - Employees with access misuse information

**What Gets Sold:**
- Email addresses and passwords
- Credit card numbers
- Social Security numbers
- Personal documents
- Login credentials
- Financial information

**How to Protect Yourself:**
🛡️ **Proactive Measures:**
- Use unique passwords for every account
- Enable two-factor authentication
- Keep software updated
- Be cautious with emails and links
- Monitor your accounts regularly

🔍 **Monitoring:**
- Check haveibeenpwned.com regularly
- Set up account alerts
- Monitor credit reports
- Use identity monitoring services

⚡ **If You're Compromised:**
1. Change passwords immediately
2. Enable 2FA if not already active
3. Monitor accounts for suspicious activity
4. Consider freezing your credit
5. Report identity theft if necessary

**Stay Informed:**
- Follow cybersecurity news
- Learn about latest scam techniques
- Keep security knowledge updated
- Share knowledge with friends and family

**Remember:** Perfect security doesn't exist, but good security practices make you a much harder target!

Want specific help with any security concern?"""
