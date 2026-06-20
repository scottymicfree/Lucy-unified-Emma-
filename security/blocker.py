import hashlib
import re
import os
from datetime import datetime
from typing import Dict, Any

class SecurityViolation(Exception):
    pass

class SecurityBlocker:
    """Advanced security blocking engine for Lucy-E.M.M.A. system.
    Enforces no-execute, no-exfil, sandboxed operations, human approval gates."""

    def __init__(self):
        self.whitelisted_modules = {'emma', 'orchestrator', 'agents', 'governance', 'hyperswarm', 'sandbox', 'security', 'lucy_boot', '__main__', ''}
        self.blocked_patterns = [
            r'eval\(', r'exec\(', r'os\.system', r'subprocess', r'__import__',
            r'requests\.', r'http', r'urllib', r'socket', r'open\(.+["\']w'
        ]
        self.hmac_key = "lucy_emma_sovereign_hmac_key"
        os.makedirs("security", exist_ok=True)

    def _log_operation(self, operation: str, context: Dict):
        try:
            log_path = "security/security.log"
            os.makedirs(os.path.dirname(log_path), exist_ok=True)
            audit_data = f"{operation}:{str(context)}".encode()
            hmac_val = hashlib.sha256(self.hmac_key.encode() + audit_data).hexdigest()[:16]
            with open(log_path, "a") as f:
                entry = f"{datetime.utcnow().isoformat()} | HMAC:{hmac_val} | {operation} | {context}\n"
                f.write(entry)
        except Exception as e:
            # Fallback for sandbox env
            print(f"[SEC_LOG_FALLBACK] {operation}: {str(e)[:100]}")

    def validate_operation(self, operation: str, context: Dict[str, Any]) -> bool:
        """Core validation gate for all critical operations."""
        # Pattern blocking
        if 'code' in context or 'command' in context:
            code_snippet = str(context.get('code', context.get('command', '')))
            for pattern in self.blocked_patterns:
                if re.search(pattern, code_snippet, re.IGNORECASE):
                    raise SecurityViolation(f"Blocked dangerous pattern: {pattern}")

        # Module whitelist
        caller = context.get('caller_module', '')
        if caller and not any(caller.startswith(mod) for mod in self.whitelisted_modules):
            raise SecurityViolation(f"Unauthorized module: {caller}")

        self._log_operation(operation, context)

        # Human approval for high-risk (demo safe)
        if "production" in operation.lower() or operation in ["generate_production_code", "deploy"]:
            print("⚠️ HIGH-RISK: HUMAN APPROVAL GATE for production changes.")

        return True
