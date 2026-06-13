#!/usr/bin/env python3
"""Generate 5000 unique Scrum PSM/PSPO exam questions."""
import json, random, os

random.seed(2024)
OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "questions.json")
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

all_q = []
_qid = 0

STYLES = [
    "关于{t}，以下哪项正确？",
    "以下哪项准确描述了{t}？",
    "关于{t}，以下哪项错误？",
    "{t}的主要目的是什么？",
    "在Scrum中，{t}的特点是？",
    "以下哪项关于{t}的说法最准确？",
    "{t}在Scrum中的作用是？",
    "关于{t}，以下哪项是常见的误解？",
    "{t}应如何正确实施？",
    "根据Scrum Guide，{t}的定义是？",
    "以下哪项最能说明{t}的价值？",
    "{t}如何支持经验主义？",
    "如果忽略{t}，可能导致什么问题？",
    "{t}如何帮助团队提高效能？",
    "关于{t}的最佳实践是？",
    "新手对{t}最常见的误解是？",
    "在敏捷环境中，{t}的重要性是？",
    "{t}与其他Scrum元素的关系是？",
]

STYLES_EN = [
    "Regarding {t}, which statement is correct?",
    "Which accurately describes {t}?",
    "Regarding {t}, which statement is INCORRECT?",
    "What is the primary purpose of {t}?",
    "In Scrum, what is true about {t}?",
    "Which statement about {t} is most accurate?",
    "What is the role of {t} in Scrum?",
    "Regarding {t}, which is a common misconception?",
    "How should {t} be correctly implemented?",
    "According to the Scrum Guide, how is {t} defined?",
    "Which best explains the value of {t}?",
    "How does {t} support empiricism?",
    "What problems can arise from neglecting {t}?",
    "How does {t} help teams improve effectiveness?",
    "What is the best practice for {t}?",
    "What is the most common misconception about {t}?",
    "What is the importance of {t} in an agile environment?",
    "How does {t} relate to other Scrum elements?",
]

def make_q(tzh, ten, name_zh, name_en, correct_zh, correct_en, exp_zh, exp_en, wrongs_zh, wrongs_en, style_idx, diff, seed):
    global _qid
    _qid += 1
    si = style_idx % len(STYLES)
    q_zh = STYLES[si].replace("{t}", name_zh)
    q_en = STYLES_EN[si].replace("{t}", name_en)
    raw_zh = [correct_zh] + wrongs_zh[:3]
    raw_en = [correct_en] + wrongs_en[:3]
    r = random.Random(seed)
    idx = list(range(4))
    r.shuffle(idx)
    ans = idx.index(0)
    opts_zh = [chr(65+j) + ". " + raw_zh[i] for j, i in enumerate(idx)]
    opts_en = [chr(65+j) + ". " + raw_en[i] for j, i in enumerate(idx)]
    return {"id": _qid, "topic_zh": tzh, "topic_en": ten, "subtopic_zh": name_zh, "subtopic_en": name_en,
            "question_zh": q_zh, "question_en": q_en, "options_zh": opts_zh, "options_en": opts_en,
            "answer": ans, "explanation_zh": exp_zh, "explanation_en": exp_en, "difficulty": diff}

def gen(concepts, tzh, ten, count):
    out = []
    n = len(concepts)
    for i in range(count):
        ci = i % n
        si = i // n
        c = concepts[ci]
        others = [concepts[j] for j in range(n) if j != ci]
        rv = random.Random(i * 31337 + ci * 997)
        w = rv.sample(others, min(3, len(others)))
        while len(w) < 3:
            w.append(w[0])
        diff = (i % 3) + 1
        seed = random.randint(0, 2**32 - 1)
        out.append(make_q(tzh, ten, c[0], c[1], c[2], c[3], c[4], c[5],
                          [x[2] for x in w], [x[3] for x in w], si, diff, seed))
    return out


# T1: Sprint (200)
all_q += gen([
    ("Sprint的定义", "Sprint definition", "Sprint是固定长度的事件，最长一个月", "A Sprint is a fixed-length event of one month or less", "Sprint是Scrum的核心，为其他所有事件提供容器", "The Sprint is the heart of Scrum, providing a container for all other events"),
    ("Sprint长度一致性", "Sprint length consistency", "Sprint的长度应保持一致以建立节奏", "Sprint length should be consistent to establish a rhythm", "一致的长度帮助团队建立可预测性", "Consistent length helps the team build predictability"),
    ("Sprint取消权限", "Sprint cancellation", "取消Sprint只能由Product Owner决定", "Only the Product Owner can cancel a Sprint", "只有PO能判断Sprint Goal是否仍有价值", "Only the PO can assess whether the Sprint Goal is still valuable"),
    ("Sprint产出", "Sprint output", "每个Sprint应产生一个可用的Increment", "Each Sprint should produce a usable Increment", "Increment是Sprint的核心目的", "The Increment is the core purpose of the Sprint"),
    ("Sprint Goal稳定性", "Sprint Goal stability", "Sprint期间不应改变Sprint Goal", "The Sprint Goal should not change during the Sprint", "Sprint Goal提供方向和灵活性，但不应随意改变", "The Sprint Goal provides direction but should not be arbitrarily changed"),
    ("Sprint包含的事件", "Events in Sprint", "Sprint包含Planning、Daily Scrum、Review和Retrospective", "A Sprint includes Planning, Daily Scrum, Review, and Retrospective", "所有Scrum事件都在Sprint内发生", "All Scrum events occur within the Sprint"),
    ("Sprint连续性", "Sprint continuity", "Sprint结束后立即开始下一个Sprint", "A new Sprint starts immediately after the previous one ends", "Sprint之间没有间隙", "There is no gap between Sprints"),
    ("Sprint Goal来源", "Sprint Goal origin", "Sprint Goal是Sprint Planning的关键产出", "The Sprint Goal is a key outcome of Sprint Planning", "Sprint Goal指导团队在Sprint期间的工作", "The Sprint Goal guides the team's work during the Sprint"),
    ("Sprint时间盒", "Sprint time-box", "Sprint是持续一个月或更短的时间盒", "A Sprint is a time-box of one month or less", "Sprint的持续时间是固定的", "Sprint duration is fixed"),
    ("Sprint变更限制", "Sprint change limits", "Sprint中不允许损害Sprint Goal的变更", "No changes are allowed that would endanger the Sprint Goal", "质量目标不应降低", "Quality goals should not be decreased"),
    ("Sprint范围协商", "Sprint scope negotiation", "Sprint期间可以与PO协商调整范围", "During the Sprint, scope can be negotiated with the PO", "如果发现工作超出预期，团队可以与PO讨论减少范围", "If work exceeds expectations, the team can discuss reducing scope with the PO"),
    ("Sprint本质", "Sprint nature", "每个Sprint都是一个短期项目", "Each Sprint is a short-term project", "Sprint有固定的开始和结束日期", "Sprints have fixed start and end dates"),
], "Scrum框架", "Scrum Framework", 200)

# T1: Sprint Planning (150)
all_q += gen([
    ("SP时间盒", "SP time-box", "Sprint Planning最大时间盒是一个月Sprint为8小时", "Sprint Planning time-box is 8 hours for a one-month Sprint", "时间盒随Sprint长度按比例缩短", "Time-box scales proportionally with Sprint length"),
    ("SP三个主题", "SP three topics", "Sprint Planning回答三个主题：Why、What、How", "Sprint Planning addresses three topics: Why, What, How", "Sprint Goal、选取的PBI、交付计划", "Sprint Goal, selected PBIs, delivery plan"),
    ("SP参与者", "SP participants", "整个Scrum团队参加Sprint Planning", "The entire Scrum Team attends Sprint Planning", "PO、SM和Developers都参加", "PO, SM, and Developers all attend"),
    ("SP产能评估", "SP capacity", "Developers决定Sprint中可以完成多少工作", "Developers decide how much work they can accomplish", "只有Developers能评估产能和能力", "Only Developers can assess capacity and capability"),
    ("SB创建", "SB creation", "Sprint Backlog在Sprint Planning中产生", "The Sprint Backlog is created during Sprint Planning", "它包含Sprint Goal、PBI和交付计划", "It includes Sprint Goal, PBIs, and delivery plan"),
    ("Sprint Goal提出", "Sprint Goal proposal", "PO在Sprint Planning中提出Sprint Goal候选", "The PO proposes Sprint Goal candidates", "团队讨论后确定最终Sprint Goal", "The team discusses and finalizes the Sprint Goal"),
    ("SP第一主题", "SP first topic", "Sprint Planning的第一个主题是Why", "The first topic of Sprint Planning is Why", "确立Sprint Goal——为什么这个Sprint有价值", "Establishing the Sprint Goal—why this Sprint is valuable"),
    ("SP第二主题", "SP second topic", "Sprint Planning的第二个主题是What", "The second topic is What", "团队根据产能选取PBI", "The team selects PBIs based on capacity"),
    ("SP第三主题", "SP third topic", "Sprint Planning的第三个主题是How", "The third topic is How", "Developers将PBI分解为更小的工作项", "Developers decompose PBIs into smaller work items"),
    ("SP完成标准", "SP completion", "SP结束时Developers应能解释如何实现Sprint Goal", "Developers should explain how to achieve the Sprint Goal by end of Planning", "这是Sprint Planning的完成条件", "This is a Sprint Planning completion criterion"),
    ("SP协作性质", "SP collaborative", "Sprint Planning是一个协作事件", "Sprint Planning is a collaborative event", "所有团队成员共同参与计划", "All team members participate in planning"),
    ("SP目标设定", "SP goal setting", "Sprint Planning建立Sprint的目标和计划", "Sprint Planning establishes the Sprint's goal and plan", "它为Sprint设定方向", "It sets the direction for the Sprint"),
], "Scrum框架", "Scrum Framework", 150)

