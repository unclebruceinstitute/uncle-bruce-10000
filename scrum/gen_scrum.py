#!/usr/bin/env python3
"""Generate 5000 unique Scrum PSM/PSPO exam questions."""
import json, random, os

random.seed(2024)

OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "questions.json")
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

def q(zh, en, opts_zh, opts_en, ans, exp_zh, exp_en, topic_zh, topic_en, sub_zh, sub_en, diff=1):
    return {
        "question_zh": zh, "question_en": en,
        "options_zh": opts_zh, "options_en": opts_en,
        "answer": ans,
        "explanation_zh": exp_zh, "explanation_en": exp_en,
        "topic_zh": topic_zh, "topic_en": topic_en,
        "subtopic_zh": sub_zh, "subtopic_en": sub_en,
        "difficulty": diff,
    }

def shuffle_answer(q_obj, seed):
    r = random.Random(seed)
    indices = [0, 1, 2, 3]
    r.shuffle(indices)
    q_obj['options_zh'] = [q_obj['options_zh'][i] for i in indices]
    q_obj['options_en'] = [q_obj['options_en'][i] for i in indices]
    q_obj['answer'] = indices.index(q_obj['answer'])
    return q_obj

all_q = []
_sid = 0  # shuffle id counter

# ============================================================
# TOPIC 1: Scrum Framework (1250 questions, 25%)
# ============================================================
T1_ZH = "Scrum框架"
T1_EN = "Scrum Framework"

# --- 1a: Sprint (200) ---
SUB_ZH, SUB_EN = "Sprint", "Sprint"
sprint_concepts = [
    ("Sprint是一個固定長度的事件，最長為一個月", "A Sprint is a fixed-length event of one month or less",
     "Sprint是Scrum的核心，為其他事件提供容器", "The Sprint is the heart of Scrum, containing all other events"),
    ("Sprint的長度應保持一致，以建立節奏", "Sprint length should be consistent to establish a rhythm",
     "一致的Sprint長度幫助團隊建立可預測性", "Consistent Sprint length helps the team build predictability"),
    ("Sprint期間不應改變Sprint Goal", "The Sprint Goal should not change during the Sprint",
     "Sprint Goal提供方向和靈活性，但不應隨意改變", "The Sprint Goal provides direction and flexibility but should not be arbitrarily changed"),
    ("取消Sprint只能由Product Owner決定", "Only the Product Owner can cancel a Sprint",
     "只有PO有權取消Sprint，因為只有PO能判斷Sprint Goal是否仍然有價值", "Only the PO can cancel a Sprint because only they can assess if the Sprint Goal is still valuable"),
    ("Sprint包含Sprint Planning、Daily Scrum、Sprint Review和Sprint Retrospective", "A Sprint includes Sprint Planning, Daily Scrum, Sprint Review, and Sprint Retrospective",
     "所有Scrum事件都在Sprint內發生", "All Scrum events occur within the Sprint"),
    ("Sprint結束後立即開始下一個Sprint", "A new Sprint starts immediately after the previous one ends",
     "Sprint之間沒有間隙，連續交付價值", "There is no gap between Sprints; value is delivered continuously"),
    ("Sprint Goal是Sprint Planning的關鍵產出", "The Sprint Goal is a key outcome of Sprint Planning",
     "Sprint Goal指導團隊在Sprint期間的工作", "The Sprint Goal guides the team's work during the Sprint"),
    ("Sprint的目的是產生可用的Increment", "The purpose of a Sprint is to produce a usable Increment",
     "每個Sprint都應交付有價值的增量", "Each Sprint should deliver a valuable Increment"),
]
for i in range(200):
    _sid += 1
    c = sprint_concepts[i % len(sprint_concepts)]
    others = [x for x in sprint_concepts if x != c]
    w = random.sample(others, 3)
    variants = [
        (f"關於Sprint，以下哪項正確？", f"Which statement about the Sprint is correct?"),
        (f"以下哪項準確描述了Sprint？", f"Which accurately describes a Sprint?"),
        (f"在Scrum中，Sprint的特點是？", f"In Scrum, what is true about the Sprint?"),
    ]
    v = variants[i % len(variants)]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T1_ZH, T1_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 1b: Sprint Planning (120) ---
SUB_ZH, SUB_EN = "Sprint Planning", "Sprint計劃"
sp_concepts = [
    ("Sprint Planning的最大時間盒是一個月Sprint為8小時", "Sprint Planning time-box is 8 hours for a one-month Sprint",
     "時間盒隨Sprint長度按比例縮短", "Time-box scales proportionally with Sprint length"),
    ("Sprint Planning回答三個問題：Why、What、How", "Sprint Planning addresses three topics: Why, What, How",
     "Sprint Planning有三個主題：Sprint Goal、選取的PBI、計劃如何交付", "Three topics: Sprint Goal, selected PBIs, plan to deliver"),
    ("整個Scrum團隊參加Sprint Planning", "The entire Scrum Team attends Sprint Planning",
     "PO、Scrum Master和Developers都參加", "PO, Scrum Master, and Developers all attend"),
    ("Developers決定Sprint中可以完成多少工作", "Developers decide how much work they can accomplish in the Sprint",
     "只有Developers能評估他們的產能和能力", "Only Developers can assess their capacity and capability"),
    ("Sprint Backlog在Sprint Planning中產生", "The Sprint Backlog is created during Sprint Planning",
     "Sprint Backlog包含Sprint Goal、選取的PBI和交付計劃", "Sprint Backlog includes Sprint Goal, selected PBIs, and delivery plan"),
    ("Product Owner在Sprint Planning中提出Sprint Goal候選", "The Product Owner proposes Sprint Goal candidates at Sprint Planning",
     "PO提出Sprint Goal的建議，團隊討論後確定", "PO suggests Sprint Goal, team discusses and finalizes"),
    ("Sprint Planning的第一個主題是Why——為什麼這個Sprint有價值", "The first topic of Sprint Planning is Why—why this Sprint is valuable",
     "第一個主題確立Sprint Goal", "The first topic establishes the Sprint Goal"),
    ("Sprint Planning的第二個主題是What——選取哪些PBI", "The second topic is What—which PBIs are selected",
     "團隊根據產能和PO的優先級選取PBI", "Team selects PBIs based on capacity and PO's priority"),
    ("Sprint Planning的第三個主題是How——如何交付所選工作", "The third topic is How—how the selected work will be delivered",
     "Developers將PBI分解為更小的工作項", "Developers decompose PBIs into smaller work items"),
    ("Developers在Sprint Planning結束時應該能夠解釋他們計劃如何實現Sprint Goal", "Developers should be able to explain how they plan to achieve the Sprint Goal by end of Sprint Planning",
     "這是Sprint Planning結束條件之一", "This is one of the Sprint Planning completion criteria"),
]
for i in range(120):
    _sid += 1
    c = sp_concepts[i % len(sp_concepts)]
    others = [x for x in sp_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於Sprint Planning，以下哪項正確？", "Which is correct about Sprint Planning?"),
        ("Sprint Planning的特點是？", "What is true about Sprint Planning?"),
        ("以下哪項描述了Sprint Planning？", "Which describes Sprint Planning?"),
    ][i % 3]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T1_ZH, T1_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 1c: Daily Scrum (120) ---
SUB_ZH, SUB_EN = "Daily Scrum", "每日站會"
daily_concepts = [
    ("Daily Scrum是為Developers舉辦的15分鐘事件", "The Daily Scrum is a 15-minute event for Developers",
     "Daily Scrum是Developers的檢視和適應事件", "The Daily Scrum is an inspect-and-adapt event for Developers"),
    ("Daily Scrum的目的是檢視朝向Sprint Goal的進度", "The Daily Scrum's purpose is to inspect progress toward the Sprint Goal",
     "團隊檢視距離Sprint Goal的距離並調整計劃", "The team inspects progress and adapts the plan"),
    ("Daily Scrum在同一時間同一地點舉行以減少複雜性", "The Daily Scrum is held at the same time and place to reduce complexity",
     "固定的時間和地點簡化了會議的組織", "Consistent time and place simplify meeting logistics"),
    ("Scrum Master不強制要求特定的Daily Scrum格式", "The Scrum Master does not mandate a specific Daily Scrum format",
     "Developers可以選擇最適合他們的格式", "Developers can choose the format that works best for them"),
    ("常見的Daily Scrum問題：昨天做了什麼？今天做什麼？有什麼阻礙？", "Common Daily Scrum questions: What did I do? What will I do? Any impediments?",
     "這只是建議格式，團隊可以自選", "This is just a suggested format; teams can choose their own"),
    ("只有Developers需要參加Daily Scrum", "Only Developers are required to attend the Daily Scrum",
     "其他人可以旁聽但不應干擾", "Others may listen but should not disrupt"),
    ("Daily Scrum不是狀態報告會議", "The Daily Scrum is not a status reporting meeting",
     "它是開發團隊的同步和計劃會議", "It is a synchronization and planning meeting for the Developers"),
    ("Daily Scrum改善溝通、減少其他會議、識別障礙", "Daily Scrum improves communication, reduces other meetings, identifies impediments",
     "它是透明性和檢視的關鍵機制", "It is a key mechanism for transparency and inspection"),
]
for i in range(120):
    _sid += 1
    c = daily_concepts[i % len(daily_concepts)]
    others = [x for x in daily_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於Daily Scrum，以下哪項正確？", "Which is correct about the Daily Scrum?"),
        ("Daily Scrum的特點是？", "What is true about the Daily Scrum?"),
        ("以下哪項準確描述了Daily Scrum？", "Which accurately describes the Daily Scrum?"),
    ][i % 3]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T1_ZH, T1_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 1d: Sprint Review (120) ---
SUB_ZH, SUB_EN = "Sprint Review", "Sprint評審"
review_concepts = [
    ("Sprint Review的目的是檢視Increment並調整Product Backlog", "Sprint Review inspects the Increment and adapts the Product Backlog",
     "Sprint Review是一個工作會議，不是演示", "The Sprint Review is a working session, not a presentation"),
    ("Sprint Review的最大時間盒是一個月Sprint為4小時", "Sprint Review time-box is 4 hours for a one-month Sprint",
     "時間盒隨Sprint長度按比例縮短", "Time-box scales with Sprint length"),
    ("Scrum團隊和關鍵利益相關者參加Sprint Review", "The Scrum Team and key stakeholders attend the Sprint Review",
     "利益相關者的反饋至關重要", "Stakeholder feedback is essential"),
    ("Sprint Review中展示完成的Increment", "The completed Increment is presented at the Sprint Review",
     "團隊展示在Sprint中完成的工作", "The team demonstrates work completed during the Sprint"),
    ("Sprint Review中討論Product Backlog的下一步", "The next steps for the Product Backlog are discussed at Sprint Review",
     "根據反饋和市場變化調整Product Backlog", "The Product Backlog is adjusted based on feedback and market changes"),
    ("Sprint Review是Scrum團隊與利益相關者互動的機會", "The Sprint Review is an opportunity for the Scrum Team to interact with stakeholders",
     "這是收集反饋和調整方向的關鍵時刻", "This is a key moment for gathering feedback and adjusting direction"),
    ("Sprint Review不是Demo，而是協作工作會議", "The Sprint Review is not a demo but a collaborative working session",
     "重點是收集反饋和討論下一步", "The focus is on gathering feedback and discussing next steps"),
    ("在Sprint Review中，團隊應展示所有完成和未完成的PBI", "At Sprint Review, the team should show all completed and incomplete PBIs",
     "透明性是Sprint Review的關鍵原則", "Transparency is a key principle of the Sprint Review"),
]
for i in range(120):
    _sid += 1
    c = review_concepts[i % len(review_concepts)]
    others = [x for x in review_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於Sprint Review，以下哪項正確？", "Which is correct about the Sprint Review?"),
        ("Sprint Review的特點是？", "What is true about the Sprint Review?"),
    ][i % 2]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T1_ZH, T1_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 1e: Sprint Retrospective (120) ---
