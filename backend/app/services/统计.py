from __future__ import annotations
from app.db import 连接


def 报文命运() -> dict:
    conn = 连接()
    try:
        rows = conn.execute(
            "SELECT 命运, COUNT(*) AS c FROM 观测报文 GROUP BY 命运"
        ).fetchall()
        return {r["命运"]: r["c"] for r in rows}
    finally:
        conn.close()


def 缓冲命运() -> dict:
    conn = 连接()
    try:
        rows = conn.execute(
            "SELECT 命运, COUNT(*) AS c FROM 入栏缓冲 GROUP BY 命运"
        ).fetchall()
        return {r["命运"]: r["c"] for r in rows}
    finally:
        conn.close()


def 按站点报文() -> dict:
    conn = 连接()
    try:
        rows = conn.execute(
            "SELECT 站点键, COUNT(*) AS c FROM 观测报文 GROUP BY 站点键"
        ).fetchall()
        return {r["站点键"]: r["c"] for r in rows}
    finally:
        conn.close()


def 装载批次摘要(限制: int = 20) -> list[dict]:
    conn = 连接()
    try:
        rows = conn.execute(
            "SELECT 编号,时刻,入流,入栏,坏点 FROM 装载批次 ORDER BY 时刻 DESC LIMIT ?",
            (限制,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def 结栏批次摘要(限制: int = 20) -> list[dict]:
    conn = 连接()
    try:
        rows = conn.execute(
            "SELECT 编号,栏号,时刻,汇总数 FROM 结栏批次 ORDER BY 时刻 DESC LIMIT ?",
            (限制,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def 按指标汇总() -> dict:
    conn = 连接()
    try:
        rows = conn.execute(
            "SELECT 指标键, COUNT(*) AS c, COALESCE(AVG(均值),0) AS 均 FROM 站点汇总账 GROUP BY 指标键"
        ).fetchall()
        return {r["指标键"]: {"笔数": r["c"], "均值": r["均"]} for r in rows}
    finally:
        conn.close()
