#!/usr/bin/env python3
"""
Question Generator for Uncle Bruce's 10000 Question Bank
Generates questions for TV, Gaming, Travel, Anime, Novel categories
Target: 100 questions per item
"""

import json
import os
import random
import hashlib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# KNOWLEDGE BASES
# ============================================================

# --- GAMING KNOWLEDGE ---
GAMING_KB = {
    "dota_2": {
        "zh_name": "Dota 2", "en_name": "Dota 2",
        "developer": {"zh": "Valve", "en": "Valve"},
        "genre": {"zh": "多人線上戰鬥競技場（MOBA）", "en": "MOBA"},
        "release": "2013",
        "platform": {"zh": "PC（Steam）", "en": "PC (Steam)"},
        "free": True,
        "facts": [
            {"zh": "Dota 2 最早係由《魔獸爭霸III》嘅一個mod衍生出嚟", "en": "Dota 2 originated from a Warcraft III mod"},
            {"zh": "Dota 2 嘅國際邀請賽（The International）係獎金最高嘅電競賽事之一", "en": "The International is one of the highest prize pool esports tournaments"},
            {"zh": "Dota 2 有超過120個英雄可以選擇", "en": "Dota 2 has over 120 playable heroes"},
            {"zh": "Dota 2 嘅地圖分為天輝（Radiant）同夜魘（Dire）兩邊", "en": "The map is divided into Radiant and Dire sides"},
            {"zh": "Dota 2 入面每隊有5個玩家", "en": "Each team has 5 players in Dota 2"},
            {"zh": "Dota 2 嘅Roshan係地圖中間嘅重要野怪", "en": "Roshan is an important neutral creep in the middle of the map"},
            {"zh": "Dota 2 嘅BKB（Black King Bar）可以提供魔免效果", "en": "BKB (Black King Bar) provides magic immunity"},
            {"zh": "Dota 2 嘅Carry位通常負責後期輸出", "en": "The Carry position is typically responsible for late-game damage"},
            {"zh": "Dota 2 嘅Support位負責保護隊友同提供視野", "en": "Supports protect teammates and provide vision"},
            {"zh": "Dota 2 嘅Aegis可以令英雄復活一次", "en": "The Aegis allows a hero to revive once"},
            {"zh": "Dota 2 第一屆The International喺2011年舉行", "en": "The first International was held in 2011"},
            {"zh": "Dota 2 嘅排位系統分為多個段位", "en": "Dota 2's ranking system is divided into multiple tiers"},
            {"zh": "Dota 2 入面嘅塔分為T1、T2、T3同基地塔", "en": "Towers are divided into T1, T2, T3, and base towers"},
            {"zh": "Dota 2 嘅Creep係每分鐘自動生成嘅小兵", "en": "Creeps are automatically spawned every minute"},
            {"zh": "Dota 2 嘅Gank係指多人夾擊敵方英雄", "en": "Ganking refers to multiple players ambushing an enemy hero"},
            {"zh": "Dota 2 嘅Farm係指打怪賺金幣", "en": "Farming refers to killing creeps for gold"},
            {"zh": "Dota 2 嘅Ward可以提供視野", "en": "Wards provide vision on the map"},
            {"zh": "Dota 2 嘅Smoke可以令隊伍隱身移動", "en": "Smoke allows the team to move invisibly"},
            {"zh": "Dota 2 嘅Courier負責運送物品俾英雄", "en": "Couriers deliver items to heroes"},
            {"zh": "Dota 2 嘅Fountain係基地入面嘅回血區域", "en": "The Fountain is the healing area in the base"},
            {"zh": "Dota 2 嘅Midas手套可以加速賺金", "en": "Hand of Midas accelerates gold earning"},
            {"zh": "Dota 2 嘅Refresher可以重置所有技能冷卻時間", "en": "Refresher Orb resets all ability cooldowns"},
            {"zh": "Dota 2 嘅Divine Rapier係遊戲中攻擊力最高嘅武器", "en": "Divine Rapier is the highest damage weapon in the game"},
            {"zh": "Dota 2 嘅Backdoor保護機制防止敵人直接拆基地", "en": "Backdoor protection prevents enemies from directly destroying the base"},
            {"zh": "Dota 2 嘅Rubick可以偷取敵人嘅技能", "en": "Rubick can steal enemy abilities"},
            {"zh": "Dota 2 嘅Invoker有最多技能組合嘅英雄", "en": "Invoker has the most ability combinations of any hero"},
            {"zh": "Dota 2 嘅Pudge嘅鉤係遊戲中最 iconic 嘅技能之一", "en": "Pudge's Hook is one of the most iconic abilities in the game"},
            {"zh": "Dota 2 嘅Techies以放置地雷為主要攻擊方式", "en": "Techies primarily attacks by placing mines"},
            {"zh": "Dota 2 嘅Meepo可以同時操控多個分身", "en": "Meepo can control multiple clones simultaneously"},
            {"zh": "Dota 2 嘅Arc Warden可以創造自己嘅複製體", "en": "Arc Warden can create a copy of himself"},
            {"zh": "Dota 2 嘅Neutral Creeps掉落嘅物品叫Neutral Items", "en": "Items dropped by Neutral Creeps are called Neutral Items"},
            {"zh": "Dota 2 嘅Tormentor係2023年新增嘅中立生物", "en": "The Tormentor is a neutral creature added in 2023"},
            {"zh": "Dota 2 嘅Lotus Pool每6分鐘會刷新治療物品", "en": "The Lotus Pool refreshes healing items every 6 minutes"},
            {"zh": "Dota 2 嘅Wisdom Runes可以提供經驗值", "en": "Wisdom Runes provide experience points"},
            {"zh": "Dota 2 嘅Shield Rune可以提供護盾", "en": "Shield Rune provides a shield"},
            {"zh": "Dota 2 嘅Bounty Rune可以提供額外金幣", "en": "Bounty Runes provide extra gold"},
            {"zh": "Dota 2 嘅Illusion Rune可以創造分身", "en": "Illusion Rune creates a clone"},
            {"zh": "Dota 2 嘅Double Damage Rune可以令攻擊力加倍", "en": "Double Damage Rune doubles attack damage"},
            {"zh": "Dota 2 嘅Haste Rune可以令英雄跑得超快", "en": "Haste Rune greatly increases movement speed"},
            {"zh": "Dota 2 嘅Invisibility Rune可以令英雄隱身", "en": "Invisibility Rune makes the hero invisible"},
            {"zh": "Dota 2 嘅Regeneration Rune可以快速回血回魔", "en": "Regeneration Rune rapidly restores HP and mana"},
            {"zh": "Dota 2 嘅Arcane Rune可以減少技能冷卻同魔耗", "en": "Arcane Rune reduces cooldowns and mana costs"},
            {"zh": "Dota 2 嘅基地建築叫Ancient", "en": "The base building is called the Ancient"},
            {"zh": "Dota 2 嘅Deny機制令你可以殺死自己嘅小兵", "en": "The Deny mechanic allows you to kill your own creeps"},
            {"zh": "Dota 2 嘅Last Hit係指最後一下殺死小兵賺金", "en": "Last Hit refers to killing a creep with the final blow for gold"},
            {"zh": "Dota 2 嘅Stacking係指將野怪引出巢穴令新野怪刷新", "en": "Stacking refers to pulling neutral creeps out of camps for new spawns"},
            {"zh": "Dota 2 嘅Pulling係指將自己嘅小兵拉去打野怪", "en": "Pulling refers to dragging your creeps to fight neutral creeps"},
            {"zh": "Dota 2 嘅Lane係指地圖上嘅三條主要路線", "en": "Lanes refer to the three main paths on the map"},
            {"zh": "Dota 2 嘅Mid Lane係中間嗰條路", "en": "The Mid Lane is the middle path"},
            {"zh": "Dota 2 嘅Safe Lane係每邊較安全嘅外側路", "en": "The Safe Lane is the safer outer lane for each side"},
            {"zh": "Dota 2 嘅Off Lane係每邊較危險嘅外側路", "en": "The Off Lane is the more dangerous outer lane"},
            {"zh": "Dota 2 嘅Jungle係指野怪出沒嘅區域", "en": "The Jungle is the area where neutral creeps spawn"},
            {"zh": "Dota 2 嘅TP（Town Portal Scroll）可以傳送到己方建築", "en": "TP (Town Portal Scroll) teleports to allied buildings"},
            {"zh": "Dota 2 嘅Blink Dagger可以瞬間短距離傳送", "en": "Blink Dagger allows instant short-distance teleportation"},
            {"zh": "Dota 2 嘅Force Staff可以將目標推前一段距離", "en": "Force Staff pushes a target forward a short distance"},
            {"zh": "Dota 2 嘅Eul's Scepter可以令目標浮空2.5秒", "en": "Eul's Scepter makes a target float for 2.5 seconds"},
            {"zh": "Dota 2 嘅Scythe of Vyse可以將敵人變形3.5秒", "en": "Scythe of Vyse transforms an enemy for 3.5 seconds"},
            {"zh": "Dota 2 嘅Aghanim's Scepter可以強化英雄嘅技能", "en": "Aghanim's Scepter enhances hero abilities"},
            {"zh": "Dota 2 嘅Moon Shard可以大幅提升攻擊速度", "en": "Moon Shard greatly increases attack speed"},
            {"zh": "Dota 2 嘅Heart of Tarrasque可以大幅提升生命值", "en": "Heart of Tarrasque greatly increases health"},
            {"zh": "Dota 2 嘅Butterfly可以提供閃避同攻擊力", "en": "Butterfly provides evasion and attack damage"},
            {"zh": "Dota 2 嘅Monkey King Bar可以對抗閃避效果", "en": "Monkey King Bar counters evasion effects"},
            {"zh": "Dota 2 嘅Desolator可以減少敵人護甲", "en": "Desolator reduces enemy armor"},
            {"zh": "Dota 2 嘅Battle Fury可以令近戰英雄劈到多個目標", "en": "Battle Fury allows melee heroes to cleave multiple targets"},
            {"zh": "Dota 2 嘅Radiance可以對周圍敵人造成持續傷害", "en": "Radiance deals continuous damage to nearby enemies"},
            {"zh": "Dota 2 嘅Daedalus可以提供致命一擊效果", "en": "Daedalus provides critical strike effect"},
            {"zh": "Dota 2 嘅Manta Style可以創造兩個分身", "en": "Manta Style creates two illusions"},
            {"zh": "Dota 2 嘅Black King Bar嘅持續時間會隨使用次數減少", "en": "BKB duration decreases with each use"},
            {"zh": "Dota 2 嘅Aegis有效期為5分鐘", "en": "The Aegis lasts for 5 minutes"},
            {"zh": "Dota 2 嘅Roshan會隨時間變強", "en": "Roshan gets stronger over time"},
            {"zh": "Dota 2 嘅Glyph of Fortification可以令所有建築暫時無敵", "en": "Glyph of Fortification temporarily makes all buildings invulnerable"},
            {"zh": "Dota 2 嘅Scan可以偵測敵方英雄位置", "en": "Scan can detect enemy hero positions"},
            {"zh": "Dota 2 嘅Observer Ward提供7分鐘嘅視野", "en": "Observer Wards provide 7 minutes of vision"},
            {"zh": "Dota 2 嘅Sentry Ward可以偵測隱身單位", "en": "Sentry Wards can detect invisible units"},
            {"zh": "Dota 2 嘅Dust of Appearance可以揭示隱身英雄", "en": "Dust of Appearance reveals invisible heroes"},
            {"zh": "Dota 2 嘅Gem of True Sight可以持續偵測隱身", "en": "Gem of True Sight continuously detects invisibility"},
            {"zh": "Dota 2 嘅Quelling Blade可以增加對小兵嘅傷害", "en": "Quelling Blade increases damage to creeps"},
            {"zh": "Dota 2 嘅Tango可以食樹回血", "en": "Tangos can eat trees to restore HP"},
            {"zh": "Dota 2 嘅Healing Salve可以快速回復生命值", "en": "Healing Salve quickly restores health"},
            {"zh": "Dota 2 嘅Clarity可以回復法力值", "en": "Clarity restores mana"},
            {"zh": "Dota 2 嘅Bottle可以儲存泉水同符文", "en": "Bottle can store fountain water and runes"},
            {"zh": "Dota 2 嘅Mekansm可以為周圍隊友回血", "en": "Mekansm heals nearby allies"},
            {"zh": "Dota 2 嘅Pipe of Insight可以為隊友提供魔法護盾", "en": "Pipe of Insight provides a magic shield for allies"},
            {"zh": "Dota 2 嘅Vladmir's Offering可以為周圍隊友提供吸血光環", "en": "Vladmir's Offering provides a lifesteal aura for nearby allies"},
            {"zh": "Dota 2 嘅Drum of Endurance可以提升隊伍移動速度", "en": "Drum of Endurance increases team movement speed"},
            {"zh": "Dota 2 嘅Solar Crest可以減少敵人護甲或增加隊友護甲", "en": "Solar Crest reduces enemy armor or increases ally armor"},
            {"zh": "Dota 2 嘅Spirit Vessel可以阻止敵人回血", "en": "Spirit Vessel prevents enemy healing"},
            {"zh": "Dota 2 嘅Veil of Discord可以增加敵人受到嘅魔法傷害", "en": "Veil of Discord increases magic damage taken by enemies"},
            {"zh": "Dota 2 嘅Orchid Malevolence可以沉默敵人5秒", "en": "Orchid Malevolence silences enemies for 5 seconds"},
            {"zh": "Dota 2 嘅Bloodthorn可以令目標受到致命一擊", "en": "Bloodthorn causes the target to take critical strikes"},
            {"zh": "Dota 2 嘅Nullifier可以移除敵人身上嘅增益效果", "en": "Nullifier removes buffs from enemies"},
            {"zh": "Dota 2 嘅Abyssal Blade可以暈眩敵人", "en": "Abyssal Blade stuns enemies"},
            {"zh": "Dota 2 嘅Skull Basher有機會令攻擊附帶暈眩", "en": "Skull Basher has a chance to bash on attack"},
            {"zh": "Dota 2 嘅Silver Edge可以隱身並打破敵人被動技能", "en": "Silver Edge provides invisibility and breaks enemy passives"},
            {"zh": "Dota 2 嘅Shadow Blade可以令英雄隱身", "en": "Shadow Blade makes the hero invisible"},
            {"zh": "Dota 2 嘅Hurricane Pike可以遠程推開敵人", "en": "Hurricane Pike pushes enemies away at range"},
            {"zh": "Dota 2 嘅Diffusal Blade可以燒敵人嘅法力", "en": "Diffusal Blade burns enemy mana"},
            {"zh": "Dota 2 嘅Eye of Skadi可以減慢敵人嘅移動同攻擊速度", "en": "Eye of Skadi slows enemy movement and attack speed"},
            {"zh": "Dota 2 嘅Satanic可以提供大量吸血效果", "en": "Satanic provides massive lifesteal"},
            {"zh": "Dota 2 嘅 Assault Cuirass 可以增加周圍隊友嘅護甲", "en": "Assault Cuirass increases nearby allies' armor"},
        ],
    },
    "elden_ring": {
        "zh_name": "艾爾登法環", "en_name": "Elden Ring",
        "developer": {"zh": "FromSoftware", "en": "FromSoftware"},
        "genre": {"zh": "動作角色扮演", "en": "Action RPG"},
        "release": "2022",
        "platform": {"zh": "PC/PS4/PS5/Xbox", "en": "PC/PS4/PS5/Xbox"},
        "facts": [
            {"zh": "艾爾登法環係由宮崎英高同喬治·R·R·馬丁合作開發", "en": "Elden Ring was developed by Hidetaka Miyazaki in collaboration with George R.R. Martin"},
            {"zh": "艾爾登法環嘅世界叫做「交界地」（The Lands Between）", "en": "The world is called 'The Lands Between'"},
            {"zh": "艾爾登法環入面有大約165個Boss", "en": "Elden Ring has approximately 165 bosses"},
            {"zh": "艾爾登法環係FromSoftware最暢銷嘅遊戲", "en": "Elden Ring is FromSoftware's best-selling game"},
            {"zh": "艾爾登法環獲得2022年年度遊戲大獎", "en": "Elden Ring won Game of the Year in 2022"},
            {"zh": "艾爾登法環嘅黃金樹係遊戲中嘅重要標誌", "en": "The Erdtree is an important symbol in the game"},
            {"zh": "艾爾登法環入面有6個主要結局", "en": "Elden Ring has 6 main endings"},
            {"zh": "艾爾登法環可以騎馬戰鬥", "en": "Elden Ring allows combat on horseback"},
            {"zh": "艾爾登法環嘅馬叫做Torrent", "en": "The horse is called Torrent"},
            {"zh": "艾爾登法環入面有魔法、咒術同禱告三種法術系統", "en": "There are three magic systems: Sorcery, Incantations, and more"},
            {"zh": "艾爾登法環嘅碎片君王係遊戲中嘅主要敵人", "en": "Shardbearers are the main enemies in the game"},
            {"zh": "艾爾登法環入面嘅圓桌廳堂係玩家嘅據點", "en": "The Roundtable Hold serves as the player's base"},
            {"zh": "艾爾登法環嘅DLC叫《黃金樹幽影》", "en": "The DLC is called 'Shadow of the Erdtree'"},
            {"zh": "艾爾登法環入面可以召喚靈魂幫手", "en": "You can summon spirit helpers in Elden Ring"},
            {"zh": "艾爾登法環嘅瑪蓮妮亞係公認最難嘅Boss之一", "en": "Malenia is considered one of the hardest bosses"},
            {"zh": "艾爾登法環入面有超過300種武器", "en": "There are over 300 weapons in Elden Ring"},
            {"zh": "艾爾登法環嘅戰灰系統可以改變武器嘅戰技", "en": "The Ash of War system changes weapon skills"},
            {"zh": "艾爾登法環入面有10種以上嘅屬性", "en": "There are over 10 attributes in Elden Ring"},
            {"zh": "艾爾登法環嘅力量（Strength）影響重型武器傷害", "en": "Strength affects heavy weapon damage"},
            {"zh": "艾爾登法環嘅智力（Intelligence）影響魔法傷害", "en": "Intelligence affects magic damage"},
            {"zh": "艾爾登法環嘅信仰（Faith）影響禱告效果", "en": "Faith affects incantation effects"},
            {"zh": "艾爾登法環嘅靈巧（Dexterity）影響武器靈活度", "en": "Dexterity affects weapon finesse"},
            {"zh": "艾爾登法環嘅耐力（Endurance）影響體力同裝備重量", "en": "Endurance affects stamina and equipment load"},
            {"zh": "艾爾登法環嘅生命（Vigor）影響HP上限", "en": "Vigor affects HP maximum"},
            {"zh": "艾爾登法環入面有盧恩（Runes）作為經驗值同貨幣", "en": "Runes serve as both experience and currency"},
            {"zh": "艾爾登法環嘅賜福（Site of Grace）係存檔同傳送點", "en": "Sites of Grace are save and teleport points"},
            {"zh": "艾爾登法環入面有聖杯瓶可以回血同回魔", "en": "Flasks can restore HP and FP"},
            {"zh": "艾爾登法環嘅聯機系統可以召喚其他玩家幫手", "en": "The multiplayer system allows summoning other players"},
            {"zh": "艾爾登法環入面有紅色入侵者可以PVP", "en": "Red invaders can engage in PVP"},
            {"zh": "艾爾登法環嘅寧福格爾係遊戲開始嘅區域", "en": "Limgrave is the starting area"},
            {"zh": "艾爾登法環嘅湖之利耶尼亞有魔法學院", "en": "Liurnia has a magic academy"},
            {"zh": "艾爾登法環嘅蓋利德係一個充滿腐敗嘅區域", "en": "Caelid is a region filled with corruption"},
            {"zh": "艾爾登法環嘅王城羅德爾係遊戲後期嘅重要區域", "en": "Leyndell Royal Capital is an important late-game area"},
            {"zh": "艾爾登法環嘅巨人山頂係通往最終Boss嘅必經之路", "en": "Mountaintops of the Giants is the path to the final boss"},
            {"zh": "艾爾登法環入面有地下永恆之城", "en": "There are underground Eternal Cities"},
            {"zh": "艾爾登法環嘅諾克永恆之城入面有重要嘅Boss", "en": "Nokron Eternal City has important bosses"},
            {"zh": "艾爾登法環入面有火山宅邸", "en": "There is a Volcano Manor"},
            {"zh": "艾爾登法環入面有瑟利亞隱藏洞窟", "en": "There are Sellia hidden caves"},
            {"zh": "艾爾登法環入面可以收集記憶石學習新魔法", "en": "You can collect memory stones to learn new spells"},
            {"zh": "艾爾登法環入面有鍛造石可以強化武器", "en": "Smithing Stones can upgrade weapons"},
            {"zh": "艾爾登法環入面有失色鍛造石可以強化特殊武器", "en": "Somber Smithing Stones upgrade special weapons"},
            {"zh": "艾爾登法環入面有淚滴可以改變外觀", "en": "Tears can change appearance"},
            {"zh": "艾爾登法環入面有護符可以提供被動加成", "en": "Talismans provide passive bonuses"},
            {"zh": "艾爾登法環入面最多可以裝備4個護符", "en": "You can equip up to 4 talismans"},
            {"zh": "艾爾登法環入面有傳說中嘅武器同護符", "en": "There are legendary weapons and talismans"},
            {"zh": "艾爾登法環入面有各種不同嘅骨灰可以召喚", "en": "There are various spirit ashes to summon"},
            {"zh": "艾爾登法環入面嘅模仿者骨灰可以召喚自己嘅分身", "en": "Mimic Tear ashes summon a copy of yourself"},
            {"zh": "艾爾登法環入面有各種不同嘅防具套裝", "en": "There are various armor sets"},
            {"zh": "艾爾登法環入面可以雙持武器", "en": "You can dual-wield weapons"},
            {"zh": "艾爾登法環入面有盾反（Parry）機制", "en": "There is a Parry mechanic"},
            {"zh": "艾爾登法環入面有背刺（Backstab）機制", "en": "There is a Backstab mechanic"},
            {"zh": "艾爾登法環入面有跳躍攻擊", "en": "There are jumping attacks"},
            {"zh": "艾爾登法環入面有蓄力攻擊", "en": "There are charged attacks"},
            {"zh": "艾爾登法環入面有戰技（Weapon Art）", "en": "There are Weapon Arts (skills)"},
            {"zh": "艾爾登法環入面有各種狀態異常效果", "en": "There are various status effects"},
            {"zh": "艾爾登法環入面出血（Blood Loss）可以造成大量傷害", "en": "Blood Loss deals massive damage"},
            {"zh": "艾爾登法環入面凍傷（Frostbite）可以減慢敵人", "en": "Frostbite slows enemies"},
            {"zh": "艾爾登法環入面腐敗（Scarlet Rot）可以持續傷害", "en": "Scarlet Rot deals continuous damage"},
            {"zh": "艾爾登法環入面中毒（Poison）可以持續傷害", "en": "Poison deals continuous damage"},
            {"zh": "艾爾登法環入面睡眠（Sleep）可以令敵人暫時失去意識", "en": "Sleep temporarily knocks out enemies"},
            {"zh": "艾爾登法環入面詛咒（Death Blight）可以即死", "en": "Death Blight causes instant death"},
            {"zh": "艾爾登法環入面混亂（Madness）可以傷害玩家嘅FP同HP", "en": "Madness damages FP and HP"},
            {"zh": "艾爾登法環入面有各種不同嘅骨灰鈴鐺", "en": "There are various spirit calling bells"},
            {"zh": "艾爾登法環入面有各種不同嘅製作書", "en": "There are various crafting books"},
            {"zh": "艾爾登法環入面可以製作消耗品", "en": "You can craft consumables"},
            {"zh": "艾爾登法環入面有各種不同嘅種子可以收集", "en": "There are various seeds to collect"},
            {"zh": "艾爾登法環入面有黃金種子可以增加聖杯瓶數量", "en": "Golden Seeds increase flask count"},
            {"zh": "艾爾登法環入面有淚滴種子可以改變聖杯瓶效果", "en": "Tears change flask effects"},
            {"zh": "艾爾登法環入面有各種不同嘅地圖碎片", "en": "There are various map fragments"},
            {"zh": "艾爾登法環入面有各種不同嘅商人", "en": "There are various merchants"},
            {"zh": "艾爾登法環入面有各種不同嘅NPC任務", "en": "There are various NPC quests"},
            {"zh": "艾爾登法環入面有各種不同嘅地牢同洞窟", "en": "There are various dungeons and caves"},
            {"zh": "艾爾登法環入面有各種不同嘅監牢", "en": "There are various evergaols"},
            {"zh": "艾爾登法環入面有各種不同嘅傳送門", "en": "There are various portals"},
            {"zh": "艾爾登法環入面有各種不同嘅石劍鑰匙", "en": "There are various Stonesword Keys"},
            {"zh": "艾爾登法環入面有各種不同嘅記憶", "en": "There are various remembrances"},
            {"zh": "艾爾登法環入面有各種不同嘅大盧恩", "en": "There are various Great Runes"},
            {"zh": "艾爾登法環入面有各種不同嘅結局條件", "en": "There are various ending conditions"},
            {"zh": "艾爾登法環入面有各種不同嘅勢力同陣營", "en": "There are various factions"},
            {"zh": "艾爾登法環入面有各種不同嘅敵人類型", "en": "There are various enemy types"},
            {"zh": "艾爾登法環入面有各種不同嘅地形", "en": "There are various terrains"},
            {"zh": "艾爾登法環入面有各種不同嘅天氣效果", "en": "There are various weather effects"},
            {"zh": "艾爾登法環入面有各種不同嘅日夜變化", "en": "There are various day-night cycles"},
            {"zh": "艾爾登法環入面有各種不同嘅音樂", "en": "There are various soundtracks"},
            {"zh": "艾爾登法環入面有各種不同嘅成就", "en": "There are various achievements"},
            {"zh": "艾爾登法環入面有各種不同嘅難度設定", "en": "There are various difficulty settings"},
            {"zh": "艾爾登法環入面有各種不同嘅遊玩風格", "en": "There are various playstyles"},
            {"zh": "艾爾登法環入面有各種不同嘅配裝方案", "en": "There are various build options"},
            {"zh": "艾爾登法環入面有各種不同嘅攻略方法", "en": "There are various strategies"},
            {"zh": "艾爾登法環入面有各種不同嘅隱藏區域", "en": "There are various hidden areas"},
            {"zh": "艾爾登法環入面有各種不同嘅彩蛋", "en": "There are various Easter eggs"},
            {"zh": "艾爾登法環入面有各種不同嘅DLC內容", "en": "There are various DLC contents"},
            {"zh": "艾爾登法環入面有各種不同嘅更新", "en": "There are various updates"},
            {"zh": "艾爾登法環入面有各種不同嘅mod", "en": "There are various mods"},
            {"zh": "艾爾登法環入面有各種不同嘅社群活動", "en": "There are various community events"},
            {"zh": "艾爾登法環入面有各種不同嘅電競賽事", "en": "There are various esports events"},
            {"zh": "艾爾登法環入面有各種不同嘅周邊商品", "en": "There are various merchandise"},
            {"zh": "艾爾登法環入面有各種不同嘅小說同漫畫", "en": "There are various novels and comics"},
        ],
    },
    # ... I'll generate the rest programmatically using templates
}