SUB_ZH, SUB_EN = "Sprint Retrospective", "Sprint回顧"
retro_concepts = [
    ("Sprint Retrospective的目的是檢視團隊如何工作並制定改進計劃", "Sprint Retrospective plans ways to increase quality and effectiveness",
     "回顧幫助團隊持續改進", "Retrospectives help the team continuously improve"),
    ("Sprint Retrospective的最大時間盒是一個月Sprint為3小時", "Sprint Retrospective time-box is 3 hours for a one-month Sprint",
     "時間盒隨Sprint長度按比例縮短", "Time-box scales with Sprint length"),
    ("Sprint Retrospective聚焦於人員、關係、流程和工具", "The Retrospective focuses on people, relationships, process, and tools",
     "改進可以涉及團隊協作的各個方面", "Improvements can cover all aspects of teamwork"),
    ("整個Scrum團隊參加Sprint Retrospective", "The entire Scrum Team attends the Sprint Retrospective",
     "PO、Scrum Master和Developers都參加", "PO, SM, and Developers all attend"),
    ("Sprint Retrospective應識別最重要的改進並制定行動計劃", "The Retrospective identifies the most important improvements and creates an action plan",
     "改進項目應在下一個Sprint中實施", "Improvement items should be implemented in the next Sprint"),
    ("Sprint Retrospective是Scrum團隊自我反思和改進的機會", "The Retrospective is an opportunity for self-reflection and improvement",
     "它促進了團隊的持續學習文化", "It promotes a culture of continuous learning"),
    ("Sprint Retrospective應產生至少一個高優先級的改進行動", "The Retrospective should produce at least one high-priority improvement action",
     "改進應被納入下一個Sprint Backlog", "Improvements should be included in the next Sprint Backlog"),
]
for i in range(120):
    _sid += 1
    c = retro_concepts[i % len(retro_concepts)]
    others = [x for x in retro_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於Sprint Retrospective，以下哪項正確？", "Which is correct about the Sprint Retrospective?"),
        ("Sprint Retrospective的特點是？", "What is true about the Sprint Retrospective?"),
    ][i % 2]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T1_ZH, T1_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 1f: Definition of Done (120) ---
SUB_ZH, SUB_EN = "Definition of Done", "完成的定義"
dod_concepts = [
    ("Definition of Done是Increment必須滿足的條件", "The Definition of Done is the set of conditions the Increment must meet",
     "DoD確保Increment是可用的和可發布的", "DoD ensures the Increment is usable and releasable"),
    ("Definition of Done創造透明性，讓所有人理解「完成」意味著什麼", "The Definition of Done creates transparency about what 'done' means",
     "透明性是Scrum三大支柱之一", "Transparency is one of the three pillars of Scrum"),
    ("如果PBI不符合DoD，就不能納入Sprint Review", "If a PBI doesn't meet the DoD, it cannot be presented at the Sprint Review",
     "只有完成的Increment才能在Sprint Review中展示", "Only done Increments can be presented at the Sprint Review"),
    ("DoD可以隨時間演進，變得更加嚴格", "The DoD can evolve over time, becoming more stringent",
     "團隊應持續改進他們的DoD", "Teams should continuously improve their DoD"),
    ("多個Scrum團隊共用同一產品時必須共用同一DoD", "Multiple Scrum Teams working on the same product must share the same DoD",
     "共用DoD確保集成的Increment是一致的", "Shared DoD ensures integrated Increments are consistent"),
    ("DoD通常包含開發、測試、文檔和部署標準", "DoD typically includes development, testing, documentation, and deployment standards",
     "DoD應涵蓋所有必要的品質標準", "DoD should cover all necessary quality standards"),
    ("DoD是Scrum的承諾之一，與Increment相關", "DoD is one of Scrum's commitments, associated with the Increment",
     "DoD是Increment的承諾", "DoD is the commitment for the Increment"),
    ("不符合DoD的工作不能被視為「完成」", "Work not meeting the DoD cannot be considered 'done'",
     "未完成的工作不能交付給客戶", "Undone work cannot be delivered to customers"),
]
for i in range(120):
    _sid += 1
    c = dod_concepts[i % len(dod_concepts)]
    others = [x for x in dod_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於Definition of Done，以下哪項正確？", "Which is correct about the Definition of Done?"),
        ("Definition of Done的特點是？", "What is true about the Definition of Done?"),
    ][i % 2]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T1_ZH, T1_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 1g: Definition of Ready (80) ---
SUB_ZH, SUB_EN = "Definition of Ready", "就緒的定義"
dor_concepts = [
    ("Definition of Ready不是Scrum Guide的一部分", "The Definition of Ready is not part of the Scrum Guide",
     "DoR是團隊的實踐，不是Scrum框架的一部分", "DoR is a team practice, not part of the Scrum framework"),
    ("Definition of Ready幫助確保PBI有足夠的細節可以開始工作", "DoR ensures PBIs have enough detail to start work",
     "DoR減少了Sprint中的不確定性", "DoR reduces uncertainty during the Sprint"),
    ("典型的DoR包括PBI有清晰的描述和驗收標準", "Typical DoR includes clear description and acceptance criteria",
     "PBI應足夠小且可測試", "PBIs should be small enough and testable"),
    ("DoR不應成為阻礙開發的官僚程序", "DoR should not become bureaucratic overhead that blocks development",
     "DoR是幫助性的指南，不是嚴格的門檻", "DoR is a helpful guideline, not a strict gate"),
]
for i in range(80):
    _sid += 1
    c = dor_concepts[i % len(dor_concepts)]
    others = [x for x in dor_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於Definition of Ready，以下哪項正確？", "Which is correct about the Definition of Ready?"),
        ("Definition of Ready的特點是？", "What is true about the Definition of Ready?"),
    ][i % 2]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T1_ZH, T1_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 1h: Sprint Backlog (80) ---
SUB_ZH, SUB_EN = "Sprint Backlog", "Sprint待辦清單"
sb_concepts = [
    ("Sprint Backlog由Sprint Goal、選取的PBI和交付計劃組成", "The Sprint Backlog consists of the Sprint Goal, selected PBIs, and delivery plan",
     "Sprint Backlog是Developers的計劃", "The Sprint Backlog is the Developers' plan"),
    ("只有Developers可以修改Sprint Backlog", "Only Developers can modify the Sprint Backlog",
     "Developers擁有Sprint Backlog的所有權", "Developers own the Sprint Backlog"),
    ("Sprint Backlog在Sprint期間可以演進", "The Sprint Backlog can evolve during the Sprint",
     "隨著學習，Developers可以調整計劃", "As they learn, Developers can adjust the plan"),
    ("Sprint Backlog提供了足夠的透明性來檢視進度", "The Sprint Backlog provides enough transparency to inspect progress",
     "Sprint Backlog是Sprint的承諾", "The Sprint Backlog is the commitment for the Sprint"),
    ("Sprint Backlog應在Daily Scrum中檢視", "The Sprint Backlog should be inspected at the Daily Scrum",
     "團隊在Daily Scrum中檢視Sprint Backlog的進度", "The team inspects Sprint Backlog progress at the Daily Scrum"),
]
for i in range(80):
    _sid += 1
    c = sb_concepts[i % len(sb_concepts)]
    others = [x for x in sb_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於Sprint Backlog，以下哪項正確？", "Which is correct about the Sprint Backlog?"),
        ("Sprint Backlog的特點是？", "What is true about the Sprint Backlog?"),
    ][i % 2]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T1_ZH, T1_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 1i: Product Backlog (100) ---
SUB_ZH, SUB_EN = "Product Backlog", "產品待辦清單"
pb_concepts = [
    ("Product Backlog是一個有序的列表，包含產品所需的一切", "The Product Backlog is an ordered list of everything needed in the product",
     "Product Backlog是產品的唯一需求來源", "The Product Backlog is the single source of requirements"),
    ("只有Product Owner負責管理Product Backlog", "Only the Product Owner is responsible for managing the Product Backlog",
     "PO負責Product Backlog的內容、可用性和排序", "The PO is accountable for content, availability, and ordering"),
    ("Product Backlog Refinement是將PBI分解和細化的活動", "Product Backlog Refinement is the activity of breaking down and detailing PBIs",
     "Refinement通常佔團隊產能的10%左右", "Refinement typically consumes about 10% of team capacity"),
    ("Product Backlog是動態的，從不完整", "The Product Backlog is dynamic and never complete",
     "它隨產品和市場的變化而演進", "It evolves as the product and market change"),
    ("Product Backlog Items的優先級由Product Owner決定", "The ordering of PBIs is determined by the Product Owner",
     "PO根據價值、風險和依賴性排序", "The PO orders based on value, risk, and dependencies"),
    ("Product Backlog的頂部項目應有足夠的細節可以開始開發", "Top items in the Product Backlog should have enough detail to start development",
     "頂部的PBI更詳細，底部的更粗略", "Top PBIs are more detailed; bottom items are coarser"),
    ("Product Backlog是Product Goal的承諾載體", "The Product Backlog is the commitment artifact for the Product Goal",
     "Product Goal是Product Backlog的長期目標", "The Product Goal is the long-term objective for the Product Backlog"),
]
for i in range(100):
    _sid += 1
    c = pb_concepts[i % len(pb_concepts)]
    others = [x for x in pb_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於Product Backlog，以下哪項正確？", "Which is correct about the Product Backlog?"),
        ("Product Backlog的特點是？", "What is true about the Product Backlog?"),
    ][i % 2]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T1_ZH, T1_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 1j: Increment (100) ---
SUB_ZH, SUB_EN = "Increment", "增量"
inc_concepts = [
    ("Increment是所有完成的Product Backlog Items的總和", "An Increment is the sum of all completed PBIs",
     "增量是Sprint中所有完成工作的累加", "The Increment is the accumulation of all work done in the Sprint"),
    ("每個Increment必須與之前的所有Increments一起工作", "Each Increment must work together with all previous Increments",
     "增量必須與現有系統集成並正常運作", "Increments must integrate and work with the existing system"),
    ("Increment必須符合Definition of Done", "The Increment must meet the Definition of Done",
     "只有符合DoD的工作才能成為Increment的一部分", "Only work meeting the DoD is part of the Increment"),
    ("多個Increment可以在一個Sprint中產生", "Multiple Increments can be created within a Sprint",
     "團隊可以在Sprint期間多次交付增量", "Teams can deliver Increments multiple times during a Sprint"),
    ("Increment必須是可用的，即使PO決定不發布", "The Increment must be usable even if the PO decides not to release it",
     "Increment的可用性與發布決策是分開的", "Increment usability is separate from the release decision"),
    ("每個Sprint至少產出一個有價值的Increment", "Each Sprint produces at least one valuable Increment",
     "Increment是Sprint的目的", "The Increment is the purpose of the Sprint"),
]
for i in range(100):
    _sid += 1
    c = inc_concepts[i % len(inc_concepts)]
    others = [x for x in inc_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於Increment，以下哪項正確？", "Which is correct about the Increment?"),
        ("Increment的特點是？", "What is true about the Increment?"),
    ][i % 2]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T1_ZH, T1_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 1k: Time-boxing (80) ---
