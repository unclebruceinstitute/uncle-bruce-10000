#!/usr/bin/env python3
"""
Generate music quiz structure for 大B舅父萬題庫
Creates full directory structure, HTML pages, and starter quiz JSON files.
"""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
MUSIC = os.path.join(BASE, 'others', 'music')

# ============================================================
# ARTIST DATA
# ============================================================
REGIONS = {
    "all": {"zh": "全部", "en": "All", "emoji": "🎵"},
    "hong_kong": {"zh": "香港", "en": "Hong Kong", "emoji": "🇭🇰"},
    "mandarin": {"zh": "華語", "en": "Mandarin", "emoji": "🇨🇳"},
    "western": {"zh": "歐美", "en": "Western", "emoji": "🌍"},
    "korean": {"zh": "韓語", "en": "Korean", "emoji": "🇰🇷"},
    "japanese": {"zh": "日語", "en": "Japanese", "emoji": "🇯🇵"},
    "other": {"zh": "其他", "en": "Other", "emoji": "🌐"},
}

CATEGORIES = {
    "male": {"zh": "男歌星", "en": "Male Singers", "emoji": "🎤"},
    "female": {"zh": "女歌星", "en": "Female Singers", "emoji": "👩‍🎤"},
    "groups": {"zh": "組合", "en": "Groups", "emoji": "👥"},
}