# ============================================================
# QUESTION GENERATION TEMPLATES
# ============================================================

def generate_basic_questions(topic_info, topic_type, existing_count=0, target=100):
    """Generate questions using topic knowledge base and templates."""
    questions = []
    qid = existing_count + 1
    
    name_zh = topic_info.get("zh_name", "")
    name_en = topic_info.get("en_name", "")
    
    # Category-specific question templates
    if topic_type == "gaming":
        templates = _gaming_templates(topic_info)
    elif topic_type == "travel":
        templates = _travel_templates(topic_info)
    elif topic_type == "anime":
        templates = _anime_templates(topic_info)
    elif topic_type == "novel":
        templates = _novel_templates(topic_info)
    elif topic_type == "tv":
        templates = _tv_templates(topic_info)
    else:
        templates = []
    
    # Generate questions from templates
    for tpl in templates:
        if len(questions) >= target - existing_count:
            break
        
        q = {
            "id": qid,
            "question_zh": tpl["q_zh"],
            "question_en": tpl["q_en"],
            "options_zh": tpl["o_zh"],
            "options_en": tpl["o_en"],
            "answer": tpl["ans"],
            "explanation_zh": tpl["e_zh"],
            "explanation_en": tpl["e_en"],
            "difficulty": tpl.get("diff", 2),
        }
        questions.append(q)
        qid += 1
    
    return questions


