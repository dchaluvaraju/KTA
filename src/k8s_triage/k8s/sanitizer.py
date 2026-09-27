import re

from k8s_triage.config import config

# Basic patterns for common secrets
SECRET_PATTERNS = [
    r"(?i)bearer\s+[a-zA-Z0-9\-\._~+]+",  # Bearer tokens
    r"eyJ[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+", # JWTs
    r"-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----(?:.|\n)*?-----END (?:RSA |OPENSSH )?PRIVATE KEY-----", # Private keys
    r"(?i)(?:password|secret|token|api_key|apikey|access_key)[\s:=]+[\"']?([a-zA-Z0-9\-\._~+/=]+)[\"']?", # Key-value secrets
    r"aws_access_key_id\s*=\s*[A-Z0-9]{20}", # AWS Access Key
    r"aws_secret_access_key\s*=\s*[a-zA-Z0-9/+=]{40}", # AWS Secret
]

def sanitize_logs(log_data: str) -> str:
    """Scrub sensitive information from logs."""
    if not log_data:
        return log_data

    sanitized = log_data
    for pattern in SECRET_PATTERNS:
        sanitized = re.sub(pattern, "[REDACTED]", sanitized)
    
    return sanitized

def truncate_logs(log_data: str, max_chars: int | None = None) -> str:
    """Truncate logs to a maximum character limit to protect context window."""
    limit = max_chars if max_chars is not None else config.max_log_chars
    if not log_data:
        return log_data
    
    if len(log_data) > limit:
        return log_data[-limit:]
    return log_data

def process_logs(log_data: str) -> str:
    """Apply both sanitization and truncation."""
    return sanitize_logs(truncate_logs(log_data))