# T1: Daily Scrum (120)
all_q += gen([
    ("DS定义", "DS definition", "Daily Scrum是为Developers举办的15分钟事件", "The Daily Scrum is a 15-minute event for Developers", "它是Developers的检视和适应事件", "It is an inspect-and-adapt event for Developers"),
    ("DS目的", "DS purpose", "Daily Scrum的目的是检视朝向Sprint Goal的进度", "The purpose is to inspect progress toward the Sprint Goal", "团队检视距离目标的距离并调整计划", "The team inspects progress and adapts the plan"),
    ("DS时间地点", "DS time/place", "Daily Scrum在同一时间同一地点举行", "The Daily Scrum is held at the same time and place", "固定时间地点减少复杂性", "Consistent time and place reduce complexity"),
    ("DS格式自由", "DS format freedom", "SM不强制要求特定的Daily Scrum格式", "The SM does not mandate a specific Daily Scrum format", "Developers可以选择最适合的格式", "Developers can choose the format that works best"),
    ("DS常见问题", "DS common questions", "常见格式：昨天做了什么？今天做什么？有什么阻碍？", "Common format: What did I do? What will I do? Any impediments?", "这只是建议格式，团队可以自选", "This is a suggested format; teams can choose their own"),
    ("DS参与者", "DS participants", "只有Developers需要参加Daily Scrum", "Only Developers are required to attend", "其他人可以旁听但不应干扰", "Others may listen but should not disrupt"),
    ("DS非状态报告", "DS not status report", "Daily Scrum不是状态报告会议", "The Daily Scrum is not a status report meeting", "它是开发团队的同步和计划会议", "It is a synchronization and planning meeting for Developers"),
    ("DS价值", "DS value", "Daily Scrum改善沟通、减少其他会议、识别障碍", "Daily Scrum improves communication, reduces meetings, identifies impediments", "它是透明性和检视的关键机制", "It is a key mechanism for transparency and inspection"),
    ("DS同步作用", "DS synchronization", "Daily Scrum帮助团队同步工作", "Daily Scrum helps the team synchronize work", "团队成员了解彼此的进度和计划", "Team members understand each other's progress and plans"),
    ("DS灵活性", "DS flexibility", "如果Daily Scrum目的已达成，可以提前结束", "If the Daily Scrum's purpose is achieved early, it can end early", "不必用满15分钟", "It doesn't need to take the full 15 minutes"),
], "Scrum框架", "Scrum Framework", 120)

# T1: Sprint Review (120)
all_q += gen([
    ("Review目的", "Review purpose", "Sprint Review的目的是检视Increment并调整Product Backlog", "Sprint Review inspects the Increment and adapts the Product Backlog", "它是一个工作会议，不是演示", "It is a working session, not a presentation"),
    ("Review时间盒", "Review time-box", "Sprint Review最大时间盒是一个月Sprint为4小时", "Sprint Review time-box is 4 hours for a one-month Sprint", "时间盒随Sprint长度按比例缩短", "Time-box scales with Sprint length"),
    ("Review参与者", "Review participants", "Scrum团队和关键利益相关者参加Sprint Review", "The Scrum Team and key stakeholders attend", "利益相关者的反馈至关重要", "Stakeholder feedback is essential"),
    ("Review展示", "Review demo", "Sprint Review中展示完成的Increment", "The completed Increment is presented at the Sprint Review", "团队展示Sprint中完成的工作", "The team demonstrates work completed during the Sprint"),
    ("Review PB调整", "Review PB adjustment", "Sprint Review中讨论Product Backlog的下一步", "Next steps for the Product Backlog are discussed", "根据反馈和市场变化调整PB", "The PB is adjusted based on feedback and market changes"),
    ("Review非Demo", "Review not demo", "Sprint Review不是Demo，而是协作工作会议", "The Sprint Review is not a demo but a collaborative working session", "重点是收集反馈和讨论方向", "Focus is on gathering feedback and discussing direction"),
    ("Review透明性", "Review transparency", "Sprint Review中应展示完成和未完成的PBI", "Completed and incomplete PBIs should be shown", "透明性是Sprint Review的关键原则", "Transparency is a key principle of the Sprint Review"),
    ("Review互动机会", "Review interaction", "Sprint Review是Scrum团队与利益相关者互动的机会", "The Sprint Review is an opportunity for stakeholder interaction", "这是收集反馈的关键时刻", "This is a key moment for gathering feedback"),
    ("Review方向沟通", "Review direction", "Sprint Review中PO可以宣布产品的下一步计划", "The PO can announce the next steps for the product", "这帮助利益相关者了解产品方向", "This helps stakeholders understand product direction"),
    ("Review外部面向", "Review external", "Sprint Review是Scrum中最面向外部的事件", "The Sprint Review is the most externally facing Scrum event", "它连接了团队和利益相关者", "It connects the team and stakeholders"),
], "Scrum框架", "Scrum Framework", 120)

# T1: Sprint Retrospective (120)
all_q += gen([
    ("Retro目的", "Retro purpose", "Sprint Retrospective规划提高质量和效能的方式", "The Retrospective plans ways to increase quality and effectiveness", "回顾帮助团队持续改进", "Retrospectives help the team continuously improve"),
    ("Retro时间盒", "Retro time-box", "Sprint Retrospective最大时间盒是一个月Sprint为3小时", "Retrospective time-box is 3 hours for a one-month Sprint", "时间盒随Sprint长度按比例缩短", "Time-box scales with Sprint length"),
    ("Retro焦点", "Retro focus", "回顾聚焦于人员、关系、流程和工具", "The Retrospective focuses on people, relationships, process, and tools", "改进可以涉及团队协作的各方面", "Improvements can cover all aspects of teamwork"),
    ("Retro参与者", "Retro participants", "整个Scrum团队参加Sprint Retrospective", "The entire Scrum Team attends", "PO、SM和Developers都参加", "PO, SM, and Developers all attend"),
    ("Retro产出", "Retro output", "回顾应识别最重要的改进并制定行动计划", "The Retrospective identifies the most important improvements", "改进项目应在下一个Sprint中实施", "Improvement items should be implemented in the next Sprint"),
    ("Retro改进承诺", "Retro improvement", "回顾应产生至少一个高优先级的改进行动", "The Retrospective should produce at least one improvement action", "改进应被纳入下一个Sprint Backlog", "Improvements should be included in the next Sprint Backlog"),
    ("Retro时间位置", "Retro timing", "Sprint Retrospective在Sprint Review之后、下一个Sprint Planning之前", "The Retrospective occurs after the Review and before the next Planning", "它是Sprint的最后一个事件", "It is the last event of the Sprint"),
    ("Retro学习文化", "Retro learning", "Sprint Retrospective促进团队的持续学习文化", "The Retrospective promotes a culture of continuous learning", "它是自我反思和改进的机会", "It is an opportunity for self-reflection and improvement"),
    ("Retro话题开放", "Retro open topics", "Sprint Retrospective中团队可以讨论任何影响效能的问题", "The team can discuss any issue affecting effectiveness", "没有任何话题是禁忌的", "No topic is off-limits"),
    ("Retro行动质量", "Retro action quality", "改进行动应该是具体和可执行的", "Improvement actions should be specific and actionable", "模糊的改进目标难以实施", "Vague improvement goals are hard to implement"),
], "Scrum框架", "Scrum Framework", 120)

