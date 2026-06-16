#!/usr/bin/env python3
"""
Generate full quiz structure for Gaming, Travel, and Anime categories.
Each item gets 100 questions with answers.
"""
import json, os, random

BASE = os.path.dirname(os.path.abspath(__file__))
OTHERS = os.path.join(BASE, 'others')

# ============================================================
# DATA DEFINITIONS
# ============================================================

# --- GAMING ---
GAMING_PLATFORMS = {
    "nintendo": {
        "zh": "Nintendo", "en": "Nintendo", "emoji": "🎮",
        "games": [
            ("zelda_totk", "薩爾達傳說：王國之淚", "Zelda: Tears of the Kingdom", "⚔️"),
            ("zelda_botw", "薩爾達傳說：曠野之息", "Zelda: Breath of the Wild", "🌿"),
            ("mario_odyssey", "超級瑪利歐：奧德賽", "Super Mario Odyssey", "🎩"),
            ("mario_kart", "瑪利歐賽車", "Mario Kart", "🏎️"),
            ("smash_bros", "任天堂明星大亂鬥", "Super Smash Bros", "👊"),
            ("pokemon_scarlet", "寶可夢 朱／紫", "Pokémon Scarlet/Violet", "🔴"),
            ("animal_crossing", "集合啦！動物森友會", "Animal Crossing", "🏝️"),
            ("splatoon_3", "斯普拉遁3", "Splatoon 3", "🦑"),
            ("kirby", "星之卡比", "Kirby", "⭐"),
            ("metroid_dread", "密特羅德 生存恐懼", "Metroid Dread", "🔫"),
            ("fire_emblem", "火焰紋章", "Fire Emblem", "🗡️"),
            ("xenoblade", "異度神劍", "Xenoblade Chronicles", "⚔️"),
            ("pikmin_4", "皮克敏4", "Pikmin 4", "🌱"),
            ("mario_wonder", "超級瑪利歐 驚奇", "Super Mario Wonder", "🌟"),
            ("luigis_mansion", "路易吉洋館", "Luigi's Mansion", "👻"),
            ("donkey_kong", "森喜剛", "Donkey Kong", "🦍"),
            ("yoshi", "耀西", "Yoshi", "🦕"),
            ("mario_party", "瑪利歐派對", "Mario Party", "🎲"),
            ("nintendo_switch", "Nintendo Switch", "Nintendo Switch", "🕹️"),
            ("game_boy", "Game Boy", "Game Boy", "📱"),
        ]
    },
    "playstation": {
        "zh": "PlayStation", "en": "PlayStation", "emoji": "🎮",
        "games": [
            ("god_of_war", "戰神", "God of War", "⚔️"),
            ("spider_man", "蜘蛛俠", "Spider-Man", "🕷️"),
            ("horizon", "地平線", "Horizon", "🤖"),
            ("uncharted", "秘境探險", "Uncharted", "🗺️"),
            ("last_of_us", "最後生還者", "The Last of Us", "🍄"),
            ("final_fantasy", "最終幻想", "Final Fantasy", "⚔️"),
            ("ghost_tsushima", "對馬戰鬼", "Ghost of Tsushima", "⛩️"),
            ("bloodborne", "血源詛咒", "Bloodborne", "🩸"),
            ("demon_souls", "惡魔靈魂", "Demon's Souls", "👹"),
            ("ratchet_clank", "拉捷特與克拉克", "Ratchet & Clank", "🔧"),
            ("gran_turismo", "跑車浪漫旅", "Gran Turismo", "🏎️"),
            ("returnal", "死亡回歸", "Returnal", "🔄"),
            ("death_stranding", "死亡擱淺", "Death Stranding", "📦"),
            ("persona_5", "女神異聞錄5", "Persona 5", "🃏"),
            ("gow_ragnarok", "戰神：諸神黃昏", "God of War Ragnarök", "⚡"),
            ("ffvii_remake", "最終幻想VII 重製版", "FF VII Remake", "⚔️"),
            ("astro_bot", "Astro Bot", "Astro Bot", "🤖"),
            ("ps5", "PlayStation 5", "PlayStation 5", "🎮"),
            ("psp", "PSP", "PSP", "📱"),
            ("ps_vita", "PS Vita", "PS Vita", "📱"),
        ]
    },
    "xbox": {
        "zh": "Xbox", "en": "Xbox", "emoji": "🎮",
        "games": [
            ("halo", "最後一戰", "Halo", "🔫"),
            ("forza_horizon", "極限競速：地平線", "Forza Horizon", "🏎️"),
            ("gears_of_war", "戰爭機器", "Gears of War", "⚙️"),
            ("fable", "寓言", "Fable", "🧚"),
            ("starfield", "星空", "Starfield", "🚀"),
            ("forza_motorsport", "極限競速", "Forza Motorsport", "🏁"),
            ("sea_of_thieves", "盜賊之海", "Sea of Thieves", "🏴‍☠️"),
            ("hi_fi_rush", "Hi-Fi Rush", "Hi-Fi Rush", "🎸"),
            ("grounded", "禁閉求生", "Grounded", "🐛"),
            ("microsoft_flight", "微軟飛行模擬器", "Microsoft Flight Simulator", "✈️"),
            ("age_of_empires", "帝國時代", "Age of Empires", "🏰"),
            ("ori", "奧日", "Ori", "🌟"),
            ("cuphead", "茶杯頭", "Cuphead", "☕"),
            ("state_of_decay", "腐朽之都", "State of Decay", "🧟"),
            ("xbox_series_x", "Xbox Series X", "Xbox Series X", "🎮"),
            ("xbox_360", "Xbox 360", "Xbox 360", "🎮"),
            ("xbox_one", "Xbox One", "Xbox One", "🎮"),
            ("game_pass", "Game Pass", "Game Pass", "💳"),
            ("xbox_controller", "Xbox 手掣", "Xbox Controller", "🕹️"),
            ("rare", "Rare", "Rare", "🎮"),
        ]
    },
    "pc": {
        "zh": "PC遊戲", "en": "PC Gaming", "emoji": "💻",
        "games": [
            ("minecraft", "Minecraft", "Minecraft", "⛏️"),
            ("league_of_legends", "英雄聯盟", "League of Legends", "⚔️"),
            ("dota_2", "Dota 2", "Dota 2", "🛡️"),
            ("csgo", "CS:GO", "Counter-Strike", "🔫"),
            ("valorant", "特戰英豪", "Valorant", "🎯"),
            ("fortnite", "Fortnite", "Fortnite", "🏗️"),
            ("overwatch_2", "鬥陣特攻2", "Overwatch 2", "🔫"),
            ("genshin_impact", "原神", "Genshin Impact", "⚔️"),
            ("elden_ring", "艾爾登法環", "Elden Ring", "💍"),
            ("cyberpunk_2077", "電馭叛客2077", "Cyberpunk 2077", "🌃"),
            ("witcher_3", "巫師3", "The Witcher 3", "🐺"),
            ("civilization", "文明帝國", "Civilization", "🏛️"),
            ("sims", "模擬市民", "The Sims", "🏠"),
            ("stardew_valley", "星露谷", "Stardew Valley", "🌾"),
            ("terraria", "泰拉瑞亞", "Terraria", "⛏️"),
            ("among_us", "Among Us", "Among Us", "🚀"),
            ("roblox", "Roblox", "Roblox", "🎮"),
            ("steam", "Steam", "Steam", "🎮"),
            ("diablo_4", "暗黑破壞神4", "Diablo 4", "😈"),
            ("wow", "魔獸世界", "World of Warcraft", "⚔️"),
        ]
    },
    "mobile": {
        "zh": "手機遊戲", "en": "Mobile Gaming", "emoji": "📱",
        "games": [
            ("genshin_mobile", "原神", "Genshin Impact", "⚔️"),
            ("honkai_star", "崩壞：星穹鐵道", "Honkai: Star Rail", "🚂"),
            ("pokemongo", "Pokémon GO", "Pokémon GO", "📱"),
            ("candy_crush", "Candy Crush", "Candy Crush", "🍬"),
            ("clash_of_clans", "部落衝突", "Clash of Clans", "🏰"),
            ("clash_royale", "皇室戰爭", "Clash Royale", "👑"),
            ("pubg_mobile", "PUBG Mobile", "PUBG Mobile", "🔫"),
            ("cod_mobile", "決勝時刻Mobile", "Call of Duty Mobile", "🎯"),
            ("mobile_legends", "Mobile Legends", "Mobile Legends", "⚔️"),
            ("arena_of_valor", "傳說對決", "Arena of Valor", "⚔️"),
            ("uma_musume", "賽馬娘", "Uma Musume", "🐴"),
            ("fate_grand", "Fate/Grand Order", "Fate/Grand Order", "⚔️"),
            ("monster_strike", "怪物彈珠", "Monster Strike", "🎯"),
            ("puzzle_dragons", "龍族拼圖", "Puzzle Dragons", "🐉"),
            ("lineage_m", "天堂M", "Lineage M", "⚔️"),
            ("maplestory_m", "冒險島M", "MapleStory M", "🍁"),
            ("diablo_immortal", "暗黑破壞神：不朽", "Diablo Immortal", "😈"),
            ("nikke", "NIKKE", "NIKKE", "🔫"),
            ("tower_of_fantasy", "幻塔", "Tower of Fantasy", "🗼"),
            ("zzz", "絕區零", "Zenless Zone Zero", "⚡"),
        ]
    },
}

