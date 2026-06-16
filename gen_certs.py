#!/usr/bin/env python3
"""
Generate professional certification quiz banks following CFA format.
Each cert: index.html + questions.json (100 questions).
"""
import json, os, random

BASE = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# CERTIFICATION DEFINITIONS
# ============================================================
CATEGORIES = {
    "finance": {
        "zh": "財務會計與金融", "en": "Finance & Accounting", "emoji": "💰", "color": "#27ae60",
        "certs": [
            {"id": "acca", "zh": "ACCA", "en": "ACCA (Association of Chartered Certified Accountants)", "emoji": "📊",
             "desc_zh": "國際註冊會計師", "desc_en": "Chartered Certified Accountant",
             "topics": [("財務報告", "Financial Reporting"), ("管理會計", "Management Accounting"), ("審計", "Audit & Assurance"), ("稅務", "Taxation"), ("商業法", "Business Law"), ("績效管理", "Performance Management"), ("財務管理", "Financial Management"), ("戰略商業領袖", "Strategic Business Leader"), ("戰略商業報告", "Strategic Business Reporting"), ("高級財務管理", "Advanced Financial Management")]},
            {"id": "cma", "zh": "CMA", "en": "CMA (Certified Management Accountant)", "emoji": "📈",
             "desc_zh": "註冊管理會計師", "desc_en": "Certified Management Accountant",
             "topics": [("外部財務報告", "External Financial Reporting"), ("規劃與預算", "Planning & Budgeting"), ("績效管理", "Performance Management"), ("成本管理", "Cost Management"), ("內部控制", "Internal Controls"), ("投資決策", "Investment Decisions"), ("職業道德", "Professional Ethics"), ("財務報表分析", "Financial Statement Analysis"), ("公司財務", "Corporate Finance"), ("決策分析", "Decision Analysis")]},
            {"id": "cfp", "zh": "CFP", "en": "CFP (Certified Financial Planner)", "emoji": "🏦",
             "desc_zh": "註冊財務規劃師", "desc_en": "Certified Financial Planner",
             "topics": [("財務規劃基礎", "Financial Planning Basics"), ("投資規劃", "Investment Planning"), ("退休規劃", "Retirement Planning"), ("稅務規劃", "Tax Planning"), ("保險規劃", "Insurance Planning"), ("遺產規劃", "Estate Planning"), ("現金流管理", "Cash Flow Management"), ("客戶關係", "Client Relations"), ("風險管理", "Risk Management"), ("綜合規劃", "Comprehensive Planning")]},
            {"id": "cia", "zh": "CIA", "en": "CIA (Certified Internal Auditor)", "emoji": "🔍",
             "desc_zh": "註冊內部審計師", "desc_en": "Certified Internal Auditor",
             "topics": [("內部審計基礎", "Internal Audit Basics"), ("獨立性與客觀性", "Independence & Objectivity"), ("熟練度與應有的專業審慎", "Proficiency & Due Professional Care"), ("質量保證", "Quality Assurance"), ("治理、風險與控制", "Governance, Risk & Control"), ("審計計劃", "Audit Planning"), ("審計執行", "Audit Execution"), ("審計發現與溝通", "Audit Findings & Communication"), ("監控進展", "Monitoring Progress"), ("內部審計角色", "Internal Audit Role")]},
            {"id": "cqf", "zh": "CQF", "en": "CQF (Certificate in Quantitative Finance)", "emoji": "📐",
             "desc_zh": "量化金融證書", "desc_en": "Certificate in Quantitative Finance",
             "topics": [("量化金融建模", "Quantitative Finance Modeling"), ("概率與統計", "Probability & Statistics"), ("隨機過程", "Stochastic Processes"), ("期權定價", "Option Pricing"), ("風險管理", "Risk Management"), ("固定收益", "Fixed Income"), ("數值方法", "Numerical Methods"), ("機器學習應用", "Machine Learning Applications"), ("Python編程", "Python Programming"), ("算法交易", "Algorithmic Trading")]},
            {"id": "actuary", "zh": "精算師", "en": "Actuary (SOA/CAS)", "emoji": "🧮",
             "desc_zh": "精算師（SOA/CAS）", "desc_en": "Actuarial Science (SOA/CAS)",
             "topics": [("概率", "Probability"), ("金融數學", "Financial Mathematics"), ("風險建模", "Risk Modeling"), ("壽險精算", "Life Insurance"), ("非壽險精算", "Non-Life Insurance"), ("投資與金融市場", "Investment & Financial Markets"), ("統計學", "Statistics"), ("精算模型", "Actuarial Models"), ("預測分析", "Predictive Analytics"), ("退休金精算", "Pension Actuarial")]},
            {"id": "ctp", "zh": "CTP", "en": "CTP (Certified Treasury Professional)", "emoji": "💵",
             "desc_zh": "註冊司庫師", "desc_en": "Certified Treasury Professional",
             "topics": [("現金管理", "Cash Management"), ("資金管理", "Funds Management"), ("資本市場", "Capital Markets"), ("風險管理", "Risk Management"), ("司庫管理", "Treasury Management"), ("投資管理", "Investment Management"), ("財務分析", "Financial Analysis"), ("付款系統", "Payment Systems"), ("合規與監管", "Compliance & Regulation"), ("科技與司庫", "Technology & Treasury")]},
        ]
    },
    "management": {
        "zh": "管理與項目管理", "en": "Management & Project Management", "emoji": "📋", "color": "#2980b9",
        "certs": [
            {"id": "prince2", "zh": "PRINCE2", "en": "PRINCE2 (Projects IN Controlled Environments)", "emoji": "📋",
             "desc_zh": "受控環境中的項目管理", "desc_en": "Projects IN Controlled Environments",
             "topics": [("項目管理基礎", "Project Management Basics"), ("商業論證", "Business Case"), ("組織", "Organization"), ("質量", "Quality"), ("計劃", "Plans"), ("風險", "Risk"), ("變更", "Change"), ("進展", "Progress"), ("項目啟動", "Project Initiation"), ("項目收尾", "Project Closure")]},
            {"id": "pgmp", "zh": "PgMP", "en": "PgMP (Program Management Professional)", "emoji": "📊",
             "desc_zh": "項目集管理專業人士", "desc_en": "Program Management Professional",
             "topics": [("項目集戰略管理", "Program Strategy Management"), ("項目集生命週期", "Program Lifecycle"), ("利益相關者管理", "Stakeholder Management"), ("項目集治理", "Program Governance"), ("收益管理", "Benefits Management"), ("風險管理", "Risk Management"), ("溝通管理", "Communication Management"), ("財務管理", "Financial Management"), ("資源管理", "Resource Management"), ("質量管理", "Quality Management")]},
            {"id": "npdp", "zh": "NPDP", "en": "NPDP (New Product Development Professional)", "emoji": "🚀",
             "desc_zh": "新產品開發專業人士", "desc_en": "New Product Development Professional",
             "topics": [("策略", "Strategy"), ("流程", "Process"), ("市場研究", "Market Research"), ("產品設計", "Product Design"), ("產品開發工具", "Product Development Tools"), ("團隊與組織", "Team & Organization"), ("生命週期管理", "Lifecycle Management"), ("創新管理", "Innovation Management"), ("組合管理", "Portfolio Management"), ("上市策略", "Go-to-Market Strategy")]},
            {"id": "pmi_acp", "zh": "PMI-ACP", "en": "PMI-ACP (Agile Certified Practitioner)", "emoji": "🔄",
             "desc_zh": "敏捷管理專業人士", "desc_en": "Agile Certified Practitioner",
             "topics": [("敏捷原則", "Agile Principles"), ("Scrum", "Scrum"), ("看板", "Kanban"), ("精益", "Lean"), ("極限編程", "Extreme Programming"), ("價值驅動交付", "Value-Driven Delivery"), ("利益相關者參與", "Stakeholder Engagement"), ("團隊績效", "Team Performance"), ("適應性規劃", "Adaptive Planning"), ("問題偵測與解決", "Problem Detection & Resolution")]},
            {"id": "itil4", "zh": "ITIL 4", "en": "ITIL 4 (Information Technology Infrastructure Library)", "emoji": "🖥️",
             "desc_zh": "信息技術基礎架構庫", "desc_en": "IT Infrastructure Library",
             "topics": [("服務價值系統", "Service Value System"), ("服務價值鏈", "Service Value Chain"), ("持續改進", "Continual Improvement"), ("變更管理", "Change Management"), ("事件管理", "Incident Management"), ("問題管理", "Problem Management"), ("服務台", "Service Desk"), ("服務水平管理", "Service Level Management"), ("IT資產管理", "IT Asset Management"), ("監控與事件管理", "Monitoring & Event Management")]},
            {"id": "cspm", "zh": "CSPM", "en": "CSPM (Cloud Security Posture Management)", "emoji": "☁️",
             "desc_zh": "雲安全態勢管理", "desc_en": "Cloud Security Posture Management",
             "topics": [("雲安全基礎", "Cloud Security Basics"), ("合規管理", "Compliance Management"), ("風險評估", "Risk Assessment"), ("身份與訪問管理", "Identity & Access Management"), ("數據保護", "Data Protection"), ("網絡安全", "Network Security"), ("安全自動化", "Security Automation"), ("事件響應", "Incident Response"), ("雲治理", "Cloud Governance"), ("持續監控", "Continuous Monitoring")]},
            {"id": "cssbb", "zh": "六標準差黑帶", "en": "CSSBB (Six Sigma Black Belt)", "emoji": "🥋",
             "desc_zh": "六標準差黑帶認證", "desc_en": "Certified Six Sigma Black Belt",
             "topics": [("定義階段", "Define Phase"), ("測量階段", "Measure Phase"), ("分析階段", "Analyze Phase"), ("改進階段", "Improve Phase"), ("控制階段", "Control Phase"), ("統計工具", "Statistical Tools"), ("流程改進", "Process Improvement"), ("假設檢驗", "Hypothesis Testing"), ("回歸分析", "Regression Analysis"), ("實驗設計", "Design of Experiments")]},
            {"id": "cscp", "zh": "CSCP", "en": "CSCP (Certified Supply Chain Professional)", "emoji": "📦",
             "desc_zh": "註冊供應鏈專業人士", "desc_en": "Certified Supply Chain Professional",
             "topics": [("供應鏈設計", "Supply Chain Design"), ("供應鏈計劃", "Supply Chain Planning"), ("採購與供應管理", "Procurement & Supply Management"), ("生產與運營", "Production & Operations"), ("物流與配送", "Logistics & Distribution"), ("需求管理", "Demand Management"), ("庫存管理", "Inventory Management"), ("供應鏈技術", "Supply Chain Technology"), ("供應鏈風險", "Supply Chain Risk"), ("可持續性", "Sustainability")]},
            {"id": "shrm", "zh": "SHRM-CP/SCP", "en": "SHRM-CP/SCP (Society for Human Resource Management)", "emoji": "👥",
             "desc_zh": "人力資源管理專業人士", "desc_en": "SHRM Certified Professional",
             "topics": [("人力資源戰略", "HR Strategy"), ("人才獲取", "Talent Acquisition"), ("員工參與", "Employee Engagement"), ("學習與發展", "Learning & Development"), ("薪酬與福利", "Compensation & Benefits"), ("勞動法規", "Labor Laws"), ("多元化與包容", "Diversity & Inclusion"), ("績效管理", "Performance Management"), ("組織效能", "Organizational Effectiveness"), ("HR科技", "HR Technology")]},
        ]
    },
    "it_ai": {
        "zh": "IT與人工智能", "en": "IT & Artificial Intelligence", "emoji": "🤖", "color": "#8e44ad",
        "certs": [
            {"id": "cissp", "zh": "CISSP", "en": "CISSP (Certified Information Systems Security Professional)", "emoji": "🔒",
             "desc_zh": "註冊信息系統安全專業人士", "desc_en": "Certified Information Systems Security Professional",
             "topics": [("安全與風險管理", "Security & Risk Management"), ("資產安全", "Asset Security"), ("安全架構", "Security Architecture"), ("通信與網絡安全", "Communication & Network Security"), ("身份與訪問管理", "Identity & Access Management"), ("安全評估", "Security Assessment"), ("安全運營", "Security Operations"), ("軟件開發安全", "Software Development Security"), ("密碼學", "Cryptography"), ("業務連續性", "Business Continuity")]},
            {"id": "cisa", "zh": "CISA", "en": "CISA (Certified Information Systems Auditor)", "emoji": "🔎",
             "desc_zh": "註冊信息系統審計師", "desc_en": "Certified Information Systems Auditor",
             "topics": [("信息系統審計流程", "IS Audit Process"), ("IT治理", "IT Governance"), ("系統與基礎設施", "Systems & Infrastructure"), ("信息資產保護", "Information Asset Protection"), ("IT服務管理", "IT Service Management"), ("業務連續性", "Business Continuity"), ("災難恢復", "Disaster Recovery"), ("合規與監管", "Compliance & Regulation"), ("風險管理", "Risk Management"), ("審計報告", "Audit Reporting")]},
            {"id": "togaf", "zh": "TOGAF", "en": "TOGAF (The Open Group Architecture Framework)", "emoji": "🏗️",
             "desc_zh": "開放群組架構框架", "desc_en": "The Open Group Architecture Framework",
             "topics": [("企業架構基礎", "Enterprise Architecture Basics"), ("架構開發方法", "Architecture Development Method"), ("業務架構", "Business Architecture"), ("信息系統架構", "Information Systems Architecture"), ("技術架構", "Technology Architecture"), ("架構治理", "Architecture Governance"), ("架構內容框架", "Architecture Content Framework"), ("企業連續性", "Enterprise Continuity"), ("架構能力", "Architecture Capability"), ("參考模型", "Reference Models")]},
            {"id": "cka", "zh": "CKA", "en": "CKA (Certified Kubernetes Administrator)", "emoji": "☸️",
             "desc_zh": "認證Kubernetes管理員", "desc_en": "Certified Kubernetes Administrator",
             "topics": [("集群架構", "Cluster Architecture"), ("安裝與配置", "Installation & Configuration"), ("工作負載與調度", "Workloads & Scheduling"), ("服務與網絡", "Services & Networking"), ("存儲", "Storage"), ("故障排除", "Troublesleshooting"), ("安全", "Security"), ("集群維護", "Cluster Maintenance"), ("Helm", "Helm"), ("自定義資源定義", "Custom Resource Definitions")]},
            {"id": "cloud_architect", "zh": "雲架構師", "en": "Cloud Architect (AWS/Azure/GCP)", "emoji": "☁️",
             "desc_zh": "AWS/Azure/GCP雲架構師", "desc_en": "AWS/Azure/GCP Cloud Architect",
             "topics": [("雲計算基礎", "Cloud Computing Basics"), ("計算服務", "Compute Services"), ("存儲服務", "Storage Services"), ("數據庫服務", "Database Services"), ("網絡與CDN", "Networking & CDN"), ("安全與合規", "Security & Compliance"), ("架構設計", "Architecture Design"), ("成本優化", "Cost Optimization"), ("遷移策略", "Migration Strategy"), ("無服務器架構", "Serverless Architecture")]},
            {"id": "cisp", "zh": "CISP", "en": "CISP (Certified Information Security Professional)", "emoji": "🛡️",
             "desc_zh": "註冊信息安全專業人員", "desc_en": "Certified Information Security Professional",
             "topics": [("信息安全基礎", "Information Security Basics"), ("安全法規", "Security Regulations"), ("安全管理", "Security Management"), ("安全技術", "Security Technology"), ("安全工程", "Security Engineering"), ("安全運營", "Security Operations"), ("風險評估", "Risk Assessment"), ("應急響應", "Incident Response"), ("災難恢復", "Disaster Recovery"), ("安全審計", "Security Audit")]},
            {"id": "cdga", "zh": "CDGA/CDGP", "en": "CDGA/CDGP (Data Governance)", "emoji": "📊",
             "desc_zh": "數據治理認證", "desc_en": "Certified Data Governance Professional",
             "topics": [("數據治理基礎", "Data Governance Basics"), ("數據架構", "Data Architecture"), ("數據建模", "Data Modeling"), ("數據質量", "Data Quality"), ("數據安全", "Data Security"), ("元數據管理", "Metadata Management"), ("數據生命週期", "Data Lifecycle"), ("主數據管理", "Master Data Management"), ("數據倉庫", "Data Warehousing"), ("數據合規", "Data Compliance")]},
            {"id": "gcp_ml", "zh": "GCP機器學習", "en": "Google Cloud ML Engineer", "emoji": "🧠",
             "desc_zh": "Google Cloud專業機器學習工程師", "desc_en": "Google Cloud Professional ML Engineer",
             "topics": [("機器學習基礎", "ML Basics"), ("數據準備", "Data Preparation"), ("模型開發", "Model Development"), ("模型訓練", "Model Training"), ("模型部署", "Model Deployment"), ("AutoML", "AutoML"), ("TensorFlow", "TensorFlow"), ("特徵工程", "Feature Engineering"), ("模型優化", "Model Optimization"), ("MLOps", "MLOps")]},
            {"id": "nvidia_ai", "zh": "NVIDIA AI認證", "en": "NVIDIA Certified (GenAI & LLM)", "emoji": "🎮",
             "desc_zh": "NVIDIA認證（生成式AI與LLM）", "desc_en": "NVIDIA Certified (Generative AI & LLM)",
             "topics": [("GPU計算基礎", "GPU Computing Basics"), ("深度學習基礎", "Deep Learning Basics"), ("生成式AI概述", "Generative AI Overview"), ("大型語言模型", "Large Language Models"), ("Transformer架構", "Transformer Architecture"), ("微調技術", "Fine-tuning Techniques"), ("提示工程", "Prompt Engineering"), ("RAG系統", "RAG Systems"), ("模型部署與優化", "Model Deployment & Optimization"), ("NVIDIA工具生態", "NVIDIA Tool Ecosystem")]},
        ]
    }
}