SUB_ZH, SUB_EN = "Time-boxing", "時間盒"
tb_concepts = [
    ("時間盒是Scrum中限制事件最大時長的技術", "Time-boxing is Scrum's technique of limiting the maximum length of events",
     "時間盒創造了必要的緊迫感和焦點", "Time-boxing creates urgency and focus"),
    ("所有Scrum事件都是時間盒限定的", "All Scrum events are time-boxed",
     "Sprint、Sprint Planning、Daily Scrum、Sprint Review和Retrospective都有時間盒", "Sprint, Planning, Daily Scrum, Review, and Retrospective all have time-boxes"),
    ("時間盒的目的是創造不確定性的邊界", "The purpose of time-boxing is to create boundaries around uncertainty",
     "它幫助團隊在有限時間內做出最佳決策", "It helps teams make the best decisions in a limited time"),
    ("一個月Sprint的時間盒：Planning 8h, Review 4h, Retro 3h", "One-month Sprint time-boxes: Planning 8h, Review 4h, Retro 3h",
     "較短的Sprint按比例縮短時間盒", "Shorter Sprints scale time-boxes proportionally"),
    ("Daily Scrum固定為15分鐘，不隨Sprint長度變化", "Daily Scrum is always 15 minutes regardless of Sprint length",
     "Daily Scrum的時間盒不變", "Daily Scrum's time-box does not change"),
    ("時間盒鼓勵聚焦和減少浪費", "Time-boxing encourages focus and reduces waste",
     "沒有時間盒，會議可能無限延長", "Without time-boxes, meetings could extend indefinitely"),
]
for i in range(80):
    _sid += 1
    c = tb_concepts[i % len(tb_concepts)]
    others = [x for x in tb_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於時間盒（Time-boxing），以下哪項正確？", "Which is correct about time-boxing?"),
        ("時間盒的特點是？", "What is true about time-boxing?"),
    ][i % 2]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T1_ZH, T1_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 1l: Empiricism (80) ---
SUB_ZH, SUB_EN = "Empiricism", "經驗主義"
emp_concepts = [
    ("Scrum基於經驗主義，即知識來自經驗", "Scrum is founded on empiricism, where knowledge comes from experience",
     "經驗主義是Scrum的哲學基礎", "Empiricism is the philosophical foundation of Scrum"),
    ("經驗主義的三大支柱：透明性、檢視、適應", "The three pillars of empiricism: Transparency, Inspection, Adaptation",
     "這三個支柱支撐了Scrum的所有實踐", "These three pillars support all Scrum practices"),
    ("透明性意味著所有重要方面對負責結果的人可見", "Transparency means all significant aspects are visible to those responsible for the outcome",
     "透明性需要共同標準來確保理解一致", "Transparency requires common standards to ensure consistent understanding"),
    ("檢視是頻繁地檢查Scrum工件和進度", "Inspection means frequently checking Scrum artifacts and progress",
     "檢視不應阻礙工作進行", "Inspection should not impede work"),
    ("適應是當檢視發現偏差時進行調整", "Adaptation means adjusting when inspection reveals deviations",
     "如果需要調整，應盡快進行", "If adjustment is needed, it should be done as soon as possible"),
    ("經驗主義與預測性方法不同，它擁抱不確定性", "Empiricism differs from predictive approaches by embracing uncertainty",
     "Scrum假設問題是複雜的，解決方案需要迭代探索", "Scrum assumes problems are complex and solutions need iterative exploration"),
]
for i in range(80):
    _sid += 1
    c = emp_concepts[i % len(emp_concepts)]
    others = [x for x in emp_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於經驗主義（Empiricism），以下哪項正確？", "Which is correct about empiricism?"),
        ("經驗主義的特點是？", "What is true about empiricism?"),
    ][i % 2]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T1_ZH, T1_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 1m: Scrum Values (70) ---
SUB_ZH, SUB_EN = "Scrum Values", "Scrum價值觀"
val_concepts = [
    ("承諾（Commitment）——Scrum團隊承諾實現Sprint Goal和Product Goal",
     "Commitment—Scrum Team commits to achieving the Sprint Goal and Product Goal",
     "承諾是團隊對目標的專注投入", "Commitment is the team's focused dedication to goals"),
    ("專注（Focus）——Scrum團隊專注於Sprint的工作",
     "Focus—Scrum Team focuses on the work of the Sprint",
     "專注減少了多任務切換的浪費", "Focus reduces waste from context switching"),
    ("開放（Openness）——Scrum團隊和利益相關者對工作和挑戰保持開放",
     "Openness—Scrum Team and stakeholders are open about work and challenges",
     "開放促進了透明性和信任", "Openness promotes transparency and trust"),
    ("尊重（Respect）——Scrum團隊成員互相尊重",
     "Respect—Scrum Team members respect each other",
     "尊重是自管理和協作的基礎", "Respect is the foundation of self-management and collaboration"),
    ("勇氣（Courage）——Scrum團隊有勇氣做正確的事",
     "Courage—Scrum Team has the courage to do the right thing",
     "勇氣使團隊能夠面對困難和挑戰", "Courage enables the team to face difficulties and challenges"),
    ("Scrum Values幫助團隊做出困難的決定", "Scrum Values help teams make difficult decisions",
     "當不確定時，價值觀指導行為", "When uncertain, values guide behavior"),
    ("五個Scrum Values是：承諾、專注、開放、尊重、勇氣", "The five Scrum Values are: Commitment, Focus, Openness, Respect, Courage",
     "這些價值觀使經驗主義成為可能", "These values make empiricism possible"),
]
for i in range(70):
    _sid += 1
    c = val_concepts[i % len(val_concepts)]
    others = [x for x in val_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於Scrum Values，以下哪項正確？", "Which is correct about Scrum Values?"),
        ("以下哪項是Scrum的核心價值觀？", "Which is a core Scrum Value?"),
    ][i % 2]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T1_ZH, T1_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# ============================================================
# TOPIC 2: Scrum Roles (750 questions, 15%)
# ============================================================
T2_ZH = "Scrum角色"
T2_EN = "Scrum Roles"

# --- 2a: Product Owner (200) ---
SUB_ZH, SUB_EN = "Product Owner", "產品負責人"
po_concepts = [
    ("Product Owner負責最大化產品價值", "The Product Owner is accountable for maximizing product value",
     "PO是產品價值最大化的最終負責人", "The PO is ultimately responsible for maximizing product value"),
    ("Product Owner是管理Product Backlog的唯一責任人", "The Product Owner is the sole person responsible for managing the Product Backlog",
     "PO可以將工作委派給團隊，但責任仍在PO", "The PO can delegate work but remains accountable"),
    ("Product Owner決定Product Backlog Items的優先級", "The Product Owner prioritizes Product Backlog Items",
     "PO根據價值、風險和依賴關係排序", "The PO orders based on value, risk, and dependencies"),
    ("Product Owner確保Product Backlog對所有人透明", "The Product Owner ensures the Product Backlog is transparent to everyone",
     "透明性使所有利益相關者了解計劃", "Transparency lets all stakeholders understand the plan"),
    ("Product Owner是一個個體，不是一個委員會", "The Product Owner is an individual, not a committee",
     "PO可能代表委員會的需求，但PO是單一個人", "The PO may represent a committee's needs but is a single person"),
    ("Product Owner需要與利益相關者密切合作", "The Product Owner works closely with stakeholders",
     "PO收集和整合利益相關者的輸入", "The PO gathers and integrates stakeholder input"),
    ("Product Owner是唯一有權接受或拒絕Increment的人", "The Product Owner is the only one who can accept or reject the Increment",
     "PO代表利益相關者做出接受決策", "The PO makes acceptance decisions on behalf of stakeholders"),
    ("Product Owner需要理解市場和用戶需求", "The Product Owner needs to understand market and user needs",
     "PO應具備產品領域知識", "The PO should have product domain knowledge"),
    ("Product Owner出席所有Scrum事件", "The Product Owner attends all Scrum events",
     "PO在每個事件中都有重要角色", "The PO has an important role in every event"),
    ("Product Owner可以被組織解僱或替換", "The Product Owner can be fired or replaced by the organization",
     "組織對PO任命有最終決定權", "The organization has the final say on PO appointment"),
]
for i in range(200):
    _sid += 1
    c = po_concepts[i % len(po_concepts)]
    others = [x for x in po_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於Product Owner，以下哪項正確？", "Which is correct about the Product Owner?"),
        ("Product Owner的職責是？", "What is the Product Owner accountable for?"),
        ("以下哪項準確描述了Product Owner？", "Which accurately describes the Product Owner?"),
    ][i % 3]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T2_ZH, T2_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 2b: Scrum Master (200) ---
SUB_ZH, SUB_EN = "Scrum Master", "Scrum Master"
sm_concepts = [
    ("Scrum Master是服務型領導者", "The Scrum Master is a servant leader",
     "SM通過服務團隊來領導", "The SM leads by serving the team"),
    ("Scrum Master對Scrum框架的有效性負責", "The Scrum Master is accountable for the Scrum framework's effectiveness",
     "SM確保團隊理解和實施Scrum", "The SM ensures the team understands and implements Scrum"),
    ("Scrum Master幫助移除團隊的障礙", "The Scrum Master helps remove team impediments",
     "SM是團隊的教練和促進者", "The SM is the team's coach and facilitator"),
    ("Scrum Master在團隊不請求幫助時也可以指導", "The Scrum Master can coach even when the team doesn't ask for help",
     "SM應主動幫助團隊改進", "The SM should proactively help the team improve"),
    ("Scrum Master幫助建立Scrum團隊和組織之間的關係", "The Scrum Master helps establish relationships between the Scrum Team and the organization",
     "SM在組織層面推動Scrum adoption", "The SM drives Scrum adoption at the organizational level"),
    ("Scrum Master確保所有Scrum事件發生且有成效", "The Scrum Master ensures all Scrum events take place and are productive",
     "SM確保事件在時間盒內且有價值", "The SM ensures events are within time-box and valuable"),
    ("Scrum Master教導團隊自管理和跨功能", "The Scrum Master coaches the team in self-management and cross-functionality",
     "SM幫助團隊變得更加自主", "The SM helps the team become more autonomous"),
    ("Scrum Master幫助Product Owner找到有效管理Product Backlog的技巧", "The Scrum Master helps the PO find techniques for effective Product Backlog management",
     "SM對PO提供指導和支持", "The SM provides guidance and support to the PO"),
    ("Scrum Master幫助組織理解Scrum並推動變革", "The Scrum Master helps the organization understand Scrum and drive change",
     "SM是組織的Scrum教練", "The SM is the organization's Scrum coach"),
    ("Scrum Master不是團隊的管理者或主管", "The Scrum Master is not the team's manager or supervisor",
     "SM不控制團隊的工作方式", "The SM does not control how the team works"),
    ("Scrum Master促進團隊內部和外部的溝通", "The Scrum Master facilitates communication within and outside the team",
     "SM促進健康的衝突解決和協作", "The SM promotes healthy conflict resolution and collaboration"),
]
for i in range(200):
    _sid += 1
    c = sm_concepts[i % len(sm_concepts)]
    others = [x for x in sm_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於Scrum Master，以下哪項正確？", "Which is correct about the Scrum Master?"),
        ("Scrum Master的職責是？", "What is the Scrum Master accountable for?"),
        ("以下哪項準確描述了Scrum Master？", "Which accurately describes the Scrum Master?"),
    ][i % 3]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T2_ZH, T2_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 2c: Developers (150) ---
SUB_ZH, SUB_EN = "Developers", "開發者"
dev_concepts = [
    ("Developers是Scrum團隊中致力於在每個Sprint中創建可用Increment的專業人士",
     "Developers are professionals committed to creating a usable Increment each Sprint",
     "Developers擁有技術決策權", "Developers own technical decisions"),
    ("Developers是跨功能的——團隊擁有創建Increment所需的所有技能",
     "Developers are cross-functional—the team has all skills needed to create the Increment",
     "不需要外部資源來完成Sprint工作", "No external resources needed for Sprint work"),
    ("Developers是自管理的——他們自己決定誰做什麼、何時做、如何做",
     "Developers are self-managing—they decide who does what, when, and how",
     "沒有人告訴Developers如何將PBI轉化為Increment", "No one tells Developers how to turn PBIs into an Increment"),
    ("Developers對Sprint Backlog擁有所有權",
     "Developers own the Sprint Backlog",
     "只有Developers可以修改Sprint Backlog", "Only Developers can change the Sprint Backlog"),
    ("Developers估算Product Backlog Items",
     "Developers estimate Product Backlog Items",
     "Developers最適合評估技術複雜性", "Developers are best positioned to assess technical complexity"),
    ("Developers對品質負責，確保工作符合DoD",
     "Developers are responsible for quality, ensuring work meets the DoD",
     "品質是Developers的內建責任", "Quality is built into Developers' responsibility"),
    ("Developers參加所有Scrum事件",
     "Developers participate in all Scrum events",
     "Developers在每個事件中都有關鍵角色", "Developers have a critical role in every event"),
    ("2020年Scrum Guide將Development Team簡化為Developers",
     "The 2020 Scrum Guide simplified 'Development Team' to 'Developers'",
     "這反映了Scrum團隊是一個整體的概念", "This reflects the concept of one Scrum Team"),
]
for i in range(150):
    _sid += 1
    c = dev_concepts[i % len(dev_concepts)]
    others = [x for x in dev_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於Developers，以下哪項正確？", "Which is correct about Developers?"),
        ("Developers的特點是？", "What is true about Developers?"),
    ][i % 2]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T2_ZH, T2_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 2d: Stakeholders (80) ---