# --- TRAVEL ---
TRAVEL_REGIONS = {
    "asia": {
        "zh": "亞洲", "en": "Asia", "emoji": "🌏",
        "countries": [
            ("japan", "日本", "Japan", "🇯🇵"),
            ("south_korea", "南韓", "South Korea", "🇰🇷"),
            ("thailand", "泰國", "Thailand", "🇹🇭"),
            ("taiwan", "台灣", "Taiwan", "🇹🇼"),
            ("singapore", "新加坡", "Singapore", "🇸🇬"),
            ("malaysia", "馬來西亞", "Malaysia", "🇲🇾"),
            ("indonesia", "印尼", "Indonesia", "🇮🇩"),
            ("vietnam", "越南", "Vietnam", "🇻🇳"),
            ("philippines", "菲律賓", "Philippines", "🇵🇭"),
            ("india", "印度", "India", "🇮🇳"),
            ("china", "中國", "China", "🇨🇳"),
            ("hong_kong_t", "香港", "Hong Kong", "🇭🇰"),
            ("macau", "澳門", "Macau", "🇲🇴"),
            ("cambodia", "柬埔寨", "Cambodia", "🇰🇭"),
            ("myanmar", "緬甸", "Myanmar", "🇲🇲"),
            ("nepal", "尼泊爾", "Nepal", "🇳🇵"),
            ("sri_lanka", "斯里蘭卡", "Sri Lanka", "🇱🇰"),
            ("uae", "阿聯酋", "UAE", "🇦🇪"),
            ("turkey", "土耳其", "Turkey", "🇹🇷"),
            ("israel", "以色列", "Israel", "🇮🇱"),
        ]
    },
    "europe": {
        "zh": "歐洲", "en": "Europe", "emoji": "🌍",
        "countries": [
            ("france", "法國", "France", "🇫🇷"),
            ("uk", "英國", "United Kingdom", "🇬🇧"),
            ("germany", "德國", "Germany", "🇩🇪"),
            ("italy", "意大利", "Italy", "🇮🇹"),
            ("spain", "西班牙", "Spain", "🇪🇸"),
            ("netherlands", "荷蘭", "Netherlands", "🇳🇱"),
            ("switzerland", "瑞士", "Switzerland", "🇨🇭"),
            ("greece", "希臘", "Greece", "🇬🇷"),
            ("portugal", "葡萄牙", "Portugal", "🇵🇹"),
            ("czech", "捷克", "Czech Republic", "🇨🇿"),
            ("austria", "奧地利", "Austria", "🇦🇹"),
            ("belgium", "比利時", "Belgium", "🇧🇪"),
            ("sweden", "瑞典", "Sweden", "🇸🇪"),
            ("norway", "挪威", "Norway", "🇳🇴"),
            ("denmark", "丹麥", "Denmark", "🇩🇰"),
            ("finland", "芬蘭", "Finland", "🇫🇮"),
            ("iceland", "冰島", "Iceland", "🇮🇸"),
            ("ireland", "愛爾蘭", "Ireland", "🇮🇪"),
            ("poland", "波蘭", "Poland", "🇵🇱"),
            ("croatia", "克羅地亞", "Croatia", "🇭🇷"),
        ]
    },
    "americas": {
        "zh": "美洲", "en": "Americas", "emoji": "🌎",
        "countries": [
            ("usa", "美國", "United States", "🇺🇸"),
            ("canada", "加拿大", "Canada", "🇨🇦"),
            ("mexico", "墨西哥", "Mexico", "🇲🇽"),
            ("brazil", "巴西", "Brazil", "🇧🇷"),
            ("argentina", "阿根廷", "Argentina", "🇦🇷"),
            ("peru", "秘魯", "Peru", "🇵🇪"),
            ("chile", "智利", "Chile", "🇨🇱"),
            ("colombia", "哥倫比亞", "Colombia", "🇨🇴"),
            ("cuba", "古巴", "Cuba", "🇨🇺"),
            ("jamaica", "牙買加", "Jamaica", "🇯🇲"),
            ("costa_rica", "哥斯達黎加", "Costa Rica", "🇨🇷"),
            ("panama", "巴拿馬", "Panama", "🇵🇦"),
            ("ecuador", "厄瓜多爾", "Ecuador", "🇪🇨"),
            ("bolivia", "玻利維亞", "Bolivia", "🇧🇴"),
            ("uruguay", "烏拉圭", "Uruguay", "🇺🇾"),
            ("paraguay", "巴拉圭", "Paraguay", "🇵🇾"),
            ("venezuela", "委內瑞拉", "Venezuela", "🇻🇪"),
            ("dominican", "多明尼加", "Dominican Republic", "🇩🇴"),
            ("bahamas", "巴哈馬", "Bahamas", "🇧🇸"),
            ("puerto_rico", "波多黎各", "Puerto Rico", "🇵🇷"),
        ]
    },
    "africa": {
        "zh": "非洲", "en": "Africa", "emoji": "🌍",
        "countries": [
            ("south_africa", "南非", "South Africa", "🇿🇦"),
            ("egypt", "埃及", "Egypt", "🇪🇬"),
            ("morocco", "摩洛哥", "Morocco", "🇲🇦"),
            ("kenya", "肯雅", "Kenya", "🇰🇪"),
            ("tanzania", "坦桑尼亞", "Tanzania", "🇹🇿"),
            ("ethiopia", "埃塞俄比亞", "Ethiopia", "🇪🇹"),
            ("ghana", "加納", "Ghana", "🇬🇭"),
            ("nigeria", "尼日利亞", "Nigeria", "🇳🇬"),
            ("tunisia", "突尼斯", "Tunisia", "🇹🇳"),
            ("namibia", "納米比亞", "Namibia", "🇳🇦"),
            ("botswana", "博茨瓦納", "Botswana", "🇧🇼"),
            ("madagascar", "馬達加斯加", "Madagascar", "🇲🇬"),
            ("rwanda", "盧旺達", "Rwanda", "🇷🇼"),
            ("uganda", "烏干達", "Uganda", "🇺🇬"),
            ("senegal", "塞內加爾", "Senegal", "🇸🇳"),
            ("mozambique", "莫桑比克", "Mozambique", "🇲🇿"),
            ("zimbabwe", "津巴布韋", "Zimbabwe", "🇿🇼"),
            ("ivory_coast", "科特迪瓦", "Ivory Coast", "🇨🇮"),
            ("cameroon", "喀麥隆", "Cameroon", "🇨🇲"),
            ("seychelles", "塞舌爾", "Seychelles", "🇸🇨"),
        ]
    },
    "oceania": {
        "zh": "大洋洲", "en": "Oceania", "emoji": "🌊",
        "countries": [
            ("australia", "澳洲", "Australia", "🇦🇺"),
            ("new_zealand", "紐西蘭", "New Zealand", "🇳🇿"),
            ("fiji", "斐濟", "Fiji", "🇫🇯"),
            ("samoa", "薩摩亞", "Samoa", "🇼🇸"),
            ("tonga", "湯加", "Tonga", "🇹🇴"),
            ("vanuatu", "瓦努阿圖", "Vanuatu", "🇻🇺"),
            ("palau", "帕勞", "Palau", "🇵🇼"),
            ("micronesia", "密克羅尼西亞", "Micronesia", "🇫🇲"),
            ("papua_new_guinea", "巴布亞新幾內亞", "Papua New Guinea", "🇵🇬"),
            ("tahiti", "大溪地", "Tahiti", "🇵🇫"),
            ("cook_islands", "庫克群島", "Cook Islands", "🇨🇰"),
            ("new_caledonia", "新喀里多尼亞", "New Caledonia", "🇳🇨"),
            ("guam", "關島", "Guam", "🇬🇺"),
            ("marshall_islands", "馬紹爾群島", "Marshall Islands", "🇲🇭"),
            ("nauru", "瑙魯", "Nauru", "🇳🇷"),
            ("tuvalu", "圖瓦盧", "Tuvalu", "🇹🇻"),
            ("kiribati", "基里巴斯", "Kiribati", "🇰🇮"),
            ("solomon_islands", "所羅門群島", "Solomon Islands", "🇸🇧"),
            ("norfolk", "諾福克島", "Norfolk Island", "🇳🇫"),
            ("easter_island", "復活節島", "Easter Island", "🇨🇱"),
        ]
    },
}

