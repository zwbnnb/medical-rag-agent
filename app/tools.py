from __future__ import annotations

from langchain_core.tools import tool


@tool
def classify_blood_pressure(systolic: float, diastolic: float) -> str:
    """根据收缩压/舒张压(mmHg)给出家庭监测示意分级。仅供 Demo，非诊疗。"""
    s, d = float(systolic), float(diastolic)
    if s >= 180 or d >= 120:
        level = "可能达到需紧急关注的示意区间"
        advice = "建议尽快就医或急诊评估，并告知症状。"
    elif s >= 140 or d >= 90:
        level = "高血压示意区间"
        advice = "建议规范复测并就医评估，勿自行停药/改药。"
    elif s >= 120 or d >= 80:
        level = "正常高值示意区间"
        advice = "建议生活方式管理并定期监测。"
    else:
        level = "大致正常示意区间"
        advice = "保持健康生活方式，按需定期监测。"
    return (
        f"输入：收缩压={s}, 舒张压={d} mmHg；分级={level}。"
        f"建议：{advice}（科普示意，非诊断）"
    )


@tool
def classify_blood_glucose(value_mmol_l: float, fasting: bool = True) -> str:
    """根据血糖(mmol/L)与是否空腹给出示意分级。仅供 Demo，非诊疗。"""
    v = float(value_mmol_l)
    if v < 3.9:
        level = "偏低/低血糖警惕示意"
        advice = "结合症状处理并尽快寻求医疗指导。"
    elif fasting:
        if v <= 6.1:
            level = "空腹大致正常示意"
            advice = "继续按医嘱监测。"
        else:
            level = "空腹偏高示意"
            advice = "建议复测并咨询医生，勿自行解读为确诊。"
    else:
        if v <= 7.8:
            level = "餐后示意可接受区间"
            advice = "记录场景，按医嘱随访。"
        else:
            level = "餐后偏高示意"
            advice = "建议复测并咨询医生。"
    mode = "空腹" if fasting else "非空腹/餐后示意"
    return (
        f"输入：血糖={v} mmol/L（{mode}）；分级={level}。"
        f"建议：{advice}（科普示意，非诊断）"
    )


@tool
def project_metrics_lookup(topic: str) -> str:
    """查询本 Demo 固化的课题量级指标（Residual-DPLS / GDSC）。topic 可为 dpls、gdsc、r2 等。"""
    t = (topic or "").lower()
    facts = {
        "dpls": "Residual-DPLS：主效应→残差结构学习→硬边特征→软融合；公开基准均值 R²≈0.84 量级。",
        "gdsc": "GDSC 5-FU 等任务：表达→AUC，全量面板重叠 n≈397；H2 Test R²≈0.27±0.15 量级。",
        "r2": "公开回归 Primary Core 均值 R²≈0.84；GDSC 药敏与 UCI 不可混平均。",
        "patent": "专利交底主题：残差通路 DPLS 主效应–交互软融合回归方法及系统。",
    }
    hits = [v for k, v in facts.items() if k in t or t in k]
    if not hits:
        hits = list(facts.values())
    return " | ".join(hits)


ALL_TOOLS = [classify_blood_pressure, classify_blood_glucose, project_metrics_lookup]