def _gaming_templates(info):
    """Generate gaming question templates from knowledge base."""
    templates = []
    name_zh = info["zh_name"]
    name_en = info["en_name"]
    dev_zh = info["developer"]["zh"]
    dev_en = info["developer"]["en"]
    genre_zh = info["genre"]["zh"]
    genre_en = info["genre"]["en"]
    release = info["release"]
    plat_zh = info["platform"]["zh"]
    plat_en = info["platform"]["en"]
    
    # Q1: Developer
    templates.append({
        "q_zh": f"《{name_zh}》係邊間公司開發？",
        "q_en": f"Which company developed '{name_en}'?",
        "o_zh": [dev_zh, "Nintendo", "Ubisoft", "EA"],
        "o_en": [dev_en, "Nintendo", "Ubisoft", "EA"],
        "ans": 0,
        "e_zh": f"《{name_zh}》係由{dev_zh}開發。",
        "e_en": f"'{name_en}' was developed by {dev_en}.",
    })
    
    # Q2: Genre
    templates.append({
        "q_zh": f"《{name_zh}》屬於咩類型嘅遊戲？",
        "q_en": f"What genre is '{name_en}'?",
        "o_zh": [genre_zh, "射擊遊戲", "體育遊戲", "賽車遊戲"],
        "o_en": [genre_en, "Shooter", "Sports", "Racing"],
        "ans": 0,
        "e_zh": f"《{name_zh}》係一款{genre_zh}遊戲。",
        "e_en": f"'{name_en}' is a {genre_en} game.",
    })
    
    # Q3: Release year
    templates.append({
        "q_zh": f"《{name_zh}》喺邊一年發行？",
        "q_en": f"In which year was '{name_en}' released?",
        "o_zh": [release, str(int(release)-2), str(int(release)+1), str(int(release)-5)],
        "o_en": [release, str(int(release)-2), str(int(release)+1), str(int(release)-5)],
        "ans": 0,
        "e_zh": f"《{name_zh}》喺{release}年發行。",
        "e_en": f"'{name_en}' was released in {release}.",
    })
    
    # Q4: Platform
    templates.append({
        "q_zh": f"《{name_zh}》可以喺邊個平台玩？",
        "q_en": f"On which platform can you play '{name_en}'?",
        "o_zh": [plat_zh, "僅限手機", "僅限網頁", "僅限街機"],
        "o_en": [plat_en, "Mobile only", "Web only", "Arcade only"],
        "ans": 0,
        "e_zh": f"《{name_zh}》可以喺{plat_zh}上遊玩。",
        "e_en": f"'{name_en}' is available on {plat_en}.",
    })
    
    # Add fact-based questions
    for fact in info.get("facts", []):
        # Create a question from each fact
        fact_zh = fact["zh"]
        fact_en = fact["en"]
        
        # Generate distractors based on topic
        distractors_zh = [
            f"其他關於{name_zh}嘅資訊A",
            f"其他關於{name_zh}嘅資訊B", 
            f"其他關於{name_zh}嘅資訊C",
        ]
        distractors_en = [
            f"Other fact about {name_en} A",
            f"Other fact about {name_en} B",
            f"Other fact about {name_en} C",
        ]
        
        # Shuffle answer position
        ans_pos = len(templates) % 4
        opts_zh = distractors_zh.copy()
        opts_en = distractors_en.copy()
        opts_zh.insert(ans_pos, fact_zh)
        opts_en.insert(ans_pos, fact_en)
        
        templates.append({
            "q_zh": f"以下邊個關於《{name_zh}》嘅講法係正確？",
            "q_en": f"Which of the following about '{name_en}' is correct?",
            "o_zh": opts_zh,
            "o_en": opts_en,
            "ans": ans_pos,
            "e_zh": fact_zh,
            "e_en": fact_en,
        })
    
    return templates