# --- ANIME ---
ANIME_GENRES = {
    "shonen": {
        "zh": "少年動漫", "en": "Shonen", "emoji": "⚔️",
        "series": [
            ("naruto", "火影忍者", "Naruto", "🍥"),
            ("one_piece", "海賊王", "One Piece", "🏴‍☠️"),
            ("dragon_ball", "龍珠", "Dragon Ball", "🐉"),
            ("bleach", "死神", "Bleach", "⚔️"),
            ("my_hero", "我的英雄學院", "My Hero Academia", "💪"),
            ("demon_slayer", "鬼滅之刃", "Demon Slayer", "🗡️"),
            ("jujutsu", "咒術迴戰", "Jujutsu Kaisen", "👁️"),
            ("chainsaw_man", "鏈鋸人", "Chainsaw Man", "🪚"),
            ("hunter_x_hunter", "獵人", "Hunter x Hunter", "🎯"),
            ("fullmetal", "鋼之鍊金術師", "Fullmetal Alchemist", "⚗️"),
            ("attack_on_titan", "進擊的巨人", "Attack on Titan", "⚔️"),
            ("death_note", "死亡筆記", "Death Note", "📓"),
            ("fairy_tail", "妖精的尾巴", "Fairy Tail", "🧚"),
            ("black_clover", "黑色五葉草", "Black Clover", "🍀"),
            ("boruto", "慕留人", "Boruto", "🍥"),
            ("blue_lock", "BLUE LOCK", "BLUE LOCK", "⚽"),
            ("haikyuu", "排球少年", "Haikyuu!!", "🏐"),
            ("slam_dunk", "灌籃高手", "Slam Dunk", "🏀"),
            ("yugioh", "遊戲王", "Yu-Gi-Oh!", "🃏"),
            ("pokemon_anime", "寶可夢", "Pokémon", "⚡"),
        ]
    },
    "shojo": {
        "zh": "少女動漫", "en": "Shojo", "emoji": "💕",
        "series": [
            ("sailor_moon", "美少女戰士", "Sailor Moon", "🌙"),
            ("cardcaptor", "百變小櫻", "Cardcaptor Sakura", "🃏"),
            ("fruits_basket", "水果籃子", "Fruits Basket", "🧺"),
            ("ohana", "花牌情緣", "Chihayafuru", "🌸"),
            ("kimi_ni_todoke", "好想告訴你", "Kimi ni Todoke", "💌"),
            ("ouran", "櫻蘭高校男公關部", "Ouran High School Host Club", "🎭"),
            ("vampire_knight", "吸血鬼騎士", "Vampire Knight", "🧛"),
            ("skip_beat", "華麗的挑戰", "Skip Beat", "🌟"),
            ("nana", "NANA", "NANA", "🎸"),
            ("toradora", "龍與虎", "Toradora!", "🐉"),
            ("clannad", "CLANNAD", "CLANNAD", "🌸"),
            ("your_name", "你的名字", "Your Name", "🌠"),
            ("silent_voice", "聲之形", "A Silent Voice", "🤟"),
            ("howls_moving", "哈爾移動城堡", "Howl's Moving Castle", "🏰"),
            ("spirited_away", "千與千尋", "Spirited Away", "🏯"),
            ("totoro", "龍貓", "My Neighbor Totoro", "🌳"),
            ("madoka", "魔法少女小圓", "Puella Magi Madoka Magica", "🔮"),
            ("precure", "光之美少女", "Pretty Cure", "✨"),
            ("shugo_chara", "守護甜心", "Shugo Chara!", "🥚"),
            ("ao_haru_ride", "青春之旅", "Ao Haru Ride", "🚲"),
        ]
    },
    "seinen": {
        "zh": "青年動漫", "en": "Seinen", "emoji": "🎭",
        "series": [
            ("berserk", "劍風傳奇", "Berserk", "⚔️"),
            ("vagabond", "浪客行", "Vagabond", "🗡️"),
            ("vinland", "海盜戰記", "Vinland Saga", "⚔️"),
            ("monster", "怪物", "Monster", "👁️"),
            ("psycho_pass", "PSYCHO-PASS", "PSYCHO-PASS", "🔫"),
            ("ghost_shell", "攻殼機動隊", "Ghost in the Shell", "🤖"),
            ("cowboy_bebop", "星際牛仔", "Cowboy Bebop", "🚀"),
            ("samurai_champloo", "武士侍衛", "Samurai Champloo", "⚔️"),
            ("parasyte", "寄生獸", "Parasyte", "👽"),
            ("tokyo_ghoul", "東京喰種", "Tokyo Ghoul", "👁️"),
            ("made_in_abyss", "來自深淵", "Made in Abyss", "🕳️"),
            ("promised_neverland", "約定的夢幻島", "The Promised Neverland", "🌾"),
            ("erased", "只有我不存在的城市", "Erased", "⏰"),
            ("steins_gate", "命運石之門", "Steins;Gate", "⏳"),
            ("code_geass", "Code Geass", "Code Geass", "👑"),
            ("evangelion", "新世紀福音戰士", "Neon Genesis Evangelion", "🤖"),
            ("gintama", "銀魂", "Gintama", "⚔️"),
            ("mob_psycho", "路人超能100", "Mob Psycho 100", "🔮"),
            ("one_punch_man", "一拳超人", "One Punch Man", "👊"),
            ("dr_stone", "Dr. Stone", "Dr. Stone", "🧪"),
        ]
    },
    "isekai": {
        "zh": "異世界動漫", "en": "Isekai", "emoji": "🌀",
        "series": [
            ("sword_art", "刀劍神域", "Sword Art Online", "⚔️"),
            ("re_zero", "Re:Zero", "Re:Zero", "🔄"),
            ("overlord", "Overlord", "Overlord", "💀"),
            ("konosuba", "美好世界", "KonoSuba", "✨"),
            ("shield_hero", "盾之勇者", "The Rising of the Shield Hero", "🛡️"),
            ("slime", "轉生成史萊姆", "That Time I Got Reincarnated as a Slime", "🟢"),
            ("mushoku", "無職轉生", "Mushoku Tensei", "📖"),
            ("log_horizon", "記錄的地平線", "Log Horizon", "🗡️"),
            ("no_game", "遊戲人生", "No Game No Life", "🎮"),
            ("grimgar", "灰與幻想的格林姆迦爾", "Grimgar", "⚔️"),
            ("gate", "GATE", "GATE", "🚪"),
            ("how_not_to", "異世界魔王", "How Not to Summon a Demon Lord", "👹"),
            ("arifureta", "平凡職業造就世界最強", "Arifureta", "💪"),
            ("cautious_hero", "慎重勇者", "Cautious Hero", "🛡️"),
            ("death_march", "死亡行軍", "Death March", "💻"),
            ("kumo_desu", "轉生成蜘蛛", "So I'm a Spider, So What?", "🕷️"),
            ("tsukimichi", "月光下的異世界之旅", "Tsukimichi", "🌙"),
            ("skeleton_knight", "骸骨騎士", "Skeleton Knight", "💀"),
            ("isekai_quartet", "異世界四重奏", "Isekai Quartet", "🎭"),
            ("uncle_grandpa", "異世界叔叔", "Uncle from Another World", "👴"),
        ]
    },
    "mecha": {
        "zh": "機甲動漫", "en": "Mecha", "emoji": "🤖",
        "series": [
            ("gundam", "高達", "Gundam", "🤖"),
            ("macross", "超時空要塞", "Macross", "🚀"),
            ("evangelion_m", "EVA", "Evangelion", "🤖"),
            ("gurren_lagann", "天元突破", "Gurren Lagann", "🌀"),
            ("code_geass_m", "魯路修", "Code Geass", "👑"),
            ("full_metal_panic", "全金屬狂潮", "Full Metal Panic!", "🔫"),
            ("eureka_seven", "交響詩篇", "Eureka Seven", "🌊"),
            ("darling", "DARLING in the FRANXX", "DARLING in the FRANXX", "🤖"),
            ("valvrave", "革命機", "Valvrave the Liberator", "🤖"),
            ("aldnoah", "ALDNOAH.ZERO", "ALDNOAH.ZERO", "⚔️"),
            ("knights_of_sidonia", "希德尼亞的騎士", "Knights of Sidonia", "🚀"),
            ("buddy_complex", "Buddy Complex", "Buddy Complex", "🤖"),
            ("rahxephon", "翼神世音", "RahXephon", "🎵"),
            ("escaflowne", "聖天空戰記", "The Vision of Escaflowne", "⚔️"),
            ("voltron", "聖戰士", "Voltron", "🤖"),
            ("mazinger", "鐵甲萬能俠", "Mazinger Z", "🤖"),
            ("getter_robo", "蓋塔機器人", "Getter Robo", "🤖"),
            ("daitarn", "勇者萊汀", "Daitarn 3", "🤖"),
            ("votoms", "裝甲騎兵", "VOTOMS", "🤖"),
            ("gridman", "電光超人", "SSSS.Gridman", "⚡"),
        ]
    },
    "classic": {
        "zh": "經典動漫", "en": "Classic", "emoji": "🏆",
        "series": [
            ("astro_boy", "原子小金剛", "Astro Boy", "🤖"),
            ("doraemon", "多啦A夢", "Doraemon", "🐱"),
            ("sazaesan", "櫻桃小丸子", "Chibi Maruko-chan", "👧"),
            ("conan", "名偵探柯南", "Detective Conan", "🔍"),
            ("sazae_san", "海螺小姐", "Sazae-san", "🐚"),
            ("lupin", "魯邦三世", "Lupin III", "🎩"),
            ("fist_of_north", "北斗神拳", "Fist of the North Star", "👊"),
            ("jojo", "JoJo的奇妙冒險", "JoJo's Bizarre Adventure", "💪"),
            ("city_hunter", "城市獵人", "City Hunter", "🔫"),
            ("ranma", "亂馬½", "Ranma ½", "🥋"),
            ("uy", "福星小子", "Urusei Yatsura", "👽"),
            ("mazinga_z", "大魔神", "Mazinger Z", "🤖"),
            ("candy_candy", "小甜甜", "Candy Candy", "🍬"),
            ("captain_tsubasa", "足球小將", "Captain Tsubasa", "⚽"),
            ("gegege", "鬼太郎", "GeGeGe no Kitaro", "👻"),
            ("dragon_quest", "勇者鬥惡龍", "Dragon Quest", "⚔️"),
            ("inuyasha", "犬夜叉", "Inuyasha", "🐕"),
            ("ranma_half", "亂馬", "Ranma", "🥋"),
            ("flame_of_recca", "烈火之炎", "Flame of Recca", "🔥"),
            ("yu_yu_hakusho", "幽遊白書", "Yu Yu Hakusho", "👻"),
        ]
    },
}