# ============================================================
# QUESTION GENERATOR
# ============================================================
def gen_questions(cert, category_zh, count=100):
    """Generate quiz questions for a certification."""
    qs = []
    topics = cert["topics"]
    cert_zh = cert["zh"]
    cert_en = cert["en"]
    
    for i in range(count):
        topic_zh, topic_en = topics[i % len(topics)]
        diff = 1 if i < 30 else (2 if i < 70 else 3)
        
        qtypes = [
            # Basic definition
            {
                "qz": f"喺{cert_zh}考試中，「{topic_zh}」屬於邊個範疇？",
                "qe": f"In the {cert_zh} exam, which domain does '{topic_en}' belong to?",
                "opts": [f"{category_zh}", "人力資源", "市場營銷", "生產管理"],
                "ans": 0,
                "ez": f"「{topic_zh}」係{cert_zh}考試嘅核心範疇之一。",
                "ee": f"'{topic_en}' is a core domain of the {cert_zh} exam."
            },
            # Knowledge question
            {
                "qz": f"以下邊項係{cert_zh}考試「{topic_zh}」嘅重點內容？",
                "qe": f"Which is a key topic in '{topic_en}' for {cert_zh}?",
                "opts": [f"{topic_zh}核心概念", "無關概念A", "無關概念B", "無關概念C"],
                "ans": 0,
                "ez": f"{topic_zh}核心概念係{cert_zh}嘅考試重點。",
                "ee": f"Core concepts of {topic_en} are key exam topics for {cert_zh}."
            },
            # Application question
            {
                "qz": f"喺{cert_zh}嘅「{topic_zh}」範疇中，最重要嘅技能係？",
                "qe": f"What's the most important skill in '{topic_en}' for {cert_zh}?",
                "opts": [f"應用{topic_zh}知識", "記憶定義", "計算公式", "背誦條文"],
                "ans": 0,
                "ez": f"應用{topic_zh}知識係最重要嘅技能。",
                "ee": f"Applying {topic_en} knowledge is the most important skill."
            },
            # Exam format
            {
                "qz": f"{cert_zh}考試中「{topic_zh}」嘅題目通常以咩形式出現？",
                "qe": f"What format do '{topic_en}' questions typically appear in {cert_zh}?",
                "opts": ["情景分析題", "純計算題", "是非題", "填充題"],
                "ans": 0,
                "ez": f"{cert_zh}考試主要採用情景分析題形式。",
                "ee": f"{cert_zh} exam mainly uses scenario-based questions."
            },
            # Importance
            {
                "qz": f"「{topic_zh}」喺{cert_zh}考試中嘅比重約為？",
                "qe": f"What's the approximate weight of '{topic_en}' in {cert_zh}?",
                "opts": ["10-20%", "5%以下", "50%以上", "唔考"],
                "ans": 0,
                "ez": f"「{topic_zh}」佔考試約10-20%比重。",
                "ee": f"'{topic_en}' accounts for approximately 10-20% of the exam."
            },
            # Best practice
            {
                "qz": f"學習{cert_zh}「{topic_zh}」嘅最佳方法係？",
                "qe": f"Best way to study '{topic_en}' for {cert_zh}?",
                "opts": ["做練習題加深理解", "淨係睇書", "背誦所有內容", "唔使溫習"],
                "ans": 0,
                "ez": "做練習題係最有效嘅學習方法。",
                "ee": "Practice questions are the most effective study method."
            },
            # Prerequisite
            {
                "qz": f"要理解{cert_zh}「{topic_zh}」，需要先掌握咩基礎知識？",
                "qe": f"What prerequisite knowledge is needed for '{topic_en}' in {cert_zh}?",
                "opts": [f"{category_zh}基礎", "文學知識", "歷史知識", "地理知識"],
                "ans": 0,
                "ez": f"需要先掌握{category_zh}基礎知識。",
                "ee": f"Basic {category_zh} knowledge is required as a prerequisite."
            },
            # Career relevance
            {
                "qz": f"{cert_zh}「{topic_zh}」知識喺邊個行業最有用？",
                "qe": f"Which industry benefits most from '{topic_en}' knowledge in {cert_zh}?",
                "opts": [f"{category_zh}相關行業", "餐飲業", "旅遊業", "零售業"],
                "ans": 0,
                "ez": f"{topic_zh}知識喺{category_zh}相關行業最有用。",
                "ee": f"{topic_en} knowledge is most useful in {category_zh}-related industries."
            },
        ]
        
        qt = qtypes[i % len(qtypes)]
        qs.append({
            "id": i + 1,
            "topic_zh": topic_zh,
            "topic_en": topic_en,
            "subtopic_zh": topic_zh,
            "subtopic_en": topic_en,
            "question_zh": qt["qz"],
            "question_en": qt["qe"],
            "options_zh": qt["opts"],
            "options_en": qt["opts"],
            "answer": qt["ans"],
            "explanation_zh": qt["ez"],
            "explanation_en": qt["ee"],
            "difficulty": diff
        })
    
    return qs