ARTISTS = {
    "hong_kong": {
        "male": [
            ("eason_chan", "陳奕迅", "Eason Chan", "🎤"),
            ("mc_cheung", "MC張天賦", "MC Cheung", "🎤"),
            ("keung_to", "姜濤", "Keung To", "🎤"),
            ("andy_lau", "劉德華", "Andy Lau", "🎤"),
            ("jacky_cheung", "張學友", "Jacky Cheung", "🎤"),
            ("leon_lai", "黎明", "Leon Lai", "🎤"),
            ("aaron_kwok", "郭富城", "Aaron Kwok", "🎤"),
            ("leo_ku", "古巨基", "Leo Ku", "🎤"),
            ("hins_cheung", "張敬軒", "Hins Cheung", "🎤"),
            ("pakyau_chau", "周柏豪", "Pakho Chau", "🎤"),
            ("wu_ngor_kwan", "吳業坤", "Ng Siu Nam", "🎤"),
            ("philip_chan", "陳柏宇", "Jason Chan", "🎤"),
            ("terrence_lam", "林家謙", "Terrence Lam", "🎤"),
            ("hung_to_lap", "洪卓立", "Jason Hung", "🎤"),
            ("wu_hung_yin", "胡鴻鈞", "Wu Hung Yin", "🎤"),
            ("eric_kot", "鄭中基", "Ronald Cheng", "🎤"),
            ("sethn_tee", "側田", "Seth Tse", "🎤"),
            ("khalil_fong", "方大同", "Khalil Fong", "🎤"),
            ("alfranco", "林奕匡", "Phil Lam", "🎤"),
            ("timothy_hui", "許廷鏗", "Alfred Hui", "🎤"),
        ],
        "female": [
            ("miriam_yeung", "楊千嬅", "Miriam Yeung", "👩‍🎤"),
            ("kay_tse", "謝安琪", "Kay Tse", "👩‍🎤"),
            ("janice_vidal", "衛蘭", "Janice Vidal", "👩‍🎤"),
            ("g.e.m.", "鄧紫棋", "G.E.M.", "👩‍🎤"),
            ("aga", "AGA", "AGA", "👩‍🎤"),
            ("jessica_wong", "林二汶", "Eman Lam", "👩‍🎤"),
            ("ivana_wong", "王菀之", "Ivana Wong", "👩‍🎤"),
            ("linsiya", "連詩雅", "Shiga Lin", "👩‍🎤"),
            ("joyce_cheng", "鄭欣宜", "Joyce Cheng", "👩‍🎤"),
            ("kary_ng", "吳雨霏", "Kary Ng", "👩‍🎤"),
            ("fiona_sit", "薛凱琪", "Fiona Sit", "👩‍🎤"),
            ("kelly_chen", "陳慧琳", "Kelly Chen", "👩‍🎤"),
            ("joey_yung", "容祖兒", "Joey Yung", "👩‍🎤"),
            ("sammi_cheng", "鄭秀文", "Sammi Cheng", "👩‍🎤"),
            ("karen_mok", "莫文蔚", "Karen Mok", "👩‍🎤"),
            ("vinci_wong", "泳兒", "Vincy Chan", "👩‍🎤"),
            ("jw", "JW王灝兒", "JW", "👩‍🎤"),
            ("mag_lam", "林欣彤", "Mag Lam", "👩‍🎤"),
            ("cherry_yeung", "黃妍", "Cherry Yeung", "👩‍🎤"),
            ("serrini", "Serrini", "Serrini", "👩‍🎤"),
        ],
        "groups": [
            ("mirror", "MIRROR", "MIRROR", "👥"),
            ("error", "ERROR", "ERROR", "👥"),
            ("suppermoment", "Supper Moment", "Supper Moment", "👥"),
            ("rubberband", "RubberBand", "RubberBand", "👥"),
            ("at17", "at17", "at17", "👥"),
            ("twins", "Twins", "Twins", "👥"),
            ("grasshopper", "草蜢", "Grasshopper", "👥"),
            ("beyond", "BEYOND", "BEYOND", "👥"),
            ("soler", "Soler", "Soler", "👥"),
            ("kolor", "Kolor", "Kolor", "👥"),
            ("dear_jane", "Dear Jane", "Dear Jane", "👥"),
            ("c_allstar", "C AllStar", "C AllStar", "👥"),
            ("fm_station", "FMStation", "FMStation", "👥"),
            ("robynn_and_kendy", "Robynn & Kendy", "Robynn & Kendy", "👥"),
            ("shine", "Shine", "Shine", "👥"),
            ("cookies", "Cookies", "Cookies", "👥"),
            ("swing", "Swing", "Swing", "👥"),
            ("mr.", "Mr.", "Mr.", "👥"),
            ("zen", "Zen", "Zen", "👥"),
            ("to_nick", "ToNick", "ToNick", "👥"),
        ],
    },
    "mandarin": {
        "male": [
            ("jay_chou", "周杰倫", "Jay Chou", "🎤"),
            ("jj_lin", "林俊傑", "JJ Lin", "🎤"),
            ("leehom_wang", "王力宏", "Wang Leehom", "🎤"),
            ("ashin", "五月天阿信", "Ashin", "🎤"),
            ("chen_yixun", "陳奕迅", "Eason Chan", "🎤"),
            ("huachen_yu", "華晨宇", "Hua Chenyu", "🎤"),
            ("maobuyi", "毛不易", "Mao Buyi", "🎤"),
            ("li_ronghao", "李榮浩", "Li Ronghao", "🎤"),
            ("xue_zhiqian", "薛之謙", "Joker Xue", "🎤"),
            ("zhang_jie", "張杰", "Jason Zhang", "🎤"),
            ("david_tao", "陶喆", "David Tao", "🎤"),
            ("wu_qingfeng", "吳青峰", "Wu Qingfeng", "🎤"),
            ("jam_hsiao", "蕭敬騰", "Jam Hsiao", "🎤"),
            ("lin_yo_jia", "林宥嘉", "Lin Youjia", "🎤"),
            ("william_wei", "韋禮安", "William Wei", "🎤"),
            ("wilber_pan", "潘瑋柏", "Wilber Pan", "🎤"),
            ("zhou_shen", "周深", "Zhou Shen", "🎤"),
            ("hu_xia", "胡夏", "Hu Xia", "🎤"),
            ("jeff_chang", "張信哲", "Jeff Chang", "🎤"),
            ("wakin_chau", "周華健", "Wakin Chau", "🎤"),
        ],
        "female": [
            ("g.e.m._mandarin", "鄧紫棋", "G.E.M.", "👩‍🎤"),
            ("jolin_tsai", "蔡依林", "Jolin Tsai", "👩‍🎤"),
            ("a-mei", "張惠妹", "A-Mei", "👩‍🎤"),
            ("sun_yanzi", "孫燕姿", "Stefanie Sun", "👩‍🎤"),
            ("jasper_fish", "梁靜茹", "Fish Leong", "👩‍🎤"),
            ("hebe_tien", "田馥甄", "Hebe Tien", "👩‍🎤"),
            ("a-lin", "A-Lin", "A-Lin", "👩‍🎤"),
            ("lala_hsu", "徐佳瑩", "LaLa Hsu", "👩‍🎤"),
            ("rainie_yang", "楊丞琳", "Rainie Yang", "👩‍🎤"),
            ("della_ding", "丁噹", "Della Ding", "👩‍🎤"),
            ("joanne_tseng", "曾沛慈", "Joanne Tseng", "👩‍🎤"),
            ("teresa_teng", "鄧麗君", "Teresa Teng", "👩‍🎤"),
            ("faye_chan", "王菲", "Faye Wong", "👩‍🎤"),
            ("na_ying", "那英", "Na Ying", "👩‍🎤"),
            ("zhou_bichang", "周筆暢", "Zhou Bichang", "👩‍🎤"),
            ("li_yuchun", "李宇春", "Li Yuchun", "👩‍🎤"),
            ("zhang_liangying", "張靚穎", "Jane Zhang", "👩‍🎤"),
            ("tia_ray", "袁婭維", "Tia Ray", "👩‍🎤"),
            ("chen_lihua", "陳立農", "Chen Linong", "👩‍🎤"),
            ("wan_fang", "萬芳", "Wan Fang", "👩‍🎤"),
        ],
        "groups": [
            ("mayday", "五月天", "Mayday", "👥"),
            ("sodagreen", "蘇打綠", "Sodagreen", "👥"),
            ("she", "S.H.E", "S.H.E", "👥"),
            ("f4", "F4", "F4", "👥"),
            ("fei_lun_hai", "飛輪海", "Fahrenheit", "👥"),
            ("tfboys", "TFBoys", "TFBoys", "👥"),
            ("nine_percent", "Nine Percent", "Nine Percent", "👥"),
            ("r1se", "R1SE", "R1SE", "👥"),
            ("the_black_swan", "黑澀會美眉", "Hey Girl", "👥"),
            ("lollipop_f", "棒棒堂", "Lollipop F", "👥"),
            ("nanquan_mother", "南拳媽媽", "NanQuan Mama", "👥"),
            ("power_station", "動力火車", "Power Station", "👥"),
            ("miyavi", "信樂團", "Shin Band", "👥"),
            ("y2j", "Y2J", "Y2J", "👥"),
            ("grasshopper_m", "草蜢", "Grasshopper", "👥"),
            ("tension", "Tension", "Tension", "👥"),
            ("energy", "Energy", "Energy", "👥"),
            ("5566", "5566", "5566", "👥"),
            ("fahrenheit_m", "飛輪海", "Fahrenheit", "👥"),
            ("by2", "BY2", "BY2", "👥"),
        ],
    },
    "western": {
        "male": [
            ("ed_sheeran", "Ed Sheeran", "Ed Sheeran", "🎤"),
            ("bruno_mars", "Bruno Mars", "Bruno Mars", "🎤"),
            ("justin_bieber", "Justin Bieber", "Justin Bieber", "🎤"),
            ("the_weeknd", "The Weeknd", "The Weeknd", "🎤"),
            ("harry_styles", "Harry Styles", "Harry Styles", "🎤"),
            ("post_malone", "Post Malone", "Post Malone", "🎤"),
            ("drake", "Drake", "Drake", "🎤"),
            ("shawn_mendes", "Shawn Mendes", "Shawn Mendes", "🎤"),
            ("charlie_puth", "Charlie Puth", "Charlie Puth", "🎤"),
            ("sam_smith", "Sam Smith", "Sam Smith", "🎤"),
            ("john_legend", "John Legend", "John Legend", "🎤"),
            ("pharrell", "Pharrell Williams", "Pharrell Williams", "🎤"),
            ("adam_levine", "Adam Levine", "Adam Levine", "🎤"),
            ("elton_john", "Elton John", "Elton John", "🎤"),
            ("freddie_mercury", "Freddie Mercury", "Freddie Mercury", "🎤"),
            ("michael_jackson", "Michael Jackson", "Michael Jackson", "🎤"),
            ("elvis_presley", "Elvis Presley", "Elvis Presley", "🎤"),
            ("john_lennon", "John Lennon", "John Lennon", "🎤"),
            ("paul_mccartney", "Paul McCartney", "Paul McCartney", "🎤"),
            ("stevie_wonder", "Stevie Wonder", "Stevie Wonder", "🎤"),
        ],
        "female": [
            ("taylor_swift", "Taylor Swift", "Taylor Swift", "👩‍🎤"),
            ("adele", "Adele", "Adele", "👩‍🎤"),
            ("billie_eilish", "Billie Eilish", "Billie Eilish", "👩‍🎤"),
            ("ariana_grande", "Ariana Grande", "Ariana Grande", "👩‍🎤"),
            ("dua_lipa", "Dua Lipa", "Dua Lipa", "👩‍🎤"),
            ("lady_gaga", "Lady Gaga", "Lady Gaga", "👩‍🎤"),
            ("katy_perry", "Katy Perry", "Katy Perry", "👩‍🎤"),
            ("rihanna", "Rihanna", "Rihanna", "👩‍🎤"),
            ("beyonce", "Beyoncé", "Beyoncé", "👩‍🎤"),
            ("olivia_rodrigo", "Olivia Rodrigo", "Olivia Rodrigo", "👩‍🎤"),
            ("sza", "SZA", "SZA", "👩‍🎤"),
            ("doja_cat", "Doja Cat", "Doja Cat", "👩‍🎤"),
            ("halsey", "Halsey", "Halsey", "👩‍🎤"),
            ("lorde", "Lorde", "Lorde", "👩‍🎤"),
            ("sabrina_carpenter", "Sabrina Carpenter", "Sabrina Carpenter", "👩‍🎤"),
            ("madonna", "Madonna", "Madonna", "👩‍🎤"),
            ("whitney_houston", "Whitney Houston", "Whitney Houston", "👩‍🎤"),
            ("mariah_carey", "Mariah Carey", "Mariah Carey", "👩‍🎤"),
            ("celine_dion", "Celine Dion", "Celine Dion", "👩‍🎤"),
            ("britney_spears", "Britney Spears", "Britney Spears", "👩‍🎤"),
        ],
        "groups": [
            ("bts", "BTS", "BTS", "👥"),
            ("coldplay", "Coldplay", "Coldplay", "👥"),
            ("imagine_dragons", "Imagine Dragons", "Imagine Dragons", "👥"),
            ("maroon5", "Maroon 5", "Maroon 5", "👥"),
            ("one_direction", "One Direction", "One Direction", "👥"),
            ("the_beatles", "The Beatles", "The Beatles", "👥"),
            ("queen", "Queen", "Queen", "👥"),
            ("nirvana", "Nirvana", "Nirvana", "👥"),
            ("u2", "U2", "U2", "👥"),
            ("abba", "ABBA", "ABBA", "👥"),
            ("backstreet_boys", "Backstreet Boys", "Backstreet Boys", "👥"),
            ("nsync", "NSYNC", "NSYNC", "👥"),
            ("spice_girls", "Spice Girls", "Spice Girls", "👥"),
            ("destinys_child", "Destiny's Child", "Destiny's Child", "👥"),
            ("linkin_park", "Linkin Park", "Linkin Park", "👥"),
            ("green_day", "Green Day", "Green Day", "👥"),
            ("foo_fighters", "Foo Fighters", "Foo Fighters", "👥"),
            ("radiohead", "Radiohead", "Radiohead", "👥"),
            ("rolling_stones", "The Rolling Stones", "The Rolling Stones", "👥"),
            ("eagles", "Eagles", "Eagles", "👥"),
        ],
    },
    "korean": {
        "male": [
            ("g-dragon", "G-Dragon", "G-Dragon", "🎤"),
            ("taeyang", "太陽", "Taeyang", "🎤"),
            ("v", "V (金泰亨)", "V", "🎤"),
            ("jungkook", "田柾國", "Jungkook", "🎤"),
            ("jimin", "朴智旻", "Jimin", "🎤"),
            ("rm_kr", "RM (金南俊)", "RM", "🎤"),
            ("exo_baekhyun", "伯賢", "Baekhyun", "🎤"),
            ("exo_chanyeol", "燦烈", "Chanyeol", "🎤"),
            ("kang_daniel", "姜丹尼爾", "Kang Daniel", "🎤"),
            ("zico", "Zico", "Zico", "🎤"),
            ("jay_park", "朴宰範", "Jay Park", "🎤"),
            ("crush", "Crush", "Crush", "🎤"),
            ("dean", "DEAN", "DEAN", "🎤"),
            ("iu_male", "朴炯植", "Park Hyung Sik", "🎤"),
            ("exo_d_o", "D.O.", "D.O.", "🎤"),
            ("winner_mino", "宋旻浩", "Mino", "🎤"),
            ("ikon_bobby", "Bobby", "Bobby", "🎤"),
            ("hoshi", "Hoshi", "Hoshi", "🎤"),
            ("dokyeom", "Dokyeom", "Dokyeom", "🎤"),
            ("jackson_wang", "王嘉爾", "Jackson Wang", "🎤"),
        ],
        "female": [
            ("iu", "IU", "IU", "👩‍🎤"),
            ("taeyeon", "太妍", "Taeyeon", "👩‍🎤"),
            ("jennie", "Jennie", "Jennie", "👩‍🎤"),
            ("lisa", "Lisa", "Lisa", "👩‍🎤"),
            ("rose", "Rosé", "Rosé", "👩‍🎤"),
            ("jisoo", "Jisoo", "Jisoo", "👩‍🎤"),
            ("solar", "頌樂", "Solar", "👩‍🎤"),
            ("hwasa", "華莎", "Hwasa", "👩‍🎤"),
            ("chung_ha", "請夏", "Chungha", "👩‍🎤"),
            ("somi", "Somi", "Somi", "👩‍🎤"),
            ("yooa", "YooA", "YooA", "👩‍🎤"),
            ("joy", "Joy", "Joy", "👩‍🎤"),
            ("wendy", "Wendy", "Wendy", "👩‍🎤"),
            ("seulgi", "瑟琪", "Seulgi", "👩‍🎤"),
            ("nayeon", "娜璉", "Nayeon", "👩‍🎤"),
            ("tzuyu", "子瑜", "Tzuyu", "👩‍🎤"),
            ("sana", "Sana", "Sana", "👩‍🎤"),
            ("jihyo", "志效", "Jihyo", "👩‍🎤"),
            ("yena", "崔叡娜", "Yena", "👩‍🎤"),
            ("eunbi", "權恩妃", "Eunbi", "👩‍🎤"),
        ],
        "groups": [
            ("bts_group", "BTS", "BTS", "👥"),
            ("blackpink", "BLACKPINK", "BLACKPINK", "👥"),
            ("exo", "EXO", "EXO", "👥"),
            ("twice_kr", "TWICE", "TWICE", "👥"),
            ("red_velvet", "Red Velvet", "Red Velvet", "👥"),
            ("nct", "NCT", "NCT", "👥"),
            ("stray_kids", "Stray Kids", "Stray Kids", "👥"),
            ("ateez", "ATEEZ", "ATEEZ", "👥"),
            ("seventeen", "SEVENTEEN", "SEVENTEEN", "👥"),
            ("got7", "GOT7", "GOT7", "👥"),
            ("shinee", "SHINee", "SHINee", "👥"),
            ("bigbang", "BIGBANG", "BIGBANG", "👥"),
            ("girls_generation", "少女時代", "Girls' Generation", "👥"),
            ("2ne1", "2NE1", "2NE1", "👥"),
            ("mamamoo", "MAMAMOO", "MAMAMOO", "👥"),
            ("itzy", "ITZY", "ITZY", "👥"),
            ("aespa", "aespa", "aespa", "👥"),
            ("ive", "IVE", "IVE", "👥"),
            ("new_jeans", "NewJeans", "NewJeans", "👥"),
            ("le_sserafim", "LE SSERAFIM", "LE SSERAFIM", "👥"),
        ],
    },
    "japanese": {
        "male": [
            ("kenshi_yonezu", "米津玄師", "Kenshi Yonezu", "🎤"),
            ("radwimps", "野田洋次郎", "Yojiro Noda", "🎤"),
            ("hikaru_utada_m", "宇多田光", "Utada Hikaru", "🎤"),
            ("gen_hoshino", "星野源", "Gen Hoshino", "🎤"),
            ("aimyon_m", "あいみょん", "Aimyon", "🎤"),
            ("one_ok_rock_taka", "Taka", "Taka", "🎤"),
            ("official髭", "Official髭男dism", "Official Hige Dandism", "🎤"),
            ("yosui_inoue", "井上陽水", "Yosui Inoue", "🎤"),
            ("tsuyoshi_domoto", "堂本剛", "Tsuyoshi Domoto", "🎤"),
            ("arashi_ohno", "大野智", "Satoshi Ohno", "🎤"),
            ("masaharu_fukuyama", "福山雅治", "Masaharu Fukuyama", "🎤"),
            ("koichi_domoto", "堂本光一", "Koichi Domoto", "🎤"),
            ("takuya_kimura", "木村拓哉", "Takuya Kimura", "🎤"),
            ("tomohisa_yamashita", "山下智久", "Tomohisa Yamashita", "🎤"),
            ("ryosuke_yamada", "山田涼介", "Ryosuke Yamada", "🎤"),
            ("yuto_nakajima", "中島裕翔", "Yuto Nakajima", "🎤"),
            ("kazuya_kamenashi", "亀梨和也", "Kazuya Kamenashi", "🎤"),
            ("jin_akanishi", "赤西仁", "Jin Akanishi", "🎤"),
            ("daigo", "DAIGO", "DAIGO", "🎤"),
            ("tatsuro_yamashita", "山下達郎", "Tatsuro Yamashita", "🎤"),
        ],
        "female": [
            ("hikaru_utada", "宇多田光", "Utada Hikaru", "👩‍🎤"),
            ("aimyon", "あいみょん", "Aimyon", "👩‍🎤"),
            ("yui_jp", "YUI", "YUI", "👩‍🎤"),
            ("lisa_jp", "LiSA", "LiSA", "👩‍🎤"),
            ("yonezu_kenshi_f", "米津玄師", "Kenshi Yonezu", "👩‍🎤"),
            ("aimer", "Aimer", "Aimer", "👩‍🎤"),
            ("yoasobi_ikura", "ikura", "ikura", "👩‍🎤"),
            ("milet", "milet", "milet", "👩‍🎤"),
            ("ado", "Ado", "Ado", "👩‍🎤"),
            ("ringo_sheena", "椎名林檎", "Ringo Sheena", "👩‍🎤"),
            ("ayumi_hamasaki", "濱崎步", "Ayumi Hamasaki", "👩‍🎤"),
            ("utada_hikaru", "宇多田光", "Utada Hikaru", "👩‍🎤"),
            ("misia", "MISIA", "MISIA", "👩‍🎤"),
            ("kumi_koda", "幸田來未", "Kumi Koda", "👩‍🎤"),
            ("namie_amuro", "安室奈美惠", "Namie Amuro", "👩‍🎤"),
            ("kyary", "Kyary Pamyu Pamyu", "Kyary Pamyu Pamyu", "👩‍🎤"),
            ("perfume_nocchi", "Nocchi", "Nocchi", "👩‍🎤"),
            ("babymetal_su", "SU-METAL", "SU-METAL", "👩‍🎤"),
            ("reina_tanaka", "田中麗奈", "Reina Tanaka", "👩‍🎤"),
            ("eriko_iwasawa", "岩澤絵里子", "Eriko Iwasawa", "👩‍🎤"),
        ],
        "groups": [
            ("arashi", "嵐", "Arashi", "👥"),
            ("yoasobi", "YOASOBI", "YOASOBI", "👥"),
            ("one_ok_rock", "ONE OK ROCK", "ONE OK ROCK", "👥"),
            ("radwimps_g", "RADWIMPS", "RADWIMPS", "👥"),
            ("babymetal", "BABYMETAL", "BABYMETAL", "👥"),
            ("perfume", "Perfume", "Perfume", "👥"),
            ("king_gnu", "King Gnu", "King Gnu", "👥"),
            ("official_hige", "Official髭男dism", "Official Hige Dandism", "👥"),
            ("aiko", "aiko", "aiko", "👥"),
            ("southern_all", "Southern All Stars", "Southern All Stars", "👥"),
            ("mr_children", "Mr.Children", "Mr.Children", "👥"),
            ("dreams_true", "DREAMS COME TRUE", "DREAMS COME TRUE", "👥"),
            ("larcenciel", "L'Arc-en-Ciel", "L'Arc-en-Ciel", "👥"),
            ("glay", "GLAY", "GLAY", "👥"),
            ("x_japan", "X Japan", "X Japan", "👥"),
            ("janne_da_arc", "Janne Da Arc", "Janne Da Arc", "👥"),
            ("bump_of_chicken", "BUMP OF CHICKEN", "BUMP OF CHICKEN", "👥"),
            ("asian_kung_fu", "ASIAN KUNG-FU GENERATION", "ASIAN KUNG-FU GENERATION", "👥"),
            ("flumpool", "flumpool", "flumpool", "👥"),
            ("scandal_jp", "SCANDAL", "SCANDAL", "👥"),
        ],
    },
    "other": {
        "male": [
            ("jay_chou_other", "周杰倫", "Jay Chou", "🎤"),
            ("richard_marx", "Richard Marx", "Richard Marx", "🎤"),
            ("andrea_bocelli", "Andrea Bocelli", "Andrea Bocelli", "🎤"),
            ("luis_fonsi", "Luis Fonsi", "Luis Fonsi", "🎤"),
            ("psy", "PSY", "PSY", "🎤"),
            ("arash", "Arash", "Arash", "🎤"),
            ("enrique_iglesias", "Enrique Iglesias", "Enrique Iglesias", "🎤"),
            ("ricky_martin", "Ricky Martin", "Ricky Martin", "🎤"),
            ("josh_groban", "Josh Groban", "Josh Groban", "🎤"),
            ("michael_buble", "Michael Bublé", "Michael Bublé", "🎤"),
            ("robbie_williams", "Robbie Williams", "Robbie Williams", "🎤"),
            ("george_michael", "George Michael", "George Michael", "🎤"),
            ("frank_sinatra", "Frank Sinatra", "Frank Sinatra", "🎤"),
            ("tony_bennett", "Tony Bennett", "Tony Bennett", "🎤"),
            ("luciano_pavarotti", "Luciano Pavarotti", "Luciano Pavarotti", "🎤"),
            ("placido_domingo", "Plácido Domingo", "Plácido Domingo", "🎤"),
            ("jose_carreras", "José Carreras", "José Carreras", "🎤"),
            ("russell_watson", "Russell Watson", "Russell Watson", "🎤"),
            ("il_divo", "Il Divo", "Il Divo", "🎤"),
            ("celine_dion_m", "Celine Dion", "Celine Dion", "🎤"),
        ],
        "female": [
            ("shakira", "Shakira", "Shakira", "👩‍🎤"),
            ("celine_dion_f", "Celine Dion", "Celine Dion", "👩‍🎤"),
            ("andrea_bocelli_f", "Laura Pausini", "Laura Pausini", "👩‍🎤"),
            ("nana_mouskouri", "Nana Mouskouri", "Nana Mouskouri", "👩‍🎤"),
            ("edith_piaf", "Edith Piaf", "Edith Piaf", "👩‍🎤"),
            ("lara_fabian", "Lara Fabian", "Lara Fabian", "👩‍🎤"),
            ("anggun", "Anggun", "Anggun", "👩‍🎤"),
            ("regine_velasquez", "Regine Velasquez", "Regine Velasquez", "👩‍🎤"),
            ("charice", "Charice", "Charice", "👩‍🎤"),
            ("leona_lewis", "Leona Lewis", "Leona Lewis", "👩‍🎤"),
            ("sarah_brightman", "Sarah Brightman", "Sarah Brightman", "👩‍🎤"),
            ("enya", "Enya", "Enya", "👩‍🎤"),
            ("sade", "Sade", "Sade", "👩‍🎤"),
            ("norah_jones", "Norah Jones", "Norah Jones", "👩‍🎤"),
            ("amy_winehouse", "Amy Winehouse", "Amy Winehouse", "👩‍🎤"),
            ("dido", "Dido", "Dido", "👩‍🎤"),
            ("corinne_bailey", "Corinne Bailey Rae", "Corinne Bailey Rae", "👩‍🎤"),
            ("joss_stone", "Joss Stone", "Joss Stone", "👩‍🎤"),
            ("alicia_keys", "Alicia Keys", "Alicia Keys", "👩‍🎤"),
            ("anastacia", "Anastacia", "Anastacia", "👩‍🎤"),
        ],
        "groups": [
            ("bts_other", "BTS", "BTS", "👥"),
            ("little_mix", "Little Mix", "Little Mix", "👥"),
            ("westlife", "Westlife", "Westlife", "👥"),
            ("boyzone", "Boyzone", "Boyzone", "👥"),
            ("take_that", "Take That", "Take That", "👥"),
            ("celtic_woman", "Celtic Woman", "Celtic Woman", "👥"),
            ("il_divo_g", "Il Divo", "Il Divo", "👥"),
            ("abba_other", "ABBA", "ABBA", "👥"),
            ("ace_of_base", "Ace of Base", "Ace of Base", "👥"),
            ("aqua", "Aqua", "Aqua", "👥"),
            ("rob_rock", "Scorpions", "Scorpions", "👥"),
            ("bon_jovi", "Bon Jovi", "Bon Jovi", "👥"),
            ("aerosmith", "Aerosmith", "Aerosmith", "👥"),
            ("def_leppard", "Def Leppard", "Def Leppard", "👥"),
            ("van_halen", "Van Halen", "Van Halen", "👥"),
            ("journey", "Journey", "Journey", "👥"),
            ("toto", "Toto", "Toto", "👥"),
            ("police", "The Police", "The Police", "👥"),
            ("dire_straits", "Dire Straits", "Dire Straits", "👥"),
            ("pink_floyd", "Pink Floyd", "Pink Floyd", "👥"),
        ],
    },
}