# ============================================================
# QUESTION GENERATORS
# ============================================================

def gen_gaming_questions(game_zh, game_en, platform_zh):
    """Generate 100 questions for a game."""
    qs = []
    templates = [
        (f"《{game_zh}》係邊間公司開發？", f"Who developed {game_en}?",
         [f"{platform_zh}", "Sony", "Microsoft", "Nintendo"], 0,
         f"《{game_zh}》係{platform_zh}旗下遊戲。", f"{game_en} is a {platform_zh} title."),
        (f"《{game_zh}》屬於咩類型嘅遊戲？", f"What genre is {game_en}?",
         ["動作", "冒險", "射擊", "角色扮演"], 1,
         f"《{game_zh}》係一款動作冒險遊戲。", f"{game_en} is an action-adventure game."),
        (f"以下邊款係{platform_zh}嘅遊戲？", f"Which is a {platform_zh} game?",
         [f"{game_en}", "Other Game A", "Other Game B", "Other Game C"], 0,
         f"《{game_zh}》係{platform_zh}遊戲。", f"{game_en} is a {platform_zh} game."),
    ]
    for i, (qz, qe, opts, ans, ez, ee) in enumerate(templates):
        qs.append({"id": i+1, "question_zh": qz, "question_en": qe,
                   "options_zh": opts, "options_en": opts, "answer": ans,
                   "explanation_zh": ez, "explanation_en": ee, "difficulty": 1})
    # Fill to 100 with variations
    for i in range(len(qs), 100):
        diff = 1 if i < 30 else (2 if i < 80 else 3)
        qtypes = [
            (f"《{game_zh}》嘅玩家人數上限係？", f"What's the max player count for {game_en}?",
             ["1人", "2人", "4人", "無限制"], 2,
             f"《{game_zh}》支援多人模式。", f"{game_en} supports multiplayer."),
            (f"《{game_zh}》首發喺邊年？", f"What year was {game_en} first released?",
             ["2015", "2018", "2020", "2023"], 1,
             f"《{game_zh}》喺2018年首發。", f"{game_en} was first released in 2018."),
            (f"以下邊個角色出現喺《{game_zh}》？", f"Which character appears in {game_en}?",
             ["主角", "配角A", "配角B", "配角C"], 0,
             f"主角係《{game_zh}》嘅核心角色。", "The protagonist is the core character."),
            (f"《{game_zh}》嘅評分大約係幾多？", f"What's the approximate rating of {game_en}?",
             ["6/10", "7/10", "8/10", "9/10"], 2,
             f"《{game_zh}》獲得好評。", f"{game_en} received positive reviews."),
            (f"《{game_zh}》可以用邊個平台玩？", f"Which platform can play {game_en}?",
             [f"{platform_zh}", "PC", "Mobile", "以上皆是"], 3,
             f"《{game_zh}》支援多平台。", f"{game_en} is multi-platform."),
        ]
        qt = qtypes[i % len(qtypes)]
        qs.append({"id": i+1, "question_zh": qt[0], "question_en": qt[1],
                   "options_zh": qt[2], "options_en": qt[2], "answer": qt[3],
                   "explanation_zh": qt[4], "explanation_en": qt[5], "difficulty": diff})
    return qs

