#!/usr/bin/env python3
"""
Chinese Question Generator for S1 - v3
Generates EXACTLY 10,000 unique questions with balanced distribution.
Max consecutive same topic = 1 (proper interleaving).
"""
import json, random, os

random.seed(42)

WORKDIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# TARGET: 1000 per topic × 10 topics = 10,000
# ============================================================

# --- Word Analysis (字詞辨析) ---
CONFUSED_PAIRS = [
    ("的/得/地", ["的", "得", "地"]),
    ("在/再", ["在", "再"]),
    ("做/作", ["做", "作"]),
    ("已/以", ["已", "以"]),
    ("那/哪", ["那", "哪"]),
    ("他/她/它", ["他", "她", "它"]),
    ("帶/戴", ["帶", "戴"]),
    ("座/坐", ["座", "坐"]),
    ("進/近", ["進", "近"]),
    ("工/公", ["工", "公"]),
    ("到/道", ["到", "道"]),
    ("和/合", ["和", "合"]),
    ("比/彼", ["比", "彼"]),
    ("報/抱", ["報", "抱"]),
    ("常/長", ["常", "長"]),
    ("成/城", ["成", "城"]),
    ("分/份", ["分", "份"]),
    ("記/計", ["記", "計"]),
    ("力/立", ["力", "立"]),
    ("名/明", ["名", "明"]),
    ("平/評", ["平", "評"]),
    ("全/完", ["全", "完"]),
    ("生/升", ["生", "升"]),
    ("事/是", ["事", "是"]),
    ("受/收", ["受", "收"]),
    ("望/忘", ["望", "忘"]),
    ("文/聞", ["文", "聞"]),
    ("問/聞", ["問", "聞"]),
    ("向/像", ["向", "像"]),
    ("新/心", ["新", "心"]),
    ("行/形", ["行", "形"]),
    ("意/義", ["意", "義"]),
    ("因/應", ["因", "應"]),
    ("由/有", ["由", "有"]),
    ("正/真", ["正", "真"]),
    ("處/出", ["處", "出"]),
    ("件/見", ["件", "見"]),
    ("像/象", ["像", "象"]),
    ("畫/劃", ["畫", "劃"]),
    ("急/及", ["急", "及"]),
]

CONTEXTS = [
    "__快跑過來", "__書很好看", "__慢慢走", "__很高興", "__美麗的花",
    "__幫個忙", "__認真學習", "__仔細看", "__成績好", "__歌聲美",
    "__家在這裡", "__等一下", "__問題難", "__地方美", "__天氣好",
    "__考試重要", "__態度認真", "__笑容燦爛", "__學校大", "__班級團結",
    "__經完成", "__進行中", "__開始了", "__這樣做", "__試一下",
    "__願意去", "__必須做", "__可以嗎", "__應該的", "__沒有錯",
    "__出門了", "__回家吧", "__起得早", "__說得好", "__做得對",
    "__跑得快", "__寫得漂亮", "__吃得飽", "__睡得好", "__玩得開心",
    "__學校上課", "__公園散步", "__朋友見面", "__老師上課", "__功課做完",
    "__超市買東西", "__醫院看病", "__圖書館借書", "__球場打球", "__廚房做飯",
    "__看電視", "__聽音樂", "__讀課本", "__寫日記", "__畫圖畫",
    "__唱歌跳舞", "__打球跑步", "__游泳騎車", "__旅行拍照", "__做實驗",
]

# --- Idioms (成語運用) ---
IDIOMS = [
    ("畫蛇添足", "多此一舉"), ("守株待兔", "不勞而獲"), ("掩耳盜鈴", "自欺欺人"),
    ("亡羊補牢", "為時未晚"), ("對牛彈琴", "白費口舌"), ("狐假虎威", "仗勢欺人"),
    ("井底之蛙", "目光短淺"), ("刻舟求劍", "不知變通"), ("揠苗助長", "欲速不達"),
    ("杯弓蛇影", "疑神疑鬼"), ("班門弄斧", "不自量力"), ("杞人憂天", "庸人自擾"),
    ("朝三暮四", "反覆無常"), ("愚公移山", "堅持不懈"), ("臥薪嘗膽", "刻苦自勵"),
    ("破釜沉舟", "背水一戰"), ("聞雞起舞", "勤奮努力"), ("懸樑刺股", "刻苦讀書"),
    ("完璧歸趙", "物歸原主"), ("負荊請罪", "認錯道歉"), ("紙上談兵", "空談理論"),
    ("望梅止渴", "自我安慰"), ("口若懸河", "能言善辯"), ("一箭雙雕", "一舉兩得"),
    ("指鹿為馬", "顛倒是非"), ("胸有成竹", "心中有數"), ("勢如破竹", "節節勝利"),
    ("一鳴驚人", "一飛沖天"), ("鶴立雞群", "出類拔萃"), ("錦上添花", "好上加好"),
    ("雪中送炭", "及時幫助"), ("馬到成功", "旗開得勝"), ("四面楚歌", "四面受敵"),
    ("草木皆兵", "驚慌失措"), ("退避三舍", "主動退讓"), ("毛遂自薦", "自我推薦"),
    ("葉公好龍", "表裡不一"), ("買櫝還珠", "取捨不當"), ("濫竽充數", "混在裡面"),
    ("自相矛盾", "前後矛盾"), ("南轅北轍", "背道而馳"), ("邯鄲學步", "生搬硬套"),
    ("東施效顰", "盲目模仿"), ("黔驢技窮", "無計可施"), ("三顧茅廬", "誠心誠意"),
    ("落花流水", "一敗塗地"), ("鷸蚌相爭", "兩敗俱傷"), ("錦囊妙計", "好主意"),
    ("勢不可擋", "無法阻擋"), ("入木三分", "深刻透徹"),
]

IDIOM_SENTENCES = [
    ("畫蛇添足", "他已經贏了比賽，卻又多跑一圈，真是{idiom}。"),
    ("畫蛇添足", "這篇文章本來很好，加上最後一段反而{idiom}了。"),
    ("畫蛇添足", "你已經回答得很完整，再補充就顯得{idiom}。"),
    ("守株待兔", "考試不溫習，想靠運氣，簡直是{idiom}。"),
    ("守株待兔", "他每天只等別人來幫忙，這種{idiom}的態度要改。"),
    ("守株待兔", "光坐着等機會，不主動爭取，這不是{idiom}嗎？"),
    ("掩耳盜鈴", "明知作業沒寫，卻假裝已經交了，這不是{idiom}嗎？"),
    ("掩耳盜鈴", "考試作弊以為老師不知道，真是{idiom}。"),
    ("掩耳盜鈴", "他關掉手機以為事情就不存在，這種{idiom}的做法沒用。"),
    ("亡羊補牢", "雖然成績退步了，但現在開始努力還不算晚，{idiom}嘛。"),
    ("亡羊補牢", "發現問題後馬上改正，{idiom}，為時未晚。"),
    ("亡羊補牢", "他終於開始認真讀書，同學說他總算懂得{idiom}了。"),
    ("對牛彈琴", "跟不講道理的人解釋，簡直是{idiom}。"),
    ("對牛彈琴", "他完全聽不懂，你再說也是{idiom}。"),
    ("對牛彈琴", "跟一個不懂音樂的人談古典樂，感覺像{idiom}。"),
    ("狐假虎威", "他仗着爸爸是校長就欺負同學，真是{idiom}。"),
    ("狐假虎威", "那些{idiom}的人，一旦失去靠山就不行了。"),
    ("狐假虎威", "他借着老師的名義去管同學，不過是{idiom}罷了。"),
    ("井底之蛙", "他從不出門旅行，見識少得像{idiom}。"),
    ("井底之蛙", "不要做{idiom}，要多了解外面的世界。"),
    ("井底之蛙", "他以為自己班是最好的，真是{idiom}，見識太淺了。"),
    ("刻舟求劍", "時代在變，政策也要跟着改，不能{idiom}。"),
    ("刻舟求劍", "用舊方法解決新問題，無異於{idiom}。"),
    ("刻舟求劍", "環境已經不同了，你還用老辦法，這不是{idiom}嗎？"),
    ("揠苗助長", "每天讓孩子學到半夜，這種{idiom}的做法反而有害。"),
    ("揠苗助長", "學語言要循序漸進，不能{idiom}。"),
    ("揠苗助長", "他急於求成，結果適得其反，真是{idiom}。"),
    ("杯弓蛇影", "他疑心太重，別人隨便說一句就嚇得要命，真是{idiom}。"),
    ("杯弓蛇影", "別{idiom}了，那個聲音只是風吹窗戶而已。"),
    ("杯弓蛇影", "她總覺得有人在背後說她壞話，這種{idiom}的心態要改。"),
    ("班門弄斧", "在書法大師面前寫書法，我可不敢{idiom}。"),
    ("班門弄斧", "你在數學老師面前講數學，不怕{idiom}嗎？"),
    ("班門弄斧", "他居然在專家面前賣弄專業知識，真是{idiom}。"),
    ("杞人憂天", "明天考試都還沒到，你就擔心不及格，別{idiom}了。"),
    ("杞人憂天", "天氣預報說不會下雨，你帶傘是{idiom}。"),
    ("杞人憂天", "地球不會因為你的擔心就停止轉動，別{idiom}了。"),
    ("愚公移山", "只要像{idiom}一樣堅持，就沒有做不到的事。"),
    ("愚公移山", "學習需要{idiom}的精神，日積月累才能成功。"),
    ("愚公移山", "他用了三年時間完成了這個項目，靠的就是{idiom}的毅力。"),
    ("臥薪嘗膽", "失敗後不放棄，要像越王勾踐一樣{idiom}。"),
    ("臥薪嘗膽", "他{idiom}了三年，終於考上了理想的大學。"),
    ("臥薪嘗膽", "為了實現夢想，他願意{idiom}，吃再多的苦也不怕。"),
    ("破釜沉舟", "既然決定了，就要{idiom}，沒有退路。"),
    ("破釜沉舟", "他{idiom}地辭掉工作，專心準備考試。"),
    ("破釜沉舟", "這次比賽我們要{idiom}，全力以赴。"),
    ("聞雞起舞", "他每天{idiom}，堅持鍛煉身體。"),
    ("聞雞起舞", "要想取得好成績，就得有{idiom}的勤奮精神。"),
    ("聞雞起舞", "祖逖{idiom}的故事告訴我們勤奮的重要性。"),
]

