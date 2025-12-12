from __future__ import annotations

from typing import Dict, Any, Optional


class AIClient:

    def __init__(self, app_name: str | None = None):
        self.app_name = app_name or "unknown_app"

    def health(self) -> Dict[str, Any]:
        return {"status": "ok", "app_name": self.app_name}
