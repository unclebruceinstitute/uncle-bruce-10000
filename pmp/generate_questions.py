#!/usr/bin/env python3
"""
PMP Exam Question Generator - 10,000 Questions
Covers PMP ECO: People (4200), Process (5000), Business Environment (800)
Aligned with PMBOK 7th Edition
"""
import json
import random
import os

random.seed(42)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# TOPIC DEFINITIONS
# ============================================================

PEOPLE_TOPICS = [
    {"id": "P01", "en": "Team Management", "zh": "团队管理",
     "scenarios": [
         "A newly formed project team is struggling with role clarity after a rapid onboarding process.",
         "Your team has members in three different time zones, causing coordination issues.",
         "Two senior team members disagree on the technical approach for a critical deliverable.",
         "A high-performing team member is showing signs of burnout after three consecutive sprints.",
         "The project sponsor wants to add a team member mid-sprint, disrupting team velocity.",
         "Your self-organizing team is avoiding accountability for sprint commitments.",
         "A remote team member feels excluded from key decisions made during in-person meetings.",
         "Team morale is low after a major scope change was imposed without consultation.",
         "You notice a team member is consistently working overtime to meet deadlines.",
         "The team is transitioning from a predictive to an agile approach and struggling with ceremonies.",
         "A team member from a different department is not fully committed to the project.",
         "Your cross-functional team lacks a shared understanding of the project goals.",
         "The team's performance metrics show declining velocity over the past four sprints.",
         "A new team leader is struggling to establish authority with experienced team members.",
         "Cultural differences between team members are causing misunderstandings in daily standups.",
     ]},
    {"id": "P02", "en": "Conflict Resolution", "zh": "冲突解决",
     "scenarios": [
         "Two team leads have fundamentally different views on the architecture design.",
         "A stakeholder is demanding features that conflict with the product owner's priorities.",
         "The development team and QA team blame each other for a production defect.",
         "A vendor's deliverable does not meet the acceptance criteria, causing a dispute.",
         "Team members disagree on whether to use a predictive or agile approach for a sub-project.",
         "A conflict arises between the project manager and a functional manager over resource allocation.",
         "The client and the project team have different interpretations of the requirements.",
         "A team member publicly criticizes a colleague's work during a sprint review.",
         "There is tension between the old guard and new hires regarding coding standards.",
         "The project sponsor and the product owner disagree on the minimum viable product definition.",
     ]},
    {"id": "P03", "en": "Leadership Styles", "zh": "领导风格",
     "scenarios": [
         "You are leading a team of experienced professionals who prefer autonomy.",
         "The organization is going through a major transformation and teams feel uncertain.",
         "Your team needs to deliver a critical milestone under extreme time pressure.",
         "A new strategic direction requires the team to pivot their approach completely.",
         "You are managing a team that is resistant to adopting agile practices.",
         "The project is in crisis mode due to a major technical failure.",
         "Your team is highly skilled but lacks motivation after repeated project cancellations.",
         "You need to build consensus among diverse stakeholders for a controversial decision.",
         "A servant leadership approach is needed to empower a self-organizing team.",
         "The organization values innovation, and you need to foster a creative environment.",
     ]},
    {"id": "P04", "en": "Stakeholder Engagement", "zh": "干系人参与",
     "scenarios": [
         "A key stakeholder is resistant to the proposed change and may sabotage the project.",
         "You discover a previously unidentified stakeholder with significant influence.",
         "The executive sponsor is disengaged and rarely available for decision-making.",
         "Multiple stakeholders have conflicting expectations about the project outcome.",
         "A regulatory body has become a stakeholder due to compliance requirements.",
         "End users are not being adequately represented in the requirements gathering process.",
         "A stakeholder with high power but low interest needs to be kept informed.",
         "The project affects multiple departments, each with different priorities.",
         "A stakeholder is requesting changes that would significantly increase the project scope.",
         "You need to manage stakeholder expectations after a schedule delay.",
     ]},
    {"id": "P05", "en": "Mentoring and Coaching", "zh": "指导与教练",
     "scenarios": [
         "A junior team member is struggling with estimating story points accurately.",
         "You want to develop a team member's leadership skills for future project roles.",
         "A technically skilled developer lacks soft skills for stakeholder communication.",
         "The organization is implementing a mentoring program for new project managers.",
         "A team member wants to transition from a technical to a management role.",
         "You are coaching a product owner who is new to agile methodologies.",
         "A team member is not receptive to feedback and resists personal development.",
         "You need to mentor a distributed team on effective remote collaboration.",
         "A high-potential employee is at risk of leaving due to lack of growth opportunities.",
         "You are building a knowledge-sharing culture within the project team.",
     ]},
    {"id": "P06", "en": "Team Building and Collaboration", "zh": "团队建设与协作",
     "scenarios": [
         "A virtual team needs to build trust and rapport across different cultures.",
         "After a team conflict, relationships need to be repaired for effective collaboration.",
         "You are forming a new agile team and need to establish working agreements.",
         "Siloed departments need to collaborate on an integrated product delivery.",
         "The team is transitioning to a collocated workspace for the first time.",
         "A merger has combined two teams with different working cultures.",
         "You need to foster collaboration between the project team and external vendors.",
         "The team lacks psychological safety, and members are afraid to raise concerns.",
         "Cross-functional team members don't understand each other's domains.",
         "You want to implement pair programming to improve knowledge sharing.",
     ]},
    {"id": "P07", "en": "Communication Management", "zh": "沟通管理",
     "scenarios": [
         "Stakeholders complain they are receiving too many project updates.",
         "Critical project information is not reaching remote team members effectively.",
         "The project status report is being interpreted differently by different audiences.",
         "A language barrier is causing misunderstandings in a multicultural team.",
         "The project uses multiple communication tools, causing information fragmentation.",
         "You need to communicate a significant project setback to the executive sponsor.",
         "The team is not effectively using the daily standup for synchronization.",
         "Stakeholders need different levels of detail in project communications.",
         "A communication breakdown between the project team and the vendor caused a delay.",
         "You need to establish a communication plan for a large, complex program.",
     ]},
    {"id": "P08", "en": "Emotional Intelligence", "zh": "情商",
     "scenarios": [
         "A team member is going through personal difficulties affecting their work.",
         "You notice tension between two team members during a retrospective.",
         "A stakeholder is expressing frustration about the project's pace.",
         "Your own stress levels are affecting your decision-making ability.",
         "A team member takes constructive criticism personally and becomes defensive.",
         "The team is demoralized after a failed sprint goal.",
         "You need to deliver bad news about a project delay to the sponsor.",
         "Cultural differences affect how team members express disagreement.",
         "A team member is not comfortable speaking up in group settings.",
         "You need to manage your emotions when a stakeholder makes unreasonable demands.",
     ]},
    {"id": "P09", "en": "Negotiation Skills", "zh": "谈判技巧",
     "scenarios": [
         "You need to negotiate additional budget for an unforeseen technical challenge.",
         "A key resource is being pulled to another project by their functional manager.",
         "The client wants to reduce the project timeline without adjusting scope.",
         "You are negotiating the terms of a contract with a critical vendor.",
         "The product owner and stakeholders disagree on feature priority.",
         "You need to negotiate a realistic deadline with the project sponsor.",
         "A team member wants a role change that would affect the project plan.",
         "You are negotiating scope creep with a demanding client.",
         "The organization wants to cut project costs by 20% mid-project.",
         "You need to negotiate shared resources between multiple projects.",
     ]},
    {"id": "P10", "en": "Performance Management", "zh": "绩效管理",
     "scenarios": [
         "A team member's performance has declined significantly over the past month.",
         "You need to conduct a performance review for a remote team member.",
         "The team's velocity has dropped, and you need to identify the root cause.",
         "A team member consistently misses deadlines but produces high-quality work.",
         "You need to set performance expectations for a newly formed team.",
         "The organization is implementing OKRs and the team needs alignment.",
         "A high performer is not being recognized, causing resentment in the team.",
         "You need to address a team member's poor communication skills.",
         "The project metrics show the team is not meeting its quality targets.",
         "You need to balance individual performance with team performance metrics.",
     ]},
    {"id": "P11", "en": "Motivation and Engagement", "zh": "激励与参与",
     "scenarios": [
         "Team members are disengaged after working on maintenance tasks for months.",
         "You want to implement intrinsic motivation strategies for a creative team.",
         "The team lost motivation after a major project failure.",
         "A team member feels their contributions are not valued by the organization.",
         "You need to keep the team motivated during a long, challenging project.",
         "The organization's reward system does not align with agile team values.",
         "Remote team members feel isolated and disconnected from the team.",
         "The team is motivated but lacks clear direction from leadership.",
         "You want to celebrate small wins to maintain team momentum.",
         "A team member is motivated by learning opportunities rather than monetary rewards.",
     ]},
    {"id": "P12", "en": "Accountability and Responsibility", "zh": "问责与责任",
     "scenarios": [
         "Team members are unclear about their individual responsibilities for deliverables.",
         "A team member blames others for missing their own commitments.",
         "The team lacks accountability for sprint goals and consistently overcommits.",
         "You need to establish a RACI matrix for a complex, multi-team project.",
         "A stakeholder is not fulfilling their agreed-upon responsibilities.",
         "The project manager is being held accountable for issues outside their control.",
         "Team members are not taking ownership of quality in their deliverables.",
         "A shared responsibility model is needed for a DevOps transformation.",
         "You need to clarify accountability between the project team and the PMO.",
         "The Definition of Done is not being consistently applied across the team.",
     ]},
]

