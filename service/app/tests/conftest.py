import sys
from pathlib import Path

import pytest

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from service.app.main import app  # noqa: E402
from service.app.security import require_api_key  # noqa: E402


@pytest.fixture(autouse=True)
def override_api_key_dependency():
    """Automatically override API key dependency for all tests to bypass authentication."""
    # Override the API key dependency to bypass authentication in tests
    app.dependency_overrides[require_api_key] = lambda: None
    yield
    # remove the override after each test
    app.dependency_overrides.clear()
