/** 探栏页面模块：verify · 栏贯验
 * 真实页面在 backend/app/static；本模块提供文案与汇总辅助。
 */
export const PAGE = 'verify';
export const TITLE = '栏贯验';
export const STAGE = {
  load: "装载：校验站点/指标/读数/观测时后写入观测报文",
  gate: "入栏：过质控门槛进缓冲，否则进坏点匣",
  close: "结栏：按站点+指标汇总均值物化",
  verify: "贯验：已汇总缓冲报文数须等于汇总账报文数之和",
};
export function fateChip(fate) {
  const map = {"已入栏":"ok","在栏":"ok","已汇总":"ok","已坏点":"warn","撕裂":"danger","对齐":"ok"};
  return { text: fate, tone: map[fate] || "" };
}
export function summarizeLoad(r) {
  if (!r) return "";
  return `入流 ${r["入流"]||0} · 入栏 ${r["入栏"]||0} · 坏点 ${r["坏点"]||0} · 驳回 ${r["驳回"]||0}`;
}
export function summarizeClose(r) {
  if (!r) return "";
  return `栏 ${r["栏号"]||"?"} · 汇总 ${r["汇总数"]||0} · 缓冲消耗 ${r["缓冲消耗"]||0}`;
}
export function summarizeVerify(r) {
  if (!r) return "";
  return `${r["是否对齐"]?"对齐":"撕裂"} · 在栏 ${r["在栏"]} · 汇总报文 ${r["汇总报文"]} · 坏点 ${r["坏点"]}`;
}
export function assertBoneCopy() {
  return "去皮：质控门槛入栏管道。勿做成告警大屏，勿抄潮切窗号或对拍左右轨。";
}
export function buildMetrics(o) {
  o = o || {};
  return [
    { key: "观测报文", value: o["观测报文"] || 0 },
    { key: "在栏", value: o["在栏"] || 0 },
    { key: "站点汇总", value: o["站点汇总"] || 0 },
    { key: "坏点", value: o["坏点"] || 0 },
  ];
}

export function emptyTip(kind) {
  const m = {
    observe: "尚无报文。请在探栏台灌入栏成汇总样例。",
    buffer: "入栏为空。要么尚未过门槛，要么已经结栏汇总。",
    summary: "尚无汇总。入栏后点结当前栏。",
    bad: "坏点匣为空。灌坏点样例可看到越界旁路。",
    verify: "尚无贯验。结栏后点跑栏贯验。",
  };
  return m[kind] || "暂无数据";
}
export function gateLabel(rules) {
  if (!rules) return "栏规未加载";
  return `${rules["当前栏号"] || "?"} · PM25 ${rules["PM25下限"] || "?"}~${rules["PM25上限"] || "?"}`;
}
export function groupByStation(rows) {
  const g = {};
  for (const r of rows || []) {
    const k = r["站点键"] || "_";
    (g[k] ||= []).push(r);
  }
  return g;
}
export function meanOf(rows) {
  if (!rows || !rows.length) return 0;
  return rows.reduce((s, r) => s + Number(r["读数"] || 0), 0) / rows.length;
}
export function verifyExplainer(row) {
  if (!row) return "";
  return row["是否对齐"] ? "入栏已汇总与站点汇总报文数一致。" : (row["说明"] || "栏账撕裂");
}
export function boneDiffersFromTide() {
  return "探栏是质控门槛入栏；潮切是事件时关窗；对拍是双轨对齐。";
}

export function verifyColumns() {
  return ["时刻", "在栏笔数", "汇总报文数", "坏点笔数", "是否对齐", "说明"];
}
export function alignTone(ok) {
  return ok ? "ok" : "warn";
}
export function verifyHint() {
  return "撕裂时先查结栏是否漏组，或汇总账是否被旁路写入。";
}