PROCESS_TOPICS = [
    {"id": "PR01", "en": "Scope Management", "zh": "范围管理",
     "scenarios": [
         "The project scope is continuously expanding due to stakeholder requests.",
         "The work breakdown structure is missing key deliverables.",
         "Requirements are ambiguous, leading to different interpretations.",
         "A change request would significantly alter the project scope baseline.",
         "The product backlog is not properly refined, causing sprint planning issues.",
         "Scope verification reveals that deliverables don't meet acceptance criteria.",
         "The project charter defines scope too broadly for effective planning.",
         "Gold plating is occurring as team members add unnecessary features.",
         "The scope management plan doesn't account for agile iterative delivery.",
         "A key requirement was missed during the initial requirements gathering.",
     ]},
    {"id": "PR02", "en": "Schedule Management", "zh": "进度管理",
     "scenarios": [
         "The critical path has shifted due to a delayed predecessor activity.",
         "The project is behind schedule and the sponsor wants a recovery plan.",
         "Resource constraints are causing schedule compression needs.",
         "A fast-tracking approach is being considered to meet the deadline.",
         "The team's velocity is inconsistent, making sprint planning unreliable.",
         "Dependencies with an external vendor are causing schedule uncertainty.",
         "The schedule baseline needs to be revised after a major scope change.",
         "Lead and lag times in the schedule are causing resource conflicts.",
         "The project uses agile release planning and needs to forecast completion.",
         "A milestone is at risk due to underestimated activity durations.",
     ]},
    {"id": "PR03", "en": "Cost Management", "zh": "成本管理",
     "scenarios": [
         "The project is over budget, and earned value metrics show a negative trend.",
         "A vendor's costs have increased significantly beyond the original estimate.",
         "The cost baseline needs to be revised due to approved change requests.",
         "The team is struggling to estimate costs for a novel technology project.",
         "Reserve analysis shows that contingency reserves are being depleted rapidly.",
         "The project sponsor wants to reduce costs without affecting scope or schedule.",
         "Earned value analysis reveals CPI of 0.85 and SPI of 0.90.",
         "Life cycle costing needs to be considered for a long-term product.",
         "The cost management plan doesn't account for agile team-based costing.",
         "A make-or-buy analysis is needed for a key project component.",
     ]},
    {"id": "PR04", "en": "Quality Management", "zh": "质量管理",
     "scenarios": [
         "Defect rates have increased significantly in recent sprints.",
         "The Definition of Done needs to be updated to include new quality standards.",
         "A quality audit reveals non-compliance with organizational processes.",
         "The team needs to implement continuous integration for better quality.",
         "Customer satisfaction scores are declining despite meeting specifications.",
         "A root cause analysis is needed for recurring quality issues.",
         "The project needs to balance quality with schedule and cost constraints.",
         "Acceptance testing reveals significant gaps in deliverable quality.",
         "The team is not effectively using retrospectives for process improvement.",
         "Quality metrics need to be defined for a new agile project.",
     ]},
    {"id": "PR05", "en": "Risk Management", "zh": "风险管理",
     "scenarios": [
         "A previously identified risk has materialized, impacting the project.",
         "The risk register has not been updated since the project planning phase.",
         "A new regulatory requirement introduces significant project risk.",
         "The team needs to perform quantitative risk analysis for key uncertainties.",
         "Risk responses are not being effectively implemented by the team.",
         "A vendor's financial instability poses a supply chain risk.",
         "The project has a high number of identified risks with low probability.",
         "An unknown unknown has occurred, requiring emergency response planning.",
         "Risk management in an agile context needs a different approach.",
         "The Monte Carlo simulation shows a 30% chance of missing the deadline.",
     ]},
    {"id": "PR06", "en": "Procurement Management", "zh": "采购管理",
     "scenarios": [
         "A vendor is not meeting the performance standards in the contract.",
         "The project needs to select a vendor for a critical component.",
         "Contract disputes are arising due to ambiguous terms and conditions.",
         "A change in project scope requires contract modifications.",
         "The procurement process is taking longer than expected, delaying the project.",
         "An agile project needs to engage external vendors iteratively.",
         "The make-or-buy analysis suggests outsourcing a key deliverable.",
         "A vendor claims additional compensation for work they consider out of scope.",
         "The project needs to ensure vendor compliance with security requirements.",
         "Procurement closeout activities need to be planned for project completion.",
     ]},
    {"id": "PR07", "en": "Integration Management", "zh": "整合管理",
     "scenarios": [
         "Multiple change requests need to be evaluated and prioritized.",
         "The project management plan needs to be updated after a major change.",
         "Knowledge management across project phases is insufficient.",
         "The project needs to be integrated with other organizational initiatives.",
         "Lessons learned from a previous phase need to be applied to the current phase.",
         "The project charter needs to be developed for a new initiative.",
         "Configuration management is not being consistently applied.",
         "The project closure process needs to capture organizational process assets.",
         "Benefits realization planning needs to be integrated into the project.",
         "A hybrid approach needs to integrate predictive and agile elements.",
     ]},
    {"id": "PR08", "en": "Agile and Hybrid Approaches", "zh": "敏捷与混合方法",
     "scenarios": [
         "The organization is transitioning from predictive to agile project management.",
         "A hybrid approach is needed for a project with both hardware and software components.",
         "The team is struggling with sprint planning and backlog prioritization.",
         "Agile metrics need to be defined to measure team performance.",
         "The project uses Scrum but needs to incorporate Kanban for maintenance work.",
         "Scaling agile across multiple teams is presenting coordination challenges.",
         "The product owner is not effectively managing the product backlog.",
         "The team needs to implement continuous delivery practices.",
         "Agile ceremonies are not providing value and need to be adapted.",
         "The project needs to balance agile flexibility with predictive governance.",
     ]},
    {"id": "PR09", "en": "Resource Management", "zh": "资源管理",
     "scenarios": [
         "Key resources are shared across multiple projects, causing availability issues.",
         "The team needs training on a new technology for the project.",
         "Resource leveling is needed to resolve overallocation issues.",
         "A critical team member is leaving the organization mid-project.",
         "The resource management plan needs to account for agile team structures.",
         "Virtual team members need effective tools and processes for collaboration.",
         "The project needs specialized resources that are scarce in the organization.",
         "Team development activities need to be planned for a new team.",
         "Resource calendars need to be updated after a project schedule change.",
         "The project needs to manage physical resources in addition to human resources.",
     ]},
    {"id": "PR10", "en": "Communications Management", "zh": "沟通管理",
     "scenarios": [
         "The communication management plan needs to be updated for a hybrid project.",
         "Information distribution is not reaching all relevant stakeholders.",
         "The project needs to implement a new collaboration tool for the team.",
         "Reporting requirements vary significantly among different stakeholder groups.",
         "The team needs to establish effective communication for a distributed project.",
         "Project performance reports need to be standardized across the program.",
         "Communication breakdowns are causing rework and misunderstandings.",
         "The project needs to manage communications during a crisis situation.",
         "Agile information radiators need to be implemented for transparency.",
         "The communication plan needs to address both internal and external audiences.",
     ]},
    {"id": "PR11", "en": "Stakeholder Management", "zh": "干系人管理",
     "scenarios": [
         "The stakeholder register needs to be updated after organizational changes.",
         "A stakeholder's influence has increased significantly during the project.",
         "The stakeholder engagement plan needs to be revised for the current phase.",
         "Multiple stakeholders have conflicting requirements and expectations.",
         "The project needs to identify and engage new stakeholders.",
         "Stakeholder satisfaction metrics show declining support for the project.",
         "The project needs to manage stakeholder resistance to change.",
         "A key stakeholder is not available for required decision-making.",
         "The stakeholder engagement assessment matrix needs to be updated.",
         "The project needs to balance stakeholder interests with project objectives.",
     ]},
    {"id": "PR12", "en": "Project Governance", "zh": "项目治理",
     "scenarios": [
         "The project needs to establish a governance framework for decision-making.",
         "A steering committee needs to be formed for a strategic project.",
         "The project needs to align with organizational governance requirements.",
         "Decision-making authority needs to be clearly defined for the project.",
         "The project needs to implement stage-gate reviews for quality control.",
         "Escalation procedures need to be established for project issues.",
         "The project needs to ensure compliance with organizational policies.",
         "Governance structures need to be adapted for an agile project.",
         "The project needs to establish a change control board.",
         "Project performance needs to be reported to the governance board.",
     ]},
    {"id": "PR13", "en": "Project Planning", "zh": "项目规划",
     "scenarios": [
         "The project management plan needs to be developed for a complex initiative.",
         "Planning activities need to be iterative for an agile project.",
         "The project needs to develop a comprehensive work breakdown structure.",
         "Activity sequencing needs to account for complex dependencies.",
         "The project needs to develop realistic duration and cost estimates.",
         "The schedule development process needs to consider resource constraints.",
         "The project needs to develop a risk management plan.",
         "The planning process needs to be tailored for a hybrid approach.",
         "The project needs to develop a quality management plan.",
         "The project needs to plan for procurement and vendor management.",
     ]},
    {"id": "PR14", "en": "Project Execution", "zh": "项目执行",
     "scenarios": [
         "The project team needs guidance on executing the project management plan.",
         "Quality assurance activities need to be implemented during execution.",
         "The project needs to manage team development during execution.",
         "Vendor management activities need to be performed during execution.",
         "The project needs to implement the approved changes during execution.",
         "The team needs to manage stakeholder engagement during execution.",
         "The project needs to distribute information as planned.",
         "The project needs to manage resources effectively during execution.",
         "The project needs to implement risk responses during execution.",
         "The project needs to manage procurement activities during execution.",
     ]},
    {"id": "PR15", "en": "Monitoring and Controlling", "zh": "监控与控制",
     "scenarios": [
         "The project needs to monitor and control project work effectively.",
         "Integrated change control needs to be implemented for the project.",
         "The project needs to validate and control scope changes.",
         "The project needs to control the schedule and manage changes.",
         "The project needs to control costs and manage the budget.",
         "The project needs to monitor and control quality.",
         "The project needs to monitor and control risks.",
         "The project needs to control procurements and vendor performance.",
         "The project needs to monitor stakeholder engagement.",
         "The project needs to report performance to stakeholders.",
     ]},
    {"id": "PR16", "en": "Project Closure", "zh": "项目收尾",
     "scenarios": [
         "The project needs to be formally closed after deliverable acceptance.",
         "Lessons learned need to be captured and documented for future projects.",
         "The project needs to release resources and close procurements.",
         "Benefits realization needs to be tracked after project closure.",
         "The project needs to archive project documents and records.",
         "The project needs to obtain formal acceptance from stakeholders.",
         "The project needs to close out contracts with vendors.",
         "The project needs to update organizational process assets.",
         "The project needs to conduct a post-project review.",
         "The project needs to transition deliverables to operations.",
     ]},
    {"id": "PR17", "en": "Tailoring and Adaptation", "zh": "裁剪与适应",
     "scenarios": [
         "The project needs to tailor the approach based on project characteristics.",
         "The team needs to adapt processes for a new project context.",
         "The project needs to select the appropriate life cycle for the project.",
         "The team needs to adapt agile practices for the organization's culture.",
         "The project needs to tailor governance requirements for the project size.",
         "The team needs to adapt communication practices for the project.",
         "The project needs to tailor the risk management approach.",
         "The team needs to adapt quality processes for the project context.",
         "The project needs to tailor the stakeholder engagement approach.",
         "The team needs to adapt the project management approach as the project evolves.",
     ]},
    {"id": "PR18", "en": "Value Delivery", "zh": "价值交付",
     "scenarios": [
         "The project needs to ensure that deliverables provide value to the organization.",
         "The team needs to focus on delivering value incrementally.",
         "The project needs to measure and communicate the value delivered.",
         "The team needs to prioritize work based on value delivery.",
         "The project needs to align value delivery with organizational strategy.",
         "The team needs to ensure that the project delivers the expected benefits.",
         "The project needs to measure customer value and satisfaction.",
         "The team needs to optimize value delivery within constraints.",
         "The project needs to ensure that value is delivered throughout the life cycle.",
         "The team needs to adapt the approach to maximize value delivery.",
     ]},
    {"id": "PR19", "en": "Project Complexity", "zh": "项目复杂性",
     "scenarios": [
         "The project has high complexity due to multiple interdependencies.",
         "The team needs to manage complexity in a large-scale project.",
         "The project needs to address complexity arising from new technology.",
         "The team needs to manage complexity in a multi-vendor environment.",
         "The project needs to address organizational complexity.",
         "The team needs to manage complexity in a global project.",
         "The project needs to address technical complexity.",
         "The team needs to manage complexity in an agile-at-scale environment.",
         "The project needs to address complexity from regulatory requirements.",
         "The team needs to manage complexity in a hybrid project approach.",
     ]},
    {"id": "PR20", "en": "Project Compliance", "zh": "项目合规",
     "scenarios": [
         "The project needs to ensure compliance with industry regulations.",
         "The team needs to implement compliance monitoring processes.",
         "The project needs to address compliance with organizational policies.",
         "The team needs to manage compliance with contractual requirements.",
         "The project needs to ensure compliance with data protection regulations.",
         "The team needs to address compliance with environmental regulations.",
         "The project needs to manage compliance with safety standards.",
         "The team needs to ensure compliance with quality standards.",
         "The project needs to address compliance with financial regulations.",
         "The team needs to manage compliance with labor regulations.",
     ]},
]

