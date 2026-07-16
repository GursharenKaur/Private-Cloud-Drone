import logging
from pathlib import Path

# ==========================================
# Log Directory
# ==========================================

LOG_DIRECTORY = Path("logs")
LOG_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)

LOG_FILE = LOG_DIRECTORY / "audit.log"

# ==========================================
# Audit Logger
# ==========================================

audit_logger = logging.getLogger("audit")

audit_logger.setLevel(logging.INFO)

if not audit_logger.handlers:

    file_handler = logging.FileHandler(LOG_FILE)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler.setFormatter(formatter)

    audit_logger.addHandler(file_handler)

    # ==========================================
# Audit Logging Helper
# ==========================================

def log_security_event(
    event: str,
) -> None:
    """
    Record a security-related audit event.
    """

    audit_logger.info(event)