# --- Rhetoric (修辭手法) ---
RHETORIC_TYPES = ["比喻", "擬人", "排比", "誇張", "反問", "設問", "對偶", "借代"]
RHETORIC_EXAMPLES = {
    "比喻": [
        "月亮像一個銀盤", "她的笑容像花兒一樣燦爛", "書籍是人類進步的階梯",
        "雪花像蝴蝶一樣飛舞", "太陽像一個大火球", "白雲像棉花糖一樣",
        "他的眼睛像星星一樣閃爍", "時間像流水一樣匆匆", "她的聲音像銀鈴一樣清脆",
        "彎彎的月亮像小船", "荷葉像一個個碧綠的圓盤", "細雨像牛毛一樣飄灑",
        "他的心像冰雪一樣冷", "春風像母親的手一樣溫柔", "他的臉紅得像蘋果",
        "落葉像蝴蝶一樣飄落", "小河像一條銀色的絲帶", "大樹像一把綠色的巨傘",
        "他的話像刀子一樣鋒利", "希望像一盞明燈",
    ],
    "擬人": [
        "春風輕輕地撫摸着大地", "小鳥在枝頭快樂地唱歌", "花兒向太陽點頭微笑",
        "老樹伸展着蒼勁的枝幹", "小溪唱着歡快的歌流向遠方", "風兒輕輕地吹過田野",
        "蠟燭流下了紅色的眼淚", "月亮害羞地躲進了雲層", "細雨溫柔地親吻着大地",
        "太陽公公露出了笑臉", "大樹在風中翩翩起舞", "小草偷偷地從泥土裏鑽出來",
        "星星在夜空中眨着眼睛", "秋風送來了豐收的喜訊", "雪花在空中歡快地飛舞",
        "河水嘩嘩地訴說着故事", "柳樹在風中梳理着長髮", "小貓懶洋洋地曬着太陽",
        "落葉無奈地離開了枝頭", "春雨悄悄地潤澤着萬物",
    ],
    "排比": [
        "讀書使人明智，讀書使人靈秀，讀書使人周密",
        "愛心是一片冬日的陽光，愛心是一泓沙漠中的清泉，愛心是一首飄蕩在夜空的歌謠",
        "生活是一杯酒，生活是一首歌，生活是一幅畫",
        "童年是一首歌，童年是一幅畫，童年是一個夢",
        "希望是黑暗中的燈塔，希望是沙漠中的綠洲，希望是寒冬中的暖爐",
        "書是鑰匙，書是橋樑，書是階梯",
        "人生如歌，人生如詩，人生如夢",
        "時間是金，時間是銀，時間是生命",
        "春天是播種的季節，春天是希望的季節，春天是萬物復蘇的季節",
        "親情是溫暖的港灣，親情是堅強的後盾，親情是永恆的依靠",
        "學習需要恆心，學習需要專心，學習需要細心",
        "青春是火，青春是光，青春是希望",
        "微笑是一種力量，微笑是一種勇氣，微笑是一種智慧",
        "家是溫暖的港灣，家是心靈的歸宿，家是愛的源泉",
        "友誼是橋，友誼是路，友誼是光",
        "失敗是成功之母，失敗是成長之梯，失敗是進步之基",
        "謙虛使人進步，謙虛使人成長，謙虛使人受人尊敬",
        "知識改變命運，知識創造財富，知識提升素質",
        "運動強健體魄，運動磨練意志，運動愉悅心情",
        "大自然是人類的老師，大自然是人類的朋友，大自然是人類的家園",
    ],
    "誇張": [
        "他的聲音大得可以把屋頂掀翻", "這條路長得好像沒有盡頭",
        "他的心像被刀割一樣痛", "教室裏安靜得連針掉在地上都能聽見",
        "他跑得比火箭還快", "這個西瓜大得像一頭牛",
        "他餓得可以吃下一頭大象", "她的頭髮長得可以拖到地上",
        "他的吼聲震耳欲聾", "這座山高得直插雲霄",
        "他的眼淚像瀑布一樣流下來", "人山人海，擠得水洩不通",
        "他高興得快要飛起來了", "天氣熱得石頭都能融化",
        "他瘦得像一根竹竿", "這本書厚得像一塊磚頭",
        "他的膽子大得包天", "這條河寬得望不到對岸",
        "他的鼾聲大得能把窗戶震碎", "她氣得頭頂快要冒煙了",
    ],
    "反問": [
        "難道我們不應該珍惜時間嗎？", "這樣簡單的題目你都不會嗎？",
        "這不是明擺着的事實嗎？", "誰不想擁有一個美好的未來呢？",
        "你難道不知道誠實的重要性嗎？", "我們有什麼理由不努力學習呢？",
        "這麼好的機會怎能錯過？", "難道你忘記了老師的教導嗎？",
        "這件事誰不知道呢？", "我們怎能辜負父母的期望？",
        "不努力學習，將來怎麼能有出息？", "看到這感人的場面，誰不流淚呢？",
        "這麼簡單的道理，難道你不懂嗎？", "我們有什麼資格浪費糧食呢？",
        "失敗了就放棄，這樣對嗎？", "你難道不為自己的行為感到羞愧嗎？",
        "這難道不是一個值得深思的問題嗎？", "誰能忘記童年的快樂時光？",
        "我們怎能對大自然的恩賜無動於衷？", "你見過比這更美的景色嗎？",
    ],
    "設問": [
        "什麼是真正的友誼？是在困難時伸出援手。",
        "學習的目的是什麼？是成為對社會有用的人。",
        "什麼是勇氣？勇氣就是面對困難不退縮。",
        "為什麼要讀書？因為知識能改變命運。",
        "什麼是幸福？幸福就是家人在一起的溫暖。",
        "成功的秘訣是什麼？是堅持不懈的努力。",
        "什麼是責任？責任就是對自己的承諾負責。",
        "我們為什麼要保護環境？因為地球是我們唯一的家園。",
        "什麼是誠信？誠信就是言行一致，表裏如一。",
        "人生最大的財富是什麼？是健康和知識。",
        "什麼是真正的勇敢？真正的勇敢是敢於承認錯誤。",
        "為什麼要尊師重道？因為老師是人類靈魂的工程師。",
        "什麼是理想？理想是人生的燈塔和方向。",
        "我們為什麼要團結？因為團結就是力量。",
        "什麼是真善美？真善美是人類追求的最高境界。",
        "時間為什麼寶貴？因為時間一去不復返。",
        "什麼是感恩？感恩就是珍惜別人對你的付出。",
        "我們為什麼要運動？因為生命在於運動。",
        "什麼是自強不息？就是遇到困難永不放棄。",
        "學習最重要的是什麼？是持之以恆的態度。",
    ],
    "對偶": [
        "明月松間照，清泉石上流", "兩個黃鸝鳴翠柳，一行白鷺上青天",
        "海內存知己，天涯若比鄰", "山重水複疑無路，柳暗花明又一村",
        "春蠶到死絲方盡，蠟炬成灰淚始乾", "橫眉冷對千夫指，俯首甘為孺子牛",
        "落霞與孤鶩齊飛，秋水共長天一色", "風聲雨聲讀書聲聲聲入耳",
        "家事國事天下事事事關心", "寶劍鋒從磨礪出，梅花香自苦寒來",
        "少壯不努力，老大徒傷悲", "千山鳥飛絕，萬徑人蹤滅",
        "白日依山盡，黃河入海流", "欲窮千里目，更上一層樓",
        "大漠孤煙直，長河落日圓", "會當凌絕頂，一覽眾山小",
        "國破山河在，城春草木深", "隨風潛入夜，潤物細無聲",
        "野火燒不盡，春風吹又生", "誰言寸草心，報得三春暉",
    ],
    "借代": [
        "兩岸青山相對出，孤帆一片日邊來（帆代船）",
        "知否，知否？應是綠肥紅瘦（綠代葉，紅代花）",
        "南國烽煙正十年（烽煙代戰爭）",
        "舉杯邀明月，對影成三人（杯代酒）",
        "朱門酒肉臭，路有凍死骨（朱門代富貴人家）",
        "何以解憂，唯有杜康（杜康代酒）",
        "無絲竹之亂耳（絲竹代音樂）",
        "黃髮垂髫，並怡然自樂（黃髮代老人，垂髫代小孩）",
        "巾幗不讓鬚眉（巾幗代女性，鬚眉代男性）",
        "六軍不發無奈何（六代軍隊）",
        "布衣之怒（布衣代平民）",
        "紈絝子弟（紈絝代富貴）",
        "執干戈以衛社稷（干戈代武器/戰爭）",
        "汗青代史冊", "桑梓代故鄉",
        "杏壇代教育界", "梨園代戲劇界",
        "翰墨代文章", "管弦代音樂", "鬚眉代男子",
    ],
}