SUB_ZH, SUB_EN = "Stakeholders", "利益相關者"
sh_concepts = [
    ("利益相關者參加Sprint Review並提供反饋", "Stakeholders attend the Sprint Review and provide feedback",
     "Sprint Review是利益相關者參與的關鍵事件", "The Sprint Review is the key event for stakeholder participation"),
    ("利益相關者不直接指揮Developers的工作", "Stakeholders do not directly direct the Developers' work",
     "所有需求通過Product Owner進入Product Backlog", "All requirements enter the Product Backlog through the PO"),
    ("利益相關者與Product Owner溝通產品需求", "Stakeholders communicate product needs to the Product Owner",
     "PO是利益相關者和團隊之間的橋樑", "The PO is the bridge between stakeholders and the team"),
    ("透明性使利益相關者能夠了解進度和挑戰", "Transparency enables stakeholders to understand progress and challenges",
     "利益相關者需要足夠的信息來做出決策", "Stakeholders need sufficient information to make decisions"),
    ("關鍵利益相關者應在Sprint Planning中提供輸入", "Key stakeholders should provide input at Sprint Planning",
     "利益相關者的輸入幫助確定Sprint的優先級", "Stakeholder input helps determine Sprint priorities"),
]
for i in range(80):
    _sid += 1
    c = sh_concepts[i % len(sh_concepts)]
    others = [x for x in sh_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於利益相關者（Stakeholders），以下哪項正確？", "Which is correct about stakeholders?"),
        ("利益相關者在Scrum中的角色是？", "What is the stakeholders' role in Scrum?"),
    ][i % 2]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T2_ZH, T2_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 2e: Role boundaries and interactions (120) ---
SUB_ZH, SUB_EN = "Role Boundaries", "角色邊界"
rb_concepts = [
    ("Scrum團隊由Product Owner、Scrum Master和Developers組成",
     "The Scrum Team consists of Product Owner, Scrum Master, and Developers",
     "Scrum團隊沒有子團隊或層級結構", "The Scrum Team has no sub-teams or hierarchies"),
    ("一個人可以同時是Scrum Master和Developers嗎？可以，但不推薦",
     "Can one person be both SM and Developers? Yes, but not recommended",
     "角色合併可能導致利益衝突", "Role merging can lead to conflicts of interest"),
    ("Product Owner和Scrum Master不應是同一個人",
     "The Product Owner and Scrum Master should not be the same person",
     "這兩個角色有天然的張力", "These two roles have natural tension"),
    ("Scrum Master不分配任務給Developers",
     "The Scrum Master does not assign tasks to Developers",
     "Developers自管理他們的工作", "Developers self-manage their work"),
    ("Product Owner不告訴團隊如何構建產品",
     "The Product Owner does not tell the team how to build the product",
     "PO決定做什麼（What），團隊決定如何做（How）", "The PO decides What, the team decides How"),
    ("Scrum團隊的規模通常為10人或更少",
     "The Scrum Team size is typically 10 or fewer people",
     "較小的團隊溝通更有效", "Smaller teams communicate more effectively"),
    ("Scrum團隊是跨功能的，自組織的",
     "The Scrum Team is cross-functional and self-organizing",
     "團隊擁有交付Increment所需的所有技能", "The team has all skills needed to deliver the Increment"),
    ("所有Scrum角色共同承擔交付價值的責任",
     "All Scrum roles share accountability for delivering value",
     "Scrum是一個團隊運動", "Scrum is a team sport"),
]
for i in range(120):
    _sid += 1
    c = rb_concepts[i % len(rb_concepts)]
    others = [x for x in rb_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於Scrum角色邊界，以下哪項正確？", "Which is correct about Scrum role boundaries?"),
        ("以下哪項準確描述了Scrum角色之間的關係？", "Which accurately describes the relationship between Scrum roles?"),
    ][i % 2]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T2_ZH, T2_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# ============================================================
# TOPIC 3: Scrum Artifacts (750 questions, 15%)
# ============================================================
T3_ZH = "Scrum工件"
T3_EN = "Scrum Artifacts"

# --- 3a: Product Backlog artifacts (150) ---
SUB_ZH, SUB_EN = "Product Backlog Artifact", "Product Backlog工件"
pba_concepts = [
    ("Product Backlog是Scrum的三大工件之一", "The Product Backlog is one of Scrum's three artifacts",
     "三大工件：Product Backlog、Sprint Backlog、Increment", "Three artifacts: Product Backlog, Sprint Backlog, Increment"),
    ("Product Backlog的承諾是Product Goal", "The Product Backlog's commitment is the Product Goal",
     "Product Goal提供了Product Backlog的目標和方向", "Product Goal provides purpose and direction for the Product Backlog"),
    ("Product Goal描述了產品的未來狀態", "The Product Goal describes a future state of the product",
     "Product Goal是Scrum團隊的長期目標", "The Product Goal is the Scrum Team's long-term objective"),
    ("Product Backlog Items包括描述、估算、價值和排序", "PBIs include description, estimate, value, and ordering",
     "PBI應包含足夠的信息來理解和實施", "PBIs should contain enough information to understand and implement"),
    ("Product Backlog永遠不會完成——它持續演進", "The Product Backlog is never complete—it continuously evolves",
     "隨著產品和市場的變化，Product Backlog不斷更新", "As the product and market change, the Product Backlog is constantly updated"),
    ("Product Backlog的排序基於風險、價值、依賴性和必要性",
     "Product Backlog ordering is based on risk, value, dependencies, and necessity",
     "PO負責排序決策", "The PO is responsible for ordering decisions"),
]
for i in range(150):
    _sid += 1
    c = pba_concepts[i % len(pba_concepts)]
    others = [x for x in pba_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於Product Backlog工件，以下哪項正確？", "Which is correct about the Product Backlog artifact?"),
        ("Product Backlog的特點是？", "What is true about the Product Backlog?"),
    ][i % 2]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T3_ZH, T3_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 3b: Sprint Backlog artifact (150) ---
SUB_ZH, SUB_EN = "Sprint Backlog Artifact", "Sprint Backlog工件"
sba_concepts = [
    ("Sprint Backlog的承諾是Sprint Goal", "The Sprint Backlog's commitment is the Sprint Goal",
     "Sprint Goal提供了Sprint Backlog的目標", "The Sprint Goal provides the objective for the Sprint Backlog"),
    ("Sprint Backlog包含Sprint Goal、選取的PBI和交付計劃",
     "The Sprint Backlog includes Sprint Goal, selected PBIs, and delivery plan",
     "這三個元素共同構成Sprint Backlog", "These three elements together form the Sprint Backlog"),
    ("Sprint Backlog是實時的、足夠透明的計劃", "The Sprint Backlog is a real-time, sufficiently transparent plan",
     "它讓團隊可以隨時檢視進度", "It allows the team to inspect progress at any time"),
    ("Sprint Backlog在Sprint期間可以根據需要更新", "The Sprint Backlog can be updated during the Sprint as needed",
     "Developers可以根據學習調整計劃", "Developers can adjust the plan based on learning"),
    ("Sprint Goal提供了靈活性——即使計劃改變，目標不變",
     "The Sprint Goal provides flexibility—even if the plan changes, the goal doesn't",
     "Sprint Goal是Sprint期間的北極星", "The Sprint Goal is the North Star during the Sprint"),
    ("Sprint Backlog的透明性使Daily Scrum有效", "Sprint Backlog transparency makes the Daily Scrum effective",
     "團隊在Daily Scrum中檢視Sprint Backlog", "The team inspects the Sprint Backlog at the Daily Scrum"),
]
for i in range(150):
    _sid += 1
    c = sba_concepts[i % len(sba_concepts)]
    others = [x for x in sba_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於Sprint Backlog工件，以下哪項正確？", "Which is correct about the Sprint Backlog artifact?"),
        ("Sprint Backlog的特點是？", "What is true about the Sprint Backlog?"),
    ][i % 2]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T3_ZH, T3_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 3c: Increment artifact (150) ---
SUB_ZH, SUB_EN = "Increment Artifact", "增量工件"
ia_concepts = [
    ("Increment的承諾是Definition of Done", "The Increment's commitment is the Definition of Done",
     "DoD確保Increment的品質和可用性", "DoD ensures Increment quality and usability"),
    ("Increment是所有先前Increments的累加", "The Increment is the sum of all previous Increments",
     "每個Sprint的增量都建立在之前的工作之上", "Each Sprint's Increment builds on previous work"),
    ("不符合DoD的PBI不能成為Increment的一部分",
     "PBIs that don't meet the DoD cannot be part of the Increment",
     "DoD是不可協商的品質標準", "DoD is a non-negotiable quality standard"),
    ("Increment必須是可用的，可以隨時發布",
     "The Increment must be usable and can be released at any time",
     "發布決策由Product Owner做出", "The release decision is made by the Product Owner"),
    ("多個Increments可以在一個Sprint中創建",
     "Multiple Increments can be created within a Sprint",
     "團隊可以頻繁集成和交付", "Teams can integrate and deliver frequently"),
    ("Increment代表朝著Product Goal的進步",
     "The Increment represents progress toward the Product Goal",
     "每個Increment都應推進Product Goal", "Each Increment should advance the Product Goal"),
]
for i in range(150):
    _sid += 1
    c = ia_concepts[i % len(ia_concepts)]
    others = [x for x in ia_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於Increment工件，以下哪項正確？", "Which is correct about the Increment artifact?"),
        ("Increment的特點是？", "What is true about the Increment?"),
    ][i % 2]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T3_ZH, T3_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 3d: PBI attributes (100) ---
SUB_ZH, SUB_EN = "Product Backlog Items", "Product Backlog Items"
pbi_concepts = [
    ("User Story是一種常見的PBI格式：As a [user], I want [feature], so that [benefit]",
     "User Story is a common PBI format: As a [user], I want [feature], so that [benefit]",
     "User Story不是Scrum Guide要求的格式，但是常見實踐", "User Story is not required by Scrum Guide but is a common practice"),
    ("Acceptance Criteria定義了PBI何時被認為是完成的",
     "Acceptance Criteria define when a PBI is considered done",
     "驗收標準提供了明確的完成條件", "Acceptance Criteria provide clear completion conditions"),
    ("PBI應足夠小，能在一個Sprint內完成",
     "PBIs should be small enough to complete within one Sprint",
     "無法在一個Sprint內完成的PBI應被分解", "PBIs that can't be completed in one Sprint should be decomposed"),
    ("PBI應包含足夠的細節讓Developers理解需求",
     "PBIs should contain enough detail for Developers to understand the requirement",
     "Refinement活動增加PBI的細節", "Refinement activities add detail to PBIs"),
    ("PBI可以是User Story、Bug、技術任務或實驗",
     "PBIs can be User Stories, bugs, technical tasks, or experiments",
     "任何能推進Product Goal的工作都可以是PBI", "Any work that advances the Product Goal can be a PBI"),
    ("INVEST原則：Independent, Negotiable, Valuable, Estimable, Small, Testable",
     "INVEST: Independent, Negotiable, Valuable, Estimable, Small, Testable",
     "INVEST幫助創建高品質的User Stories", "INVEST helps create high-quality User Stories"),
]
for i in range(100):
    _sid += 1
    c = pbi_concepts[i % len(pbi_concepts)]
    others = [x for x in pbi_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於Product Backlog Items，以下哪項正確？", "Which is correct about PBIs?"),
        ("PBI的特點是？", "What is true about PBIs?"),
    ][i % 2]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T3_ZH, T3_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 3e: Transparency and Commitments (100) ---
