import sqlite3
from datetime import datetime
from typing import List, Optional
from .models import WisdomRecord, GovernanceCategory, RecordStatus
from .crypto import SovereignCryptoEngine
try:
    from ..security.blocker import SecurityBlocker, SecurityViolation
except ImportError:
    # Fallback for direct script runs
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from security.blocker import SecurityBlocker, SecurityViolation

class SecurityError(Exception):
    pass

class WisdomStore:
    def __init__(self, db_path: str = "wisdom.db"):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS wisdom_records (
                    id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    category TEXT NOT NULL,
                    law TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    source_hash TEXT NOT NULL,
                    status TEXT NOT NULL,
                    supersedes TEXT,
                    signature TEXT NOT NULL
                )
            """)
            conn.commit()
            print(f"[DEBUG] Database initialized at {self.db_path}")

    def append_law(self, record: WisdomRecord) -> str:
        """Signs and writes a new persistent law to E.M.M.A.'s core long-term memory."""
        # Security check before any mutation
        blocker = SecurityBlocker()
        blocker.validate_operation("append_law", {"record_id": record.id, "caller_module": "wisdom.storage"})

        record.signature = SovereignCryptoEngine.sign_record(record)
        
        with sqlite3.connect(self.db_path) as conn:
            if record.supersedes:
                conn.execute(
                    "UPDATE wisdom_records SET status = ? WHERE id = ?",
                    (RecordStatus.SUPERSEDED.value, record.supersedes)
                )
            
            conn.execute(
                """
                INSERT INTO wisdom_records (id, timestamp, category, law, confidence, source_hash, status, supersedes, signature)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.id,
                    record.timestamp.isoformat(),
                    record.category.value,
                    record.law,
                    record.confidence,
                    record.source_hash,
                    record.status.value,
                    record.supersedes,
                    record.signature
                )
            )
            conn.commit()
        return record.id

    def query_active_laws(self, category: Optional[GovernanceCategory] = None) -> List[WisdomRecord]:
        """Retrieves and cryptographically validates all currently active laws."""
        # Security check
        blocker = SecurityBlocker()
        blocker.validate_operation("query_active_laws", {"category": category, "caller_module": "wisdom.storage"})

        query = "SELECT * FROM wisdom_records WHERE status = 'ACTIVE'"
        params = []
        if category:
            query += " AND category = ?"
            params.append(category.value)

        active_records = []
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            for row in cursor.fetchall():
                record = WisdomRecord(
                    id=row[0],
                    timestamp=datetime.fromisoformat(row[1]),
                    category=GovernanceCategory(row[2]),
                    law=row[3],
                    confidence=row[4],
                    source_hash=row[5],
                    status=RecordStatus(row[6]),
                    supersedes=row[7],
                    signature=row[8]
                )
                # Enforce cryptographic barrier upon retrieval
                if not SovereignCryptoEngine.verify_record(record):
                    raise SecurityError(f"CRITICAL: Structural corruption detected on WisdomRecord {record.id}!")
                active_records.append(record)
        return active_records
