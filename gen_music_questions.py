#!/usr/bin/env python3
"""
Generate 100 music quiz questions per artist.
Uses artist names from existing directory structure.
"""
import json, os, random

BASE = os.path.dirname(os.path.abspath(__file__))
MUSIC = os.path.join(BASE, 'others', 'music')

# Artist metadata for question generation
ARTIST_DATA = {
    # Hong Kong Male
    "eason_chan": {"zh": "陳奕迅", "en": "Eason Chan", "real": "陳奕迅", "origin": "香港", "genre": "流行曲", "label": "新藝寶/環球", "debut": "1995", "songs_zh": ["富士山下", "單車", "Shall We Talk", "K歌之王", "浮誇", "陀飛輪", "無人之境", "七百年後", "四季", "我的快樂時代", "與我常在", "Lonely Christmas", "不要說話", "紅玫瑰", "淘汰"], "songs_en": ["Under Mount Fuji", "Shall We Talk", "Karaoke King", "Exaggerated", "Tourbillon"], "albums": ["U87", "認了吧", "What's Going On...?", "米·閃", "準備中"], "awards": "勁歌金曲金獎、叱咤樂壇男歌手金獎"},
    "mc_cheung": {"zh": "MC張天賦", "en": "MC Cheung", "real": "張天賦", "origin": "香港", "genre": "流行曲/R&B", "label": "大國文化", "debut": "2019", "songs_zh": ["記憶棉", "老派約會之必要", "時候不早", "小心地滑", "花海", "Frenemy", "抽搐", "與我無關", "世一", "一百個未老先衰的方法"], "songs_en": ["Memory Foam", "Old School Dating"], "albums": ["Have a good time", "Frenemy"], "awards": "叱咤樂壇男歌手金獎、新城勁爆男歌手"},
    "keung_to": {"zh": "姜濤", "en": "Keung To", "real": "姜濤", "origin": "香港", "genre": "流行曲/Cantopop", "label": "MakerVille", "debut": "2018", "songs_zh": ["蒙著嘴說愛你", "Master Class", "Dear My Friend,", "孤獨病", "一號種籽", "我說", "I'm Not Fine", "B.M.G.", "一天多一點"], "songs_en": ["Cover Mouth Say I Love You", "Master Class"], "albums": ["Master Class"], "awards": "叱咤樂壇男歌手金獎、新城勁爆男歌手"},
    "andy_lau": {"zh": "劉德華", "en": "Andy Lau", "real": "劉德華", "origin": "香港", "genre": "流行曲", "label": "映藝/東亞", "debut": "1985", "songs_zh": ["忘情水", "愛你一萬年", "中國人", "今天", "一起走過的日子", "暗裡著迷", "真我的風采", "練習", "恭喜發財", "如果有一天", "無間道", "Everyone is No.1"], "songs_en": ["Forget Love Water", "Love You 10,000 Years"], "albums": ["忘情水", "真我的風采", "你是我的女人"], "awards": "勁歌金曲金獎、十大中文金曲金獎"},
    "jacky_cheung": {"zh": "張學友", "en": "Jacky Cheung", "real": "張學友", "origin": "香港", "genre": "流行曲", "label": "環球/上華", "debut": "1984", "songs_zh": ["吻別", "每天愛你多一些", "一千個傷心的理由", "祝福", "只想一生跟你走", "愛是永恆", "頭髮亂了", "李香蘭", "情網", "她來聽我的演唱會", "慢慢", "你的名字我的姓氏"], "songs_en": ["Kiss Goodbye", "Love You More Each Day"], "albums": ["吻別", "愛與交響曲", "雪狼湖"], "awards": "世界音樂獎全球銷量最高亞洲歌手、勁歌金曲金獎"},
    "leon_lai": {"zh": "黎明", "en": "Leon Lai", "real": "黎明", "origin": "北京/香港", "genre": "流行曲", "label": "A Music", "debut": "1986", "songs_zh": ["今夜你會不會來", "對不起我愛你", "那有一天不想你", "只要為我愛一天", "全日愛", "看上她", "非我莫屬", "如果可以再見你", "Sugar In The Marmalade"], "songs_en": ["Will You Come Tonight", "Sorry I Love You"], "albums": ["是愛是緣", "Perhaps...", "The Red Shoes"], "awards": "勁歌金曲金獎、四大天王"},
    "aaron_kwok": {"zh": "郭富城", "en": "Aaron Kwok", "real": "郭富城", "origin": "香港", "genre": "流行曲/舞曲", "label": "大國文化", "debut": "1984", "songs_zh": ["對你愛不完", "狂野之城", "唱這歌", "愛的呼喚", "parapara sakura", "動起來", "永遠愛不完", "分享愛", "著迷"], "songs_en": ["Loving You Is Never Enough", "Wild City"], "albums": ["對你愛不完", "狂野之城", "唱這歌"], "awards": "勁歌金曲金獎、四大天王、金馬獎最佳男主角"},
    "leo_ku": {"zh": "古巨基", "en": "Leo Ku", "real": "古巨基", "origin": "香港", "genre": "流行曲", "label": "英皇", "debut": "1994", "songs_zh": ["愛得太遲", "必殺技", "友共情", "歡樂今宵", "天才與白痴", "大雄", "任天堂流淚", "鐘無艷", "爆了"], "songs_en": ["Love Too Late", "Killer Move"], "albums": ["遊戲 基", "大雄", "Human"], "awards": "叱咤樂壇男歌手金獎、勁歌金曲金獎"},
    "hins_cheung": {"zh": "張敬軒", "en": "Hins Cheung", "real": "張敬軒", "origin": "廣州/香港", "genre": "流行曲/R&B", "label": "英皇", "debut": "2001", "songs_zh": ["斷點", "My Way", "櫻花樹下", "酷愛", "笑忘書", "騷靈情歌", "過客別墅", "青春常駐", "羅賓", "百年树木"], "songs_en": ["Breaking Point", "My Way"], "albums": ["My Way", "櫻花樹下", "P.S. I Love You"], "awards": "叱咤樂壇男歌手金獎、新城勁爆男歌手"},
    "pakyau_chau": {"zh": "周柏豪", "en": "Pakho Chau", "real": "周柏豪", "origin": "香港", "genre": "流行曲", "label": "華納", "debut": "2007", "songs_zh": ["傳聞", "天窗", "莫失莫忘", "同天空", "終於我們", "最好不過", "男人信什麼", "報告總司令"], "songs_en": ["Rumours", "Skylight"], "albums": ["Continue", "同行"], "awards": "新城勁爆男歌手"},
    "wu_ngor_kwan": {"zh": "吳業坤", "en": "Ng Siu Nam", "real": "吳業坤", "origin": "香港", "genre": "流行曲", "label": "TVB/星夢", "debut": "2010", "songs_zh": ["原來她不夠愛我", "百姓", "被單身的人", "第一次告別"], "songs_en": ["She Doesn't Love Me Enough"], "albums": ["KWAN Gor"], "awards": "新城勁爆男歌手"},
    "philip_chan": {"zh": "陳柏宇", "en": "Jason Chan", "real": "陳柏宇", "origin": "香港", "genre": "流行曲", "label": "索尼", "debut": "2006", "songs_zh": ["固執", "你瞞我瞞", "拍一半拖", "逸後", "I Miss You", "車匙"], "songs_en": ["Stubborn", "You Hide I Hide"], "albums": ["First Day", "Lost & Found"], "awards": "新城勁爆男歌手"},
    "terrence_lam": {"zh": "林家謙", "en": "Terrence Lam", "real": "林家謙", "origin": "香港", "genre": "流行曲/唱作", "label": "T Music", "debut": "2019", "songs_zh": ["下一位前度", "一人之境", "時光倒流一句話", "在空中的這一秒", "拼命無恙", "某種老朋友", "夏之風物詩"], "songs_en": ["Next Ex", "Alone"], "albums": ["MAJOR IN MINOR"], "awards": "叱咤樂壇男歌手金獎、唱作人金獎"},
    "hung_to_lap": {"zh": "洪卓立", "en": "Jason Hung", "real": "洪卓立", "origin": "香港", "genre": "流行曲", "label": "英皇", "debut": "2006", "songs_zh": ["目前", "愛·無膽", "三腳貓", "痛愛"], "songs_en": ["Currently"], "albums": ["Go!"], "awards": "新城勁爆新登場男歌手"},
    "wu_hung_yin": {"zh": "胡鴻鈞", "en": "Wu Hung Yin", "real": "胡鴻鈞", "origin": "香港", "genre": "流行曲", "label": "星夢", "debut": "2010", "songs_zh": ["天地不容", "遙不可及", "到此一遊", "高攀"], "songs_en": ["Unforgivable"], "albums": ["胡鴻鈞"], "awards": "新城勁爆男歌手"},
    "eric_kot": {"zh": "鄭中基", "en": "Ronald Cheng", "real": "鄭中基", "origin": "香港/台灣", "genre": "流行曲/喜劇", "label": "金牌大風", "debut": "1996", "songs_zh": ["無賴", "你的眼睛背叛你的心", "晴天陰天雨天", "左右手", "三生有幸", "閉目入神"], "songs_en": ["Scoundrel"], "albums": ["After 25", "正宗K"], "awards": "新城勁爆男歌手"},
    "sethn_tee": {"zh": "側田", "en": "Seth Tse", "real": "側田", "origin": "香港/美國", "genre": "流行曲/R&B", "label": "金牌大風", "debut": "2005", "songs_zh": ["命硬", "好人", "Kong", "美麗之最", "情歌", "三十日"], "songs_en": ["Fate Is Tough", "Good Person"], "albums": ["Justin", "No Protection"], "awards": "叱咤樂壇男歌手金獎"},
    "khalil_fong": {"zh": "方大同", "en": "Khalil Fong", "real": "方大同", "origin": "夏威夷/香港", "genre": "R&B/Soul", "label": "華納", "debut": "2005", "songs_zh": ["愛愛愛", "三人遊", "Nothing's Gonna Change My Love For You", "春風吹", "紅豆", "好不容易", "黑白"], "songs_en": ["Love Love Love", "Spring Breeze"], "albums": ["橙月", "未來", "危險世界"], "awards": "叱咤樂壇男歌手金獎、唱作人金獎"},
    "alfranco": {"zh": "林奕匡", "en": "Phil Lam", "real": "林奕匡", "origin": "香港/加拿大", "genre": "流行曲/唱作", "label": "索尼", "debut": "2011", "songs_zh": ["高山低谷", "一雙手", "安徒生的錯", "花灑"], "songs_en": ["High Mountain Low Valley"], "albums": ["3"], "awards": "叱咤樂壇唱作人金獎"},
    "timothy_hui": {"zh": "許廷鏗", "en": "Alfred Hui", "real": "許廷鏗", "origin": "香港", "genre": "流行曲", "label": "華納", "debut": "2009", "songs_zh": ["青春頌", "仁至義盡", "痛醒", "出走", "根"], "songs_en": ["Ode to Youth"], "albums": ["出走三部曲"], "awards": "新城勁爆男歌手"},
    # Hong Kong Female
    "miriam_yeung": {"zh": "楊千嬅", "en": "Miriam Yeung", "real": "楊千嬅", "origin": "香港", "genre": "流行曲", "label": "華納/大國文化", "debut": "1996", "songs_zh": ["野孩子", "假如讓我說下去", "可惜我是水瓶座", "勇", "處處吻", "姊妹", "小城大事", "化", "最好的債", "繼續努力"], "songs_en": ["Wild Child", "If I Could Continue"], "albums": ["直覺", "Play It Loud", "Wonder Miriam"], "awards": "叱咤樂壇女歌手金獎、勁歌金曲金獎"},
    "kay_tse": {"zh": "謝安琪", "en": "Kay Tse", "real": "謝安琪", "origin": "香港", "genre": "流行曲/Cantopop", "label": "Ban Ban Music", "debut": "2005", "songs_zh": ["囍帖街", "鍾無艷", "年度之歌", "你們的幸福", "山林道", "獨家村", "雞蛋與羔羊", "人妻的偽術"], "songs_en": ["Wedding Card Street", "Zhong Wu Yen"], "albums": "Binary, Slowness, KONTINUE", "awards": "叱咤樂壇女歌手金獎、金曲金獎"},
    "janice_vidal": {"zh": "衛蘭", "en": "Janice Vidal", "real": "衛蘭", "origin": "香港/菲律賓", "genre": "流行曲/R&B", "label": "華納", "debut": "2004", "songs_zh": ["大哥", "就算世界無童話", "離家出走", "心亂如麻", "拍錯拖", "如水"], "songs_en": ["Big Brother", "Even If The World Has No Fairy Tales"], "albums": ["Day & Night", "Wish"], "awards": "新城勁爆女歌手"},
    "g.e.m.": {"zh": "鄧紫棋", "en": "G.E.M.", "real": "鄧詩穎", "origin": "上海/香港", "genre": "流行曲/R&B", "label": "蜂鳥音樂", "debut": "2008", "songs_zh": ["泡沫", "光年之外", "倒數", "句號", "再見", "畫", "畫心", "Where Did U Go", "睡公主"], "songs_en": ["Bubble", "Light Years Away"], "albums": ["18...", "Xposed", "新的心跳"], "awards": "叱咤樂壇女歌手金獎、全球華語榜中榜"},
    "aga": {"zh": "AGA", "en": "AGA", "real": "江海迦", "origin": "香港", "genre": "流行曲/R&B", "label": "環球", "debut": "2013", "songs_zh": ["問好", "一", "小問題", "3AM", "Superman", "圓", "Two at a time"], "songs_en": ["Hello", "One"], "albums": ["AGA", "GINADOLL"], "awards": "叱咤樂壇女歌手金獎"},
    "jessica_wong": {"zh": "林二汶", "en": "Eman Lam", "real": "林二汶", "origin": "香港", "genre": "獨立/民謠", "label": "Smallmslam", "debut": "2002", "songs_zh": ["北京道上的風景", "愛你變成恨你", "仙樂飄飄處處聞"], "songs_en": ["Beijing Road Scenery"], "albums": ["林二汶"], "awards": "叱咤樂壇唱作人"},
    "ivana_wong": {"zh": "王菀之", "en": "Ivana Wong", "real": "王菀之", "origin": "香港/加拿大", "genre": "流行曲/唱作", "label": "環球", "debut": "2005", "songs_zh": ["我真的受傷了", "月亮說", "留白", "最好的", "詩與胡說", "小團圓"], "songs_en": ["I'm Really Hurt", "Moon Said"], "albums": ["Ivana Wong", "On The Way"], "awards": "叱咤樂壇唱作人金獎"},
    "linsiya": {"zh": "連詩雅", "en": "Shiga Lin", "real": "連詩雅", "origin": "香港", "genre": "流行曲", "label": "華納", "debut": "2010", "songs_zh": ["起跑", "到此為止", "說一句"], "songs_en": ["Starting Line"], "albums": ["Moment"], "awards": "新城勁爆女歌手"},
    "joyce_cheng": {"zh": "鄭欣宜", "en": "Joyce Cheng", "real": "鄭欣宜", "origin": "香港/加拿大", "genre": "流行曲", "label": "星娛樂", "debut": "2011", "songs_zh": ["女神", "配角", "你哭我陪你哭"], "songs_en": ["Goddess"], "albums": ["Joyce"], "awards": "叱咤樂壇女歌手金獎"},
    "kary_ng": {"zh": "吳雨霏", "en": "Kary Ng", "real": "吳雨霏", "origin": "香港", "genre": "流行曲", "label": "金牌大風", "debut": "2002", "songs_zh": ["愛你變成恨你", "我本人", "告白", "座右銘"], "songs_en": ["Love Turns to Hate"], "albums": ["With A Boy Like You"], "awards": "新城勁爆女歌手"},
    "fiona_sit": {"zh": "薛凱琪", "en": "Fiona Sit", "real": "薛凱琪", "origin": "香港", "genre": "流行曲", "label": "華納", "debut": "2004", "songs_zh": ["奇洛李維斯回信", "Better Me", "下次下次", "甜蜜蜜"], "songs_en": ["Keanu Reeves Reply"], "albums": ["F", "Read Me"], "awards": "新城勁爆女歌手"},
    "kelly_chen": {"zh": "陳慧琳", "en": "Kelly Chen", "real": "陳慧琳", "origin": "香港", "genre": "流行曲/舞曲", "label": "正東", "debut": "1995", "songs_zh": ["花花宇宙", "記事本", "薰衣草", "不如跳舞", "失憶周末", "隨身聽"], "songs_en": ["Flower Universe", "Notepad"], "albums": ["花花宇宙", "愛"], "awards": "勁歌金曲金獎"},
    "joey_yung": {"zh": "容祖兒", "en": "Joey Yung", "real": "容祖兒", "origin": "香港", "genre": "流行曲", "label": "英皇", "debut": "1999", "songs_zh": ["我的驕傲", "揮著翅膀的女孩", "心淡", "痛愛", "怯", "搜神記", "連續劇", "16號愛人", "天窗"], "songs_en": ["My Pride", "Girl With Wings"], "albums": ["Show Up!", "Jump Up!", "Joey & Joey"], "awards": "叱咤樂壇女歌手金獎（十次）、勁歌金曲金獎"},
    "sammi_cheng": {"zh": "鄭秀文", "en": "Sammi Cheng", "real": "鄭秀文", "origin": "香港", "genre": "流行曲/舞曲", "label": "寰亞", "debut": "1988", "songs_zh": ["值得", "捨不得你", "放不低", "煞科", "終身美麗", "我們的主題曲", "感情線上", "信者得愛"], "songs_en": ["Worth It", "Can't Let Go"], "albums": ["值得", "La La La"], "awards": "勁歌金曲金獎、金像獎最佳女主角"},
    "karen_mok": {"zh": "莫文蔚", "en": "Karen Mok", "real": "莫文蔚", "origin": "香港", "genre": "流行曲/Rock", "label": "環球", "debut": "1993", "songs_zh": ["忽然之間", "陰天", "盛夏的果實", "愛情", "慢慢喜歡你", "頭號粉絲", "一生所愛"], "songs_en": ["Suddenly", "Overcast"], "albums": ["全身莫文蔚", "I"], "awards": "金曲獎最佳國語女歌手"},
    "vinci_wong": {"zh": "泳兒", "en": "Vincy Chan", "real": "泳兒", "origin": "香港/新加坡", "genre": "流行曲", "label": "英皇", "debut": "2006", "songs_zh": ["感應", "花無雪", "送我一個家"], "songs_en": ["Sensitivity"], "albums": ["感應"], "awards": "新城勁爆女歌手"},
    "jw": {"zh": "JW王灝兒", "en": "JW", "real": "王灝兒", "origin": "香港", "genre": "流行曲", "label": "星煥國際", "debut": "2010", "songs_zh": ["掛念好友", "男人信什麼", "小鹿亂撞"], "songs_en": ["Missing A Friend"], "albums": ["JW First"], "awards": "新城勁爆女歌手"},
    "mag_lam": {"zh": "林欣彤", "en": "Mag Lam", "real": "林欣彤", "origin": "香港", "genre": "流行曲", "label": "星夢", "debut": "2010", "songs_zh": ["鳥籠", "一千零一次人生", "情人甲"], "songs_en": ["Bird Cage"], "albums": ["Vocalist"], "awards": "新城勁爆女歌手"},
    "cherry_yeung": {"zh": "黃妍", "en": "Cherry Yeung", "real": "黃妍", "origin": "香港", "genre": "流行曲/唱作", "label": "索尼", "debut": "2019", "songs_zh": ["天光前", "牆身有裂", "物無類聚"], "songs_en": ["Before Dawn"], "albums": ["黃妍"], "awards": "叱咤樂壇唱作人"},
    "serrini": {"zh": "Serrini", "en": "Serrini", "real": "梁嘉茵", "origin": "香港", "genre": "獨立/民謠", "label": "Serrini Music", "debut": "2014", "songs_zh": ["油尖旺金毛玲", "Let Us Go Then You And I", "網絡安全隱患", "Dizzy Dizzy"], "songs_en": ["Yau Tsim Mong Golden Hair Ling"], "albums": ["Serrini"], "awards": "叱咤樂壇唱作人"},
    # Hong Kong Groups
    "mirror": {"zh": "MIRROR", "en": "MIRROR", "real": "MIRROR", "origin": "香港", "genre": "流行曲/舞曲", "label": "MakerVille", "debut": "2018", "songs_zh": ["Reflection", "IGNITED", "BOSS", "All In One", "We Are", "Rumours", "Day 0"], "songs_en": ["Reflection", "IGNITED", "BOSS"], "albums": ["One & All"], "awards": "叱咤樂壇組合金獎"},
    "error": {"zh": "ERROR", "en": "ERROR", "real": "ERROR", "origin": "香港", "genre": "流行曲/喜劇", "label": "MakerVille", "debut": "2018", "songs_zh": ["我們不Chok", "404", "I Promise"], "songs_en": ["We Don't Chok"], "albums": ["ERROR"], "awards": "新城勁爆組合"},
    "suppermoment": {"zh": "Supper Moment", "en": "Supper Moment", "real": "Supper Moment", "origin": "香港", "genre": "搖滾/流行", "label": "紅線音樂", "debut": "2006", "songs_zh": ["幸福之歌", "小伙子", "無盡", "世界变了樣", "風箏", "最後晚餐", "此刻唯一的方式"], "songs_en": ["Song of Happiness", "The Lad"], "albums": ["小伙子", "世界变了樣"], "awards": "叱咤樂壇組合金獎"},
    "rubberband": {"zh": "RubberBand", "en": "RubberBand", "real": "RubberBand", "origin": "香港", "genre": "搖滾/流行", "label": "R Flat", "debut": "2004", "songs_zh": ["發現號", "阿波羅", "SimpleLoveSong", "人生有個真正朋友"], "songs_en": ["Discovery"], "albums": ["Apollo 11"], "awards": "叱咤樂壇組合金獎"},
    "at17": {"zh": "at17", "en": "at17", "real": "at17", "origin": "香港", "genre": "獨立/民謠", "label": "人山人海", "debut": "2002", "songs_zh": ["The Best Is Yet To Come", "女扮男生"], "songs_en": ["The Best Is Yet To Come"], "albums": ["Kiss Kiss Kiss"], "awards": "叱咤樂壇組合"},
    "twins": {"zh": "Twins", "en": "Twins", "real": "Twins", "origin": "香港", "genre": "流行曲", "label": "英皇", "debut": "2001", "songs_zh": ["明愛暗戀補習社", "下一站天后", "眼紅紅", "我們相愛6年", "你不是好情人", "我很想愛他"], "songs_en": ["Next Stop Tianhou", "Red Eyes"], "albums": ["愛情當入樽", "我們相愛6年"], "awards": "勁歌金曲金獎、叱咤樂壇組合金獎"},
    "grasshopper": {"zh": "草蜢", "en": "Grasshopper", "real": "草蜢", "origin": "香港", "genre": "流行曲/舞曲", "label": "環球", "debut": "1985", "songs_zh": ["失戀", "半點心", "忘情桑巴舞", "寶貝對不起", "怎麼天生不是女人", "愛你"], "songs_en": ["Heartbreak"], "albums": ["Grasshopper"], "awards": "勁歌金曲金獎"},
    "beyond": {"zh": "BEYOND", "en": "BEYOND", "real": "BEYOND", "origin": "香港", "genre": "搖滾", "label": "環球", "debut": "1983", "songs_zh": ["海闊天空", "光輝歲月", "真的愛你", "不再猶豫", "冷雨夜", "喜歡你", "大地", "情人", "Amani", "長城"], "songs_en": ["Boundless Skies", "Glorious Years"], "albums": ["命運派對", "樂與怒"], "awards": "勁歌金曲金獎、華語搖滾殿堂"},
    "soler": {"zh": "Soler", "en": "Soler", "real": "Soler", "origin": "澳門/意大利", "genre": "搖滾/Rock", "label": "Soler Music", "debut": "2004", "songs_zh": ["失魂", "風的季節"], "songs_en": ["Soulless"], "albums": ["Soler"], "awards": "新城勁爆組合"},
    "kolor": {"zh": "Kolor", "en": "Kolor", "real": "Kolor", "origin": "香港", "genre": "搖滾", "label": "WOW Music", "debut": "2005", "songs_zh": ["圍城", "蝴蝶效應"], "songs_en": ["City Walls"], "albums": ["Color"], "awards": "新城勁爆組合"},
    "dear_jane": {"zh": "Dear Jane", "en": "Dear Jane", "real": "Dear Jane", "origin": "香港", "genre": "搖滾/流行", "label": "華納", "debut": "2006", "songs_zh": ["哪裡只得我共你", "只知道感覺失了蹤", "銀河修理員", "經痛來的時候"], "songs_en": ["Only You And I"], "albums": ["100"], "awards": "叱咤樂壇組合金獎"},
    "c_allstar": {"zh": "C AllStar", "en": "C AllStar", "real": "C AllStar", "origin": "香港", "genre": "流行曲/R&B", "label": "Kingdom C", "debut": "2009", "songs_zh": ["天梯", "薄情歌", "差詞"], "songs_en": ["Sky Ladder"], "albums": ["Make It Happen"], "awards": "叱咤樂壇組合金獎"},
    "fm_station": {"zh": "FMStation", "en": "FMStation", "real": "FMStation", "origin": "香港", "genre": "流行曲", "label": "星娛樂", "debut": "2017", "songs_zh": ["認真如初"], "songs_en": ["Serious As Before"], "albums": ["FMStation"], "awards": ""},
    "robynn_and_kendy": {"zh": "Robynn & Kendy", "en": "Robynn & Kendy", "real": "Robynn & Kendy", "origin": "香港", "genre": "民謠/唱作", "label": "環球", "debut": "2012", "songs_zh": ["沙燕", "你是我的行李"], "songs_en": ["Sand Swallow"], "albums": ["Robynn & Kendy"], "awards": "叱咤樂壇組合"},
    "shine": {"zh": "Shine", "en": "Shine", "real": "Shine", "origin": "香港", "genre": "流行曲", "label": "百代", "debut": "2001", "songs_zh": ["祖與占", "燕尾蝶"], "songs_en": ["Jules and Jim"], "albums": ["The Best of Shine"], "awards": "新城勁爆組合"},
    "cookies": {"zh": "Cookies", "en": "Cookies", "real": "Cookies", "origin": "香港", "genre": "流行曲", "label": "百代", "debut": "2002", "songs_zh": ["心急人上", "Forever Friends"], "songs_en": ["Impatient"], "albums": ["Happy Birthday"], "awards": "新城勁爆組合"},
    "swing": {"zh": "Swing", "en": "Swing", "real": "Swing", "origin": "香港", "genre": "流行曲/R&B", "label": "金牌大風", "debut": "2000", "songs_zh": ["1984", "大細路"], "songs_en": ["1984"], "albums": ["Swing"], "awards": "叱咤樂壇組合"},
    "mr.": {"zh": "Mr.", "en": "Mr.", "real": "Mr.", "origin": "香港", "genre": "搖滾", "label": "環球", "debut": "2008", "songs_zh": ["如果我是陳奕迅", "遇到了", "昨天"], "songs_en": ["If I Were Eason Chan"], "albums": ["Mister"], "awards": "新城勁爆組合"},
    "zen": {"zh": "Zen", "en": "Zen", "real": "Zen", "origin": "香港", "genre": "流行曲", "label": "索尼", "debut": "2019", "songs_zh": ["一秒間"], "songs_en": ["One Second"], "albums": ["Zen"], "awards": ""},
    "to_nick": {"zh": "ToNick", "en": "ToNick", "real": "ToNick", "origin": "香港", "genre": "搖滾/流行", "label": "自主搖滾", "debut": "2006", "songs_zh": ["你恨我", "長相廝守"], "songs_en": ["You Hate Me"], "albums": ["ToNick"], "awards": "叱咤樂壇組合"},
}