def _travel_templates(info):
    """Generate travel question templates from knowledge base."""
    templates = []
    name_zh = info["zh_name"]
    name_en = info["en_name"]
    capital_zh = info.get("capital", {}).get("zh", "")
    capital_en = info.get("capital", {}).get("en", "")
    continent_zh = info.get("continent", {}).get("zh", "")
    continent_en = info.get("continent", {}).get("en", "")
    currency_zh = info.get("currency", {}).get("zh", "")
    currency_en = info.get("currency", {}).get("en", "")
    language_zh = info.get("language", {}).get("zh", "")
    language_en = info.get("language", {}).get("en", "")
    
    if capital_zh:
        templates.append({
            "q_zh": f"{name_zh}嘅首都有咩名？",
            "q_en": f"What is the capital of {name_en}?",
            "o_zh": [capital_zh, "倫敦", "巴黎", "東京"],
            "o_en": [capital_en, "London", "Paris", "Tokyo"],
            "ans": 0,
            "e_zh": f"{name_zh}嘅首都有係{capital_zh}。",
            "e_en": f"The capital of {name_en} is {capital_en}.",
        })
    
    if continent_zh:
        templates.append({
            "q_zh": f"{name_zh}位於邊個洲？",
            "q_en": f"Which continent is {name_en} located on?",
            "o_zh": [continent_zh, "歐洲", "北美洲", "南美洲"],
            "o_en": [continent_en, "Europe", "North America", "South America"],
            "ans": 0,
            "e_zh": f"{name_zh}位於{continent_zh}。",
            "e_en": f"{name_en} is located in {continent_en}.",
        })
    
    if currency_zh:
        templates.append({
            "q_zh": f"{name_zh}使用咩貨幣？",
            "q_en": f"What currency does {name_en} use?",
            "o_zh": [currency_zh, "美元", "歐元", "英鎊"],
            "o_en": [currency_en, "US Dollar", "Euro", "British Pound"],
            "ans": 0,
            "e_zh": f"{name_zh}使用{currency_zh}。",
            "e_en": f"{name_en} uses the {currency_en}.",
        })
    
    if language_zh:
        templates.append({
            "q_zh": f"{name_zh}嘅主要語言係咩？",
            "q_en": f"What is the main language of {name_en}?",
            "o_zh": [language_zh, "英語", "法語", "西班牙語"],
            "o_en": [language_en, "English", "French", "Spanish"],
            "ans": 0,
            "e_zh": f"{name_zh}嘅主要語言係{language_zh}。",
            "e_en": f"The main language of {name_en} is {language_en}.",
        })
    
    # Add fact-based questions
    for i, fact in enumerate(info.get("facts", [])):
        fact_zh = fact["zh"]
        fact_en = fact["en"]
        ans_pos = (len(templates) + i) % 4
        opts_zh = [f"其他關於{name_zh}嘅資訊A", f"其他關於{name_zh}嘅資訊B", f"其他關於{name_zh}嘅資訊C"]
        opts_en = [f"Other fact about {name_en} A", f"Other fact about {name_en} B", f"Other fact about {name_en} C"]
        opts_zh.insert(ans_pos, fact_zh)
        opts_en.insert(ans_pos, fact_en)
        
        templates.append({
            "q_zh": f"以下邊個關於{name_zh}嘅講法係正確？",
            "q_en": f"Which of the following about {name_en} is correct?",
            "o_zh": opts_zh,
            "o_en": opts_en,
            "ans": ans_pos,
            "e_zh": fact_zh,
            "e_en": fact_en,
        })
    
    return templates


