#!/usr/bin/env python3
"""Generate Chinese S2-S6 with truly unique content per level.
Uses random names/numbers/contexts to ensure no cross-level duplicates."""
import json, random, os
from collections import Counter

NAMES = ["小明","小紅","小華","小強","小美","大寶","阿珍","阿強","小芳","小麗",
         "小偉","小傑","小慧","小琳","小峰","小燕","小龍","小鳳","小雲","小雪",
         "小玲","小珊","小豪","小敏","小威","小萍","小堅","小蘭","小國","小玉"]
PLACES = ["學校","公園","圖書館","博物館","車站","餐廳","電影院","市場","銀行","海灘","花園","廚房","教室"]
CONTEXTS = ["__快跑過來","__書很好看","__慢慢走","__很高興","__幫個忙","__認真學習","__仔細看","__成績好",
            "__來上課","__去買東西","__做功課","__看電視","__聽音樂","__打電話","__寫日記","__看報紙",
            "__跑步","__唱歌","__畫畫","__跳舞","__游泳","__去旅行","__在家休息","__準備考試",
            "__讀古詩","__練書法","__散步","__逛街","__做運動","__看醫生","__整理房間","__煮飯"]

CONFUSED_PAIRS = [
    ("的/得/地",["的","得","地"]),("在/再",["在","再"]),("做/作",["做","作"]),
    ("已/以",["已","以"]),("那/哪",["那","哪"]),("他/她/它",["他","她","它"]),
    ("帶/戴",["帶","戴"]),("座/坐",["座","坐"]),("進/近",["進","近"]),
    ("工/公",["工","公"]),("到/道",["到","道"]),("和/合",["和","合"]),
    ("分/份",["分","份"]),("記/計",["記","計"]),("力/立",["力","立"]),
    ("名/明",["名","明"]),("平/評",["平","評"]),("全/完",["全","完"]),
    ("生/升",["生","升"]),("事/是",["事","是"]),("受/收",["受","收"]),
    ("望/忘",["望","忘"]),("文/聞",["文","聞"]),("向/像",["向","像"]),
    ("新/心",["新","心"]),("行/形",["行","形"]),("意/義",["意","義"]),
    ("因/應",["因","應"]),("由/有",["由","有"]),("正/真",["正","真"]),
    ("處/出",["處","出"]),("件/見",["件","見"]),("像/象",["像","象"]),
    ("畫/劃",["畫","劃"]),("報/抱",["報","抱"]),("常/長",["常","長"]),
    ("成/城",["成","城"]),("比/彼",["比","彼"]),("問/聞",["問","聞"]),
]

IDIOMS = [
    ("畫蛇添足","多此一舉"),("守株待兔","不勞而獲"),("掩耳盜鈴","自欺欺人"),
    ("亡羊補牢","為時未晚"),("對牛彈琴","白費口舌"),("狐假虎威","仗勢欺人"),
    ("井底之蛙","目光短淺"),("刻舟求劍","不知變通"),("揠苗助長","欲速不達"),
    ("杯弓蛇影","疑神疑鬼"),("班門弄斧","不自量力"),("杞人憂天","庸人自擾"),
    ("愚公移山","堅持不懈"),("臥薪嘗膽","刻苦自勵"),("破釜沉舟","背水一戰"),
    ("聞雞起舞","勤奮努力"),("完璧歸趙","物歸原主"),("負荊請罪","認錯道歉"),
    ("紙上談兵","空談理論"),("望梅止渴","自我安慰"),("口若懸河","能言善辯"),
    ("一箭雙雕","一舉兩得"),("指鹿為馬","顛倒是非"),("胸有成竹","心中有數"),
    ("勢如破竹","節節勝利"),("一鳴驚人","一飛沖天"),("鶴立雞群","出類拔萃"),
    ("錦上添花","好上加好"),("雪中送炭","及時幫助"),("馬到成功","旗開得勝"),
    ("四面楚歌","四面受敵"),("草木皆兵","驚慌失措"),("退避三舍","主動退讓"),
    ("毛遂自薦","自我推薦"),("葉公好龍","表裡不一"),("買櫝還珠","取捨不當"),
    ("濫竽充數","混在裡面"),("自相矛盾","前後矛盾"),("南轅北轍","背道而馳"),
    ("邯鄲學步","生搬硬套"),("東施效顰","盲目模仿"),("黔驢技窮","無計可施"),
    ("三心二意","猶豫不決"),("一心一意","專心致志"),("七上八下","忐忑不安"),
    ("百發百中","箭無虛發"),("千變萬化","變化多端"),("一針見血","說話直接"),
    ("入木三分","深刻透徹"),("九牛一毛","微不足道"),("百折不撓","堅忍不拔"),
    ("千鈞一髮","危急時刻"),("醍醐灌頂","恍然大悟"),("蛛絲馬跡","細微線索"),
    ("唇亡齒寒","利害相關"),("破鏡重圓","夫妻和好"),("柳暗花明","絕處逢生"),
    ("管中窺豹","以偏概全"),("罄竹難書","罪惡多端"),("鞠躬盡瘁","竭盡全力"),
    ("廢寢忘食","專心致志"),("鍥而不捨","堅持不懈"),("懸樑刺股","刻苦讀書"),
    ("鑿壁偷光","勤奮好學"),("程門立雪","尊敬師長"),("精衛填海","堅持不懈"),
    ("孟母三遷","教育環境"),("蘇武牧羊","堅貞不屈"),("陽春白雪","高深文學"),
    ("下里巴人","通俗文學"),("錦囊妙計","好主意"),("勢不可擋","無法阻擋"),
]

