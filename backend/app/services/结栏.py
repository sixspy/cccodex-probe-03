"""结栏：入栏缓冲按站点+指标汇总物化。"""
from __future__ import annotations
import json
import uuid
from collections import defaultdict
from app.db import 连接
from app.seed import 此刻
from app.services import 目录


def 结当前栏() -> dict:
    规 = 目录.栏规()
    栏号 = 规.get("当前栏号", "B-demo")
    批 = f"结栏-{uuid.uuid4().hex[:8]}"
    conn = 连接()
    try:
        rows = conn.execute(
            "SELECT * FROM 入栏缓冲 WHERE 栏号=? AND 命运='在栏'", (栏号,)
        ).fetchall()
        groups: dict[tuple[str, str], list] = defaultdict(list)
        for r in rows:
            groups[(r["站点键"], r["指标键"])].append(r)
        汇总 = 0
        明细 = []
        时刻 = 此刻()
        for (站点, 指标), evs in groups.items():
            均值 = sum(float(e["读数"]) for e in evs) / len(evs)
            编号 = f"汇-{栏号}-{站点}-{指标}-{uuid.uuid4().hex[:6]}"
            conn.execute(
                """INSERT INTO 站点汇总账(汇总编号,栏号,站点键,指标键,报文数,均值,物化时,命运)
                   VALUES (?,?,?,?,?,?,?,?)""",
                (编号, 栏号, 站点, 指标, len(evs), 均值, 时刻, "已汇总"),
            )
            for e in evs:
                conn.execute(
                    "UPDATE 入栏缓冲 SET 命运=? WHERE 报文编号=?",
                    ("已汇总", e["报文编号"]),
                )
                conn.execute(
                    "UPDATE 观测报文 SET 命运=? WHERE 报文编号=?",
                    ("已汇总", e["报文编号"]),
                )
            汇总 += 1
            明细.append({
                "汇总编号": 编号,
                "站点键": 站点,
                "指标键": 指标,
                "报文数": len(evs),
                "均值": round(均值, 4),
            })
        报告 = {
            "批次编号": 批,
            "栏号": 栏号,
            "汇总数": 汇总,
            "缓冲消耗": len(rows),
            "明细": 明细,
            "空栏": len(rows) == 0,
        }
        conn.execute(
            """INSERT INTO 结栏批次(编号,栏号,时刻,汇总数,报告) VALUES (?,?,?,?,?)""",
            (批, 栏号, 时刻, 汇总, json.dumps(报告, ensure_ascii=False)),
        )
        conn.commit()
        return 报告
    finally:
        conn.close()


def 预览结栏() -> dict:
    """只读：当前栏在栏缓冲按站点指标分组，不写库。"""
    规 = 目录.栏规()
    栏号 = 规.get("当前栏号", "B-demo")
    conn = 连接()
    try:
        rows = conn.execute(
            "SELECT * FROM 入栏缓冲 WHERE 栏号=? AND 命运='在栏'", (栏号,)
        ).fetchall()
        groups: dict[tuple[str, str], list] = defaultdict(list)
        for r in rows:
            groups[(r["站点键"], r["指标键"])].append(dict(r))
        预览 = []
        for (站点, 指标), evs in sorted(groups.items()):
            预览.append({
                "站点键": 站点,
                "指标键": 指标,
                "报文数": len(evs),
                "均值": round(sum(float(e["读数"]) for e in evs) / len(evs), 4),
            })
        return {"栏号": 栏号, "在栏": len(rows), "将汇总组": 预览}
    finally:
        conn.close()