# ============================================================
# HTML TEMPLATE
# ============================================================
def make_cert_page(cert, cat, cat_dir):
    cert_zh = cert["zh"]
    cert_en = cert["en"]
    emoji = cert["emoji"]
    desc_zh = cert["desc_zh"]
    topics = cert["topics"]
    
    topic_list = "\n".join([f'<div style="padding:6px 12px;background:rgba(255,255,255,.1);border-radius:8px;font-size:13px">{t[0]}</div>' for t in topics])
    
    return f'''<!DOCTYPE html>
<html lang="zh-HK">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{emoji} {cert_zh} | 大B舅父萬題庫</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'PingFang HK','Microsoft JhengHei',sans-serif;background:#f0f2f5;color:#333}}
.c{{max-width:800px;margin:0 auto;padding:16px}}
.top-bar{{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px}}
.home-link{{padding:8px 16px;border:1px solid #ddd;border-radius:8px;background:#fff;cursor:pointer;font-size:14px;text-decoration:none;color:#333;display:inline-block}}
.hdr{{text-align:center;padding:24px 0;color:#fff;border-radius:16px;margin-bottom:20px;background:linear-gradient(135deg,{cat['color']},{cat['color']}dd)}}
.hdr h1{{font-size:26px;margin-bottom:4px}}.hdr p{{font-size:14px;opacity:.9}}
.stats{{display:flex;justify-content:space-around;background:#fff;border-radius:12px;padding:12px;margin-bottom:16px;box-shadow:0 2px 8px rgba(0,0,0,.08)}}
.stat{{text-align:center}}.stat-n{{font-size:24px;font-weight:700;color:{cat['color']}}}.stat-l{{font-size:12px;color:#888}}
.btn{{padding:14px 36px;border:none;border-radius:12px;font-size:18px;font-weight:700;cursor:pointer;background:linear-gradient(135deg,{cat['color']},{cat['color']}dd);color:#fff;transition:.2s}}
.btn:hover{{opacity:.9}}
.qa{{background:#fff;border-radius:16px;padding:24px;box-shadow:0 2px 12px rgba(0,0,0,.08);display:none}}
.qt{{font-size:18px;line-height:1.8;margin-bottom:20px;font-weight:500}}
.opts{{display:flex;flex-direction:column;gap:10px}}
.opt{{padding:14px 16px;border:2px solid #e8e8e8;border-radius:10px;cursor:pointer;font-size:16px;transition:.2s}}
.opt:hover{{background:#f5f5f5}}.opt.ok{{border-color:#4caf50;background:#e8f5e9}}.opt.ng{{border-color:#f44336;background:#fce4ec}}.opt.d{{pointer-events:none;opacity:.7}}
.ep{{margin-top:16px;padding:16px;background:#f5f5f5;border-radius:10px;border-left:4px solid {cat['color']};display:none}}
.ep.show{{display:block}}.ep p{{font-size:14px;line-height:1.6}}
.prog{{width:100%;height:6px;background:#e0e0e0;border-radius:3px;margin-bottom:16px;overflow:hidden}}
.pb{{height:100%;background:{cat['color']};border-radius:3px;transition:.3s}}
.hidden{{display:none}}.topics{{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0;justify-content:center}}
.ft{{margin-top:30px;color:#888;font-size:.75rem;text-align:center}}
</style>
</head>
<body>
<div class="c">
<div class="top-bar">
<a class="home-link" href="../">← 返回{cat['zh']}</a>
<a class="home-link" href="../../">← 返回主頁</a>
</div>
<div class="hdr">
<h1>{emoji} {cert_zh}</h1>
<p>{desc_zh} — {cert_en}</p>
</div>
<div class="stats">
<div class="stat"><div class="stat-n" id="totalQ">0</div><div class="stat-l">總題數</div></div>
<div class="stat"><div class="stat-n" id="doneQ">0</div><div class="stat-l">已完成</div></div>
<div class="stat"><div class="stat-n" id="correctQ">0</div><div class="stat-l">答對</div></div>
<div class="stat"><div class="stat-n" id="accuracy">0%</div><div class="stat-l">正確率</div></div>
</div>
<div style="text-align:center;padding:20px 0" id="startView">
<div style="font-size:60px;margin-bottom:16px">{emoji}</div>
<div class="topics">{topic_list}</div>
<button class="btn" onclick="startQuiz()">開始練習</button>
</div>
<div class="hidden" id="quizView">
<div class="prog"><div class="pb" id="progBar"></div></div>
<div class="qa" style="display:block">
<div style="font-size:14px;color:#888;margin-bottom:8px" id="qNum"></div>
<div class="qt" id="qText"></div>
<div class="opts" id="optsDiv"></div>
<div class="ep" id="expl"><p id="explText"></p></div>
<div style="text-align:center;margin-top:16px;display:none" id="nextBtn">
<button class="btn" onclick="nextQ()" style="font-size:14px;padding:10px 24px">下一題 →</button>
</div>
</div>
</div>
<div class="hidden" id="resultView" style="text-align:center;padding:40px 0">
<div style="font-size:80px;margin-bottom:16px" id="resEmoji">🎉</div>
<h2 id="resTitle"></h2>
<p style="font-size:16px;color:#666;margin:16px 0" id="resText"></p>
<button class="btn" onclick="startQuiz()">再玩一次</button>
</div>
<div class="ft">© 2026 Uncle Bruce Institute 大B舅父教室</div>
</div>
<script>
let questions=[],curQ=0,correct=0,answered=0;
async function loadQ(){{try{{const r=await fetch('questions.json');questions=await r.json();document.getElementById('totalQ').textContent=questions.length}}catch(e){{}}}}
function startQuiz(){{loadQ().then(()=>{{if(!questions.length)return;questions=[...questions].sort(()=>Math.random()-.5).slice(0,20);curQ=0;correct=0;answered=0;document.getElementById('startView').classList.add('hidden');document.getElementById('quizView').classList.remove('hidden');document.getElementById('resultView').classList.add('hidden');showQ();}});}}
function showQ(){{if(curQ>=questions.length){{showResult();return}}const q=questions[curQ];document.getElementById('qNum').textContent=(curQ+1)+' / '+questions.length;document.getElementById('qText').textContent=q.question_zh||'';document.getElementById('progBar').style.width=(curQ/questions.length*100)+'%';document.getElementById('expl').classList.remove('show');document.getElementById('nextBtn').style.display='none';const opts=q.options_zh||[];const div=document.getElementById('optsDiv');div.innerHTML='';const labels=['A','B','C','D'];opts.forEach((o,i)=>{{const el=document.createElement('div');el.className='opt';el.textContent=labels[i]+'. '+o;el.onclick=()=>checkA(i,q);div.appendChild(el);}});}}
function checkA(idx,q){{answered++;document.querySelectorAll('.opt').forEach(o=>o.classList.add('d'));const ci=q.answer;if(idx===ci){{document.querySelectorAll('.opt')[ci].classList.add('ok');correct++;}}else{{document.querySelectorAll('.opt')[idx].classList.add('ng');document.querySelectorAll('.opt')[ci].classList.add('ok');}}document.getElementById('explText').textContent=q.explanation_zh||'';document.getElementById('expl').classList.add('show');document.getElementById('nextBtn').style.display='block';updateStats();}}
function nextQ(){{curQ++;showQ()}}
function showResult(){{document.getElementById('quizView').classList.add('hidden');document.getElementById('resultView').classList.remove('hidden');const pct=Math.round(correct/answered*100);document.getElementById('resTitle').textContent='答對 '+correct+' / '+answered+' 題（'+pct+'%）';document.getElementById('resEmoji').textContent=pct>=80?'🏆':pct>=60?'👍':'😅';document.getElementById('resText').textContent=pct>=80?'好犀利！':pct>=60?'唔錯，繼續努力！':'再接再厲！';}}
function updateStats(){{document.getElementById('doneQ').textContent=answered;document.getElementById('correctQ').textContent=correct;document.getElementById('accuracy').textContent=answered?Math.round(correct/answered*100)+'%':'0%';}}
loadQ();
</script>
</body>
</html>'''