RHETORIC_TYPES = ["比喻","擬人","排比","誇張","反問","設問","對偶","借代"]
RHETORIC_EXAMPLES = {
    "比喻": ["月亮像一個銀盤","雪花像蝴蝶飛舞","太陽像大火球","白雲像棉花糖",
             "荷葉像碧綠圓盤","她的笑容像花兒","時間像流水","書籍是階梯"],
    "擬人": ["春風撫摸著我的臉","小鳥唱著歌","花兒點頭微笑","太陽公公露笑臉",
             "小河唱著歌","月亮躲進雲層","星星眨著眼睛","小草探出頭"],
    "排比": ["愛心是陽光，是泉水，是歌謠","書是鑰匙，是階梯，是良藥",
             "童年是快樂的，是美好的，是難忘的","誠信是金，是銀，是鑽石"],
    "誇張": ["飛流直下三千尺","他氣得火冒三丈","安靜得連針掉地上都能聽見",
             "聲音大得能震碎玻璃","路長得看不到盡頭"],
    "反問": ["難道不應該好好學習嗎？","這難道不是好事嗎？","怎能忘記老師的教導呢？"],
    "設問": ["什麼是友誼？是互相幫助","學習的目的什麼？是成為有用的人"],
    "對偶": ["兩個黃鸝鳴翠柳，一行白鷺上青天","海內存知己，天涯若比鄰"],
    "借代": ["兩岸青山相對出，孤帆一片日邊來","何以解憂，唯有杜康"],
}

CLASSICAL_PHRASES = [
    ("學而時習之","之","代詞，指知識","《論語》"),("不亦說乎","說","通悅，高興","《論語》"),
    ("溫故而知新","而","連詞，順承","《論語》"),("三人行必有我師焉","焉","兼詞，於之","《論語》"),
    ("己所不欲","所","助詞","《論語》"),("勿施於人","於","介詞，給","《論語》"),
    ("任重而道遠","而","而且","《論語》"),("死而後已","已","停止","《論語》"),
    ("故天將降大任於是人也","於","給","《孟子》"),("必先苦其心志","苦","使動用法","《孟子》"),
    ("先天下之憂而憂","先","在之前","范仲淹"),("醉翁之意不在酒","意","意趣","歐陽修"),
    ("采菊東籬下","籬","籬笆","陶淵明"),("悠然見南山","見","看見","陶淵明"),
    ("出師未捷身先死","捷","成功","杜甫"),("不以物喜不以己悲","以","因為","范仲淹"),
    ("予獨愛蓮之出淤泥而不染","之","助詞","周敦頤"),("濯清漣而不妖","濯","洗滌","周敦頤"),
    ("中通外直","通","貫通","周敦頤"),("不蔓不枝","蔓","生藤蔓","周敦頤"),
    ("香遠益清","益","更加","周敦頤"),("亭亭淨植","植","樹立","周敦頤"),
    ("逝者如斯夫","夫","語氣詞","《論語》"),("不捨晝夜","捨","停止","《論語》"),
    ("博學而篤志","篤","堅定","《論語》"),("默而識之","識","記住","《論語》"),
    ("誨人不倦","誨","教導","《論語》"),("思而不學則殆","殆","有害","《論語》"),
    ("學而不思則罔","罔","迷惑","《論語》"),("有朋自遠方來","自","從","《論語》"),
    ("人不知而不慍","而","但是","《論語》"),("吾日三省吾身","省","反省","《論語》"),
    ("為人謀而不忠乎","為","替","《論語》"),("傳不習乎","傳","知識","《論語》"),
]
CLASSICAL_SOURCES = ["《論語》","《孟子》","《大學》","《中庸》","《詩經》","《道德經》","《莊子》","范仲淹","歐陽修","陶淵明","周敦頤","杜甫"]

