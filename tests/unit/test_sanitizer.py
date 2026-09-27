from k8s_triage.k8s.sanitizer import process_logs, sanitize_logs, truncate_logs


def test_sanitize_logs() -> None:
    raw_log = 'connecting to DB with password="my-super-secret-password"'
    sanitized = sanitize_logs(raw_log)
    assert 'my-super-secret-password' not in sanitized
    assert '[REDACTED]' in sanitized
    
    raw_log_2 = 'Bearer abcdef123456 token string'
    sanitized_2 = sanitize_logs(raw_log_2)
    assert 'abcdef123456' not in sanitized_2
    assert '[REDACTED]' in sanitized_2


def test_truncate_logs() -> None:
    raw_log = "a" * 15000
    truncated = truncate_logs(raw_log, max_chars=12000)
    assert len(truncated) == 12000
    
    raw_log_short = "a" * 100
    truncated_short = truncate_logs(raw_log_short, max_chars=12000)
    assert len(truncated_short) == 100


def test_process_logs() -> None:
    raw_log = "a" * 15000 + ' aws_access_key_id=AKIAIOSFODNN7EXAMPLE'
    processed = process_logs(raw_log)
    assert len(processed) <= 12000
    assert 'AKIAIOSFODNN7EXAMPLE' not in processed