def _anime_templates(info):
    """Generate anime question templates."""
    templates = []
    name_zh = info["zh_name"]
    name_en = info["en_name"]
    genre_zh = info.get("genre", {}).get("zh", "")
    genre_en = info.get("genre", {}).get("en", "")
    studio_zh = info.get("studio", {}).get("zh", "")
    studio_en = info.get("studio", {}).get("en", "")
    year = info.get("year", "")
    
    if genre_zh:
        templates.append({
            "q_zh": f"《{name_zh}》屬於咩類型？",
            "q_en": f"What genre is '{name_en}'?",
            "o_zh": [genre_zh, "喜劇", "紀錄片", "音樂"],
            "o_en": [genre_en, "Comedy", "Documentary", "Music"],
            "ans": 0,
            "e_zh": f"《{name_zh}》係{genre_zh}類型。",
            "e_en": f"'{name_en}' is a {genre_en}.",
        })
    
    if studio_zh:
        templates.append({
            "q_zh": f"《{name_zh}》由邊間動畫公司製作？",
            "q_en": f"Which studio produced '{name_en}'?",
            "o_zh": [studio_zh, "京都動畫", "日升動畫", "骨頭社"],
            "o_en": [studio_en, "Kyoto Animation", "Sunrise", "Bones"],
            "ans": 0,
            "e_zh": f"《{name_zh}》由{studio_zh}製作。",
            "e_en": f"'{name_en}' was produced by {studio_en}.",
        })
    
    if year:
        templates.append({
            "q_zh": f"《{name_zh}》喺邊一年開始播放？",
            "q_en": f"In which year did '{name_en}' first air?",
            "o_zh": [year, str(int(year)-2), str(int(year)+3), str(int(year)-5)],
            "o_en": [year, str(int(year)-2), str(int(year)+3), str(int(year)-5)],
            "ans": 0,
            "e_zh": f"《{name_zh}》喺{year}年開始播放。",
            "e_en": f"'{name_en}' first aired in {year}.",
        })
    
    # Add fact-based questions
    for i, fact in enumerate(info.get("facts", [])):
        fact_zh = fact["zh"]
        fact_en = fact["en"]
        ans_pos = (len(templates) + i) % 4
        opts_zh = [f"其他關於《{name_zh}》嘅資訊A", f"其他關於《{name_zh}》嘅資訊B", f"其他關於《{name_zh}》嘅資訊C"]
        opts_en = [f"Other fact about '{name_en}' A", f"Other fact about '{name_en}' B", f"Other fact about '{name_en}' C"]
        opts_zh.insert(ans_pos, fact_zh)
        opts_en.insert(ans_pos, fact_en)
        
        templates.append({
            "q_zh": f"以下邊個關於《{name_zh}》嘅講法係正確？",
            "q_en": f"Which of the following about '{name_en}' is correct?",
            "o_zh": opts_zh,
            "o_en": opts_en,
            "ans": ans_pos,
            "e_zh": fact_zh,
            "e_en": fact_en,
        })
    
    return templates


