"""报文校验与门槛。"""
from __future__ import annotations

必填 = ("报文编号", "站点键", "指标键", "读数", "观测时")


def 校验报文(ev: dict) -> list[str]:
    if not isinstance(ev, dict):
        return ["报文不是对象"]
    错 = []
    for k in 必填:
        if ev.get(k) in (None, ""):
            错.append(f"缺字段:{k}")
    try:
        float(ev.get("读数"))
    except (TypeError, ValueError):
        错.append("读数非数值")
    编号 = str(ev.get("报文编号") or "")
    if 编号 and (" " in 编号 or "\t" in 编号):
        错.append("报文编号含空白")
    return 错


def 校验批次(体: dict) -> list[str]:
    if not isinstance(体, dict):
        return ["体须为对象"]
    报文 = 体.get("报文")
    if not isinstance(报文, list) or not 报文:
        return ["报文列表为空"]
    错 = []
    见 = set()
    for i, ev in enumerate(报文):
        for e in 校验报文(ev or {}):
            错.append(f"[{i}]{e}")
        编号 = str((ev or {}).get("报文编号", ""))
        if 编号 and 编号 in 见:
            错.append(f"[{i}]报文编号重复")
        if 编号:
            见.add(编号)
    return 错


def 过门槛(读数: float, 规: dict, 指标键: str) -> tuple[bool, str]:
    """基线：仅对 PM25 做上下限；其它指标默认过门槛。"""
    if 指标键 != "PM25":
        return True, "非PM25默认过门槛"
    try:
        lo = float(规.get("PM25下限", "0"))
        hi = float(规.get("PM25上限", "75"))
    except ValueError:
        return False, "栏规阈值损坏"
    if 读数 < lo or 读数 > hi:
        return False, f"PM25越界[{lo},{hi}]"
    return True, "过门槛"


def 摘要错误(错: list[str], 上限: int = 8) -> str:
    if not 错:
        return ""
    head = 错[:上限]
    more = len(错) - len(head)
    text = "; ".join(head)
    if more > 0:
        text += f" …另有{more}条"
    return text


def 校验栏规补丁(体: dict) -> list[str]:
    if not isinstance(体, dict):
        return ["栏规补丁须为对象"]
    错: list[str] = []
    for k in ("PM25上限", "PM25下限", "标定偏移上限"):
        if k in 体:
            try:
                float(体[k])
            except Exception:
                错.append(f"{k}非数值")
    if "PM25上限" in 体 and "PM25下限" in 体:
        try:
            if float(体["PM25下限"]) > float(体["PM25上限"]):
                错.append("PM25下限不得大于上限")
        except Exception:
            pass
    return 错


def 指标是否受控(指标键: str) -> bool:
    return 指标键 == "PM25"