# ============================================================
# HTML TEMPLATES
# ============================================================
def make_page(title_zh, title_en, emoji, items, base_path, back_path="../../", back_text="返回主頁"):
    """Generate a category/selection page."""
    cards = ""
    for item in items:
        cards += f'''<div class="card" onclick="location.href='{item["href"]}'">
<div class="emoji">{item["emoji"]}</div>
<div class="name">{item["zh"]}</div>
<div class="sub">{item["en"]}</div>
<div class="count">{item.get("count","")}</div>
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
.hdr{{text-align:center;padding:24px 0;color:#fff;border-radius:16px;margin-bottom:20px;background:linear-gradient(135deg,#8e44ad,#9b59b6)}}
.hdr h1{{font-size:26px;margin-bottom:4px}}
.hdr p{{font-size:14px;opacity:.9}}
.top-bar{{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px}}
.home-link{{padding:8px 16px;border:1px solid #ddd;border-radius:8px;background:#fff;cursor:pointer;font-size:14px;text-decoration:none;color:#333;display:inline-block}}
.home-link:hover{{background:#f5f5f5}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px}}
.card{{padding:18px 12px;background:#fff;border-radius:14px;cursor:pointer;transition:.25s;box-shadow:0 2px 8px rgba(0,0,0,.06);text-align:center;border:2px solid transparent}}
.card:hover{{transform:translateY(-3px);box-shadow:0 6px 20px rgba(0,0,0,.12);border-color:#8e44ad}}
.card .emoji{{font-size:32px;margin-bottom:6px}}
.card .name{{font-size:15px;font-weight:700;margin-bottom:2px}}
.card .sub{{font-size:12px;color:#888}}
.card .count{{font-size:11px;color:#aaa;margin-top:4px}}
.ft{{margin-top:30px;color:#888;font-size:.75rem;text-align:center}}
</style>
</head>
<body>
<div class="c">
<div class="top-bar">
<a class="home-link" href="{back_path}" data-zh="← {back_text}" data-en="← Back">← {back_text}</a>
</div>
<div class="hdr">
<h1>{emoji} {title_zh}</h1>
<p>{title_en}</p>
</div>
<div class="grid">{cards}</div>
<div class="ft">© 2026 Uncle Bruce Institute 大B舅父教室</div>
</div>
</body>
</html>'''