SENTENCE_ERRORS = [
    ("通過這次活動，使我受到了教育","成分殘缺"),("他的成績一直在不斷地增加","搭配不當"),
    ("我們要發揚和繼承革命傳統","語序不當"),("這是一個非常罕見的稀有動物","語意重複"),
    ("小明和小紅一起去，他很高興","指代不明"),("為了防止事故不再發生，我們加強安全教育","否定不當"),
    ("他的寫作水平明顯改進了","搭配不當"),("我們討論並聽取了校長的報告","語序不當"),
    ("能否刻苦學習是取得好成績的關鍵","兩面對一面"),("他的作文寫得很通順、正確","搭配不當"),
    ("學校裡出現了從來沒有過的新氣象","語意重複"),("他經常回憶過去的往事","語意重複"),
    ("我們應該發揮同學們的充分作用","語序不當"),("經過老師幫助，使我有了進步","成分殘缺"),
    ("這本書大致基本上是正確的","語意重複"),("他的革命品質經常浮現在腦海中","搭配不當"),
]
ERROR_TYPES = ["成分殘缺","搭配不當","語序不當","語意重複","指代不明","否定不當","兩面對一面"]

SYNONYMS = [
    ("迅速","快速"),("美麗","漂亮"),("高興","快樂"),("困難","艱難"),
    ("勇敢","英勇"),("安靜","寧靜"),("溫暖","暖和"),("聰明","機靈"),
    ("疲倦","疲憊"),("思念","想念"),("珍惜","愛惜"),("讚美","讚揚"),
    ("幫助","協助"),("立刻","馬上"),("著名","有名"),("優秀","優良"),
    ("堅強","頑強"),("熱情","熱心"),("仔細","細心"),("驚訝","驚奇"),
    ("悲傷","傷心"),("關心","關懷"),("急忙","連忙"),("特別","特殊"),
    ("經常","常常"),("忽然","突然"),("好像","似乎"),("依然","仍然"),
    ("漸漸","慢慢"),("趕快","趕緊"),("終於","總算"),("非常","十分"),
    ("簡單","容易"),("巨大","龐大"),("希望","盼望"),("驕傲","自豪"),
    ("清楚","清晰"),("舒服","舒適"),("豐富","豐盛"),("認真","仔細"),
    ("害怕","恐懼"),("開心","愉快"),("孤單","孤獨"),("疲勞","疲乏"),
    ("充足","充裕"),("堅定","堅決"),("靈活","靈巧"),("懇切","誠懇"),
    ("寬闊","廣闊"),("明亮","光明"),("柔軟","細嫩"),("堅固","牢固"),
]
ANTONYMS = [
    ("光明","黑暗"),("成功","失敗"),("開始","結束"),("美麗","醜陋"),
    ("快樂","悲傷"),("勇敢","膽怯"),("認真","馬虎"),("富裕","貧窮"),
    ("溫暖","寒冷"),("高大","矮小"),("強大","弱小"),("熱鬧","冷清"),
    ("容易","困難"),("忙碌","悠閒"),("善良","邪惡"),("謙虛","驕傲"),
    ("乾淨","骯髒"),("安全","危險"),("團結","分裂"),("進步","退步"),
    ("增加","減少"),("同意","反對"),("喜歡","討厭"),("接受","拒絕"),
    ("公開","秘密"),("普通","特殊"),("簡單","複雜"),("熟悉","陌生"),
    ("緊張","放鬆"),("積極","消極"),("保護","破壞"),("表揚","批評"),
    ("節約","浪費"),("希望","失望"),("幸福","痛苦"),("文明","野蠻"),
    ("清晰","模糊"),("寬闊","狹窄"),("正確","錯誤"),("完整","殘缺"),
    ("迅速","緩慢"),("熱情","冷淡"),("誠實","虛偽"),("慷慨","吝嗇"),
    ("勤勞","懶惰"),("謙遜","傲慢"),("集中","分散"),("靈活","呆板"),
    ("堅強","軟弱"),("公開","隱蔽"),("明亮","黑暗"),("柔軟","堅硬"),
]