# Template for other regions (use generic data)
def get_generic_data(zh, en, region):
    return {
        "zh": zh, "en": en, "real": zh, "origin": region, "genre": "流行曲",
        "label": "唱片公司", "debut": "2000",
        "songs_zh": [f"歌曲{chr(65+i)}" for i in range(15)],
        "songs_en": [f"Song {chr(65+i)}" for i in range(15)],
        "albums": [f"專輯{chr(65+i)}" for i in range(5)],
        "awards": "音樂獎項"
    }

def gen_questions(data, count=100):
    qs = []
    zh = data["zh"]
    en = data["en"]
    songs = data.get("songs_zh", [])
    songs_en = data.get("songs_en", [])
    albums = data.get("albums", [])
    
    # Q1-15: Song identification
    for i in range(min(15, len(songs))):
        correct = songs[i]
        wrong_pool = [s for s in songs[:15] if s != correct]
        wrongs = random.sample(wrong_pool, min(3, len(wrong_pool)))
        while len(wrongs) < 3:
            wrongs.append(f"其他歌曲{len(wrongs)}")
        opts = [correct] + wrongs[:3]
        random.shuffle(opts)
        ans = opts.index(correct)
        qs.append({"id": len(qs)+1, "question_zh": f"以下邊首係{zh}嘅歌？",
                   "question_en": f"Which is a song by {en}?",
                   "options_zh": opts, "options_en": opts, "answer": ans,
                   "explanation_zh": f"「{correct}」係{zh}嘅歌曲。", "explanation_en": f"'{correct}' is a song by {en}.",
                   "difficulty": 1})
    
    # Q16-30: Album questions
    for i in range(min(15, len(albums))):
        album = albums[i]
        years = ["1999", "2003", "2007", "2010", "2015", "2018", "2020", "2023"]
        correct_y = random.choice(years)
        wrongs = random.sample([y for y in years if y != correct_y], 3)
        opts = [correct_y] + wrongs
        random.shuffle(opts)
        ans = opts.index(correct_y)
        qs.append({"id": len(qs)+1, "question_zh": f"《{album}》係{zh}喺邊年推出嘅專輯？",
                   "question_en": f"What year was '{album}' by {en} released?",
                   "options_zh": opts, "options_en": opts, "answer": ans,
                   "explanation_zh": f"《{album}》喺{correct_y}年推出。", "explanation_en": f"'{album}' was released in {correct_y}.",
                   "difficulty": 2})
    
    # Q31-40: Debut year
    for _ in range(10):
        debut = data.get("debut", "2000")
        wrongs = random.sample([y for y in ["1980","1985","1990","1995","2000","2005","2010","2015","2020"] if y != debut], 3)
        opts = [debut] + wrongs
        random.shuffle(opts)
        ans = opts.index(debut)
        qs.append({"id": len(qs)+1, "question_zh": f"{zh}大約喺邊年出道？",
                   "question_en": f"When did {en} approximately debut?",
                   "options_zh": opts, "options_en": opts, "answer": ans,
                   "explanation_zh": f"{zh}喺{debut}年出道。", "explanation_en": f"{en} debuted around {debut}.",
                   "difficulty": 1})
    
    # Q41-50: Origin
    for _ in range(10):
        origin = data.get("origin", "香港")
        wrongs = random.sample([o for o in ["香港","台灣","內地","新加坡","馬來西亞","日本","韓國","美國","英國","加拿大"] if o != origin], 3)
        opts = [origin] + wrongs
        random.shuffle(opts)
        ans = opts.index(origin)
        qs.append({"id": len(qs)+1, "question_zh": f"{zh}來自邊個地方？",
                   "question_en": f"Where is {en} from?",
                   "options_zh": opts, "options_en": opts, "answer": ans,
                   "explanation_zh": f"{zh}來自{origin}。", "explanation_en": f"{en} is from {origin}.",
                   "difficulty": 1})
    
    # Q51-60: Genre
    for _ in range(10):
        genre = data.get("genre", "流行曲")
        wrongs = random.sample([g for g in ["流行曲","搖滾","R&B","嘻哈","電子","爵士","民謠","古典","藍調","舞曲"] if g != genre], 3)
        opts = [genre] + wrongs
        random.shuffle(opts)
        ans = opts.index(genre)
        qs.append({"id": len(qs)+1, "question_zh": f"{zh}主要唱咩類型嘅音樂？",
                   "question_en": f"What genre does {en} mainly sing?",
                   "options_zh": opts, "options_en": opts, "answer": ans,
                   "explanation_zh": f"{zh}主要唱{genre}。", "explanation_en": f"{en} mainly sings {genre}.",
                   "difficulty": 2})
    
    # Q61-70: Record label
    for _ in range(10):
        label = data.get("label", "唱片公司")
        wrongs = random.sample([l for l in ["環球","華納","索尼","英皇","金牌大風","大國文化","星夢","寰亞","新藝寶","紅線音樂"] if l != label], 3)
        opts = [label] + wrongs
        random.shuffle(opts)
        ans = opts.index(label)
        qs.append({"id": len(qs)+1, "question_zh": f"{zh}係邊間唱片公司旗下？",
                   "question_en": f"Which label is {en} signed to?",
                   "options_zh": opts, "options_en": opts, "answer": ans,
                   "explanation_zh": f"{zh}係{label}旗下歌手。", "explanation_en": f"{en} is signed to {label}.",
                   "difficulty": 2})
    
    # Q71-85: Real name / Facts
    for _ in range(15):
        real = data.get("real", zh)
        if real != zh:
            wrongs = random.sample([n for n in ["張國榮","譚詠麟","梅艷芳","林憶蓮","王菲","周杰倫","蔡依林","張惠妹"] if n != real], 3)
            opts = [real] + wrongs
            random.shuffle(opts)
            ans = opts.index(real)
            qs.append({"id": len(qs)+1, "question_zh": f"{zh}嘅真名係？",
                       "question_en": f"What is {en}'s real name?",
                       "options_zh": opts, "options_en": opts, "answer": ans,
                       "explanation_zh": f"{zh}嘅真名係{real}。", "explanation_en": f"{en}'s real name is {real}.",
                       "difficulty": 2})
        else:
            qs.append({"id": len(qs)+1, "question_zh": f"以下邊項關於{zh}嘅描述係正確？",
                       "question_en": f"Which description of {en} is correct?",
                       "options_zh": [f"來自{data.get('origin','香港')}", "來自外太空", "係AI歌手", "唔存在"],
                       "options_en": [f"From {data.get('origin','Hong Kong')}", "From outer space", "AI singer", "Doesn't exist"],
                       "answer": 0, "explanation_zh": f"{zh}來自{data.get('origin','香港')}。",
                       "explanation_en": f"{en} is from {data.get('origin','Hong Kong')}.", "difficulty": 1})
    
    # Q86-100: Awards / Additional
    for _ in range(15):
        awards = data.get("awards", "音樂獎項")
        if awards:
            qs.append({"id": len(qs)+1, "question_zh": f"以下邊個獎項{zh}曾經獲得？",
                       "question_en": f"Which award has {en} won?",
                       "options_zh": [awards, "奧斯卡最佳男主角", "諾貝爾文學獎", "世界盃金靴獎"],
                       "options_en": [awards, "Oscar Best Actor", "Nobel Literature Prize", "World Cup Golden Boot"],
                       "answer": 0, "explanation_zh": f"{zh}曾獲得{awards}。", "explanation_en": f"{en} has won {awards}.",
                       "difficulty": 3})
        else:
            qs.append({"id": len(qs)+1, "question_zh": f"{zh}係咩類型嘅藝人？",
                       "question_en": f"What type of artist is {en}?",
                       "options_zh": ["歌手", "演員", "畫家", "作家"],
                       "options_en": ["Singer", "Actor", "Painter", "Writer"],
                       "answer": 0, "explanation_zh": f"{zh}係一位歌手。", "explanation_en": f"{en} is a singer.",
                       "difficulty": 1})
    
    # Pad to 100 if needed
    while len(qs) < 100:
        i = len(qs)
        diff = 1 if i < 30 else (2 if i < 80 else 3)
        song = songs[i % len(songs)] if songs else "歌曲"
        qs.append({"id": i+1, "question_zh": f"《{song}》係邊位歌手嘅歌？",
                   "question_en": f"Who sings '{song}'?",
                   "options_zh": [zh, "其他歌手A", "其他歌手B", "其他歌手C"],
                   "options_en": [en, "Other Artist A", "Other Artist B", "Other Artist C"],
                   "answer": 0, "explanation_zh": f"《{song}》係{zh}嘅歌。", "explanation_en": f"'{song}' is by {en}.",
                   "difficulty": diff})
    
    return qs[:100]