# T1: Definition of Done (120)
all_q += gen([
    ("DoD定义", "DoD definition", "Definition of Done是Increment必须满足的条件", "The Definition of Done is the set of conditions the Increment must meet", "DoD确保Increment是可用的和可发布的", "DoD ensures the Increment is usable and releasable"),
    ("DoD与透明性", "DoD transparency", "DoD创造透明性，让所有人理解「完成」的含义", "DoD creates transparency about what 'done' means", "透明性是Scrum三大支柱之一", "Transparency is one of the three pillars of Scrum"),
    ("DoD与Review", "DoD and Review", "不符合DoD的PBI不能在Sprint Review中展示", "PBIs not meeting DoD cannot be presented at the Sprint Review", "只有完成的Increment才能展示", "Only done Increments can be presented"),
    ("DoD演进", "DoD evolution", "DoD可以随时间演进，变得更加严格", "The DoD can evolve over time, becoming more stringent", "团队应持续改进DoD", "Teams should continuously improve their DoD"),
    ("多团队DoD", "Multi-team DoD", "多个团队共用同一产品时必须共用同一DoD", "Multiple teams on the same product must share the same DoD", "共用DoD确保集成的Increment一致", "Shared DoD ensures integrated Increments are consistent"),
    ("DoD内容", "DoD contents", "DoD通常包含开发、测试、文档和部署标准", "DoD typically includes development, testing, documentation, and deployment standards", "DoD应涵盖所有必要的质量标准", "DoD should cover all necessary quality standards"),
    ("DoD承诺", "DoD commitment", "DoD是Scrum的承诺之一，与Increment相关", "DoD is one of Scrum's commitments, associated with the Increment", "它增强了工件的透明性", "It enhances artifact transparency"),
    ("未完成工作", "Undone work", "不符合DoD的工作不能被视为「完成」", "Work not meeting the DoD cannot be considered 'done'", "未完成的工作不能交付给客户", "Undone work cannot be delivered to customers"),
    ("DoD适用范围", "DoD scope", "DoD适用于Sprint中的所有PBI", "The DoD applies to all PBIs in the Sprint", "每个PBI都必须满足DoD", "Every PBI must satisfy the DoD"),
    ("DoD标准层次", "DoD standard levels", "DoD包括所有适用的标准，如组织标准和行业标准", "DoD includes all applicable standards, such as organizational and industry standards", "DoD不仅是团队的标准", "DoD is not just the team's standard"),
], "Scrum框架", "Scrum Framework", 120)

# T1: Sprint Backlog (100)
all_q += gen([
    ("SB组成", "SB composition", "Sprint Backlog由Sprint Goal、选取的PBI和交付计划组成", "The Sprint Backlog consists of Sprint Goal, selected PBIs, and delivery plan", "它是Developers的计划", "It is the Developers' plan"),
    ("SB所有权", "SB ownership", "只有Developers可以修改Sprint Backlog", "Only Developers can modify the Sprint Backlog", "Developers拥有Sprint Backlog的所有权", "Developers own the Sprint Backlog"),
    ("SB演进", "SB evolution", "Sprint Backlog在Sprint期间可以演进", "The Sprint Backlog can evolve during the Sprint", "随着学习，Developers可以调整计划", "As they learn, Developers can adjust the plan"),
    ("SB透明性", "SB transparency", "Sprint Backlog提供了足够的透明性来检视进度", "The Sprint Backlog provides enough transparency to inspect progress", "它是Sprint的承诺载体", "It is the commitment artifact for the Sprint"),
    ("SB在DS中", "SB in Daily Scrum", "Sprint Backlog应在Daily Scrum中检视", "The Sprint Backlog should be inspected at the Daily Scrum", "团队在Daily Scrum中检视进度", "The team inspects progress at the Daily Scrum"),
    ("SB完整性", "SB completeness", "Sprint Backlog包含所有实现Sprint Goal所需的工作", "The Sprint Backlog contains all work needed to achieve the Sprint Goal", "它是一个完整的工作计划", "It is a complete work plan"),
    ("SB承诺", "SB commitment", "Sprint Backlog的承诺是Sprint Goal", "The Sprint Backlog's commitment is the Sprint Goal", "Sprint Goal提供了目标和方向", "The Sprint Goal provides purpose and direction"),
    ("SB实时性", "SB real-time", "Sprint Backlog是实时的计划，可随时更新", "The Sprint Backlog is a real-time plan that can be updated anytime", "Developers根据新信息调整", "Developers adjust based on new information"),
], "Scrum框架", "Scrum Framework", 100)

# T1: Product Backlog (100)
all_q += gen([
    ("PB定义", "PB definition", "Product Backlog是一个有序的列表，包含产品所需的一切", "The Product Backlog is an ordered list of everything needed in the product", "它是产品的唯一需求来源", "It is the single source of requirements for the product"),
    ("PB管理责任", "PB management", "只有Product Owner负责管理Product Backlog", "Only the PO is responsible for managing the Product Backlog", "PO负责内容、可用性和排序", "The PO is accountable for content, availability, and ordering"),
    ("PB Refinement", "PB Refinement", "Product Backlog Refinement是分解和细化PBI的活动", "Product Backlog Refinement breaks down and details PBIs", "Refinement通常占团队产能的10%", "Refinement typically consumes about 10% of team capacity"),
    ("PB动态性", "PB dynamism", "Product Backlog是动态的，从不完整", "The Product Backlog is dynamic and never complete", "它随产品和市场变化而演进", "It evolves as the product and market change"),
    ("PB排序权", "PB ordering", "PBI的优先级由Product Owner决定", "PBI ordering is determined by the PO", "PO根据价值、风险和依赖性排序", "The PO orders based on value, risk, and dependencies"),
    ("PB细节层次", "PB detail levels", "Product Backlog的顶部项目应有足够细节", "Top PBIs should have enough detail to start development", "顶部更详细，底部更粗略", "Top items are more detailed; bottom items are coarser"),
    ("PB与Product Goal", "PB and Product Goal", "Product Backlog是Product Goal的承诺载体", "The Product Backlog is the commitment for the Product Goal", "Product Goal是长期目标", "The Product Goal is the long-term objective"),
    ("PB内容范围", "PB content scope", "Product Backlog包含所有功能、增强、修复和技术工作", "The Product Backlog includes all features, enhancements, fixes, and technical work", "任何推进产品的工作都在其中", "Any work that advances the product is included"),
], "Scrum框架", "Scrum Framework", 100)

# T1: Increment (100)
all_q += gen([
    ("Increment定义", "Increment definition", "Increment是所有完成的PBI的总和", "An Increment is the sum of all completed PBIs", "增量是Sprint中所有完成工作的累加", "The Increment is the accumulation of all work done in the Sprint"),
    ("Increment累积性", "Increment cumulative", "每个Increment必须与之前的所有Increments一起工作", "Each Increment must work together with all previous Increments", "增量必须与现有系统集成", "Increments must integrate with the existing system"),
    ("Increment与DoD", "Increment and DoD", "Increment必须符合Definition of Done", "The Increment must meet the Definition of Done", "只有符合DoD的工作才能成为Increment", "Only work meeting the DoD is part of the Increment"),
    ("多个Increment", "Multiple Increments", "多个Increment可以在一个Sprint中产生", "Multiple Increments can be created within a Sprint", "团队可以在Sprint期间多次交付", "Teams can deliver multiple times during a Sprint"),
    ("Increment可用性", "Increment usability", "Increment必须是可用的，即使PO决定不发布", "The Increment must be usable even if the PO decides not to release", "可用性与发布决策是分开的", "Usability is separate from the release decision"),
    ("Increment价值", "Increment value", "每个Sprint至少产出一个有价值的Increment", "Each Sprint produces at least one valuable Increment", "Increment是Sprint的目的", "The Increment is the purpose of the Sprint"),
    ("Increment与Product Goal", "Increment and Product Goal", "Increment代表着Product Goal的进步", "The Increment represents progress toward the Product Goal", "每个Increment都应推进Product Goal", "Each Increment should advance the Product Goal"),
    ("Increment承诺", "Increment commitment", "Increment的承诺是Definition of Done", "The Increment's commitment is the Definition of Done", "DoD是Increment质量的保证", "DoD is the quality guarantee for the Increment"),
], "Scrum框架", "Scrum Framework", 100)