BUSINESS_TOPICS = [
    {"id": "B01", "en": "Organizational Strategy", "zh": "组织战略",
     "scenarios": [
         "The project needs to align with the organization's strategic objectives.",
         "A new strategic direction requires the project to pivot.",
         "The project needs to demonstrate alignment with business goals.",
         "The organization is evaluating whether the project still supports strategy.",
         "The project needs to adapt to a change in organizational strategy.",
         "The team needs to understand how the project fits into the portfolio.",
         "The project needs to support the organization's digital transformation.",
         "Strategic alignment needs to be assessed for project prioritization.",
         "The project needs to contribute to the organization's competitive advantage.",
         "The team needs to understand the business context for the project.",
     ]},
    {"id": "B02", "en": "Benefits Realization", "zh": "收益实现",
     "scenarios": [
         "The project needs to define and track benefits realization metrics.",
         "The team needs to ensure that the project delivers the expected benefits.",
         "Benefits realization planning needs to be integrated into the project.",
         "The project needs to measure the actual benefits against the planned benefits.",
         "The team needs to communicate the benefits delivered to stakeholders.",
         "The project needs to establish a benefits sustainment plan.",
         "Benefits realization needs to be tracked after project closure.",
         "The team needs to identify and manage benefits-related risks.",
         "The project needs to align benefits with organizational objectives.",
         "The team needs to ensure that benefits are measurable and achievable.",
     ]},
    {"id": "B03", "en": "Change Management", "zh": "变更管理",
     "scenarios": [
         "The project is implementing a significant organizational change.",
         "The team needs to manage resistance to change from stakeholders.",
         "The project needs to develop a change management plan.",
         "The team needs to assess the impact of change on the organization.",
         "The project needs to communicate the change effectively to stakeholders.",
         "The team needs to support stakeholders through the change transition.",
         "The project needs to measure the effectiveness of change management.",
         "The team needs to identify and manage change-related risks.",
         "The project needs to align change management with project management.",
         "The team needs to ensure that changes are sustained after implementation.",
     ]},
    {"id": "B04", "en": "Compliance and Governance", "zh": "合规与治理",
     "scenarios": [
         "The project needs to ensure compliance with new regulatory requirements.",
         "The team needs to implement governance structures for the project.",
         "The project needs to address compliance with industry standards.",
         "The team needs to manage compliance with organizational policies.",
         "The project needs to ensure compliance with data privacy regulations.",
         "The team needs to address compliance with contractual obligations.",
         "The project needs to manage compliance with environmental regulations.",
         "The team needs to ensure compliance with safety and health regulations.",
         "The project needs to address compliance with financial regulations.",
         "The team needs to manage compliance with procurement regulations.",
     ]},
    {"id": "B05", "en": "Business Environment Analysis", "zh": "商业环境分析",
     "scenarios": [
         "The project needs to assess the impact of market changes.",
         "The team needs to analyze the competitive landscape for the project.",
         "The project needs to address economic factors affecting the business case.",
         "The team needs to assess the impact of technological changes.",
         "The project needs to analyze the political and legal environment.",
         "The team needs to assess the impact of social and cultural factors.",
         "The project needs to analyze the environmental and sustainability factors.",
         "The team needs to assess the impact of industry trends.",
         "The project needs to analyze the organizational culture and readiness.",
         "The team needs to assess the impact of external dependencies.",
     ]},
    {"id": "B06", "en": "Project Selection and Prioritization", "zh": "项目选择与优先级",
     "scenarios": [
         "The organization needs to select projects that align with strategy.",
         "The team needs to prioritize projects based on value and risk.",
         "The project needs to demonstrate its business case for approval.",
         "The team needs to assess project feasibility and viability.",
         "The project needs to be prioritized within the portfolio.",
         "The team needs to evaluate project proposals using selection criteria.",
         "The project needs to demonstrate return on investment.",
         "The team needs to assess the project's alignment with organizational goals.",
         "The project needs to be evaluated for resource requirements.",
         "The team needs to prioritize projects based on urgency and importance.",
     ]},
    {"id": "B07", "en": "Organizational Change and Culture", "zh": "组织变革与文化",
     "scenarios": [
         "The project is driving organizational culture change.",
         "The team needs to assess organizational readiness for change.",
         "The project needs to align with the organizational culture.",
         "The team needs to manage cultural differences in a global project.",
         "The project needs to support the organization's transformation initiative.",
         "The team needs to address resistance to cultural change.",
         "The project needs to assess the impact of culture on project success.",
         "The team needs to develop strategies for culture change management.",
         "The project needs to align with the organization's values and norms.",
         "The team needs to manage the impact of organizational restructuring.",
     ]},
    {"id": "B08", "en": "Market and Customer Focus", "zh": "市场与客户关注",
     "scenarios": [
         "The project needs to focus on customer needs and expectations.",
         "The team needs to analyze market trends for the project.",
         "The project needs to assess customer satisfaction and feedback.",
         "The team needs to manage customer relationships during the project.",
         "The project needs to align with market demands and opportunities.",
         "The team needs to assess the competitive landscape.",
         "The project needs to focus on delivering customer value.",
         "The team needs to manage customer expectations effectively.",
         "The project needs to assess the impact of market changes.",
         "The team needs to ensure that the project meets customer requirements.",
     ]},
]