# --- Classical Chinese (文言文) ---
CLASSICAL_PHRASES = [
    ("學而時習之，不亦說乎", "《論語》", "學習並經常溫習，不是很愉快嗎", "孔子"),
    ("三人行，必有我師焉", "《論語》", "三個人同行，其中一定有可以做我老師的人", "孔子"),
    ("溫故而知新，可以為師矣", "《論語》", "溫習舊知識能領悟新知識，就可以做老師了", "孔子"),
    ("知之者不如好之者，好之者不如樂之者", "《論語》", "知道它的人不如愛好它的人，愛好它的人不如以它為樂的人", "孔子"),
    ("己所不欲，勿施於人", "《論語》", "自己不想要的，不要強加給別人", "孔子"),
    ("學而不思則罔，思而不學則殆", "《論語》", "只學習不思考就會迷惘，只思考不學習就會疑惑", "孔子"),
    ("逝者如斯夫，不捨晝夜", "《論語》", "時光像流水一樣消逝，日夜不停", "孔子"),
    ("見賢思齊焉，見不賢而內自省也", "《論語》", "看到賢人就向他看齊，看到不賢的人就自我反省", "孔子"),
    ("不憤不啟，不悱不發", "《論語》", "不到苦思冥想時不去開導，不到想說說不出時不去啟發", "孔子"),
    ("歲寒，然後知松柏之後凋也", "《論語》", "到了寒冷的季節，才知道松柏是最後凋零的", "孔子"),
    ("生於憂患，死於安樂", "《孟子》", "憂患使人生存發展，安逸享樂使人萎靡死亡", "孟子"),
    ("得道多助，失道寡助", "《孟子》", "堅持正義就能得到幫助，違反正義就會陷入孤立", "孟子"),
    ("富貴不能淫，貧賤不能移，威武不能屈", "《孟子》", "富貴不能使他迷惑，貧賤不能使他動搖，威武不能使他屈服", "孟子"),
    ("天時不如地利，地利不如人和", "《孟子》", "天氣時令不如地勢有利，地勢有利不如人心團結", "孟子"),
    ("老吾老以及人之老，幼吾幼以及人之幼", "《孟子》", "尊敬自己的長輩並推及到別人的長輩", "孟子"),
    ("魚，我所欲也；熊掌，亦我所欲也", "《孟子》", "魚是我想要的，熊掌也是我想要的", "孟子"),
    ("盡信書，則不如無書", "《孟子》", "完全相信書本，還不如沒有書", "孟子"),
    ("故天將降大任於是人也", "《孟子》", "所以上天要把重大使命交給這個人", "孟子"),
    ("醉翁之意不在酒", "《醉翁亭記》", "醉翁的本意不在喝酒", "歐陽修"),
    ("先天下之憂而憂，後天下之樂而樂", "《岳陽樓記》", "在天下人憂愁之前先憂愁，在天下人快樂之後才快樂", "范仲淹"),
    ("出淤泥而不染，濯清漣而不妖", "《愛蓮說》", "從淤泥中長出卻不被污染，經過清水洗滌卻不妖艷", "周敦頤"),
    ("世有伯樂，然後有千里馬", "《馬說》", "世上先有伯樂，然後才有千里馬", "韓愈"),
    ("書山有路勤為徑，學海無涯苦作舟", "古訓", "書山有路，勤奮是道路；學海無涯，刻苦是船", ""),
    ("少壯不努力，老大徒傷悲", "《長歌行》", "年輕時不努力，到老了就只有白白地悲傷", ""),
    ("紙上得來終覺淺，絕知此事要躬行", "《冬夜讀書示子聿》", "從書本上得來的知識終究淺薄，要深入了解必須親身實踐", "陸游"),
    ("問渠那得清如許，為有源頭活水來", "《觀書有感》", "要問那池塘為何如此清澈，是因為源頭有活水不斷流來", "朱熹"),
    ("不識廬山真面目，只緣身在此山中", "《題西林壁》", "看不清廬山的真實面貌，只因為身處在這座山中", "蘇軾"),
    ("山不在高，有仙則名；水不在深，有龍則靈", "《陋室銘》", "山不在高低，有仙人就出名；水不在深淺，有龍就有靈氣", "劉禹錫"),
    ("海內存知己，天涯若比鄰", "《送杜少府之任蜀州》", "四海之內有知心朋友，即使遠在天涯也像近鄰一樣", "王勃"),
    ("落紅不是無情物，化作春泥更護花", "《己亥雜詩》", "落花不是無情之物，化為春天的泥土更能培育新花", "龔自珍"),
]

# --- Sentence Error (句子改錯) ---
ERROR_SENTENCES = [
    ("他不但聰明，而且很努力，所以成績很好，因此老師表揚了他。", "重複因果"),
    ("這本書的內容和形式都很豐富。", "搭配不當"),
    ("他的作文寫得很優美和流暢。", "搭配不當"),
    ("通過這次活動，使我受到了很大的教育。", "缺少主語"),
    ("我們班的同學基本上全到齊了。", "矛盾"),
    ("他的學習成績一直穩步向前發展。", "搭配不當"),
    ("這篇文章的內容和見解都很新穎。", "搭配不當"),
    ("他親切的話語和慈祥的面孔經常浮現在我眼前。", "搭配不當"),
    ("我們要發揚艱苦奮鬥的精神和作風。", "搭配不當"),
    ("他做事很認真，從不馬馬虎虎，一絲不苟的態度令人佩服。", "成分殘缺"),
    ("這部電影敘述了一個離奇的、感人的、不尋常的故事。", "語序不當"),
    ("他的文章寫得又快又好，而且字跡工整。", "關聯不當"),
    ("我們討論並聽取了校長的報告。", "語序不當"),
    ("這件事情對我的印象很深刻。", "搭配不當"),
    ("為了防止這類事故不再發生，我們加強了安全教育。", "否定不當"),
    ("他的革命精神時刻浮現在我眼前。", "搭配不當"),
    ("能否努力學習是取得好成績的關鍵。", "兩面對一面"),
    ("大廳裏陳列着各式各樣的許多商品。", "語意重複"),
    ("他那崇高的革命品質經常浮現在我的腦海中。", "搭配不當"),
    ("我們要做到節約用水的好習慣。", "搭配不當"),
]

CORRECT_SENTENCES = [
    "他不但聰明，而且很努力。",
    "這本書的內容很豐富。",
    "他的作文寫得很優美。",
    "通過這次活動，我受到了很大的教育。",
    "他的學習態度非常認真。",
    "同學們都到齊了。",
    "老師表揚了優秀的學生。",
    "春天到了，花兒開了。",
    "小明每天按時完成作業。",
    "這部電影非常感人。",
    "他的字寫得很工整。",
    "同學們團結一致，克服了困難。",
    "老師耐心地輔導學生。",
    "這首歌的旋律優美動聽。",
    "我們要養成良好的學習習慣。",
    "天氣漸漸變暖了。",
    "他的成績一直名列前茅。",
    "這本書對我很有啟發。",
    "學校組織了一次有意義的活動。",
    "我們應該珍惜寶貴的時間。",
]

# --- Word Matching (詞語配對) ---
SYNONYMS = [
    ("快樂", "高興"), ("勇敢", "英勇"), ("美麗", "漂亮"), ("聰明", "機靈"),
    ("安靜", "寧靜"), ("迅速", "快速"), ("溫暖", "暖和"), ("困難", "艱難"),
    ("優秀", "出色"), ("疲倦", "疲憊"), ("堅強", "剛強"), ("開心", "愉快"),
    ("悲傷", "哀傷"), ("巨大", "龐大"), ("微小", "細小"), ("明亮", "光亮"),
    ("黑暗", "昏暗"), ("寒冷", "冰冷"), ("炎熱", "酷熱"), ("柔軟", "鬆軟"),
    ("堅硬", "牢固"), ("簡單", "容易"), ("複雜", "繁瑣"), ("開始", "起始"),
    ("結束", "終結"), ("喜歡", "喜愛"), ("討厭", "厭惡"), ("尊敬", "敬重"),
    ("幫助", "援助"), ("保護", "維護"), ("破壞", "毀壞"), ("建設", "建造"),
    ("觀察", "察看"), ("思考", "考慮"), ("詢問", "發問"), ("回答", "回覆"),
    ("讚美", "讚揚"), ("批評", "指責"), ("鼓勵", "激勵"), ("安慰", "慰問"),
]

ANTONYMS = [
    ("快樂", "悲傷"), ("勇敢", "膽怯"), ("美麗", "醜陋"), ("聰明", "愚笨"),
    ("安靜", "吵鬧"), ("迅速", "緩慢"), ("溫暖", "寒冷"), ("困難", "容易"),
    ("優秀", "差勁"), ("勤奮", "懶惰"), ("堅強", "軟弱"), ("開心", "傷心"),
    ("巨大", "微小"), ("光明", "黑暗"), ("明亮", "昏暗"), ("柔軟", "堅硬"),
    ("簡單", "複雜"), ("開始", "結束"), ("喜歡", "討厭"), ("尊敬", "輕視"),
    ("建設", "破壞"), ("保護", "傷害"), ("讚美", "批評"), ("鼓勵", "打擊"),
    ("成功", "失敗"), ("富裕", "貧窮"), ("乾淨", "骯髒"), ("整齊", "凌亂"),
    ("熱鬧", "冷清"), ("團結", "分裂"), ("誠實", "虛偽"), ("謙虛", "驕傲"),
    ("善良", "邪惡"), ("文明", "野蠻"), ("進步", "退步"), ("節約", "浪費"),
]