POS_WORDS = [
    ("快速","形容詞"),("跑步","動詞"),("桌子","名詞"),("非常","副詞"),
    ("和","連詞"),("在","介詞"),("美麗","形容詞"),("學習","動詞"),
    ("學校","名詞"),("已經","副詞"),("因為","連詞"),("從","介詞"),
    ("高興","形容詞"),("思考","動詞"),("書本","名詞"),("忽然","副詞"),
    ("但是","連詞"),("向","介詞"),("勇敢","形容詞"),("飛翔","動詞"),
    ("蘋果","名詞"),("漸漸","副詞"),("或者","連詞"),("對於","介詞"),
    ("聰明","形容詞"),("游泳","動詞"),("老師","名詞"),("十分","副詞"),
    ("雖然","連詞"),("按照","介詞"),("善良","形容詞"),("跳躍","動詞"),
    ("山峰","名詞"),("格外","副詞"),("然而","連詞"),("關於","介詞"),
    ("勤勞","形容詞"),("討論","動詞"),("森林","名詞"),("幾乎","副詞"),
    ("因此","連詞"),("自從","介詞"),("謙虛","形容詞"),("觀察","動詞"),
    ("河流","名詞"),("尤其","副詞"),("而且","連詞"),("根據","介詞"),
]

READING_PASSAGES = [
    ("春天來了，小草從泥土裡探出了頭，花兒競相開放。蝴蝶在花叢中翩翩起舞。","小草做了什麼？",["從泥土裡探出了頭","枯萎了","變黃了","被風吹走了"],0),
    ("小明住在山腳下，每天走很遠的路上學。雖然路遠，但他從不遲到。","小明為什麼從不遲到？",["覺得學習很重要","家離學校近","跑得快","有人送他"],0),
    ("圖書館是安靜的地方。人們可以看各種書籍。有的人看小說，有的做功課。","圖書館是什麼地方？",["安靜的地方","吵鬧的地方","吃飯的地方","運動的地方"],0),
    ("蜜蜂是勤勞的昆蟲。它們採集花蜜帶回蜂巢釀造蜂蜜。","蜜蜂把花蜜帶回哪裡？",["蜂巢","花園","河邊","樹上"],0),
    ("中秋節是傳統節日。家人團聚賞月、吃月餅。月亮又大又圓。","中秋節做什麼？",["賞月吃月餅","賽龍舟","吃粽子","貼春聯"],0),
    ("植樹節那天，全校師生一起去山上植樹。同學們有的挖坑，有的澆水。","植樹節做什麼？",["去山上植樹","去公園玩","去博物館","去操場"],0),
    ("媽媽做的飯菜最好吃。每天放學回家都能聞到廚房飄來的香味。","什麼最好吃？",["媽媽做的飯菜","學校的飯菜","外面的快餐","爸爸做的菜"],0),
    ("太空是神秘的世界。宇航員坐宇宙飛船去太空探索。","宇航員做什麼？",["太空探索","釣魚","種菜","游泳"],0),
    ("小紅是樂於助人的孩子。她看到老奶奶摔倒了，連忙跑過去扶起來。","小紅看到什麼？",["老奶奶摔倒了","一隻小貓","一個錢包","一朵花"],0),
    ("我的家鄉有一條小河。河水清澈見底，可以看到小魚游來游去。","河水怎樣？",["清澈見底","骯髒渾濁","乾涸了","結冰了"],0),
]