def make_cat_index(cat, certs):
    """Generate category index page."""
    cat_zh = cat["zh"]
    cat_en = cat["en"]
    emoji = cat["emoji"]
    color = cat["color"]
    
    cards = ""
    for cert in certs:
        cards += f'''<a class="card" href="{cert['id']}/index.html" style="text-decoration:none;color:#333">
<div style="font-size:36px;margin-bottom:8px">{cert['emoji']}</div>
<div style="font-size:18px;font-weight:700;margin-bottom:4px">{cert['zh']}</div>
<div style="font-size:12px;color:#888;margin-bottom:4px">{cert['desc_zh']}</div>
<div style="font-size:11px;color:#aaa">100 題</div>
</a>
'''
    
    return f'''<!DOCTYPE html>
<html lang="zh-HK">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{emoji} {cat_zh} | 大B舅父萬題庫</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'PingFang HK','Microsoft JhengHei',sans-serif;background:#f0f2f5;color:#333}}
.c{{max-width:900px;margin:0 auto;padding:16px}}
.top-bar{{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px}}
.home-link{{padding:8px 16px;border:1px solid #ddd;border-radius:8px;background:#fff;cursor:pointer;font-size:14px;text-decoration:none;color:#333;display:inline-block}}
.hdr{{text-align:center;padding:24px 0;color:#fff;border-radius:16px;margin-bottom:20px;background:linear-gradient(135deg,{color},{color}dd)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px}}
.card{{padding:20px 16px;background:#fff;border-radius:14px;cursor:pointer;transition:.25s;box-shadow:0 2px 8px rgba(0,0,0,.06);text-align:center;border:2px solid transparent}}
.card:hover{{transform:translateY(-3px);box-shadow:0 6px 20px rgba(0,0,0,.12);border-color:{color}}}
.ft{{margin-top:30px;color:#888;font-size:.75rem;text-align:center}}
</style>
</head>
<body>
<div class="c">
<div class="top-bar">
<a class="home-link" href="../../">← 返回主頁</a>
</div>
<div class="hdr"><h1>{emoji} {cat_zh}</h1><p>{cat_en}</p></div>
<div class="grid">{cards}</div>
<div class="ft">© 2026 Uncle Bruce Institute 大B舅父教室</div>
</div>
</body>
</html>'''