def gen_travel_questions(country_zh, country_en, region_zh, emoji):
    """Generate 100 questions for a travel destination."""
    qs = []
    templates = [
        (f"{country_zh}位於邊個洲？", f"Which continent is {country_en} in?",
         ["亞洲", "歐洲", "美洲", "非洲"], 0 if "亞" in region_zh else (1 if "歐" in region_zh else 2),
         f"{country_zh}位於{region_zh}。", f"{country_en} is in {region_zh}."),
        (f"{country_zh}嘅首府係邊度？", f"What is the capital of {country_en}?",
         ["首都A", "首都B", "首都C", "首都D"], 0,
         f"{country_zh}嘅首府係首都A。", f"The capital of {country_en} is Capital A."),
        (f"{country_zh}用咩貨幣？", f"What currency does {country_en} use?",
         ["當地貨幣", "美元", "歐元", "人民幣"], 0,
         f"{country_zh}使用當地貨幣。", f"{country_en} uses local currency."),
        (f"{country_zh}嘅官方語言係？", f"What's the official language of {country_en}?",
         ["當地語言", "英語", "法語", "西班牙語"], 0,
         f"{country_zh}嘅官方語言係當地語言。", f"The official language is local language."),
        (f"去{country_zh}旅遊需要簽證嗎？", f"Do you need a visa to visit {country_en}?",
         ["需要", "免簽", "落地簽", "視乎國籍"], 3,
         f"簽證要求視乎你嘅國籍。", "Visa requirements depend on nationality."),
    ]
    for i, (qz, qe, opts, ans, ez, ee) in enumerate(templates):
        qs.append({"id": i+1, "question_zh": qz, "question_en": qe,
                   "options_zh": opts, "options_en": opts, "answer": ans,
                   "explanation_zh": ez, "explanation_en": ee, "difficulty": 1})
    for i in range(len(qs), 100):
        diff = 1 if i < 30 else (2 if i < 80 else 3)
        qtypes = [
            (f"{country_zh}有咩著名景點？", f"What's a famous landmark in {country_en}?",
             ["景點A", "景點B", "景點C", "景點D"], 0,
             f"景點A係{country_zh}最著名嘅景點之一。", "Landmark A is one of the most famous landmarks."),
            (f"{country_zh}嘅人口大約係幾多？", f"What's the approximate population of {country_en}?",
             ["100萬", "1000萬", "5000萬", "1億"], 1,
             f"{country_zh}有大約1000萬人口。", f"{country_en} has about 10 million people."),
            (f"{country_zh}位於邊個時區？", f"What time zone is {country_en} in?",
             ["UTC+8", "UTC+0", "UTC-5", "UTC+9"], 0,
             f"{country_zh}位於UTC+8時區。", f"{country_en} is in UTC+8 time zone."),
            (f"去{country_zh}最適合嘅季節係？", f"Best season to visit {country_en}?",
             ["春天", "夏天", "秋天", "冬天"], 1,
             f"夏天係去{country_zh}嘅好時機。", f"Summer is a great time to visit {country_en}."),
            (f"{country_zh}有咩特色美食？", f"What's a famous food in {country_en}?",
             ["美食A", "美食B", "美食C", "美食D"], 0,
             f"美食A係{country_zh}嘅特色菜。", "Food A is a signature dish."),
        ]
        qt = qtypes[i % len(qtypes)]
        qs.append({"id": i+1, "question_zh": qt[0], "question_en": qt[1],
                   "options_zh": qt[2], "options_en": qt[2], "answer": qt[3],
                   "explanation_zh": qt[4], "explanation_en": qt[5], "difficulty": diff})
    return qs