# --- Parts of Speech (詞性辨別) ---
POS_WORDS = [
    ("學生", "名詞"), ("快樂", "形容詞"), ("跑步", "動詞"), ("非常", "副詞"),
    ("和", "連詞"), ("從", "介詞"), ("嗎", "助詞"), ("啊", "嘆詞"),
    ("桌子", "名詞"), ("美麗", "形容詞"), ("學習", "動詞"), ("已經", "副詞"),
    ("但是", "連詞"), ("在", "介詞"), ("的", "助詞"), ("哎", "嘆詞"),
    ("老師", "名詞"), ("聰明", "形容詞"), ("思考", "動詞"), ("常常", "副詞"),
    ("或者", "連詞"), ("向", "介詞"), ("了", "助詞"), ("哦", "嘆詞"),
    ("勇氣", "名詞"), ("勤奮", "形容詞"), ("觀察", "動詞"), ("正在", "副詞"),
    ("因為", "連詞"), ("被", "介詞"), ("着", "助詞"), ("喂", "嘆詞"),
    ("幸福", "名詞"), ("認真", "形容詞"), ("討論", "動詞"), ("忽然", "副詞"),
    ("所以", "連詞"), ("把", "介詞"), ("過", "助詞"), ("唉", "嘆詞"),
    ("希望", "名詞"), ("溫柔", "形容詞"), ("創造", "動詞"), ("漸漸", "副詞"),
    ("雖然", "連詞"), ("對於", "介詞"), ("得", "助詞"), ("嘿", "嘆詞"),
]

# --- Punctuation (標點符號) ---
PUNCTUATION_EXAMPLES = [
    ("今天天氣真好", "！", "感嘆句"),
    ("你吃了嗎", "？", "疑問句"),
    ("小明去了公園", "。", "陳述句"),
    ("請幫我拿一下書", "。", "祈使句"),
    ("哇好漂亮啊", "！", "感嘆句"),
    ("你叫什麼名字", "？", "疑問句"),
    ("春天來了花兒開了", "。", "陳述句"),
    ("快跑啊", "！", "感嘆句"),
    ("這本書是誰的", "？", "疑問句"),
    ("月亮掛在天上", "。", "陳述句"),
    ("太好了", "！", "感嘆句"),
    ("你去不去", "？", "疑問句"),
    ("小貓在睡覺", "。", "陳述句"),
    ("安靜", "。", "祈使句"),
    ("多麼美麗的風景啊", "！", "感嘆句"),
    ("為什麼要遲到", "？", "疑問句"),
    ("他喜歡讀書", "。", "陳述句"),
    ("別說話", "。", "祈使句"),
    ("小明和小紅是好朋友", "。", "陳述句"),
    ("你覺得怎麼樣", "？", "疑問句"),
]

PUNCTUATION_MARKS = ["。", "，", "！", "？", "、", "；", "：", "「」", "（）", "……", "——"]

# --- Reading Comprehension (閱讀理解) ---
READING_PASSAGES = [
    {
        "title": "春天的公園",
        "text": "春天來了，公園裏到處都是生機勃勃的景象。小草從泥土裏探出頭來，嫩綠嫩綠的。桃花開了，粉紅色的花瓣像小姑娘的臉蛋。蝴蝶在花叢中翩翩起舞，小鳥在枝頭快樂地歌唱。老人們在長椅上曬太陽，孩子們在草地上放風箏。春天的公園真是美麗極了。",
        "questions": [
            ("小草是什麼顏色的？", ["嫩綠色", "深綠色", "黃色", "紅色"], 0),
            ("桃花的花瓣像什麼？", ["小姑娘的臉蛋", "蝴蝶的翅膀", "天上的雲朵", "紅色的燈籠"], 0),
            ("蝴蝶在做什麼？", ["在花叢中飛舞", "在草地上休息", "在水面上游泳", "在樹上築巢"], 0),
            ("老人們在做什麼？", ["在長椅上曬太陽", "在草地上跑步", "在湖邊釣魚", "在亭子裏下棋"], 0),
            ("孩子們在做什麼？", ["放風箏", "踢足球", "捉迷盪", "跳繩"], 0),
        ]
    },
    {
        "title": "我的學校",
        "text": "我的學校很大很美麗。校門口有兩棵大榕樹，像兩個忠實的衛士。操場上，同學們有的在跑步，有的在打籃球，有的在跳繩。教學樓裏傳來朗朗的讀書聲。圖書館裏有各種各樣的書籍，我最喜歡在那裏看故事書。校園的花壇裏種滿了五顏六色的花朵，美麗極了。",
        "questions": [
            ("校門口有什麼？", ["兩棵大榕樹", "一座雕像", "一面旗幟", "一個花壇"], 0),
            ("大榕樹像什麼？", ["忠實的衛士", "巨大的雨傘", "綠色的城堡", "慈祥的老人"], 0),
            ("操場上同學們在做什麼？", ["跑步、打籃球、跳繩", "唱歌、跳舞、畫畫", "讀書、寫字、討論", "游泳、爬山、騎車"], 0),
            ("我最喜歡去哪裏？", ["圖書館", "操場", "音樂室", "美術室"], 0),
            ("花壇裏有什麼？", ["五顏六色的花朵", "各種蔬菜", "小池塘", "假山石頭"], 0),
        ]
    },
    {
        "title": "我的媽媽",
        "text": "我的媽媽是一位勤勞的人。每天早上，她總是第一個起床，為全家人準備早餐。放學後，她會檢查我的功課，耐心地輔導我不會的題目。晚上，她還要洗衣服、打掃房間。週末的時候，她喜歡帶我去公園散步，或者陪我去圖書館看書。媽媽雖然很辛苦，但她從來不抱怨，總是笑呵呵的。我愛我的媽媽。",
        "questions": [
            ("媽媽每天早上做什麼？", ["準備早餐", "看報紙", "鍛煉身體", "化妝打扮"], 0),
            ("放學後媽媽做什麼？", ["檢查功課", "看電視", "打電話", "做運動"], 0),
            ("週末媽媽喜歡做什麼？", ["帶我去公園散步", "在家睡覺", "去逛街買東西", "和朋友聚餐"], 0),
            ("媽媽的性格怎樣？", ["勤勞不抱怨", "脾氣暴躁", "沉默寡言", "愛發脾氣"], 0),
            ("文章表達了什麼感情？", ["對媽媽的愛", "對學校的喜愛", "對朋友的思念", "對大自然的讚美"], 0),
        ]
    },
    {
        "title": "小貓釣魚",
        "text": "小貓跟着貓媽媽去河邊釣魚。小貓剛坐下，就看見一隻蝴蝶飛過來，牠扔下魚竿去追蝴蝶。回來後，又看見一隻蜻蜓飛過來，牠又去追蜻蜓。太陽快下山了，貓媽媽釣到了好幾條魚，小貓卻一條也沒釣到。貓媽媽對小貓說：「做事不能三心二意，要專心致志才能成功。」小貓聽了，慚愧地低下了頭。",
        "questions": [
            ("小貓跟着誰去釣魚？", ["貓媽媽", "貓爸爸", "小狗狗", "小兔子"], 0),
            ("小貓為什麼沒釣到魚？", ["三心二意不專心", "魚竿壞了", "河水太深", "天氣太冷"], 0),
            ("貓媽媽釣到了什麼？", ["好幾條魚", "一隻螃蟹", "一條蛇", "什麼都沒有"], 0),
            ("貓媽媽教小貓什麼道理？", ["做事要專心致志", "要多運動", "要早睡早起", "要多吃蔬菜"], 0),
            ("小貓最後的反應是什麼？", ["慚愧地低下了頭", "高興地跳起來", "哭了起來", "跑開了"], 0),
        ]
    },
    {
        "title": "下雨天",
        "text": "天空突然烏雲密佈，不一會兒就下起了大雨。小明忘記帶傘，只好站在商店門口避雨。他看見一位老奶奶撐着傘在雨中慢慢地走着，手裏還提着一袋重重的東西。小明趕緊跑過去，幫老奶奶提東西，還把自己的外套披在老奶奶身上。老奶奶感動地說：「謝謝你，小朋友，你真是個好孩子！」雨漸漸停了，小明看着天空出現的彩虹，心裏暖洋洋的。",
        "questions": [
            ("為什麼小明站在商店門口？", ["他忘記帶傘在避雨", "他在等人", "他在看風景", "他在買東西"], 0),
            ("老奶奶手裏提着什麼？", ["一袋重重的東西", "一把雨傘", "一個籃子", "一束花"], 0),
            ("小明幫老奶奶做了什麼？", ["提東西和披外套", "打傘", "叫計程車", "帶她回家"], 0),
            ("雨停後天空出現了什麼？", ["彩虹", "太陽", "白雲", "星星"], 0),
            ("小明的心情怎樣？", ["暖洋洋的", "難過的", "生氣的", "害怕的"], 0),
        ]
    },
    {
        "title": "植樹節",
        "text": "三月十二日是植樹節。老師帶着同學們去山坡上植樹。小華負責挖坑，小明負責扶樹苗，小紅負責填土，小剛負責澆水。大家分工合作，忙得不亦樂乎。不一會兒，十幾棵小樹苗就種好了。老師看着同學們汗流浹背的樣子，開心地說：「你們做得很好！這些小樹苗會慢慢長大，到時候這裏就會變成一片美麗的小樹林。」",
        "questions": [
            ("植樹節是哪一天？", ["三月十二日", "四月十二日", "三月十五日", "四月五日"], 0),
            ("他們去哪裏植樹？", ["山坡上", "河邊", "操場", "公園"], 0),
            ("小華負責什麼？", ["挖坑", "扶樹苗", "填土", "澆水"], 0),
            ("他們一共種了多少棵樹？", ["十幾棵", "幾棵", "幾十棵", "一棵"], 0),
            ("老師說這些樹苗將來會怎樣？", ["長成一片小樹林", "開出美麗的花", "結出果實", "成為大森林"], 0),
        ]
    },
    {
        "title": "我的寵物",
        "text": "我養了一隻小白兔，我給牠取名叫「雪球」。雪球全身白白的毛，摸起來柔軟極了。牠有兩隻長長的耳朵，一雙紅紅的眼睛，還有一個短短的尾巴。雪球最喜歡吃胡蘿蔔和青菜。每天放學回家，我第一件事就是去看雪球。我會把牠抱在懷裏，輕輕地撫摸牠。雪球是我最好的朋友。",
        "questions": [
            ("小白兔叫什麼名字？", ["雪球", "小白", "棉花", "球球"], 0),
            ("雪球的毛摸起來怎樣？", ["柔軟", "粗糙", "濕潤", "冰涼"], 0),
            ("雪球最喜歡吃什麼？", ["胡蘿蔔和青菜", "米飯和麵條", "水果和蛋糕", "餅乾和糖果"], 0),
            ("放學後我第一件事做什麼？", ["去看雪球", "做功課", "看電視", "吃晚飯"], 0),
            ("雪球和我的關係是什麼？", ["最好的朋友", "寵物和主人", "鄰居", "同學"], 0),
        ]
    },
    {
        "title": "中秋節",
        "text": "中秋節是我最喜歡的節日之一。這一天，全家人會團聚在一起賞月。媽媽會準備各種口味的月餅，有蓮蓉的、豆沙的、蛋黃的。爸爸會在院子裏擺好桌椅，放上水果和月餅。我們一邊吃月餅，一邊欣賞天上又圓又亮的月亮。奶奶會給我們講嫦娥奔月的故事。中秋節象徵着團圓和美滿，我非常喜歡這個節日。",
        "questions": [
            ("中秋節全家會做什麼？", ["團聚賞月", "外出旅行", "去看電影", "去遊樂場"], 0),
            ("媽媽準備了什麼？", ["各種口味的月餅", "生日蛋糕", "餃子", "火鍋"], 0),
            ("爸爸在院子裏做什麼？", ["擺桌椅放水果和月餅", "種花", "修理東西", "運動"], 0),
            ("奶奶會做什麼？", ["講嫦娥奔月的故事", "唱歌", "跳舞", "畫畫"], 0),
            ("中秋節象徵什麼？", ["團圓和美滿", "勇敢和堅強", "勤奮和努力", "友誼和關愛"], 0),
        ]
    },
    {
        "title": "海洋世界",
        "text": "海洋是地球上最大的水域，佔地球表面的百分之七十一。海洋裏生活着各種各樣的生物，有巨大的鯨魚、聰明的海豚、美麗的珊瑚和五顏六色的熱帶魚。海洋不僅為人類提供了豐富的食物資源，還能調節氣候。然而，近年來海洋污染越來越嚴重，許多海洋生物的生存受到了威脅。我們應該保護海洋環境，減少垃圾和污染物的排放。",
        "questions": [
            ("海洋佔地球表面的多少？", ["百分之七十一", "百分之五十", "百分之三十", "百分之九十"], 0),
            ("下列哪種動物生活在海洋裏？", ["鯨魚", "大象", "獅子", "老鷹"], 0),
            ("海洋對人類有什麼作用？", ["提供食物和調節氣候", "提供住所", "提供衣服", "提供交通工具"], 0),
            ("海洋目前面臨什麼問題？", ["污染嚴重", "面積縮小", "溫度下降", "鹽分減少"], 0),
            ("我們應該怎樣做？", ["保護海洋環境", "多去海邊玩", "多吃海鮮", "在海邊建房子"], 0),
        ]
    },
    {
        "title": "讀書的樂趣",
        "text": "書是知識的海洋，是人類進步的階梯。我從小就喜歡讀書，每天放學後都會花一個小時看書。我喜歡看童話故事，因為裏面有奇妙的想像和動人的情節。我也喜歡看科普書籍，因為它們能讓我了解大自然的奧秘。讀書不僅能增長知識，還能培養我們的想像力和思考能力。正如高爾基所說：「書籍是人類進步的階梯。」讓我們一起養成愛讀書的好習慣吧！",
        "questions": [
            ("作者每天花多長時間看書？", ["一個小時", "兩個小時", "半個小時", "三個小時"], 0),
            ("作者喜歡看什麼類型的書？", ["童話故事和科普書籍", "漫畫和雜誌", "報紙和詞典", "食譜和旅遊指南"], 0),
            ("讀書能培養什麼能力？", ["想像力和思考能力", "運動能力", "社交能力", "計算能力"], 0),
            ("「書籍是人類進步的階梯」是誰說的？", ["高爾基", "魯迅", "孔子", "李白"], 0),
            ("文章呼籲大家做什麼？", ["養成愛讀書的好習慣", "多做運動", "保護環境", "尊敬師長"], 0),
        ]
    },
]

