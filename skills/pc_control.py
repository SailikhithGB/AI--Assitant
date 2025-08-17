"""
PC Control Skill - System Command Execution
Handles computer control tasks like opening applications, managing windows, etc.
"""

import os
import subprocess
import platform
import logging
import webbrowser
from typing import Optional, Dict, Any
import time

logger = logging.getLogger(__name__)

class PCControl:
    """
    PC Control skill for managing computer operations
    Handles application launching, window management, and system commands
    """
    
    def __init__(self):
        self.system = platform.system().lower()
        logger.info(f"PC Control initialized for {self.system}")
        
        # Common applications mapping
        self.app_mappings = self._init_app_mappings()
        
    def _init_app_mappings(self) -> Dict[str, Dict[str, str]]:
        """Initialize application mappings for different operating systems"""
        mappings = {
            'windows': {
                'notepad': 'notepad.exe',
                'calculator': 'calc.exe',
                'paint': 'mspaint.exe',
                'file explorer': 'explorer.exe',
                'cmd': 'cmd.exe',
                'powershell': 'powershell.exe',
                'task manager': 'taskmgr.exe',
                'control panel': 'control.exe',
                'chrome': 'chrome.exe',
                'firefox': 'firefox.exe',
                'edge': 'msedge.exe'
            },
            'darwin': {  # macOS
                'safari': 'open -a Safari',
                'chrome': 'open -a "Google Chrome"',
                'firefox': 'open -a Firefox',
                'finder': 'open -a Finder',
                'terminal': 'open -a Terminal',
                'calculator': 'open -a Calculator',
                'textedit': 'open -a TextEdit',
                'activity monitor': 'open -a "Activity Monitor"',
                'system preferences': 'open -a "System Preferences"'
            },
            'linux': {
                'firefox': 'firefox',
                'chrome': 'google-chrome',
                'chromium': 'chromium-browser',
                'terminal': 'gnome-terminal',
                'file manager': 'nautilus',
                'calculator': 'gnome-calculator',
                'text editor': 'gedit',
                'system monitor': 'gnome-system-monitor'
            }
        }
        
        return mappings.get(self.system, {})
    
    def route(self, command: str) -> Optional[str]:
        """Route PC control commands"""
        try:
            command_lower = command.lower().strip()
            
            # Open applications
            if command_lower.startswith(('open ', 'launch ', 'start ')):
                return self._handle_open_command(command_lower)
            
            # Close applications
            elif command_lower.startswith(('close ', 'quit ', 'stop ')):
                return self._handle_close_command(command_lower)
            
            # System commands
            elif any(keyword in command_lower for keyword in ['shutdown', 'restart', 'sleep', 'lock']):
                return self._handle_system_command(command_lower)
            
            # File operations
            elif any(keyword in command_lower for keyword in ['create file', 'delete file', 'copy file']):
                return self._handle_file_operation(command_lower)
            
            # Volume control
            elif any(keyword in command_lower for keyword in ['volume up', 'volume down', 'mute']):
                return self._handle_volume_control(command_lower)
            
            return None  # Command not handled by this skill
            
        except Exception as e:
            logger.error(f"Error in PC control routing: {e}")
            return f"Error executing PC command: {e}"
    
    def _handle_open_command(self, command: str) -> str:
        """Handle application opening commands"""
        try:
            # Extract application name
            for prefix in ['open ', 'launch ', 'start ']:
                if command.startswith(prefix):
                    app_name = command[len(prefix):].strip()
                    break
            else:
                return "Could not identify application to open."
            
            # Handle web URLs
            if app_name.startswith(('http://', 'https://', 'www.')):
                return self._open_url(app_name)
            
            # Handle specific websites/services
            if app_name in ['youtube', 'youtube.com']:
                return self._open_url('https://youtube.com')
            elif app_name in ['google', 'google.com']:
                return self._open_url('https://google.com')
            elif app_name in ['github', 'github.com']:
                return self._open_url('https://github.com')
            elif app_name in ['gmail', 'email']:
                return self._open_url('https://gmail.com')
            
            # Handle local applications
            return self._open_application(app_name)
            
        except Exception as e:
            logger.error(f"Error opening application: {e}")
            return f"Failed to open application: {e}"
    
    def _open_url(self, url: str) -> str:
        """Open URL in default browser"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            webbrowser.open(url)
            return f"Opened {url} in your default browser."
            
        except Exception as e:
            logger.error(f"Error opening URL: {e}")
            return f"Failed to open URL: {e}"
    
    def _open_application(self, app_name: str) -> str:
        """Open local application"""
        try:
            # Check if app is in our mappings
            app_command = None
            for mapped_name, command in self.app_mappings.items():
                if app_name.lower() in mapped_name.lower() or mapped_name.lower() in app_name.lower():
                    app_command = command
                    break
            
            if not app_command:
                # Try direct command
                app_command = app_name
            
            # Execute command based on OS
            if self.system == 'windows':
                subprocess.Popen(app_command, shell=True)
            elif self.system == 'darwin':
                if not app_command.startswith('open'):
                    app_command = f'open -a "{app_command}"'
                subprocess.Popen(app_command, shell=True)
            else:  # Linux
                subprocess.Popen(app_command, shell=True)
            
            return f"Opened {app_name}."
            
        except FileNotFoundError:
            return f"Application '{app_name}' not found on your system."
        except Exception as e:
            logger.error(f"Error opening application {app_name}: {e}")
            return f"Failed to open {app_name}: {e}"
    
    def _handle_close_command(self, command: str) -> str:
        """Handle application closing commands"""
        try:
            # Extract application name
            for prefix in ['close ', 'quit ', 'stop ']:
                if command.startswith(prefix):
                    app_name = command[len(prefix):].strip()
                    break
            else:
                return "Could not identify application to close."
            
            if self.system == 'windows':
                # Use taskkill on Windows
                result = subprocess.run(['taskkill', '/f', '/im', f'{app_name}.exe'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    return f"Closed {app_name}."
                else:
                    return f"Could not close {app_name} - it may not be running."
            
            elif self.system == 'darwin':
                # Use osascript on macOS
                script = f'tell application "{app_name}" to quit'
                result = subprocess.run(['osascript', '-e', script], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    return f"Closed {app_name}."
                else:
                    return f"Could not close {app_name} - it may not be running."
            
            else:  # Linux
                # Use pkill on Linux
                result = subprocess.run(['pkill', '-f', app_name], 
                                      capture_output=True, text=True)
                return f"Attempted to close {app_name}."
            
        except Exception as e:
            logger.error(f"Error closing application: {e}")
            return f"Failed to close application: {e}"
    
    def _handle_system_command(self, command: str) -> str:
        """Handle system-level commands"""
        try:
            if 'shutdown' in command:
                return self._confirm_system_action("shutdown", "shut down")
            elif 'restart' in command:
                return self._confirm_system_action("restart", "restart")
            elif 'sleep' in command:
                return self._system_sleep()
            elif 'lock' in command:
                return self._system_lock()
            
            return "System command not recognized."
            
        except Exception as e:
            logger.error(f"Error executing system command: {e}")
            return f"Failed to execute system command: {e}"
    
    def _confirm_system_action(self, action: str, action_name: str) -> str:
        """Request confirmation for critical system actions"""
        return (f"System {action_name} requires explicit confirmation for safety. "
                f"Please use your system's built-in {action_name} method or confirm this action manually.")
    
    def _system_sleep(self) -> str:
        """Put system to sleep"""
        try:
            if self.system == 'windows':
                subprocess.run(['rundll32.exe', 'powrprof.dll,SetSuspendState', '0,1,0'])
            elif self.system == 'darwin':
                subprocess.run(['pmset', 'sleepnow'])
            else:  # Linux
                subprocess.run(['systemctl', 'suspend'])
            
            return "System is going to sleep."
            
        except Exception as e:
            logger.error(f"Error putting system to sleep: {e}")
            return f"Failed to put system to sleep: {e}"
    
    def _system_lock(self) -> str:
        """Lock the system"""
        try:
            if self.system == 'windows':
                subprocess.run(['rundll32.exe', 'user32.dll,LockWorkStation'])
            elif self.system == 'darwin':
                subprocess.run(['/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession', '-suspend'])
            else:  # Linux
                subprocess.run(['loginctl', 'lock-session'])
            
            return "System locked."
            
        except Exception as e:
            logger.error(f"Error locking system: {e}")
            return f"Failed to lock system: {e}"
    
    def _handle_file_operation(self, command: str) -> str:
        """Handle basic file operations"""
        try:
            if 'create file' in command:
                return "File creation requires specific file path. Please use your file manager or specify the complete path."
            elif 'delete file' in command:
                return "File deletion requires explicit confirmation and file path for safety."
            elif 'copy file' in command:
                return "File copying requires source and destination paths. Please use your file manager."
            
            return "File operation not supported through voice commands for safety."
            
        except Exception as e:
            logger.error(f"Error in file operation: {e}")
            return f"File operation failed: {e}"
    
    def _handle_volume_control(self, command: str) -> str:
        """Handle volume control commands"""
        try:
            if self.system == 'windows':
                return "Volume control through Windows requires additional setup. Please use your system volume controls."
            elif self.system == 'darwin':
                if 'volume up' in command:
                    subprocess.run(['osascript', '-e', 'set volume output volume (output volume of (get volume settings) + 10)'])
                    return "Volume increased."
                elif 'volume down' in command:
                    subprocess.run(['osascript', '-e', 'set volume output volume (output volume of (get volume settings) - 10)'])
                    return "Volume decreased."
                elif 'mute' in command:
                    subprocess.run(['osascript', '-e', 'set volume output muted true'])
                    return "Audio muted."
            else:  # Linux
                return "Volume control through Linux requires additional audio system setup."
            
        except Exception as e:
            logger.error(f"Error controlling volume: {e}")
            return f"Volume control failed: {e}"
    
    def get_running_applications(self) -> Dict[str, Any]:
        """Get list of currently running applications"""
        try:
            running_apps = []
            
            if self.system == 'windows':
                result = subprocess.run(['tasklist', '/fo', 'csv'], capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    for line in lines[1:10]:  # First 10 processes
                        parts = line.split(',')
                        if len(parts) > 0:
                            app_name = parts[0].strip('"')
                            running_apps.append(app_name)
            
            elif self.system == 'darwin':
                result = subprocess.run(['ps', '-A', '-o', 'comm'], capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    running_apps = [line.strip() for line in lines[1:10]]  # First 10
            
            else:  # Linux
                result = subprocess.run(['ps', '-eo', 'comm', '--no-headers'], capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    running_apps = list(set(lines[:10]))  # First 10 unique
            
            return {
                'running_applications': running_apps,
                'system': self.system,
                'total_found': len(running_apps)
            }
            
        except Exception as e:
            logger.error(f"Error getting running applications: {e}")
            return {'error': str(e)}
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get basic system information"""
        try:
            import psutil
            
            return {
                'system': platform.system(),
                'platform': platform.platform(),
                'processor': platform.processor(),
                'cpu_percent': psutil.cpu_percent(),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent if self.system != 'windows' else psutil.disk_usage('C:\\').percent
            }
            
        except ImportError:
            return {
                'system': platform.system(),
                'platform': platform.platform(),
                'note': 'Install psutil for detailed system information'
            }
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            return {'error': str(e)}