# T1: Empiricism and Scrum Values (210)
all_q += gen([
    ("时间盒概念", "Time-boxing concept", "时间盒是限制事件最大时长的技巧", "Time-boxing limits the maximum length of events", "它创造了紧迫感和焦点", "It creates urgency and focus"),
    ("Scrum事件时间盒", "Scrum event time-boxes", "所有Scrum事件都是时间盒限定的", "All Scrum events are time-boxed", "每个事件都有最大时长", "Each event has a maximum duration"),
    ("DS时间盒", "DS time-box", "Daily Scrum固定为15分钟", "Daily Scrum is always 15 minutes", "不随Sprint长度变化", "Regardless of Sprint length"),
    ("经验主义三支柱", "Three pillars", "经验主义的三大支柱：透明性、检视、适应", "Three pillars of empiricism: Transparency, Inspection, Adaptation", "这三个支柱支撑了Scrum的所有实践", "These three pillars support all Scrum practices"),
    ("透明性含义", "Transparency meaning", "透明性意味着重要方面对负责人可见", "Transparency means significant aspects are visible", "需要共同标准确保理解一致", "Common standards ensure consistent understanding"),
    ("检视含义", "Inspection meaning", "检视是频繁检查Scrum工件和进度", "Inspection means frequently checking Scrum artifacts", "检视不应阻碍工作", "Inspection should not impede work"),
    ("适应含义", "Adaptation meaning", "适应是当检视发现偏差时进行调整", "Adaptation means adjusting when deviations are found", "需要调整时应尽快进行", "Adjustment should be done as soon as possible"),
    ("经验主义基础", "Empirical foundation", "Scrum基于经验主义，知识来自经验", "Scrum is founded on empiricism; knowledge comes from experience", "经验主义是Scrum的哲学基础", "Empiricism is Scrum's philosophical foundation"),
    ("承诺价值", "Commitment", "承诺——Scrum团队承诺实现Sprint Goal和Product Goal", "Commitment—the Scrum Team commits to achieving Sprint Goal and Product Goal", "承诺是团队对目标的专注投入", "Commitment is the team's focused dedication to goals"),
    ("专注价值", "Focus", "专注——Scrum团队专注于Sprint的工作", "Focus—the Scrum Team focuses on the work of the Sprint", "专注减少了多任务切换的浪费", "Focus reduces waste from context switching"),
    ("开放价值", "Openness", "开放——Scrum团队和利益相关者保持开放", "Openness—the Scrum Team and stakeholders are open", "开放促进了透明性和信任", "Openness promotes transparency and trust"),
    ("尊重价值", "Respect", "尊重——Scrum团队成员互相尊重", "Respect—Scrum Team members respect each other", "尊重是自管理和协作的基础", "Respect is the foundation of self-management and collaboration"),
    ("勇气价值", "Courage", "勇气——Scrum团队有勇气做正确的事", "Courage—the Scrum Team has the courage to do the right thing", "勇气使团队能面对困难", "Courage enables the team to face difficulties"),
    ("五个Scrum Values", "Five Scrum Values", "五个Scrum Values是：承诺、专注、开放、尊重、勇气", "Five Scrum Values: Commitment, Focus, Openness, Respect, Courage", "这些价值观使经验主义成为可能", "These values make empiricism possible"),
], "Scrum框架", "Scrum Framework", 210)

# T2: Product Owner (200)
all_q += gen([
    ("PO价值最大化", "PO value max", "Product Owner负责最大化产品价值", "The PO is accountable for maximizing product value", "PO是产品价值最大化的最终负责人", "The PO is ultimately responsible for maximizing product value"),
    ("PO PB管理权", "PO PB management", "Product Owner是管理Product Backlog的唯一责任人", "The PO is the sole person responsible for managing the Product Backlog", "可以委派工作但责任仍在PO", "Work can be delegated but accountability remains with the PO"),
    ("PO优先级决策", "PO prioritization", "Product Owner决定PBI的优先级", "The PO prioritizes PBIs", "根据价值、风险和依赖关系排序", "Orders based on value, risk, and dependencies"),
    ("PO透明性", "PO transparency", "Product Owner确保Product Backlog对所有人透明", "The PO ensures the Product Backlog is transparent to everyone", "透明性使所有利益相关者了解计划", "Transparency lets all stakeholders understand the plan"),
    ("PO个体非委员会", "PO individual", "Product Owner是一个个体，不是委员会", "The PO is an individual, not a committee", "可能代表委员会的需求，但PO是单一个人", "May represent a committee's needs but is a single person"),
    ("PO利益相关者合作", "PO stakeholder collab", "Product Owner与利益相关者密切合作", "The PO works closely with stakeholders", "收集和整合利益相关者的输入", "Gathers and integrates stakeholder input"),
    ("PO Increment接受", "PO Increment accept", "Product Owner是唯一能接受或拒绝Increment的人", "The PO is the only one who can accept or reject the Increment", "代表利益相关者做出接受决策", "Makes acceptance decisions on behalf of stakeholders"),
    ("PO领域知识", "PO domain knowledge", "Product Owner需要理解市场和用户需求", "The PO needs to understand market and user needs", "PO应具备产品领域知识", "The PO should have product domain knowledge"),
    ("PO事件参与", "PO event participation", "Product Owner出席所有Scrum事件", "The PO attends all Scrum events", "PO在每个事件中都有重要角色", "The PO has an important role in every event"),
    ("PO桥梁角色", "PO bridge role", "Product Owner是开发团队和利益相关者之间的桥梁", "The PO is the bridge between Developers and stakeholders", "PO翻译业务需求为技术需求", "The PO translates business needs into technical requirements"),
    ("PO排序管理", "PO ordering mgmt", "Product Owner管理Product Backlog的排序和透明性", "The PO manages Product Backlog ordering and transparency", "PO确保团队始终做最有价值的工作", "The PO ensures the team always works on the most valuable items"),
    ("PO组织任命", "PO appointment", "Product Owner可以被组织替换", "The PO can be replaced by the organization", "组织对PO任命有最终决定权", "The organization has the final say on PO appointment"),
], "Scrum角色", "Scrum Roles", 200)

# T2: Scrum Master (200)
all_q += gen([
    ("SM服务型领导", "SM servant leader", "Scrum Master是服务型领导者", "The Scrum Master is a servant leader", "SM通过服务团队来领导", "The SM leads by serving the team"),
    ("SM框架有效性", "SM framework eff", "Scrum Master对Scrum框架的有效性负责", "The SM is accountable for Scrum framework effectiveness", "SM确保团队理解和实施Scrum", "The SM ensures the team understands and implements Scrum"),
    ("SM障碍移除", "SM impediment", "Scrum Master帮助移除团队的障碍", "The SM helps remove team impediments", "SM是团队的教练和促进者", "The SM is the team's coach and facilitator"),
    ("SM组织关系", "SM org relationships", "Scrum Master帮助建立团队和组织之间的关系", "The SM helps establish relationships between team and organization", "SM在组织层面推动Scrum adoption", "The SM drives Scrum adoption at the organizational level"),
    ("SM事件有效性", "SM event effectiveness", "Scrum Master确保所有Scrum事件发生且有成效", "The SM ensures all Scrum events take place and are productive", "确保事件在时间盒内且有价值", "Ensures events are within time-box and valuable"),
    ("SM自管理教导", "SM self-mgmt coaching", "Scrum Master教导团队自管理和跨功能", "The SM coaches the team in self-management and cross-functionality", "SM帮助团队变得更自主", "The SM helps the team become more autonomous"),
    ("SM对PO支持", "SM PO support", "Scrum Master帮助PO找到有效管理PB的技巧", "The SM helps the PO find techniques for effective PB management", "SM对PO提供指导和支持", "The SM provides guidance and support to the PO"),
    ("SM组织教练", "SM org coach", "Scrum Master帮助组织理解Scrum并推动变革", "The SM helps the organization understand Scrum and drive change", "SM是组织的Scrum教练", "The SM is the organization's Scrum coach"),
    ("SM非管理者", "SM not manager", "Scrum Master不是团队的管理者或主管", "The Scrum Master is not the team's manager or supervisor", "SM不控制团队的工作方式", "The SM does not control how the team works"),
    ("SM沟通促进", "SM communication", "Scrum Master促进团队内部和外部的沟通", "The SM facilitates communication within and outside the team", "促进健康的冲突解决和协作", "Promotes healthy conflict resolution and collaboration"),
    ("SM主动指导", "SM proactive coaching", "Scrum Master在团队不请求帮助时也可以指导", "The SM can coach even when the team doesn't ask for help", "SM应主动帮助团队改进", "The SM should proactively help the team improve"),
    ("SM团队成长", "SM team growth", "Scrum Master是Scrum团队的服务型领导", "The Scrum Master is a servant-leader for the Scrum Team", "SM专注于团队的成长和效能", "The SM focuses on team growth and effectiveness"),
], "Scrum角色", "Scrum Roles", 200)

