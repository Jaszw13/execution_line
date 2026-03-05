def calculate_kill_line_risk(
    region: str,  # "US" 或 "HK"
    monthly_income: float,  # 月稳定收入
    monthly_rigid_expenses: float,  # 月刚性支出（房租/房贷、账单、保险等）
    cash_savings: float,  # 现金/活期储蓄
    total_debt: float,  # 总债务（信用卡、贷款等）
    net_assets: float,  # 净资产（总资产-总负债）
    has_medical_insurance: bool,  # 是否有稳定医保/医疗险
    has_unemployment_insurance: bool,  # 是否有失业保险（仅美国）
    is_negative_equity: bool = False,  # 是否负资产（仅香港，按揭物业市值<未还贷款）
    has_domestic_helper: bool = False,  # 是否雇佣外籍家庭佣工（仅香港）
    children_in_private_school: bool = False  # 子女是否读直资/国际学校（仅香港）
) -> dict:
    """
    计算个人/家庭触及“斩杀线”的风险等级
    返回: {"risk_level": "高风险/中风险/低风险", "trigger_factors": [触发风险的关键因素]}
    """
    trigger_factors = []
    
    # ---------------- 美国地区逻辑 ----------------
    if region == "US":
        # 1. 应急储蓄缓冲：现金<3个月刚性支出 或 无法覆盖400美元意外
        if cash_savings < monthly_rigid_expenses * 3:
            trigger_factors.append("应急储蓄不足3个月刚性支出")
        if cash_savings < 400:
            trigger_factors.append("无法覆盖400美元意外开支")
        
        # 2. 收支与债务压力：刚性支出>收入70% 或 债务收入比>40%
        if monthly_rigid_expenses / monthly_income > 0.7:
            trigger_factors.append("月度刚性支出占收入超70%")
        if total_debt / (monthly_income * 12) > 0.4:  # 债务/年收入
            trigger_factors.append("债务收入比超40%")
        
        # 3. 资产底线：净资产<14万美元（约100万人民币）
        if net_assets < 140000:
            trigger_factors.append("家庭净资产低于14万美元")
        
        # 4. 制度护盾缺失：无医保或失业保险
        if not has_medical_insurance:
            trigger_factors.append("无稳定医保")
        if not has_unemployment_insurance:
            trigger_factors.append("无失业保险")
        
        # 风险判定：满足3个及以上因素为高风险，1-2个为中风险，0个为低风险
        if len(trigger_factors) >= 3:
            risk_level = "高风险（已触及斩杀线）"
        elif 1 <= len(trigger_factors) <= 2:
            risk_level = "中风险（接近斩杀线）"
        else:
            risk_level = "低风险（安全）"
    
    # ---------------- 香港地区逻辑 ----------------
    elif region == "HK":
        # 1. 核心触发：负资产 + 现金流枯竭
        if is_negative_equity:
            trigger_factors.append("持有负资产物业")
        if cash_savings < monthly_rigid_expenses * 3:
            trigger_factors.append("应急储蓄不足3个月刚性支出")
        
        # 2. 中产刚性支出压力（香港特色）
        if has_domestic_helper:
            trigger_factors.append("需承担外籍家庭佣工开支")
        if children_in_private_school:
            trigger_factors.append("需承担直资/国际学校学费")
        
        # 3. 债务与收支压力
        if monthly_rigid_expenses / monthly_income > 0.7:
            trigger_factors.append("月度刚性支出占收入超70%")
        
        # 风险判定：负资产+现金流枯竭为高风险；满足2个因素为中风险；否则低风险
        if is_negative_equity and cash_savings < monthly_rigid_expenses * 3:
            risk_level = "高风险（已触及斩杀线）"
        elif len(trigger_factors) >= 2:
            risk_level = "中风险（接近斩杀线）"
        else:
            risk_level = "低风险（安全）"
    
    else:
        raise ValueError("地区仅支持 'US' 或 'HK'")
    
    return {"risk_level": risk_level, "trigger_factors": trigger_factors}