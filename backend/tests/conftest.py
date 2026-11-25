from pathlib import Path
import pytest

_FIXTURES = Path(__file__).resolve().parents[1].parent / "fixtures"


@pytest.fixture(autouse=True)
def _isolated_db(tmp_path, monkeypatch):
    monkeypatch.setenv("数据目录", str(tmp_path))
    monkeypatch.setenv("夹具目录", str(_FIXTURES))
    import app.db as db
    db.数据目录 = Path(tmp_path)
    db.夹具目录 = _FIXTURES
    db.库路径 = db.数据目录 / "探栏.db"
    from app import seed
    seed.初始化库()
    yield
