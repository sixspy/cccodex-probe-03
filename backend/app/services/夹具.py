from __future__ import annotations
import json
from app import db
from app.services import 校验


def 列表() -> list[str]:
    root = db.夹具目录
    if not root.is_dir():
        return []
    return sorted(p.stem for p in root.glob("*.json"))


def 读取(名: str) -> dict:
    p = db.夹具目录 / f"{名}.json"
    if not p.is_file():
        raise FileNotFoundError(名)
    return json.loads(p.read_text(encoding="utf-8"))


def 预检(名: str) -> dict:
    体 = 读取(名)
    错 = 校验.校验批次(体)
    return {
        "夹具": 名,
        "报文数": len(体.get("报文") or []),
        "是否可装": not 错,
        "错误": 错,
        "摘要": 校验.摘要错误(错) if 错 else "",
    }


def 全部预检() -> list[dict]:
    return [预检(n) for n in 列表()]