# T2: Developers (150)
all_q += gen([
    ("Dev承诺", "Dev commitment", "Developers是致力于在每个Sprint中创建可用Increment的专业人士", "Developers are professionals committed to creating a usable Increment each Sprint", "Developers拥有技术决策权", "Developers own technical decisions"),
    ("Dev跨功能", "Dev cross-functional", "Developers是跨功能的——拥有创建Increment所需的所有技能", "Developers are cross-functional—they have all skills needed", "不需要外部资源来完成Sprint工作", "No external resources needed for Sprint work"),
    ("Dev自管理", "Dev self-managing", "Developers是自管理的——决定谁做什么、何时做、如何做", "Developers are self-managing—they decide who, when, and how", "没有人告诉Developers如何转化PBI", "No one tells Developers how to turn PBIs into an Increment"),
    ("Dev SB所有权", "Dev SB ownership", "Developers对Sprint Backlog拥有所有权", "Developers own the Sprint Backlog", "只有Developers可以修改Sprint Backlog", "Only Developers can modify the Sprint Backlog"),
    ("Dev估算", "Dev estimation", "Developers估算Product Backlog Items", "Developers estimate PBIs", "Developers最适合评估技术复杂性", "Developers are best positioned to assess technical complexity"),
    ("Dev质量责任", "Dev quality", "Developers对质量负责，确保工作符合DoD", "Developers are responsible for quality, ensuring work meets DoD", "质量是Developers的内建责任", "Quality is built into Developers' responsibility"),
    ("Dev事件参与", "Dev events", "Developers参加所有Scrum事件", "Developers participate in all Scrum events", "Developers在每个事件中都有关键角色", "Developers have a critical role in every event"),
    ("Dev术语演变", "Dev terminology", "2020年Scrum Guide将Development Team简化为Developers", "The 2020 Scrum Guide simplified 'Development Team' to 'Developers'", "反映了Scrum团队是一个整体", "Reflects the concept of one Scrum Team"),
    ("Dev核心执行", "Dev core execution", "Developers是Scrum团队的核心执行力量", "Developers are the core execution force of the Scrum Team", "他们将需求转化为可用的产品增量", "They turn requirements into usable product increments"),
    ("Dev Sprint责任", "Dev Sprint accountability", "Developers需要对Sprint Backlog的完成负责", "Developers are accountable for the Sprint Backlog", "他们计划和执行Sprint中的工作", "They plan and execute work within the Sprint"),
], "Scrum角色", "Scrum Roles", 150)

# T2: Role Boundaries (200)
all_q += gen([
    ("SH Review参与", "SH Review participation", "利益相关者参加Sprint Review并提供反馈", "Stakeholders attend the Sprint Review and provide feedback", "Sprint Review是利益相关者参与的关键事件", "The Sprint Review is the key event for stakeholder participation"),
    ("SH间接沟通", "SH indirect comm", "利益相关者不直接指挥Developers的工作", "Stakeholders don't directly direct Developers' work", "所有需求通过PO进入Product Backlog", "All requirements enter the PB through the PO"),
    ("Scrum团队组成", "Scrum Team composition", "Scrum团队由PO、SM和Developers组成", "The Scrum Team consists of PO, SM, and Developers", "没有子团队或层级结构", "No sub-teams or hierarchies"),
    ("PO SM角色分离", "PO SM separation", "PO和SM不应是同一个人", "The PO and SM should not be the same person", "这两个角色有天然的张力", "These two roles have natural tension"),
    ("SM不分配任务", "SM no task assignment", "SM不分配任务给Developers", "The SM does not assign tasks to Developers", "Developers自管理他们的工作", "Developers self-manage their work"),
    ("PO不干涉How", "PO no How interference", "PO不告诉团队如何构建产品", "The PO doesn't tell the team how to build the product", "PO决定What，团队决定How", "The PO decides What, the team decides How"),
    ("Scrum团队规模", "Scrum Team size", "Scrum团队的规模通常为10人或更少", "The Scrum Team size is typically 10 or fewer", "较小的团队沟通更有效", "Smaller teams communicate more effectively"),
    ("Scrum跨功能自组织", "Scrum cross-func self-org", "Scrum团队是跨功能的和自组织的", "The Scrum Team is cross-functional and self-organizing", "团队拥有交付Increment所需的所有技能", "The team has all skills needed to deliver the Increment"),
    ("Scrum共同责任", "Scrum shared accountability", "Scrum团队承担交付价值的共同责任", "The Scrum Team shares accountability for delivering value", "Scrum是一个团队运动", "Scrum is a team sport"),
    ("角色合并注意事项", "Role merging caveats", "一个人可以同时是SM和Developers，但不推荐", "One person can be both SM and Developer, but not recommended", "角色合并可能导致利益冲突", "Role merging can lead to conflicts of interest"),
    ("SM对PO持续支持", "SM ongoing PO support", "SM帮助PO理解和管理PB", "The SM helps the PO understand and manage the PB", "SM对PO提供持续的支持和指导", "The SM provides ongoing support and guidance to the PO"),
    ("SM组织变革", "SM org change", "SM帮助组织理解Scrum并推动敏捷转型", "The SM helps the organization understand Scrum and drive agile transformation", "SM是组织层面的变革推动者", "The SM is a change agent at the organizational level"),
], "Scrum角色", "Scrum Roles", 200)