# ============================================================
# QUESTION TEMPLATES
# ============================================================

def make_question_templates():
    """Return a list of (question_en, question_zh, [options_en], [options_zh], answer_idx, explanation_en, explanation_zh) templates."""
    templates = []

    # Template type 1: "What should the project manager do FIRST?"
    def first_action(q_en, q_zh, opts_en, opts_zh, ans, exp_en, exp_zh):
        return (q_en, q_zh, opts_en, opts_zh, ans, exp_en, exp_zh)

    # We'll generate questions dynamically based on scenarios
    return templates

# ============================================================
# QUESTION GENERATION ENGINE
# ============================================================

QUESTION_TYPES = [
    "first_action",
    "best_approach",
    "tool_technique",
    "agile_role",
    "predictive_process",
    "hybrid_scenario",
    "ethical_scenario",
    "stakeholder_engagement",
    "risk_response",
    "conflict_resolution",
]

def generate_question_options_and_explanation(scenario, topic_id, topic_en, topic_zh, domain, q_type, difficulty):
    """Generate a complete question with options and explanation based on scenario and type."""

    # Question patterns by type
    patterns = {
        "first_action": {
            "en": [
                f"In this scenario, what should the project manager do FIRST?",
                f"What is the FIRST action the project manager should take?",
                f"What should the project manager do IMMEDIATELY?",
                f"What is the MOST appropriate first step?",
            ],
            "zh": [
                f"在这种情况下，项目经理应该首先做什么？",
                f"项目经理应该采取的第一个行动是什么？",
                f"项目经理应该立即做什么？",
                f"最合适的第一步是什么？",
            ],
        },
        "best_approach": {
            "en": [
                f"What is the BEST approach for the project manager in this situation?",
                f"Which approach should the project manager adopt?",
                f"What is the MOST effective way to handle this situation?",
                f"Which course of action is MOST appropriate?",
            ],
            "zh": [
                f"在这种情况下，项目经理的最佳方法是什么？",
                f"项目经理应该采用哪种方法？",
                f"处理这种情况最有效的方式是什么？",
                f"最合适的行动方案是什么？",
            ],
        },
        "tool_technique": {
            "en": [
                f"Which tool or technique is MOST appropriate for this situation?",
                f"What tool should the project manager use?",
                f"Which technique would be MOST effective here?",
                f"What is the BEST tool or technique to apply?",
            ],
            "zh": [
                f"哪种工具或技术最适合这种情况？",
                f"项目经理应该使用什么工具？",
                f"哪种技术在这里最有效？",
                f"最好应用什么工具或技术？",
            ],
        },
        "agile_role": {
            "en": [
                f"In an agile context, who should be responsible for addressing this?",
                f"Which agile role should handle this situation?",
                f"According to agile practices, who should take the lead?",
                f"Which team member should address this in an agile environment?",
            ],
            "zh": [
                f"在敏捷环境中，谁应该负责处理这个问题？",
                f"哪个敏捷角色应该处理这种情况？",
                f"根据敏捷实践，谁应该带头？",
                f"在敏捷环境中，哪个团队成员应该处理这个问题？",
            ],
        },
        "predictive_process": {
            "en": [
                f"In a predictive approach, which process should be applied?",
                f"Which predictive process group does this belong to?",
                f"What is the correct predictive process to follow?",
                f"Which process should the project manager invoke?",
            ],
            "zh": [
                f"在预测性方法中，应该应用哪个过程？",
                f"这属于哪个预测性过程组？",
                f"正确的预测性过程是什么？",
                f"项目经理应该调用哪个过程？",
            ],
        },
        "hybrid_scenario": {
            "en": [
                f"In a hybrid project environment, what is the BEST approach?",
                f"How should the project manager handle this in a hybrid context?",
                f"Which hybrid approach is MOST appropriate?",
                f"What should the project manager do in this hybrid situation?",
            ],
            "zh": [
                f"在混合项目环境中，最佳方法是什么？",
                f"项目经理在混合环境中应该如何处理？",
                f"哪种混合方法最合适？",
                f"在这种混合情况下，项目经理应该做什么？",
            ],
        },
        "ethical_scenario": {
            "en": [
                f"What is the MOST ethical course of action?",
                f"According to the PMI Code of Ethics, what should the project manager do?",
                f"What is the ethically appropriate response?",
                f"Which action aligns with PMI's ethical standards?",
            ],
            "zh": [
                f"最符合道德的行动方案是什么？",
                f"根据PMI道德准则，项目经理应该做什么？",
                f"道德上适当的回应是什么？",
                f"哪个行动符合PMI的道德标准？",
            ],
        },
        "stakeholder_engagement": {
            "en": [
                f"How should the project manager engage this stakeholder?",
                f"What is the BEST stakeholder engagement strategy?",
                f"Which engagement approach is MOST appropriate?",
                f"How should the project manager manage this stakeholder relationship?",
            ],
            "zh": [
                f"项目经理应该如何与该干系人互动？",
                f"最佳的干系人参与策略是什么？",
                f"哪种参与方法最合适？",
                f"项目经理应该如何管理这种干系人关系？",
            ],
        },
        "risk_response": {
            "en": [
                f"What is the BEST risk response strategy for this situation?",
                f"Which risk response should the project manager implement?",
                f"How should the project manager respond to this risk?",
                f"Which risk strategy is MOST appropriate?",
            ],
            "zh": [
                f"这种情况下的最佳风险应对策略是什么？",
                f"项目经理应该实施哪种风险应对？",
                f"项目经理应该如何应对这个风险？",
                f"哪种风险策略最合适？",
            ],
        },
        "conflict_resolution": {
            "en": [
                f"Which conflict resolution approach is MOST appropriate?",
                f"How should the project manager resolve this conflict?",
                f"Which conflict resolution technique should be used?",
                f"What is the BEST way to address this conflict?",
            ],
            "zh": [
                f"哪种冲突解决方法最合适？",
                f"项目经理应该如何解决这个冲突？",
                f"应该使用哪种冲突解决技术？",
                f"解决这个冲突的最佳方式是什么？",
            ],
        },
    }

    # Option generators by topic and type
    def gen_options(topic_id, q_type, difficulty):
        """Generate contextually appropriate options."""
        # Topic-specific option pools
        option_pools = {
            "P01": {  # Team Management
                "en": [
                    ["Facilitate a team charter session to clarify roles and responsibilities",
                     "Replace the underperforming team members immediately",
                     "Escalate the issue to the functional manager",
                     "Ignore the issue and hope it resolves itself"],
                    ["Implement regular one-on-one meetings with team members",
                     "Increase surveillance and monitoring of team activities",
                     "Assign all critical tasks to the most experienced member",
                     "Document the issues for performance reviews"],
                    ["Organize a team-building activity to improve collaboration",
                     "Mandate overtime to meet project deadlines",
                     "Restructure the entire team organization",
                     "Limit communication to formal channels only"],
                    ["Establish clear working agreements and team norms",
                     "Impose strict rules and penalties for non-compliance",
                     "Allow complete autonomy without any guidelines",
                     "Delegate all decisions to the most senior member"],
                    ["Conduct a retrospective to identify and address team issues",
                     "Blame specific team members for the problems",
                     "Ignore the issues as they are part of team development",
                     "Immediately escalate to senior management"],
                ],
                "zh": [
                    ["组织团队章程会议，明确角色和职责",
                     "立即替换表现不佳的团队成员",
                     "将问题上报给职能经理",
                     "忽略问题，希望它自行解决"],
                    ["实施与团队成员的定期一对一会议",
                     "加强对团队活动的监视和监控",
                     "将所有关键任务分配给最有经验的成员",
                     "记录问题用于绩效评估"],
                    ["组织团队建设活动以改善协作",
                     "强制加班以满足项目截止日期",
                     "重组整个团队组织",
                     "将沟通限制为仅正式渠道"],
                    ["建立明确的工作协议和团队规范",
                     "对不合规行为施加严格规则和惩罚",
                     "允许完全自主，没有任何指导方针",
                     "将所有决策委托给最资深的成员"],
                    ["进行回顾会议以识别和解决团队问题",
                     "指责特定团队成员造成的问题",
                     "忽略问题，因为它们是团队发展的一部分",
                     "立即向高级管理层上报"],
                ],
            },
            "P02": {  # Conflict Resolution
                "en": [
                    ["Use a collaborative approach to find a win-win solution",
                     "Impose the project manager's decision on both parties",
                     "Avoid the conflict and hope it resolves naturally",
                     "Escalate to senior management immediately"],
                    ["Facilitate a meeting between the conflicting parties to discuss the issue",
                     "Take sides with the party who has more authority",
                     "Document the conflict and wait for resolution",
                     "Separate the conflicting parties permanently"],
                    ["Apply the compromising technique to reach a middle ground",
                     "Force one party to accept the other's position",
                     "Ignore the conflict as it's not project-related",
                     "Replace one of the conflicting parties"],
                    ["Use the confronting technique to address the root cause",
                     "Smooth over the conflict without addressing the real issue",
                     "Withdraw from the situation entirely",
                     "Apply authority to end the conflict"],
                    ["Implement a structured conflict resolution process",
                     "Avoid discussing the conflict in team meetings",
                     "Let the team resolve it without any intervention",
                     "Escalate all conflicts to the sponsor"],
                ],
                "zh": [
                    ["使用合作方法寻找双赢解决方案",
                     "将项目经理的决定强加给双方",
                     "避免冲突，希望它自然解决",
                     "立即向高级管理层上报"],
                    ["组织冲突双方会议讨论问题",
                     "支持拥有更多权力的一方",
                     "记录冲突并等待解决",
                     "永久分离冲突双方"],
                    ["应用妥协技术达成中间立场",
                     "强迫一方接受另一方的立场",
                     "忽略冲突，因为它与项目无关",
                     "替换冲突一方"],
                    ["使用面对技术解决根本原因",
                     "在不解决真正问题的情况下平息冲突",
                     "完全退出情况",
                     "运用权力结束冲突"],
                    ["实施结构化的冲突解决过程",
                     "在团队会议中避免讨论冲突",
                     "让团队在没有任何干预的情况下解决",
                     "将所有冲突上报给发起人"],
                ],
            },
            "P03": {  # Leadership Styles
                "en": [
                    ["Adopt a servant leadership approach to empower the team",
                     "Use an autocratic leadership style for quick decisions",
                     "Apply a laissez-faire approach with no direction",
                     "Use only transactional leadership with rewards and penalties"],
                    ["Implement transformational leadership to inspire the team",
                     "Maintain strict hierarchical control over all decisions",
                     "Avoid making any leadership decisions",
                     "Delegate all leadership responsibilities to the team"],
                    ["Use situational leadership based on team maturity",
                     "Apply the same leadership style regardless of context",
                     "Only use directive leadership in all situations",
                     "Avoid adapting leadership style to the situation"],
                    ["Practice empathetic leadership to understand team needs",
                     "Focus only on task completion without considering people",
                     "Avoid emotional situations entirely",
                     "Use fear as a motivational tool"],
                    ["Lead by example and demonstrate desired behaviors",
                     "Only give instructions without demonstrating",
                     "Distance yourself from the team to maintain authority",
                     "Avoid visibility to prevent criticism"],
                ],
                "zh": [
                    ["采用服务型领导方法赋能团队",
                     "使用专制领导风格进行快速决策",
                     "采用无方向的自由放任方法",
                     "仅使用交易型领导，结合奖惩"],
                    ["实施变革型领导以激励团队",
                     "对所有决策保持严格的等级控制",
                     "避免做出任何领导决策",
                     "将所有领导责任委托给团队"],
                    ["根据团队成熟度使用情境领导",
                     "无论上下文如何都应用相同的领导风格",
                     "在所有情况下仅使用指令型领导",
                     "避免根据情况调整领导风格"],
                    ["实践同理心领导以理解团队需求",
                     "只关注任务完成而不考虑人员",
                     "完全避免情绪化情况",
                     "使用恐惧作为激励工具"],
                    ["以身作则，展示期望的行为",
                     "只给指示而不示范",
                     "与团队保持距离以维护权威",
                     "避免可见性以防止批评"],
                ],
            },
        }

        # Default options for topics not in the specific pool
        default_en = [
            [f"Apply {topic_en} best practices to address the situation",
             f"Ignore the {topic_en.lower()} issues and focus on deliverables",
             f"Escalate all {topic_en.lower()} decisions to senior management",
             f"Delegate {topic_en.lower()} responsibilities entirely to the team"],
            [f"Develop a comprehensive {topic_en.lower()} plan",
             f"Use ad-hoc approaches without formal planning",
             f"Copy the approach from a previous project without adaptation",
             f"Wait for problems to arise before taking action"],
            [f"Engage stakeholders in {topic_en.lower()} decision-making",
             f"Make all decisions without stakeholder input",
             f"Avoid stakeholder engagement to save time",
             f"Only engage stakeholders who agree with the approach"],
            [f"Implement continuous improvement in {topic_en.lower()}",
             f"Maintain the status quo without changes",
             f"Only make changes when absolutely necessary",
             f"Avoid retrospectives and lessons learned"],
            [f"Use data-driven approaches for {topic_en.lower()} decisions",
             f"Rely solely on intuition and gut feeling",
             f"Copy metrics from other projects without context",
             f"Avoid measuring performance to reduce overhead"],
        ]

        default_zh = [
            [f"应用{topic_zh}最佳实践来应对情况",
             f"忽略{topic_zh}问题，专注于交付物",
             f"将所有{topic_zh}决策上报给高级管理层",
             f"将{topic_zh}责任完全委托给团队"],
            [f"制定全面的{topic_zh}计划",
             f"使用临时方法，不进行正式规划",
             f"直接复制以前项目的方法而不进行调整",
             f"等问题出现后再采取行动"],
            [f"让干系人参与{topic_zh}决策",
             f"在没有干系人意见的情况下做出所有决策",
             f"为节省时间避免干系人参与",
             f"只与同意该方法的干系人互动"],
            [f"在{topic_zh}中实施持续改进",
             f"保持现状，不做任何改变",
             f"只在绝对必要时做出改变",
             f"避免回顾会议和经验教训"],
            [f"使用数据驱动的方法进行{topic_zh}决策",
             f"完全依赖直觉和预感",
             f"在没有上下文的情况下复制其他项目的指标",
             f"为减少开销避免衡量绩效"],
        ]

        if topic_id in option_pools:
            pool = option_pools[topic_id]
            idx = random.randint(0, len(pool["en"]) - 1)
            return pool["en"][idx], pool["zh"][idx]
        else:
            idx = random.randint(0, len(default_en) - 1)
            return default_en[idx], default_zh[idx]

    def gen_explanation(topic_en, topic_zh, domain, q_type, answer_text_en, answer_text_zh, difficulty):
        """Generate explanation for the correct answer."""
        explanations = {
            "first_action": {
                "en": f"The correct answer focuses on the FIRST action because in {topic_en.lower()}, addressing the immediate situation is critical before taking further steps. According to PMBOK 7th Edition principles, the project manager should prioritize understanding the situation and taking the most appropriate initial action. This approach aligns with the {domain} domain requirements and demonstrates effective {topic_en.lower()} practices.",
                "zh": f"正确答案关注的是第一个行动，因为在{topic_zh}中，在采取进一步步骤之前处理即时情况至关重要。根据PMBOK第7版原则，项目经理应优先理解情况并采取最合适的初始行动。这种方法符合{domain}领域要求，并展示了有效的{topic_zh}实践。",
            },
            "best_approach": {
                "en": f"The best approach in this {topic_en.lower()} scenario involves applying professional judgment and established best practices. According to PMBOK 7th Edition, the project manager should consider the context, stakeholders, and project objectives when determining the approach. This solution aligns with the principles of {domain} management and promotes effective project delivery.",
                "zh": f"在这种{topic_zh}场景中，最佳方法涉及应用专业判断和既定最佳实践。根据PMBOK第7版，项目经理在确定方法时应考虑背景、干系人和项目目标。此解决方案符合{domain}管理原则，并促进有效的项目交付。",
            },
            "tool_technique": {
                "en": f"The selected tool or technique is most appropriate for this {topic_en.lower()} situation because it directly addresses the core issue. According to PMBOK 7th Edition, selecting the right tools and techniques is essential for effective project management. The chosen approach demonstrates alignment with {domain} best practices and promotes efficient project execution.",
                "zh": f"所选工具或技术最适合这种{topic_zh}情况，因为它直接解决核心问题。根据PMBOK第7版，选择正确的工具和技术对于有效的项目管理至关重要。所选方法展示了与{domain}最佳实践的一致性，并促进高效的项目执行。",
            },
            "agile_role": {
                "en": f"In an agile context, the identified role is responsible for this {topic_en.lower()} activity according to agile frameworks. The Scrum Guide and agile principles define clear role responsibilities. This answer aligns with agile practices and demonstrates understanding of role-based accountability in agile environments.",
                "zh": f"在敏捷环境中，根据敏捷框架，所识别的角色负责此{topic_zh}活动。Scrum指南和敏捷原则定义了明确的角色职责。此答案符合敏捷实践，并展示了对敏捷环境中基于角色的问责制的理解。",
            },
            "predictive_process": {
                "en": f"The correct predictive process for this {topic_en.lower()} scenario follows the structured approach defined in PMBOK. In a predictive environment, processes are sequential and well-defined. This answer demonstrates understanding of the process groups and knowledge areas relevant to {topic_en.lower()} in a predictive context.",
                "zh": f"这种{topic_zh}场景的正确预测性过程遵循PMBOK中定义的结构化方法。在预测性环境中，过程是顺序的且明确定义的。此答案展示了对预测性环境中与{topic_zh}相关的过程组和知识领域的理解。",
            },
            "hybrid_scenario": {
                "en": f"In a hybrid project environment, this {topic_en.lower()} approach combines elements of both predictive and agile methodologies. The project manager must adapt the approach based on the project context. This answer demonstrates understanding of how to tailor {topic_en.lower()} practices for a hybrid environment.",
                "zh": f"在混合项目环境中，这种{topic_zh}方法结合了预测性和敏捷方法论的元素。项目经理必须根据项目背景调整方法。此答案展示了对如何为混合环境定制{topic_zh}实践的理解。",
            },
            "ethical_scenario": {
                "en": f"This {topic_en.lower()} response aligns with PMI's Code of Ethics and Professional Conduct. The ethical approach requires honesty, responsibility, respect, and fairness. The project manager must consider the ethical implications of their decisions and act with integrity in all {topic_en.lower()} matters.",
                "zh": f"这种{topic_zh}回应符合PMI道德和专业行为准则。道德方法要求诚实、责任、尊重和公平。项目经理必须考虑其决策的道德影响，并在所有{topic_zh}事项中以诚信行事。",
            },
            "stakeholder_engagement": {
                "en": f"This {topic_en.lower()} approach effectively manages stakeholder expectations and engagement. According to PMBOK 7th Edition, stakeholder engagement is critical for project success. The selected strategy demonstrates understanding of stakeholder analysis and engagement planning principles.",
                "zh": f"这种{topic_zh}方法有效地管理干系人期望和参与。根据PMBOK第7版，干系人参与对项目成功至关重要。所选策略展示了对干系人分析和参与规划原则的理解。",
            },
            "risk_response": {
                "en": f"The selected {topic_en.lower()} risk response strategy is most appropriate because it directly addresses the identified risk. According to PMBOK 7th Edition, risk responses should be proportionate to the risk impact and probability. This approach demonstrates effective risk management in the {domain} context.",
                "zh": f"所选的{topic_zh}风险应对策略最合适，因为它直接解决了已识别的风险。根据PMBOK第7版，风险应对应与风险影响和概率成比例。此方法展示了{domain}背景下的有效风险管理。",
            },
            "conflict_resolution": {
                "en": f"This {topic_en.lower()} conflict resolution approach is most effective because it addresses the root cause while maintaining professional relationships. According to PMBOK 7th Edition, conflict resolution should aim for win-win outcomes. This approach demonstrates effective {topic_en.lower()} and promotes team collaboration.",
                "zh": f"这种{topic_zh}冲突解决方法最有效，因为它在维护专业关系的同时解决了根本原因。根据PMBOK第7版，冲突解决应以双赢结果为目标。此方法展示了有效的{topic_zh}并促进团队协作。",
            },
        }

        base = explanations.get(q_type, explanations["best_approach"])
        return base["en"], base["zh"]

    # Pick question type
    q_type = q_type
    patterns_for_type = patterns[q_type]

    q_en = scenario + " " + random.choice(patterns_for_type["en"])
    q_zh = scenario + " " + random.choice(patterns_for_type["zh"])

    opts_en, opts_zh = gen_options(topic_id, q_type, difficulty)

    # Shuffle but track answer
    answer_idx = 0  # First option is always correct before shuffle
    indices = list(range(4))
    random.shuffle(indices)
    shuffled_en = [opts_en[i] for i in indices]
    shuffled_zh = [opts_zh[i] for i in indices]
    new_answer = indices.index(0)

    exp_en, exp_zh = gen_explanation(topic_en, topic_zh, domain, q_type, shuffled_en[new_answer], shuffled_zh[new_answer], difficulty)

    return q_en, q_zh, shuffled_en, shuffled_zh, new_answer, exp_en, exp_zh