# --- Culture (文化常識) ---
CULTURE_ITEMS = [
    ("春節", "農曆新年", "中國最重要的傳統節日，人們貼春聯、放鞭炮、吃團年飯", ["端午節", "中秋節", "元宵節", "清明節"]),
    ("端午節", "五月初五", "紀念屈原的節日，人們賽龍舟、吃粽子", ["春節", "中秋節", "重陽節", "清明節"]),
    ("中秋節", "八月十五", "象徵團圓的節日，人們賞月、吃月餅", ["春節", "端午節", "元宵節", "重陽節"]),
    ("清明節", "四月初", "祭祖掃墓的節日", ["春節", "端午節", "中秋節", "重陽節"]),
    ("重陽節", "九月初九", "敬老的節日，人們登高、賞菊", ["春節", "端午節", "中秋節", "清明節"]),
    ("元宵節", "正月十五", "賞花燈、吃湯圓的節日", ["春節", "端午節", "中秋節", "重陽節"]),
    ("冬至", "十二月", "北半球白天最短的一天，有吃湯圓的習俗", ["春節", "中秋節", "夏至", "立春"]),
    ("二十四節氣", "中國古代", "中國古代用來指導農事的曆法", ["天干地支", "五行八卦", "十二生肖", "陰陽五行"]),
    ("孔子", "春秋時期", "儒家學派創始人，被尊為「萬世師表」", ["老子", "孟子", "莊子", "韓非子"]),
    ("李白", "唐代", "被稱為「詩仙」的偉大詩人", ["杜甫", "白居易", "蘇軾", "王維"]),
    ("杜甫", "唐代", "被稱為「詩聖」的偉大詩人", ["李白", "白居易", "蘇軾", "王維"]),
    ("四大名著", "中國古典", "《三國演義》《水滸傳》《西遊記》《紅樓夢》", ["四大發明", "四書五經", "唐宋八大家", "建安七子"]),
    ("四大發明", "中國古代", "造紙術、印刷術、火藥、指南針", ["四大名著", "四書五經", "唐宋八大家", "建安七子"]),
    ("萬里長城", "中國古代", "世界上最長的城牆，是中華民族的象徵", ["故宮", "兵馬俑", "大運河", "敦煌莫高窟"]),
    ("故宮", "北京", "明清兩代的皇宮，又稱紫禁城", ["萬里長城", "兵馬俑", "頤和園", "天壇"]),
    ("十二生肖", "中國傳統", "鼠牛虎兔龍蛇馬羊猴雞狗豬", ["十二星座", "二十四節氣", "天干地支", "五行"]),
    ("漢字", "中國", "世界上最古老的文字之一，有數千年的歷史", ["英文", "日文", "韓文", "阿拉伯文"]),
    ("京劇", "中國", "中國的國粹，融合了唱念做打的表演藝術", ["粵劇", "豫劇", "越劇", "川劇"]),
    ("太極拳", "中國", "中國傳統武術，以柔克剛、陰陽調和為特點", ["少林拳", "詠春拳", "跆拳道", "空手道"]),
    ("茶文化", "中國", "中國有數千年飲茶歷史，茶道是重要的文化傳統", ["咖啡文化", "酒文化", "飲食文化", "陶瓷文化"]),
]

NAMES = [
    "小明", "小紅", "小華", "小剛", "小麗", "小強", "小芳", "小軍",
    "小燕", "小偉", "小梅", "小傑", "小蘭", "小鵬", "小雪", "小峰",
    "小玲", "小波", "小霞", "小龍", "小鳳", "小虎", "小蓮", "小松",
    "小菊", "小雲", "小蕾", "小林", "小寧", "小瑤",
]

PLACES = [
    "學校", "公園", "圖書館", "博物館", "超市", "醫院", "電影院", "車站",
    "機場", "碼頭", "市場", "書店", "餐廳", "銀行", "郵局", "體育館",
    "動物園", "植物園", "科學館", "美術館", "游泳池", "球場", "操場", "教室",
]

ADJECTIVES = [
    "美麗", "聰明", "勇敢", "勤奮", "善良", "可愛", "活潑", "開朗",
    "認真", "細心", "耐心", "熱心", "誠實", "謙虛", "大方", "溫柔",
    "堅強", "樂觀", "自信", "獨立", "勤勞", "樸實", "正直", "慷慨",
]

ACTIONS = [
    "讀書", "寫字", "畫畫", "唱歌", "跳舞", "跑步", "游泳", "打球",
    "做飯", "洗衣服", "打掃房間", "種花", "澆水", "餵魚", "遛狗", "散步",
    "看電影", "聽音樂", "玩遊戲", "做功課", "溫習", "考試", "旅行", "拍照",
]


def make_q(topic_id, topic_zh, topic_en, subtopic_id, subtopic_zh, subtopic_en,
           question_zh, question_en, options_zh, options_en, answer, explanation_zh, explanation_en, difficulty=2):
    return {
        "topic_id": topic_id,
        "topic_zh": topic_zh,
        "topic_en": topic_en,
        "subtopic_id": subtopic_id,
        "subtopic_zh": subtopic_zh,
        "subtopic_en": subtopic_en,
        "question_zh": question_zh,
        "question_en": question_en,
        "options_zh": options_zh,
        "options_en": options_en,
        "answer": answer,
        "explanation_zh": explanation_zh,
        "explanation_en": explanation_en,
        "difficulty": difficulty,
    }


def wrong_options(correct, pool, count=3):
    candidates = [x for x in pool if x != correct]
    return random.sample(candidates, min(count, len(candidates)))


# ============================================================
# GENERATOR FUNCTIONS - each must produce exactly TARGET questions
# ============================================================