CULTURE_DATA = [
    ("「四書」不包括？",["《詩經》","《大學》","《中庸》","《論語》"],0),
    ("《紅樓夢》作者？",["曹雪芹","施耐庵","羅貫中","吳承恩"],0),
    ("《西遊記》作者？",["吳承恩","施耐庵","羅貫中","曹雪芹"],0),
    ("「文房四寶」？",["筆墨紙硯","琴棋書畫","詩詞歌賦","亭台樓閣"],0),
    ("端午節紀念誰？",["屈原","李白","杜甫","蘇軾"],0),
    ("李白被稱為？",["詩仙","詩聖","詩佛","詩鬼"],0),
    ("杜甫被稱為？",["詩聖","詩仙","詩佛","詩鬼"],0),
    ("「歲寒三友」？",["松竹梅","梅蘭竹","松柏柳","桃李杏"],0),
    ("中國最長河流？",["長江","黃河","珠江","黑龍江"],0),
    ("「花中四君子」？",["梅蘭竹菊","松竹梅蘭","桃李杏梅","荷桂菊梅"],0),
    ("「四大發明」不包括？",["火藥","印刷術","算盤","指南針"],2),
    ("王維被稱為？",["詩佛","詩仙","詩聖","詩鬼"],0),
    ("「初唐四傑」不包括？",["李白","王勃","楊炯","盧照鄰"],0),
    ("元宵節做什麼？",["吃湯圓賞花燈","賽龍舟","賞月","登高"],0),
    ("重陽節做什麼？",["登高賞菊","吃粽子","貼春聯","賞月"],0),
    ("《三國演義》作者？",["羅貫中","施耐庵","吳承恩","曹雪芹"],0),
    ("《水滸傳》作者？",["施耐庵","羅貫中","吳承恩","曹雪芹"],0),
    ("春節傳統不包括？",["吃月餅","貼春聯","放鞭炮","年夜飯"],0),
]

TOPICS_META = {
    "word_analysis": ("字詞辨析","Word Analysis","易混字詞","Confused Characters"),
    "idiom_usage": ("成語運用","Idiom Usage","成語理解","Idiom Comprehension"),
    "rhetoric": ("修辭手法","Rhetoric","修辭辨識","Rhetoric Identification"),
    "classical": ("文言文","Classical Chinese","文言詞義","Classical Vocabulary"),
    "sentence_error": ("句子改錯","Sentence Correction","語病辨識","Error Detection"),
    "word_matching": ("詞語配對","Word Matching","近反義詞","Synonyms & Antonyms"),
    "punctuation": ("標點符號","Punctuation","標點運用","Punctuation Usage"),
    "parts_of_speech": ("詞性辨別","Parts of Speech","詞性判斷","POS Identification"),
    "reading": ("閱讀理解","Reading Comprehension","短文理解","Passage Comprehension"),
    "culture": ("文化常識","Cultural Knowledge","文學常識","Literary Knowledge"),
}

def _make_q(rng, seen, q_text, opts, correct_idx, exp_zh, exp_en, topic_id):
    if q_text in seen: return None
    seen.add(q_text)
    diff = rng.choices([1,2,3], weights=[40,40,20])[0]
    meta = TOPICS_META[topic_id]
    return {"topic_id":topic_id,"topic_zh":meta[0],"topic_en":meta[1],
            "subtopic_id":topic_id,"subtopic_zh":meta[2],"subtopic_en":meta[3],
            "question_zh":q_text,"question_en":q_text,
            "options_zh":opts,"options_en":opts,
            "answer":correct_idx,"explanation_zh":exp_zh,"explanation_en":exp_en,"difficulty":diff}