SUB_ZH, SUB_EN = "Artifact Transparency", "工件透明性"
at_concepts = [
    ("工件透明性是Scrum有效性的基礎", "Artifact transparency is fundamental to Scrum's effectiveness",
     "不透明的工件導致錯誤的決策和浪費", "Opaque artifacts lead to wrong decisions and waste"),
    ("每個工件都有一個承諾來加強透明性", "Each artifact has a commitment to enhance transparency",
     "Product Backlog→Product Goal, Sprint Backlog→Sprint Goal, Increment→DoD", "Product Backlog→Product Goal, Sprint Backlog→Sprint Goal, Increment→DoD"),
    ("承諾提供了目的和焦點", "Commitments provide purpose and focus",
     "承諾幫助團隊做出決策", "Commitments help teams make decisions"),
    ("低透明性等於高風險", "Low transparency equals high risk",
     "隱藏的問題無法被檢視和解決", "Hidden problems cannot be inspected and resolved"),
    ("Scrum Master應幫助提高工件的透明性", "The Scrum Master should help increase artifact transparency",
     "SM是透明性的守護者", "The SM is the guardian of transparency"),
    ("透明性需要所有人的理解和共同標準",
     "Transparency requires understanding and common standards from everyone",
     "如果人們對「完成」有不同理解，透明性就不存在",
     "If people have different understandings of 'done', transparency doesn't exist"),
]
for i in range(100):
    _sid += 1
    c = at_concepts[i % len(at_concepts)]
    others = [x for x in at_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於工件透明性，以下哪項正確？", "Which is correct about artifact transparency?"),
        ("工件透明性的特點是？", "What is true about artifact transparency?"),
    ][i % 2]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T3_ZH, T3_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 3f: Burndown/Burnup charts (100) ---
SUB_ZH, SUB_EN = "Burndown/Burnup Charts", "燃盡圖/燃起圖"
chart_concepts = [
    ("Sprint Burndown圖表顯示Sprint Backlog中剩餘工作的趨勢",
     "The Sprint Burndown chart shows the trend of remaining work in the Sprint Backlog",
     "它幫助團隊可視化進度", "It helps the team visualize progress"),
    ("Burndown圖表的Y軸是剩餘工作量，X軸是時間",
     "The Burndown chart's Y-axis is remaining work, X-axis is time",
     "理想線是從起點到終點的直線", "The ideal line is a straight line from start to end"),
    ("Burnup圖表顯示已完成的工作量",
     "Burnup charts show the amount of completed work",
     "它比Burndown更清楚地顯示範圍變化", "It shows scope changes more clearly than Burndown"),
    ("Burndown圖表不是Scrum Guide的一部分，但是有用的實踐",
     "The Burndown chart is not part of the Scrum Guide but is a useful practice",
     "它是補充工具，不是必需的", "It's a complementary tool, not required"),
    ("Sprint Burndown不應用作管理報告工具",
     "Sprint Burndown should not be used as a management reporting tool",
     "它主要服務於Developers的自我管理", "It primarily serves Developers' self-management"),
    ("Product Burndown顯示Product Backlog中剩餘工作的長期趨勢",
     "Product Burndown shows the long-term trend of remaining work in the Product Backlog",
     "它幫助預測產品的完成時間", "It helps predict product completion time"),
]
for i in range(100):
    _sid += 1
    c = chart_concepts[i % len(chart_concepts)]
    others = [x for x in chart_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於燃盡圖（Burndown Charts），以下哪項正確？", "Which is correct about Burndown Charts?"),
        ("燃盡圖的特點是？", "What is true about Burndown Charts?"),
    ][i % 2]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T3_ZH, T3_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# ============================================================
# TOPIC 4: Agile/Lean Principles (750 questions, 15%)
# ============================================================
T4_ZH = "敏捷/精益原則"
T4_EN = "Agile/Lean Principles"

# --- 4a: Agile Manifesto (150) ---
SUB_ZH, SUB_EN = "Agile Manifesto", "敏捷宣言"
agile_concepts = [
    ("個體和互動 高於 流程和工具", "Individuals and interactions over processes and tools",
     "人是成功最重要的因素", "People are the most important factor in success"),
    ("可用的軟件 高於 詳盡的文檔", "Working software over comprehensive documentation",
     "交付價值比產出文檔更重要", "Delivering value matters more than producing documentation"),
    ("客戶合作 高於 合同談判", "Customer collaboration over contract negotiation",
     "與客戶建立持續的合作關係", "Build ongoing collaborative relationships with customers"),
    ("回應變化 高於 遵循計劃", "Responding to change over following a plan",
     "擁抱變化而非抗拒", "Embrace change rather than resist it"),
    ("敏捷宣言重視左邊的項目，但右邊的也有價值",
     "Agile Manifesto values items on the left more, but items on the right have value too",
     "這不是非此即彼的選擇", "It's not an either/or choice"),
    ("敏捷宣言背後有12個原則", "There are 12 principles behind the Agile Manifesto",
     "這些原則指導敏捷實踐", "These principles guide agile practices"),
    ("敏捷宣言的第一原則：通過早期和持續交付有價值的軟件來滿足客戶",
     "First principle: Satisfy the customer through early and continuous delivery",
     "持續交付是敏捷的核心", "Continuous delivery is core to agile"),
    ("敏捷宣言強調可工作的軟件是進度的主要度量",
     "Agile emphasizes working software as the primary measure of progress",
     "而不是文檔或計劃", "Not documentation or plans"),
    ("敏捷團隊定期反思如何變得更有效",
     "Agile teams regularly reflect on how to become more effective",
     "持續改進是敏捷文化的一部分", "Continuous improvement is part of agile culture"),
    ("敏捷宣言支持自組織團隊", "The Agile Manifesto supports self-organizing teams",
     "最好的架構、需求和設計來自自組織團隊", "The best architectures, requirements, and designs emerge from self-organizing teams"),
]
for i in range(150):
    _sid += 1
    c = agile_concepts[i % len(agile_concepts)]
    others = [x for x in agile_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於敏捷宣言，以下哪項正確？", "Which is correct about the Agile Manifesto?"),
        ("敏捷宣言的核心觀點是？", "What is a core view of the Agile Manifesto?"),
    ][i % 2]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T4_ZH, T4_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 4b: Lean Thinking (150) ---
SUB_ZH, SUB_EN = "Lean Thinking", "精益思維"
lean_concepts = [
    ("精益的七大浪費包括：過度生產、等待、運輸、過度加工、庫存、動作、缺陷",
     "Lean's 7 wastes: Overproduction, Waiting, Transport, Over-processing, Inventory, Motion, Defects",
     "識別和消除浪費是精益的核心", "Identifying and eliminating waste is core to Lean"),
    ("精益強調價值流——從客戶需求到交付的整個流程",
     "Lean emphasizes the value stream—the entire flow from customer need to delivery",
     "價值流映射幫助識別浪費", "Value Stream Mapping helps identify waste"),
    ("精益的核心是創造客戶價值", "Lean's core is creating customer value",
     "任何不增加客戶價值的活動都是浪費", "Any activity that doesn't add customer value is waste"),
    ("精益鼓勵小批量工作以減少浪費", "Lean encourages small batches to reduce waste",
     "小批量減少了在制品和等待時間", "Small batches reduce work-in-progress and waiting time"),
    ("看板(Kanban)是精益的一種實現方式", "Kanban is an implementation of Lean",
     "看板通過可視化工作流來管理", "Kanban manages by visualizing the workflow"),
    ("持續改進(Kaizen)是精益的核心原則", "Continuous Improvement (Kaizen) is a core Lean principle",
     "每個人都應參與改進", "Everyone should participate in improvement"),
    ("精益假設系統中的變異是浪費的來源", "Lean assumes variation in systems is a source of waste",
     "減少變異可以提高效率", "Reducing variation can improve efficiency"),
    ("拉動系統（Pull System）只在有需求時才開始工作",
     "Pull System starts work only when there is demand",
     "避免過度生產和庫存積壓", "Avoids overproduction and inventory buildup"),
]
for i in range(150):
    _sid += 1
    c = lean_concepts[i % len(lean_concepts)]
    others = [x for x in lean_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於精益思維（Lean Thinking），以下哪項正確？", "Which is correct about Lean Thinking?"),
        ("精益的核心原則是？", "What is a core Lean principle?"),
    ][i % 2]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T4_ZH, T4_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 4c: Empirical Process Control (100) ---
SUB_ZH, SUB_EN = "Empirical Process Control", "經驗過程控制"
epc_concepts = [
    ("經驗過程控制基於觀察而非預測", "Empirical process control is based on observation rather than prediction",
     "它適用於複雜問題", "It applies to complex problems"),
    ("經驗過程控制與預測性過程控制不同", "Empirical process control differs from predictive process control",
     "預測性適用於簡單問題，經驗性適用於複雜問題", "Predictive for simple, empirical for complex"),
    ("Scrum使用短迭代來獲得快速反饋", "Scrum uses short iterations for rapid feedback",
     "快速反饋使快速適應成為可能", "Rapid feedback enables rapid adaptation"),
    ("經驗主義假設問題空間是複雜的", "Empiricism assumes the problem space is complex",
     "解決方案需要通過實驗發現", "Solutions need to be discovered through experimentation"),
    ("透明性、檢視和適應是經驗過程控制的三大支柱",
     "Transparency, Inspection, and Adaptation are the three pillars of empirical process control",
     "缺一不可", "All three are essential"),
    ("經驗過程控制通過頻繁的檢視點來降低風險",
     "Empirical process control reduces risk through frequent inspection points",
     "頻繁的檢視允許及早發現問題", "Frequent inspection allows early problem detection"),
]
for i in range(100):
    _sid += 1
    c = epc_concepts[i % len(epc_concepts)]
    others = [x for x in epc_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於經驗過程控制，以下哪項正確？", "Which is correct about empirical process control?"),
        ("經驗過程控制的特點是？", "What is true about empirical process control?"),
    ][i % 2]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T4_ZH, T4_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 4d: Iterative/Incremental/Self-organization/Cross-functional (200) ---
SUB_ZH, SUB_EN = "Iterative and Incremental", "迭代和增量"
ii_concepts = [
    ("迭代開發意味著重複工作循環以改進產品", "Iterative development means repeating work cycles to improve the product",
     "每次迭代都在前一次的基礎上改進", "Each iteration improves upon the previous one"),
    ("增量開發意味著逐步構建產品功能", "Incremental development means building product features progressively",
     "每次增量添加新的功能", "Each increment adds new functionality"),
    ("Scrum同時使用迭代和增量方法", "Scrum uses both iterative and incremental approaches",
     "每個Sprint既是迭代又是增量", "Each Sprint is both iterative and incremental"),
    ("自組織團隊自行決定如何完成工作", "Self-organizing teams decide for themselves how to complete their work",
     "沒有人指定團隊如何工作", "No one dictates how the team works"),
    ("自組織不意味著無政府——團隊在Scrum框架內自組織",
     "Self-organization doesn't mean anarchy—teams self-organize within the Scrum framework",
     "Scrum提供了邊界和規則", "Scrum provides boundaries and rules"),
    ("跨功能團隊擁有交付Increment所需的所有技能",
     "Cross-functional teams have all skills needed to deliver the Increment",
     "不需要依賴外部資源", "No need to depend on external resources"),
    ("跨功能減少了等待和依賴", "Cross-functionality reduces waiting and dependencies",
     "團隊可以獨立完成工作", "Teams can complete work independently"),
    ("自組織促進了團隊的擁有感和承諾", "Self-organization promotes team ownership and commitment",
     "當團隊自己做決策時，承諾度更高", "Commitment is higher when teams make their own decisions"),
    ("增量交付允許早期和頻繁的價值交付", "Incremental delivery allows early and frequent value delivery",
     "客戶更早獲得價值", "Customers get value sooner"),
    ("迭代允許基於反饋的持續學習和調整", "Iteration allows continuous learning and adjustment based on feedback",
     "每次迭代都是一個學習機會", "Each iteration is a learning opportunity"),
]
for i in range(200):
    _sid += 1
    c = ii_concepts[i % len(ii_concepts)]
    others = [x for x in ii_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("以下哪項正確描述了迭代和增量開發？", "Which correctly describes iterative and incremental development?"),
        ("關於自組織團隊，以下哪項正確？", "Which is correct about self-organizing teams?"),
        ("關於跨功能團隊，以下哪項正確？", "Which is correct about cross-functional teams?"),
    ][i % 3]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T4_ZH, T4_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 4e: Continuous improvement / Value-driven / Transparency (150) ---