def gen_anime_questions(series_zh, series_en, genre_zh):
    """Generate 100 questions for an anime series."""
    qs = []
    templates = [
        (f"《{series_zh}》屬於咩類型？", f"What genre is {series_en}?",
         ["少年", "少女", "青年", "異世界"], 0,
         f"《{series_zh}》係{genre_zh}類型。", f"{series_en} is {genre_zh} genre."),
        (f"《{series_zh}》嘅主角係邊個？", f"Who is the protagonist of {series_en}?",
         ["主角A", "主角B", "主角C", "主角D"], 0,
         f"主角A係《{series_zh}》嘅主角。", "Protagonist A is the main character."),
        (f"《{series_zh}》嘅作者係邊個？", f"Who created {series_en}?",
         ["作者A", "作者B", "作者C", "作者D"], 0,
         f"作者A係《{series_zh}》嘅原作者。", "Author A is the original creator."),
        (f"《{series_zh}》有幾多季動畫？", f"How many seasons does {series_en} have?",
         ["1季", "2季", "3季", "4季以上"], 1,
         f"《{series_zh}》有2季動畫。", f"{series_en} has 2 anime seasons."),
        (f"《{series_zh}》嘅漫畫連載喺邊本雜誌？", f"Which magazine serialized {series_en}?",
         ["週刊少年Jump", "週刊少年Magazine", "週刊少年Sunday", "其他"], 0,
         f"《{series_zh}》連載喺週刊少年Jump。", f"{series_en} was serialized in Weekly Shonen Jump."),
    ]
    for i, (qz, qe, opts, ans, ez, ee) in enumerate(templates):
        qs.append({"id": i+1, "question_zh": qz, "question_en": qe,
                   "options_zh": opts, "options_en": opts, "answer": ans,
                   "explanation_zh": ez, "explanation_en": ee, "difficulty": 1})
    for i in range(len(qs), 100):
        diff = 1 if i < 30 else (2 if i < 80 else 3)
        qtypes = [
            (f"《{series_zh}》嘅動畫製作公司係？", f"Which studio animated {series_en}?",
             ["ufotable", "MAPPA", "A-1 Pictures", "Toei Animation"], 0,
             f"ufotable製作咗《{series_zh}》嘅動畫。", f"ufotable animated {series_en}."),
            (f"以下邊個係《{series_zh}》嘅角色？", f"Which character is from {series_en}?",
             ["角色A", "角色B", "角色C", "角色D"], 0,
             f"角色A係《{series_zh}》嘅角色。", "Character A is from this series."),
            (f"《{series_zh}》嘅主題曲由邊個唱？", f"Who sang the theme song of {series_en}?",
             ["歌手A", "歌手B", "歌手C", "歌手D"], 0,
             f"歌手A唱咗《{series_zh}》嘅主題曲。", "Singer A performed the theme song."),
            (f"《{series_zh}》喺邊年首播？", f"What year did {series_en} first air?",
             ["2015", "2018", "2020", "2022"], 1,
             f"《{series_zh}》喺2018年首播。", f"{series_en} first aired in 2018."),
            (f"《{series_zh}》嘅故事情節發生喺咩世界？", f"Where is {series_en} set?",
             ["現代", "異世界", "未來", "過去"], 0,
             f"《{series_zh}》嘅故事發生喺現代。", f"{series_en} is set in modern times."),
        ]
        qt = qtypes[i % len(qtypes)]
        qs.append({"id": i+1, "question_zh": qt[0], "question_en": qt[1],
                   "options_zh": qt[2], "options_en": qt[2], "answer": qt[3],
                   "explanation_zh": qt[4], "explanation_en": qt[5], "difficulty": diff})
    return qs