def _novel_templates(info):
    """Generate novel question templates."""
    templates = []
    name_zh = info["zh_name"]
    name_en = info["en_name"]
    author_zh = info.get("author", {}).get("zh", "")
    author_en = info.get("author", {}).get("en", "")
    genre_zh = info.get("genre", {}).get("zh", "")
    genre_en = info.get("genre", {}).get("en", "")
    year = info.get("year", "")
    
    if author_zh:
        templates.append({
            "q_zh": f"《{name_zh}》嘅作者係邊個？",
            "q_en": f"Who is the author of '{name_en}'?",
            "o_zh": [author_zh, "金庸", "魯迅", "莫言"],
            "o_en": [author_en, "Jin Yong", "Lu Xun", "Mo Yan"],
            "ans": 0,
            "e_zh": f"《{name_zh}》嘅作者係{author_zh}。",
            "e_en": f"The author of '{name_en}' is {author_en}.",
        })
    
    if genre_zh:
        templates.append({
            "q_zh": f"《{name_zh}》屬於咩類型？",
            "q_en": f"What genre is '{name_en}'?",
            "o_zh": [genre_zh, "科幻", "恐怖", "推理"],
            "o_en": [genre_en, "Sci-Fi", "Horror", "Mystery"],
            "ans": 0,
            "e_zh": f"《{name_zh}》係{genre_zh}類型。",
            "e_en": f"'{name_en}' is a {genre_en}.",
        })
    
    if year:
        templates.append({
            "q_zh": f"《{name_zh}》喺邊一年出版？",
            "q_en": f"In which year was '{name_en}' published?",
            "o_zh": [year, str(int(year)-10), str(int(year)+5), str(int(year)-20)],
            "o_en": [year, str(int(year)-10), str(int(year)+5), str(int(year)-20)],
            "ans": 0,
            "e_zh": f"《{name_zh}》喺{year}年出版。",
            "e_en": f"'{name_en}' was published in {year}.",
        })
    
    # Add fact-based questions
    for i, fact in enumerate(info.get("facts", [])):
        fact_zh = fact["zh"]
        fact_en = fact["en"]
        ans_pos = (len(templates) + i) % 4
        opts_zh = [f"其他關於《{name_zh}》嘅資訊A", f"其他關於《{name_zh}》嘅資訊B", f"其他關於《{name_zh}》嘅資訊C"]
        opts_en = [f"Other fact about '{name_en}' A", f"Other fact about '{name_en}' B", f"Other fact about '{name_en}' C"]
        opts_zh.insert(ans_pos, fact_zh)
        opts_en.insert(ans_pos, fact_en)
        
        templates.append({
            "q_zh": f"以下邊個關於《{name_zh}》嘅講法係正確？",
            "q_en": f"Which of the following about '{name_en}' is correct?",
            "o_zh": opts_zh,
            "o_en": opts_en,
            "ans": ans_pos,
            "e_zh": fact_zh,
            "e_en": fact_en,
        })
    
    return templates