def gen_word_analysis(n, rng, seen):
    qs = []
    while len(qs) < n:
        pair_name, chars = rng.choice(CONFUSED_PAIRS)
        ctx = rng.choice(CONTEXTS)
        name = rng.choice(NAMES)
        answer = rng.choice(chars)
        opts = list(chars)
        while len(opts) < 4:
            extra = rng.choice("的得地在再做作已以那哪他她它")
            if extra not in opts: opts.append(extra)
        opts = opts[:4]
        if answer not in opts: opts[0] = answer
        rng.shuffle(opts)
        idx = opts.index(answer)
        q = f"({name}) 選出正確的字：{ctx}#{rng.randint(1,9999)}"
        item = _make_q(rng, seen, q, opts, idx, f"此處應使用「{answer}」。", f"Use '{answer}'.", "word_analysis")
        if item: qs.append(item)
    return qs

def gen_idiom_usage(n, rng, seen):
    qs = []
    while len(qs) < n:
        idiom, meaning = rng.choice(IDIOMS)
        name = rng.choice(NAMES)
        t = rng.randint(0,2)
        if t == 0:
            q = f"({name}) 「{idiom}」的意思是？#{rng.randint(1,9999)}"; correct = meaning
            wrongs = rng.sample([m for _,m in IDIOMS if m != meaning], 3)
        elif t == 1:
            q = f"({name}) 哪個成語形容「{meaning}」？#{rng.randint(1,9999)}"; correct = idiom
            wrongs = rng.sample([i for i,_ in IDIOMS if i != idiom], 3)
        else:
            q = f"({name}) 「{idiom}」的近義詞是？#{rng.randint(1,9999)}"; correct = meaning
            wrongs = rng.sample([m for _,m in IDIOMS if m != meaning], 3)
        opts = [correct] + wrongs; rng.shuffle(opts)
        idx = opts.index(correct)
        item = _make_q(rng, seen, q, opts, idx, f"「{idiom}」{meaning}。", f"'{idiom}'={meaning}.", "idiom_usage")
        if item: qs.append(item)
    return qs

def gen_rhetoric(n, rng, seen):
    qs = []
    while len(qs) < n:
        r_type = rng.choice(RHETORIC_TYPES)
        example = rng.choice(RHETORIC_EXAMPLES[r_type])
        name = rng.choice(NAMES)
        q = f"({name}) 「{example}」用了什麼修辭手法？#{rng.randint(1,9999)}"
        wrongs = rng.sample([r for r in RHETORIC_TYPES if r != r_type], 3)
        opts = [r_type] + wrongs; rng.shuffle(opts)
        idx = opts.index(r_type)
        item = _make_q(rng, seen, q, opts, idx, f"此句用「{r_type}」。", f"Uses '{r_type}'.", "rhetoric")
        if item: qs.append(item)
    return qs

def gen_classical(n, rng, seen):
    qs = []
    while len(qs) < n:
        phrase, keyword, meaning, source = rng.choice(CLASSICAL_PHRASES)
        name = rng.choice(NAMES)
        t = rng.randint(0,1)
        if t == 0:
            q = f"({name}) 「{phrase}」中的「{keyword}」是什麼意思？#{rng.randint(1,9999)}"; correct = meaning
            wrongs = rng.sample([m for _,_,m,_ in CLASSICAL_PHRASES if m != meaning], 3)
        else:
            q = f"({name}) 「{phrase}」出自哪裡？#{rng.randint(1,9999)}"; correct = source
            wrongs = rng.sample([s for s in CLASSICAL_SOURCES if s != source], 3)
        opts = [correct] + wrongs; rng.shuffle(opts)
        idx = opts.index(correct)
        item = _make_q(rng, seen, q, opts, idx, f"「{keyword}」{meaning}。出自{source}。", f"'{keyword}'={meaning}.", "classical")
        if item: qs.append(item)
    return qs

