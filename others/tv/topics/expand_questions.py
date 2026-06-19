#!/usr/bin/env python3
"""
Expand TV quiz database from 2,662 to ~5,000 questions.
Each file: 22 → ~41 questions (41 × 121 files ≈ 4,961).

Adds diverse, high-quality questions covering:
- Cast & characters
- Plot & storylines
- Year/episodes/seasons
- Classic scenes & quotes
- Director/writer
- Genre comparisons
- Adaptation/remake info
"""

import json
import os
import random

random.seed(42)

# ============================================================
# KNOWLEDGE BASE
# ============================================================

SHOWS = {
    # ── CN DRAMA ──
    "cang_lan_jue": {
        "zh": "蒼蘭訣", "en": "Love Between Fairy and Devil",
        "genre_zh": "仙俠", "genre_en": "Xianxia Fantasy",
        "year": 2022, "episodes": 36,
        "cast_zh": ["虞書欣", "王鶴棣"], "cast_en": ["Esther Yu", "Wang Hedi"],
        "characters_zh": ["小蘭花", "東方青蒼"], "characters_en": ["Xiao Lanhua", "Dongfang Qingcang"],
        "platform": "愛奇藝",
        "desc_zh": "仙俠劇，講述仙女小蘭花同月尊東方青蒼嘅愛情故事",
        "desc_en": "A xianxia romance between a fairy and the Moon Supreme",
    },
    "chang_yue_jin_ming": {
        "zh": "長月燼明", "en": "Till the End of the Moon",
        "genre_zh": "仙俠", "genre_en": "Xianxia Fantasy",
        "year": 2023, "episodes": 40,
        "cast_zh": ["白鹿", "羅雲熙"], "cast_en": ["Bai Lu", "Luo Yunxi"],
        "characters_zh": ["黎蘇蘇", "澹臺燼"], "characters_en": ["Li Sushi", "Tantai Jin"],
        "platform": "優酷",
        "desc_zh": "仙俠劇，講述神女為拯救蒼生回到五百年前阻止魔神覺醒",
        "desc_en": "A xianxia drama about a goddess sent back 500 years to prevent the Devil God's awakening",
    },
    "chen_qing_ling": {
        "zh": "陳情令", "en": "The Untamed",
        "genre_zh": "仙俠", "genre_en": "Xianxia Fantasy",
        "year": 2019, "episodes": 50,
        "cast_zh": ["肖戰", "王一博"], "cast_en": ["Xiao Zhan", "Wang Yibo"],
        "characters_zh": ["魏無羨", "藍忘機"], "characters_en": ["Wei Wuxian", "Lan Wangji"],
        "platform": "騰訊視頻",
        "desc_zh": "改編自墨香銅臭小說《魔道祖師》",
        "desc_en": "Adapted from Mo Xiang Tong Xiu's novel 'Mo Dao Zu Shi'",
        "adaptation_zh": "改編自網絡小說《魔道祖師》", "adaptation_en": "Adapted from the web novel 'Mo Dao Zu Shi'",
    },
    "du_luo": {
        "zh": "獨步", "en": "Walking Alone",
        "genre_zh": "古裝", "genre_en": "Historical",
        "year": 2023, "episodes": 40,
        "cast_zh": ["成毅", "曾舜晞"], "cast_en": ["Cheng Yi", "Joseph Zeng"],
        "characters_zh": ["王小石", "白愁飛"], "characters_en": ["Wang Xiaoshi", "Bai Choufei"],
        "platform": "愛奇藝",
        "desc_zh": "古裝武俠劇，改編自溫瑞安同名小說",
        "desc_en": "A wuxia drama adapted from Wen Ruian's novel",
        "adaptation_zh": "改編自溫瑞安小說", "adaptation_en": "Adapted from Wen Ruian's novel",
    },
    "gu_jian_qi_tan": {
        "zh": "古劍奇譚", "en": "Swords of Legends",
        "genre_zh": "仙俠", "genre_en": "Xianxia Fantasy",
        "year": 2014, "episodes": 52,
        "cast_zh": ["李易峰", "楊冪"], "cast_en": ["Li Yifeng", "Yang Mi"],
        "characters_zh": ["百里屠蘇", "風晴雪"], "characters_en": ["Baili Tusu", "Feng Qingxue"],
        "platform": "湖南衛視",
        "desc_zh": "改編自同名遊戲",
        "desc_en": "Adapted from the video game of the same name",
        "adaptation_zh": "改編自同名電腦遊戲", "adaptation_en": "Adapted from the video game",
    },
    "hua_qian_gu": {
        "zh": "花千骨", "en": "The Journey of Flower",
        "genre_zh": "仙俠", "genre_en": "Xianxia Fantasy",
        "year": 2015, "episodes": 58,
        "cast_zh": ["霍建華", "趙麗穎"], "cast_en": ["Wallace Huo", "Zhao Liying"],
        "characters_zh": ["白子畫", "花千骨"], "characters_en": ["Bai Zihua", "Hua Qiangu"],
        "platform": "湖南衛視",
        "desc_zh": "仙俠劇，講述花千骨同長留上仙白子畫嘅師徒戀",
        "desc_en": "A xianxia romance between a disciple and her immortal master",
    },
    "lang_ya_bang": {
        "zh": "瑯琊榜", "en": "Nirvana in Fire",
        "genre_zh": "古裝權謀", "genre_en": "Historical Political",
        "year": 2015, "episodes": 54,
        "cast_zh": ["胡歌", "劉濤", "王凱"], "cast_en": ["Hu Ge", "Liu Tao", "Wang Kai"],
        "characters_zh": ["梅長蘇", "霓凰郡主", "靖王"], "characters_en": ["Mei Changsu", "Princess Nihuang", "Prince Jing"],
        "platform": "北京衛視/東方衛視",
        "desc_zh": "古裝權謀劇，梅長蘇為翻案以病弱之軀攪動朝堂風雲",
        "desc_en": "A political drama about Mei Changsu's quest for justice",
        "director_zh": "孔笙", "director_en": "Kong Sheng",
    },
    "liu_xing_hua_yuan": {
        "zh": "流星花園", "en": "Meteor Garden",
        "genre_zh": "偶像劇", "genre_en": "Idol Drama",
        "year": 2018, "episodes": 49,
        "cast_zh": ["王鶴棣", "沈月"], "cast_en": ["Dylan Wang", "Shen Yue"],
        "characters_zh": ["道明寺", "杉菜"], "characters_en": ["Dao Ming Si", "Shan Cai"],
        "platform": "湖南衛視",
        "desc_zh": "改編自日本漫畫《花樣男子》",
        "desc_en": "Adapted from Japanese manga 'Boys Over Flowers'",
        "adaptation_zh": "改編自神尾葉子漫畫《花樣男子》", "adaptation_en": "Adapted from Yoko Kamio's manga 'Hana Yori Dango'",
    },
    "other": {
        "zh": "其他內地劇", "en": "Other CN Dramas",
        "genre_zh": "綜合", "genre_en": "Mixed",
        "year": 2020, "episodes": 40,
        "cast_zh": [], "cast_en": [],
        "characters_zh": [], "characters_en": [],
        "platform": "",
        "desc_zh": "其他內地劇集嘅綜合題目",
        "desc_en": "Mixed questions about other Chinese dramas",
    },
    "qing_yu_nian": {
        "zh": "慶餘年", "en": "Joy of Life",
        "genre_zh": "古裝權謀", "genre_en": "Historical Political",
        "year": 2019, "episodes": 46,
        "cast_zh": ["張若昀", "李沁", "陳道明"], "cast_en": ["Zhang Ruoyun", "Li Qin", "Chen Daoming"],
        "characters_zh": ["范閒", "林婉兒", "慶帝"], "characters_en": ["Fan Xian", "Lin Waner", "Emperor Qing"],
        "platform": "騰訊視頻/愛奇藝",
        "desc_zh": "古裝劇，講述穿越者范閒喺古代嘅冒險故事",
        "desc_en": "About a modern man reborn in ancient times navigating political intrigue",
        "adaptation_zh": "改編自貓膩同名小說", "adaptation_en": "Adapted from Mao Ni's novel",
    },
    "qing_yun_zhi": {
        "zh": "青雲志", "en": "Noble Aspirations",
        "genre_zh": "仙俠", "genre_en": "Xianxia Fantasy",
        "year": 2016, "episodes": 55,
        "cast_zh": ["李易峰", "趙麗穎"], "cast_en": ["Li Yifeng", "Zhao Liying"],
        "characters_zh": ["張小凡", "碧瑤"], "characters_en": ["Zhang Xiaofan", "Bi Yao"],
        "platform": "湖南衛視",
        "desc_zh": "改編自蕭鼎小說《誅仙》",
        "desc_en": "Adapted from Xiao Ding's novel 'Zhu Xian'",
        "adaptation_zh": "改編自小說《誅仙》", "adaptation_en": "Adapted from the novel 'Zhu Xian'",
    },
    "ru_yi_chuan": {
        "zh": "如懿傳", "en": "Ruyi's Royal Love in the Palace",
        "genre_zh": "宮鬥", "genre_en": "Palace Drama",
        "year": 2018, "episodes": 87,
        "cast_zh": ["周迅", "霍建華"], "cast_en": ["Zhou Xun", "Wallace Huo"],
        "characters_zh": ["如懿", "乾隆帝"], "characters_en": ["Ruyi", "Emperor Qianlong"],
        "platform": "騰訊視頻",
        "desc_zh": "宮鬥劇，講述如懿同乾隆帝從相愛到心死嘅故事",
        "desc_en": "A palace drama about Empress Nara's tragic love with Emperor Qianlong",
    },
    "san_sheng_san_shi": {
        "zh": "三生三世十里桃花", "en": "Eternal Love",
        "genre_zh": "仙俠", "genre_en": "Xianxia Fantasy",
        "year": 2017, "episodes": 58,
        "cast_zh": ["趙又廷", "楊冪"], "cast_en": ["Mark Chao", "Yang Mi"],
        "characters_zh": ["夜華", "白淺"], "characters_en": ["Ye Hua", "Bai Qian"],
        "platform": "浙江衛視/東方衛視",
        "desc_zh": "仙俠劇，講述三生三世嘅愛情",
        "desc_en": "A xianxia romance spanning three lifetimes",
        "adaptation_zh": "改編自唐七同名小說", "adaptation_en": "Adapted from Tang Qi's novel",
    },
    "shan_he_ling": {
        "zh": "山河令", "en": "Word of Honor",
        "genre_zh": "武俠", "genre_en": "Wuxia",
        "year": 2021, "episodes": 36,
        "cast_zh": ["龔俊", "張哲瀚"], "cast_en": ["Gong Jun", "Zhang Zhehan"],
        "characters_zh": ["溫客行", "周子舒"], "characters_en": ["Wen Kexing", "Zhou Zishu"],
        "platform": "優酷",
        "desc_zh": "武俠劇，改編自Priest小說《天涯客》",
        "desc_en": "A wuxia drama adapted from Priest's novel 'Tian Ya Ke'",
        "adaptation_zh": "改編自Priest小說《天涯客》", "adaptation_en": "Adapted from Priest's novel 'Tian Ya Ke'",
    },
    "wan_mei": {
        "zh": "完美伴侶", "en": "Perfect Couple",
        "genre_zh": "都市情感", "genre_en": "Urban Romance",
        "year": 2022, "episodes": 40,
        "cast_zh": ["高圓圓", "張魯一"], "cast_en": ["Gao Yuanyanyuan", "Zhang Luyi"],
        "characters_zh": ["陳珊", "孫磊"], "characters_en": ["Chen Shan", "Sun Lei"],
        "platform": "湖南衛視",
        "desc_zh": "都市情感劇，探討現代婚姻同職場平衡",
        "desc_en": "An urban drama about balancing marriage and career",
    },
    "xi_yuan_mi_yu": {
        "zh": "西遊記", "en": "Journey to the West",
        "genre_zh": "古裝神話", "genre_en": "Mythological",
        "year": 1986, "episodes": 25,
        "cast_zh": ["六小齡童", "馬德華"], "cast_en": ["Liu Xiao Ling Tong", "Ma Dehua"],
        "characters_zh": ["孫悟空", "豬八戒", "唐僧"], "characters_en": ["Sun Wukong", "Zhu Bajie", "Tang Seng"],
        "platform": "央視",
        "desc_zh": "改編自吳承恩同名小說，講述唐僧師徒四人西天取經",
        "desc_en": "Adapted from Wu Cheng'en's classic novel about the pilgrimage to the West",
        "adaptation_zh": "改編自吳承恩古典小說", "adaptation_en": "Adapted from Wu Cheng'en's classic novel",
        "director_zh": "楊潔", "director_en": "Yang Jie",
    },
    "xing_han_can_lan": {
        "zh": "星漢燦爛", "en": "Love Like the Galaxy",
        "genre_zh": "古裝愛情", "genre_en": "Historical Romance",
        "year": 2022, "episodes": 56,
        "cast_zh": ["吳磊", "趙露思"], "cast_en": ["Wu Lei", "Zhao Lusi"],
        "characters_zh": ["凌不疑", "程少商"], "characters_en": ["Ling Buyi", "Cheng Shaoshang"],
        "platform": "騰訊視頻",
        "desc_zh": "古裝劇，講述將門孤女程少商同新帝義子凌不疑嘅愛情故事",
        "desc_en": "A historical romance between a general's daughter and the emperor's godson",
        "adaptation_zh": "改編自關心則亂同名小說", "adaptation_en": "Adapted from Guan Xin Ze Luan's novel",
    },
    "zhen_huan_zhuan": {
        "zh": "甄嬛傳", "en": "Empresses in the Palace",
        "genre_zh": "宮鬥", "genre_en": "Palace Drama",
        "year": 2011, "episodes": 76,
        "cast_zh": ["孫儷", "陳建斌", "蔡少芬"], "cast_en": ["Sun Li", "Chen Jianbin", "Ada Choi"],
        "characters_zh": ["甄嬛", "雍正帝", "皇后"], "characters_en": ["Zhen Huan", "Emperor Yongzheng", "Empress"],
        "platform": "浙江衛視",
        "desc_zh": "宮鬥劇經典，講述甄嬛入宮後嘅成長同權謀鬥爭",
        "desc_en": "A classic palace drama about Zhen Huan's rise in the imperial harem",
        "director_zh": "鄭曉龍", "director_en": "Zheng Xiaolong",
    },
    # ── HK DRAMA ──
    "bi_xue_jian": {
        "zh": "碧血劍", "en": "Sword Stained with Royal Blood",
        "genre_zh": "武俠", "genre_en": "Wuxia",
        "year": 1985, "episodes": 20,
        "cast_zh": ["黃日華", "莊靜而"], "cast_en": ["Felix Wong", "Ching Yee Chong"],
        "characters_zh": ["袁承志", "溫青青"], "characters_en": ["Yuan Chengzhi", "Wen Qingqing"],
        "platform": "TVB",
        "desc_zh": "改編自金庸同名小說",
        "desc_en": "Adapted from Jin Yong's novel",
        "adaptation_zh": "改編自金庸小說", "adaptation_en": "Adapted from Jin Yong's novel",
    },
    "da_tang_shuang_long": {
        "zh": "大唐雙龍傳", "en": "Twin of Brothers",
        "genre_zh": "武俠", "genre_en": "Wuxia",
        "year": 2004, "episodes": 42,
        "cast_zh": ["林峯", "吳卓羲"], "cast_en": ["Raymond Lam", "Ron Ng"],
        "characters_zh": ["徐子陵", "寇仲"], "characters_en": ["Xu Ziling", "Kou Zhong"],
        "platform": "TVB",
        "desc_zh": "改編自黃易同名小說",
        "desc_en": "Adapted from Huang Yi's novel",
        "adaptation_zh": "改編自黃易小說", "adaptation_en": "Adapted from Huang Yi's novel",
    },
    "fei_hu_wai_chuan": {
        "zh": "飛虎外傳", "en": "Flying Tiger",
        "genre_zh": "警匪", "genre_en": "Police Drama",
        "year": 2018, "episodes": 30,
        "cast_zh": ["馬德鍾", "苗僑偉"], "cast_en": ["Joe Ma", "Miu Kiu Wai"],
        "characters_zh": ["展瀚韜", "沈志敖"], "characters_en": ["Chin Ho Tao", "Sum Chi Ngo"],
        "platform": "TVB/邵氏兄弟",
        "desc_zh": "警匪劇，講述飛虎隊精英嘅故事",
        "desc_en": "A police drama about the Special Duties Unit (SDU)",
    },
    "feng_shen_bang": {
        "zh": "封神榜", "en": "Gods of Honour",
        "genre_zh": "古裝神話", "genre_en": "Mythological",
        "year": 2001, "episodes": 40,
        "cast_zh": ["陳浩民", "溫碧霞"], "cast_en": ["Benny Chan", "Irene Wan"],
        "characters_zh": ["哪吒", "妲己"], "characters_en": ["Nezha", "Daji"],
        "platform": "TVB",
        "desc_zh": "改編自古典小說《封神演義》",
        "desc_en": "Adapted from the classic novel 'Investiture of the Gods'",
        "adaptation_zh": "改編自《封神演義》", "adaptation_en": "Adapted from 'Fengshen Yanyi'",
    },
    "lian_cheng_jue": {
        "zh": "連城訣", "en": "A Deadly Secret",
        "genre_zh": "武俠", "genre_en": "Wuxia",
        "year": 1989, "episodes": 20,
        "cast_zh": ["郭晉安", "黎美嫻"], "cast_en": ["Roger Kwok", "Lai Mei Han"],
        "characters_zh": ["狄雲", "戚芳"], "characters_en": ["Di Yun", "Qi Fang"],
        "platform": "TVB",
        "desc_zh": "改編自金庸同名小說",
        "desc_en": "Adapted from Jin Yong's novel",
        "adaptation_zh": "改編自金庸小說", "adaptation_en": "Adapted from Jin Yong's novel",
    },
    "lu_ding_ji": {
        "zh": "鹿鼎記", "en": "The Duke of Mount Deer",
        "genre_zh": "武俠喜劇", "genre_en": "Wuxia Comedy",
        "year": 1998, "episodes": 45,
        "cast_zh": ["陳小春", "馬浚偉"], "cast_en": ["Jordan Chan", "Steven Ma"],
        "characters_zh": ["韋小寶", "康熙帝"], "characters_en": ["Wai Siu Bo", "Emperor Kangxi"],
        "platform": "TVB",
        "desc_zh": "改編自金庸小說，講述韋小寶嘅傳奇經歷",
        "desc_en": "Adapted from Jin Yong's novel about the lovable rogue Wai Siu Bo",
        "adaptation_zh": "改編自金庸小說", "adaptation_en": "Adapted from Jin Yong's novel",
    },
    "other": {
        "zh": "其他武俠劇", "en": "Other HK Wuxia Dramas",
        "genre_zh": "武俠", "genre_en": "Wuxia",
        "year": 2000, "episodes": 30,
        "cast_zh": [], "cast_en": [],
        "characters_zh": [], "characters_en": [],
        "platform": "TVB",
        "desc_zh": "其他TVB武俠劇集嘅綜合題目",
        "desc_en": "Mixed questions about other TVB wuxia dramas",
    },
    "she_diao_ying_xiong_chuan": {
        "zh": "射鵰英雄傳", "en": "The Legend of the Condor Heroes",
        "genre_zh": "武俠", "genre_en": "Wuxia",
        "year": 1983, "episodes": 59,
        "cast_zh": ["黃日華", "翁美玲"], "cast_en": ["Felix Wong", "Barbara Yung"],
        "characters_zh": ["郭靖", "黃蓉"], "characters_en": ["Guo Jing", "Huang Rong"],
        "platform": "TVB",
        "desc_zh": "金庸經典武俠劇，講述郭靖黃蓉嘅故事",
        "desc_en": "Jin Yong's classic wuxia about Guo Jing and Huang Rong",
        "adaptation_zh": "改編自金庸小說", "adaptation_en": "Adapted from Jin Yong's novel",
    },
    "shen_diao_xia_lv": {
        "zh": "神鵰俠侶", "en": "The Return of the Condor Heroes",
        "genre_zh": "武俠", "genre_en": "Wuxia",
        "year": 1995, "episodes": 32,
        "cast_zh": ["古天樂", "李若彤"], "cast_en": ["Louis Koo", "Carman Lee"],
        "characters_zh": ["楊過", "小龍女"], "characters_en": ["Yang Guo", "Xiaolongnü"],
        "platform": "TVB",
        "desc_zh": "金庸經典，講述楊過同小龍女嘅師徒戀",
        "desc_en": "Jin Yong's classic about Yang Guo and Xiaolongnü's love story",
        "adaptation_zh": "改編自金庸小說", "adaptation_en": "Adapted from Jin Yong's novel",
    },
    "shu_jian_en_chou_lu": {
        "zh": "書劍恩仇錄", "en": "The Book and the Sword",
        "genre_zh": "武俠", "genre_en": "Wuxia",
        "year": 1976, "episodes": 60,
        "cast_zh": ["鄭少秋"], "cast_en": ["Adam Cheng"],
        "characters_zh": ["陳家洛"], "characters_en": ["Chen Jialuo"],
        "platform": "TVB",
        "desc_zh": "TVB首部金庸劇，鄭少秋主演",
        "desc_en": "TVB's first Jin Yong adaptation, starring Adam Cheng",
        "adaptation_zh": "改編自金庸小說", "adaptation_en": "Adapted from Jin Yong's novel",
    },
    "tian_long_ba_bu": {
        "zh": "天龍八部", "en": "Demi-Gods and Semi-Devils",
        "genre_zh": "武俠", "genre_en": "Wuxia",
        "year": 1997, "episodes": 45,
        "cast_zh": ["黃日華", "陳浩民", "樊少皇"], "cast_en": ["Felix Wong", "Benny Chan", "Fan Siu Wong"],
        "characters_zh": ["喬峰", "段譽", "虛竹"], "characters_en": ["Qiao Feng", "Duan Yu", "Xu Zhu"],
        "platform": "TVB",
        "desc_zh": "金庸武俠劇，講述三個主角嘅江湖故事",
        "desc_en": "Jin Yong's wuxia epic following three protagonists",
        "adaptation_zh": "改編自金庸小說", "adaptation_en": "Adapted from Jin Yong's novel",
    },
    "tian_shan_tong_lao": {
        "zh": "天山童姥", "en": "Child Elder of Tian Mountain",
        "genre_zh": "武俠", "genre_en": "Wuxia",
        "year": 1990, "episodes": 20,
        "cast_zh": ["林青霞"], "cast_en": ["Brigitte Lin"],
        "characters_zh": ["天山童姥"], "characters_en": ["Child Elder of Tian Mountain"],
        "platform": "TVB",
        "desc_zh": "武俠劇",
        "desc_en": "A wuxia drama",
    },
    "wu_mu_zhi_jian": {
        "zh": "武穆遺書", "en": "Legend of Wumu",
        "genre_zh": "武俠", "genre_en": "Wuxia",
        "year": 1990, "episodes": 20,
        "cast_zh": [], "cast_en": [],
        "characters_zh": [], "characters_en": [],
        "platform": "TVB",
        "desc_zh": "武俠劇",
        "desc_en": "A wuxia drama",
    },
    "xi_you_ji": {
        "zh": "西遊記", "en": "Journey to the West",
        "genre_zh": "古裝神話", "genre_en": "Mythological",
        "year": 1996, "episodes": 30,
        "cast_zh": ["張衛健", "江華"], "cast_en": ["Dicky Cheung", "Kwong Wa"],
        "characters_zh": ["孫悟空", "唐三藏"], "characters_en": ["Sun Wukong", "Tang Sanzang"],
        "platform": "TVB",
        "desc_zh": "TVB版西遊記，張衛健飾演孫悟空",
        "desc_en": "TVB's Journey to the West with Dicky Cheung as Sun Wukong",
        "adaptation_zh": "改編自吳承恩小說", "adaptation_en": "Adapted from Wu Cheng'en's novel",
    },
    "xia_ke_xing": {
        "zh": "俠客行", "en": "Ode to Gallantry",
        "genre_zh": "武俠", "genre_en": "Wuxia",
        "year": 1989, "episodes": 20,
        "cast_zh": ["梁朝偉"], "cast_en": ["Tony Leung Chiu-wai"],
        "characters_zh": ["石破天", "石中玉"], "characters_en": ["Shi Potian", "Shi Zhongyu"],
        "platform": "TVB",
        "desc_zh": "改編自金庸小說，梁朝偉一人分飾兩角",
        "desc_en": "Adapted from Jin Yong's novel, Tony Leung plays dual roles",
        "adaptation_zh": "改編自金庸小說", "adaptation_en": "Adapted from Jin Yong's novel",
    },
    "xiao_ao_jiang_hu": {
        "zh": "笑傲江湖", "en": "The Smiling, Proud Wanderer",
        "genre_zh": "武俠", "genre_en": "Wuxia",
        "year": 1996, "episodes": 40,
        "cast_zh": ["呂頌賢", "梁佩玲"], "cast_en": ["Lui Shun Yin", "Leung Pui Ling"],
        "characters_zh": ["令狐沖", "任盈盈"], "characters_en": ["Linghu Chong", "Ren Yingying"],
        "platform": "TVB",
        "desc_zh": "改編自金庸小說",
        "desc_en": "Adapted from Jin Yong's novel",
        "adaptation_zh": "改編自金庸小說", "adaptation_en": "Adapted from Jin Yong's novel",
    },
    "xue_sha_shuang_long": {
        "zh": "血薦軒轅", "en": "Strike at Heart",
        "genre_zh": "古裝", "genre_en": "Historical",
        "year": 2004, "episodes": 30,
        "cast_zh": ["林峯", "葉璇"], "cast_en": ["Raymond Lam", "Ye Xuan"],
        "characters_zh": [], "characters_en": [],
        "platform": "TVB",
        "desc_zh": "古裝劇",
        "desc_en": "A historical drama",
    },
    "yi_tian_tu_long_ji": {
        "zh": "倚天屠龍記", "en": "The Heaven Sword and Dragon Saber",
        "genre_zh": "武俠", "genre_en": "Wuxia",
        "year": 2001, "episodes": 42,
        "cast_zh": ["吳啟華", "黎姿"], "cast_en": ["Ng Kai Wa", "Gigi Lai"],
        "characters_zh": ["張無忌", "趙敏"], "characters_en": ["Zhang Wuji", "Zhao Min"],
        "platform": "TVB",
        "desc_zh": "改編自金庸小說",
        "desc_en": "Adapted from Jin Yong's novel",
        "adaptation_zh": "改編自金庸小說", "adaptation_en": "Adapted from Jin Yong's novel",
    },
    # ── HK MODERN ──
    "chong_shang_yun_ding": {
        "zh": "衝上雲霄", "en": "Triumph in the Skies",
        "genre_zh": "時裝", "genre_en": "Modern Drama",
        "year": 2003, "episodes": 40,
        "cast_zh": ["吳鎮宇", "陳慧珊", "馬德鐘"], "cast_en": ["Francis Ng", "Flora Chan", "Joe Ma"],
        "characters_zh": ["唐亦琛", "樂以珊"], "characters_en": ["Tong Yat San", "Lok Yi Shan"],
        "platform": "TVB",
        "desc_zh": "講述航空公司機師同空姐嘅故事",
        "desc_en": "A drama about pilots and flight attendants",
    },
    "da_nao_guang_chang": {
        "zh": "大鬧廣昌隆", "en": "A Ghostly Affair",
        "genre_zh": "靈異", "genre_en": "Supernatural",
        "year": 1993, "episodes": 20,
        "cast_zh": ["周海媚", "林家棟"], "cast_en": ["Kathy Chow", "Lam Ka Tung"],
        "characters_zh": [], "characters_en": [],
        "platform": "TVB",
        "desc_zh": "靈異劇，經典人鬼情未了故事",
        "desc_en": "A supernatural romance drama",
    },
    "da_tang_shuang_long": {
        "zh": "大唐雙龍傳", "en": "Twin of Brothers",
        "genre_zh": "古裝", "genre_en": "Historical",
        "year": 2004, "episodes": 42,
        "cast_zh": ["林峯", "吳卓羲"], "cast_en": ["Raymond Lam", "Ron Ng"],
        "characters_zh": ["徐子陵", "寇仲"], "characters_en": ["Xu Ziling", "Kou Zhong"],
        "platform": "TVB",
        "desc_zh": "改編自黃易小說",
        "desc_en": "Adapted from Huang Yi's novel",
        "adaptation_zh": "改編自黃易小說", "adaptation_en": "Adapted from Huang Yi's novel",
    },
    "da_zhang_fu": {
        "zh": "大丈夫", "en": "Men in Charge",
        "genre_zh": "時裝", "genre_en": "Modern Drama",
        "year": 2012, "episodes": 30,
        "cast_zh": ["歐陽震華", "關詠荷"], "cast_en": ["Bobby Au-yeung", "Esther Kwan"],
        "characters_zh": [], "characters_en": [],
        "platform": "TVB",
        "desc_zh": "時裝劇",
        "desc_en": "A modern drama",
    },
    "dian_tang_shi_jie": {
        "zh": "殿堂", "en": "The Drive of Life",
        "genre_zh": "時裝", "genre_en": "Modern Drama",
        "year": 2007, "episodes": 60,
        "cast_zh": ["林峯", "佘詩曼"], "cast_en": ["Raymond Lam", "Charmaine Sheh"],
        "characters_zh": [], "characters_en": [],
        "platform": "TVB",
        "desc_zh": "時裝劇，講述汽車工業嘅故事",
        "desc_en": "A drama about the automobile industry",
    },
    "fei_nv_zhuan": {
        "zh": "肥婆奶奶扭計冤家", "en": "A Kindred Spirit",
        "genre_zh": "處境喜劇", "genre_en": "Sitcom",
        "year": 1995, "episodes": 50,
        "cast_zh": ["薛家燕", "苑瓊丹"], "cast_en": ["Sit Ka Yin", "Kingdom Yuen"],
        "characters_zh": [], "characters_en": [],
        "platform": "TVB",
        "desc_zh": "處境喜劇",
        "desc_en": "A sitcom",
    },
    "gong_wu_jia_qi": {
        "zh": "公公出宮", "en": "Short End of the Stick",
        "genre_zh": "古裝喜劇", "genre_en": "Historical Comedy",
        "year": 2016, "episodes": 32,
        "cast_zh": ["黎耀祥", "胡定欣"], "cast_en": ["Wayne Lai", "Nancy Wu"],
        "characters_zh": [], "characters_en": [],
        "platform": "TVB",
        "desc_zh": "古裝喜劇，講述太監出宮後嘅故事",
        "desc_en": "A comedy about eunuchs after leaving the palace",
    },
    "ji_dao": {
        "zh": "極道", "en": "The Unholy Alliance",
        "genre_zh": "警匪", "genre_en": "Police Drama",
        "year": 2017, "episodes": 30,
        "cast_zh": ["陳展鵬", "胡定欣"], "cast_en": ["Ruco Chan", "Nancy Wu"],
        "characters_zh": [], "characters_en": [],
        "platform": "TVB",
        "desc_zh": "警匪動作劇",
        "desc_en": "An action police drama",
    },
    "jian_zheng_feng_yun": {
        "zh": "鑑證風雲", "en": "Forensic Heroes",
        "genre_zh": "警匪", "genre_en": "Police Drama",
        "year": 2006, "episodes": 25,
        "cast_zh": ["歐陽震華", "蒙嘉慧"], "cast_en": ["Bobby Au-yeung", "Mong Ka Wai"],
        "characters_zh": ["高彥博", "梁小柔"], "characters_en": ["Ko Yim Pok", "Leung Siu Yau"],
        "platform": "TVB",
        "desc_zh": "法證先鋒系列，講述法醫破案嘅故事",
        "desc_en": "The Forensic Heroes series about forensic science solving cases",
    },
    "lie_huo_xiong_xin": {
        "zh": "烈火雄心", "en": "Burning Flame",
        "genre_zh": "時裝", "genre_en": "Modern Drama",
        "year": 1998, "episodes": 35,
        "cast_zh": ["王喜", "古天樂"], "cast_en": ["Wong Hei", "Louis Koo"],
        "characters_zh": ["紀德田"], "characters_en": ["Kei Tak Tin"],
        "platform": "TVB",
        "desc_zh": "消防員劇集，講述消防員嘅英勇故事",
        "desc_en": "A drama about the bravery of firefighters",
    },
    "mi_mi_ji_di": {
        "zh": "妙手仁心", "en": "Healing Hands",
        "genre_zh": "醫療", "genre_en": "Medical Drama",
        "year": 1998, "episodes": 32,
        "cast_zh": ["吳啟華", "蔡少芬"], "cast_en": ["Ng Kai Wa", "Ada Choi"],
        "characters_zh": ["程至美", "唐姿禮"], "characters_en": ["Ching Chi Mei", "Tong Chi Lai"],
        "platform": "TVB",
        "desc_zh": "經典醫療劇，講述醫生嘅故事",
        "desc_en": "A classic medical drama about doctors' lives",
    },
    "mi_tang_you_huo": {
        "zh": "溏心風暴", "en": "Heart of Greed",
        "genre_zh": "時裝", "genre_en": "Modern Drama",
        "year": 2007, "episodes": 40,
        "cast_zh": ["李司棋", "夏雨", "關菊英"], "cast_en": ["Louise Lee", "Ha Yu", "Susanna Kwan"],
        "characters_zh": ["大契", "細契"], "characters_en": ["Tai Kai", "Sai Kai"],
        "platform": "TVB",
        "desc_zh": "家族爭產劇，「大契」金句深入民心",
        "desc_en": "A family drama about inheritance disputes",
    },
    "other": {
        "zh": "其他港劇", "en": "Other HK Modern Dramas",
        "genre_zh": "時裝", "genre_en": "Modern Drama",
        "year": 2010, "episodes": 30,
        "cast_zh": [], "cast_en": [],
        "characters_zh": [], "characters_en": [],
        "platform": "TVB",
        "desc_zh": "其他香港時裝劇嘅綜合題目",
        "desc_en": "Mixed questions about other HK modern dramas",
    },
    "qian_long_xia_jiang_nan": {
        "zh": "乾隆大帝", "en": "The Emperor and I",
        "genre_zh": "古裝", "genre_en": "Historical",
        "year": 1998, "episodes": 20,
        "cast_zh": ["江華", "張可頤"], "cast_en": ["Kwong Wa", "Maggie Cheung Ho Yee"],
        "characters_zh": ["乾隆帝"], "characters_en": ["Emperor Qianlong"],
        "platform": "TVB",
        "desc_zh": "古裝劇，講述乾隆帝嘅故事",
        "desc_en": "A historical drama about Emperor Qianlong",
    },
    "shi_tu_xing_zhe": {
        "zh": "使徒行者", "en": "Line Walker",
        "genre_zh": "警匪", "genre_en": "Police Drama",
        "year": 2014, "episodes": 31,
        "cast_zh": ["苗僑偉", "佘詩曼", "林峯"], "cast_en": ["Miu Kiu Wai", "Charmaine Sheh", "Raymond Lam"],
        "characters_zh": ["卓凱", "釘姐"], "characters_en": ["Cheuk Hoi", "Ding Jie"],
        "platform": "TVB",
        "desc_zh": "臥底警匪劇，當年收視冠軍",
        "desc_en": "An undercover police drama that was a ratings hit",
    },
    "wu_feng_zhi_yun": {
        "zh": "幕後大老爺", "en": "My Unfair Lady",
        "genre_zh": "古裝喜劇", "genre_en": "Historical Comedy",
        "year": 2017, "episodes": 25,
        "cast_zh": ["馬國明", "唐詩詠"], "cast_en": ["Kenneth Ma", "Natalie Tong"],
        "characters_zh": [], "characters_en": [],
        "platform": "TVB",
        "desc_zh": "古裝喜劇",
        "desc_en": "A historical comedy",
    },
    "wu_jian_dao": {
        "zh": "無間道", "en": "Infernal Affairs",
        "genre_zh": "警匪", "genre_en": "Crime Thriller",
        "year": 2022, "episodes": 12,
        "cast_zh": ["羅嘉良", "羅仲謙"], "cast_en": ["Gallen Lo", "Him Law"],
        "characters_zh": [], "characters_en": [],
        "platform": "TVB/邵氏兄弟",
        "desc_zh": "改編自經典電影《無間道》",
        "desc_en": "Adapted from the classic film 'Infernal Affairs'",
        "adaptation_zh": "改編自2002年電影《無間道》", "adaptation_en": "Adapted from the 2002 film 'Infernal Affairs'",
    },
    "yi_wai": {
        "zh": "意外", "en": "The ICAC Investigators",
        "genre_zh": "警匪", "genre_en": "Crime Drama",
        "year": 2019, "episodes": 25,
        "cast_zh": ["黃宗澤"], "cast_en": ["Bosco Wong"],
        "characters_zh": [], "characters_en": [],
        "platform": "TVB",
        "desc_zh": "ICAC廉政公署劇集",
        "desc_en": "An ICAC (Independent Commission Against Corruption) drama",
    },
    "zhu_bao": {
        "zh": "珠光寶氣", "en": "The Gem of Life",
        "genre_zh": "時裝", "genre_en": "Modern Drama",
        "year": 2008, "episodes": 82,
        "cast_zh": ["黎姿", "蔡少芬", "邵美琪"], "cast_en": ["Gigi Lai", "Ada Choi", "Maggie Siu"],
        "characters_zh": ["康雅言", "康雅瞳", "康雅思"], "characters_en": ["Hong Nga Yin", "Hong Nga Tung", "Hong Nga Sz"],
        "platform": "TVB",
        "desc_zh": "講述康家三姊妹嘅故事，當年台慶劇",
        "desc_en": "A drama about three sisters from the Hong family",
    },
    "zhui_zong": {
        "zh": "追蹤", "en": "The Taxidriver",
        "genre_zh": "警匪", "genre_en": "Crime Drama",
        "year": 2014, "episodes": 25,
        "cast_zh": ["郭晉安"], "cast_en": ["Roger Kwok"],
        "characters_zh": [], "characters_en": [],
        "platform": "TVB",
        "desc_zh": "懸疑追蹤劇",
        "desc_en": "A suspenseful crime drama",
    },
    # ── JAPANESE DRAMA ──
    "alice_borderland": {
        "zh": "今際之國的闘士", "en": "Alice in Borderland",
        "genre_zh": "科幻驚悚", "genre_en": "Sci-fi Thriller",
        "year": 2020, "episodes": 16,
        "cast_zh": ["山崎賢人", "土屋太鳳"], "cast_en": ["Kento Yamazaki", "Tao Tsuchiya"],
        "characters_zh": ["有棲良平", "宇佐木柚葉"], "characters_en": ["Arisu", "Usagi"],
        "platform": "Netflix",
        "desc_zh": "改編自麻生羽呂同名漫畫",
        "desc_en": "Adapted from Haro Aso's manga",
        "adaptation_zh": "改編自麻生羽呂漫畫", "adaptation_en": "Adapted from Haro Aso's manga",
    },
    "beautiful_life": {
        "zh": "美麗人生", "en": "Beautiful Life",
        "genre_zh": "愛情", "genre_en": "Romance",
        "year": 2000, "episodes": 11,
        "cast_zh": ["木村拓哉", "常盤貴子"], "cast_en": ["Takuya Kimura", "Takako Tokiwa"],
        "characters_zh": ["沖島柊二", "町田杏子"], "characters_en": ["Shuji Okishima", "Kyoko Machida"],
        "platform": "TBS",
        "desc_zh": "經典日劇，講述髮型師同坐輪椅嘅女圖書館員嘅愛情",
        "desc_en": "A classic J-drama about a hairdresser and a wheelchair-bound librarian",
    },
    "death_note": {
        "zh": "死亡筆記", "en": "Death Note",
        "genre_zh": "懸疑", "genre_en": "Suspense",
        "year": 2015, "episodes": 11,
        "cast_zh": ["窪田正孝", "山崎賢人"], "cast_en": ["Masataka Kubota", "Kento Yamazaki"],
        "characters_zh": ["夜神月", "L"], "characters_en": ["Light Yagami", "L"],
        "platform": "日本電視台",
        "desc_zh": "改編自同名漫畫",
        "desc_en": "Adapted from the manga",
        "adaptation_zh": "改編自大場鶇同小畑健漫畫", "adaptation_en": "Adapted from Tsugumi Ohba and Takeshi Obata's manga",
    },
    "gto": {
        "zh": "麻辣教師GTO", "en": "GTO: Great Teacher Onizuka",
        "genre_zh": "校園喜劇", "genre_en": "School Comedy",
        "year": 1998, "episodes": 12,
        "cast_zh": ["反町隆史", "松島菜菜子"], "cast_en": ["Takashi Sorimachi", "Nanako Matsushima"],
        "characters_zh": ["鬼塚英吉", "冬月梓"], "characters_en": ["Eikichi Onizuka", "Azusa Fuyutsuki"],
        "platform": "富士電視台",
        "desc_zh": "改編自同名漫畫",
        "desc_en": "Adapted from the manga",
        "adaptation_zh": "改編自藤澤亨漫畫", "adaptation_en": "Adapted from Tooru Fujisawa's manga",
    },
    "hanzawa_naoki": {
        "zh": "半澤直樹", "en": "Hanzawa Naoki",
        "genre_zh": "職場", "genre_en": "Workplace Drama",
        "year": 2013, "episodes": 20,
        "cast_zh": ["堺雅人", "上戶彩"], "cast_en": ["Masato Sakai", "Aya Ueto"],
        "characters_zh": ["半澤直樹", "半澤花"], "characters_en": ["Naoki Hanzawa", "Hana Hanzawa"],
        "platform": "TBS",
        "desc_zh": "銀行職場劇，「加倍奉還」成為流行語",
        "desc_en": "A banking drama that spawned the catchphrase 'I will pay you back double'",
    },
    "hero": {
        "zh": "律政英雄", "en": "Hero",
        "genre_zh": "律政", "genre_en": "Legal Drama",
        "year": 2001, "episodes": 11,
        "cast_zh": ["木村拓哉", "松隆子"], "cast_en": ["Takuya Kimura", "Takako Matsu"],
        "characters_zh": ["久利生公平", "雨宮舞子"], "characters_en": ["Kohei Kuryu", "Maiko Amamiya"],
        "platform": "富士電視台",
        "desc_zh": "律政劇，木村拓哉飾演不按牌理出牌嘅檢察官",
        "desc_en": "A legal drama starring Kimura as an unconventional prosecutor",
    },
    "jin": {
        "zh": "仁醫", "en": "Jin",
        "genre_zh": "穿越", "genre_en": "Time Travel",
        "year": 2009, "episodes": 11,
        "cast_zh": ["大澤隆夫", "中谷美紀"], "cast_en": ["Takao Osawa", "Miki Nakatani"],
        "characters_zh": ["南方仁"], "characters_en": ["Jin Minakata"],
        "platform": "TBS",
        "desc_zh": "穿越劇，現代外科醫生回到幕末時代",
        "desc_en": "A time-travel drama about a modern surgeon in the Edo period",
        "adaptation_zh": "改編自村上也香志同名漫畫", "adaptation_en": "Adapted from Murakami Motoka's manga",
    },
    "kaseifu_no_mita": {
        "zh": "家政婦三田", "en": "I'm Mita, Your Housekeeper",
        "genre_zh": "家庭", "genre_en": "Family Drama",
        "year": 2011, "episodes": 11,
        "cast_zh": ["松嶋菜菜子"], "cast_en": ["Nanako Matsushima"],
        "characters_zh": ["三田燈"], "characters_en": ["Mita Akari"],
        "platform": "日本電視台",
        "desc_zh": "講述一個什麼都做嘅家政婦同失去母親嘅家庭嘅故事",
        "desc_en": "About a housekeeper who will do anything for a grieving family",
    },
    "last_friends": {
        "zh": "最後的朋友", "en": "Last Friends",
        "genre_zh": "群像劇", "genre_en": "Ensemble Drama",
        "year": 2008, "episodes": 11,
        "cast_zh": ["長澤正美", "上野樹里", "瑛太"], "cast_en": ["Masami Nagasawa", "Juri Ueno", "Eita"],
        "characters_zh": ["藍田美知留", "岸本瑠可"], "characters_en": ["Michiru Aida", "Ruka Kishimoto"],
        "platform": "富士電視台",
        "desc_zh": "探討家庭暴力、性別認同等社會議題",
        "desc_en": "Explores domestic violence and gender identity issues",
    },
    "long_vacation": {
        "zh": "悠長假期", "en": "Long Vacation",
        "genre_zh": "愛情", "genre_en": "Romance",
        "year": 1996, "episodes": 12,
        "cast_zh": ["木村拓哉", "山口智子"], "cast_en": ["Takuya Kimura", "Tomoko Yamaguchi"],
        "characters_zh": ["瀬名秀俊", "葉山南"], "characters_en": ["Hidetoshi Sena", "Minami Hayama"],
        "platform": "富士電視台",
        "desc_zh": "經典愛情劇，木村拓哉飾演鋼琴家",
        "desc_en": "A classic romance drama with Kimura as a pianist",
    },
    "nobuta_wo_produce": {
        "zh": "野豬大改造", "en": "Nobuta wo Produce",
        "genre_zh": "校園", "genre_en": "School Drama",
        "year": 2005, "episodes": 10,
        "cast_zh": ["山下智久", "龜梨和也", "戶田惠梨香"], "cast_en": ["Tomohisa Yamashita", "Kamenashi Kazuya", "Erika Toda"],
        "characters_zh": ["桐谷修二", "草野彰", "小谷信子"], "characters_en": ["Shuji Kiritani", "Akira Kusano", "Nobuko Kotani"],
        "platform": "日本電視台",
        "desc_zh": "校園劇，兩個男生幫助被欺凌嘅女同學重拾自信",
        "desc_en": "A school drama about two boys helping a bullied girl",
    },
    "orange_days": {
        "zh": "Orange Days", "en": "Orange Days",
        "genre_zh": "愛情", "genre_en": "Romance",
        "year": 2004, "episodes": 11,
        "cast_zh": ["妻夫木聰", "柴崎幸"], "cast_en": ["Satoshi Tsumabuki", "Kou Shibasaki"],
        "characters_zh": ["結城櫂"], "characters_en": ["Kai Yuki"],
        "platform": "TBS",
        "desc_zh": "大學愛情劇，講述聽障女孩同大學生嘅愛情",
        "desc_en": "A campus romance between a hearing-impaired girl and a university student",
    },
    "other": {
        "zh": "其他日劇", "en": "Other Japanese Dramas",
        "genre_zh": "綜合", "genre_en": "Mixed",
        "year": 2010, "episodes": 11,
        "cast_zh": [], "cast_en": [],
        "characters_zh": [], "characters_en": [],
        "platform": "",
        "desc_zh": "其他日劇嘅綜合題目",
        "desc_en": "Mixed questions about other Japanese dramas",
    },
    "tokyo_love_story": {
        "zh": "東京愛情故事", "en": "Tokyo Love Story",
        "genre_zh": "愛情", "genre_en": "Romance",
        "year": 1991, "episodes": 11,
        "cast_zh": ["織田裕二", "鈴木保奈美"], "cast_en": ["Yuji Oda", "Honami Suzuki"],
        "characters_zh": ["永尾完治", "赤名莉香"], "characters_en": ["Kanji Nagao", "Rika Akana"],
        "platform": "富士電視台",
        "desc_zh": "90年代經典愛情劇",
        "desc_en": "A 90s classic romance",
        "adaptation_zh": "改編自柴門文漫畫", "adaptation_en": "Adapted from Fumi Saimon's manga",
    },
    "trick": {
        "zh": "Trick", "en": "Trick",
        "genre_zh": "懸疑喜劇", "genre_en": "Mystery Comedy",
        "year": 2000, "episodes": 10,
        "cast_zh": ["仲間由紀惠", "阿部寬"], "cast_en": ["Yukie Nakama", "Hiroshi Abe"],
        "characters_zh": ["山田奈緒子", "上田次郎"], "characters_en": ["Naoko Yamada", "Jiro Ueda"],
        "platform": "朝日電視台",
        "desc_zh": "懸疑喜劇，講述魔術師同物理學家聯手破解超自然事件",
        "desc_en": "A mystery comedy about a magician and physicist debunking supernatural events",
    },
    "water_boys": {
        "zh": "水男孩", "en": "Water Boys",
        "genre_zh": "校園喜劇", "genre_en": "School Comedy",
        "year": 2003, "episodes": 11,
        "cast_zh": ["山田孝之", "妻夫木聰"], "cast_en": ["Takayuki Yamada", "Satoshi Tsumabuki"],
        "characters_zh": ["進藤勘九郎"], "characters_en": ["Kankuro Shindo"],
        "platform": "富士電視台",
        "desc_zh": "校園喜劇，講述男生們學習水上芭蕾嘅故事",
        "desc_en": "A school comedy about boys learning synchronized swimming",
    },
    "your_turn_to_kill": {
        "zh": "輪到你了", "en": "Your Turn to Kill",
        "genre_zh": "懸疑", "genre_en": "Mystery",
        "year": 2019, "episodes": 20,
        "cast_zh": ["唐澤壽明", "廣末涼子"], "cast_en": ["Toshiaki Karisawa", "Ryoko Hirosue"],
        "characters_zh": [], "characters_en": [],
        "platform": "日本電視台",
        "desc_zh": "懸疑劇，居民們輪流「投票」殺人",
        "desc_en": "A mystery drama about residents taking turns to vote for elimination",
    },
    # ── KOREAN DRAMA ──
    "all_of_us_dead": {
        "zh": "殭屍校園", "en": "All of Us Are Dead",
        "genre_zh": "殭屍", "genre_en": "Zombie Horror",
        "year": 2022, "episodes": 12,
        "cast_zh": ["朴持厚", "尹燦榮"], "cast_en": ["Park Ji-hoo", "Yoon Chan-young"],
        "characters_zh": ["南溫召", "李青山"], "characters_en": ["Nam On-jo", "Lee Cheong-san"],
        "platform": "Netflix",
        "desc_zh": "改編自網絡漫畫",
        "desc_en": "Adapted from a webtoon",
        "adaptation_zh": "改編自朱東根網絡漫畫", "adaptation_en": "Adapted from Joo Dong-geun's webtoon",
    },
    "crash_landing": {
        "zh": "愛的迫降", "en": "Crash Landing on You",
        "genre_zh": "愛情", "genre_en": "Romance",
        "year": 2019, "episodes": 16,
        "cast_zh": ["玄彬", "孫藝珍"], "cast_en": ["Hyun Bin", "Son Ye-jin"],
        "characters_zh": ["利正赫", "尹世理"], "characters_en": ["Ri Jeong-hyeok", "Yoon Se-ri"],
        "platform": "tvN",
        "desc_zh": "講述南韓財閥女意外降落北韓同軍官嘅愛情故事",
        "desc_en": "A South Korean heiress crash-lands in North Korea and falls for an army officer",
    },
    "descendants_sun": {
        "zh": "太陽的後裔", "en": "Descendants of the Sun",
        "genre_zh": "愛情", "genre_en": "Romance",
        "year": 2016, "episodes": 16,
        "cast_zh": ["宋仲基", "宋慧喬"], "cast_en": ["Song Joong-ki", "Song Hye-kyo"],
        "characters_zh": ["柳時鎮", "姜暮煙"], "characters_en": ["Yoo Si-jin", "Kang Mo-yeon"],
        "platform": "KBS2",
        "desc_zh": "講述特種兵同醫生嘅愛情故事，風靡全亞洲",
        "desc_en": "A romance between a special forces captain and a doctor, a pan-Asian hit",
    },
    "extraordinary_attorney": {
        "zh": "非常律師禹英禑", "en": "Extraordinary Attorney Woo",
        "genre_zh": "律政", "genre_en": "Legal Drama",
        "year": 2022, "episodes": 16,
        "cast_zh": ["朴恩斌", "姜泰伍"], "cast_en": ["Park Eun-bin", "Kang Tae-oh"],
        "characters_zh": ["禹英禑", "李俊浩"], "characters_en": ["Woo Young-woo", "Lee Jun-ho"],
        "platform": "ENA",
        "desc_zh": "講述自閉症譜系障礙律師嘅成長故事",
        "desc_en": "About an autistic attorney's growth at a prestigious law firm",
    },
    "glory": {
        "zh": "黑暗榮耀", "en": "The Glory",
        "genre_zh": "復仇", "genre_en": "Revenge Thriller",
        "year": 2022, "episodes": 16,
        "cast_zh": ["宋慧喬", "李到晛"], "cast_en": ["Song Hye-kyo", "Lee Do-hyun"],
        "characters_zh": ["文同珢"], "characters_en": ["Moon Dong-eun"],
        "platform": "Netflix",
        "desc_zh": "復仇劇，講述校園暴力受害者精心策劃嘅復仇",
        "desc_en": "A revenge drama about a school bullying victim's meticulously planned revenge",
    },
    "goblin": {
        "zh": "鬼怪", "en": "Guardian: The Lonely and Great God",
        "genre_zh": "奇幻愛情", "genre_en": "Fantasy Romance",
        "year": 2016, "episodes": 16,
        "cast_zh": ["孔劉", "金高銀", "李棟旭"], "cast_en": ["Gong Yoo", "Kim Go-eun", "Lee Dong-wook"],
        "characters_zh": ["金侁", "池恩倬", "死神"], "characters_en": ["Kim Shin", "Ji Eun-tak", "Grim Reaper"],
        "platform": "tvN",
        "desc_zh": "奇幻愛情劇，講述鬼怪新娘嘅故事",
        "desc_en": "A fantasy romance about a goblin and his bride",
    },
    "itaewon_class": {
        "zh": "梨泰院Class", "en": "Itaewon Class",
        "genre_zh": "復仇", "genre_en": "Revenge Drama",
        "year": 2020, "episodes": 16,
        "cast_zh": ["朴敘俊", "金多美"], "cast_en": ["Park Seo-joon", "Kim Da-mi"],
        "characters_zh": ["朴世路", "趙以瑞"], "characters_en": ["Park Saeroyi", "Jo Yi-seo"],
        "platform": "JTBC",
        "desc_zh": "改編自網絡漫畫",
        "desc_en": "Adapted from a webtoon",
        "adaptation_zh": "改編自趙光真網絡漫畫", "adaptation_en": "Adapted from Jo Gwang-jin's webtoon",
    },
    "kingdom": {
        "zh": "王國", "en": "Kingdom",
        "genre_zh": "古裝殭屍", "genre_en": "Historical Zombie",
        "year": 2019, "episodes": 12,
        "cast_zh": ["朱智勛", "裴斗娜"], "cast_en": ["Ju Ji-hoon", "Bae Doona"],
        "characters_zh": ["李蒼", "徐菲"], "characters_en": ["Prince Lee Chang", "Seo-bi"],
        "platform": "Netflix",
        "desc_zh": "朝鮮時代殭屍劇",
        "desc_en": "A Joseon-era zombie drama",
        "adaptation_zh": "改編自網絡漫畫《神的國度》", "adaptation_en": "Adapted from the webtoon 'The Kingdom of the Gods'",
    },
    "mask_girl": {
        "zh": "假面女郎", "en": "Mask Girl",
        "genre_zh": "驚悚", "genre_en": "Thriller",
        "year": 2023, "episodes": 7,
        "cast_zh": ["高賢廷", "Nana"], "cast_en": ["Go Hyun-jung", "Nana"],
        "characters_zh": ["金貌美"], "characters_en": ["Kim Mo-mi"],
        "platform": "Netflix",
        "desc_zh": "改編自網絡漫畫",
        "desc_en": "Adapted from a webtoon",
        "adaptation_zh": "改編自網絡漫畫", "adaptation_en": "Adapted from the webtoon",
    },
    "moving": {
        "zh": "異能", "en": "Moving",
        "genre_zh": "超能力", "genre_en": "Superpower Drama",
        "year": 2023, "episodes": 20,
        "cast_zh": ["趙寅成", "韓孝周", "柳承龍"], "cast_en": ["Zo In-sung", "Han Hyo-joo", "Ryu Seung-ryong"],
        "characters_zh": ["金奉皙", "李美賢"], "characters_en": ["Kim Bong-seok", "Lee Mi-hyun"],
        "platform": "Disney+",
        "desc_zh": "改編自網絡漫畫",
        "desc_en": "Adapted from a webtoon",
        "adaptation_zh": "改編自姜草網絡漫畫", "adaptation_en": "Adapted from Kang Full's webtoon",
    },
    "my_love_from_star": {
        "zh": "來自星星的你", "en": "My Love from the Star",
        "genre_zh": "奇幻愛情", "genre_en": "Fantasy Romance",
        "year": 2013, "episodes": 21,
        "cast_zh": ["金秀賢", "全智賢"], "cast_en": ["Kim Soo-hyun", "Jun Ji-hyun"],
        "characters_zh": ["都敏俊", "千頌伊"], "characters_en": ["Do Min-joon", "Cheon Song-yi"],
        "platform": "SBS",
        "desc_zh": "講述外星人喺地球生活400年後愛上頂級女星嘅故事",
        "desc_en": "About an alien who has lived on Earth for 400 years falling for a top actress",
    },
    "other": {
        "zh": "其他韓劇", "en": "Other Korean Dramas",
        "genre_zh": "綜合", "genre_en": "Mixed",
        "year": 2020, "episodes": 16,
        "cast_zh": [], "cast_en": [],
        "characters_zh": [], "characters_en": [],
        "platform": "",
        "desc_zh": "其他韓劇嘅綜合題目",
        "desc_en": "Mixed questions about other Korean dramas",
    },
    "reply_1988": {
        "zh": "請回答1988", "en": "Reply 1988",
        "genre_zh": "家庭", "genre_en": "Family Drama",
        "year": 2015, "episodes": 20,
        "cast_zh": ["李惠利", "柳俊烈", "朴寶劍"], "cast_en": ["Lee Hye-ri", "Ryu Jun-yeol", "Park Bo-gum"],
        "characters_zh": ["成德善", "金正煥", "崔澤"], "characters_en": ["Sung Deok-sun", "Kim Jung-hwan", "Choi Taek"],
        "platform": "tvN",
        "desc_zh": "以1988年首爾雙門洞為背景",
        "desc_en": "Set in 1988 Seoul's Ssangmun-dong",
    },
    "signal": {
        "zh": "Signal", "en": "Signal",
        "genre_zh": "懸疑", "genre_en": "Mystery Thriller",
        "year": 2016, "episodes": 16,
        "cast_zh": ["李帝勳", "趙震雄", "金惠秀"], "cast_en": ["Lee Je-hoon", "Cho Jin-woong", "Kim Hye-soo"],
        "characters_zh": ["朴海英", "李材韓"], "characters_en": ["Park Hae-young", "Lee Jae-han"],
        "platform": "tvN",
        "desc_zh": "講述通過對講機跨越時空聯手破案嘅故事",
        "desc_en": "About solving cold cases across time through a walkie-talkie",
    },
    "sky_castle": {
        "zh": "Sky Castle", "en": "SKY Castle",
        "genre_zh": "諷刺", "genre_en": "Satire Drama",
        "year": 2018, "episodes": 20,
        "cast_zh": ["廉晶雅", "李泰蘭"], "cast_en": ["Yum Jung-ah", "Lee Tae-ran"],
        "characters_zh": ["韓瑞珍"], "characters_en": ["Han Seo-jin"],
        "platform": "JTBC",
        "desc_zh": "諷刺韓國上流社會教育狂熱嘅黑色喜劇",
        "desc_en": "A dark satire about the education obsession of Korea's elite",
    },
    "squid_game": {
        "zh": "魷魚遊戲", "en": "Squid Game",
        "genre_zh": "驚悚", "genre_en": "Thriller",
        "year": 2021, "episodes": 9,
        "cast_zh": ["李政宰", "朴海秀"], "cast_en": ["Lee Jung-jae", "Park Hae-soo"],
        "characters_zh": ["成奇勳", "曹尚佑"], "characters_en": ["Seong Gi-hun", "Cho Sang-woo"],
        "platform": "Netflix",
        "desc_zh": "講述456名負債者參加致命兒童遊戲爭取巨額獎金",
        "desc_en": "456 debt-ridden players compete in deadly children's games for a huge cash prize",
    },
    "vincenzo": {
        "zh": "Vincenzo", "en": "Vincenzo",
        "genre_zh": "黑色喜劇", "genre_en": "Dark Comedy",
        "year": 2021, "episodes": 20,
        "cast_zh": ["宋仲基", "全汝彬"], "cast_en": ["Song Joong-ki", "Jeon Yeo-been"],
        "characters_zh": ["Vincenzo", "洪車瑛"], "characters_en": ["Vincenzo Cassano", "Hong Cha-young"],
        "platform": "tvN",
        "desc_zh": "講述意大利黑手黨律師回到韓國用以暴制暴嘅方式伸張正義",
        "desc_en": "An Italian mafia lawyer returns to Korea and fights injustice his own way",
    },
    "world_of_married": {
        "zh": "夫妻的世界", "en": "The World of the Married",
        "genre_zh": "復仇", "genre_en": "Revenge Drama",
        "year": 2020, "episodes": 16,
        "cast_zh": ["金喜愛", "朴海俊"], "cast_en": ["Kim Hee-ae", "Park Hae-joon"],
        "characters_zh": ["池善雨"], "characters_en": ["Ji Sun-woo"],
        "platform": "JTBC",
        "desc_zh": "改編自英劇《Doctor Foster》",
        "desc_en": "Adapted from 'Doctor Foster'",
        "adaptation_zh": "改編自英劇《Doctor Foster》", "adaptation_en": "Adapted from BBC's 'Doctor Foster'",
    },
    # ── VARIETY SHOW ──
    "back_to_field": {
        "zh": "嚮往的生活", "en": "Back to Field",
        "genre_zh": "真人秀", "genre_en": "Reality Show",
        "year": 2017, "episodes": 80,
        "cast_zh": ["何炅", "黃磊", "彭昱暢"], "cast_en": ["He Jiong", "Huang Lei", "Peng Yuchang"],
        "characters_zh": [], "characters_en": [],
        "platform": "湖南衛視",
        "desc_zh": "田園生活真人秀",
        "desc_en": "A rural reality show",
    },
    "dad_where_are_we": {
        "zh": "爸爸去哪兒", "en": "Where Are We Going, Dad?",
        "genre_zh": "親子真人秀", "genre_en": "Parenting Reality",
        "year": 2013, "episodes": 60,
        "cast_zh": ["林志穎", "田亮"], "cast_en": ["Jimmy Lin", "Tian Liang"],
        "characters_zh": [], "characters_en": [],
        "platform": "湖南衛視",
        "desc_zh": "親子真人秀，爸爸帶仔女去旅行",
        "desc_en": "A parenting reality show where dads take their kids on trips",
    },
    "day_day_up": {
        "zh": "天天向上", "en": "Day Day Up",
        "genre_zh": "綜藝", "genre_en": "Variety Show",
        "year": 2008, "episodes": 500,
        "cast_zh": ["汪涵", "大張偉"], "cast_en": ["Wang Han", "Da Zhangwei"],
        "characters_zh": [], "characters_en": [],
        "platform": "湖南衛視",
        "desc_zh": "知識性綜藝節目",
        "desc_en": "An educational variety show",
    },
    "happy_camp": {
        "zh": "快樂大本營", "en": "Happy Camp",
        "genre_zh": "綜藝", "genre_en": "Variety Show",
        "year": 1997, "episodes": 1000,
        "cast_zh": ["何炅", "謝娜", "李維嘉"], "cast_en": ["He Jiong", "Xie Na", "Wei Jia"],
        "characters_zh": [], "characters_en": [],
        "platform": "湖南衛視",
        "desc_zh": "中國最長壽綜藝節目之一",
        "desc_en": "One of China's longest-running variety shows",
    },
    "i_am_a_singer": {
        "zh": "我是歌手", "en": "I Am a Singer",
        "genre_zh": "音樂競演", "genre_en": "Music Competition",
        "year": 2013, "episodes": 80,
        "cast_zh": [], "cast_en": [],
        "characters_zh": [], "characters_en": [],
        "platform": "湖南衛視",
        "desc_zh": "專業歌手競演節目，後改名為《歌手》",
        "desc_en": "A professional singing competition later renamed 'Singer'",
    },
    "infinity_challenge": {
        "zh": "無限挑戰", "en": "Infinite Challenge",
        "genre_zh": "綜藝", "genre_en": "Variety Show",
        "year": 2005, "episodes": 563,
        "cast_zh": ["劉在錫", "朴明洙"], "cast_en": ["Yoo Jae-suk", "Park Myung-soo"],
        "characters_zh": [], "characters_en": [],
        "platform": "MBC",
        "desc_zh": "韓國國民綜藝，被譽為韓國綜藝嘅教科書",
        "desc_en": "Korea's national variety show, considered the textbook of Korean entertainment",
    },
    "keep_running": {
        "zh": "奔跑吧", "en": "Keep Running",
        "genre_zh": "真人秀", "genre_en": "Reality Show",
        "year": 2014, "episodes": 100,
        "cast_zh": ["李晨", "Angelababy", "鄭愷"], "cast_en": ["Li Chen", "Angelababy", "Zheng Kai"],
        "characters_zh": [], "characters_en": [],
        "platform": "浙江衛視",
        "desc_zh": "改編自韓國《Running Man》",
        "desc_en": "Adapted from Korea's 'Running Man'",
        "adaptation_zh": "改編自韓國SBS《Running Man》", "adaptation_en": "Adapted from SBS's 'Running Man'",
    },
    "other": {
        "zh": "其他綜藝", "en": "Other Variety Shows",
        "genre_zh": "綜藝", "genre_en": "Variety Show",
        "year": 2020, "episodes": 50,
        "cast_zh": [], "cast_en": [],
        "characters_zh": [], "characters_en": [],
        "platform": "",
        "desc_zh": "其他綜藝節目嘅綜合題目",
        "desc_en": "Mixed questions about other variety shows",
    },
    "produce_101": {
        "zh": "Produce 101", "en": "Produce 101",
        "genre_zh": "選秀", "genre_en": "Talent Competition",
        "year": 2016, "episodes": 11,
        "cast_zh": [], "cast_en": [],
        "characters_zh": [], "characters_en": [],
        "platform": "Mnet",
        "desc_zh": "韓國選秀節目，觀眾投票選出出道組合",
        "desc_en": "A Korean survival show where viewers vote to form debut groups",
    },
    "rap_of_china": {
        "zh": "中國有嘻哈", "en": "The Rap of China",
        "genre_zh": "音樂競演", "genre_en": "Music Competition",
        "year": 2017, "episodes": 60,
        "cast_zh": ["吳亦凡", "潘瑋柏"], "cast_en": ["Kris Wu", "Wilber Pan"],
        "characters_zh": [], "characters_en": [],
        "platform": "愛奇藝",
        "desc_zh": "中國首個大型嘻哈選秀節目",
        "desc_en": "China's first large-scale hip-hop competition show",
    },
    "running_man": {
        "zh": "Running Man", "en": "Running Man",
        "genre_zh": "綜藝", "genre_en": "Variety Show",
        "year": 2010, "episodes": 600,
        "cast_zh": ["劉在錫", "池石鎮", "金鐘國"], "cast_en": ["Yoo Jae-suk", "Jee Seok-jin", "Kim Jong-kook"],
        "characters_zh": [], "characters_en": [],
        "platform": "SBS",
        "desc_zh": "韓國長壽綜藝節目，以追逐遊戲聞名",
        "desc_en": "Korea's long-running variety show famous for its tag games",
    },
    "singer": {
        "zh": "歌手", "en": "Singer",
        "genre_zh": "音樂競演", "genre_en": "Music Competition",
        "year": 2017, "episodes": 40,
        "cast_zh": [], "cast_en": [],
        "characters_zh": [], "characters_en": [],
        "platform": "湖南衛視",
        "desc_zh": "《我是歌手》改名後嘅版本",
        "desc_en": "The renamed version of 'I Am a Singer'",
    },
    "street_dance": {
        "zh": "這！就是街舞", "en": "Street Dance of China",
        "genre_zh": "舞蹈競演", "genre_en": "Dance Competition",
        "year": 2018, "episodes": 40,
        "cast_zh": ["易烊千璽", "羅志祥"], "cast_en": ["Jackson Yee", "Show Lo"],
        "characters_zh": [], "characters_en": [],
        "platform": "優酷",
        "desc_zh": "街舞選秀節目",
        "desc_en": "A street dance competition show",
    },
    # ── WESTERN TV ──
    "black_mirror": {
        "zh": "黑鏡", "en": "Black Mirror",
        "genre_zh": "科幻選集", "genre_en": "Sci-fi Anthology",
        "year": 2011, "episodes": 27,
        "cast_zh": [], "cast_en": [],
        "characters_zh": [], "characters_en": [],
        "platform": "Netflix/Channel 4",
        "desc_zh": "選集式科幻劇，每集探討科技對社會嘅影響",
        "desc_en": "An anthology sci-fi series exploring technology's impact on society",
        "creator_zh": "查理·布魯克", "creator_en": "Charlie Brooker",
    },
    "breaking_bad": {
        "zh": "絕命毒師", "en": "Breaking Bad",
        "genre_zh": "犯罪", "genre_en": "Crime Drama",
        "year": 2008, "episodes": 62,
        "cast_zh": ["白恩·高斯汀", "亞倫·保羅"], "cast_en": ["Bryan Cranston", "Aaron Paul"],
        "characters_zh": ["沃特·懷特", "傑西·平克曼"], "characters_en": ["Walter White", "Jesse Pinkman"],
        "platform": "AMC",
        "desc_zh": "講述化學老師確診癌症後製毒嘅故事",
        "desc_en": "A chemistry teacher turns to manufacturing meth after a cancer diagnosis",
        "creator_zh": "文斯·吉利根", "creator_en": "Vince Gilligan",
    },
    "crown": {
        "zh": "王冠", "en": "The Crown",
        "genre_zh": "歷史傳記", "genre_en": "Historical Biography",
        "year": 2016, "episodes": 60,
        "cast_zh": ["嘉莉·科根", "奧利花高文"], "cast_en": ["Claire Foy", "Olivia Colman", "Imelda Staunton"],
        "characters_zh": ["伊麗莎白二世"], "characters_en": ["Queen Elizabeth II"],
        "platform": "Netflix",
        "desc_zh": "講述英女王伊麗莎白二世嘅統治生涯",
        "desc_en": "Chronicles the reign of Queen Elizabeth II",
    },
    "friends": {
        "zh": "老友記", "en": "Friends",
        "genre_zh": "處境喜劇", "genre_en": "Sitcom",
        "year": 1994, "episodes": 236,
        "cast_zh": ["珍妮花·安妮絲頓", "哥迪妮·雅", "麗莎·古露"], "cast_en": ["Jennifer Aniston", "Courteney Cox", "Lisa Kudrow", "Matt LeBlanc", "Matthew Perry", "David Schwimmer"],
        "characters_zh": ["瑞秋", "莫妮卡", "菲比", "祖伊", "錢德", "羅斯"], "characters_en": ["Rachel", "Monica", "Phoebe", "Joey", "Chandler", "Ross"],
        "platform": "NBC",
        "desc_zh": "六個朋友喺紐約嘅生活喜劇",
        "desc_en": "A sitcom about six friends in New York",
        "creator_zh": "大衛·克萊恩/瑪爾塔·考夫曼", "creator_en": "David Crane & Marta Kauffman",
    },
    "game_of_thrones": {
        "zh": "權力的遊戲", "en": "Game of Thrones",
        "genre_zh": "奇幻", "genre_en": "Fantasy",
        "year": 2011, "episodes": 73,
        "cast_zh": ["琦特·夏靈頓", "艾美莉·克拉克"], "cast_en": ["Kit Harington", "Emilia Clarke", "Peter Dinklage"],
        "characters_zh": ["雪諾", "丹妮莉絲", "小惡魔"], "characters_en": ["Jon Snow", "Daenerys Targaryen", "Tyrion Lannister"],
        "platform": "HBO",
        "desc_zh": "改編自喬治·R·R·馬丁小說，史詩奇幻巨作",
        "desc_en": "Adapted from George R.R. Martin's novels, an epic fantasy saga",
        "adaptation_zh": "改編自《冰與火之歌》系列小說", "adaptation_en": "Adapted from 'A Song of Ice and Fire' novel series",
        "creator_zh": "大衛·班尼奧夫/D·B·威斯", "creator_en": "David Benioff & D.B. Weiss",
    },
    "house_of_dragon": {
        "zh": "龍之家族", "en": "House of the Dragon",
        "genre_zh": "奇幻", "genre_en": "Fantasy",
        "year": 2022, "episodes": 20,
        "cast_zh": ["馬特·史密斯", "艾瑪·戴西"], "cast_en": ["Matt Smith", "Emma D'Arcy"],
        "characters_zh": ["戴蒙", "雷妮拉"], "characters_en": ["Daemon Targaryen", "Rhaenyra Targaryen"],
        "platform": "HBO",
        "desc_zh": "《權力的遊戲》前傳，講述坦格利安家族嘅內戰",
        "desc_en": "A 'Game of Thrones' prequel about the Targaryen civil war",
        "adaptation_zh": "改編自馬丁小說《火與血》", "adaptation_en": "Adapted from Martin's 'Fire & Blood'",
    },
    "last_of_us": {
        "zh": "最後生還者", "en": "The Last of Us",
        "genre_zh": "末日", "genre_en": "Post-apocalyptic",
        "year": 2023, "episodes": 18,
        "cast_zh": ["柏度·柏斯卡", "貝拉·拉姆齊"], "cast_en": ["Pedro Pascal", "Bella Ramsey"],
        "characters_zh": ["祖爾", "艾莉"], "characters_en": ["Joel", "Ellie"],
        "platform": "HBO",
        "desc_zh": "改編自同名遊戲，末日背景下嘅生存故事",
        "desc_en": "Adapted from the video game, a post-apocalyptic survival story",
        "adaptation_zh": "改編自Naughty Dog同名遊戲", "adaptation_en": "Adapted from Naughty Dog's video game",
    },
    "mandalorian": {
        "zh": "曼達洛人", "en": "The Mandalorian",
        "genre_zh": "科幻", "genre_en": "Sci-fi",
        "year": 2019, "episodes": 24,
        "cast_zh": ["柏度·柏斯卡"], "cast_en": ["Pedro Pascal"],
        "characters_zh": ["曼達洛人", "尤達寶寶"], "characters_en": ["The Mandalorian", "Grogu"],
        "platform": "Disney+",
        "desc_zh": "星球大戰宇宙劇集",
        "desc_en": "A Star Wars universe series",
    },
    "office": {
        "zh": "辦公室", "en": "The Office (US)",
        "genre_zh": "處境喜劇", "genre_en": "Sitcom",
        "year": 2005, "episodes": 201,
        "cast_zh": ["史提夫·卡爾", "尊·堅尼地"], "cast_en": ["Steve Carell", "John Krasinski", "Rainn Wilson"],
        "characters_zh": ["米高·史葛", "吉姆", "德懷特"], "characters_en": ["Michael Scott", "Jim Halpert", "Dwight Schrute"],
        "platform": "NBC",
        "desc_zh": "改編自英劇，以偽紀錄片形式講述辦公室生活",
        "desc_en": "Adapted from the UK series, a mockumentary about office life",
        "adaptation_zh": "改編自英國版《The Office》", "adaptation_en": "Adapted from the UK version created by Ricky Gervais",
    },
    "other": {
        "zh": "其他歐美劇", "en": "Other Western TV",
        "genre_zh": "綜合", "genre_en": "Mixed",
        "year": 2020, "episodes": 10,
        "cast_zh": [], "cast_en": [],
        "characters_zh": [], "characters_en": [],
        "platform": "",
        "desc_zh": "其他歐美劇集嘅綜合題目",
        "desc_en": "Mixed questions about other Western TV shows",
    },
    "rings_of_power": {
        "zh": "力量之戒", "en": "The Rings of Power",
        "genre_zh": "奇幻", "genre_en": "Fantasy",
        "year": 2022, "episodes": 16,
        "cast_zh": ["摩菲德·克拉克"], "cast_en": ["Morfydd Clark"],
        "characters_zh": ["加拉德瑞爾"], "characters_en": ["Galadriel"],
        "platform": "Amazon Prime",
        "desc_zh": "改編自托爾金作品，《魔戒》前傳",
        "desc_en": "Adapted from Tolkien's works, a prequel to 'The Lord of the Rings'",
        "adaptation_zh": "改編自J·R·R·托爾金嘅附錄", "adaptation_en": "Adapted from J.R.R. Tolkien's appendices",
    },
    "seinfeld": {
        "zh": "宋飛傳", "en": "Seinfeld",
        "genre_zh": "處境喜劇", "genre_en": "Sitcom",
        "year": 1989, "episodes": 180,
        "cast_zh": ["謝利·宋飛", "積遜·阿歷山大"], "cast_en": ["Jerry Seinfeld", "Jason Alexander", "Julia Louis-Dreyfus"],
        "characters_zh": ["謝利", "佐治", "伊蓮"], "characters_en": ["Jerry", "George", "Elaine", "Kramer"],
        "platform": "NBC",
        "desc_zh": "被稱為「關於無嘅節目」，90年代經典喜劇",
        "desc_en": "Known as 'the show about nothing', a classic 90s sitcom",
    },
    "sherlock": {
        "zh": "新福爾摩斯", "en": "Sherlock",
        "genre_zh": "懸疑", "genre_en": "Mystery",
        "year": 2010, "episodes": 13,
        "cast_zh": ["班尼狄·甘巴貝治", "馬田·費曼"], "cast_en": ["Benedict Cumberbatch", "Martin Freeman"],
        "characters_zh": ["福爾摩斯", "華生"], "characters_en": ["Sherlock Holmes", "John Watson"],
        "platform": "BBC",
        "desc_zh": "現代版福爾摩斯",
        "desc_en": "A modern adaptation of Sherlock Holmes",
        "adaptation_zh": "改編自柯南·道爾嘅福爾摩斯系列", "adaptation_en": "Adapted from Arthur Conan Doyle's Sherlock Holmes stories",
    },
    "stranger_things": {
        "zh": "怪奇物語", "en": "Stranger Things",
        "genre_zh": "科幻恐怖", "genre_en": "Sci-fi Horror",
        "year": 2016, "episodes": 34,
        "cast_zh": ["米莉·芭比·布朗", "芬恩·禾夫"], "cast_en": ["Millie Bobby Brown", "Finn Wolfhard", "Winona Ryder"],
        "characters_zh": ["十一", "威爾"], "characters_en": ["Eleven", "Will Byers"],
        "platform": "Netflix",
        "desc_zh": "以80年代為背景，講述小鎮上嘅超自然事件",
        "desc_en": "Set in the 1980s, about supernatural events in a small town",
    },
    "wednesday": {
        "zh": "星期三", "en": "Wednesday",
        "genre_zh": "暗黑喜劇", "genre_en": "Dark Comedy",
        "year": 2022, "episodes": 8,
        "cast_zh": ["真娜·奧特嘉"], "cast_en": ["Jenna Ortega"],
        "characters_zh": ["星期三·阿達"], "characters_en": ["Wednesday Addams"],
        "platform": "Netflix",
        "desc_zh": "《阿達一族》衍生劇",
        "desc_en": "An Addams Family spin-off",
        "adaptation_zh": "改編自查爾斯·阿達斯嘅《阿達一族》", "adaptation_en": "Based on Charles Addams' 'The Addams Family'",
    },
    "westworld": {
        "zh": "西部世界", "en": "Westworld",
        "genre_zh": "科幻", "genre_en": "Sci-fi",
        "year": 2016, "episodes": 36,
        "cast_zh": ["安東尼·鶴健士", "伊雲·活地"], "cast_en": ["Anthony Hopkins", "Evan Rachel Wood", "Ed Harris"],
        "characters_zh": ["德洛麗絲", "伯納德"], "characters_en": ["Dolores", "Bernard"],
        "platform": "HBO",
        "desc_zh": "講述以AI機器人為主題嘅高科技主題公園",
        "desc_en": "About a high-tech theme park populated by AI hosts",
        "adaptation_zh": "改編自1973年同名電影", "adaptation_en": "Adapted from Michael Crichton's 1973 film",
    },
    "witcher": {
        "zh": "獵魔士", "en": "The Witcher",
        "genre_zh": "奇幻", "genre_en": "Fantasy",
        "year": 2019, "episodes": 24,
        "cast_zh": ["亨利·卡維爾", "安雅·夏洛特拉"], "cast_en": ["Henry Cavill", "Anya Chalotra", "Freya Allan"],
        "characters_zh": ["傑洛特", "葉妮芙", "希里"], "characters_en": ["Geralt of Rivia", "Yennefer", "Ciri"],
        "platform": "Netflix",
        "desc_zh": "改編自波蘭小說/遊戲",
        "desc_en": "Adapted from the Polish novels/games",
        "adaptation_zh": "改編自安德烈·薩普科夫斯基小說", "adaptation_en": "Adapted from Andrzej Sapkowski's novels",
    },
}