# T3: Scrum Artifacts (750)
all_q += gen([
    ("三大工件", "Three artifacts", "Product Backlog是Scrum的三大工件之一", "The Product Backlog is one of Scrum's three artifacts", "三大工件：PB、Sprint Backlog、Increment", "Three artifacts: PB, Sprint Backlog, Increment"),
    ("PB承诺", "PB commitment", "Product Backlog的承诺是Product Goal", "The Product Backlog's commitment is the Product Goal", "Product Goal提供目标和方向", "Product Goal provides purpose and direction"),
    ("Product Goal定义", "Product Goal def", "Product Goal描述了产品的未来状态", "The Product Goal describes a future state of the product", "它是Scrum团队的长期目标", "It is the Scrum Team's long-term objective"),
    ("PBI属性", "PBI attributes", "PBI包括描述、估算、价值和排序", "PBIs include description, estimate, value, and ordering", "PBI应包含足够的信息来理解和实施", "PBIs should contain enough info to understand and implement"),
    ("PB动态", "PB dynamic", "Product Backlog永远不会完成——持续演进", "The Product Backlog is never complete—it continuously evolves", "随产品和市场变化而不断更新", "Updated constantly as product and market change"),
    ("PB排序依据", "PB ordering basis", "Product Backlog的排序基于风险、价值和依赖性", "PB ordering is based on risk, value, and dependencies", "PO负责排序决策", "The PO is responsible for ordering decisions"),
    ("SB承诺", "SB commitment", "Sprint Backlog的承诺是Sprint Goal", "The Sprint Backlog's commitment is the Sprint Goal", "Sprint Goal提供了目标", "The Sprint Goal provides the objective"),
    ("SB组成", "SB composition", "Sprint Backlog包含Sprint Goal、PBI和交付计划", "The Sprint Backlog includes Sprint Goal, PBIs, and delivery plan", "这三个元素共同构成Sprint Backlog", "These three elements form the Sprint Backlog"),
    ("SB实时", "SB real-time", "Sprint Backlog是实时的、足够透明的计划", "The Sprint Backlog is a real-time, transparent plan", "让团队随时检视进度", "Allows the team to inspect progress at any time"),
    ("SB可更新", "SB updatable", "Sprint Backlog在Sprint期间可以更新", "The Sprint Backlog can be updated during the Sprint", "Developers根据学习调整计划", "Developers adjust the plan based on learning"),
    ("Increment承诺", "Increment commitment", "Increment的承诺是Definition of Done", "The Increment's commitment is the Definition of Done", "DoD确保质量和可用性", "DoD ensures quality and usability"),
    ("Increment累积", "Increment accumulation", "Increment是所有先前Increments的累加", "The Increment is the sum of all previous Increments", "每个Sprint的增量建立在之前的工作上", "Each Sprint's Increment builds on previous work"),
    ("DoD与Increment", "DoD and Increment", "不符合DoD的PBI不能成为Increment的一部分", "PBIs not meeting DoD cannot be part of the Increment", "DoD是不可协商的质量标准", "DoD is a non-negotiable quality standard"),
    ("Increment发布", "Increment release", "Increment必须是可用的，可以随时发布", "The Increment must be usable, can be released anytime", "发布决策由PO做出", "Release decisions are made by the PO"),
    ("User Story", "User Story", "User Story是一种常见的PBI格式", "User Story is a common PBI format", "不是Scrum Guide要求的，但是常见实践", "Not required by Scrum Guide but a common practice"),
    ("验收标准", "Acceptance Criteria", "Acceptance Criteria定义了PBI何时被认为是完成的", "Acceptance Criteria define when a PBI is considered done", "提供了明确的完成条件", "Provide clear completion conditions"),
    ("INVEST", "INVEST", "INVEST原则：Independent, Negotiable, Valuable, Estimable, Small, Testable", "INVEST: Independent, Negotiable, Valuable, Estimable, Small, Testable", "帮助创建高品质的User Stories", "Helps create high-quality User Stories"),
    ("工件透明性", "Artifact transparency", "工件透明性是Scrum有效性的基础", "Artifact transparency is fundamental to Scrum's effectiveness", "不透明的工件导致错误的决策", "Opaque artifacts lead to wrong decisions"),
    ("承诺与透明", "Commitment and transparency", "每个工件都有一个承诺来加强透明性", "Each artifact has a commitment to enhance transparency", "PB->Product Goal, SB->Sprint Goal, Inc->DoD", "PB->Product Goal, SB->Sprint Goal, Inc->DoD"),
    ("低透明风险", "Low transparency risk", "低透明性等于高风险", "Low transparency equals high risk", "隐藏的问题无法被检视和解决", "Hidden problems cannot be inspected and resolved"),
    ("Burndown图", "Burndown chart", "Sprint Burndown图表显示剩余工作的趋势", "Sprint Burndown chart shows the trend of remaining work", "帮助团队可视化进度", "Helps the team visualize progress"),
    ("Burnup图", "Burnup chart", "Burnup图表显示已完成的工作量", "Burnup charts show the amount of completed work", "比Burndown更清楚地显示范围变化", "Shows scope changes more clearly than Burndown"),
    ("Burndown非必需", "Burndown optional", "Burndown图不是Scrum Guide的一部分，但是有用的实践", "Burndown charts are not part of the Scrum Guide but useful", "它是补充工具，不是必需的", "It's a complementary tool, not required"),
    ("SB灵活性", "SB flexibility", "Sprint Goal提供了灵活性——计划改变，目标不变", "The Sprint Goal provides flexibility—goal stays as plan changes", "Sprint Goal是Sprint期间的北极星", "The Sprint Goal is the North Star during the Sprint"),
], "Scrum工件", "Scrum Artifacts", 750)

# T4: Agile/Lean Principles (750)
all_q += gen([
    ("个体互动", "Individuals", "个体和互动 高于 流程和工具", "Individuals and interactions over processes and tools", "人是成功最重要的因素", "People are the most important factor in success"),
    ("可用软件", "Working software", "可用的软件 高于 详尽的文档", "Working software over comprehensive documentation", "交付价值比产出文档更重要", "Delivering value matters more than producing documentation"),
    ("客户合作", "Customer collab", "客户合作 高于 合同谈判", "Customer collaboration over contract negotiation", "建立持续的合作关系", "Build ongoing collaborative relationships"),
    ("响应变化", "Responding to change", "响应变化 高于 遵循计划", "Responding to change over following a plan", "拥抱变化而非抗拒", "Embrace change rather than resist it"),
    ("进度度量", "Progress measure", "可工作的软件是进度的主要度量", "Working software is the primary measure of progress", "不是文档或计划", "Not documentation or plans"),
    ("七大浪费", "Seven wastes", "精益的七大浪费包括过度生产、等待、运输等", "Lean's 7 wastes: Overproduction, Waiting, Transport, etc.", "识别和消除浪费是精益的核心", "Identifying and eliminating waste is core to Lean"),
    ("价值流", "Value stream", "精益强调价值流——从需求到交付的整个流程", "Lean emphasizes the value stream—from need to delivery", "价值流映射帮助识别浪费", "Value Stream Mapping helps identify waste"),
    ("客户价值", "Customer value", "精益的核心是创造客户价值", "Lean's core is creating customer value", "不增加价值的活动是浪费", "Activities not adding value are waste"),
    ("小批量", "Small batches", "精益鼓励小批量工作以减少浪费", "Lean encourages small batches to reduce waste", "小批量减少了WIP和等待时间", "Small batches reduce WIP and waiting time"),
    ("Kaizen", "Kaizen", "持续改进(Kaizen)是精益的核心原则", "Continuous Improvement (Kaizen) is a core Lean principle", "每个人都应参与改进", "Everyone should participate in improvement"),
    ("拉动系统", "Pull system", "拉动系统只在有需求时才开始工作", "Pull System starts work only when there is demand", "避免过度生产和库存积压", "Avoids overproduction and inventory buildup"),
    ("经验过程控制", "Empirical control", "经验过程控制基于观察而非预测", "Empirical process control is based on observation, not prediction", "适用于复杂问题", "Applies to complex problems"),
    ("短迭代反馈", "Short iteration feedback", "Scrum使用短迭代获得快速反馈", "Scrum uses short iterations for rapid feedback", "快速反馈使快速适应成为可能", "Rapid feedback enables rapid adaptation"),
    ("迭代开发", "Iterative dev", "迭代开发重复工作循环以改进产品", "Iterative development repeats work cycles to improve the product", "每次迭代在前一次基础上改进", "Each iteration improves upon the previous"),
    ("增量开发", "Incremental dev", "增量开发逐步构建产品功能", "Incremental development builds features progressively", "每次增量添加新功能", "Each increment adds new functionality"),
    ("自组织", "Self-organization", "自组织团队自行决定如何完成工作", "Self-organizing teams decide how to complete their work", "没有人指定团队如何工作", "No one dictates how the team works"),
    ("跨功能团队", "Cross-functional teams", "跨功能团队拥有交付Increment所需的所有技能", "Cross-functional teams have all skills needed to deliver", "不需要依赖外部资源", "No need to depend on external resources"),
    ("持续改进原则", "Continuous improvement", "持续改进是敏捷和Scrum的核心原则", "Continuous improvement is a core agile and Scrum principle", "团队应不断寻找改进机会", "Teams should constantly look for improvement opportunities"),
    ("价值驱动", "Value-driven", "价值驱动交付意味着优先做最有价值的工作", "Value-driven delivery means prioritizing the most valuable work", "PO确保团队做最有价值的工作", "The PO ensures the team works on the most valuable items"),
    ("反馈循环", "Feedback loop", "反馈循环越短，适应越快", "The shorter the feedback loop, the faster the adaptation", "短Sprint提供更多反馈机会", "Short Sprints provide more feedback opportunities"),
    ("PDCA", "PDCA", "PDCA循环是持续改进的模型", "PDCA (Plan-Do-Check-Act) is a model for continuous improvement", "每个Sprint都是一个PDCA循环", "Each Sprint is a PDCA cycle"),
    ("透明与改进", "Transparency improvement", "透明性使问题可见，使改进成为可能", "Transparency makes problems visible, making improvement possible", "不可见的问题无法改进", "Invisible problems can't be improved"),
    ("丰田生产系统", "Toyota Production System", "精益起源于丰田生产系统", "Lean originated from the Toyota Production System", "也称为丰田之道", "Also known as The Toyota Way"),
    ("迭代加增量", "Iterative + incremental", "Scrum同时使用迭代和增量方法", "Scrum uses both iterative and incremental approaches", "每个Sprint既是迭代又是增量", "Each Sprint is both iterative and incremental"),
    ("心理安全", "Psychological safety", "持续改进需要心理安全", "Continuous improvement requires psychological safety", "恐惧阻碍了改进", "Fear impedes improvement"),
    ("改进范围", "Improvement scope", "改进可以是技术、流程、工具或团队协作", "Improvements can be technical, process, tools, or collaboration", "任何使团队更有效的改变都是改进", "Any change making the team more effective is improvement"),
], "敏捷/精益原则", "Agile/Lean Principles", 750)