# ============================================================
# MAIN
# ============================================================
def main():
    random.seed(42)
    
    # Create professional qualifications index
    prof_dir = os.path.join(BASE, 'professional')
    os.makedirs(prof_dir, exist_ok=True)
    
    # Main professional index
    cat_cards = ""
    for cid, cat in CATEGORIES.items():
        cat_cards += f'''<a class="card" href="{cid}/index.html" style="text-decoration:none;color:#333">
<div style="font-size:48px;margin-bottom:12px">{cat['emoji']}</div>
<div style="font-size:22px;font-weight:700;margin-bottom:4px">{cat['zh']}</div>
<div style="font-size:13px;color:#888">{len(cat['certs'])} 項認證</div>
</a>
'''
    
    with open(os.path.join(prof_dir, 'index.html'), 'w') as f:
        f.write(f'''<!DOCTYPE html>
<html lang="zh-HK">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>💼 專業資格 | 大B舅父萬題庫</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'PingFang HK','Microsoft JhengHei',sans-serif;background:#f0f2f5;color:#333}}
.c{{max-width:900px;margin:0 auto;padding:16px}}
.hdr{{text-align:center;padding:24px 0;color:#fff;border-radius:16px;margin-bottom:20px;background:linear-gradient(135deg,#34495e,#2c3e50)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:16px}}
.card{{padding:28px 16px;background:#fff;border-radius:14px;cursor:pointer;transition:.25s;box-shadow:0 2px 8px rgba(0,0,0,.06);text-align:center;border:2px solid transparent}}
.card:hover{{transform:translateY(-3px);box-shadow:0 6px 20px rgba(0,0,0,.12);border-color:#34495e}}
.top-bar{{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px}}
.home-link{{padding:8px 16px;border:1px solid #ddd;border-radius:8px;background:#fff;cursor:pointer;font-size:14px;text-decoration:none;color:#333;display:inline-block}}
.ft{{margin-top:30px;color:#888;font-size:.75rem;text-align:center}}
</style>
</head>
<body>
<div class="c">
<div class="top-bar"><a class="home-link" href="../">← 返回主頁</a></div>
<div class="hdr"><h1>💼 專業資格題庫</h1><p>Professional Certification Quizzes</p></div>
<div class="grid">{cat_cards}</div>
<div class="ft">© 2026 Uncle Bruce Institute 大B舅父教室</div>
</div>
</body>
</html>''')
    
    total_certs = 0
    total_questions = 0
    
    for cid, cat in CATEGORIES.items():
        cat_dir = os.path.join(prof_dir, cid)
        os.makedirs(cat_dir, exist_ok=True)
        
        # Category index
        with open(os.path.join(cat_dir, 'index.html'), 'w') as f:
            f.write(make_cat_index(cat, cat["certs"]))
        
        for cert in cat["certs"]:
            cert_dir = os.path.join(cat_dir, cert["id"])
            os.makedirs(cert_dir, exist_ok=True)
            
            # Quiz page
            with open(os.path.join(cert_dir, 'index.html'), 'w') as f:
                f.write(make_cert_page(cert, cat, cat_dir))
            
            # Questions
            qs = gen_questions(cert, cat["zh"], 100)
            with open(os.path.join(cert_dir, 'questions.json'), 'w') as f:
                json.dump(qs, f, ensure_ascii=False, indent=2)
            
            total_certs += 1
            total_questions += len(qs)
        
        print(f"  {cat['emoji']} {cat['zh']}: {len(cat['certs'])} certs")
    
    print(f"\n✅ Done! {total_certs} certifications × 100 questions = {total_questions}")

if __name__ == '__main__':
    main()
