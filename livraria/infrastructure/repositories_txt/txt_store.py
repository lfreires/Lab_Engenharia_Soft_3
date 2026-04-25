from __future__ import annotations

import json
from pathlib import Path


class TxtStore:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)
        if not self._path.exists():
            self._path.write_text("", encoding="utf-8")

    def read_all(self) -> list[dict]:
        lines = self._path.read_text(encoding="utf-8").splitlines()
        result = []
        for line in lines:
            line = line.strip()
            if line:
                try:
                    result.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
        return result

    def write_all(self, records: list[dict]) -> None:
        text = "\n".join(json.dumps(r, ensure_ascii=False) for r in records)
        self._path.write_text((text + "\n") if text else "", encoding="utf-8")

    def append(self, record: dict) -> None:
        line = json.dumps(record, ensure_ascii=False) + "\n"
        with self._path.open("a", encoding="utf-8") as f:
            f.write(line)