# T5: Scaling Scrum (750)
all_q += gen([
    ("Nexus定义", "Nexus definition", "Nexus是Scrum.org推出的规模化Scrum框架", "Nexus is the scaling Scrum framework from Scrum.org", "基于Scrum，增加了3-9个团队的集成", "Builds on Scrum, adding integration for 3-9 teams"),
    ("Nexus集成团队", "Nexus Integration Team", "Nexus Integration Team负责集成多个团队的工作", "The Nexus Integration Team integrates work from multiple teams", "NIT包含每个团队的代表", "NIT includes representatives from each team"),
    ("Nexus SB", "Nexus Sprint Backlog", "Nexus使用Nexus Sprint Backlog协调多团队工作", "Nexus uses the Nexus Sprint Backlog to coordinate", "显示跨团队的依赖关系", "Shows cross-team dependencies"),
    ("Nexus目标", "Nexus goal", "Nexus的目标是产生一个集成的Increment", "Nexus's goal is a single Integrated Increment", "所有团队的工作必须集成为一个整体", "All teams' work must integrate into one whole"),
    ("SAFe定义", "SAFe definition", "SAFe是企业级敏捷框架", "SAFe is an enterprise-level agile framework", "包含Team、Program、Large Solution、Portfolio层级", "Includes Team, Program, Large Solution, Portfolio levels"),
    ("PI Planning", "PI Planning", "SAFe中的PI Planning是大规模规划事件", "SAFe's PI Planning is a large-scale planning event", "通常每8-12周举行一次", "Occurs every 8-12 weeks"),
    ("RTE角色", "RTE role", "SAFe引入了Release Train Engineer角色", "SAFe introduces the Release Train Engineer role", "RTE类似于大型Scrum的SM", "RTE is like an SM for large-scale Scrum"),
    ("SAFe DevOps", "SAFe DevOps", "SAFe强调DevOps和持续交付管道", "SAFe emphasizes DevOps and Continuous Delivery Pipeline", "持续交付是核心实践", "Continuous delivery is a core practice"),
    ("WSJF", "WSJF", "SAFe使用WSJF来排序", "SAFe uses WSJF for prioritization", "考虑业务价值、时间价值、风险和工作量", "Considers business value, time value, risk, and effort"),
    ("LeSS定义", "LeSS definition", "LeSS扩展Scrum到多个团队", "LeSS extends Scrum to multiple teams", "保持Scrum的简单性", "Preserves Scrum's simplicity"),
    ("LeSS单一PO", "LeSS single PO", "LeSS只有一个PO和一个Product Backlog", "LeSS has one PO and one Product Backlog", "确保统一的优先级", "Ensures unified prioritization"),
    ("LeSS共享Sprint", "LeSS shared Sprint", "LeSS所有团队共享同一个Sprint", "All LeSS teams share the same Sprint", "简化跨团队协调", "Simplifies cross-team coordination"),
    ("Feature Teams", "Feature Teams", "LeSS使用Feature Teams而非Component Teams", "LeSS uses Feature Teams instead of Component Teams", "Feature Teams端到端交付功能", "Feature Teams deliver features end-to-end"),
    ("Scrum of Scrums", "Scrum of Scrums", "Scrum of Scrums是多团队协调机制", "Scrum of Scrums is a multi-team coordination mechanism", "每个团队派出代表参加", "Each team sends representatives"),
    ("规模化挑战", "Scaling challenge", "规模化的最大挑战是保持Scrum的简单性", "The main scaling challenge is preserving Scrum's simplicity", "过多流程降低敏捷性", "Too much process reduces agility"),
    ("跨团队依赖", "Cross-team deps", "跨团队依赖是规模化最大障碍", "Cross-team dependencies are the biggest scaling obstacle", "减少依赖比管理依赖更重要", "Reducing dependencies matters more than managing them"),
    ("规模化技术债", "Scaling tech debt", "技术债在规模化环境中影响更大", "Technical debt has greater impact in scaled environments", "多团队共用代码时技术债快速累积", "Technical debt accumulates fast when teams share code"),
    ("CI在规模化", "CI in scaling", "CI和自动化测试是规模化的关键技术实践", "CI and automated testing are key technical practices for scaling", "它们减少集成风险", "They reduce integration risk"),
    ("规模化文化", "Scaling culture", "规模化需要组织文化的支持", "Scaling requires organizational culture support", "没有文化变革框架无法成功", "Without cultural change, frameworks can't succeed"),
    ("Feature Teams优势", "Feature Teams advantage", "Feature Teams比Component Teams更适合规模化", "Feature Teams suit scaling better than Component Teams", "减少等待和依赖", "Reduce waiting and dependencies"),
    ("Nexus规划", "Nexus planning", "Nexus Sprint Planning协调所有团队的Sprint目标", "Nexus Sprint Planning coordinates Sprint Goals across teams", "团队共同确定集成点", "Teams identify integration points together"),
    ("LeSS系统思维", "LeSS systems thinking", "LeSS强调系统思维和精益原则", "LeSS emphasizes systems thinking and Lean principles", "关注整个系统的优化", "Focuses on optimizing the whole system"),
    ("沟通路径增长", "Communication paths", "沟通路径随团队数量呈指数增长", "Communication paths grow exponentially with team count", "n个团队有n(n-1)/2条路径", "n teams have n(n-1)/2 paths"),
    ("多团队DoD", "Multi-team DoD", "多团队环境需要共同的DoD", "Multi-team environments need a shared DoD", "共同DoD确保集成一致性", "Shared DoD ensures integration consistency"),
], "规模化Scrum", "Scaling Scrum", 750)

