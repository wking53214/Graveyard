import hashlib
import json
import sqlite3
from typing import Any, Optional

from .models import LineageEvent, LineageRecord


class LineageEngine:

    def __init__(self, storage_path: Optional[str] = None):
        self.records = {}
        self._canonical_payloads = {}
        self.events = []
        self._connection = None
        if storage_path is not None:
            self._connection = sqlite3.connect(storage_path)
            self._connection.execute(
                """
                CREATE TABLE IF NOT EXISTS lineage_snapshots (
                    subject_id TEXT PRIMARY KEY,
                    payload BLOB NOT NULL
                )
                """
            )
            self._connection.execute(
                """
                CREATE TABLE IF NOT EXISTS lineage_events (
                    sequence INTEGER PRIMARY KEY,
                    event_type TEXT NOT NULL,
                    subject_id TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    previous_hash TEXT,
                    event_hash TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            self._connection.commit()
            self._load_storage()

    def _load_storage(self):
        rows = self._connection.execute(
            """
            SELECT sequence, event_type, subject_id, payload,
                   previous_hash, event_hash, created_at
            FROM lineage_events
            ORDER BY sequence
            """
        ).fetchall()
        for row in rows:
            self.events.append(
                LineageEvent(
                    row[0],
                    row[1],
                    row[2],
                    json.loads(row[3]),
                    row[4],
                    row[5],
                )
            )

        for subject_id, payload in self._connection.execute(
            "SELECT subject_id, payload FROM lineage_snapshots"
        ):
            self._canonical_payloads[subject_id] = bytes(payload)

        for event in self.events:
            if event.event_type == "LINEAGE_TRANSITION":
                data = event.payload
                self.records[event.subject_id] = LineageRecord(
                    artifact_id=event.subject_id,
                    canonical_hash=data["canonical_hash"],
                    parent_artifact_id=data["parent_artifact_id"],
                    parent_hash=data["parent_hash"],
                    branch_id=data["branch_id"],
                    lineage_hash=data["lineage_hash"],
                    version=data["version"],
                    provenance_status=data["provenance_status"],
                )
            elif event.event_type == "PARENT_LINK":
                record = self.records.get(event.subject_id)
                if record is not None:
                    record.parent_artifact_id = event.payload["parent_artifact_id"]
                    record.parent_hash = event.payload["parent_hash"]

    def _append_event(self, event_type: str, subject_id: str, payload: dict):
        event_data = {
            "sequence": len(self.events) + 1,
            "event_type": event_type,
            "subject_id": subject_id,
            "payload": payload,
            "previous_hash": self.events[-1].event_hash if self.events else "",
        }
        event_hash = self.hash_artifact(
            self.canonicalize_artifact(event_data)
        )
        event = LineageEvent(
            event_data["sequence"],
            event_type,
            subject_id,
            payload,
            event_data["previous_hash"] or None,
            event_hash,
        )
        self.events.append(event)
        if self._connection is not None:
            self._connection.execute(
                """
                INSERT INTO lineage_events
                (sequence, event_type, subject_id, payload, previous_hash,
                 event_hash, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event.sequence,
                    event.event_type,
                    event.subject_id,
                    json.dumps(event.payload, sort_keys=True, separators=(",", ":")),
                    event.previous_hash,
                    event.event_hash,
                    event.created_at.isoformat(),
                ),
            )
            self._connection.commit()
        return event

    @staticmethod
    def canonicalize_artifact(payload: Any) -> bytes:
        if payload is None:
            payload = {}

        if isinstance(payload, (bytes, bytearray)):
            return bytes(payload)

        if hasattr(payload, "__dict__"):
            payload = vars(payload)

        if isinstance(payload, str):
            return payload.encode("utf-8")

        try:
            return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        except TypeError:
            return str(payload).encode("utf-8")

    @staticmethod
    def hash_artifact(canonical_bytes: bytes) -> str:
        return hashlib.sha256(canonical_bytes).hexdigest()

    def _build_lineage_hash(
        self,
        subject_id: str,
        canonical_hash: str,
        parent_artifact_id: Optional[str] = None,
        branch_id: Optional[str] = None,
        provenance_status: Optional[str] = None,
        version: int = 1,
    ) -> str:
        parent_record = self.records.get(parent_artifact_id) if parent_artifact_id else None
        parent_hash = parent_record.canonical_hash if parent_record else None
        payload = {
            "subject_id": subject_id,
            "canonical_hash": canonical_hash,
            "parent_artifact_id": parent_artifact_id or "",
            "parent_hash": parent_hash or "",
            "branch_id": branch_id or "",
            "provenance_status": provenance_status or "",
            "version": version,
        }
        return hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()

    def record_lineage_transition(
        self,
        subject_id: str,
        payload: Any,
        parent_artifact_id: Optional[str] = None,
        branch_id: Optional[str] = None,
        provenance_status: Optional[str] = None,
        version: int = 1,
    ) -> LineageRecord:
        canonical_bytes = self.canonicalize_artifact(payload)
        canonical_hash = self.hash_artifact(canonical_bytes)
        self._canonical_payloads[subject_id] = canonical_bytes
        if self._connection is not None:
            self._connection.execute(
                """
                INSERT OR REPLACE INTO lineage_snapshots (subject_id, payload)
                VALUES (?, ?)
                """,
                (subject_id, canonical_bytes),
            )
            self._connection.commit()

        record = self.records.get(subject_id)
        if record is None:
            record = LineageRecord(
                artifact_id=subject_id,
                canonical_hash=canonical_hash,
                version=version,
                provenance_status=provenance_status,
            )

        record.canonical_hash = canonical_hash
        record.version = version
        record.provenance_status = provenance_status or record.provenance_status

        if parent_artifact_id is not None:
            record.parent_artifact_id = parent_artifact_id
            parent_record = self.records.get(parent_artifact_id)
            if parent_record is not None:
                record.parent_hash = parent_record.canonical_hash

        if branch_id is not None:
            record.branch_id = branch_id

        record.lineage_hash = self._build_lineage_hash(
            subject_id,
            canonical_hash,
            parent_artifact_id=record.parent_artifact_id,
            branch_id=record.branch_id,
            provenance_status=record.provenance_status,
            version=record.version,
        )

        self.records[subject_id] = record
        self._append_event(
            "LINEAGE_TRANSITION",
            subject_id,
            {
                "canonical_hash": record.canonical_hash,
                "parent_artifact_id": record.parent_artifact_id,
                "parent_hash": record.parent_hash,
                "branch_id": record.branch_id,
                "lineage_hash": record.lineage_hash,
                "version": record.version,
                "provenance_status": record.provenance_status,
            },
        )
        return record

    def link_parent_artifact(self, child_id: str, parent_id: str) -> LineageRecord:
        record = self.records.get(child_id)
        if record is None:
            record = LineageRecord(artifact_id=child_id, canonical_hash="")
        record.parent_artifact_id = parent_id
        parent_record = self.records.get(parent_id)
        if parent_record is not None:
            record.parent_hash = parent_record.canonical_hash
        self.records[child_id] = record
        self._append_event(
            "PARENT_LINK",
            child_id,
            {
                "parent_artifact_id": parent_id,
                "parent_hash": record.parent_hash,
            },
        )
        return record

    def verify_events(self) -> bool:
        previous_hash = None
        for expected_sequence, event in enumerate(self.events, start=1):
            if event.sequence != expected_sequence:
                return False
            event_data = {
                "sequence": event.sequence,
                "event_type": event.event_type,
                "subject_id": event.subject_id,
                "payload": event.payload,
                "previous_hash": previous_hash or "",
            }
            expected_hash = self.hash_artifact(
                self.canonicalize_artifact(event_data)
            )
            if (
                event.previous_hash != previous_hash
                or event.event_hash != expected_hash
            ):
                return False
            previous_hash = event.event_hash
        return True

    def snapshot(self, subject_id: str) -> Optional[bytes]:
        snapshot = self._canonical_payloads.get(subject_id)
        return bytes(snapshot) if snapshot is not None else None

    def verify_lineage(self, subject_id: str, payload: Any = None) -> bool:
        record = self.records.get(subject_id)
        if record is None:
            return False
        if not self.verify_events():
            return False
        canonical_bytes = self._canonical_payloads.get(subject_id)
        if canonical_bytes is None:
            return False

        expected_canonical_hash = self.hash_artifact(canonical_bytes)
        if payload is not None:
            expected_canonical_hash = self.hash_artifact(
                self.canonicalize_artifact(payload)
            )
        if record.canonical_hash != expected_canonical_hash:
            return False

        parent_record = (
            self.records.get(record.parent_artifact_id)
            if record.parent_artifact_id
            else None
        )
        if record.parent_artifact_id and (
            parent_record is None
            or record.parent_hash != parent_record.canonical_hash
        ):
            return False

        expected_lineage_hash = self._build_lineage_hash(
            record.artifact_id,
            expected_canonical_hash,
            parent_artifact_id=record.parent_artifact_id,
            branch_id=record.branch_id,
            provenance_status=record.provenance_status,
            version=record.version,
        )
        return record.lineage_hash == expected_lineage_hash


__all__ = ["LineageEngine"]