def generate_questions_for_topic(topic, domain, count, start_id, difficulty_range):
    """Generate a specified number of questions for a given topic."""
    questions = []
    q_types = QUESTION_TYPES.copy()

    for i in range(count):
        scenario = random.choice(topic["scenarios"])
        q_type = q_types[i % len(q_types)]
        difficulty = random.randint(difficulty_range[0], difficulty_range[1])

        # Add variation to scenarios
        variations = [
            "",
            " The project is using an agile approach.",
            " The project follows a predictive methodology.",
            " The organization is transitioning to agile.",
            " This is a hybrid project with both hardware and software components.",
            " The project is in the execution phase.",
            " The project is in the planning phase.",
            " The team is distributed across multiple locations.",
            " The project has a tight deadline.",
            " The project has limited budget.",
            " The organization has a strong project management culture.",
            " The project involves external vendors.",
            " The project is part of a larger program.",
            " The team is newly formed.",
            " The project has high visibility with senior management.",
        ]

        scenario_with_variation = scenario + random.choice(variations)

        topic_en = topic["en"]
        topic_zh = topic["zh"]

        q_en, q_zh, opts_en, opts_zh, answer, exp_en, exp_zh = generate_question_options_and_explanation(
            scenario_with_variation, topic["id"], topic_en, topic_zh, domain, q_type, difficulty
        )

        # Add more variety to difficulty explanation
        diff_labels = {1: "Foundational", 2: "Intermediate", 3: "Advanced"}
        diff_labels_zh = {1: "基础", 2: "中级", 3: "高级"}

        question = {
            "id": start_id + i,
            "subtopic_id": topic["id"],
            "topic_en": topic_en,
            "topic_zh": topic_zh,
            "question_en": q_en,
            "question_zh": q_zh,
            "options_en": opts_en,
            "options_zh": opts_zh,
            "answer": answer,
            "explanation_en": exp_en,
            "explanation_zh": exp_zh,
            "difficulty": difficulty,
        }
        questions.append(question)

    return questions