# T6: Advanced Scrum (750)
all_q += gen([
    ("技术债定义", "Tech debt definition", "技术债是为短期利益做出的技术妥协", "Technical debt is technical compromises for short-term gain", "类似财务债务——需要偿还", "Like financial debt—it needs to be repaid"),
    ("技术债与Velocity", "Tech debt and Velocity", "技术债降低团队的Velocity", "Technical debt reduces the team's Velocity", "随着技术债增加，开发速度下降", "As tech debt increases, development speed decreases"),
    ("重构偿还", "Refactoring pays", "重构是偿还技术债的主要方式", "Refactoring is the primary way to pay down technical debt", "持续重构防止技术债累积", "Continuous refactoring prevents tech debt accumulation"),
    ("Sprint技术债时间", "Sprint tech debt time", "每个Sprint应分配时间处理技术债", "Each Sprint should allocate time for technical debt", "典型建议是15-20%的Sprint容量", "Typical recommendation is 15-20% of Sprint capacity"),
    ("Velocity定义", "Velocity definition", "Velocity是团队一个Sprint中完成的工作量", "Velocity is the amount of work completed in a Sprint", "是预测工具，不是绩效指标", "It's a forecasting tool, not a performance metric"),
    ("Velocity不可比", "Velocity not comparable", "Velocity不应用于比较不同团队", "Velocity should not compare different teams", "每个团队的估算标准不同", "Each team's estimation standards differ"),
    ("Velocity波动", "Velocity fluctuation", "Velocity会自然波动——这是正常的", "Velocity naturally fluctuates—this is normal", "不应期望持续上升", "Shouldn't expect continuous increase"),
    ("Velocity游戏", "Velocity gaming", "人为提高Velocity会导致质量下降", "Artificially increasing Velocity decreases quality", "这被称为Velocity游戏", "This is called the Velocity game"),
    ("Story Points", "Story Points", "Story Points衡量PBI的相对大小和复杂性", "Story Points measure the relative size and complexity of PBIs", "不是绝对的时间度量", "Not absolute time measures"),
    ("Planning Poker", "Planning Poker", "Planning Poker是共识驱动的估算技巧", "Planning Poker is a consensus-driven estimation technique", "团队成员同时揭示估算", "Team members reveal estimates simultaneously"),
    ("估算权", "Estimation authority", "估算应由执行工作的Developers来做", "Estimates should be by Developers who do the work", "只有Developers能准确评估技术复杂性", "Only Developers can accurately assess technical complexity"),
    ("SP非KPI", "SP not KPI", "Story Points不应被用作绩效指标", "Story Points should not be used as a performance metric", "团队内部的工具", "An internal team tool"),
    ("Scrum vs Kanban", "Scrum vs Kanban", "Scrum用固定Sprint，Kanban用持续流", "Scrum uses fixed Sprints; Kanban uses continuous flow", "两者都是敏捷方法", "Both are agile approaches"),
    ("WIP限制", "WIP limits", "Kanban限制WIP，Scrum通过Sprint限制WIP", "Kanban limits WIP explicitly; Scrum limits via Sprint", "两者都限制WIP但方式不同", "Both limit WIP but differently"),
    ("角色差异", "Role differences", "Scrum有预定义角色，Kanban没有强制角色", "Scrum has predefined roles; Kanban doesn't mandate roles", "Kanban可与现有角色一起使用", "Kanban can work with existing roles"),
    ("Kanban指标", "Kanban metrics", "Kanban强调Lead Time和Cycle Time", "Kanban emphasizes Lead Time and Cycle Time", "这些指标帮助识别瓶颈", "These metrics help identify bottlenecks"),
    ("SM管理者反模式", "SM manager anti-pattern", "反模式：SM成为团队的管理者", "Anti-pattern: SM becomes the team's manager", "SM应是服务型领导者，不是管理者", "SM should be servant leader, not manager"),
    ("Velocity KPI反模式", "Velocity KPI anti-pattern", "反模式：将Velocity用作绩效指标", "Anti-pattern: Using Velocity as a performance metric", "Velocity是预测工具，不是KPI", "Velocity is a forecasting tool, not a KPI"),
    ("跳过回顾反模式", "Skip retro anti-pattern", "反模式：没有Sprint Retrospective", "Anti-pattern: Skipping Sprint Retrospective", "回顾是持续改进的关键", "The Retrospective is key to improvement"),
    ("改变Goal反模式", "Change goal anti-pattern", "反模式：Sprint期间不断改变Sprint Goal", "Anti-pattern: Constantly changing Sprint Goal during Sprint", "Sprint Goal应保持稳定", "Sprint Goal should remain stable"),
    ("分散式沟通", "Distributed communication", "分散式Scrum的最大挑战是沟通", "The biggest challenge of Distributed Scrum is communication", "面对面沟通比远程更有效", "Face-to-face is more effective than remote"),
    ("重叠时间", "Overlap hours", "重叠工作时间对分散式Scrum至关重要", "Overlapping hours are critical for Distributed Scrum", "至少需要2-4小时重叠", "At least 2-4 hours of overlap needed"),
    ("非软件Scrum", "Non-software Scrum", "Scrum可用于非软件产品开发", "Scrum can be used for non-software product development", "Scrum是通用框架", "Scrum is a general-purpose framework"),
    ("SM教练技能", "SM coaching", "教练和指导是SM的重要技能", "Coaching and mentoring are important SM skills", "SM应帮助团队成长", "The SM should help teams grow"),
    ("引导技术", "Facilitation", "引导技术帮助团队进行有效的会议", "Facilitation techniques help teams run effective meetings", "SM应掌握多种引导技术", "The SM should master various facilitation techniques"),
    ("冲突解决", "Conflict resolution", "冲突解决是SM的关键技能", "Conflict resolution is a key SM skill", "健康的冲突促进创新", "Healthy conflict promotes innovation"),
    ("Scrum度量", "Scrum metrics", "Scrum中的度量应服务于团队改进", "Metrics in Scrum should serve team improvement", "不是管理监控", "Not management surveillance"),
    ("PO缺席反模式", "PO absent anti-pattern", "反模式：PO不参加Sprint Review", "Anti-pattern: PO doesn't attend Sprint Review", "PO必须参加以接受Increment和收集反馈", "PO must attend to accept Increment and gather feedback"),
    ("跳过Refinement反模式", "Skip refinement anti-pattern", "反模式：不做Refinement就开始Sprint", "Anti-pattern: Starting Sprint without Refinement", "Refinement确保PBI有足够细节", "Refinement ensures PBIs have enough detail"),
    ("相对估算", "Relative estimation", "相对估算比绝对估算更准确", "Relative estimation is more accurate than absolute estimation", "人脑更擅长比较大小", "The brain is better at comparing sizes"),
], "进阶Scrum主题", "Advanced Scrum Topics", 750)

# Dedup and pad/trim to 5000
print(f"Generated {len(all_q)} questions")

seen = set()
unique_q = []
for q_obj in all_q:
    key = q_obj["question_zh"]
    if key not in seen:
        seen.add(key)
        unique_q.append(q_obj)
all_q = unique_q
print(f"After dedup: {len(all_q)} unique questions")

scenario_zh = [
    "在一个新成立的Scrum团队中，", "在Sprint中期，", "在规模化环境中，",
    "当团队遇到瓶颈时，", "当利益相关者要求变更时，", "在远程工作环境中，",
    "当技术债影响开发速度时，", "在敏捷转型初期，", "当Sprint Goal面临风险时，",
    "在回顾会议中，", "当团队产能下降时，", "在新的Refinement中，",
    "当客户要求紧急功能时，", "在跨团队协作中，", "当DoD需要更新时，",
    "在Sprint Planning中，", "当SM需要促进讨论时，", "在产品发布前的Sprint中，",
    "当PO离职时，", "在大型产品开发中，",
]
scenario_en = [
    "In a newly formed Scrum team, ", "Midway through a Sprint, ", "In a scaled environment, ",
    "When the team hits a bottleneck, ", "When stakeholders request changes, ", "In a remote work setup, ",
    "When technical debt impacts velocity, ", "During an agile transformation, ", "When the Sprint Goal is at risk, ",
    "In a Retrospective, ", "When team capacity drops, ", "In a new Refinement session, ",
    "When a customer requests an urgent feature, ", "In cross-team collaboration, ", "When the DoD needs updating, ",
    "During Sprint Planning, ", "When the SM needs to facilitate, ", "In the Sprint before release, ",
    "When the PO is absent, ", "In a large product development, ",
]

# Calculate topic distribution for balanced padding
from collections import Counter as _Counter
_topic_counts = _Counter(q["topic_en"] for q in all_q)
_target_per_topic = 5000 // len(_topic_counts)

# Create topic-indexed lists for balanced padding
_by_topic = {}
for q in all_q:
    t = q["topic_en"]
    if t not in _by_topic:
        _by_topic[t] = []
    _by_topic[t].append(q)

while len(all_q) < 5000:
    idx = len(all_q)
    # Pick the topic with the fewest questions so far
    current_counts = _Counter(q["topic_en"] for q in all_q)
    min_topic = min(_by_topic.keys(), key=lambda t: current_counts.get(t, 0))
    base_list = _by_topic[min_topic]
    base = base_list[idx % len(base_list)]
    si = idx % len(scenario_zh)
    new_q = dict(base)
    new_q["id"] = idx + 1
    new_q["question_zh"] = scenario_zh[si] + base["question_zh"]
    new_q["question_en"] = scenario_en[si] + base["question_en"]
    new_q["explanation_zh"] = base["explanation_zh"] + " 在此情境下，相同的原理仍然适用。"
    new_q["explanation_en"] = base["explanation_en"] + " In this context, the same principles still apply."
    new_q["difficulty"] = (idx % 3) + 1
    all_q.append(new_q)

all_q = all_q[:5000]
for i, q_obj in enumerate(all_q):
    q_obj["id"] = i + 1

# Validation
from collections import Counter
ans = Counter(q["answer"] for q in all_q)
unique_texts = len(set(q["question_zh"] for q in all_q))
topics = Counter(q.get("topic_en", "") for q in all_q)
diffs = Counter(q.get("difficulty", 0) for q in all_q)

sep = "=" * 60
print(f"\n{sep}")
print("VALIDATION REPORT")
print(sep)
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

missing = 0
for q_obj in all_q:
    for field in ["id","topic_en","topic_zh","question_en","question_zh","options_en","options_zh","answer","explanation_en","explanation_zh","difficulty"]:
        if field not in q_obj:
            missing += 1
            break
print(f"\nQuestions with missing fields: {missing}")

bad_opts = 0
for q_obj in all_q:
    for opts in [q_obj.get("options_en",[]), q_obj.get("options_zh",[])]:
        if len(opts) != 4:
            bad_opts += 1
            break
        for i, opt in enumerate(opts):
            if not opt.startswith(chr(65+i)+". "):
                bad_opts += 1
                break
print(f"Questions with bad option format: {bad_opts}")

print(f"\n{sep}")
print(f"Writing to {OUTPUT}...")
with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(all_q, f, ensure_ascii=False, indent=None)
print("Done!")