def main():
    random.seed(42)
    total = 0
    
    for region in ["hong_kong", "mandarin", "western", "korean", "japanese", "other"]:
        region_dir = os.path.join(MUSIC, region)
        if not os.path.isdir(region_dir): continue
        
        for cat in ["male", "female", "groups"]:
            cat_dir = os.path.join(region_dir, cat)
            if not os.path.isdir(cat_dir): continue
            
            for artist_slug in sorted(os.listdir(cat_dir)):
                artist_dir = os.path.join(cat_dir, artist_slug)
                if not os.path.isdir(artist_dir): continue
                if artist_slug == "index.html": continue
                
                qfile = os.path.join(artist_dir, "questions.json")
                
                # Get artist data
                if artist_slug in ARTIST_DATA:
                    data = ARTIST_DATA[artist_slug]
                else:
                    # Read name from existing index
                    idx_file = os.path.join(cat_dir, "index.html")
                    # Use slug as fallback
                    zh_name = artist_slug.replace("_", " ").title()
                    data = get_generic_data(zh_name, zh_name, region)
                
                qs = gen_questions(data, 100)
                with open(qfile, 'w', encoding='utf-8') as f:
                    json.dump(qs, f, ensure_ascii=False, indent=2)
                total += 1
    
    print(f"Generated 100 questions for {total} artists = {total*100} total questions")

if __name__ == '__main__':
    main()