def make_quiz_page(artist_zh, artist_en, emoji, region_zh, cat_zh, back_path):
    """Generate an artist quiz page."""
    return f'''<!DOCTYPE html>
<html lang="zh-HK">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{emoji} {artist_zh} | 音樂題庫 — 大B舅父萬題庫</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'PingFang HK','Microsoft JhengHei',sans-serif;background:#f0f2f5;color:#333}}
.c{{max-width:800px;margin:0 auto;padding:16px}}
.top-bar{{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px}}
.home-link{{padding:8px 16px;border:1px solid #ddd;border-radius:8px;background:#fff;cursor:pointer;font-size:14px;text-decoration:none;color:#333;display:inline-block}}
.hdr{{text-align:center;padding:24px 0;color:#fff;border-radius:16px;margin-bottom:20px;background:linear-gradient(135deg,#8e44ad,#9b59b6)}}
.hdr h1{{font-size:24px;margin-bottom:4px}}
.hdr p{{font-size:14px;opacity:.9}}
.stats{{display:flex;justify-content:space-around;background:#fff;border-radius:12px;padding:12px;margin-bottom:16px;box-shadow:0 2px 8px rgba(0,0,0,.08)}}
.stat{{text-align:center}}.stat-n{{font-size:24px;font-weight:700;color:#8e44ad}}.stat-l{{font-size:12px;color:#888}}
.btn{{padding:14px 36px;border:none;border-radius:12px;font-size:18px;font-weight:700;cursor:pointer;background:linear-gradient(135deg,#8e44ad,#9b59b6);color:#fff;transition:.2s}}
.btn:hover{{opacity:.9}}
.qa{{background:#fff;border-radius:16px;padding:24px;box-shadow:0 2px 12px rgba(0,0,0,.08);display:none}}
.qt{{font-size:18px;line-height:1.8;margin-bottom:20px;font-weight:500}}
.opts{{display:flex;flex-direction:column;gap:10px}}
.opt{{padding:14px 16px;border:2px solid #e8e8e8;border-radius:10px;cursor:pointer;font-size:16px;transition:.2s}}
.opt:hover{{background:#f3e5f5}}.opt.ok{{border-color:#4caf50;background:#e8f5e9}}.opt.ng{{border-color:#f44336;background:#fce4ec}}.opt.d{{pointer-events:none;opacity:.7}}
.ep{{margin-top:16px;padding:16px;background:#f3e5f5;border-radius:10px;border-left:4px solid #8e44ad;display:none}}
.ep.show{{display:block}}.ep p{{font-size:14px;line-height:1.6}}
.prog{{width:100%;height:6px;background:#e0e0e0;border-radius:3px;margin-bottom:16px;overflow:hidden}}
.pb{{height:100%;background:#8e44ad;border-radius:3px;transition:.3s}}
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
<h1>{emoji} {artist_zh}</h1>
<p>{artist_en} — {region_zh} {cat_zh}</p>
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
<div class="qa">
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
function startQuiz(){{
loadQ().then(()=>{{
if(!questions.length)return;
questions=[...questions].sort(()=>Math.random()-.5).slice(0,20);
curQ=0;correct=0;answered=0;
document.getElementById('startView').classList.add('hidden');
document.getElementById('quizView').classList.remove('hidden');
document.getElementById('resultView').classList.add('hidden');
showQ();
}});
}}
function showQ(){{
if(curQ>=questions.length){{showResult();return}}
const q=questions[curQ];
document.getElementById('qNum').textContent=`$ {{curQ+1}} / $ {{questions.length}}`;
document.getElementById('qText').textContent=q.question_zh||'';
document.getElementById('progBar').style.width=`${{(curQ/questions.length)*100}}%`;
document.getElementById('expl').classList.remove('show');
document.getElementById('nextBtn').style.display='none';
const opts=q.options_zh||[];
const div=document.getElementById('optsDiv');
div.innerHTML='';
const labels=['A','B','C','D'];
opts.forEach((o,i)=>{{
const el=document.createElement('div');
el.className='opt';
el.textContent=labels[i]+'. '+o;
el.onclick=()=>checkA(i,q);
div.appendChild(el);
}});
}}
function checkA(idx,q){{
answered++;
document.querySelectorAll('.opt').forEach(o=>o.classList.add('d'));
const ci=q.answer;
if(idx===ci){{document.querySelectorAll('.opt')[ci].classList.add('ok');correct++;}}
else{{document.querySelectorAll('.opt')[idx].classList.add('ng');document.querySelectorAll('.opt')[ci].classList.add('ok');}}
document.getElementById('explText').textContent=q.explanation_zh||'';
document.getElementById('expl').classList.add('show');
document.getElementById('nextBtn').style.display='block';
updateStats();
}}
function nextQ(){{curQ++;showQ()}}
function showResult(){{
document.getElementById('quizView').classList.add('hidden');
document.getElementById('resultView').classList.remove('hidden');
const pct=Math.round(correct/answered*100);
document.getElementById('resTitle').textContent=`答對 $ {{correct}} / $ {{answered}} 題（$ {{pct}}%）`;
document.getElementById('resEmoji').textContent=pct>=80?'🏆':pct>=60?'👍':'😅';
document.getElementById('resText').textContent=pct>=80?'好犀利！':pct>=60?'唔錯，繼續努力！':'再接再厲！';
}}
function updateStats(){{
document.getElementById('doneQ').textContent=answered;
document.getElementById('correctQ').textContent=correct;
document.getElementById('accuracy').textContent=answered?Math.round(correct/answered*100)+'%':'0%';
}}
loadQ();
</script>
</body>
</html>'''