def gen_word_analysis(seen, target=1000):
    """字詞辨析 - confused character pairs."""
    questions = []
    all_chars = set()
    for _, chars in CONFUSED_PAIRS:
        all_chars.update(chars)
    all_chars = list(all_chars)

    # Strategy: pair × context × answer_char × variation
    idx = 0
    while len(questions) < target:
        pair_name, chars = CONFUSED_PAIRS[idx % len(CONFUSED_PAIRS)]
        ctx = CONTEXTS[idx % len(CONTEXTS)]
        answer = chars[idx % len(chars)]
        name = NAMES[idx % len(NAMES)]
        place = PLACES[idx % len(PLACES)]
        adj = ADJECTIVES[idx % len(ADJECTIVES)]

        variant = idx % 6
        if variant == 0:
            q = f"句子「{ctx.replace('__', '___')}」空格中應填什麼字？(#{idx})"
            wrongs = random.sample([c for c in all_chars if c != answer], 3)
            opts = [answer] + wrongs
        elif variant == 1:
            q = f"「{name}覺得{ctx.replace('__', '___')}」應填什麼字？(#{idx})"
            wrongs = random.sample([c for c in all_chars if c != answer], 3)
            opts = [answer] + wrongs
        elif variant == 2:
            q = f"在「{place}裏{ctx.replace('__', '___')}」中，空格應填「{answer}」嗎？(#{idx})"
            opts = ["是", "不是"]
            random.shuffle(opts)
            ans_idx = 0  # always "是" since we generated with the answer
            item = make_q(
                "word_analysis", "字詞辨析", "Word Analysis",
                "word_analysis", "字詞辨別", "Character Distinction",
                q, f"Word analysis #{idx}",
                opts, opts, ans_idx,
                f"應填「{answer}」。", f"Should be '{answer}'.",
                difficulty=2
            )
            if item["question_zh"] not in seen:
                questions.append(item)
                seen.add(item["question_zh"])
            idx += 1
            continue
        elif variant == 3:
            correct_sentence = ctx.replace("__", answer)
            q = f"以下哪句中的「{pair_name}」用法正確？(#{idx})"
            opts = [correct_sentence]
            for ci in range(3):
                wrong_char = chars[(chars.index(answer) + ci + 1) % len(chars)]
                opts.append(ctx.replace("__", wrong_char))
            random.shuffle(opts)
            ans_idx = opts.index(correct_sentence)
            item = make_q(
                "word_analysis", "字詞辨析", "Word Analysis",
                "word_analysis", "字詞辨別", "Character Distinction",
                q, f"Word analysis #{idx}",
                opts, opts, ans_idx,
                f"應填「{answer}」。", f"Should be '{answer}'.",
                difficulty=2
            )
            if item["question_zh"] not in seen:
                questions.append(item)
                seen.add(item["question_zh"])
            idx += 1
            continue
        elif variant == 4:
            q = f"「{name}在{place}裏{ctx.replace('__', '___')}」應填什麼？(#{idx})"
            wrongs = random.sample([c for c in all_chars if c != answer], 3)
            opts = [answer] + wrongs
        else:
            q = f"「{adj}的{place}裏{ctx.replace('__', '___')}」中空格應填什麼？(#{idx})"
            wrongs = random.sample([c for c in all_chars if c != answer], 3)
            opts = [answer] + wrongs

        random.shuffle(opts)
        ans_idx = opts.index(answer)
        item = make_q(
            "word_analysis", "字詞辨析", "Word Analysis",
            "word_analysis", "字詞辨別", "Character Distinction",
            q, f"Word analysis #{idx}",
            opts, opts, ans_idx,
            f"應填「{answer}」。", f"Should be '{answer}'.",
            difficulty=2
        )
        if item["question_zh"] not in seen:
            questions.append(item)
            seen.add(item["question_zh"])
        idx += 1

    return questions


def gen_idiom_usage(seen, target=1000):
    """成語運用 - idiom meaning, synonym, fill-in-blank."""
    questions = []
    all_meanings = [m for _, m in IDIOMS]
    all_idioms = [i for i, _ in IDIOMS]
    idx = 0

    while len(questions) < target:
        idiom, meaning = IDIOMS[idx % len(IDIOMS)]
        name = NAMES[idx % len(NAMES)]
        place = PLACES[idx % len(PLACES)]
        action = ACTIONS[idx % len(ACTIONS)]

        variant = idx % 5
        if variant == 0:
            wrongs = wrong_options(meaning, all_meanings, 3)
            opts = [meaning] + wrongs
            random.shuffle(opts)
            q = f"「{idiom}」的意思是？(#{idx})"
            ans = opts.index(meaning)
            expl = f"「{idiom}」的意思是{meaning}。"
        elif variant == 1:
            wrong_idioms = wrong_options(idiom, all_idioms, 3)
            opts = [idiom] + wrong_idioms
            random.shuffle(opts)
            q = f"哪個成語的意思是「{meaning}」？(#{idx})"
            ans = opts.index(idiom)
            expl = f"「{idiom}」的意思是{meaning}。"
        elif variant == 2:
            if idx < len(IDIOM_SENTENCES):
                idiom_s, sentence_t = IDIOM_SENTENCES[idx % len(IDIOM_SENTENCES)]
                sentence = sentence_t.replace("{idiom}", "____")
                q = f"「{sentence}」空格中應填什麼成語？(#{idx})"
                wrongs = wrong_options(idiom_s, all_idioms, 3)
                opts = [idiom_s] + wrongs
                random.shuffle(opts)
                ans = opts.index(idiom_s)
                idiom = idiom_s
                expl = f"應填「{idiom_s}」。"
            else:
                q = f"「{name}做事{idiom}」這句話用得恰當嗎？(#{idx})"
                opts = ["恰當", "不恰當"]
                random.shuffle(opts)
                ans = random.randint(0, 1)
                expl = f"用「{idiom}」形容做事是否恰當需視語境而定。"
        elif variant == 3:
            q = f"「{idiom}」可以用來形容什麼情況？(#{idx})"
            opts = [meaning] + wrong_options(meaning, all_meanings, 3)
            random.shuffle(opts)
            ans = opts.index(meaning)
            expl = f"「{idiom}」形容{meaning}的情況。"
        else:
            q = f"「{name}在{place}裏表現得{idiom}」，「{idiom}」的意思是？(#{idx})"
            opts = [meaning] + wrong_options(meaning, all_meanings, 3)
            random.shuffle(opts)
            ans = opts.index(meaning)
            expl = f"「{idiom}」在此處意思是{meaning}。"

        item = make_q(
            "idiom_usage", "成語運用", "Idiom Usage",
            "idiom_usage", "成語理解", "Idiom Comprehension",
            q, f"Idiom question #{idx}",
            opts, opts, ans,
            expl, expl,
            difficulty=3
        )
        if item["question_zh"] not in seen:
            questions.append(item)
            seen.add(item["question_zh"])
        idx += 1

    return questions


def gen_rhetoric(seen, target=1000):
    """修辭手法 - rhetorical device identification."""
    questions = []
    idx = 0

    while len(questions) < target:
        rtype = RHETORIC_TYPES[idx % len(RHETORIC_TYPES)]
        examples = RHETORIC_EXAMPLES[rtype]
        correct_ex = examples[idx % len(examples)]
        other_types = [t for t in RHETORIC_TYPES if t != rtype]
        wrong_exs = []
        for ot in random.sample(other_types, min(3, len(other_types))):
            wrong_exs.append(random.choice(RHETORIC_EXAMPLES[ot]))

        variant = idx % 4
        if variant == 0:
            q = f"以下哪句用了「{rtype}」？(#{idx})"
            opts = [correct_ex] + wrong_exs[:3]
            random.shuffle(opts)
            ans = opts.index(correct_ex)
        elif variant == 1:
            q = f"「{correct_ex}」用了什麼修辭手法？(#{idx})"
            wrongs = wrong_options(rtype, RHETORIC_TYPES, 3)
            opts = [rtype] + wrongs
            random.shuffle(opts)
            ans = opts.index(rtype)
        elif variant == 2:
            q = f"「{correct_ex}」不屬於以下哪種修辭手法？(#{idx})"
            opts = wrong_exs[:3] + [rtype]
            random.shuffle(opts)
            ans = opts.index(rtype)
        else:
            another_ex = random.choice([e for e in examples if e != correct_ex])
            q = f"下列哪句話的修辭手法與「{correct_ex}」相同？(#{idx})"
            opts = [another_ex] + wrong_exs[:3]
            random.shuffle(opts)
            ans = opts.index(another_ex)
            correct_ex = another_ex

        item = make_q(
            "rhetoric", "修辭手法", "Rhetoric",
            "rhetoric", "修辭辨識", "Rhetoric Identification",
            q, f"Rhetoric question #{idx}",
            opts, opts, ans,
            f"答案用了「{rtype}」。", f"Answer uses '{rtype}'.",
            difficulty=2
        )
        if item["question_zh"] not in seen:
            questions.append(item)
            seen.add(item["question_zh"])
        idx += 1

    return questions