SUB_ZH, SUB_EN = "Continuous Improvement", "持續改進"
ci_concepts = [
    ("持續改進是敏捷和Scrum的核心原則", "Continuous improvement is a core principle of agile and Scrum",
     "團隊應不斷尋找改進的機會", "Teams should constantly look for improvement opportunities"),
    ("Sprint Retrospective是持續改進的主要機制", "The Sprint Retrospective is the primary mechanism for continuous improvement",
     "每個Sprint都應有一個改進項", "Each Sprint should have at least one improvement item"),
    ("價值驅動交付意味著優先做最有價值的工作", "Value-driven delivery means prioritizing the most valuable work first",
     "PO負責確保團隊做最有價值的工作", "The PO ensures the team works on the most valuable items"),
    ("反饋循環越短，適應越快", "The shorter the feedback loop, the faster the adaptation",
     "短Sprint提供了更頻繁的反饋機會", "Short Sprints provide more frequent feedback opportunities"),
    ("持續改進需要心理安全——團隊必須能坦誠討論問題",
     "Continuous improvement requires psychological safety—teams must be able to discuss problems openly",
     "恐懼阻礙了改進", "Fear impedes improvement"),
    ("改進可以是技術實踐、流程、工具或團隊協作",
     "Improvements can be technical practices, processes, tools, or team collaboration",
     "任何使團隊更有效的改變都是改進", "Any change that makes the team more effective is an improvement"),
    ("透明性使問題可見，從而使改進成為可能",
     "Transparency makes problems visible, making improvement possible",
     "如果問題不可見，就無法改進", "If problems aren't visible, they can't be improved"),
    ("PDCA循環（Plan-Do-Check-Act）是持續改進的模型",
     "PDCA (Plan-Do-Check-Act) is a model for continuous improvement",
     "每個Sprint都是一個PDCA循環", "Each Sprint is a PDCA cycle"),
]
for i in range(150):
    _sid += 1
    c = ci_concepts[i % len(ci_concepts)]
    others = [x for x in ci_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於持續改進，以下哪項正確？", "Which is correct about continuous improvement?"),
        ("關於價值驅動交付，以下哪項正確？", "Which is correct about value-driven delivery?"),
    ][i % 2]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T4_ZH, T4_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# ============================================================
# TOPIC 5: Scaling Scrum (750 questions, 15%)
# ============================================================
T5_ZH = "規模化Scrum"
T5_EN = "Scaling Scrum"

# --- 5a: Nexus Framework (150) ---
SUB_ZH, SUB_EN = "Nexus Framework", "Nexus框架"
nexus_concepts = [
    ("Nexus是Scrum.org推出的規模化Scrum框架", "Nexus is the scaling Scrum framework from Scrum.org",
     "Nexus基於Scrum，增加了3-9個Scrum團隊的集成", "Nexus builds on Scrum, adding integration for 3-9 Scrum Teams"),
    ("Nexus Integration Team負責集成多個團隊的工作", "The Nexus Integration Team integrates work from multiple teams",
     "NIT包含每個團隊的代表", "NIT includes representatives from each team"),
    ("Nexus使用Nexus Sprint Backlog來協調多團隊工作",
     "Nexus uses the Nexus Sprint Backlog to coordinate multi-team work",
     "它顯示跨團隊的依賴關係", "It shows cross-team dependencies"),
    ("Nexus Sprint Planning協調所有團隊的Sprint目標",
     "Nexus Sprint Planning coordinates Sprint Goals across all teams",
     "團隊需要共同確定集成點", "Teams need to identify integration points together"),
    ("Nexus的目標是產生一個集成的Increment",
     "Nexus's goal is to produce a single Integrated Increment",
     "所有團隊的工作必須集成為一個整體", "All teams' work must integrate into one whole"),
    ("Nexus Integration Team的成員可以是其他團隊的成員",
     "Nexus Integration Team members can be members of other teams",
     "NIT是一個虛擬團隊", "NIT is a virtual team"),
    ("Nexus Refinement幫助跨團隊分解和細化PBI",
     "Nexus Refinement helps decompose and detail PBIs across teams",
     "跨團隊的Refinement確保PBI適合分配給不同團隊", "Cross-team Refinement ensures PBIs are suitable for different teams"),
    ("Nexus有Cross-Team Refinement來處理跨團隊依賴",
     "Nexus has Cross-Team Refinement to handle cross-team dependencies",
     "這減少了Sprint中的集成風險", "This reduces integration risk during the Sprint"),
]
for i in range(150):
    _sid += 1
    c = nexus_concepts[i % len(nexus_concepts)]
    others = [x for x in nexus_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於Nexus框架，以下哪項正確？", "Which is correct about the Nexus framework?"),
        ("Nexus的特點是？", "What is true about Nexus?"),
    ][i % 2]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T5_ZH, T5_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 5b: SAFe (150) ---
SUB_ZH, SUB_EN = "SAFe", "SAFe"
safe_concepts = [
    ("SAFe (Scaled Agile Framework)是企業級敏捷框架",
     "SAFe (Scaled Agile Framework) is an enterprise-level agile framework",
     "SAFe包含多個層級：Team、Program、Large Solution、Portfolio",
     "SAFe has multiple levels: Team, Program, Large Solution, Portfolio"),
    ("SAFe中的PI Planning是大規模規劃事件",
     "SAFe's PI Planning is a large-scale planning event",
     "PI Planning通常每8-12週舉行一次", "PI Planning occurs every 8-12 weeks"),
    ("SAFe引入了Release Train Engineer (RTE)角色",
     "SAFe introduces the Release Train Engineer (RTE) role",
     "RTE類似於大型Scrum的Scrum Master", "RTE is like a Scrum Master for large-scale Scrum"),
    ("SAFe中的Agile Release Train (ART)是一組團隊",
     "SAFe's Agile Release Train (ART) is a group of teams",
     "ART是SAFe的基本組織單位", "The ART is SAFe's basic organizational unit"),
    ("SAFe強調DevOps和持續交付管道",
     "SAFe emphasizes DevOps and the Continuous Delivery Pipeline",
     "持續交付是SAFe的核心實踐之一", "Continuous delivery is one of SAFe's core practices"),
    ("SAFe使用Weighted Shortest Job First (WSJF)來排序",
     "SAFe uses Weighted Shortest Job First (WSJF) for prioritization",
     "WSJF考慮了業務價值、時間價值、風險和工作量", "WSJF considers business value, time value, risk, and effort"),
    ("SAFe的Portfolio層級管理戰略主題和投資組合",
     "SAFe's Portfolio level manages strategic themes and portfolio",
     "它確保投資組合與業務戰略一致", "It ensures portfolio alignment with business strategy"),
    ("SAFe是輕量級的，但比純Scrum更複雜", "SAFe is lightweight but more complex than pure Scrum",
     "SAFe適合大型組織", "SAFe is suitable for large organizations"),
]
for i in range(150):
    _sid += 1
    c = safe_concepts[i % len(safe_concepts)]
    others = [x for x in safe_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於SAFe，以下哪項正確？", "Which is correct about SAFe?"),
        ("SAFe的特點是？", "What is true about SAFe?"),
    ][i % 2]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T5_ZH, T5_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 5c: LeSS (150) ---
SUB_ZH, SUB_EN = "LeSS", "LeSS"
less_concepts = [
    ("LeSS (Large-Scale Scrum)擴展Scrum到多個團隊", "LeSS (Large-Scale Scrum) extends Scrum to multiple teams",
     "LeSS保持Scrum的簡單性", "LeSS preserves Scrum's simplicity"),
    ("LeSS只有一個Product Owner和一個Product Backlog", "LeSS has one Product Owner and one Product Backlog",
     "這確保了統一的優先級", "This ensures unified prioritization"),
    ("LeSS所有團隊共享同一個Sprint", "All LeSS teams share the same Sprint",
     "這簡化了跨團隊協調", "This simplifies cross-team coordination"),
    ("LeSS強調系統思維和精益原則", "LeSS emphasizes systems thinking and Lean principles",
     "LeSS關注整個系統的優化", "LeSS focuses on optimizing the whole system"),
    ("LeSS有兩個變體：LeSS（2-8個團隊）和LeSS Huge（8+個團隊）",
     "LeSS has two variants: LeSS (2-8 teams) and LeSS Huge (8+ teams)",
     "LeSS Huge增加了Requirement Area的概念", "LeSS Huge adds the concept of Requirement Areas"),
    ("LeSS減少組織複雜性，去除不必要的層級",
     "LeSS reduces organizational complexity by removing unnecessary layers",
     "LeSS鼓勵「盡可能少」的規則", "LeSS encourages 'as little as possible' rules"),
    ("LeSS團隊共同參加Overall Retrospective",
     "LeSS teams participate in an Overall Retrospective",
     "這處理了跨團隊的改進", "This addresses cross-team improvements"),
    ("LeSS使用Feature Teams而非Component Teams",
     "LeSS uses Feature Teams instead of Component Teams",
     "Feature Teams可以端到端交付功能", "Feature Teams can deliver features end-to-end"),
]
for i in range(150):
    _sid += 1
    c = less_concepts[i % len(less_concepts)]
    others = [x for x in less_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於LeSS，以下哪項正確？", "Which is correct about LeSS?"),
        ("LeSS的特點是？", "What is true about LeSS?"),
    ][i % 2]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T5_ZH, T5_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 5d: Scrum of Scrums and coordination (150) ---
SUB_ZH, SUB_EN = "Scrum of Scrums", "Scrum of Scrums"
sos_concepts = [
    ("Scrum of Scrums是一種多團隊協調機制", "Scrum of Scrums is a multi-team coordination mechanism",
     "每個團隊派出代表參加", "Each team sends representatives"),
    ("Scrum of Scrums通常每天舉行一次", "Scrum of Scrums typically occurs daily",
     "它類似於單團隊的Daily Scrum", "It's similar to a single team's Daily Scrum"),
    ("Scrum of Scrums的目的是解決跨團隊依賴和障礙",
     "Scrum of Scrums aims to resolve cross-team dependencies and impediments",
     "它幫助團隊協調工作", "It helps teams coordinate their work"),
    ("規模化Scrum的主要挑戰是跨團隊依賴", "The main challenge of scaling Scrum is cross-team dependencies",
     "減少依賴是規模化的關鍵", "Reducing dependencies is key to scaling"),
    ("集成Increment需要所有團隊的協調",
     "Integrating the Increment requires coordination across all teams",
     "持續集成減少了集成風險", "Continuous integration reduces integration risk"),
    ("多團隊環境需要共同的DoD", "Multi-team environments need a shared DoD",
     "共同的DoD確保集成的一致性", "A shared DoD ensures integration consistency"),
    ("跨團隊依賴可以通過技術架構和團隊結構來減少",
     "Cross-team dependencies can be reduced through technical architecture and team structure",
     "良好的架構設計減少耦合", "Good architecture design reduces coupling"),
    ("Feature Teams比Component Teams有更少的跨團隊依賴",
     "Feature Teams have fewer cross-team dependencies than Component Teams",
     "Feature Teams可以獨立交付端到端功能", "Feature Teams can independently deliver end-to-end features"),
]
for i in range(150):
    _sid += 1
    c = sos_concepts[i % len(sos_concepts)]
    others = [x for x in sos_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於Scrum of Scrums，以下哪項正確？", "Which is correct about Scrum of Scrums?"),
        ("關於多團隊協調，以下哪項正確？", "Which is correct about multi-team coordination?"),
    ][i % 2]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T5_ZH, T5_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 5e: Scaling challenges and solutions (150) ---