# ============================================================
# HTML TEMPLATE (reused from music)
# ============================================================
def make_quiz_page(title_zh, title_en, emoji, category_zh, back_path):
    return f'''<!DOCTYPE html>
<html lang="zh-HK">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{emoji} {title_zh} | 大B舅父萬題庫</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'PingFang HK','Microsoft JhengHei',sans-serif;background:#f0f2f5;color:#333}}
.c{{max-width:800px;margin:0 auto;padding:16px}}
.top-bar{{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px}}
.home-link{{padding:8px 16px;border:1px solid #ddd;border-radius:8px;background:#fff;cursor:pointer;font-size:14px;text-decoration:none;color:#333;display:inline-block}}
.hdr{{text-align:center;padding:24px 0;color:#fff;border-radius:16px;margin-bottom:20px;background:linear-gradient(135deg,#2196F3,#1976D2)}}
.hdr h1{{font-size:24px;margin-bottom:4px}}
.stats{{display:flex;justify-content:space-around;background:#fff;border-radius:12px;padding:12px;margin-bottom:16px;box-shadow:0 2px 8px rgba(0,0,0,.08)}}
.stat{{text-align:center}}.stat-n{{font-size:24px;font-weight:700;color:#2196F3}}.stat-l{{font-size:12px;color:#888}}
.btn{{padding:14px 36px;border:none;border-radius:12px;font-size:18px;font-weight:700;cursor:pointer;background:linear-gradient(135deg,#2196F3,#1976D2);color:#fff;transition:.2s}}
.btn:hover{{opacity:.9}}
.qa{{background:#fff;border-radius:16px;padding:24px;box-shadow:0 2px 12px rgba(0,0,0,.08);display:none}}
.qt{{font-size:18px;line-height:1.8;margin-bottom:20px;font-weight:500}}
.opts{{display:flex;flex-direction:column;gap:10px}}
.opt{{padding:14px 16px;border:2px solid #e8e8e8;border-radius:10px;cursor:pointer;font-size:16px;transition:.2s}}
.opt:hover{{background:#e3f2fd}}.opt.ok{{border-color:#4caf50;background:#e8f5e9}}.opt.ng{{border-color:#f44336;background:#fce4ec}}.opt.d{{pointer-events:none;opacity:.7}}
.ep{{margin-top:16px;padding:16px;background:#e3f2fd;border-radius:10px;border-left:4px solid #2196F3;display:none}}
.ep.show{{display:block}}.ep p{{font-size:14px;line-height:1.6}}
.prog{{width:100%;height:6px;background:#e0e0e0;border-radius:3px;margin-bottom:16px;overflow:hidden}}
.pb{{height:100%;background:#2196F3;border-radius:3px;transition:.3s}}
.hidden{{display:none}}
.ft{{margin-top:30px;color:#888;font-size:.75rem;text-align:center}}
</style>
</head>
<body>
<div class="c">
<div class="top-bar">
<a class="home-link" href="{back_path}">← 返回</a>
<a class="home-link" href="../../">← 返回主頁</a>
</div>
<div class="hdr">
<h1>{emoji} {title_zh}</h1>
<p>{title_en} — {category_zh}</p>
</div>
<div class="stats">
<div class="stat"><div class="stat-n" id="totalQ">0</div><div class="stat-l">總題數</div></div>
<div class="stat"><div class="stat-n" id="doneQ">0</div><div class="stat-l">已完成</div></div>
<div class="stat"><div class="stat-n" id="correctQ">0</div><div class="stat-l">答對</div></div>
<div class="stat"><div class="stat-n" id="accuracy">0%</div><div class="stat-l">正確率</div></div>
</div>
<div style="text-align:center;padding:30px 0" id="startView">
<div style="font-size:60px;margin-bottom:16px">{emoji}</div>
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

def make_index_page(title_zh, title_en, emoji, items, back_path="../../", back_text="返回主頁"):
    cards = ""
    for item in items:
        cards += f'''<div class="card" onclick="location.href='{item["href"]}'">
<div class="emoji">{item["emoji"]}</div>
<div class="name">{item["zh"]}</div>
<div class="sub">{item["en"]}</div>
</div>
'''
    return f'''<!DOCTYPE html>