# ============================================================
# MAIN GENERATION
# ============================================================

def main():
    all_questions = []
    current_id = 1

    # Distribution
    people_count = 4200
    process_count = 5000
    business_count = 800

    # People Domain: 4200 questions across 12 topics
    people_per_topic = people_count // len(PEOPLE_TOPICS)
    people_remainder = people_count % len(PEOPLE_TOPICS)

    print(f"Generating People domain: {people_count} questions...")
    for i, topic in enumerate(PEOPLE_TOPICS):
        count = people_per_topic + (1 if i < people_remainder else 0)
        questions = generate_questions_for_topic(topic, "People", count, current_id, (1, 3))
        all_questions.extend(questions)
        current_id += count
        print(f"  {topic['en']}: {count} questions (IDs {current_id-count}-{current_id-1})")

    # Process Domain: 5000 questions across 20 topics
    process_per_topic = process_count // len(PROCESS_TOPICS)
    process_remainder = process_count % len(PROCESS_TOPICS)

    print(f"\nGenerating Process domain: {process_count} questions...")
    for i, topic in enumerate(PROCESS_TOPICS):
        count = process_per_topic + (1 if i < process_remainder else 0)
        questions = generate_questions_for_topic(topic, "Process", count, current_id, (1, 3))
        all_questions.extend(questions)
        current_id += count
        print(f"  {topic['en']}: {count} questions (IDs {current_id-count}-{current_id-1})")

    # Business Environment Domain: 800 questions across 8 topics
    business_per_topic = business_count // len(BUSINESS_TOPICS)
    business_remainder = business_count % len(BUSINESS_TOPICS)

    print(f"\nGenerating Business Environment domain: {business_count} questions...")
    for i, topic in enumerate(BUSINESS_TOPICS):
        count = business_per_topic + (1 if i < business_remainder else 0)
        questions = generate_questions_for_topic(topic, "Business Environment", count, current_id, (1, 3))
        all_questions.extend(questions)
        current_id += count
        print(f"  {topic['en']}: {count} questions (IDs {current_id-count}-{current_id-1})")

    print(f"\nTotal questions generated: {len(all_questions)}")

    # Save to JSON
    output_path = os.path.join(OUTPUT_DIR, "questions.json")
    print(f"\nSaving to {output_path}...")

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_questions, f, ensure_ascii=False, indent=2)

    file_size = os.path.getsize(output_path)
    print(f"File saved: {file_size / (1024*1024):.1f} MB")

    # Verify
    with open(output_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"Verification: {len(data)} questions in file")

    # Stats
    difficulties = {}
    topics = {}
    for q in data:
        d = q["difficulty"]
        t = q["subtopic_id"]
        difficulties[d] = difficulties.get(d, 0) + 1
        topics[t] = topics.get(t, 0) + 1

    print("\nDifficulty distribution:")
    for d in sorted(difficulties):
        print(f"  Level {d}: {difficulties[d]}")

    print("\nTopic distribution:")
    for t in sorted(topics):
        print(f"  {t}: {topics[t]}")


if __name__ == "__main__":
    main()