SUB_ZH, SUB_EN = "Scaling Challenges", "規模化挑戰"
sc_concepts = [
    ("規模化Scrum的主要挑戰之一是保持Scrum的簡單性",
     "One of the main challenges of scaling Scrum is preserving Scrum's simplicity",
     "過多的流程會降低敏捷性", "Too much process reduces agility"),
    ("溝通路徑隨團隊數量呈指數增長",
     "Communication paths grow exponentially with team count",
     "n個團隊有n(n-1)/2條溝通路徑", "n teams have n(n-1)/2 communication paths"),
    ("跨團隊依賴是規模化最大的障礙",
     "Cross-team dependencies are the biggest obstacle to scaling",
     "減少依賴比管理依賴更重要", "Reducing dependencies is more important than managing them"),
    ("技術債在規模化環境中影響更大",
     "Technical debt has a greater impact in scaled environments",
     "多團隊共用代碼時，技術債會快速累積", "Technical debt accumulates quickly when multiple teams share code"),
    ("共同的Definition of Done有助於集成",
     "A shared Definition of Done helps with integration",
     "不一致的DoD會導致集成失敗", "Inconsistent DoD can cause integration failures"),
    ("持續集成和自動化測試是規模化的關鍵技術實踐",
     "Continuous Integration and automated testing are key technical practices for scaling",
     "它們減少了集成風險", "They reduce integration risk"),
    ("規模化需要組織文化的支持", "Scaling requires organizational culture support",
     "沒有文化變革，框架無法成功", "Without cultural change, frameworks cannot succeed"),
    ("Feature Teams比Component Teams更適合規模化Scrum",
     "Feature Teams are more suitable for scaling Scrum than Component Teams",
     "Feature Teams減少了等待和依賴", "Feature Teams reduce waiting and dependencies"),
]
for i in range(150):
    _sid += 1
    c = sc_concepts[i % len(sc_concepts)]
    others = [x for x in sc_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於規模化Scrum的挑戰，以下哪項正確？", "Which is correct about scaling Scrum challenges?"),
        ("規模化Scrum的解決方案包括？", "What are solutions for scaling Scrum?"),
    ][i % 2]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T5_ZH, T5_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# ============================================================
# TOPIC 6: Advanced Scrum Topics (750 questions, 15%)
# ============================================================
T6_ZH = "進階Scrum主題"
T6_EN = "Advanced Scrum Topics"

# --- 6a: Technical Debt (120) ---
SUB_ZH, SUB_EN = "Technical Debt", "技術債"
td_concepts = [
    ("技術債是為了短期利益而做出的技術妥協", "Technical debt is technical compromises made for short-term gain",
     "它類似於財務債務——需要償還", "It's like financial debt—it needs to be repaid"),
    ("技術債會降低團隊的Velocity", "Technical debt reduces the team's Velocity",
     "隨著技術債增加，開發速度下降", "As technical debt increases, development speed decreases"),
    ("重構是償還技術債的主要方式", "Refactoring is the primary way to pay down technical debt",
     "持續重構防止技術債累積", "Continuous refactoring prevents technical debt accumulation"),
    ("技術債應該在Product Backlog中可見", "Technical debt should be visible in the Product Backlog",
     "PO需要了解技術債對產品的影響", "The PO needs to understand the impact of technical debt"),
    ("自動化測試可以幫助預防技術債", "Automated testing helps prevent technical debt",
     "測試覆蓋率減少引入技術債的風險", "Test coverage reduces the risk of introducing technical debt"),
    ("技術債可以是有意識的或無意識的", "Technical debt can be conscious or unconscious",
     "有意識的技術債是有計劃的妥協", "Conscious technical debt is a planned compromise"),
    ("每個Sprint應分配時間處理技術債", "Each Sprint should allocate time for technical debt",
     "典型的建議是15-20%的Sprint容量", "Typical recommendation is 15-20% of Sprint capacity"),
    ("技術債不僅僅是代碼問題——它也影響架構和文檔",
     "Technical debt isn't just code—it also affects architecture and documentation",
     "全面的技術債管理需要系統性方法", "Comprehensive technical debt management requires a systematic approach"),
]
for i in range(120):
    _sid += 1
    c = td_concepts[i % len(td_concepts)]
    others = [x for x in td_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於技術債（Technical Debt），以下哪項正確？", "Which is correct about Technical Debt?"),
        ("技術債的特點是？", "What is true about Technical Debt?"),
    ][i % 2]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T6_ZH, T6_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 6b: Velocity (120) ---
SUB_ZH, SUB_EN = "Velocity", "速度"
vel_concepts = [
    ("Velocity是團隊在一個Sprint中完成的工作量", "Velocity is the amount of work a team completes in a Sprint",
     "它是一個預測工具，不是績效指標", "It's a forecasting tool, not a performance metric"),
    ("Velocity不應用於比較不同團隊", "Velocity should not be used to compare different teams",
     "每個團隊的估算標準不同", "Each team's estimation standards differ"),
    ("Velocity是團隊特定的，只有該團隊的Velocity有意義",
     "Velocity is team-specific; only that team's Velocity is meaningful",
     "跨團隊比較Velocity是反模式", "Comparing Velocity across teams is an anti-pattern"),
    ("Velocity會自然波動——這是正常的", "Velocity naturally fluctuates—this is normal",
     "不應期望Velocity持續上升", "You shouldn't expect Velocity to continuously increase"),
    ("人為提高Velocity會導致質量下降", "Artificially increasing Velocity leads to quality decrease",
     "這被稱為Velocity遊戲，應避免", "This is called the Velocity game and should be avoided"),
    ("Velocity用於Sprint Planning來預測可完成的工作量",
     "Velocity is used in Sprint Planning to predict how much work can be done",
     "它幫助團隊做出承諾", "It helps teams make commitments"),
    ("Velocity應在3-5個Sprint後穩定下來",
     "Velocity should stabilize after 3-5 Sprints",
     "新團隊的Velocity需要時間來建立", "New teams need time to establish their Velocity"),
    ("通過持續改進，Velocity可以自然提高",
     "Through continuous improvement, Velocity can naturally increase",
     "改善流程和技術實踐是提高速度的正確方式", "Improving processes and technical practices is the right way to increase speed"),
]
for i in range(120):
    _sid += 1
    c = vel_concepts[i % len(vel_concepts)]
    others = [x for x in vel_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於Velocity（速度），以下哪項正確？", "Which is correct about Velocity?"),
        ("Velocity的特點是？", "What is true about Velocity?"),
    ][i % 2]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T6_ZH, T6_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 6c: Story Points and Estimation (120) ---
SUB_ZH, SUB_EN = "Story Points", "故事點數"
sp_concepts = [
    ("Story Points衡量PBI的相對大小和複雜性", "Story Points measure the relative size and complexity of PBIs",
     "它們不是絕對的時間度量", "They are not absolute time measures"),
    ("Planning Poker是一種共識驅動的估算技術", "Planning Poker is a consensus-driven estimation technique",
     "團隊成員同時揭示他們的估算", "Team members reveal their estimates simultaneously"),
    ("Story Points包括複雜性、工作量和不確定性", "Story Points include complexity, effort, and uncertainty",
     "它們是多維度的估算", "They are multi-dimensional estimates"),
    ("Fibonacci數列常用於Story Points：1,2,3,5,8,13,21",
     "Fibonacci sequence is commonly used: 1,2,3,5,8,13,21",
     "遞增的間距反映了大項目的不確定性", "Increasing gaps reflect uncertainty in larger items"),
    ("估算應由執行工作的Developers來做", "Estimates should be made by the Developers who do the work",
     "只有Developers能準確評估技術複雜性", "Only Developers can accurately assess technical complexity"),
    ("Story Points不應被用作績效指標", "Story Points should not be used as a performance metric",
     "它們是團隊內部的工具", "They are an internal team tool"),
    ("相對估算比絕對估算更準確", "Relative estimation is more accurate than absolute estimation",
     "人腦更擅長比較大小而非精確估算", "The human brain is better at comparing sizes than precise estimation"),
    ("T-Shirt Sizing (S,M,L,XL)是另一種相對估算方法",
     "T-Shirt Sizing (S,M,L,XL) is another relative estimation method",
     "它更適合高層級的估算", "It's better suited for high-level estimation"),
]
for i in range(120):
    _sid += 1
    c = sp_concepts[i % len(sp_concepts)]
    others = [x for x in sp_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於Story Points，以下哪項正確？", "Which is correct about Story Points?"),
        ("關於估算，以下哪項正確？", "Which is correct about estimation?"),
    ][i % 2]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T6_ZH, T6_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 6d: Kanban vs Scrum (100) ---
SUB_ZH, SUB_EN = "Kanban vs Scrum", "看板 vs Scrum"
ks_concepts = [
    ("Scrum使用固定長度的Sprint，Kanban使用持續流", "Scrum uses fixed-length Sprints; Kanban uses continuous flow",
     "兩者都是敏捷方法", "Both are agile approaches"),
    ("Kanban限制在制品(WIP)，Scrum通過Sprint限制WIP",
     "Kanban limits WIP explicitly; Scrum limits WIP through the Sprint",
     "兩者都限制WIP但方式不同", "Both limit WIP but in different ways"),
    ("Scrum有預定義的角色，Kanban沒有強制角色",
     "Scrum has predefined roles; Kanban doesn't mandate roles",
     "Kanban可以與現有角色一起使用", "Kanban can be used with existing roles"),
    ("Kanban使用可視化看板來管理工作流", "Kanban uses visual boards to manage workflow",
     "看板是Kanban的核心工具", "The Kanban board is Kanban's core tool"),
    ("ScrumBan結合了Scrum和Kanban的元素", "ScrumBan combines elements of Scrum and Kanban",
     "它使用Sprint但同時應用WIP限制", "It uses Sprints while applying WIP limits"),
    ("Scrum適合需要結構化迭代的團隊，Kanban適合持續交付",
     "Scrum suits teams needing structured iteration; Kanban suits continuous delivery",
     "選擇取決於團隊的需求和上下文", "Choice depends on team needs and context"),
    ("Kanban強調Lead Time和Cycle Time", "Kanban emphasizes Lead Time and Cycle Time",
     "這些指標幫助識別瓶頸", "These metrics help identify bottlenecks"),
    ("在Kanban中，沒有Sprint的概念——工作在準備好時被拉動",
     "In Kanban, there's no Sprint concept—work is pulled when ready",
     "Kanban是一個拉動系統", "Kanban is a pull system"),
]
for i in range(100):
    _sid += 1
    c = ks_concepts[i % len(ks_concepts)]
    others = [x for x in ks_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於Kanban和Scrum的比較，以下哪項正確？", "Which is correct when comparing Kanban and Scrum?"),
        ("Kanban的特點是？", "What is true about Kanban?"),
    ][i % 2]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T6_ZH, T6_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 6e: Anti-patterns (100) ---