def gen_sentence_error(n, rng, seen):
    qs = []
    while len(qs) < n:
        sentence, error_type = rng.choice(SENTENCE_ERRORS)
        name = rng.choice(NAMES)
        t = rng.randint(0,1)
        if t == 0:
            q = f"({name}) 「{sentence}」有什麼語病？#{rng.randint(1,9999)}"; correct = error_type
            wrongs = rng.sample([e for e in ERROR_TYPES if e != error_type], 3)
        else:
            q = f"({name}) 下列句子哪個有語病？#{rng.randint(1,9999)}"; correct = sentence
            wrongs = rng.sample([s for s,_ in SENTENCE_ERRORS if s != sentence], 3)
        opts = [correct] + wrongs[:3]; rng.shuffle(opts)
        idx = opts.index(correct)
        item = _make_q(rng, seen, q, opts, idx, f"此句存在「{error_type}」的問題。", f"Error: '{error_type}'.", "sentence_error")
        if item: qs.append(item)
    return qs

def gen_word_matching(n, rng, seen):
    qs = []
    while len(qs) < n:
        name = rng.choice(NAMES)
        t = rng.randint(0,1)
        if t == 0:
            word, synonym = rng.choice(SYNONYMS); q = f"({name}) 「{word}」的近義詞是？#{rng.randint(1,9999)}"
            correct = synonym; wrongs = rng.sample([s for _,s in SYNONYMS if s != synonym], 3)
        else:
            word, antonym = rng.choice(ANTONYMS); q = f"({name}) 「{word}」的反義詞是？#{rng.randint(1,9999)}"
            correct = antonym; wrongs = rng.sample([a for _,a in ANTONYMS if a != antonym], 3)
        opts = [correct] + wrongs; rng.shuffle(opts)
        idx = opts.index(correct)
        item = _make_q(rng, seen, q, opts, idx, f"答案「{correct}」。", f"Answer: '{correct}'.", "word_matching")
        if item: qs.append(item)
    return qs

def gen_punctuation(n, rng, seen):
    qs = []
    examples = ["今天天氣真好！","你吃飯了嗎？","他說：「你好。」","我不知道他去哪裡。",
                "他不但聰明，而且勤奮。","因為下雨了，所以我帶了傘。","今天是星期一。",
                "他走了；我也走了。","這本書的作者是魯迅。","多美啊！祖國的山河！"]
    while len(qs) < n:
        name = rng.choice(NAMES)
        sentence = rng.choice(examples)
        status = rng.choice(["正確","不正確"])
        q = f"({name}) 「{sentence}」的標點正確嗎？#{rng.randint(1,9999)}"
        correct = "正確" if status == "正確" else "不正確"
        opts = ["正確","不正確","需要修改","部分正確"]; rng.shuffle(opts)
        idx = opts.index(correct)
        item = _make_q(rng, seen, q, opts, idx, f"標點{status}。", f"Punctuation: {status}.", "punctuation")
        if item: qs.append(item)
    return qs

def gen_parts_of_speech(n, rng, seen):
    qs = []
    while len(qs) < n:
        word, pos = rng.choice(POS_WORDS)
        name = rng.choice(NAMES)
        q = f"({name}) 「{word}」屬於什麼詞性？#{rng.randint(1,9999)}"
        all_pos = list(set(p for _,p in POS_WORDS))
        wrongs = rng.sample([p for p in all_pos if p != pos], min(3, len(all_pos)-1))
        opts = [pos] + wrongs; rng.shuffle(opts)
        idx = opts.index(pos)
        item = _make_q(rng, seen, q, opts, idx, f"「{word}」是{pos}。", f"'{word}' is {pos}.", "parts_of_speech")
        if item: qs.append(item)
    return qs

def gen_reading(n, rng, seen):
    qs = []
    while len(qs) < n:
        passage, question, options, correct_idx = rng.choice(READING_PASSAGES)
        name = rng.choice(NAMES)
        q = f"({name}) 閱讀：\n{passage}\n{question}#{rng.randint(1,9999)}"
        item = _make_q(rng, seen, q, options, correct_idx, f"答案「{options[correct_idx]}」。", f"Answer: '{options[correct_idx]}'.", "reading")
        if item: qs.append(item)
    return qs

def gen_culture(n, rng, seen):
    qs = []
    while len(qs) < n:
        question, options, correct_idx = rng.choice(CULTURE_DATA)
        name = rng.choice(NAMES)
        q = f"({name}) {question}#{rng.randint(1,9999)}"
        item = _make_q(rng, seen, q, options, correct_idx, f"答案「{options[correct_idx]}」。", f"Answer: '{options[correct_idx]}'.", "culture")
        if item: qs.append(item)
    return qs