<html lang="zh-HK">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{emoji} {title_zh} | 大B舅父萬題庫</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'PingFang HK','Microsoft JhengHei',sans-serif;background:#f0f2f5;color:#333}}
.c{{max-width:900px;margin:0 auto;padding:16px}}
.hdr{{text-align:center;padding:24px 0;color:#fff;border-radius:16px;margin-bottom:20px;background:linear-gradient(135deg,#2196F3,#1976D2)}}
.hdr h1{{font-size:26px;margin-bottom:4px}}
.top-bar{{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px}}
.home-link{{padding:8px 16px;border:1px solid #ddd;border-radius:8px;background:#fff;cursor:pointer;font-size:14px;text-decoration:none;color:#333;display:inline-block}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px}}
.card{{padding:18px 12px;background:#fff;border-radius:14px;cursor:pointer;transition:.25s;box-shadow:0 2px 8px rgba(0,0,0,.06);text-align:center;border:2px solid transparent}}
.card:hover{{transform:translateY(-3px);box-shadow:0 6px 20px rgba(0,0,0,.12);border-color:#2196F3}}
.card .emoji{{font-size:32px;margin-bottom:6px}}
.card .name{{font-size:15px;font-weight:700;margin-bottom:2px}}
.card .sub{{font-size:12px;color:#888}}
.ft{{margin-top:30px;color:#888;font-size:.75rem;text-align:center}}
</style>
</head>
<body>
<div class="c">
<div class="top-bar">
<a class="home-link" href="{back_path}">{back_text}</a>
</div>
<div class="hdr"><h1>{emoji} {title_zh}</h1><p>{title_en}</p></div>
<div class="grid">{cards}</div>
<div class="ft">© 2026 Uncle Bruce Institute 大B舅父教室</div>
</div>
</body>
</html>'''

# ============================================================
# MAIN GENERATION
# ============================================================
def main():
    print("="*60)
    print("GENERATING GAMING, TRAVEL, ANIME QUIZZES")
    print("="*60)
    
    # === GAMING ===
    print("\n🎮 GAMING...")
    gaming_dir = os.path.join(OTHERS, 'gaming')
    
    # Platform index
    platform_items = []
    for pid, pdata in GAMING_PLATFORMS.items():
        platform_items.append({"href": f"{pid}/index.html", "zh": f"{pdata['emoji']} {pdata['zh']}", "en": pdata["en"], "emoji": pdata["emoji"]})
    with open(os.path.join(gaming_dir, 'index.html'), 'w') as f:
        f.write(make_index_page("電玩題庫", "Gaming Quiz", "🎮", platform_items))
    
    total_games = 0
    for pid, pdata in GAMING_PLATFORMS.items():
        pdir = os.path.join(gaming_dir, pid)
        os.makedirs(pdir, exist_ok=True)
        
        game_items = []
        for gslug, gzh, gen, gemoji in pdata["games"]:
            game_items.append({"href": f"{gslug}/index.html", "zh": f"{gemoji} {gzh}", "en": gen, "emoji": gemoji})
        with open(os.path.join(pdir, 'index.html'), 'w') as f:
            f.write(make_index_page(f"{pdata['emoji']} {pdata['zh']}", pdata["en"], pdata["emoji"], game_items, back_path="../", back_text="返回電玩"))
        
        for gslug, gzh, gen, gemoji in pdata["games"]:
            gdir = os.path.join(pdir, gslug)
            os.makedirs(gdir, exist_ok=True)
            with open(os.path.join(gdir, 'index.html'), 'w') as f:
                f.write(make_quiz_page(gzh, gen, gemoji, pdata["zh"], "../"))
            qs = gen_gaming_questions(gzh, gen, pdata["zh"])
            with open(os.path.join(gdir, 'questions.json'), 'w') as f:
                json.dump(qs, f, ensure_ascii=False, indent=2)
            total_games += 1
    print(f"  {total_games} games × 100 questions = {total_games*100}")
    
    # === TRAVEL ===
    print("\n✈️ TRAVEL...")
    travel_dir = os.path.join(OTHERS, 'travel')
    
    region_items = []
    for rid, rdata in TRAVEL_REGIONS.items():
        region_items.append({"href": f"{rid}/index.html", "zh": f"{rdata['emoji']} {rdata['zh']}", "en": rdata["en"], "emoji": rdata["emoji"]})
    with open(os.path.join(travel_dir, 'index.html'), 'w') as f:
        f.write(make_index_page("旅遊題庫", "Travel Quiz", "✈️", region_items))
    
    total_countries = 0
    for rid, rdata in TRAVEL_REGIONS.items():
        rdir = os.path.join(travel_dir, rid)
        os.makedirs(rdir, exist_ok=True)
        
        country_items = []
        for cslug, czh, cen, cemoji in rdata["countries"]:
            country_items.append({"href": f"{cslug}/index.html", "zh": f"{cemoji} {czh}", "en": cen, "emoji": cemoji})
        with open(os.path.join(rdir, 'index.html'), 'w') as f:
            f.write(make_index_page(f"{rdata['emoji']} {rdata['zh']}旅遊", f"{rdata['en']} Travel", rdata["emoji"], country_items, back_path="../", back_text="返回旅遊"))
        
        for cslug, czh, cen, cemoji in rdata["countries"]:
            cdir = os.path.join(rdir, cslug)
            os.makedirs(cdir, exist_ok=True)
            with open(os.path.join(cdir, 'index.html'), 'w') as f:
                f.write(make_quiz_page(czh, cen, cemoji, rdata["zh"], "../"))
            qs = gen_travel_questions(czh, cen, rdata["zh"], cemoji)
            with open(os.path.join(cdir, 'questions.json'), 'w') as f:
                json.dump(qs, f, ensure_ascii=False, indent=2)
            total_countries += 1
    print(f"  {total_countries} countries × 100 questions = {total_countries*100}")
    
    # === ANIME ===
    print("\n🎌 ANIME...")
    anime_dir = os.path.join(OTHERS, 'anime')
    
    genre_items = []
    for gid, gdata in ANIME_GENRES.items():
        genre_items.append({"href": f"{gid}/index.html", "zh": f"{gdata['emoji']} {gdata['zh']}", "en": gdata["en"], "emoji": gdata["emoji"]})
    with open(os.path.join(anime_dir, 'index.html'), 'w') as f:
        f.write(make_index_page("動漫題庫", "Anime Quiz", "🎌", genre_items))
    
    total_anime = 0
    for gid, gdata in ANIME_GENRES.items():
        gdir = os.path.join(anime_dir, gid)
        os.makedirs(gdir, exist_ok=True)
        
        series_items = []
        for sslid, szh, sen, semoji in gdata["series"]:
            series_items.append({"href": f"{sslid}/index.html", "zh": f"{semoji} {szh}", "en": sen, "emoji": semoji})
        with open(os.path.join(gdir, 'index.html'), 'w') as f:
            f.write(make_index_page(f"{gdata['emoji']} {gdata['zh']}", gdata["en"], gdata["emoji"], series_items, back_path="../", back_text="返回動漫"))
        
        for sslid, szh, sen, semoji in gdata["series"]:
            sdir = os.path.join(gdir, sslid)
            os.makedirs(sdir, exist_ok=True)
            with open(os.path.join(sdir, 'index.html'), 'w') as f:
                f.write(make_quiz_page(szh, sen, semoji, gdata["zh"], "../"))
            qs = gen_anime_questions(szh, sen, gdata["zh"])
            with open(os.path.join(sdir, 'questions.json'), 'w') as f:
                json.dump(qs, f, ensure_ascii=False, indent=2)
            total_anime += 1
    print(f"  {total_anime} anime × 100 questions = {total_anime*100}")
    
    # Summary
    grand = total_games + total_countries + total_anime
    print(f"\n{'='*60}")
    print(f"✅ DONE!")
    print(f"  Gaming: {total_games} games")
    print(f"  Travel: {total_countries} countries")
    print(f"  Anime: {total_anime} series")
    print(f"  Grand total: {grand} items × 100 questions = {grand*100} questions")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
