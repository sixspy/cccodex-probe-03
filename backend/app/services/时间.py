"""观测时工具。"""
from __future__ import annotations
from datetime import datetime, timedelta, timezone


def 解析时(s: str) -> datetime:
    s = (s or "").replace("Z", "+00:00")
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def 比较观测序(a: str, b: str) -> int:
    ta, tb = 解析时(a), 解析时(b)
    if ta < tb:
        return -1
    if ta > tb:
        return 1
    return 0


def 是否跨日界(栏参考时: str, 观测时: str) -> bool:
    return 解析时(栏参考时).date() != 解析时(观测时).date()


def 格式栏号(前缀: str, 时刻: str) -> str:
    t = 解析时(时刻)
    return f"{前缀}-{t.strftime('%Y%m%d')}"


def 漂移秒(站点时: str, 仓时: str) -> float:
    return abs((解析时(站点时) - 解析时(仓时)).total_seconds())


def 推进日(时刻: str, 天: int = 1) -> str:
    t = 解析时(时刻) + timedelta(days=天)
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def 是否可解析(s: str) -> bool:
    try:
        解析时(s)
        return True
    except Exception:
        return False


def 观测序排序键(观测时: str) -> datetime:
    return 解析时(观测时)
