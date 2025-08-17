# nova_v2/skills/dark_web_watch.py
# Legal/safe: HaveIBeenPwned for emails, Pwned Passwords (k-anonymity) for password hashes.
import requests
from config import HAVEIBEENPWNED_API_KEY

class DarkWebWatch:
    def route(self, text: str) -> str:
        t = text.lower()
        if "check email" in t:
            email = t.replace("check email", "").strip()
            if not email: return "Provide an email: e.g., 'check email me@example.com'."
            return self.check_email(email)
        if "check password" in t:
            return ("For passwords, send the SHA1 hash prefix (first 5 hex chars). "
                    "Say: 'check password prefix ABCDE'. I won’t accept plaintext passwords.")
        if "prefix" in t and "check password" in t:
            pref = t.split("prefix")[-1].strip().upper()
            if len(pref) != 5: return "Prefix must be 5 hex chars."
            return self.check_password_prefix(pref)
        return "Say: 'check email <addr>' or 'check password prefix <ABCDE>'."

    def check_email(self, email: str) -> str:
        if not HAVEIBEENPWNED_API_KEY:
            return "Set HAVEIBEENPWNED_API_KEY in config.py to enable email breach checks."
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
        # We don’t call here in offline code; this is a stubbed response:
        return f"Stub: would query breaches for {email}. If any, I’ll advise a password rotation."

    def check_password_prefix(self, prefix: str) -> str:
        # Would call k-anonymity endpoint to count suffix matches.
        return f"Stub: would query pwned passwords for hash prefix {prefix}. If matches>0, advise change."