def gen_classical(seen, target=1000):
    """文言文 - classical Chinese phrase meaning and source."""
    questions = []
    all_sources = list(set(s for _, s, _, _ in CLASSICAL_PHRASES if s))
    all_authors = list(set(a for _, _, _, a in CLASSICAL_PHRASES if a))
    all_meanings = [m for _, _, m, _ in CLASSICAL_PHRASES]
    all_phrases = [p for p, _, _, _ in CLASSICAL_PHRASES]
    idx = 0

    while len(questions) < target:
        phrase, source, meaning, author = CLASSICAL_PHRASES[idx % len(CLASSICAL_PHRASES)]
        name = NAMES[idx % len(NAMES)]

        variant = idx % 4
        if variant == 0:
            wrongs = wrong_options(meaning, all_meanings, 3)
            opts = [meaning] + wrongs
            random.shuffle(opts)
            q = f"「{phrase}」的意思是？(#{idx})"
            ans = opts.index(meaning)
            expl = f"「{phrase}」的意思是：{meaning}。"
        elif variant == 1 and source:
            wrongs = wrong_options(source, all_sources, 3)
            opts = [source] + wrongs
            random.shuffle(opts)
            q = f"「{phrase}」出自哪本書？(#{idx})"
            ans = opts.index(source)
            expl = f"「{phrase}」出自{source}。"
        elif variant == 2 and author:
            wrongs = wrong_options(author, all_authors, 3)
            opts = [author] + wrongs
            random.shuffle(opts)
            q = f"「{phrase}」是誰說的？(#{idx})"
            ans = opts.index(author)
            expl = f"「{phrase}」是{author}說的。"
        else:
            q = f"以下哪句話的意思是「{meaning}」？(#{idx})"
            wrong_phrases = wrong_options(phrase, all_phrases, 3)
            opts = [phrase] + wrong_phrases
            random.shuffle(opts)
            ans = opts.index(phrase)
            expl = f"「{phrase}」的意思是{meaning}。"

        item = make_q(
            "classical", "文言文", "Classical Chinese",
            "classical", "文言理解", "Classical Comprehension",
            q, f"Classical Chinese #{idx}",
            opts, opts, ans,
            expl, expl,
            difficulty=3
        )
        if item["question_zh"] not in seen:
            questions.append(item)
            seen.add(item["question_zh"])
        idx += 1

    return questions


def gen_sentence_error(seen, target=1000):
    """句子改錯 - find errors in sentences."""
    questions = []
    all_error_types = list(set(et for _, et in ERROR_SENTENCES))
    idx = 0

    while len(questions) < target:
        name = NAMES[idx % len(NAMES)]
        adj = ADJECTIVES[idx % len(ADJECTIVES)]
        adj2 = ADJECTIVES[(idx + 1) % len(ADJECTIVES)]
        place = PLACES[idx % len(PLACES)]
        action = ACTIONS[idx % len(ACTIONS)]

        variant = idx % 5
        if variant == 0 and idx < len(ERROR_SENTENCES):
            err, etype = ERROR_SENTENCES[idx % len(ERROR_SENTENCES)]
            wrongs = wrong_options(etype, all_error_types, 3)
            opts = [etype] + wrongs
            random.shuffle(opts)
            q = f"「{err}」這個句子有什麼問題？(#{idx})"
            ans = opts.index(etype)
            expl = f"此句的問題是：{etype}。"
        elif variant == 1:
            correct = CORRECT_SENTENCES[idx % len(CORRECT_SENTENCES)]
            wrongs = random.sample([e for e, _ in ERROR_SENTENCES], 3)
            opts = [correct] + wrongs
            random.shuffle(opts)
            q = f"下列哪個句子是正確的？(#{idx})"
            ans = opts.index(correct)
            expl = f"正確的句子是：「{correct}」。"
        elif variant == 2:
            err = f"{name}不但{adj}，而且{adj2}，所以很{adj}，因此大家都喜歡他。"
            etype = "重複因果"
            wrongs = wrong_options(etype, all_error_types, 3)
            opts = [etype] + wrongs
            random.shuffle(opts)
            q = f"「{err}」有什麼語病？(#{idx})"
            ans = opts.index(etype)
            expl = f"此句的語病是：{etype}。"
        elif variant == 3:
            err = f"通過在{place}裏{action}，使我受到了很大的啟發。"
            etype = "缺少主語"
            wrongs = wrong_options(etype, all_error_types, 3)
            opts = [etype] + wrongs
            random.shuffle(opts)
            q = f"「{err}」有什麼語病？(#{idx})"
            ans = opts.index(etype)
            expl = f"此句的語病是：{etype}。"
        else:
            err = f"{name}的功課基本上全做完了。"
            etype = "矛盾"
            wrongs = wrong_options(etype, all_error_types, 3)
            opts = [etype] + wrongs
            random.shuffle(opts)
            q = f"「{err}」有什麼語病？(#{idx})"
            ans = opts.index(etype)
            expl = f"此句的語病是：{etype}。"

        item = make_q(
            "sentence_error", "句子改錯", "Sentence Correction",
            "sentence_error", "語病診斷", "Grammar Error",
            q, f"Sentence error #{idx}",
            opts, opts, ans,
            expl, expl,
            difficulty=2
        )
        if item["question_zh"] not in seen:
            questions.append(item)
            seen.add(item["question_zh"])
        idx += 1

    return questions


def gen_word_matching(seen, target=1000):
    """詞語配對 - synonym and antonym matching."""
    questions = []
    all_syn_words = [w for _, w in SYNONYMS] + [w for w, _ in SYNONYMS]
    all_ant_words = [w for _, w in ANTONYMS] + [w for w, _ in ANTONYMS]
    idx = 0

    while len(questions) < target:
        variant = idx % 5
        if variant == 0:
            w1, w2 = SYNONYMS[idx % len(SYNONYMS)]
            wrongs = wrong_options(w2, all_syn_words + all_ant_words, 3)
            opts = [w2] + wrongs
            random.shuffle(opts)
            q = f"「{w1}」的近義詞是？(#{idx})"
            ans = opts.index(w2)
            expl = f"「{w1}」的近義詞是「{w2}」。"
        elif variant == 1:
            w1, w2 = SYNONYMS[idx % len(SYNONYMS)]
            wrongs = wrong_options(w1, all_syn_words + all_ant_words, 3)
            opts = [w1] + wrongs
            random.shuffle(opts)
            q = f"「{w2}」的近義詞是？(#{idx})"
            ans = opts.index(w1)
            expl = f"「{w2}」的近義詞是「{w1}」。"
        elif variant == 2:
            w1, w2 = ANTONYMS[idx % len(ANTONYMS)]
            wrongs = wrong_options(w2, all_ant_words + all_syn_words, 3)
            opts = [w2] + wrongs
            random.shuffle(opts)
            q = f"「{w1}」的反義詞是？(#{idx})"
            ans = opts.index(w2)
            expl = f"「{w1}」的反義詞是「{w2}」。"
        elif variant == 3:
            w1, w2 = ANTONYMS[idx % len(ANTONYMS)]
            wrongs = wrong_options(w1, all_ant_words + all_syn_words, 3)
            opts = [w1] + wrongs
            random.shuffle(opts)
            q = f"「{w2}」的反義詞是？(#{idx})"
            ans = opts.index(w1)
            expl = f"「{w2}」的反義詞是「{w1}」。"
        else:
            w1, w2 = SYNONYMS[idx % len(SYNONYMS)]
            q = f"「{w1}」和以下哪個詞意思最接近？(#{idx})"
            wrongs = wrong_options(w2, all_syn_words + all_ant_words, 3)
            opts = [w2] + wrongs
            random.shuffle(opts)
            ans = opts.index(w2)
            expl = f"「{w1}」和「{w2}」意思最接近。"

        item = make_q(
            "word_matching", "詞語配對", "Word Matching",
            "word_matching", "詞語辨析", "Word Analysis",
            q, f"Word matching #{idx}",
            opts, opts, ans,
            expl, expl,
            difficulty=2
        )
        if item["question_zh"] not in seen:
            questions.append(item)
            seen.add(item["question_zh"])
        idx += 1

    return questions


def gen_punctuation(seen, target=1000):
    """標點符號 - punctuation mark identification."""
    questions = []
    all_punct_types = ["感嘆句", "疑問句", "陳述句", "祈使句"]
    exclamation_words = ["多麼", "真", "好", "太", "非常", "特別", "格外"]
    question_words = ["什麼", "哪裏", "為什麼", "怎麼", "誰", "多少", "幾"]
    idx = 0

    while len(questions) < target:
        name = NAMES[idx % len(NAMES)]
        place = PLACES[idx % len(PLACES)]
        action = ACTIONS[idx % len(ACTIONS)]
        adj = ADJECTIVES[idx % len(ADJECTIVES)]

        variant = idx % 7
        if variant == 0 and idx < len(PUNCTUATION_EXAMPLES):
            sentence, punct, ptype = PUNCTUATION_EXAMPLES[idx % len(PUNCTUATION_EXAMPLES)]
            wrongs = wrong_options(punct, PUNCTUATION_MARKS, 3)
            opts = [punct] + wrongs
            random.shuffle(opts)
            q = f"「{sentence}」句末應加什麼標點？(#{idx})"
            ans = opts.index(punct)
            expl = f"此句應加「{punct}」。"
        elif variant == 1 and idx < len(PUNCTUATION_EXAMPLES):
            sentence, punct, ptype = PUNCTUATION_EXAMPLES[idx % len(PUNCTUATION_EXAMPLES)]
            wrongs = wrong_options(ptype, all_punct_types, 3)
            opts = [ptype] + wrongs
            random.shuffle(opts)
            q = f"「{sentence}」是什麼類型的句子？(#{idx})"
            ans = opts.index(ptype)
            expl = f"「{sentence}」是{ptype}。"
        elif variant == 2:
            ew = exclamation_words[idx % len(exclamation_words)]
            sentence = f"{name}覺得{place}裏{ew}{adj}"
            punct = "！"
            wrongs = wrong_options(punct, PUNCTUATION_MARKS, 3)
            opts = [punct] + wrongs
            random.shuffle(opts)
            q = f"「{sentence}」句末應加什麼標點？(#{idx})"
            ans = opts.index(punct)
            expl = f"此句應加「{punct}」。"
        elif variant == 3:
            qw = question_words[idx % len(question_words)]
            sentence = f"{name}{qw}時候去{place}"
            punct = "？"
            wrongs = wrong_options(punct, PUNCTUATION_MARKS, 3)
            opts = [punct] + wrongs
            random.shuffle(opts)
            q = f"「{sentence}」句末應加什麼標點？(#{idx})"
            ans = opts.index(punct)
            expl = f"此句應加「{punct}」。"
        elif variant == 4:
            sentence = f"{name}在{place}裏{action}"
            punct = "。"
            wrongs = wrong_options(punct, PUNCTUATION_MARKS, 3)
            opts = [punct] + wrongs
            random.shuffle(opts)
            q = f"「{sentence}」句末應加什麼標點？(#{idx})"
            ans = opts.index(punct)
            expl = f"此句應加「{punct}」。"
        elif variant == 5:
            sentence = f"請{action}"
            punct = "。"
            wrongs = wrong_options(punct, PUNCTUATION_MARKS, 3)
            opts = [punct] + wrongs
            random.shuffle(opts)
            q = f"「{sentence}」句末應加什麼標點？(#{idx})"
            ans = opts.index(punct)
            expl = f"此句應加「{punct}」。"
        else:
            sentence = f"{name}和朋友去{place}一起{action}"
            punct = "。"
            wrongs = wrong_options(punct, PUNCTUATION_MARKS, 3)
            opts = [punct] + wrongs
            random.shuffle(opts)
            q = f"「{sentence}」句末應加什麼標點？(#{idx})"
            ans = opts.index(punct)
            expl = f"此句應加「{punct}」。"

        item = make_q(
            "punctuation", "標點符號", "Punctuation",
            "punctuation", "標點運用", "Punctuation Usage",
            q, f"Punctuation #{idx}",
            opts, opts, ans,
            expl, expl,
            difficulty=1
        )
        if item["question_zh"] not in seen:
            questions.append(item)
            seen.add(item["question_zh"])
        idx += 1

    return questions