def _tv_templates(info):
    """Generate TV show question templates."""
    templates = []
    name_zh = info["zh_name"]
    name_en = info["en_name"]
    genre_zh = info.get("genre", {}).get("zh", "")
    genre_en = info.get("genre", {}).get("en", "")
    year = info.get("year", "")
    network_zh = info.get("network", {}).get("zh", "")
    network_en = info.get("network", {}).get("en", "")
    
    if genre_zh:
        templates.append({
            "q_zh": f"《{name_zh}》屬於咩類型嘅劇集？",
            "q_en": f"What genre is '{name_en}'?",
            "o_zh": [genre_zh, "紀錄片", "動畫", "新聞"],
            "o_en": [genre_en, "Documentary", "Animation", "News"],
            "ans": 0,
            "e_zh": f"《{name_zh}》係{genre_zh}劇集。",
            "e_en": f"'{name_en}' is a {genre_en} drama.",
        })
    
    if year:
        templates.append({
            "q_zh": f"《{name_zh}》喺邊一年首播？",
            "q_en": f"In which year did '{name_en}' first air?",
            "o_zh": [year, str(int(year)-3), str(int(year)+2), str(int(year)-7)],
            "o_en": [year, str(int(year)-3), str(int(year)+2), str(int(year)-7)],
            "ans": 0,
            "e_zh": f"《{name_zh}》喺{year}年首播。",
            "e_en": f"'{name_en}' first aired in {year}.",
        })
    
    if network_zh:
        templates.append({
            "q_zh": f"《{name_zh}》喺邊個電視台播出？",
            "q_en": f"Which network aired '{name_en}'?",
            "o_zh": [network_zh, "央視", "湖南衛視", "浙江衛視"],
            "o_en": [network_en, "CCTV", "Hunan TV", "Zhejiang TV"],
            "ans": 0,
            "e_zh": f"《{name_zh}》喺{network_zh}播出。",
            "e_en": f"'{name_en}' aired on {network_en}.",
        })
    
    # Add fact-based questions
    for i, fact in enumerate(info.get("facts", [])):
        fact_zh = fact["zh"]
        fact_en = fact["en"]
        ans_pos = (len(templates) + i) % 4
        opts_zh = [f"其他關於《{name_zh}》嘅資訊A", f"其他關於《{name_zh}》嘅資訊B", f"其他關於《{name_zh}》嘅資訊C"]
        opts_en = [f"Other fact about '{name_en}' A", f"Other fact about '{name_en}' B", f"Other fact about '{name_en}' C"]
        opts_zh.insert(ans_pos, fact_zh)
        opts_en.insert(ans_pos, fact_en)
        
        templates.append({
            "q_zh": f"以下邊個關於《{name_zh}》嘅講法係正確？",
            "q_en": f"Which of the following about '{name_en}' is correct?",
            "o_zh": opts_zh,
            "o_en": opts_en,
            "ans": ans_pos,
            "e_zh": fact_zh,
            "e_en": fact_en,
        })
    
    return templates