# ============================================================
# Question generation helpers
# ============================================================

def shuffle_options(correct_zh, correct_en, distractors_zh, distractors_en):
    """Create 4 options with random answer position."""
    indices = random.sample(range(len(distractors_zh)), min(3, len(distractors_zh)))
    d_zh = [distractors_zh[i] for i in indices][:3]
    d_en = [distractors_en[i] for i in indices][:3]
    while len(d_zh) < 3:
        d_zh.append("其他選項")
        d_en.append("Other option")
    pos = random.randint(0, 3)
    opts_zh = d_zh[:pos] + [correct_zh] + d_zh[pos:]
    opts_en = d_en[:pos] + [correct_en] + d_en[pos:]
    return opts_zh, opts_en, pos


def make_q(qid, q_zh, q_en, opts_zh, opts_en, answer, expl_zh, expl_en, difficulty):
    return {
        "id": qid, "question_zh": q_zh, "question_en": q_en,
        "options_zh": opts_zh, "options_en": opts_en,
        "answer": answer, "explanation_zh": expl_zh, "explanation_en": expl_en,
        "difficulty": difficulty,
    }


def generate_questions_for_show(show_key, category, existing_count, target=41):
    """Generate additional questions for a show."""
    info = SHOWS.get(show_key)
    if not info:
        return []

    needed = target - existing_count
    if needed <= 0:
        return []

    questions = []
    sid = 26  # Start after existing IDs (max 25)

    # Build distractor pools
    same_cat = [(v["zh"], v["en"]) for k, v in SHOWS.items()
                if k != show_key and k != "other"]
    random.shuffle(same_cat)
    dist_zh = [s[0] for s in same_cat]
    dist_en = [s[1] for s in same_cat]

    # === Q Type 1: English name ===
    if info["en"] and info["en"] != info["zh"]:
        o_zh, o_en, ans = shuffle_options(info["en"], info["en"],
            [s[1] for s in same_cat], [s[1] for s in same_cat])
        questions.append(make_q(sid + len(questions),
            f"《{info['zh']}》嘅英文名係咩？",
            f"What is the English name of '{info['zh']}'?",
            o_zh, o_en, ans,
            f"《{info['zh']}》嘅英文名係「{info['en']}」。",
            f"The English name of '{info['zh']}' is '{info['en']}'.", 2))

    # === Q Type 2: Genre ===
    if info["genre_zh"] and info["genre_zh"] not in ["綜合"]:
        all_genres = [("仙俠","Xianxia"), ("武俠","Wuxia"), ("宮鬥","Palace Drama"),
                      ("愛情","Romance"), ("懸疑","Mystery"), ("喜劇","Comedy"),
                      ("科幻","Sci-fi"), ("動作","Action"), ("古裝","Historical"),
                      ("時裝","Modern"), ("奇幻","Fantasy"), ("驚悚","Thriller"),
                      ("犯罪","Crime"), ("家庭","Family"), ("校園","School"),
                      ("復仇","Revenge"), ("靈異","Supernatural"), ("律政","Legal"),
                      ("醫療","Medical"), ("處境喜劇","Sitcom"), ("偶像劇","Idol Drama"),
                      ("穿越","Time Travel"), ("黑色喜劇","Dark Comedy"), ("諷刺","Satire"),
                      ("超能力","Superpower"), ("末日","Post-apocalyptic"), ("選集","Anthology"),
                      ("傳記","Biography"), ("職場","Workplace"), ("群像劇","Ensemble")]
        others = [(z, e) for z, e in all_genres if z != info["genre_zh"]]
        random.shuffle(others)
        o_zh, o_en, ans = shuffle_options(info["genre_zh"], info["genre_en"],
            [g[0] for g in others[:10]], [g[1] for g in others[:10]])
        questions.append(make_q(sid + len(questions),
            f"《{info['zh']}》屬於咩類型？",
            f"What genre is '{info['zh']}'?",
            o_zh, o_en, ans,
            f"《{info['zh']}》係{info['genre_zh']}類型。",
            f"'{info['zh']}' is a {info['genre_en']} show.", 1))

    # === Q Type 3: Year ===
    if info["year"]:
        wrong_years = [y for y in range(1985, 2025) if abs(y - info["year"]) > 2]
        random.shuffle(wrong_years)
        o_zh, o_en, ans = shuffle_options(str(info["year"]), str(info["year"]),
            [str(y) for y in wrong_years[:10]], [str(y) for y in wrong_years[:10]])
        questions.append(make_q(sid + len(questions),
            f"《{info['zh']}》係邊年首播？",
            f"What year did '{info['zh']}' first air?",
            o_zh, o_en, ans,
            f"《{info['zh']}》喺{info['year']}年首播。",
            f"'{info['zh']}' first aired in {info['year']}.", 2))

    # === Q Type 4: Platform ===
    if info["platform"]:
        all_plats = ["TVB", "Netflix", "HBO", "tvN", "SBS", "MBC", "KBS2", "NBC", "AMC",
                    "湖南衛視", "浙江衛視", "東方衛視", "央視", "愛奇藝", "騰訊視頻", "優酷",
                    "Disney+", "Amazon Prime", "BBC", "Channel 4", "富士電視台", "TBS",
                    "日本電視台", "朝日電視台", "ENA", "JTBC"]
        other_plats = [p for p in all_plats if p != info["platform"]]
        random.shuffle(other_plats)
        o_zh, o_en, ans = shuffle_options(info["platform"], info["platform"],
            other_plats[:10], other_plats[:10])
        questions.append(make_q(sid + len(questions),
            f"《{info['zh']}》喺邊個平台/頻道播出？",
            f"On which platform did '{info['zh']}' air?",
            o_zh, o_en, ans,
            f"《{info['zh']}》喺{info['platform']}播出。",
            f"'{info['zh']}' aired on {info['platform']}.", 2))

    # === Q Type 5: Cast member ===
    if info["cast_zh"]:
        m_zh = random.choice(info["cast_zh"])
        mi = info["cast_zh"].index(m_zh)
        m_en = info["cast_en"][mi] if mi < len(info["cast_en"]) else m_zh
        all_cast = []
        for k, v in SHOWS.items():
            if k != show_key:
                for i, c in enumerate(v.get("cast_zh", [])):
                    ce = v["cast_en"][i] if i < len(v.get("cast_en", [])) else c
                    all_cast.append((c, ce))
        random.shuffle(all_cast)
        wrong_zh = [c[0] for c in all_cast[:10] if c[0] != m_zh]
        wrong_en = [c[1] for c in all_cast[:10] if c[1] != m_en]
        o_zh, o_en, ans = shuffle_options(m_zh, m_en, wrong_zh, wrong_en)
        questions.append(make_q(sid + len(questions),
            f"以下邊個係《{info['zh']}》嘅主演？",
            f"Which actor/actress starred in '{info['zh']}'?",
            o_zh, o_en, ans,
            f"「{m_zh}」係《{info['zh']}》嘅主演之一。",
            f"'{m_en}' is one of the leads in '{info['zh']}'.", 2))

    # === Q Type 6: Character name ===
    if info["characters_zh"]:
        c_zh = random.choice(info["characters_zh"])
        ci = info["characters_zh"].index(c_zh)
        c_en = info["characters_en"][ci] if ci < len(info["characters_en"]) else c_zh
        all_chars = []
        for k, v in SHOWS.items():
            if k != show_key:
                for i, c in enumerate(v.get("characters_zh", [])):
                    ce = v["characters_en"][i] if i < len(v.get("characters_en", [])) else c
                    all_chars.append((c, ce))
        random.shuffle(all_chars)
        wrong_zh = [c[0] for c in all_chars[:10] if c[0] != c_zh]
        wrong_en = [c[1] for c in all_chars[:10] if c[1] != c_en]
        o_zh, o_en, ans = shuffle_options(c_zh, c_en, wrong_zh, wrong_en)
        questions.append(make_q(sid + len(questions),
            f"「{c_zh}」係《{info['zh']}》入面邊個角色？",
            f"Which character from '{info['zh']}' is '{c_zh}'?",
            o_zh, o_en, ans,
            f"「{c_zh}」係《{info['zh']}》入面嘅角色。",
            f"'{c_en}' is a character from '{info['zh']}'.", 3))

    # === Q Type 7: Episode count ===
    if info["episodes"]:
        wrong_eps = []
        for k, v in SHOWS.items():
            if k != show_key and v.get("episodes"):
                wrong_eps.append(str(v["episodes"]))
        random.shuffle(wrong_eps)
        o_zh, o_en, ans = shuffle_options(str(info["episodes"]), str(info["episodes"]),
            wrong_eps[:10], wrong_eps[:10])
        questions.append(make_q(sid + len(questions),
            f"《{info['zh']}》有幾多集？",
            f"How many episodes does '{info['zh']}' have?",
            o_zh, o_en, ans,
            f"《{info['zh']}》共有{info['episodes']}集。",
            f"'{info['zh']}' has {info['episodes']} episodes.", 3))

    # === Q Type 8: Director ===
    if info.get("director_zh"):
        directors_zh = ["張藝謀","陳凱歌","王家衛","杜琪峯","徐克","李安","孔笙","鄭曉龍","楊潔"]
        directors_en = ["Zhang Yimou","Chen Kaige","Wong Kar-wai","Johnnie To","Tsui Hark","Ang Lee","Kong Sheng","Zheng Xiaolong","Yang Jie"]
        others = [(z, e) for z, e in zip(directors_zh, directors_en) if z != info["director_zh"]]
        random.shuffle(others)
        o_zh, o_en, ans = shuffle_options(info["director_zh"],
            info.get("director_en", info["director_zh"]),
            [d[0] for d in others[:10]], [d[1] for d in others[:10]])
        questions.append(make_q(sid + len(questions),
            f"《{info['zh']}》嘅導演係邊個？",
            f"Who directed '{info['zh']}'?",
            o_zh, o_en, ans,
            f"《{info['zh']}》嘅導演係{info['director_zh']}。",
            f"'{info['zh']}' was directed by {info.get('director_en', info['director_zh'])}.", 3))

    # === Q Type 9: Creator ===
    if info.get("creator_zh"):
        creators_zh = ["史提芬·史匹堡","J·J·艾布斯","活地·阿倫","大衛·芬治","馬田·史高西斯"]
        creators_en = ["Steven Spielberg","J.J. Abrams","Woody Allen","David Fincher","Martin Scorsese"]
        others = [(z, e) for z, e in zip(creators_zh, creators_en) if z != info["creator_zh"]]
        random.shuffle(others)
        o_zh, o_en, ans = shuffle_options(info["creator_zh"],
            info.get("creator_en", info["creator_zh"]),
            [d[0] for d in others[:10]], [d[1] for d in others[:10]])
        questions.append(make_q(sid + len(questions),
            f"《{info['zh']}》嘅創作人係邊個？",
            f"Who created '{info['zh']}'?",
            o_zh, o_en, ans,
            f"《{info['zh']}》嘅創作人係{info['creator_zh']}。",
            f"'{info['zh']}' was created by {info.get('creator_en', info['creator_zh'])}.", 3))

    # === Q Type 10: Adaptation ===
    if info.get("adaptation_zh"):
        o_zh, o_en, ans = shuffle_options(info["adaptation_zh"],
            info.get("adaptation_en", info["adaptation_zh"]),
            ["改編自同名小說","改編自真實事件","原創劇本","改編自漫畫","改編自遊戲"],
            ["Adapted from a novel","Based on true events","Original screenplay","Adapted from manga","Adapted from a game"])
        questions.append(make_q(sid + len(questions),
            f"《{info['zh']}》嘅原作係咩？",
            f"What is '{info['zh']}' adapted from?",
            o_zh, o_en, ans,
            f"《{info['zh']}》{info['adaptation_zh']}。",
            f"'{info['zh']}' is {info.get('adaptation_en', '')}.", 3))

    # === Q Type 11: Description → Show ===
    if info.get("desc_zh") and info["desc_zh"] and len(info["desc_zh"]) > 10:
        o_zh, o_en, ans = shuffle_options(info["zh"], info["en"], dist_zh[:10], dist_en[:10])
        short = info["desc_zh"][:30]
        questions.append(make_q(sid + len(questions),
            f"「{short}⋯⋯」係描述邊套劇？",
            f"'{info.get('desc_en', '')[:40]}...' describes which show?",
            o_zh, o_en, ans,
            f"呢個描述嘅係《{info['zh']}》。",
            f"This describes '{info['zh']}'.", 2))

    # === Q Type 12: Cast pair → Show ===
    if len(info.get("cast_zh", [])) >= 2:
        m1_zh, m2_zh = info["cast_zh"][0], info["cast_zh"][1]
        m1_en = info["cast_en"][0] if info["cast_en"] else m1_zh
        m2_en = info["cast_en"][1] if len(info["cast_en"]) > 1 else m2_zh
        o_zh, o_en, ans = shuffle_options(info["zh"], info["en"], dist_zh[:10], dist_en[:10])
        questions.append(make_q(sid + len(questions),
            f"以下邊套劇同時有「{m1_zh}」同「{m2_zh}」演出？",
            f"Which show features both '{m1_zh}' and '{m2_zh}'?",
            o_zh, o_en, ans,
            f"《{info['zh']}》由{m1_zh}同{m2_zh}主演。",
            f"'{info['en']}' stars both {m1_en} and {m2_en}.", 2))

    # === Q Type 13: Character → Show ===
    if info["characters_zh"]:
        c_zh = random.choice(info["characters_zh"])
        ci = info["characters_zh"].index(c_zh)
        c_en = info["characters_en"][ci] if ci < len(info["characters_en"]) else c_zh
        o_zh, o_en, ans = shuffle_options(info["zh"], info["en"], dist_zh[:10], dist_en[:10])
        questions.append(make_q(sid + len(questions),
            f"「{c_zh}」係邊套劇嘅角色？",
            f"Which show does the character '{c_zh}' appear in?",
            o_zh, o_en, ans,
            f"「{c_zh}」係《{info['zh']}》入面嘅角色。",
            f"'{c_en}' is a character from '{info['zh']}'.", 1))

    # === Q Type 14: Same genre ===
    same_genre = [(k, v) for k, v in SHOWS.items()
                  if v.get("genre_zh") == info.get("genre_zh") and k != show_key and k != "other"]
    if same_genre and info.get("genre_zh"):
        other = random.choice(same_genre)
        o_zh, o_en, ans = shuffle_options(info["zh"], info["en"],
            [other[1]["zh"]] + dist_zh[:9], [other[1]["en"]] + dist_en[:9])
        questions.append(make_q(sid + len(questions),
            f"以下邊套劇同《{other[1]['zh']}》屬於同一類型（{info['genre_zh']}）？",
            f"Which show is in the same genre ({info['genre_en']}) as '{other[1]['zh']}'?",
            o_zh, o_en, ans,
            f"《{info['zh']}》同《{other[1]['zh']}》都係{info['genre_zh']}類型。",
            f"'{info['zh']}' and '{other[1]['en']}' are both {info['genre_en']}.", 2))

    # === Q Type 15: Decade ===
    if info["year"]:
        decade = (info["year"] // 10) * 10
        other_decades = [d for d in range(1980, 2030, 10) if d != decade]
        random.shuffle(other_decades)
        o_zh, o_en, ans = shuffle_options(f"{decade}年代", f"{decade}s",
            [f"{d}年代" for d in other_decades[:10]], [f"{d}s" for d in other_decades[:10]])
        questions.append(make_q(sid + len(questions),
            f"《{info['zh']}》係邊個年代嘅作品？",
            f"Which decade was '{info['zh']}' from?",
            o_zh, o_en, ans,
            f"《{info['zh']}》係{decade}年代嘅作品。",
            f"'{info['zh']}' is from the {decade}s.", 1))

    return questions[:needed]


def improve_existing(questions, show_key):
    """Improve existing questions: better distractors and explanations."""
    info = SHOWS.get(show_key)
    if not info:
        return questions

    same_cat = [(v["zh"], v["en"]) for k, v in SHOWS.items()
                if k != show_key and k != "other"]
    random.shuffle(same_cat)

    for q in questions:
        # Improve explanations for template questions
        if q["explanation_zh"] == f"正確答案係「{info['zh']}」。":
            q["explanation_zh"] = f"《{info['zh']}》嘅正確名稱就係「{info['zh']}」，英文名係「{info['en']}」。"
            q["explanation_en"] = f"The correct name is '{info['zh']}', with the English title '{info['en']}'."

        if q["explanation_zh"].startswith("正確答案係「") and q["explanation_zh"].endswith("」。"):
            ans_text = q["options_zh"][q["answer"]]
            if ans_text == info.get("genre_zh"):
                q["explanation_zh"] = f"《{info['zh']}》係{info['genre_zh']}類型劇集。"
                q["explanation_en"] = f"'{info['zh']}' is a {info['genre_en']} show."

        # Replace generic distractors with real show names for Q1-Q3
        if q["id"] <= 3 and len(same_cat) >= 3:
            correct = q["options_zh"][q["answer"]]
            new_zh, new_en = [], []
            used = set()
            di = 0
            for i in range(4):
                if i == q["answer"]:
                    new_zh.append(correct)
                    new_en.append(q["options_en"][i])
                else:
                    while di < len(same_cat):
                        dz, de = same_cat[di]
                        di += 1
                        if dz not in used and dz != correct:
                            new_zh.append(dz)
                            new_en.append(de)
                            used.add(dz)
                            break
                    else:
                        new_zh.append(q["options_zh"][i])
                        new_en.append(q["options_en"][i])
            q["options_zh"] = new_zh
            q["options_en"] = new_en

    return questions


def process_category(cat_dir):
    """Process all files in a category."""
    total_new = 0
    total_files = 0
    total_questions = 0

    for fname in sorted(os.listdir(cat_dir)):
        if not fname.endswith(".json") or fname == "index.json":
            continue

        fpath = os.path.join(cat_dir, fname)
        show_key = fname.replace(".json", "")

        with open(fpath, "r", encoding="utf-8") as f:\n            questions = json.load(f)\n\n        existing = len(questions)\n        questions = improve_existing(questions, show_key)\n        new_qs = generate_questions_for_show(show_key, cat_dir, existing, target=41)
        questions.extend(new_qs)

        # Re-assign IDs sequentially
        for i, q in enumerate(questions):
            q["id"] = i + 1

        with open(fpath, "w", encoding="utf-8") as f:\n            json.dump(questions, f, ensure_ascii=False, indent=2)\n\n        total_new += len(new_qs)\n        total_files += 1\n        total_questions += len(questions)
        print(f"  {fname}: {existing} -> {len(questions)} (+{len(new_qs)})")

    return total_files, total_new, total_questions


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    categories = ["cn_drama", "hk_drama", "hk_modern", "japanese_drama",
                  "korean_drama", "variety_show", "western_tv"]

    grand_new = 0
    grand_total = 0

    for cat in categories:
        cat_dir = os.path.join(base_dir, cat)
        if not os.path.isdir(cat_dir):
            print(f"Skipping {cat}: not found")
            continue

        print(f"\n{'='*60}\nProcessing: {cat}\n{'='*60}")
        fc, nc, tc = process_category(cat_dir)
        grand_new += nc
        grand_total += tc
        print(f"\n  Category: {tc} questions ({nc} new)")

    print(f"\n{'='*60}")
    print(f"GRAND TOTAL: {grand_total} questions ({grand_new} new)")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