def make_quiz_json(artist_zh, artist_en):
    """Generate starter quiz questions for an artist."""
    questions = []
    templates = [
        {
            "q_zh": f"{artist_zh}出道嘅年份係？",
            "q_en": f"When did {artist_en} debut?",
            "opts": ["1990年代", "2000年代", "2010年代", "2020年代"],
            "ans": 1,
            "exp_zh": f"{artist_zh}喺2000年代出道。",
            "exp_en": f"{artist_en} debuted in the 2000s."
        },
        {
            "q_zh": f"{artist_zh}係邊個地方嘅歌手？",
            "q_en": f"Where is {artist_en} from?",
            "opts": ["香港", "台灣", "內地", "海外"],
            "ans": 0,
            "exp_zh": f"{artist_zh}係香港歌手。",
            "exp_en": f"{artist_en} is from Hong Kong."
        },
        {
            "q_zh": f"以下邊首係{artist_zh}嘅代表作？",
            "q_en": f"Which is a representative song of {artist_en}?",
            "opts": ["歌曲A", "歌曲B", "歌曲C", "歌曲D"],
            "ans": 0,
            "exp_zh": f"「歌曲A」係{artist_zh}嘅代表作之一。",
            "exp_en": "'Song A' is one of {artist_en}'s representative songs."
        },
    ]
    for i, t in enumerate(templates):
        questions.append({
            "id": i+1,
            "question_zh": t["q_zh"],
            "question_en": t["q_en"],
            "options_zh": t["opts"],
            "options_en": t["opts"],
            "answer": t["ans"],
            "explanation_zh": t["exp_zh"],
            "explanation_en": t["exp_en"],
            "difficulty": 1
        })
    return questions