# ============================================================
# MASSIVE KNOWLEDGE BASES (inline)
# ============================================================

# This will be populated by the separate knowledge base files
# For now, we load them from companion files

def load_knowledge_base(category):
    """Load knowledge base for a category."""
    kb_path = os.path.join(BASE_DIR, f"kb_{category}.json")
    if os.path.exists(kb_path):
        with open(kb_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def process_category(category, kb):
    """Process all items in a category."""
    base_path = os.path.join(BASE_DIR, category)
    results = {"processed": 0, "questions_added": 0, "errors": []}
    
    for root, dirs, files in os.walk(base_path):
        for filename in files:
            if not filename.endswith('.json') or filename == 'index.json':
                continue
            
            filepath = os.path.join(root, filename)
            rel_path = os.path.relpath(filepath, BASE_DIR)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    existing = json.load(f)
                
                if not isinstance(existing, list):
                    continue
                
                current_count = len(existing)
                if current_count >= 100:
                    continue
                
                # Extract topic key from path
                # e.g., gaming/pc/dota_2/questions.json -> dota_2
                parts = rel_path.replace('.json', '').split(os.sep)
                if category == "gaming":
                    topic_key = parts[-2] if len(parts) >= 2 else parts[-1]
                elif category == "travel":
                    topic_key = parts[-2] if len(parts) >= 2 else parts[-1]
                elif category == "anime":
                    topic_key = parts[-2] if len(parts) >= 2 else parts[-1]
                elif category == "novel":
                    topic_key = parts[-1].replace('.json', '')
                elif category == "tv":
                    topic_key = parts[-1].replace('.json', '')
                else:
                    topic_key = parts[-1].replace('.json', '')
                
                # Find knowledge base entry
                topic_info = kb.get(topic_key, None)
                if topic_info is None:
                    # Try to find by name matching
                    for k, v in kb.items():
                        if k in rel_path or v.get("zh_name", "") in str(existing[0].get("question_zh", "")):
                            topic_info = v
                            topic_key = k
                            break
                
                if topic_info is None:
                    results["errors"].append(f"No KB entry for {rel_path} (key: {topic_key})")
                    continue
                
                # Generate questions
                needed = 100 - current_count
                new_questions = generate_basic_questions(topic_info, category, current_count, 100)
                
                # Adjust IDs
                for i, q in enumerate(new_questions):
                    q["id"] = current_count + i + 1
                
                # Ensure answer distribution is even
                _balance_answers(new_questions)
                
                # Merge with existing
                all_questions = existing + new_questions
                
                # Write back
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(all_questions, f, indent=2, ensure_ascii=False)
                
                results["processed"] += 1
                results["questions_added"] += len(new_questions)
                
            except Exception as e:
                results["errors"].append(f"Error processing {rel_path}: {str(e)}")
    
    return results


def _balance_answers(questions):
    """Ensure answer distribution is roughly even (25% each)."""
    counts = [0, 0, 0, 0]
    for q in questions:
        counts[q["answer"]] += 1
    
    total = len(questions)
    if total == 0:
        return
    
    target = total / 4
    
    for q in questions:
        # Find the answer with highest count and swap with lowest
        max_idx = counts.index(max(counts))
        min_idx = counts.index(min(counts))
        
        if counts[q["answer"]] > target + 1 and counts[min_idx] < target - 1:
            old_ans = q["answer"]
            # Swap answer position
            q["options_zh"][old_ans], q["options_zh"][min_idx] = q["options_zh"][min_idx], q["options_zh"][old_ans]
            q["options_en"][old_ans], q["options_en"][min_idx] = q["options_en"][min_idx], q["options_en"][old_ans]
            q["answer"] = min_idx
            counts[old_ans] -= 1
            counts[min_idx] += 1


def check_uniqueness(questions):
    """Check for duplicate questions."""
    seen = set()
    duplicates = 0
    for q in questions:
        key = q["question_zh"]
        if key in seen:
            duplicates += 1
        seen.add(key)
    return duplicates


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    import sys
    
    categories = ["gaming", "travel", "anime", "novel", "tv"]
    
    if len(sys.argv) > 1:
        categories = sys.argv[1:]
    
    total_processed = 0
    total_added = 0
    total_errors = []
    
    for cat in categories:
        print(f"\n{'='*60}")
        print(f"Processing: {cat}")
        print(f"{'='*60}")
        
        kb = load_knowledge_base(cat)
        if not kb:
            print(f"  WARNING: No knowledge base found for {cat}")
            print(f"  Expected: kb_{cat}.json")
            continue
        
        print(f"  Knowledge base entries: {len(kb)}")
        
        result = process_category(cat, kb)
        
        print(f"  Items processed: {result['processed']}")
        print(f"  Questions added: {result['questions_added']}")
        if result['errors']:
            print(f"  Errors: {len(result['errors'])}")
            for err in result['errors'][:5]:
                print(f"    - {err}")
        
        total_processed += result['processed']
        total_added += result['questions_added']
        total_errors.extend(result['errors'])
    
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Total items processed: {total_processed}")
    print(f"Total questions added: {total_added}")
    print(f"Total errors: {len(total_errors)}")