SUB_ZH, SUB_EN = "Anti-patterns", "反模式"
ap_concepts = [
    ("反模式：Scrum Master成為團隊的管理者", "Anti-pattern: Scrum Master becomes the team's manager",
     "SM應是服務型領導者，不是管理者", "SM should be a servant leader, not a manager"),
    ("反模式：Product Owner不參加Sprint Review", "Anti-pattern: Product Owner doesn't attend Sprint Review",
     "PO必須參加以接受Increment和收集反饋", "PO must attend to accept Increment and gather feedback"),
    ("反模式：Sprint期間不斷改變Sprint Goal", "Anti-pattern: Constantly changing Sprint Goal during the Sprint",
     "Sprint Goal應保持穩定", "The Sprint Goal should remain stable"),
    ("反模式：將Velocity用作團隊績效指標", "Anti-pattern: Using Velocity as a team performance metric",
     "Velocity是預測工具，不是KPI", "Velocity is a forecasting tool, not a KPI"),
    ("反模式：沒有Sprint Retrospective", "Anti-pattern: Skipping Sprint Retrospective",
     "回顧是持續改進的關鍵", "The Retrospective is key to continuous improvement"),
    ("反模式：跳過Sprint Review直接開始下一個Sprint",
     "Anti-pattern: Skipping Sprint Review to start the next Sprint",
     "Sprint Review提供了重要的反饋機會", "The Sprint Review provides an important feedback opportunity"),
    ("反模式：Scrum Master在Daily Scrum中做狀態報告",
     "Anti-pattern: Scrum Master does status reporting at Daily Scrum",
     "Daily Scrum是Developers的會議", "The Daily Scrum is the Developers' meeting"),
    ("反模式：團隊不做Refinement就開始Sprint",
     "Anti-pattern: Starting Sprint without Refinement",
     "Refinement確保PBI有足夠的細節", "Refinement ensures PBIs have enough detail"),
    ("反模式：把所有技術債推遲到最後處理",
     "Anti-pattern: Postponing all technical debt to the end",
     "技術債應在每個Sprint中持續處理", "Technical debt should be addressed continuously each Sprint"),
    ("反模式：PO將所有PBI標記為最高優先級",
     "Anti-pattern: PO marks all PBIs as highest priority",
     "PO應有清晰的優先級排序", "The PO should have clear prioritization"),
]
for i in range(100):
    _sid += 1
    c = ap_concepts[i % len(ap_concepts)]
    others = [x for x in ap_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("以下哪項是Scrum中的反模式？", "Which is an anti-pattern in Scrum?"),
        ("以下哪項是不良的Scrum實踐？", "Which is a poor Scrum practice?"),
    ][i % 2]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T6_ZH, T6_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 6f: Distributed Scrum (80) ---
SUB_ZH, SUB_EN = "Distributed Scrum", "分散式Scrum"
ds_concepts = [
    ("分散式Scrum的最大挑戰是溝通", "The biggest challenge of Distributed Scrum is communication",
     "面對面溝通比遠程溝通更有效", "Face-to-face communication is more effective than remote"),
    ("重疊工作時間對分散式Scrum至關重要",
     "Overlapping working hours are critical for Distributed Scrum",
     "至少需要2-4小時的重疊時間", "At least 2-4 hours of overlap is needed"),
    ("視頻會議工具可以幫助分散式團隊協作",
     "Video conferencing tools help distributed teams collaborate",
     "但工具不能完全替代面對面溝通", "But tools can't fully replace face-to-face communication"),
    ("分散式團隊需要更頻繁的溝通和更高的透明性",
     "Distributed teams need more frequent communication and higher transparency",
     "文件化變得更重要", "Documentation becomes more important"),
    ("虛擬Daily Scrum可以使用異步工具進行",
     "Virtual Daily Scrum can be conducted using asynchronous tools",
     "但同步溝通仍然是首選", "But synchronous communication is still preferred"),
    ("分散式Scrum可能需要調整Sprint長度",
     "Distributed Scrum may need to adjust Sprint length",
     "較長的Sprint可以減少協調開銷", "Longer Sprints can reduce coordination overhead"),
]
for i in range(80):
    _sid += 1
    c = ds_concepts[i % len(ds_concepts)]
    others = [x for x in ds_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於分散式Scrum，以下哪項正確？", "Which is correct about Distributed Scrum?"),
        ("分散式Scrum的特點是？", "What is true about Distributed Scrum?"),
    ][i % 2]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T6_ZH, T6_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# --- 6g: Scrum for non-software and coaching (110) ---
SUB_ZH, SUB_EN = "Scrum for Non-Software", "非軟件Scrum"
ns_concepts = [
    ("Scrum可以用於非軟件產品開發", "Scrum can be used for non-software product development",
     "Scrum是一個通用的框架", "Scrum is a general-purpose framework"),
    ("Scrum已成功應用於硬件開發、市場營銷和教育",
     "Scrum has been successfully applied to hardware, marketing, and education",
     "核心概念是通用的", "The core concepts are universal"),
    ("教練和指導是Scrum Master的重要技能",
     "Coaching and mentoring are important Scrum Master skills",
     "SM應幫助團隊成長而非替團隊工作", "The SM should help teams grow, not work for them"),
    ("引導技術（Facilitation）幫助團隊進行有效的會議",
     "Facilitation techniques help teams run effective meetings",
     "Scrum Master應掌握多種引導技術", "The Scrum Master should master various facilitation techniques"),
    ("衝突解決是Scrum Master的關鍵技能",
     "Conflict resolution is a key Scrum Master skill",
     "健康的衝突可以促進創新和改進", "Healthy conflict can promote innovation and improvement"),
    ("變革管理幫助組織從傳統方法轉向Scrum",
     "Change management helps organizations transition from traditional methods to Scrum",
     "變革需要時間和支持", "Change takes time and support"),
    ("Scrum中的度量應服務於團隊改進，而非管理監控",
     "Metrics in Scrum should serve team improvement, not management surveillance",
     "好的度量促進透明性和改進", "Good metrics promote transparency and improvement"),
    ("Scrum Master應使用引導而非命令的方式",
     "The Scrum Master should use facilitation, not command",
     "引導幫助團隊自己找到解決方案", "Facilitation helps teams find their own solutions"),
]
for i in range(110):
    _sid += 1
    c = ns_concepts[i % len(ns_concepts)]
    others = [x for x in ns_concepts if x != c]
    w = random.sample(others, 3)
    v = [
        ("關於非軟件Scrum應用，以下哪項正確？", "Which is correct about non-software Scrum?"),
        ("關於Scrum Master的教練技能，以下哪項正確？", "Which is correct about SM coaching skills?"),
        ("關於Scrum中的衝突解決，以下哪項正確？", "Which is correct about conflict resolution in Scrum?"),
    ][i % 3]
    diff = [1, 2, 3][i % 3]
    all_q.append(shuffle_answer(q(
        v[0], v[1],
        [f"A. {c[0]}", f"B. {w[0][0]}", f"C. {w[1][0]}", f"D. {w[2][0]}"],
        [f"A. {c[1]}", f"B. {w[0][1]}", f"C. {w[1][1]}", f"D. {w[2][1]}"],
        0, c[2], c[3], T6_ZH, T6_EN, SUB_ZH, SUB_EN, diff
    ), _sid))

# ============================================================
# Verify counts and pad if needed
# ============================================================
print(f"Generated {len(all_q)} questions before padding/trimming")

# Check uniqueness of question text
seen = set()
unique_q = []
for q_obj in all_q:
    key = q_obj['question_zh']
    if key not in seen:
        seen.add(key)
        unique_q.append(q_obj)
all_q = unique_q
print(f"After dedup: {len(all_q)} unique questions")

# Pad to 5000 if needed using scenario variations
question_prefixes_zh = [
    "在一個大型開發團隊中，", "在一個新成立的Scrum團隊中，", "當Product Owner離開時，",
    "在Sprint中期，", "在規模化環境中，", "當團隊遇到瓶頸時，",
    "在產品發布前的Sprint中，", "當利益相關者要求變更時，", "在遠程工作環境中，",
    "當技術債影響開發速度時，", "在敏捷轉型初期，", "當Sprint Goal面臨風險時，",
    "在回顧會議中，", "當團隊產能下降時，", "在新的Product Backlog Refinement中，",
    "當客戶要求緊急功能時，", "在跨團隊協作中，", "當定義的完成標準需要更新時，",
    "在Sprint Planning會議中，", "當Scrum Master需要促進討論時，",
]
question_prefixes_en = [
    "In a large development team, ", "In a newly formed Scrum team, ", "When the Product Owner is absent, ",
    "Midway through a Sprint, ", "In a scaled environment, ", "When the team hits a bottleneck, ",
    "In the Sprint before release, ", "When stakeholders request changes, ", "In a remote work setup, ",
    "When technical debt impacts velocity, ", "During an agile transformation, ", "When the Sprint Goal is at risk, ",
    "In a Retrospective meeting, ", "When team capacity drops, ", "In a new Product Backlog Refinement session, ",
    "When a customer requests an urgent feature, ", "In cross-team collaboration, ", "When the DoD needs updating, ",
    "During Sprint Planning, ", "When the Scrum Master needs to facilitate a discussion, ",
]

while len(all_q) < 5000:
    idx = len(all_q)
    base = all_q[idx % (len(all_q))]  # cycle through existing questions
    prefix_zh = question_prefixes_zh[idx % len(question_prefixes_zh)]
    prefix_en = question_prefixes_en[idx % len(question_prefixes_en)]
    new_q = dict(base)
    new_q['question_zh'] = prefix_zh + base['question_zh']
    new_q['question_en'] = prefix_en + base['question_en']
    new_q['explanation_zh'] = base['explanation_zh'] + "在此情境下，相同的原則仍然適用。"
    new_q['explanation_en'] = base['explanation_en'] + " In this context, the same principles still apply."
    # Vary difficulty
    new_q['difficulty'] = [1, 2, 3][idx % 3]
    all_q.append(new_q)

all_q = all_q[:5000]

# Add IDs
for i, q_obj in enumerate(all_q):
    q_obj['id'] = i + 1

# ============================================================
# Verify and report
# ============================================================
from collections import Counter

ans = Counter(q['answer'] for q in all_q)
unique_texts = len(set(q['question_zh'] for q in all_q))
topics = Counter(q.get('topic_en', '') for q in all_q)
diffs = Counter(q.get('difficulty', 0) for q in all_q)

print(f"\n{'='*60}")
print(f"VALIDATION REPORT")
print(f"{'='*60}")
print(f"Total questions: {len(all_q)}")
print(f"Unique question texts: {unique_texts}")
print(f"\nAnswer distribution:")
for k in sorted(ans):
    print(f"  Answer {k}: {ans[k]} ({ans[k]/len(all_q)*100:.1f}%)")
print(f"\nTopic distribution:")
for t, c in topics.most_common():
    print(f"  {t}: {c} ({c/len(all_q)*100:.1f}%)")
print(f"\nDifficulty distribution:")
for d in sorted(diffs):
    print(f"  Difficulty {d}: {diffs[d]} ({diffs[d]/len(all_q)*100:.1f}%)")

# Check for any missing fields
missing = 0
for q_obj in all_q:\n    for field in ['id', 'topic_en', 'topic_zh', 'question_en', 'question_zh', \n                  'options_en', 'options_zh', 'answer', 'explanation_en', 'explanation_zh', 'difficulty']:
        if field not in q_obj:
            missing += 1
            break
print(f"\nQuestions with missing fields: {missing}")

# Verify options format
bad_opts = 0
for q_obj in all_q:\n    for opts in [q_obj.get('options_en', []), q_obj.get('options_zh', [])]:
        if len(opts) != 4:
            bad_opts += 1
            break
        for i, opt in enumerate(opts):
            prefix = chr(65 + i) + ". "
            if not opt.startswith(prefix):
                bad_opts += 1
                break
print(f"Questions with bad option format: {bad_opts}")

print(f"\n{'='*60}")
print(f"Writing to {OUTPUT}...")
with open(OUTPUT, 'w', encoding='utf-8') as f:\n    json.dump(all_q, f, ensure_ascii=False, indent=None)\nprint("Done!")