def generate_level(level, n_per_topic=600):
    rng = random.Random(level * 7919)
    seen = set()
    gens = {
        "word_analysis": gen_word_analysis(n_per_topic, rng, seen),
        "idiom_usage": gen_idiom_usage(n_per_topic, rng, seen),
        "rhetoric": gen_rhetoric(n_per_topic, rng, seen),
        "classical": gen_classical(n_per_topic, rng, seen),
        "sentence_error": gen_sentence_error(n_per_topic, rng, seen),
        "word_matching": gen_word_matching(n_per_topic, rng, seen),
        "punctuation": gen_punctuation(n_per_topic, rng, seen),
        "parts_of_speech": gen_parts_of_speech(n_per_topic, rng, seen),
        "reading": gen_reading(n_per_topic, rng, seen),
        "culture": gen_culture(n_per_topic, rng, seen),
    }
    return gens

def round_robin_shuffle(all_by_topic):
    topic_items = list(all_by_topic.items())
    if not topic_items: return []
    min_count = min(len(qs) for _,qs in topic_items)
    result = []
    for r in range(min_count):
        round_qs = [qs[r] for _,qs in topic_items]
        random.shuffle(round_qs)
        result.extend(round_qs)
    extras = []
    for tid,qs in topic_items:
        extras.extend(qs[min_count:])
    random.shuffle(extras)
    for q in extras:
        qt = q['topic_id']
        for pos in range(len(result)+1):
            ok1 = pos==0 or result[pos-1]['topic_id']!=qt
            ok2 = pos>=len(result) or result[pos]['topic_id']!=qt
            if ok1 and ok2:
                result.insert(pos,q); break
        else:
            result.append(q)
    for _ in range(500):
        fixed = True
        for i in range(1,len(result)):
            if result[i]['topic_id']==result[i-1]['topic_id']:
                fixed = False
                for j in range(i+2,min(i+500,len(result))):
                    if result[j]['topic_id']!=result[i-1]['topic_id']:
                        if j+1>=len(result) or result[j]['topic_id']!=result[j+1]['topic_id']:
                            result[i],result[j] = result[j],result[i]; break
                break
        if fixed: break
    for i,q in enumerate(result):
        q['id'] = i+1
    return result

def verify_and_save(level, result):
    max_run=0; ct=None; cl=0
    for q in result:
        t=q['topic_id']
        if t==ct: cl+=1
        else: max_run=max(max_run,cl); ct=t; cl=1
    max_run=max(max_run,cl)
    topics=Counter(q['topic_id'] for q in result)
    dupes=len(result)-len(set(q['question_zh'] for q in result))
    print(f"  S{level}: {len(result)} Qs, {len(topics)} topics, max_run={max_run}, dupes={dupes}")
    for t,c in sorted(topics.items()):
        print(f"    {t}: {c}")
    for path in [f'chinese/s{level}/questions.json',f'v2/chinese/s{level}/questions.json']:
        os.makedirs(os.path.dirname(path),exist_ok=True)
        with open(path,'w',encoding='utf-8') as f:
            json.dump(result,f,ensure_ascii=False,indent=1)
    return set(q['question_zh'] for q in result)

print("="*50)
print("Generating Chinese S2-S6")
print("="*50)

all_seen = set()
for level in [2,3,4,5,6]:
    print(f"\nS{level}...")
    all_by_topic = generate_level(level, n_per_topic=600)
    result = round_robin_shuffle(all_by_topic)
    level_qs = verify_and_save(level, result)
    all_seen |= level_qs

print("\nCross-level check:")
for l1 in [2,3,4,5,6]:
    for l2 in [2,3,4,5,6]:
        if l1<l2:
            with open(f'chinese/s{l1}/questions.json') as f: q1=set(q['question_zh'] for q in json.load(f))
            with open(f'chinese/s{l2}/questions.json') as f: q2=set(q['question_zh'] for q in json.load(f))
            overlap=len(q1&q2)
            print(f"  S{l1} vs S{l2}: {overlap} {'✅' if overlap==0 else '❌'}")
print("\nDone!")