# ============================================================
# MAIN GENERATION
# ============================================================
def main():
    print("Generating music quiz structure...")
    
    # 1. Main music index
    region_items = []
    for rid, rinfo in REGIONS.items():
        region_items.append({
            "href": f"{rid}/index.html",
            "zh": f"{rinfo['emoji']} {rinfo['zh']}",
            "en": rinfo["en"],
            "emoji": rinfo["emoji"],
        })
    
    with open(os.path.join(MUSIC, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(make_page("音樂題庫", "Music Quiz", "🎵", region_items, MUSIC))
    print("  Created music/index.html")
    
    # 2. For each region
    for rid, rinfo in REGIONS.items():
        region_dir = os.path.join(MUSIC, rid)
        os.makedirs(region_dir, exist_ok=True)
        
        # Region index → show categories (male/female/groups)
        cat_items = []
        for cid, cinfo in CATEGORIES.items():
            artists = ARTISTS.get(rid, {}).get(cid, [])
            cat_items.append({
                "href": f"{cid}/index.html",
                "zh": f"{cinfo['emoji']} {cinfo['zh']}",
                "en": cinfo["en"],
                "emoji": cinfo["emoji"],
                "count": f"{len(artists)} 位" if artists else "",
            })
        
        with open(os.path.join(region_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(make_page(
                f"{rinfo['emoji']} {rinfo['zh']}音樂",
                f"{rinfo['en']} Music",
                rinfo["emoji"],
                cat_items,
                region_dir,
                back_path="../../",
                back_text="返回音樂主頁"
            ))
        print(f"  Created {rid}/index.html")
        
        # 3. For each category in this region
        for cid, cinfo in CATEGORIES.items():
            cat_dir = os.path.join(region_dir, cid)
            os.makedirs(cat_dir, exist_ok=True)
            
            artists = ARTISTS.get(rid, {}).get(cid, [])
            
            # Category index → show artists
            artist_items = []
            for aslug, azh, aen, aemoji in artists:
                artist_items.append({
                    "href": f"{aslug}/index.html",
                    "zh": f"{aemoji} {azh}",
                    "en": aen,
                    "emoji": aemoji,
                })
            
            with open(os.path.join(cat_dir, 'index.html'), 'w', encoding='utf-8') as f:
                f.write(make_page(
                    f"{cinfo['emoji']} {rinfo['zh']}{cinfo['zh']}",
                    f"{rinfo['en']} {cinfo['en']}",
                    cinfo["emoji"],
                    artist_items,
                    cat_dir,
                    back_path="../",
                    back_text=f"返回{rinfo['zh']}"
                ))
            print(f"  Created {rid}/{cid}/index.html ({len(artists)} artists)")
            
            # 4. For each artist
            for aslug, azh, aen, aemoji in artists:
                artist_dir = os.path.join(cat_dir, aslug)
                os.makedirs(artist_dir, exist_ok=True)
                
                # Quiz page
                with open(os.path.join(artist_dir, 'index.html'), 'w', encoding='utf-8') as f:
                    f.write(make_quiz_page(azh, aen, aemoji, rinfo["zh"], cinfo["zh"], "../"))
                
                # Questions JSON
                qs = make_quiz_json(azh, aen)
                with open(os.path.join(artist_dir, 'questions.json'), 'w', encoding='utf-8') as f:
                    json.dump(qs, f, ensure_ascii=False, indent=2)
    
    # 5. Update the "Others" index page
    others_index = os.path.join(BASE, 'others', 'index.html')
    if os.path.exists(others_index):
        with open(others_index) as f:
            content = f.read()
        # Add music, computer, travel, gaming, anime cards if not present
        new_cards = [
            ("🎵", "音樂", "Music Quiz", "music/index.html", "香港、華語、歐美、韓語、日語音樂題庫"),
            ("💻", "電腦", "Computer Quiz", "computer/index.html", "電腦與科技知識題庫"),
            ("✈️", "旅遊", "Travel Quiz", "travel/index.html", "世界旅遊知識題庫"),
            ("🎮", "電玩", "Gaming Quiz", "gaming/index.html", "電玩遊戲知識題庫"),
            ("🎌", "動漫", "Anime Quiz", "anime/index.html", "動漫知識題庫"),
        ]
        for emoji, zh, en, href, desc in new_cards:
            if href not in content:
                print(f"  Note: Add {zh} card to others/index.html")
    
    # Count totals
    total_artists = sum(len(artists) for region in ARTISTS.values() for artists in region.values())
    total_dirs = total_artists  # each artist gets a directory
    print(f"\n✅ Done! {total_artists} artists, {total_dirs} quiz directories created")
    print(f"   Regions: {len(REGIONS)}")
    print(f"   Categories per region: {len(CATEGORIES)}")
    print(f"   Artists per category: ~20")

if __name__ == '__main__':
    main()
