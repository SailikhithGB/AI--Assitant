"""
Cross Device Skill - Multi-Device Coordination
Manages interactions across multiple devices and platforms
"""

import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import json
import platform

logger = logging.getLogger(__name__)

class CrossDevice:
    """
    Cross Device system for coordinating actions across multiple devices
    Provides safe, consent-based multi-device functionality
    """
    
    def __init__(self):
        self.device_sessions = {}
        self.pending_actions = {}
        self.supported_platforms = ['windows', 'darwin', 'linux']
        self.current_platform = platform.system().lower()
        
    def route(self, text: str, require_confirmation: bool = True) -> Optional[str]:
        """Route cross-device requests"""
        try:
            text_lower = text.lower()
            
            # Device status queries
            if any(phrase in text_lower for phrase in ['device status', 'connected devices', 'my devices']):
                return self._get_device_status()
            
            # Cross-device file sharing
            elif any(phrase in text_lower for phrase in ['share file', 'send to device', 'sync file']):
                return self._handle_file_sharing_request(text, require_confirmation)
            
            # Notification sync
            elif any(phrase in text_lower for phrase in ['sync notifications', 'notification sync', 'mirror notifications']):
                return self._handle_notification_sync(require_confirmation)
            
            # Clipboard sync
            elif any(phrase in text_lower for phrase in ['sync clipboard', 'clipboard sync', 'share clipboard']):
                return self._handle_clipboard_sync(require_confirmation)
            
            # Remote control requests
            elif any(phrase in text_lower for phrase in ['remote control', 'control device', 'remote access']):
                return self._handle_remote_control_request(text, require_confirmation)
            
            # Session continuity
            elif any(phrase in text_lower for phrase in ['continue on', 'switch device', 'handoff']):
                return self._handle_session_continuity(text, require_confirmation)
            
            return None
            
        except Exception as e:
            logger.error(f"Error in cross-device routing: {e}")
            return f"Cross-device coordination error: {e}"
    
    def _get_device_status(self) -> str:
        """Get status of connected devices"""
        return f"""🖥️ **Device Status Report**

**Current Device:**
- Platform: {self.current_platform.title()}
- Session ID: Local-{datetime.now().strftime('%Y%m%d')}
- Status: Active ✅

**Cross-Device Features Available:**
📁 **File Sharing** - Share files between devices
🔔 **Notification Sync** - Mirror notifications across devices  
📋 **Clipboard Sync** - Share clipboard content
🖱️ **Remote Control** - Limited remote access (with consent)
🔄 **Session Continuity** - Continue work on another device

**Security Features:**
- All actions require explicit consent
- No automatic background sync
- Local network preferred over internet
- Encrypted connections when possible

**Setup Required:**
To enable cross-device features, you would need:
1. Install companion apps on target devices
2. Configure network permissions
3. Set up secure authentication
4. Enable specific features you want

**Note:** Cross-device features are currently in simulation mode. Real implementation would require additional setup and security considerations.

Want help setting up any specific cross-device feature?"""
    
    def _handle_file_sharing_request(self, text: str, require_confirmation: bool) -> str:
        """Handle file sharing between devices"""
        if require_confirmation:
            return """📁 **Cross-Device File Sharing**

For security and privacy, file sharing between devices requires:

**Setup Requirements:**
1. **Secure Network** - Both devices on same trusted network
2. **Authentication** - Verified device identity
3. **Explicit Consent** - Manual approval for each transfer
4. **Encryption** - Files encrypted during transfer

**Recommended Alternatives:**
✅ **Cloud Storage** - Google Drive, Dropbox, OneDrive
✅ **Email** - For smaller files
✅ **USB Drive** - For local transfers
✅ **Bluetooth** - For nearby devices
✅ **Network Shares** - For home/office networks

**If you proceed:**
1. Specify source and destination devices
2. Select specific files to share
3. Confirm transfer on both devices
4. Verify successful transfer

**Privacy Note:** I don't have access to your files or network. Any file sharing would need to be set up through your operating system or dedicated apps.

Would you like guidance on setting up secure file sharing with built-in tools?"""
        
        else:
            return "File sharing initiated. Please confirm on target device."
    
    def _handle_notification_sync(self, require_confirmation: bool) -> str:
        """Handle notification synchronization"""
        if require_confirmation:
            return """🔔 **Notification Sync Setup**

**What Notification Sync Provides:**
- See phone notifications on computer
- Respond to messages from any device
- Unified notification center
- Cross-platform alert management

**Privacy Considerations:**
⚠️ **Sensitive Information** - Notifications may contain private data
⚠️ **Network Security** - Notifications sent over network
⚠️ **Storage** - Notification history may be stored
⚠️ **Access Control** - Other users might see notifications

**Recommended Solutions:**
📱 **Built-in Options:**
- iPhone + Mac: Use Apple's Handoff and Universal Clipboard
- Android + Windows: Use Microsoft's Phone Link
- Android + Chrome OS: Built-in Android integration

🔧 **Third-party Apps:**
- KDE Connect (cross-platform)
- Pushbullet (commercial)
- Join (Android focus)

**Security Best Practices:**
1. Use apps from trusted developers
2. Review notification permissions carefully
3. Enable end-to-end encryption if available
4. Regularly audit connected devices
5. Use local network when possible

**Would you like help setting up any of these official solutions?**"""
        
        else:
            return "Notification sync would be enabled. Confirm on all target devices."
    
    def _handle_clipboard_sync(self, require_confirmation: bool) -> str:
        """Handle clipboard synchronization"""
        if require_confirmation:
            return """📋 **Clipboard Sync Information**

**What Clipboard Sync Does:**
- Copy text on one device, paste on another
- Share images and formatted content
- Maintain clipboard history across devices
- Seamless workflow continuity

**Security Risks:**
🔓 **Sensitive Data** - Passwords, personal info in clipboard
🔓 **Network Transfer** - Clipboard data sent over network
🔓 **Storage** - Clipboard history may be logged
🔓 **Interception** - Risk of data being intercepted

**Safe Alternatives:**
✅ **Built-in Solutions:**
- Apple: Universal Clipboard (Mac + iOS)
- Microsoft: Cloud Clipboard (Windows)
- Google: Chrome sync (limited)

✅ **Security-Focused Apps:**
- KDE Connect (open source)
- Clipboard managers with encryption
- VPN-based solutions

**Best Practices:**
1. **Never sync sensitive data** like passwords
2. **Clear clipboard** after sensitive operations
3. **Use encrypted connections** only
4. **Regular security audits** of connected devices
5. **Disable auto-sync** for sensitive work

**Manual Alternative:**
Instead of automatic sync, consider:
- Secure note-taking apps (encrypted)
- Email drafts for text sharing
- Cloud storage for files
- QR codes for URLs/short text

Want guidance on setting up secure clipboard sharing?"""
        
        else:
            return "Clipboard sync initiated. Verify on target devices."
    
    def _handle_remote_control_request(self, text: str, require_confirmation: bool) -> str:
        """Handle remote control requests"""
        if require_confirmation:
            return """🖱️ **Remote Control Security Notice**

**⚠️ IMPORTANT SECURITY WARNING ⚠️**
Remote control access provides complete control over a device and should be used with extreme caution.

**Legitimate Use Cases:**
- IT support from trusted technicians
- Accessing your own devices remotely
- Helping family members with tech issues
- Work-approved remote access solutions

**Security Requirements:**
🔐 **Strong Authentication** - Multi-factor authentication
🔐 **Encrypted Connections** - End-to-end encryption
🔐 **Session Logging** - Track all remote sessions
🔐 **Time Limits** - Automatic session expiration
🔐 **Explicit Consent** - Manual approval for each session

**Trusted Solutions:**
✅ **TeamViewer** - Popular, secure commercial solution
✅ **Chrome Remote Desktop** - Google's free solution
✅ **Microsoft Remote Desktop** - For Windows environments
✅ **VNC** - Open source option (requires setup)
✅ **SSH** - Command-line access (technical users)

**Red Flags - NEVER Allow:**
❌ Unsolicited remote access requests
❌ "Tech support" calls asking for access
❌ Remote access for "prize claims" or "refunds"
❌ Access from unknown or untrusted parties
❌ Permanent or unmonitored access

**If You Need Remote Access:**
1. Use official apps from device app stores
2. Set up access only when needed
3. Use strong passwords and 2FA
4. Monitor active sessions
5. Revoke access when finished

**I cannot and will not provide actual remote access. This is for your security.**

Need help setting up secure remote access for legitimate purposes?"""
        
        else:
            return "Remote control cannot be enabled for security reasons."
    
    def _handle_session_continuity(self, text: str, require_confirmation: bool) -> str:
        """Handle session continuity between devices"""
        if require_confirmation:
            return """🔄 **Session Continuity Options**

**What Session Continuity Provides:**
- Start work on one device, continue on another
- Sync application state and data
- Seamless workflow transitions
- Context preservation across devices

**Built-in Solutions:**
📱 **Apple Ecosystem:**
- Handoff (start on iPhone, continue on Mac)
- Universal Clipboard
- Safari tab sync
- Document sync via iCloud

💻 **Microsoft Ecosystem:**
- Timeline (Windows 10/11)
- Office 365 sync
- Edge browser sync
- Microsoft 365 apps

🌐 **Google Ecosystem:**
- Chrome browser sync
- Google Workspace apps
- Android + Chrome OS integration

**Manual Continuity Methods:**
📝 **Document-Based:**
- Save work to cloud storage
- Use auto-syncing apps (Google Docs, Notion)
- Email drafts to yourself
- Cross-platform note apps (OneNote, Evernote)

🔖 **Bookmark and Link Sharing:**
- Browser bookmark sync
- Read-later apps (Pocket, Instapaper)
- URL sharing apps
- QR codes for quick transfers

**Privacy Considerations:**
- Session data may be stored in cloud
- Application state might contain sensitive info
- Network traffic during sync
- Multiple device access logs

**Recommendations:**
1. Use official ecosystem solutions when possible
2. Choose apps with end-to-end encryption
3. Regularly review synced data
4. Log out of shared/public devices
5. Use different accounts for work/personal

**Current Session Info:**
- Platform: {self.current_platform.title()}
- Started: {datetime.now().strftime('%H:%M')}
- Session Type: Local

Want help setting up continuity with specific apps or services?"""
        
        else:
            return "Session continuity prepared. Switch to target device to continue."
    
    def register_device(self, device_info: Dict[str, Any]) -> str:
        """Register a new device for cross-device features"""
        device_id = device_info.get('device_id', f"device_{datetime.now().timestamp()}")
        
        self.device_sessions[device_id] = {
            'info': device_info,
            'registered_at': datetime.now(),
            'last_seen': datetime.now(),
            'status': 'registered'
        }
        
        return f"Device {device_id} registered successfully. Confirmation required for cross-device actions."
    
    def get_connected_devices(self) -> List[Dict[str, Any]]:
        """Get list of connected devices"""
        devices = []
        for device_id, session in self.device_sessions.items():
            devices.append({
                'device_id': device_id,
                'platform': session['info'].get('platform', 'unknown'),
                'name': session['info'].get('name', 'Unknown Device'),
                'last_seen': session['last_seen'].isoformat(),
                'status': session['status']
            })
        
        return devices
    
    def sync_with_device(self, device_id: str, data: Dict[str, Any], require_confirmation: bool = True) -> str:
        """Sync data with specific device"""
        if require_confirmation:
            return f"Sync request prepared for device {device_id}. Manual confirmation required on target device for security."
        
        if device_id not in self.device_sessions:
            return f"Device {device_id} not found or not registered."
        
        # In a real implementation, this would handle secure data transfer
        return f"Data sync initiated with device {device_id}. Confirmation pending."
    
    def get_cross_device_suggestions(self) -> List[str]:
        """Get suggestions for cross-device workflows"""
        return [
            "Use cloud storage apps for seamless file access across devices",
            "Set up browser sync to continue browsing sessions",
            "Use note-taking apps that sync across platforms",
            "Consider password managers that work on all devices",
            "Set up email on all devices for communication continuity",
            "Use messaging apps with multi-device support",
            "Configure calendar sync for schedule coordination",
            "Set up photo backup for media accessibility"
        ]
    
    def cleanup_old_sessions(self, hours: int = 24):
        """Clean up old device sessions"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        expired_devices = []
        for device_id, session in list(self.device_sessions.items()):
            if session['last_seen'] < cutoff_time:
                expired_devices.append(device_id)
                del self.device_sessions[device_id]
        
        logger.info(f"Cleaned up {len(expired_devices)} expired device sessions")
        
        return expired_devices