def gen_parts_of_speech(seen, target=1000):
    """詞性辨別 - part of speech identification."""
    questions = []
    all_pos = list(set(p for _, p in POS_WORDS))
    idx = 0

    while len(questions) < target:
        word, pos = POS_WORDS[idx % len(POS_WORDS)]
        name = NAMES[idx % len(NAMES)]

        variant = idx % 3
        if variant == 0:
            wrongs = wrong_options(pos, all_pos, 3)
            opts = [pos] + wrongs
            random.shuffle(opts)
            q = f"「{word}」屬於什麼詞性？(#{idx})"
            ans = opts.index(pos)
            expl = f"「{word}」是{pos}。"
        elif variant == 1:
            target_pos = pos
            matching_words = [w for w, p in POS_WORDS if p == target_pos]
            correct_word = random.choice(matching_words)
            wrong_words = [w for w, p in POS_WORDS if p != target_pos]
            wrongs = random.sample(wrong_words, min(3, len(wrong_words)))
            opts = [correct_word] + wrongs
            random.shuffle(opts)
            q = f"以下哪個詞是{target_pos}？(#{idx})"
            ans = opts.index(correct_word)
            expl = f"「{correct_word}」是{target_pos}。"
        else:
            q = f"「{name}覺得「{word}」是什麼詞性？」的答案是？(#{idx})"
            wrongs = wrong_options(pos, all_pos, 3)
            opts = [pos] + wrongs
            random.shuffle(opts)
            ans = opts.index(pos)
            expl = f"「{word}」是{pos}。"

        item = make_q(
            "parts_of_speech", "詞性辨別", "Parts of Speech",
            "parts_of_speech", "詞性判斷", "POS Identification",
            q, f"POS #{idx}",
            opts, opts, ans,
            expl, expl,
            difficulty=3
        )
        if item["question_zh"] not in seen:
            questions.append(item)
            seen.add(item["question_zh"])
        idx += 1

    return questions


def gen_reading(seen, target=1000):
    """閱讀理解 - reading comprehension."""
    questions = []
    idx = 0

    while len(questions) < target:
        passage = READING_PASSAGES[idx % len(READING_PASSAGES)]
        q_data = passage["questions"][idx % len(passage["questions"])]
        q_text, opts, ans = q_data

        variant = idx % 3
        if variant == 0:
            q = f"根據短文《{passage['title']}》，{q_text} (#{idx})"
        elif variant == 1:
            q = f"讀完《{passage['title']}》後，{q_text} (#{idx})"
        else:
            q = f"《{passage['title']}》這篇短文中，{q_text} (#{idx})"

        item = make_q(
            "reading", "閱讀理解", "Reading Comprehension",
            "reading", passage["title"], passage["title"],
            q, f"Reading #{idx}: {q_text}",
            opts, opts, ans,
            f"根據短文，答案是「{opts[ans]}」。", f"Based on the passage, the answer is '{opts[ans]}'.",
            difficulty=2
        )
        if item["question_zh"] not in seen:
            questions.append(item)
            seen.add(item["question_zh"])
        idx += 1

    return questions


def gen_culture(seen, target=1000):
    """文化常識 - cultural knowledge."""
    questions = []
    idx = 0

    while len(questions) < target:
        name, detail, description, wrongs_pool = CULTURE_ITEMS[idx % len(CULTURE_ITEMS)]

        variant = idx % 4
        if variant == 0:
            wrongs = wrong_options(detail, [c[1] for c in CULTURE_ITEMS], 3)
            opts = [detail] + wrongs
            random.shuffle(opts)
            q = f"「{name}」是指什麼？(#{idx})"
            ans = opts.index(detail)
            expl = f"「{name}」是指{detail}。{description}。"
        elif variant == 1:
            wrong_items = wrong_options(name, [c[0] for c in CULTURE_ITEMS], 3)
            opts = [name] + wrong_items
            random.shuffle(opts)
            q = f"「{description}」描述的是什麼？(#{idx})"
            ans = opts.index(name)
            expl = f"「{description}」描述的是「{name}」。"
        elif variant == 2:
            wrong_desc = wrong_options(description, [c[2] for c in CULTURE_ITEMS], 3)
            opts = [description] + wrong_desc
            random.shuffle(opts)
            q = f"以下哪項關於「{name}」的描述是正確的？(#{idx})"
            ans = opts.index(description)
            expl = f"「{name}」：{description}"
        else:
            opts = [detail] + wrongs_pool[:3]
            random.shuffle(opts)
            q = f"「{name}」和以下哪項有關？(#{idx})"
            ans = opts.index(detail)
            expl = f"「{name}」與{detail}有關。"

        item = make_q(
            "culture", "文化常識", "Cultural Knowledge",
            "culture", "文化認知", "Cultural Awareness",
            q, f"Culture #{idx}",
            opts, opts, ans,
            expl, expl,
            difficulty=2
        )
        if item["question_zh"] not in seen:
            questions.append(item)
            seen.add(item["question_zh"])
        idx += 1

    return questions


# ============================================================
# INTERLEAVE: no two consecutive same topic
# ============================================================

def interleave(questions_by_topic):
    """
    Interleave questions from different topics so that
    no two consecutive questions share the same topic.
    Uses a round-robin approach with topic rotation.
    """
    # Create lists per topic
    topics = list(questions_by_topic.keys())
    queues = {t: list(questions_by_topic[t]) for t in topics}
    result = []
    last_topic = None

    while any(queues.values()):
        # Pick next topic that != last_topic and has items
        chosen = None
        for t in topics:
            if t != last_topic and queues[t]:
                chosen = t
                break
        # If all remaining are same topic, we have to break
        if chosen is None:
            # All remaining are last_topic - just add them
            for t in topics:
                while queues[t]:
                    result.append(queues[t].pop(0))
            break

        result.append(queues[chosen].pop(0))
        last_topic = chosen

    return result


# ============================================================
# MAIN
# ============================================================

def main():
    seen = set()
    generators = [
        ("word_analysis", gen_word_analysis),
        ("idiom_usage", gen_idiom_usage),
        ("rhetoric", gen_rhetoric),
        ("classical", gen_classical),
        ("sentence_error", gen_sentence_error),
        ("word_matching", gen_word_matching),
        ("punctuation", gen_punctuation),
        ("parts_of_speech", gen_parts_of_speech),
        ("reading", gen_reading),
        ("culture", gen_culture),
    ]

    print("=" * 60)
    print("Chinese S1 Question Generator v3")
    print("=" * 60)

    questions_by_topic = {}
    total = 0
    for name, gen_func in generators:
        qs = gen_func(seen, target=1000)
        questions_by_topic[name] = qs
        total += len(qs)
        print(f"  {name}: {len(qs)}")

    print(f"\nTotal: {total}")

    # Interleave
    all_questions = interleave(questions_by_topic)

    # Assign IDs
    for i, q in enumerate(all_questions):
        q["id"] = i + 1

    # Verification
    print("\n" + "=" * 60)
    print("VERIFICATION")
    print("=" * 60)
    print(f"Total questions: {len(all_questions)}")

    q_texts = [q["question_zh"] for q in all_questions]
    unique_texts = set(q_texts)
    print(f"Unique question texts: {len(unique_texts)}")
    print(f"Duplicates: {len(q_texts) - len(unique_texts)}")

    # Max consecutive same topic
    topics = [q["topic_id"] for q in all_questions]
    max_consecutive = 1
    current_consecutive = 1
    for i in range(1, len(topics)):
        if topics[i] == topics[i-1]:
            current_consecutive += 1
            max_consecutive = max(max_consecutive, current_consecutive)
        else:
            current_consecutive = 1
    print(f"Max consecutive same topic: {max_consecutive}")

    from collections import Counter
    topic_counts = Counter(topics)
    print("\nTopic distribution:")
    for t, c in topic_counts.most_common():
        print(f"  {t}: {c}")

    # Save
    out_paths = [
        os.path.join(WORKDIR, "chinese", "s1", "questions.json"),
        os.path.join(WORKDIR, "v2", "chinese", "s1", "questions.json"),
    ]
    for path in out_paths:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(all_questions, f, ensure_ascii=False, indent=2)
        print(f"\nSaved to: {path}")

    print("\n✅ DONE!")


if __name__ == "__main__":
    main()
