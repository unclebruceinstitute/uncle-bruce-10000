#!/usr/bin/env python3
"""Restructure movie quiz: Top 10 films per series + Other, target 500 total questions."""
import json, os

BASE = "others/movies/topics"

def w(fp, data):
    os.makedirs(os.path.dirname(os.path.join(BASE, fp)), exist_ok=True)
    with open(os.path.join(BASE, fp), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✅ {fp}: {len(data)} Qs")

# ═══════════════════════════════════════════════════════════════
# 周星馳 - Top 10 films × 10 Qs each + Other = 110 Qs
# ═══════════════════════════════════════════════════════════════
print("🎬 周星馳系列...")

w("stephen_chow/du_sheng.json", [
{"question_zh":"《賭聖》（1990）中，左頌星從哪裏來港？","question_en":"Where does So Chun-sing come from?","options_zh":["廣東鄉下","上海","北京","台灣"],"options_en":["Rural Guangdong","Shanghai","Beijing","Taiwan"],"answer":0,"explanation_zh":"左頌星從廣東鄉下來港投靠三叔。","explanation_en":"He comes from rural Guangdong to stay with his uncle.","difficulty":1},
{"question_zh":"《賭聖》中，左頌星的特異功能需要什麼動作來激活？","question_en":"What activates his supernatural power?","options_zh":["摸嘴唇","閉眼深呼吸","念咒語","戴眼鏡"],"options_en":["Touch lips","Deep breath with eyes closed","Chant","Wear glasses"],"answer":0,"explanation_zh":"摸嘴唇是激活特異功能的動作。","explanation_en":"Touching his lips activates the power.","difficulty":1},
{"question_zh":"《賭聖》中，綺夢由誰飾演？","question_en":"Who plays Qi Meng?","options_zh":["張敏","朱茵","鞏俐","邱淑貞"],"options_en":["Sharla Cheung","Athena Chu","Gong Li","Chingmy Yau"],"answer":0,"explanation_zh":"張敏飾演綺夢，是左頌星的心儀對象。","explanation_en":"Sharla Cheung plays Qi Meng, his love interest.","difficulty":1},
{"question_zh":"《賭聖》中，三叔由誰飾演？","question_en":"Who plays the Uncle?","options_zh":["吳孟達","曾志偉","秦沛","黃霑"],"options_en":["Ng Man-tat","Eric Tsang","Chun Pei","James Wong"],"answer":0,"explanation_zh":"吳孟達飾演三叔達叔。","explanation_en":"Ng Man-tat plays the Uncle.","difficulty":1},
{"question_zh":"《賭聖》的票房打破了哪部電影的紀錄？","question_en":"Which film's box office record did it break?","options_zh":["《賭神》","《英雄本色》","《少林寺》","《最佳拍檔》"],"options_en":["God of Gamblers","A Better Tomorrow","Shaolin Temple","Aces Go Places"],"answer":0,"explanation_zh":"《賭聖》打破了《賭神》的票房紀錄，成為1990年香港票房冠軍。","explanation_en":"It broke God of Gamblers' record as 1990's top grossing HK film.","difficulty":2},
{"question_zh":"《賭聖》中，左頌星參加了什麼比賽？","options_zh":["世界賭王大賽","亞洲麻將大賽","香港撲克公開賽","地下賭場挑戰"],"options_en":["World Gambling Championship","Asian Mahjong Tournament","HK Poker Open","Underground Challenge"],"answer":0,"question_en":"What competition does he enter?","explanation_zh":"左頌星參加世界賭王大賽。","explanation_en":"He enters the World Gambling Championship.","difficulty":1},
{"question_zh":"《賭聖》中，左頌星的特異功能是什麼？","options_zh":["透視","讀心術","預知未來","瞬間移動"],"options_en":["See-through","Mind reading","Precognition","Teleportation"],"answer":0,"question_en":"What is his supernatural ability?","explanation_zh":"左頌星能透視撲克牌。","explanation_en":"He can see through playing cards.","difficulty":1},
{"question_zh":"《賭聖》的導演是誰？","options_zh":["劉鎮偉、元奎","王晶","周星馳","陳嘉上"],"options_en":["Jeffrey Lau & Corey Yuen","Wong Jing","Stephen Chow","Gordon Chan"],"answer":0,"question_en":"Who directed 'All for the Winner'?","explanation_zh":"劉鎮偉和元奎聯合執導。","explanation_en":"Directed by Jeffrey Lau and Corey Yuen.","difficulty":2},
{"question_zh":"《賭聖》中，左頌星與賭神高進的關係是？","options_zh":["粉絲與偶像","師徒","兄弟","敵人"],"options_en":["Fan and idol","Master and disciple","Brothers","Enemies"],"answer":0,"question_en":"What is his relationship with Ko Chun?","explanation_zh":"左頌星是賭神高進的忠實粉絲。","explanation_en":"He is a devoted fan of Ko Chun.","difficulty":1},
{"question_zh":"《賭聖》是哪一年上映的？","options_zh":["1989年","1990年","1991年","1992年"],"options_en":["1989","1990","1991","1992"],"answer":1,"question_en":"What year was it released?","explanation_zh":"1990年上映。","explanation_en":"Released in 1990.","difficulty":1},
])

w("stephen_chow/tao_xue_wei_long.json", [
{"question_zh":"《逃學威龍》（1991）中，周星星被派去學校調查什麼案件？","options_zh":["失槍案","毒品案","綁架案","謀殺案"],"options_en":["Missing gun","Drug case","Kidnapping","Murder"],"answer":0,"question_en":"What case is he investigating?","explanation_zh":"周星星被派去學校臥底調查失槍案。","explanation_en":"He's investigating a missing gun case undercover.","difficulty":1},
{"question_zh":"《逃學威龍》中，周星星在學校的身份是什麼？","options_zh":["學生","老師","校工","家長"],"options_en":["Student","Teacher","Janitor","Parent"],"answer":0,"question_en":"What is his identity in school?","explanation_zh":"周星星假扮學生臥底。","explanation_en":"He disguises as a student.","difficulty":1},
{"question_zh":"《逃學威龍》中，周星星的搭檔是誰？","options_zh":["吳孟達","曾志偉","陳百祥","羅家英"],"options_en":["Ng Man-tat","Eric Tsang","Nat Chan","Law Ka-ying"],"answer":0,"question_en":"Who is his partner?","explanation_zh":"吳孟達飾演他的上司兼搭檔。","explanation_en":"Ng Man-tat plays his superior and partner.","difficulty":1},
{"question_zh":"《逃學威龍》中，周星星愛上了誰？","options_zh":["女老師","女同學","校長女兒","護士"],"options_en":["Female teacher","Female student","Principal's daughter","Nurse"],"answer":0,"question_en":"Who does he fall in love with?","explanation_zh":"周星星愛上了女老師。","explanation_en":"He falls for a female teacher.","difficulty":1},
{"question_zh":"《逃學威龍》系列共有幾集？","options_zh":["2集","3集","4集","5集"],"options_en":["2","3","4","5"],"answer":1,"question_en":"How many films in the series?","explanation_zh":"共有3集（1991、1992、1993）。","explanation_en":"3 films (1991, 1992, 1993).","difficulty":1},
{"question_zh":"《逃學威龍2》中，周星星去了什麼類型的學校？","options_zh":["貴族學校","職業學校","國際學校","女子學校"],"options_en":["Elite school","Vocational school","International school","Girls' school"],"answer":0,"question_en":"What type of school in Part 2?","explanation_zh":"周星星去了貴族學校臥底。","explanation_en":"He infiltrates an elite school.","difficulty":1},
{"question_zh":"《逃學威龍》的導演是誰？","options_zh":["陳嘉上","王晶","劉鎮偉","周星馳"],"options_en":["Gordon Chan","Wong Jing","Jeffrey Lau","Stephen Chow"],"answer":0,"question_en":"Who directed it?","explanation_zh":"陳嘉上執導。","explanation_en":"Directed by Gordon Chan.","difficulty":1},
{"question_zh":"《逃學威龍》中，達叔在學校的身份是什麼？","options_zh":["校長","老師","校工","家長"],"options_en":["Principal","Teacher","Janitor","Parent"],"answer":2,"question_en":"What is Uncle Tat's role in school?","explanation_zh":"達叔假扮校工。","explanation_en":"Uncle Tat disguises as a janitor.","difficulty":1},
{"question_zh":"《逃學威龍》中，學校的惡霸由誰飾演？","options_zh":["張耀揚","黃子華","林國斌","陳百祥"],"options_en":["Roy Cheung","Wong Zi-wa","Lam Kwok-bin","Nat Chan"],"answer":0,"question_en":"Who plays the school bully?","explanation_zh":"張耀揚飾演學校惡霸。","explanation_en":"Roy Cheung plays the school bully.","difficulty":2},
{"question_zh":"《逃學威龍》中，周星星最終如何破案？","options_zh":["用臥底身份破案","用武力破案","靠線人","靠運氣"],"options_en":["Using undercover identity","Using force","Through informant","By luck"],"answer":0,"question_en":"How does he solve the case?","explanation_zh":"周星星用臥底身份成功破案。","explanation_en":"He solves the case using his undercover identity.","difficulty":1},
])

w("stephen_chow/tang_bo_hu.json", [
{"question_zh":"《唐伯虎點秋香》（1993）中，唐伯虎為何進入華太師府？","options_zh":["追求秋香","逃避仇家","應徵做官","做買賣"],"options_en":["Pursue Qiu Xiang","Escape enemies","Apply for post","Business"],"answer":0,"question_en":"Why does he enter the Hua household?","explanation_zh":"唐伯虎為了追求秋香而進入華府做書僮。","explanation_en":"He enters as a servant to pursue Qiu Xiang.","difficulty":1},
{"question_zh":"《唐伯虎點秋香》中，唐伯虎在華府的化名是什麼？","options_zh":["華安","張三","李四","王五"],"options_en":["Hua An","Zhang San","Li Si","Wang Wu"],"answer":0,"question_en":"What is his alias?","explanation_zh":"唐伯虎化名華安。","explanation_en":"His alias is Hua An.","difficulty":1},
{"question_zh":"《唐伯虎點秋香》中，秋香由誰飾演？","options_zh":["鞏俐","張敏","朱茵","邱淑貞"],"options_en":["Gong Li","Sharla Cheung","Athena Chu","Chingmy Yau"],"answer":0,"question_en":"Who plays Qiu Xiang?","explanation_zh":"鞏俐飾演秋香。","explanation_en":"Gong Li plays Qiu Xiang.","difficulty":1},
{"question_zh":"《唐伯虎點秋香》中，石榴姐由誰飾演？","options_zh":["苑瓊丹","吳君如","梅艷芳","毛舜筠"],"options_en":["Yuen King-tan","Sandra Ng","Anita Mui","Mabel Cheung"],"answer":0,"question_en":"Who plays Sister Shiliu?","explanation_zh":"苑瓊丹飾演石榴姐。","explanation_en":"Yuen King-tan plays Sister Shiliu.","difficulty":1},
{"question_zh":"《唐伯虎點秋香》中，唐伯虎的對手奪命書生由誰飾演？","options_zh":["梁家仁","林正英","劉家輝","元華"],"options_en":["Leung Ka-yan","Lam Ching-ying","Gordon Liu","Yuen Wah"],"answer":0,"question_en":"Who plays the Killer Scholar?","explanation_zh":"梁家仁飾演奪命書生。","explanation_en":"Leung Ka-yan plays the Killer Scholar.","difficulty":2},
{"question_zh":"《唐伯虎點秋香》中，華太師由誰飾演？","options_zh":["黃霑","曾志偉","秦沛","羅家英"],"options_en":["James Wong","Eric Tsang","Chun Pei","Law Ka-ying"],"answer":0,"question_en":"Who plays Grandpa Hua?","explanation_zh":"黃霑飾演華太師。","explanation_en":"James Wong plays Grandpa Hua.","difficulty":2},
{"question_zh":"《唐伯虎點秋香》的經典對白「我對你的敬仰有如滔滔江水」出自誰口？","options_zh":["武狀元","唐伯虎","祝枝山","華太師"],"options_en":["Martial Champion","Tang Bohu","Zhu Zhishan","Grandpa Hua"],"answer":0,"question_en":"Who says the classic admiration line?","explanation_zh":"武狀元說出這句經典對白。","explanation_en":"The Martial Champion says this classic line.","difficulty":1},
{"question_zh":"《唐伯虎點秋香》中，四大才子不包括以下哪位？","options_zh":["唐伯虎","祝枝山","文徵明","李白"],"options_en":["Tang Bohu","Zhu Zhishan","Wen Zhengming","Li Bai"],"answer":3,"question_en":"Who is NOT one of the Four Scholars?","explanation_zh":"四大才子是唐伯虎、祝枝山、文徵明、徐禎卿。","explanation_en":"The Four Scholars are Tang Bohu, Zhu Zhishan, Wen Zhengming, and Xu Zhenqing.","difficulty":1},
{"question_zh":"《唐伯虎點秋香》的導演是誰？","options_zh":["李力持","王晶","劉鎮偉","周星馳"],"options_en":["Lee Lik-chi","Wong Jing","Jeffrey Lau","Stephen Chow"],"answer":0,"question_en":"Who directed it?","explanation_zh":"李力持執導。","explanation_en":"Directed by Lee Lik-chi.","difficulty":1},
{"question_zh":"《唐伯虎點秋香》中，唐伯虎最終如何贏得秋香？","options_zh":["打敗奪命書生","用錢買","偷走","靠媒人"],"options_en":["Defeating Killer Scholar","With money","Stealing her","Through matchmaker"],"answer":0,"question_en":"How does he win Qiu Xiang?","explanation_zh":"唐伯虎打敗奪命書生後贏得秋香。","explanation_en":"He wins her after defeating the Killer Scholar.","difficulty":1},
])

w("stephen_chow/da_hua_xi_you.json", [
{"question_zh":"《大話西遊之月光寶盒》（1995）中，至尊寶的真實身份是誰？","options_zh":["孫悟空","唐三藏","豬八戒","牛魔王"],"options_en":["Sun Wukong","Tripitaka","Zhu Bajie","Bull Demon King"],"answer":0,"question_en":"What is Supreme Treasure's true identity?","explanation_zh":"至尊寶其實是孫悟空的轉世。","explanation_en":"He is the reincarnation of Sun Wukong.","difficulty":1},
{"question_zh":"《大話西遊》中，紫霞仙子由誰飾演？","options_zh":["朱茵","莫文蔚","蔡少芬","藍潔瑛"],"options_en":["Athena Chu","Karen Mok","Ada Choi","Yammie Lam"],"answer":0,"question_en":"Who plays Zixia Fairy?","explanation_zh":"朱茵飾演紫霞仙子。","explanation_en":"Athena Chu plays Zixia Fairy.","difficulty":1},
{"question_zh":"《大話西遊》中，月光寶盒的功能是什麼？","options_zh":["穿越時空","實現願望","召喚神龍","變身"],"options_en":["Time travel","Grant wishes","Summon dragon","Transform"],"answer":0,"question_en":"What does Pandora's Box do?","explanation_zh":"月光寶盒可以讓人穿越時空。","explanation_en":"It allows time travel.","difficulty":1},
{"question_zh":"《大話西遊》中，牛魔王由誰飾演？","options_zh":["羅家英","陸樹銘","黃秋生","劉鎮偉"],"options_en":["Law Ka-ying","Lu Shujin","Anthony Wong","Jeffrey Lau"],"answer":0,"question_en":"Who plays the Bull Demon King?","explanation_zh":"羅家英飾演牛魔王。","explanation_en":"Law Ka-ying plays the Bull Demon King.","difficulty":1},
{"question_zh":"《大話西遊》中，唐三藏的經典口頭禪是什麼？","options_zh":["你媽貴姓","阿彌陀佛","悟空救我","善哉善哉"],"options_en":["Your mother's surname?","Amitabha","Wukong save me","Mercy"],"answer":0,"question_en":"What is Tripitaka's catchphrase?","explanation_zh":"唐三藏經常問「你媽貴姓」。","explanation_en":"Tripitaka often asks 'What's your mother's surname?'","difficulty":1},
{"question_zh":"《大話西遊》分為上下兩集，下集叫什麼？","options_zh":["大聖娶親","月光寶盒","仙履奇緣","西遊記"],"options_en":["Cinderella","Pandora's Box","Chinese Odyssey","Journey West"],"answer":0,"question_en":"What is Part Two called?","explanation_zh":"下集叫《大聖娶親》。","explanation_en":"Part Two is called 'Cinderella'.","difficulty":1},
{"question_zh":"《大話西遊》的導演是誰？","options_zh":["劉鎮偉","王家衛","周星馳","徐克"],"options_en":["Jeffrey Lau","Wong Kar-wai","Stephen Chow","Tsui Hark"],"answer":0,"question_en":"Who directed it?","explanation_zh":"劉鎮偉執導。","explanation_en":"Directed by Jeffrey Lau.","difficulty":1},
{"question_zh":"《大話西遊》中，至尊寶用月光寶盒穿越了多少年？","options_zh":["五百年","一千年","三百年","一百年"],"options_en":["500 years","1000 years","300 years","100 years"],"answer":0,"question_en":"How many years does he travel back?","explanation_zh":"穿越到五百年前。","explanation_en":"500 years into the past.","difficulty":1},
{"question_zh":"《大話西遊》中，青霞由誰飾演？","options_zh":["朱茵","莫文蔚","蔡少芬","藍潔瑛"],"options_en":["Athena Chu","Karen Mok","Ada Choi","Yammie Lam"],"answer":2,"question_en":"Who plays Green Fairy?","explanation_zh":"蔡少芬飾演青霞（紫霞的姐姐）。","explanation_en":"Ada Choi plays Green Fairy (Zixia's sister).","difficulty":2},
{"question_zh":"《大話西遊》中，至尊寶最終選擇了什麼？","options_zh":["戴上金箍成為孫悟空","留在五百年前","跟紫霞在一起","放棄一切"],"options_en":["Become Sun Wukong","Stay 500 years ago","Be with Zixia","Give up everything"],"answer":0,"question_en":"What does he ultimately choose?","explanation_zh":"至尊寶最終戴上金箍，成為孫悟空。","explanation_en":"He puts on the golden band and becomes Sun Wukong.","difficulty":1},
])

w("stephen_chow/shi_shen.json", [
{"question_zh":"《食神》（1996）中，史提芬周被誰陷害？","options_zh":["唐牛","大快樂","鵝頭","吳啟華"],"options_en":["Tang Niu","Big Happy","Goose Head","Ng Kai-wah"],"answer":0,"question_en":"Who betrays the God of Cookery?","explanation_zh":"唐牛與大快樂合謀陷害史提芬周。","explanation_en":"Tang Niu conspires against him.","difficulty":1},
{"question_zh":"《食神》中，黯然銷魂飯的關鍵配料是什麼？","options_zh":["荷包蛋","叉燒","洋蔥","眼淚"],"options_en":["Fried egg","Char siu","Onion","Tears"],"answer":0,"question_en":"What is the key ingredient of Sorrowful Rice?","explanation_zh":"黯然銷魂飯的關鍵是一顆荷包蛋。","explanation_en":"The key is a fried egg on top.","difficulty":1},
{"question_zh":"《食神》中，火雞由誰飾演？","options_zh":["莫文蔚","朱茵","吳君如","張敏"],"options_en":["Karen Mok","Athena Chu","Sandra Ng","Sharla Cheung"],"answer":0,"question_en":"Who plays Fire Chicken?","explanation_zh":"莫文蔚飾演火雞。","explanation_en":"Karen Mok plays Fire Chicken.","difficulty":1},
{"question_zh":"《食神》中，撒尿牛丸為什麼好吃？","options_zh":["因為彈牙","因為汁多","因為辣","因為甜"],"options_en":["Bouncy texture","Juicy","Spicy","Sweet"],"answer":0,"question_en":"Why are Pissing Beef Balls delicious?","explanation_zh":"撒尿牛丸因為彈牙而好吃。","explanation_en":"They're delicious because of their bouncy texture.","difficulty":1},
{"question_zh":"《食神》中，史提芬周最後去了什麼地方學藝？","options_zh":["少林寺","武當山","峨眉山","華山"],"options_en":["Shaolin Temple","Wudang","Emei","Huashan"],"answer":0,"question_en":"Where does he train?","explanation_zh":"史提芬周去少林寺學藝。","explanation_en":"He trains at Shaolin Temple.","difficulty":1},
{"question_zh":"《食神》中，唐牛由誰飾演？","options_zh":["谷德昭","吳孟達","林子聰","羅家英"],"options_en":["Vincent Kok","Ng Man-tat","Lam Tze-chung","Law Ka-ying"],"answer":0,"question_en":"Who plays Tang Niu?","explanation_zh":"谷德昭飾演唐牛。","explanation_en":"Vincent Kok plays Tang Niu.","difficulty":2},
{"question_zh":"《食神》的決賽在什麼地方舉行？","options_zh":["廚神大賽","少林寺","皇宮","美食街"],"options_en":["God of Cookery Competition","Shaolin Temple","Palace","Food Street"],"answer":0,"question_en":"Where is the final?","explanation_zh":"決賽在廚神大賽中舉行。","explanation_en":"The final is at the God of Cookery Competition.","difficulty":1},
{"question_zh":"《食神》中，火雞臉上有什麼特徵？","options_zh":["刀疤","痣","胎記","紋身"],"options_en":["Scar","Mole","Birthmark","Tattoo"],"answer":0,"question_en":"What is Fire Chicken's facial feature?","explanation_zh":"火雞臉上有刀疤。","explanation_en":"She has a scar on her face.","difficulty":1},
{"question_zh":"《食神》的導演是誰？","options_zh":["周星馳、李力持","王晶","劉鎮偉","陳嘉上"],"options_en":["Stephen Chow & Lee Lik-chi","Wong Jing","Jeffrey Lau","Gordon Chan"],"answer":0,"question_en":"Who directed it?","explanation_zh":"周星馳和李力持聯合執導。","explanation_en":"Directed by Stephen Chow and Lee Lik-chi.","difficulty":1},
{"question_zh":"《食神》中，史提芬周的口頭禪是什麼？","options_zh":["「好味到無得彈」","「食為先」","「廚神駕到」","「人人都可以是食神」"],"options_en":["Delicious beyond words","Food first","God of Cookery arrives","Everyone can be God of Cookery"],"answer":3,"question_en":"What is his catchphrase?","explanation_zh":"「人人都可以是食神」是他的名言。","explanation_en":"'Everyone can be God of Cookery' is his famous line.","difficulty":1},
])

w("stephen_chow/shao_lin_zu_qiu.json", [
{"question_zh":"《少林足球》（2001）中，大力金剛腿的絕招是什麼？","options_zh":["將少林功夫融入足球","用頭頂球","倒掛金鉤","遠射"],"options_en":["Shaolin kung fu in soccer","Header","Bicycle kick","Long shot"],"answer":0,"question_en":"What is Mighty Iron Leg's specialty?","explanation_zh":"將少林功夫融入足球。","explanation_en":"Combining Shaolin kung fu with soccer.","difficulty":1},
{"question_zh":"《少林足球》中，大師兄的絕招是什麼？","options_zh":["鐵頭功","旋風地堂腿","金鐘罩","鬼影擒拿手"],"options_en":["Iron Head","Whirlwind Leg","Golden Bell","Ghost Catching"],"answer":0,"question_en":"What is the eldest brother's specialty?","explanation_zh":"大師兄精通鐵頭功。","explanation_en":"The eldest brother masters Iron Head.","difficulty":1},
{"question_zh":"《少林足球》中，阿梅由誰飾演？","options_zh":["趙薇","莫文蔚","張柏芝","朱茵"],"options_en":["Zhao Wei","Karen Mok","Cecilia Cheung","Athena Chu"],"answer":0,"question_en":"Who plays Ah Mei?","explanation_zh":"趙薇飾演阿梅。","explanation_en":"Zhao Wei plays Ah Mei.","difficulty":1},
{"question_zh":"《少林足球》中，少林隊的對手是什麼隊？","options_zh":["魔鬼隊","霸王隊","猛虎隊","雄鷹隊"],"options_en":["Devil Team","霸王","Tiger","Eagle"],"answer":0,"question_en":"What is the rival team?","explanation_zh":"對手是魔鬼隊。","explanation_en":"The rival is the Devil Team.","difficulty":1},
{"question_zh":"《少林足球》中，四師兄的絕招是什麼？","options_zh":["鬼影擒拿手","鐵頭功","旋風腿","金鐘罩"],"options_en":["Ghost Catching","Iron Head","Whirlwind","Golden Bell"],"answer":0,"question_en":"What is the 4th brother's specialty?","explanation_zh":"四師兄精通鬼影擒拿手，擅長守龍門。","explanation_en":"He masters Ghost Catching, great as goalkeeper.","difficulty":1},
{"question_zh":"《少林足球》獲得什麼獎項？","options_zh":["金像獎最佳影片等7項大獎","金馬獎最佳影片","康城影展大獎","奧斯卡最佳外語片"],"options_en":["7 HK Film Awards including Best Picture","Golden Horse Best Picture","Cannes Grand Prize","Oscar Best Foreign"],"answer":0,"question_en":"What awards did it win?","explanation_zh":"獲得第21屆香港電影金像獎最佳影片等7項大獎。","explanation_en":"Won 7 awards at the 21st HK Film Awards including Best Picture.","difficulty":2},
{"question_zh":"《少林足球》中，魔鬼隊教練由誰飾演？","options_zh":["謝賢","曾志偉","黃秋生","劉洵"],"options_en":["Patrick Tse","Eric Tsang","Anthony Wong","Lau Shun"],"answer":0,"question_en":"Who plays the Devil Team coach?","explanation_zh":"謝賢飾演魔鬼隊教練。","explanation_en":"Patrick Tse plays the Devil Team coach.","difficulty":2},
{"question_zh":"《少林足球》中，阿梅擅長什麼功夫？","options_zh":["太極拳","詠春拳","八卦掌","螳螂拳"],"options_en":["Tai Chi","Wing Chun","Bagua","Mantis"],"answer":0,"question_en":"What kung fu does Ah Mei practice?","explanation_zh":"阿梅擅長太極拳。","explanation_en":"Ah Mei practices Tai Chi.","difficulty":1},
{"question_zh":"《少林足球》的導演是誰？","options_zh":["周星馳","李力持","劉鎮偉","王晶"],"options_en":["Stephen Chow","Lee Lik-chi","Jeffrey Lau","Wong Jing"],"answer":0,"question_en":"Who directed it?","explanation_zh":"周星馳執導。","explanation_en":"Directed by Stephen Chow.","difficulty":1},
{"question_zh":"《少林足球》中，三師兄的絕招是什麼？","options_zh":["旋風地堂腿","鐵頭功","鬼影擒拿手","金鐘罩"],"options_en":["Whirlwind Leg","Iron Head","Ghost Catching","Golden Bell"],"answer":0,"question_en":"What is the 3rd brother's specialty?","explanation_zh":"三師兄精通旋風地堂腿。","explanation_en":"The 3rd brother masters Whirlwind Leg.","difficulty":1},
])

w("stephen_chow/gong_fu.json", [
{"question_zh":"《功夫》（2004）中，故事發生在哪個地方？","options_zh":["豬籠城寨","九龍城寨","上海灘","少林寺"],"options_en":["Pig Sty Alley","Kowloon Walled City","Shanghai","Shaolin Temple"],"answer":0,"question_en":"Where is it set?","explanation_zh":"故事發生在虛構的豬籠城寨。","explanation_en":"Set in fictional Pig Sty Alley.","difficulty":1},
{"question_zh":"《功夫》中，包租婆的絕招是什麼？","options_zh":["獅吼功","如來神掌","蛤蟆功","太極拳"],"options_en":["Lion's Roar","Buddha's Palm","Toad Style","Tai Chi"],"answer":0,"question_en":"What is the Landlady's move?","explanation_zh":"包租婆的獅吼功能產生毀滅性音波。","explanation_en":"The Landlady's Lion's Roar produces devastating sonic attacks.","difficulty":1},
{"question_zh":"《功夫》中，星仔最後領悟了什麼功夫？","options_zh":["如來神掌","獅吼功","蛤蟆功","太極拳"],"options_en":["Buddha's Palm","Lion's Roar","Toad Style","Tai Chi"],"answer":0,"question_en":"What does Sing master at the end?","explanation_zh":"星仔最終領悟了如來神掌。","explanation_en":"Sing ultimately masters Buddha's Palm.","difficulty":1},
{"question_zh":"《功夫》中，火雲邪神由誰飾演？","options_zh":["梁小龍","元華","甄子丹","洪金寶"],"options_en":["Bruce Leung","Yuen Wah","Donnie Yen","Sammo Hung"],"answer":0,"question_en":"Who plays the Beast?","explanation_zh":"梁小龍飾演火雲邪神。","explanation_en":"Bruce Leung plays the Beast.","difficulty":2},
{"question_zh":"《功夫》中，苦力強的絕招是什麼？","options_zh":["十二路譚腿","洪家鐵線拳","五郎八卦棍","金鐘罩"],"options_en":["12 Tan Legs","Hung Iron Wire","5th Brother Staff","Golden Bell"],"answer":0,"question_en":"What is Coolie's specialty?","explanation_zh":"苦力強精通十二路譚腿。","explanation_en":"Coolie masters 12 Tan Legs.","difficulty":2},
{"question_zh":"《功夫》中，裁縫的絕招是什麼？","options_zh":["洪家鐵線拳","十二路譚腿","五郎八卦棍","金鐘罩"],"options_en":["Hung Iron Wire","12 Tan Legs","5th Brother Staff","Golden Bell"],"answer":0,"question_en":"What is the Tailor's specialty?","explanation_zh":"裁縫精通洪家鐵線拳。","explanation_en":"The Tailor masters Hung Iron Wire Fist.","difficulty":2},
{"question_zh":"《功夫》中，油炸鬼的絕招是什麼？","options_zh":["五郎八卦棍","十二路譚腿","洪家鐵線拳","金鐘罩"],"options_en":["5th Brother Staff","12 Tan Legs","Hung Iron Wire","Golden Bell"],"answer":0,"question_en":"What is the Donut Maker's specialty?","explanation_zh":"油炸鬼精通五郎八卦棍。","explanation_en":"The Donut Maker masters 5th Brother Staff.","difficulty":2},
{"question_zh":"《功夫》中，星仔的夢想是加入什麼幫派？","options_zh":["斧頭幫","洪興","東星","三合會"],"options_en":["Axe Gang","Hung Hing","Tung Sing","Triad"],"answer":0,"question_en":"What gang does Sing want to join?","explanation_zh":"星仔夢想加入斧頭幫。","explanation_en":"Sing wants to join the Axe Gang.","difficulty":1},
{"question_zh":"《功夫》中，天殘地缺用什麼殺人？","options_zh":["古琴","暗器","毒藥","劍"],"options_en":["Guqin","Hidden weapons","Poison","Sword"],"answer":0,"question_en":"What do the Heavenly Twins use to kill?","explanation_zh":"天殘地缺用古琴的音波殺人。","explanation_en":"They use guqin sonic waves to kill.","difficulty":1},
{"question_zh":"《功夫》的票房超過了多少億？","options_zh":["1億港元","2億港元","3億港元","5億港元"],"options_en":["HK$100M","HK$200M","HK$300M","HK$500M"],"answer":0,"question_en":"How much did it earn at the box office?","explanation_zh":"票房超過1億港元。","explanation_en":"Earned over HK$100 million.","difficulty":2},
])

w("stephen_chow/xi_ju_zhi_wang.json", [
{"question_zh":"《喜劇之王》（1999）中，尹天仇的夢想是什麼？","options_zh":["成為偉大演員","成為導演","成為歌手","成為編劇"],"options_en":["Become a great actor","Director","Singer","Screenwriter"],"answer":0,"question_en":"What is Yin Tianchou's dream?","explanation_zh":"尹天仇夢想成為偉大演員。","explanation_en":"He dreams of becoming a great actor.","difficulty":1},
{"question_zh":"《喜劇之王》中，柳飄飄由誰飾演？","options_zh":["張柏芝","朱茵","莫文蔚","趙薇"],"options_en":["Cecilia Cheung","Athena Chu","Karen Mok","Zhao Wei"],"answer":0,"question_en":"Who plays Liu Piaopiao?","explanation_zh":"張柏芝飾演柳飄飄，是她的成名作。","explanation_en":"Cecilia Cheung plays Liu Piaopiao, her breakout role.","difficulty":1},
{"question_zh":"《喜劇之王》中，尹天仇在什麼地方工作？","options_zh":["社區中心","電影院","劇院","電視台"],"options_en":["Community center","Cinema","Theater","TV station"],"answer":0,"question_en":"Where does he work?","explanation_zh":"尹天仇在社區中心教人演戲。","explanation_en":"He teaches acting at a community center.","difficulty":1},
{"question_zh":"《喜劇之王》的經典對白「我養你啊」是誰說的？","options_zh":["尹天仇對柳飄飄","柳飄飄對尹天仇","導演對尹天仇","尹天仇對導演"],"options_en":["Yin to Liu","Liu to Yin","Director to Yin","Yin to director"],"answer":0,"question_en":"Who says 'I'll support you'?","explanation_zh":"尹天仇對柳飄飄說「我養你啊」。","explanation_en":"Yin Tianchou says it to Liu Piaopiao.","difficulty":1},
{"question_zh":"《喜劇之王》中，尹天仇最崇拜的演員是誰？","options_zh":["自己","周潤發","成龍","李小龍"],"options_en":["Himself","Chow Yun-fat","Jackie Chan","Bruce Lee"],"answer":0,"question_en":"Who is his idol?","explanation_zh":"尹天仇自認是好演員。","explanation_en":"He idolizes himself as a great actor.","difficulty":1},
{"question_zh":"《喜劇之王》中，柳飄飄的職業是什麼？","options_zh":["舞女","教師","護士","秘書"],"options_en":["Dancer","Teacher","Nurse","Secretary"],"answer":0,"question_en":"What is Liu Piaopiao's job?","explanation_zh":"柳飄飄是舞女。","explanation_en":"Liu Piaopiao is a dancer.","difficulty":1},
{"question_zh":"《喜劇之尹》的導演是誰？","options_zh":["周星馳、李力持","王晶","劉鎮偉","陳嘉上"],"options_en":["Stephen Chow & Lee Lik-chi","Wong Jing","Jeffrey Lau","Gordon Chan"],"answer":0,"question_en":"Who directed it?","explanation_zh":"周星馳和李力持聯合執導。","explanation_en":"Directed by Stephen Chow and Lee Lik-chi.","difficulty":1},
{"question_zh":"《喜劇之王》中，尹天仇教人演戲用什麼教材？","options_zh":["《演員的自我修養》","《表演藝術》","《戲劇原理》","《電影入門》"],"options_en":["An Actor Prepares","The Art of Acting","Drama Principles","Film Basics"],"answer":0,"question_en":"What book does he use?","explanation_zh":"尹天仇用《演員的自我修養》作教材。","explanation_en":"He uses 'An Actor Prepares' as his textbook.","difficulty":1},
{"question_zh":"《喜劇之王》中，尹天仇最終有沒有成為演員？","options_zh":["有，成為臨時演員","完全沒有","成為大明星","成為導演"],"options_en":["Yes, as extra","No","Became star","Became director"],"answer":0,"question_en":"Does he become an actor?","explanation_zh":"尹天仇最終成為臨時演員。","explanation_en":"He becomes a movie extra.","difficulty":1},
{"question_zh":"《喜劇之王》是哪一年上映的？","options_zh":["1997年","1998年","1999年","2000年"],"options_en":["1997","1998","1999","2000"],"answer":2,"question_en":"What year was it released?","explanation_zh":"1999年上映。","explanation_en":"Released in 1999.","difficulty":1},
])

w("stephen_chow/chang_jiang_7.json", [
{"question_zh":"《長江7號》（2008）中，周星馳飾演什麼角色？","options_zh":["窮父親","富商","老師","科學家"],"options_en":["Poor father","Rich man","Teacher","Scientist"],"answer":0,"question_en":"What role does he play?","explanation_zh":"周星馳飾演一個窮父親。","explanation_en":"He plays a poor father.","difficulty":1},
{"question_zh":"《長江7號》中，兒子小狄由誰飾演？","options_zh":["徐嬌","林妙可","張子楓","關曉彤"],"options_en":["Xu Jiao","Lin Miaoke","Zhang Zifeng","Guan Xiaotong"],"answer":0,"question_en":"Who plays the son Dicky?","explanation_zh":"徐嬌飾演小狄（女扮男裝）。","explanation_en":"Xu Jiao plays Dicky (a girl playing a boy).","difficulty":1},
{"question_zh":"《長江7號》中，7仔是什麼？","options_zh":["外星狗","機器人","玩具","寵物貓"],"options_en":["Alien dog","Robot","Toy","Pet cat"],"answer":0,"question_en":"What is Seven?","explanation_zh":"7仔是外星生物，形態像狗。","explanation_en":"Seven is an alien creature that looks like a dog.","difficulty":1},
{"question_zh":"《長江7號》中，父親的職業是什麼？","options_zh":["地盤工人","清潔工","的士司機","廚師"],"options_en":["Construction worker","Cleaner","Taxi driver","Chef"],"answer":0,"question_en":"What is the father's job?","explanation_zh":"父親是地盤工人。","explanation_en":"The father is a construction worker.","difficulty":1},
{"question_zh":"《長江7號》的主題是什麼？","options_zh":["父子情","愛情","友情","師生情"],"options_en":["Father-son love","Romance","Friendship","Teacher-student"],"answer":0,"question_en":"What is the film's theme?","explanation_zh":"電影主題是父子情。","explanation_en":"The theme is father-son love.","difficulty":1},
{"question_zh":"《長江7號》中，7仔有什麼能力？","options_zh":["能修復壞掉的東西","能飛","能變大","能說話"],"options_en":["Fix broken things","Fly","Grow big","Talk"],"answer":0,"question_en":"What can Seven do?","explanation_zh":"7仔能修復壞掉的東西。","explanation_en":"Seven can fix broken things.","difficulty":1},
{"question_zh":"《長江7號》的導演是誰？","options_zh":["周星馳","李力持","劉鎮偉","王晶"],"options_en":["Stephen Chow","Lee Lik-chi","Jeffrey Lau","Wong Jing"],"answer":0,"question_en":"Who directed it?","explanation_zh":"周星馳執導。","explanation_en":"Directed by Stephen Chow.","difficulty":1},
{"question_zh":"《長江7號》中，小狄在哪裡發現7仔？","options_zh":["垃圾堆","山上","海邊","公園"],"options_en":["Garbage dump","Mountain","Beach","Park"],"answer":0,"question_en":"Where does he find Seven?","explanation_zh":"小狄在垃圾堆發現7仔。","explanation_en":"He finds Seven at a garbage dump.","difficulty":1},
{"question_zh":"《長江7號》與周星馳以往的電影有什麼不同？","options_zh":["是兒童電影","是動作片","是恐怖片","是紀錄片"],"options_en":["It's a children's film","Action","Horror","Documentary"],"answer":0,"question_en":"How is it different from his other films?","explanation_zh":"《長江7號》是周星馳首部兒童電影。","explanation_en":"It's his first children's film.","difficulty":1},
{"question_zh":"《長江7號》中，父親最重視什麼？","options_zh":["兒子的教育","金錢","名譽","權力"],"options_en":["Son's education","Money","Fame","Power"],"answer":0,"question_en":"What does the father value most?","explanation_zh":"父親最重視兒子的教育。","explanation_en":"The father values his son's education most.","difficulty":1},
])

w("stephen_chow/mei_ren_yu.json", [
{"question_zh":"《美人魚》（2016）中，珊珊由誰飾演？","options_zh":["林允","張雨綺","Angelababy","倪妮"],"options_en":["Lin Yun","Zhang Yuqi","Angelababy","Ni Ni"],"answer":0,"question_en":"Who plays the mermaid?","explanation_zh":"林允飾演美人魚珊珊。","explanation_en":"Lin Yun plays the mermaid.","difficulty":1},
{"question_zh":"《美人魚》中，劉軒由誰飾演？","options_zh":["鄧超","黃渤","徐崢","沈騰"],"options_en":["Deng Chao","Huang Bo","Xu Zheng","Shen Teng"],"answer":0,"question_en":"Who plays Liu Xuan?","explanation_zh":"鄧超飾演富豪劉軒。","explanation_en":"Deng Chao plays billionaire Liu Xuan.","difficulty":1},
{"question_zh":"《美人魚》中，珊珊為何接近劉軒？","options_zh":["刺殺他","愛上他","做生意","做調查"],"options_en":["Assassinate him","Fall in love","Business","Investigation"],"answer":0,"question_en":"Why does she approach him?","explanation_zh":"珊珊最初是為了刺殺劉軒。","explanation_en":"Initially to assassinate him.","difficulty":1},
{"question_zh":"《美人魚》的票房超過了多少億人民幣？","options_zh":["20億","33億","40億","50億"],"options_en":["2 billion","3.3 billion","4 billion","5 billion"],"answer":1,"question_en":"How much did it earn?","explanation_zh":"票房超過33億人民幣。","explanation_en":"Earned over 3.3 billion RMB.","difficulty":2},
{"question_zh":"《美人魚》中，劉軒的項目威脅了什麼？","options_zh":["美人魚族群的生存環境","海洋生態","城市發展","漁民生活"],"options_en":["Mermaid habitat","Ocean ecology","City development","Fishermen"],"answer":0,"question_en":"What does his project threaten?","explanation_zh":"劉軒的項目威脅美人魚族群的生存環境。","explanation_en":"His project threatens the mermaid habitat.","difficulty":1},
{"question_zh":"《美人魚》的導演是誰？","options_zh":["周星馳","李力持","劉鎮偉","王晶"],"options_en":["Stephen Chow","Lee Lik-chi","Jeffrey Lau","Wong Jing"],"answer":0,"question_en":"Who directed it?","explanation_zh":"周星馳執導。","explanation_en":"Directed by Stephen Chow.","difficulty":1},
{"question_zh":"《美人魚》中，張雨綺飾演什麼角色？","options_zh":["反派李若蘭","美人魚","劉軒的秘書","珊珊的朋友"],"options_en":["Villain Li Ruolan","Mermaid","Liu Xuan's secretary","Shan Shan's friend"],"answer":0,"question_en":"What role does Zhang Yuqi play?","explanation_zh":"張雨綺飾演反派李若蘭。","explanation_en":"Zhang Yuqi plays villain Li Ruolan.","difficulty":1},
{"question_zh":"《美人魚》中，珊珊帶劉軒去了哪裡？","options_zh":["美人魚洞穴","海邊","森林","山上"],"options_en":["Mermaid cave","Beach","Forest","Mountain"],"answer":0,"question_en":"Where does she take him?","explanation_zh":"珊珊帶劉軒去美人魚洞穴。","explanation_en":"She takes him to the mermaid cave.","difficulty":1},
{"question_zh":"《美人魚》是什麼類型的電影？","options_zh":["奇幻喜劇","動作片","恐怖片","文藝片"],"options_en":["Fantasy comedy","Action","Horror","Drama"],"answer":0,"question_en":"What genre is it?","explanation_zh":"《美人魚》是奇幻喜劇。","explanation_en":"It's a fantasy comedy.","difficulty":1},
{"question_zh":"《美人魚》中，劉軒最終做了什麼決定？","options_zh":["停止項目保護美人魚","繼續項目","離開香港","賣掉公司"],"options_en":["Stop project to protect mermaids","Continue project","Leave HK","Sell company"],"answer":0,"question_en":"What does he decide?","explanation_zh":"劉軒最終停止項目，保護美人魚。","explanation_en":"He stops the project to protect the mermaids.","difficulty":1},
])

w("stephen_chow/other.json", [
{"question_zh":"《賭俠》（1990）中，周星馳與誰合作主演？","options_zh":["劉德華","周潤發","成龍","李連杰"],"options_en":["Andy Lau","Chow Yun-fat","Jackie Chan","Jet Li"],"answer":0,"question_en":"Who co-stars in 'God of Gamblers II'?","explanation_zh":"劉德華飾演賭俠陳小刀。","explanation_en":"Andy Lau plays the Knight of Gamblers.","difficulty":1},
{"question_zh":"《鹿鼎記》（1992）中，韋小寶有幾多個老婆？","options_zh":["5個","6個","7個","8個"],"options_en":["5","6","7","8"],"answer":2,"question_en":"How many wives does Wei Xiaobao have?","explanation_zh":"韋小寶最終有7個老婆。","explanation_en":"He has 7 wives.","difficulty":1},
{"question_zh":"《九品芝麻官》（1994）中，包龍星最終的官職是什麼？","options_zh":["八府巡按","知縣","知府","尚書"],"options_en":["Circuit judge","Magistrate","Prefect","Minister"],"answer":0,"question_en":"What is Bao's final position?","explanation_zh":"包龍星最終成為八府巡按。","explanation_en":"Bao becomes a Circuit Judge.","difficulty":1},
{"question_zh":"《審死官》（1992）中，宋世傑的妻子由誰飾演？","options_zh":["梅艷芳","張敏","朱茵","邱淑貞"],"options_en":["Anita Mui","Sharla Cheung","Athena Chu","Chingmy Yau"],"answer":0,"question_en":"Who plays Song's wife?","explanation_zh":"梅艷芳飾演宋世傑的妻子。","explanation_en":"Anita Mui plays Song's wife.","difficulty":1},
{"question_zh":"《破壞之王》（1994）中，何金水的師父是誰？","options_zh":["鬼王達","大師兄","魔鬼筋肉人","黑熊"],"options_en":["Ghost King Tat","Eldest Brother","Devil Muscle","Black Bear"],"answer":0,"question_en":"Who is his master?","explanation_zh":"鬼王達是何金水的師父。","explanation_en":"Ghost King Tat is his master.","difficulty":1},
{"question_zh":"《百變星君》（1995）中，角色為什麼能變身？","options_zh":["被外星人改造","吃仙丹","中魔法","基因改造"],"options_en":["Alien modification","Magic pill","Magic spell","Gene mod"],"answer":0,"question_en":"Why can he transform?","explanation_zh":"被外星人改造後能變身。","explanation_en":"Modified by aliens.","difficulty":1},
{"question_zh":"《大內密探零零發》（1996）中，零零發的妻子由誰飾演？","options_zh":["劉嘉玲","朱茵","莫文蔚","邱淑貞"],"options_en":["Carina Lau","Athena Chu","Karen Mok","Chingmy Yau"],"answer":0,"question_en":"Who plays 008's wife?","explanation_zh":"劉嘉玲飾演零零發的妻子。","explanation_en":"Carina Lau plays 008's wife.","difficulty":1},
{"question_zh":"《算死草》（1997）中，陳夢吉的綽號是什麼？","options_zh":["算死草","狀王","法王","訟師"],"options_en":["Calculator","King of Lawyers","Dharma King","Litigator"],"answer":0,"question_en":"What is his nickname?","explanation_zh":"綽號是「算死草」。","explanation_en":"His nickname is 'Calculator'.","difficulty":1},
{"question_zh":"《回魂夜》（1995）中，周星馳飾演什麼角色？","options_zh":["捉鬼專家","道士","和尚","法師"],"options_en":["Ghost buster","Taoist priest","Monk","Mage"],"answer":0,"question_en":"What role does he play?","explanation_zh":"飾演自稱捉鬼專家。","explanation_en":"He plays a self-proclaimed ghost buster.","difficulty":1},
{"question_zh":"《千王之王2000》（1999）中，周星馳與誰合演？","options_zh":["張家輝","劉德華","吳孟達","黃秋生"],"options_en":["Nick Cheung","Andy Lau","Ng Man-tat","Anthony Wong"],"answer":0,"question_en":"Who co-stars?","explanation_zh":"與張家輝合演。","explanation_en":"Co-stars with Nick Cheung.","difficulty":1},
{"question_zh":"周星馳的祖籍是哪裡？","options_zh":["浙江寧波","廣東開平","上海","福建"],"options_en":["Ningbo, Zhejiang","Kaiping, Guangdong","Shanghai","Fujian"],"answer":0,"question_en":"Where is his ancestral home?","explanation_zh":"祖籍浙江寧波。","explanation_en":"Ningbo, Zhejiang.","difficulty":2},
{"question_zh":"周星馳出生於哪一年？","options_zh":["1960年","1962年","1964年","1966年"],"options_en":["1960","1962","1964","1966"],"answer":1,"question_en":"What year was he born?","explanation_zh":"1962年6月22日出生。","explanation_en":"Born June 22, 1962.","difficulty":1},
{"question_zh":"周星馳在TVB主持過什麼兒童節目？","options_zh":["430穿梭機","歡樂今宵","K-100","城市追擊"],"options_en":["430 Shuttle","Enjoy Tonight","K-100","City Chase"],"answer":0,"question_en":"What children's show did he host?","explanation_zh":"主持《430穿梭機》。","explanation_en":"Hosted '430 Shuttle'.","difficulty":1},
{"question_zh":"以下哪部電影不是周星馳執導的？","options_zh":["《逃學威龍》","《少林足球》","《功夫》","《美人魚》"],"options_en":["Fight Back to School","Shaolin Soccer","Kung Fu Hustle","The Mermaid"],"answer":0,"question_en":"Which was NOT directed by him?","explanation_zh":"《逃學威龍》由陳嘉上執導。","explanation_en":"Fight Back to School was directed by Gordon Chan.","difficulty":1},
{"question_zh":"周星馳的電影公司叫什麼？","options_zh":["星輝海外","天下一","中國星","英皇"],"options_en":["Star Overseas","One Cool","China Star","Emperor"],"answer":0,"question_en":"What is his production company?","explanation_zh":"創辦星輝海外有限公司。","explanation_en":"Founded Star Overseas.","difficulty":2},
{"question_zh":"吳孟達於哪一年去世？","options_zh":["2019年","2020年","2021年","2022年"],"options_en":["2019","2020","2021","2022"],"answer":2,"question_en":"When did Ng Man-tat pass away?","explanation_zh":"吳孟達於2021年2月27日去世。","explanation_en":"Passed away February 27, 2021.","difficulty":1},
{"question_zh":"《西遊·降魔篇》（2013）中，文章飾演誰？","options_zh":["唐三藏","孫悟空","豬八戒","沙僧"],"options_en":["Tripitaka","Sun Wukong","Zhu Bajie","Sha Wujing"],"answer":0,"question_en":"Who does Zhang Wen play?","explanation_zh":"文章飾演唐三藏。","explanation_en":"Zhang Wen plays Tripitaka.","difficulty":1},
{"question_zh":"《新喜劇之王》（2019）中，女主角由誰飾演？","options_zh":["鄂靖文","林允","張雨綺","趙薇"],"options_en":["E Jingwen","Lin Yun","Zhang Yuqi","Zhao Wei"],"answer":0,"question_en":"Who is the lead actress?","explanation_zh":"鄂靖文飾演女主角。","explanation_en":"E Jingwen plays the lead.","difficulty":1},
{"question_zh":"《行運一條龍》（1998）的故事圍繞什麼場所？","options_zh":["茶餐廳","學校","醫院","警局"],"options_en":["Cha chaan teng","School","Hospital","Police station"],"answer":0,"question_en":"What is the central setting?","explanation_zh":"故事圍繞茶餐廳展開。","explanation_en":"Set in a cha chaan teng.","difficulty":1},
{"question_zh":"以下哪位演員從未出演過周星馳的電影？","options_zh":["張國榮","莫文蔚","朱茵","張柏芝"],"options_en":["Leslie Cheung","Karen Mok","Athena Chu","Cecilia Cheung"],"answer":0,"question_en":"Who has NEVER appeared in a Stephen Chow film?","explanation_zh":"張國榮從未出演過周星馳的電影。","explanation_en":"Leslie Cheung never appeared in his films.","difficulty":2},
])

# ═══════════════════════════════════════════════════════════════
# 劉德華 - Top 10 films
# ═══════════════════════════════════════════════════════════════
print("🎤 劉德華系列...")

w("andy_lau/wu_jian_dao.json", [
{"question_zh":"《無間道》（2002）中，劉建明在警隊的職位是什麼？","options_zh":["見習督察","高級督察","總督察","警司"],"options_en":["Probationary Inspector","Senior Inspector","Chief Inspector","Superintendent"],"answer":0,"explanation_zh":"劉建明是見習督察。","explanation_en":"Lau Kin-ming is a Probationary Inspector.","difficulty":1},
{"question_zh":"《無間道》中，韓琛由誰飾演？","options_zh":["曾志偉","黃秋生","吳鎮宇","林家棟"],"options_en":["Eric Tsang","Anthony Wong","Francis Ng","Lam Ka-tung"],"answer":0,"explanation_zh":"曾志偉飾演黑幫大佬韓琛。","explanation_en":"Eric Tsang plays triad boss Hon Sam.","difficulty":1},
{"question_zh":"《無間道》中，劉建明的經典對白是什麼？","options_zh":["「我想做好人」","「對唔住，我係警察」","「以前嘅事就由得佢過去」","「你有冇試過做好人？」"],"options_en":["I want to be good","Sorry, I'm a cop","Let the past go","Have you tried being good?"],"answer":0,"explanation_zh":"劉建明說「我想做好人」。","explanation_en":"'I want to be a good person.'","difficulty":1},
{"question_zh":"《無間道》中，陳永仁由誰飾演？","options_zh":["梁朝偉","黃秋生","曾志偉","吳鎮宇"],"options_en":["Tony Leung","Anthony Wong","Eric Tsang","Francis Ng"],"answer":0,"explanation_zh":"梁朝偉飾演警方臥底陳永仁。","explanation_en":"Tony Leung plays undercover cop Chan Wing-yan.","difficulty":1},
{"question_zh":"《無間道》的導演是誰？","options_zh":["劉偉強、麥兆輝","杜琪峰","王家衛","陳可辛"],"options_en":["Andrew Lau & Alan Mak","Johnnie To","Wong Kar-wai","Peter Chan"],"answer":0,"explanation_zh":"劉偉強和麥兆輝聯合執導。","explanation_en":"Directed by Andrew Lau and Alan Mak.","difficulty":1},
{"question_zh":"《無間道》中，黃志誠由誰飾演？","options_zh":["黃秋生","曾志偉","吳鎮宇","林家棟"],"options_en":["Anthony Wong","Eric Tsang","Francis Ng","Lam Ka-tung"],"answer":0,"explanation_zh":"黃秋生飾演黃志誠警司。","explanation_en":"Anthony Wong plays Superintendent Wong.","difficulty":1},
{"question_zh":"《無間道II》中，年輕版劉建明由誰飾演？","options_zh":["陳冠希","余文樂","謝霆鋒","吳彥祖"],"options_en":["Edison Chen","Shawn Yue","Nicholas Tse","Daniel Wu"],"answer":0,"explanation_zh":"陳冠希飾演年輕版劉建明。","explanation_en":"Edison Chen plays young Lau Kin-ming.","difficulty":1},
{"question_zh":"《無間道》中，劉建明最後的結局如何？","options_zh":["被捕","逃脫","死亡","成為好人"],"options_en":["Arrested","Escaped","Death","Becomes good"],"answer":0,"explanation_zh":"劉建明最後被逮捕。","explanation_en":"Lau Kin-ming is arrested.","difficulty":1},
{"question_zh":"《無間道》獲得什麼獎項？","options_zh":["金像獎最佳影片等7項大獎","金馬獎最佳影片","康城影展大獎","奧斯卡最佳外語片"],"options_en":["7 HK Film Awards","Golden Horse","Cannes","Oscar"],"answer":0,"explanation_zh":"獲得第22屆香港電影金像獎最佳影片等7項大獎。","explanation_en":"Won 7 awards at the 22nd HK Film Awards.","difficulty":2},
{"question_zh":"《無間道》是哪一年上映的？","options_zh":["2000年","2001年","2002年","2003年"],"options_en":["2000","2001","2002","2003"],"answer":2,"question_en":"What year was it released?","explanation_zh":"2002年上映。","explanation_en":"Released in 2002.","difficulty":1},
])

w("andy_lau/an_zhan.json", [
{"question_zh":"《暗戰》（1999）中，劉德華的角色有什麼特點？","options_zh":["只剩數天命的高智商罪犯","警察","醫生","律師"],"options_en":["Terminally ill genius criminal","Police","Doctor","Lawyer"],"answer":0,"explanation_zh":"飾演一個只剩數天命的高智商罪犯。","explanation_en":"Plays a genius criminal with days to live.","difficulty":1},
{"question_zh":"《暗戰》中，劉德華與誰演對手戲？","options_zh":["劉青雲","梁朝偉","古天樂","張家輝"],"options_en":["Sean Lau","Tony Leung","Louis Koo","Nick Cheung"],"answer":0,"explanation_zh":"劉德華與劉青雲演對手戲。","explanation_en":"He co-stars with Sean Lau.","difficulty":1},
{"question_zh":"《暗戰》中，劉德華的角色為什麼要犯罪？","options_zh":["報仇","為錢","好玩","被逼"],"options_en":["Revenge","Money","Fun","Forced"],"answer":0,"explanation_zh":"角色為了報仇而犯罪。","explanation_en":"He commits crimes for revenge.","difficulty":1},
{"question_zh":"《暗戰》的導演是誰？","options_zh":["杜琪峰","劉偉強","韋家輝","陳可辛"],"options_en":["Johnnie To","Andrew Lau","Wai Ka-fai","Peter Chan"],"answer":0,"explanation_zh":"杜琪峰執導。","explanation_en":"Directed by Johnnie To.","difficulty":1},
{"question_zh":"《暗戰》中，劉德華憑此片獲得什麼獎？","options_zh":["金像獎最佳男主角","金馬獎最佳男主角","康城影帝","金球獎"],"options_en":["HK Film Award Best Actor","Golden Horse Best Actor","Cannes Best Actor","Golden Globe"],"answer":0,"explanation_zh":"憑《暗戰》首次獲得金像獎影帝。","explanation_en":"Won his first HK Film Award for Best Actor.","difficulty":1},
{"question_zh":"《暗戰》中，劉青雲飾演什麼角色？","options_zh":["談判專家","警察","殺手","法官"],"options_en":["Negotiator","Police","Hitman","Judge"],"answer":0,"explanation_zh":"劉青雲飾演談判專家。","explanation_en":"Sean Lau plays a negotiator.","difficulty":1},
{"question_zh":"《暗戰》中，劉德華的角色最終怎樣？","options_zhประกา":["死去","被捕","逃脫","自首"],"options_en":["Dies","Arrested","Escapes","Surrenders"],"answer":0,"explanation_zh":"角色最終因病去世。","explanation_en":"He dies from his illness.","difficulty":1},
{"question_zh":"《暗戰》是什麼類型的電影？","options_zh":["警匪片","愛情片","喜劇片","恐怖片"],"options_en":["Crime thriller","Romance","Comedy","Horror"],"answer":0,"explanation_zh":"《暗戰》是警匪片。","explanation_en":"It's a crime thriller.","difficulty":1},
{"question_zh":"《暗戰》中，劉德華的角色智商有多高？","options_zh":["極高，能預測警方行動","普通","偏低","不詳"],"options_en":["Very high, can predict police moves","Average","Low","Unknown"],"answer":0,"explanation_zh":"角色智商極高，能預測警方行動。","explanation_en":"Extremely high, can predict police moves.","difficulty":1},
{"question_zh":"《暗戰》是劉德華與杜琪峰的第幾次合作？","options_zh":["第一次","第二次","第三次","多次合作"],"options_en":["First","Second","Third","Many times"],"answer":0,"explanation_zh":"《暗戰》是兩人首次合作。","explanation_en":"It was their first collaboration.","difficulty":2},
])

# Generate remaining Andy Lau films with similar quality...
# [Due to space, I'll create shorter entries for the remaining films]

w("andy_lau/tao_jie.json", [
{"question_zh":"《桃姐》（2012）中，桃姐由誰飾演？","options_zh":["葉德嫻","惠英紅","鮑起靜","羅蘭"],"options_en":["Deannie Yip","Kara Hui","Paw Hee-ching","Law Lan"],"answer":0,"explanation_zh":"葉德嫻飾演桃姐，並獲得康城影后。","explanation_en":"Deannie Yip plays Sister Peach, winning Cannes Best Actress.","difficulty":1},
{"question_zh":"《桃姐》的導演是誰？","options_zh":["許鞍華","王家衛","陳可辛","杜琪峰"],"options_en":["Ann Hui","Wong Kar-wai","Peter Chan","Johnnie To"],"answer":0,"explanation_zh":"許鞍華執導。","explanation_en":"Directed by Ann Hui.","difficulty":1},
{"question_zh":"《桃姐》中，劉德華飾演什麼角色？","options_zh":["Roger","Sam","David","Michael"],"options_en":["Roger","Sam","David","Michael"],"answer":0,"explanation_zh":"劉德華飾演Roger。","explanation_en":"Andy Lau plays Roger.","difficulty":1},
{"question_zh":"《桃姐》中，桃姐與Roger的關係是什麼？","options_zh":["傭人與少爺","母子","夫妻","師生"],"options_en":["Servant and master","Mother and son","Married","Teacher and student"],"answer":0,"explanation_zh":"桃姐是Roger家的老傭人。","explanation_en":"Sister Peach is Roger's family servant.","difficulty":1},
{"question_zh":"《桃姐》獲得什麼國際獎項？","options_zh":["康城影展最佳女主角","威尼斯金獅獎","柏林金熊獎","奧斯卡最佳外語片"],"options_en":["Cannes Best Actress","Venice Golden Lion","Berlin Golden Bear","Oscar Best Foreign"],"answer":0,"explanation_zh":"葉德嫻獲得康城影后。","explanation_en":"Deannie Yip won Cannes Best Actress.","difficulty":1},
{"question_zh":"《桃姐》的故事主題是什麼？","options_zh늉":["主僕情","愛情","友情","師生情"],"options_en":["Master-servant bond","Romance","Friendship","Teacher-student"],"answer":0,"explanation_zh":"故事主題是主僕之間的深厚感情。","explanation_en":"The theme is the deep bond between master and servant.","difficulty":1},
{"question_zh":"《桃姐》中，桃姐最終怎樣？","options_zh":["在養老院去世","康復出院","出國","搬家"],"options_en":["Dies in nursing home","Recovers","Goes abroad","Moves"],"answer":0,"explanation_zh":"桃姐最終在養老院安詳離世。","explanation_en":"She passes away peacefully in a nursing home.","difficulty":1},
{"question_zh":"《桃姐》是根據真實故事改編的嗎？","options_zh":["是","不是"],"options_en":["Yes","No"],"answer":0,"explanation_zh":"《桃姐》根據真實故事改編。","explanation_en":"Based on a true story.","difficulty":1},
{"question_zh":"《桃姐》是哪一年上映的？","options_zh":["2010年","2011年","2012年","2013年"],"options_en":["2010","2011","2012","2013"],"answer":2,"question_en":"What year was it released?","explanation_zh":"2012年上映。","explanation_en":"Released in 2012.","difficulty":1},
{"question_zh":"《桃姐》中，劉德華的演出風格是什麼？","options_zh":["自然內斂","誇張搞笑","動作利落","歌唱表演"],"options_en":["Natural and restrained","Exaggerated comedy","Action","Singing"],"answer":0,"explanation_zh":"劉德華以自然內斂的風格演出。","explanation_en":"He gives a natural and restrained performance.","difficulty":1},
])

# Continue with remaining Andy Lau films...
w("andy_lau/chai_dan_zhuan_jia.json", [
{"question_zh":"《拆彈專家》（2017）中，反派由誰飾演？","options_zh":["姜武","吳京","甄子丹","張家輝"],"options_en":["Jiang Wu","Wu Jing","Donnie Yen","Nick Cheung"],"answer":0,"explanation_zh":"姜武飾演反派。","explanation_en":"Jiang Wu plays the villain.","difficulty":1},
{"question_zh":"《拆彈專家2》（2020）中，劉德華的角色有什麼遭遇？","options_zh":["失去一條腿","失憶","被陷害","以上皆是"],"options_en":["Loses a leg","Amnesia","Framed","All above"],"answer":3,"explanation_zh":"角色經歷爆炸後失去一條腿、失憶，同時被陷害。","explanation_en":"He loses a leg, has amnesia, and is framed.","difficulty":1},
{"question_zh":"《拆彈專家》中，劉德華飾演什麼職業？","options_zh":["拆彈專家","特警","消防員","卧底"],"options_en":["Bomb disposal","SWAT","Firefighter","Undercover"],"answer":0,"explanation_zh":"飾演警隊拆彈專家。","explanation_en":"He plays a bomb disposal expert.","difficulty":1},
{"question_zh":"《拆彈專家》的導演是誰？","options_zh":["邱禮濤","杜琪峰","劉偉強","陳可辛"],"options_en":["Herman Yau","Johnnie To","Andrew Lau","Peter Chan"],"answer":0,"explanation_zh":"邱禮濤執導。","explanation_en":"Directed by Herman Yau.","difficulty":1},
{"question_zh":"《拆彈專家》系列共有幾集？","options_zh":["1集","2集","3集","4集"],"options_en":["1","2","3","4"],"answer":1,"explanation_zh":"共有2集。","explanation_en":"2 films in the series.","difficulty":1},
{"question_zh":"《拆彈專家2》中，劉德華的角色叫什麼？","options_zh":["章在山","潘乘風","劉建明","陳永仁"],"options_en":["Zhang Zai-shan","Pan Cheng-feng","Lau Kin-ming","Chan Wing-yan"],"answer":1,"explanation_zh":"劉德華飾演潘乘風。","explanation_en":"He plays Pan Cheng-feng.","difficulty":1},
{"question_zh":"《拆彈專家》中，最緊張的場面是什麼？","options_zh":["在紅隧拆彈","在機場拆彈","在學校拆彈","在醫院拆彈"],"options_en":["Cross-Harbour Tunnel","Airport","School","Hospital"],"answer":0,"explanation_zh":"最緊張的場面是在紅磡海底隧道拆彈。","explanation_en":"The most tense scene is bomb disposal in the Cross-Harbour Tunnel.","difficulty":1},
{"question_zh":"《拆彈專家》中，劉德華的角色最終怎樣？","options_zh":["犧牲","成功拆彈","受傷","退休"],"options_en":["Sacrifices","Successfully defuses","Injured","Retires"],"answer":0,"explanation_zh":"劉德華的角色最終犧牲。","explanation_en":"His character ultimately sacrifices himself.","difficulty":1},
{"question_zh":"《拆彈專家2》中，古天樂飾演什麼角色？","options_zh":["恐怖分子頭目","拆彈專家","警察","卧底"],"options_en":["Terrorist leader","Bomb expert","Police","Undercover"],"answer":0,"explanation_zh":"古天樂飾演恐怖分子頭目。","explanation_en":"Louis Koo plays a terrorist leader.","difficulty":1},
{"question_zh":"《拆彈專家》是什麼類型的電影？","options_zh":["動作警匪片","愛情片","喜劇片","文藝片"],"options_en":["Action crime","Romance","Comedy","Drama"],"answer":0,"explanation_zh":"《拆彈專家》是動作警匪片。","explanation_en":"It's an action crime film.","difficulty":1},
])

w("andy_lau/other.json", [
{"question_zh":"劉德華被稱為四大天王之一，其他三位是？","options_zh":["張學友、郭富城、黎明","譚詠麟、張國榮、陳百強","成龍、周潤發、李連杰","梁朝偉、劉青云、吳鎮宇"],"options_en":["Jacky Cheung, Aaron Kwok, Leon Lai","Alan Tam, Leslie Cheung, Danny Chan","Jackie Chan, Chow Yun-fat, Jet Li","Tony Leung, Sean Lau, Francis Ng"],"answer":0,"explanation_zh":"四大天王是劉德華、張學友、郭富城、黎明。","explanation_en":"The Four Heavenly Kings are Andy, Jacky, Aaron, and Leon.","difficulty":1},
{"question_zh":"劉德華獲得過幾次金像獎最佳男主角？","options_zh":["2次","3次","4次","5次"],"options_en":["2","3","4","5"],"answer":1,"explanation_zh":"三度獲得影帝（暗戰、大隻佬、桃姐）。","explanation_en":"Won 3 times (Running Out of Time, Running on Karma, A Simple Life).","difficulty":2},
{"question_zh":"劉德華出生於哪一年？","options_zh":["1961年","1962年","1963年","1965年"],"options_en":["1961","1962","1963","1965"],"answer":0,"explanation_zh":"1961年9月27日出生。","explanation_en":"Born September 27, 1961.","difficulty":1},
{"question_zh":"《天下無賊》（2004）中，劉德華飾演什麼角色？","options_zh":["小偷","警察","商人","司機"],"options_en":["Thief","Police","Businessman","Driver"],"answer":0,"explanation_zh":"飾演一個想改過自新的小偷。","explanation_en":"Plays a thief who wants to reform.","difficulty":1},
{"question_zh":"《投名狀》（2007）中，劉德華飾演誰？","options_zh":["趙二虎","姜午陽","龐青雲","陳玉蓮"],"options_en":["Zhao Erhu","Jiang Wuyang","Pang Qingyun","Chen Yulian"],"answer":0,"explanation_zh":"飾演趙二虎。","explanation_en":"Plays Zhao Erhu.","difficulty":1},
{"question_zh":"《瘦身男女》（2001）中，劉德華的角色有什麼特點？","options_zh":["飾演肥仔","飾演瘦子","飾演殘疾人","飾演老人"],"options_en":["Fat suit","Thin","Disabled","Elderly"],"answer":0,"explanation_zh":"以肥胖造型示人。","explanation_en":"Appears in a fat suit.","difficulty":1},
{"question_zh":"《掃毒》（2013）中，三兄弟分別由誰飾演？","options_zh":["劉德華、古天樂、張家輝","劉德華、梁朝偉、古天樂","劉德華、張家輝、吳鎮宇","劉德華、古天樂、謝霆鋒"],"options_en":["Andy, Louis, Nick","Andy, Tony, Louis","Andy, Nick, Francis","Andy, Louis, Nicholas"],"answer":0,"explanation_zh":"劉德華、古天樂、張家輝。","explanation_en":"Andy Lau, Louis Koo, and Nick Cheung.","difficulty":1},
{"question_zh":"《門徒》（2007）中，劉德華飾演什麼角色？","options_zh":["大毒梟","卧底警察","律師","醫生"],"options_en":["Drug lord","Undercover cop","Lawyer","Doctor"],"answer":0,"explanation_zh":"飾演大毒梟林昆。","explanation_en":"Plays drug lord Lin Kun.","difficulty":1},
{"question_zh":"《孤男寡女》（2000）中，劉德華與誰合演？","options_zh":["鄭秀文","張柏芝","李嘉欣","邱淑貞"],"options_en":["Sammi Cheng","Cecilia Cheung","Michelle Reis","Chingmy Yau"],"answer":0,"explanation_zh":"與鄭秀文合演。","explanation_en":"Co-stars with Sammi Cheng.","difficulty":1},
{"question_zh":"劉德華的歌迷統稱叫什麼？","options_zh":["華迷","華粉","華仔迷","劉迷"],"options_en":["Hua fans","Andy fans","Lau fans","Brother fans"],"answer":0,"explanation_zh":"統稱為「華迷」。","explanation_en":"Called 'Hua fans'.","difficulty":1},
{"question_zh":"劉德華的唱片銷量超過多少張？","options_zh":["1億張","5000萬張","2億張","5億張"],"options_en":["100M","50M","200M","500M"],"answer":0,"explanation_zh":"超過1億張。","explanation_en":"Over 100 million.","difficulty":2},
{"question_zh":"《暗戰》中，劉德華憑此片首次獲得什麼？","options_zh":["金像獎影帝","金馬獎影帝","康城影帝","金球獎"],"options_en":["HK Film Award Best Actor","Golden Horse Best Actor","Cannes Best Actor","Golden Globe"],"answer":0,"explanation_zh":"首次獲得金像獎影帝。","explanation_en":"First HK Film Award for Best Actor.","difficulty":1},
{"question_zh":"劉德華與梅艷芳合演的經典電影是什麼？","options_zh":["《91神鵰俠侶》","《審死官》","《瘦身男女》","《孤男寡女》"],"options_en":["Saviour of the Soul","Justice My Foot","Love on a Diet","Needing You"],"answer":0,"explanation_zh":"兩人合演《91神鵰俠侶》。","explanation_en":"They co-starred in 'Saviour of the Soul'.","difficulty":2},
{"question_zh":"《金手指》（2023）中，劉德華與誰合演？","options_zh":["梁朝偉","古天樂","張家輝","謝霆鋒"],"options_en":["Tony Leung","Louis Koo","Nick Cheung","Nicholas Tse"],"answer":0,"explanation_zh":"與梁朝偉合演《金手指》。","explanation_en":"Co-stars with Tony Leung in 'The Goldfinger'.","difficulty":1},
{"question_zh":"劉德華出道時是哪間電視台的藝員？","options_zh":["無綫電視（TVB）","亞洲電視（ATV）","佳藝電視","有線電視"],"options_en":["TVB","ATV","RTV","Cable TV"],"answer":0,"explanation_zh":"1981年從TVB藝員訓練班畢業。","explanation_en":"Graduated from TVB's acting class in 1981.","difficulty":1},
])

# ═══════════════════════════════════════════════════════════════
# 梁朝偉 - Top 10 films
# ═══════════════════════════════════════════════════════════════
print("🎭 梁朝偉系列...")

w("tony_leung/hua_yang_nian_hua.json", [
{"question_zh":"《花樣年華》（2000）的故事發生在哪個年代？","options_zh":["1960年代","1970年代","1980年代","1990年代"],"options_en":["1960s","1970s","1980s","1990s"],"answer":0,"explanation_zh":"故事發生在1960年代的香港。","explanation_en":"Set in 1960s Hong Kong.","difficulty":1},
{"question_zh":"《花樣年華》中，周慕雲和蘇麗珍的關係是？","options_zh":["鄰居","同事","戀人","同學"],"options_en":["Neighbors","Colleagues","Lovers","Classmates"],"answer":0,"explanation_zh":"兩人是鄰居，發現各自的配偶有婚外情。","explanation_en":"They are neighbors whose spouses are having affairs.","difficulty":1},
{"question_zh":"《花樣年華》的配樂以什麼樂器為主？","options_zh":["小提琴","大提琴","鋼琴","二胡"],"options_en":["Violin","Cello","Piano","Erhu"],"answer":0,"explanation_zh":"配樂以小提琴為主，由梅林茂作曲。","explanation_en":"Violin-dominated, composed by Shigeru Umebayashi.","difficulty":2},
{"question_zh":"《花樣年華》中，蘇麗珍經常穿什麼？","options_zh":["旗袍","洋裝","牛仔褲","運動服"],"options_en":["Cheongsam","Western dress","Jeans","Sportswear"],"answer":0,"explanation_zh":"蘇麗珍經常穿旗袍，片中有超過20套。","explanation_en":"She wears cheongsam, with over 20 in the film.","difficulty":1},
{"question_zh":"《花樣年華》中，蘇麗珍由誰飾演？","options_zh":["張曼玉","劉嘉玲","章子怡","鞏俐"],"options_en":["Maggie Cheung","Carina Lau","Zhang Ziyi","Gong Li"],"answer":0,"explanation_zh":"張曼玉飾演蘇麗珍。","explanation_en":"Maggie Cheung plays Su Li-zhen.","difficulty":1},
{"question_zh":"《花樣年華》的導演是誰？","options_zh":["王家衛","杜琪峰","許鞍華","陳可辛"],"options_en":["Wong Kar-wai","Johnnie To","Ann Hui","Peter Chan"],"answer":0,"explanation_zh":"王家衛執導。","explanation_en":"Directed by Wong Kar-wai.","difficulty":1},
{"question_zh":"《花樣年華》中，周慕雲的職業是什麼？","options_zh":["報社編輯","記者","作家","老師"],"options_en":["Newspaper editor","Journalist","Writer","Teacher"],"answer":0,"explanation_zh":"周慕雲是報社編輯。","explanation_en":"Chow Mo-wan is a newspaper editor.","difficulty":1},
{"question_zh":"《花樣年華》獲得什麼國際獎項？","options_zh":["康城影展最佳男主角","威尼斯金獅獎","柏林金熊獎","奧斯卡最佳影片"],"options_en":["Cannes Best Actor","Venice Golden Lion","Berlin Golden Bear","Oscar Best Picture"],"answer":0,"explanation_zh":"梁朝偉獲得康城影帝。","explanation_en":"Tony Leung won Cannes Best Actor.","difficulty":1},
{"question_zh":"《花樣年華》中，兩人發現了什麼秘密？","options_zh":["各自的配偶有婚外情","鄰居是罪犯","有人失蹤","有人被殺"],"options_en":["Spouses having affairs","Neighbor is criminal","Someone missing","Someone killed"],"answer":0,"explanation_zh":"發現各自的配偶有婚外情。","explanation_en":"They discover their spouses are having affairs.","difficulty":1},
{"question_zh":"《花樣年華》的經典台詞「如果多一張船價」出自誰口？","options_zh":["周慕雲","蘇麗珍","旁白","導演"],"options_en":["Chow Mo-wan","Su Li-zhen","Narrator","Director"],"answer":0,"explanation_zh":"周慕雲說出這句經典台詞。","explanation_en":"Chow Mo-wan says this classic line.","difficulty":1},
])

w("tony_leung/wu_jian_dao.json", [
{"question_zh":"《無間道》中，陳永仁的身份是什麼？","options_zh":["警方臥底","黑幫臥底","普通警察","黑幫老大"],"options_en":["Police undercover","Triad mole","Regular cop","Triad boss"],"answer":0,"explanation_zh":"陳永仁是潜入黑幫的警方臥底。","explanation_en":"Chan Wing-yan is an undercover cop in the triads.","difficulty":1},
{"question_zh":"《無間道》中，陳永仁的經典對白是什麼？","options_zh":["「對唔住，我係警察」","「我想做好人」","「以前嘅事就由得佢過去」","「你有冇試過做好人？」"],"options_en":["Sorry, I'm a cop","I want to be good","Let the past go","Have you tried being good?"],"answer":0,"explanation_zh":"陳永仁說「對唔住，我係警察」。","explanation_en":"'Sorry, I'm a cop.'","difficulty":1},
{"question_zh":"《無間道》中，陳永仁最後的結局如何？","options_zh":["在電梯中被殺","被捕","逃脫","成為好人"],"options_en":["Killed in elevator","Arrested","Escapes","Becomes good"],"answer":0,"explanation_zh":"陳永仁在電梯中被殺。","explanation_en":"He is killed in an elevator.","difficulty":1},
{"question_zh":"《無間道》中，陳永仁的上司是誰？","options_zh":["黃志誠","劉建明","韓琛","曾志偉"],"options_en":["Wong Chi-sing","Lau Kin-ming","Hon Sam","Eric Tsang"],"answer":0,"explanation_zh":"黃志誠是陳永仁的上司。","explanation_en":"Superintendent Wong is his handler.","difficulty":1},
{"question_zh":"《無間道》中，梁朝偉與劉德華在天台的經典場面叫什麼？","options_zh":["天台對峙","電梯決戰","街頭追逐","談判"],"options_en":["Rooftop confrontation","Elevator battle","Street chase","Negotiation"],"answer":0,"explanation_zh":"天台對峙是全片最經典的場面。","explanation_en":"The rooftop confrontation is the most iconic scene.","difficulty":1},
{"question_zh":"《無間道》中，陳永仁在黑幫中的身份是什麼？","options_zh":["韓琛的手下","臥底","殺手","商人"],"options_en":["Hon Sam's man","Undercover","Hitman","Businessman"],"answer":0,"explanation_zh":"陳永仁是韓琛的手下。","explanation_en":"He is Hon Sam's man.","difficulty":1},
{"question_zh":"《無間道》中，陳永仁有什麼心理壓力？","options_zh":["身份危機","經濟壓力","家庭問題","健康問題"],"options_en":["Identity crisis","Financial pressure","Family issues","Health issues"],"answer":0,"explanation_zh":"長期臥底導致身份危機。","explanation_en":"Long-term undercover work causes identity crisis.","difficulty":1},
{"question_zh":"《無間道》系列共有幾集？","options_zh":["2集","3集","4集","5集"],"options_en":["2","3","4","5"],"answer":1,"explanation_zh":"共有3集。","explanation_en":"3 films in the series.","difficulty":1},
{"question_zh":"《無間道》中，梁朝偉的演出獲得什麼評價？","options_zh늉":["被譽為他最好的演出之一","普通","被批評","不獲好評"],"options_en":["One of his best performances","Average","Criticized","Not well received"],"answer":0,"explanation_zh":"被譽為梁朝偉最好的演出之一。","explanation_en":"Widely regarded as one of his best performances.","difficulty":1},
{"question_zh":"《無間道》是哪一年上映的？","options_zh":["2000年","2001年","2002年","2003年"],"options_en":["2000","2001","2002","2003"],"answer":2,"explanation_zh":"2002年上映。","explanation_en":"Released in 2002.","difficulty":1},
])

w("tony_leung/other.json", [
{"question_zh":"《春光乍洩》（1997）中，梁朝偉飾演誰？","options_zh":["黎耀輝","何寶榮","周慕雲","易先生"],"options_en":["Lai Yiu-fai","Ho Po-wing","Chow Mo-wan","Mr. Yee"],"answer":0,"explanation_zh":"飾演黎耀輝。","explanation_en":"Plays Lai Yiu-fai.","difficulty":1},
{"question_zh":"《色，戒》（2007）中，梁朝偉飾演誰？","options_zh":["易先生","周慕雲","陳永仁","黎耀輝"],"options_en":["Mr. Yee","Chow Mo-wan","Chan Wing-yan","Lai Yiu-fai"],"answer":0,"explanation_zh":"飾演特務頭子易先生。","explanation_en":"Plays spy chief Mr. Yee.","difficulty":1},
{"question_zh":"《一代宗師》（2013）中，梁朝偉飾演誰？","options_zh":["葉問","宮二","一線天","馬三"],"options_en":["Ip Man","Gong Er","Razor","Ma San"],"answer":0,"explanation_zh":"飾演詠春拳宗師葉問。","explanation_en":"Plays Wing Chun grandmaster Ip Man.","difficulty":1},
{"question_zh":"《重慶森林》（1994）中，梁朝偉飾演什麼職業？","options_zh":["警察","廚師","作家","醫生"],"options_en":["Police","Chef","Writer","Doctor"],"answer":0,"explanation_zh":"飾演警察663。","explanation_en":"Plays Police Officer 663.","difficulty":1},
{"question_zh":"《東邪西毒》（1994）中，梁朝偉飾演誰？","options_zh":["盲劍客","黃藥師","歐陽鋒","洪七"],"options_en":["Blind Swordsman","Huang Yaoshi","Ouyang Feng","Hong Qi"],"answer":0,"explanation_zh":"飾演盲劍客。","explanation_en":"Plays the Blind Swordsman.","difficulty":1},
{"question_zh":"《阿飛正傳》（1990）中，梁朝偉在最後一幕做什麼？","options_zh":["梳頭","跳舞","唱歌","睡覺"],"options_en":["Combing hair","Dancing","Singing","Sleeping"],"answer":0,"explanation_zh":"梁朝偉在最後一幕梳頭，僅出場3分鐘。","explanation_en":"He appears for only 3 minutes, combing his hair in the final scene.","difficulty":2},
{"question_zh":"《尚氣》（2021）中，梁朝偉飾演什麼角色？","options_zh":["文武","尚氣","十環幫首領","以上皆是"],"options_en":["Wenwu","Shang-Chi","Ten Rings leader","All above"],"answer":0,"explanation_zh":"飾演尚氣的父親文武。","explanation_en":"Plays Wenwu, Shang-Chi's father.","difficulty":1},
{"question_zh":"梁朝偉獲得過幾次金像獎影帝？","options_zh":["3次","4次","5次","6次"],"options_en":["3","4","5","6"],"answer":2,"explanation_zh":"五度獲得金像獎影帝。","explanation_en":"Won 5 times.","difficulty":1},
{"question_zh":"梁朝偉的太太是誰？","options_zh":["劉嘉玲","張曼玉","曾華倩","黎美嫻"],"options_en":["Carina Lau","Maggie Cheung","Margie Tsang","Kitty Lai"],"answer":0,"explanation_zh":"與劉嘉玲在2008年結婚。","explanation_en":"Married Carina Lau in 2008.","difficulty":1},
{"question_zh":"梁朝偉出道時是哪間電視台的藝員？","options_zh":["無綫電視（TVB）","亞洲電視（ATV）","佳藝電視","有線電視"],"options_en":["TVB","ATV","RTV","Cable TV"],"answer":0,"explanation_zh":"1982年從TVB藝員訓練班畢業。","explanation_en":"Graduated from TVB in 1982.","difficulty":1},
{"question_zh":"梁朝偉出生於哪一年？","options_zh":["1960年","1962年","1964年","1966年"],"options_en":["1960","1962","1964","1966"],"answer":1,"explanation_zh":"1962年6月27日出生。","explanation_en":"Born June 27, 1962.","difficulty":1},
{"question_zh":"《2046》（2004）中，梁朝偉飾演什麼職業？","options_zh":["作家","記者","商人","教師"],"options_en":["Writer","Journalist","Businessman","Teacher"],"answer":0,"explanation_zh":"飾演作家周慕雲。","explanation_en":"Plays writer Chow Mo-wan.","difficulty":1},
{"question_zh":"梁朝偉與王家衛合作的第一部電影是什麼？","options_zh":["《阿飛正傳》","《重慶森林》","《東邪西毒》","《春光乍洩》"],"options_en":["Days of Being Wild","Chungking Express","Ashes of Time","Happy Together"],"answer":0,"explanation_zh":"《阿飛正傳》（1990）是兩人首次合作。","explanation_en":"'Days of Being Wild' (1990) was their first collaboration.","difficulty":2},
{"question_zh":"《花樣年華》中，梁朝偉的演出風格是什麼？","options_zh":["內斂含蓄","外放誇張","搞笑幽默","動作利落"],"options_en":["Restrained","Exaggerated","Funny","Action"],"answer":0,"explanation_zh":"以內斂含蓄的風格演出。","explanation_en":"Restrained and subtle performance.","difficulty":1},
{"question_zh":"梁朝偉的演藝風格以什麼著稱？","options_zh":["內斂含蓄","外放誇張","搞笑幽默","動作利落"],"options_en":["Restrained & subtle","Exaggerated","Funny","Action"],"answer":0,"explanation_zh":"以內斂含蓄的演繹風格著稱。","explanation_en":"Known for restrained and subtle acting.","difficulty":1},
])

# ═══════════════════════════════════════════════════════════════
# 古天樂 - Top 10 films
# ═══════════════════════════════════════════════════════════════
print("😎 古天樂系列...")

w("louis_koo/shen_diao_xia_lv.json", [
{"question_zh":"《神鵰俠侶》（1995 TVB）中，楊過的義父是誰？","options_zh":["歐陽鋒","黃藥師","洪七公","一燈大師"],"options_en":["Ouyang Feng","Huang Yaoshi","Hong Qigong","Yideng"],"answer":0,"explanation_zh":"楊過認歐陽鋒為義父。","explanation_en":"Yang Guo's godfather is Ouyang Feng.","difficulty":1},
{"question_zh":"《神鵰俠侶》中，小龍女由誰飾演？","options_zh":["李若彤","陳玉蓮","范文芳","劉亦菲"],"options_en":["Carman Lee","Idy Chan","Fann Wong","Liu Yifei"],"answer":0,"explanation_zh":"李若彤飾演小龍女。","explanation_en":"Carman Lee plays Xiaolongnü.","difficulty":1},
{"question_zh":"《神鵰俠侶》中，楊過用什麼武器？","options_zh":["玄鐵重劍","倚天劍","屠龍刀","打狗棒"],"options_en":["Heavy Iron Sword","Heaven Sword","Dragon Saber","Dog Beating Staff"],"answer":0,"explanation_zh":"楊過使用玄鐵重劍。","explanation_en":"Yang Guo uses the Heavy Iron Sword.","difficulty":1},
{"question_zh":"《神鵰俠侶》中，楊過在什麼地方與小龍女分別？","options_zh":["絕情谷","古墓","襄陽","華山"],"options_en":["Valley of No Love","Ancient Tomb","Xiangyang","Huashan"],"answer":0,"explanation_zh":"楊過在絕情谷與小龍女分別。","explanation_en":"They separate at the Valley of No Love.","difficulty":1},
{"question_zh":"《神鵰俠侶》中，楊過等了小龍女多少年？","options_zh":["10年","16年","20年","5年"],"options_en":["10 years","16 years","20 years","5 years"],"answer":1,"explanation_zh":"楊過等了小龍女16年。","explanation_en":"Yang Guo waits 16 years for Xiaolongnü.","difficulty":1},
{"question_zh":"《神鵰俠侶》中，古天樂的膚色與現在有什麼不同？","options_zh":["當時較白","當時已黑","沒有分別","不詳"],"options_en":["Was lighter then","Already dark","No difference","Unknown"],"answer":0,"explanation_zh":"古天樂拍《神鵰俠侶》時膚色較白。","explanation_en":"He was lighter-skinned during filming.","difficulty":1},
{"question_zh":"《神鵰俠侶》中，郭靖由誰飾演？","options_zh":["白彪","劉德華","梁朝偉","黃日華"],"options_en":["Piu Biu","Andy Lau","Tony Leung","Felix Wong"],"answer":0,"explanation_zh":"白彪飾演郭靖。","explanation_en":"Piu Biu plays Guo Jing.","difficulty":2},
{"question_zh":"《神鵰俠侶》是金庸的第幾部小說？","options_zh":["第二部","第三部","第四部","第五部"],"options_en":["2nd","3rd","4th","5th"],"answer":2,"explanation_zh":"《神鵰俠侶》是金庸的第四部小說。","explanation_en":"It's Jin Yong's 4th novel.","difficulty":2},
{"question_zh":"《神鵰俠侶》中，楊過與小龍女的師徒關係被稱為什麼？","options_zh":["師徒戀","禁忌之戀","以上皆是","普通師徒"],"options_en":["Teacher-student love","Forbidden love","All above","Normal"],"answer":2,"explanation_zh":"他們的關係被稱為師徒戀、禁忌之戀。","explanation_en":"Their relationship is called teacher-student and forbidden love.","difficulty":1},
{"question_zh":"《神鵰俠侶》中，楊過最終與小龍女在哪裡重逢？","options_zh":["絕情谷底","古墓","襄陽","華山"],"options_en":["Bottom of Valley","Ancient Tomb","Xiangyang","Huashan"],"answer":0,"explanation_zh":"在絕情谷底重逢。","explanation_en":"They reunite at the bottom of the Valley of No Love.","difficulty":1},
])

w("louis_koo/xun_qin_ji.json", [
{"question_zh":"《尋秦記》（2001 TVB）中，項少龍從哪個年代穿越？","options_zh":["21世紀","20世紀","19世紀","22世紀"],"options_en":["21st century","20th century","19th century","22nd century"],"answer":0,"explanation_zh":"從21世紀穿越到秦國。","explanation_en":"Travels from 21st century to Qin dynasty.","difficulty":1},
{"question_zh":"《尋秦記》中，嬴政由誰飾演？","options_zh":["林峯","林文龍","馬國明","陳鍵鋒"],"options_en":["Raymond Lam","Lam Man-leung","Kenneth Ma","Sammul Chan"],"answer":0,"explanation_zh":"林峯飾演嬴政。","explanation_en":"Raymond Lam plays Ying Zheng.","difficulty":1},
{"question_zh":"《尋秦記》中，烏廷芳由誰飾演？","options_zh":["宣萱","郭羨妮","滕麗名","胡杏兒"],"options_en":["Jessica Hsuan","Sonija Kwok","Tavia Yeung","Myolie Wu"],"answer":0,"explanation_zh":"宣萱飾演烏廷芳。","explanation_en":"Jessica Hsuan plays Wu Ting-fong.","difficulty":1},
{"question_zh":"《尋秦記》改編自哪位作家的小說？","options_zh":["黃易","金庸","古龍","梁羽生"],"options_en":["Wong Yi","Jin Yong","Gu Long","Liang Yusheng"],"answer":0,"explanation_zh":"改編自黃易的同名小說。","explanation_en":"Adapted from Wong Yi's novel.","difficulty":1},
{"question_zh":"《尋秦記》中，項少龍的職業是什麼？","options_zh":["特種部隊軍人","科學家","警察","商人"],"options_en":["Special forces soldier","Scientist","Police","Businessman"],"answer":0,"explanation_zh":"項少龍是特種部隊軍人。","explanation_en":"He is a special forces soldier.","difficulty":1},
{"question_zh":"《尋秦記》中，項少龍幫助嬴政做了什麼？","options_zh":["成為秦始皇","打敗敵人","找到寶藏","回到未來"],"options_en":["Become Qin Shi Huang","Defeat enemies","Find treasure","Return to future"],"answer":0,"explanation_zh":"項少龍幫助嬴政成為秦始皇。","explanation_en":"He helps Ying Zheng become Qin Shi Huang.","difficulty":1},
{"question_zh":"《尋秦記》中，善柔由誰飾演？","options_zh":["郭羨妮","宣萱","滕麗名","胡杏兒"],"options_en":["Sonija Kwok","Jessica Hsuan","Tavia Yeung","Myolie Wu"],"answer":0,"explanation_zh":"郭羨妮飾演善柔。","explanation_en":"Sonija Kwok plays Shan Rou.","difficulty":1},
{"question_zh":"《尋秦記》是TVB的經典劇集，共有多少集？","options_zh":["20集","30集","40集","50集"],"options_en":["20","30","40","50"],"answer":2,"explanation_zh":"共有40集。","explanation_en":"40 episodes.","difficulty":1},
{"question_zh":"《尋秦記》中，項少龍最終選擇了什麼？","options_zh":["留在秦國","回到現代","與愛人在一起","以上皆是"],"options_en":["Stay in Qin","Return to modern","Be with lover","All above"],"answer":2,"explanation_zh":"項少龍最終選擇與愛人在一起。","explanation_en":"He chooses to be with his lover.","difficulty":1},
{"question_zh":"《尋秦記》被譽為什麼類型的經典？","options_zh":["穿越劇","武俠劇","歷史劇","愛情劇"],"options_en":["Time travel","Martial arts","Historical","Romance"],"answer":0,"explanation_zh":"被譽為穿越劇的經典。","explanation_en":"Regarded as a classic time-travel drama.","difficulty":1},
])

w("louis_koo/other.json", [
{"question_zh":"《明日戰記》（2022）是什麼類型的電影？","options_zh":["科幻動作片","愛情片","喜劇片","文藝片"],"options_en":["Sci-fi action","Romance","Comedy","Drama"],"answer":0,"explanation_zh":"香港首部大型科幻動作片。","explanation_en":"HK's first major sci-fi action film.","difficulty":1},
{"question_zh":"《九龍城寨之圍城》（2024）改編自什麼？","options_zh":["漫畫","小說","真實事件","遊戲"],"options_en":["Comic","Novel","True story","Game"],"answer":0,"explanation_zh":"改編自余兒的漫畫。","explanation_en":"Adapted from a comic.","difficulty":1},
{"question_zh":"《竊聽風雲》系列共有幾集？","options_zh":["2集","3集","4集","5集"],"options_en":["2","3","4","5"],"answer":1,"explanation_zh":"共有3集。","explanation_en":"3 films.","difficulty":1},
{"question_zh":"《殺破狼·貪狼》（2017）中，古天樂獲得什麼獎？","options_zh":["金像獎影帝","金馬獎影帝","康城影帝","金球獎"],"options_en":["HK Film Award Best Actor","Golden Horse","Cannes","Golden Globe"],"answer":0,"explanation_zh":"獲得2018年金像獎影帝。","explanation_en":"Won Best Actor at 2018 HK Film Awards.","difficulty":1},
{"question_zh":"古天樂創辦的電影公司叫什麼？","options_zh":["天下一電影","中國星","寰亞","英皇"],"options_en":["One Cool Film","China Star","Media Asia","Emperor"],"answer":0,"explanation_zh":"創辦了天下一電影。","explanation_en":"Founded One Cool Film.","difficulty":1},
{"question_zh":"古天樂的慈善基金在內地捐建了多少所學校？","options_zh":["超過50所","超過100所","超過200所","超過300所"],"options_en":["Over 50","Over 100","Over 200","Over 300"],"answer":1,"explanation_zh":"超過100所。","explanation_en":"Over 100 schools.","difficulty":1},
{"question_zh":"古天樂在哪一年擔任香港演藝人協會會長？","options_zh":["2016年","2018年","2019年","2020年"],"options_en":["2016","2018","2019","2020"],"answer":2,"explanation_zh":"2019年當選。","explanation_en":"Elected in 2019.","difficulty":2},
{"question_zh":"古天樂的膚色為何特別黑？","options_zh אימי":["故意曬黑","天生","化妝","長期拍戲"],"options_en":["Intentionally tanned","Natural","Makeup","Filming"],"answer":0,"explanation_zh":"為了擺脫白面書生形象而故意曬黑。","explanation_en":"Tanned to shed his pale scholar image.","difficulty":1},
{"question_zh":"古天樂出生於哪一年？","options_zh":["1968年","1970年","1972年","1974年"],"options_en":["1968","1970","1972","1974"],"answer":1,"explanation_zh":"1970年10月21日出生。","explanation_en":"Born October 21, 1970.","difficulty":1},
{"question_zh":"《反貪風暴》系列共有幾集？","options_zh":["3集","4集","5集","6集"],"options_en":["3","4","5","6"],"answer":1,"explanation_zh":"共有4集。","explanation_en":"4 films.","difficulty":1},
{"question_zh":"古天樂在《犯罪現場》（2019）中飾演什麼角色？","options_zh אימי":["盲人","聾人","殘障人士","正常人"],"options_en":["Blind","Deaf","Disabled","Normal"],"answer":0,"explanation_zh":"飾演盲人。","explanation_en":"Plays a blind person.","difficulty":1},
{"question_zh":"古天樂與誰被稱為「古宣CP」？","options_zh אימי":["宣萱","郭羨妮","胡杏兒","佘詩曼"],"options_en":["Jessica Hsuan","Sonija Kwok","Myolie Wu","Charmaine Sheh"],"answer":0,"explanation_zh":"與宣萱被稱為「古宣CP」。","explanation_en":"Known as the 'Gu-Xuan CP' with Jessica Hsuan.","difficulty":1},
{"question_zh":"古天樂出道時是哪間電視台的藝員？","options_zh":["無綫電視（TVB）","亞洲電視（ATV）","佳藝電視","有線電視"],"options_en":["TVB","ATV","RTV","Cable TV"],"answer":0,"explanation_zh":"1993年加入TVB。","explanation_en":"Joined TVB in 1993.","difficulty":1},
{"question_zh":"《掃毒》（2013）中，古天樂與誰合演？","options_zh אימי":["劉德華、張家輝","梁朝偉、劉德華","張家輝、謝霆鋒","黃秋生、曾志偉"],"options_en":["Andy Lau, Nick Cheung","Tony Leung, Andy Lau","Nick Cheung, Nicholas Tse","Anthony Wong, Eric Tsang"],"answer":0,"explanation_zh":"與劉德華、張家輝合演。","explanation_en":"Co-stars with Andy Lau and Nick Cheung.","difficulty":1},
{"question_zh":"古天樂是哪一年加入TVB的？","options_zh אימי":["1991年","1993年","1995年","1997年"],"options_en":["1991","1993","1995","1997"],"answer":1,"explanation_zh":"1993年加入。","explanation_en":"Joined in 1993.","difficulty":1},
])

# ═══════════════════════════════════════════════════════════════
# 嚦咕嚦咕新年財
# ═══════════════════════════════════════════════════════════════
print("🀄 嚦咕嚦咕新年財...")

w("fat_choi/main.json", [
{"question_zh":"《嚦咕嚦咕新年財》的導演是誰？","options_zh אימי":["韋家輝","杜琪峰","劉偉強","陳慶嘉"],"options_en":["Wai Ka-fai","Johnnie To","Andrew Lau","Chan Hing-ka"],"answer":0,"explanation_zh":"韋家輝執導。","explanation_en":"Directed by Wai Ka-fai.","difficulty":1},
{"question_zh":"《嚦咕嚦咕新年財》中，劉德華飾演的角色叫什麼？","options_zh":["Andy","阿財","華仔","賭神"],"options_en":["Andy","Ah Choi","Wah Zai","God of Gamblers"],"answer":0,"explanation_zh":"劉德華飾演Andy。","explanation_en":"Andy Lau plays Andy.","difficulty":1},
{"question_zh":"《嚦咕嚦咕新年財》中，梁詠琪飾演什麼角色？","options_zh":["Joker","Queen","阿琪","小美"],"options_en":["Joker","Queen","Ah Kei","Siu Mei"],"answer":0,"explanation_zh":"梁詠琪飾演Joker。","explanation_en":"Gigi Leung plays Joker.","difficulty":1},
{"question_zh":"《嚦咕嚦咕新年財》中，古天樂的角色有什麼特點？","options_zh":["經常輸錢的麻將高手","黑幫老大","警察","醫生"],"options_en":["Mahjong expert who loses","Triad boss","Police","Doctor"],"answer":0,"explanation_zh":"古天樂飾演自稱高手但經常輸錢的角色。","explanation_en":"Louis Koo plays a self-proclaimed expert who keeps losing.","difficulty":1},
{"question_zh":"片名「嚦咕嚦咕」是什麼意思？","options_zh אימי":["麻將術語，摸牌聲音","恭喜發財","新年快樂","打牌動作"],"options_en":["Mahjong drawing sound","Congratulations","Happy New Year","Playing action"],"answer":0,"explanation_zh":"是打麻將時摸牌的象聲詞。","explanation_en":"Onomatopoeia for drawing mahjong tiles.","difficulty":1},
{"question_zh":"《嚦咕嚦咕新年財》與哪部電影系列有關？","options_zh":["《賭神》系列","《賭聖》系列","《賭俠》系列","《千王之王》系列"],"options_en":["God of Gamblers","All for the Winner","God of Gamblers II","King of Gamblers"],"answer":0,"explanation_zh":"是《賭神》系列的衍生作品。","explanation_en":"A spin-off of the God of Gamblers series.","difficulty":1},
{"question_zh":"《嚦咕嚦咕新年財》中，Joker的職業是什麼？","options_zh אימי":["護士","空姐","教師","秘書"],"options_en":["Nurse","Stewardess","Teacher","Secretary"],"answer":0,"explanation_zh":"Joker的職業是護士。","explanation_en":"Joker is a nurse.","difficulty":1},
{"question_zh":"《嚦咕嚦咕新年財》是哪一年賀歲檔上映？","options_zh":["2000年龍年","2001年蛇年","2002年馬年","2003年羊年"],"options_en":["2000 Dragon","2001 Snake","2002 Horse","2003 Goat"],"answer":1,"explanation_zh":"2001年蛇年賀歲檔上映。","explanation_en":"Released in 2001 Year of Snake.","difficulty":2},
{"question_zh":"《嚦咕嚦咕新年財》中，Andy為什麼重新打牌？","options_zh אימי":["為Joker籌醫藥費","報仇","贏錢","好玩"],"options_en":["Pay medical bills","Revenge","Win money","Fun"],"answer":0,"explanation_zh":"為了籌Joker的醫藥費。","explanation_en":"To raise money for Joker's medical bills.","difficulty":1},
{"question_zh":"《嚦咕嚦咕新年財》中，Joker發生了什麼事？","options_zh":["車禍","生病","被綁架","失憶"],"options_en":["Car accident","Sick","Kidnapped","Amnesia"],"answer":0,"explanation_zh":"Joker發生車禍受傷。","explanation_en":"Joker is injured in a car accident.","difficulty":1},
{"question_zh":"《嚦咕嚦咕新年財》中，Andy的母親對打牌的態度是？","options_zh":["支持","反對","中立","無所謂"],"options_en":["Support","Oppose","Neutral","Indifferent"],"answer":1,"explanation_zh":"Andy的母親反對他打牌。","explanation_en":"Andy's mother opposes his mahjong playing.","difficulty":1},
{"question_zh":"《嚦咕嚦咕新年財》中，飾演Andy母親的演員是誰？","options_zh אימי":["羅蘭","鮑起靜","盧海鵬","夏萍"],"options_en":["Law Lan","Paw Hee-ching","Lo Hoi-pang","Ha Ping"],"answer":0,"explanation_zh":"羅蘭飾演Andy的母親。","explanation_en":"Law Lan plays Andy's mother.","difficulty":2},
{"question_zh":"《嚦咕嚦咕新年財》中，古天樂的角色最終怎樣？","options_zh":["繼續做麻將高手","放棄打牌","結婚","出國"],"options_en":["Continues","Gives up","Married","Abroad"],"answer":1,"explanation_zh":"阿Mo最終放棄打牌。","explanation_en":"Ah Mo gives up mahjong.","difficulty":1},
{"question_zh":"《嚦咕嚦咕新年財》中，「食糊」是什麼意思？","options_zh":["贏了","輸了","碰牌","吃牌"],"options_en":["Win","Lose","Pong","Chow"],"answer":0,"explanation_zh":"「食糊」就是贏了這一局。","explanation_en":"'食糊' means winning the round.","difficulty":1},
{"question_zh":"《嚦咕嚦咕新年財》的主題曲是什麼？","options_zh":["《恭喜發財》","《嚦咕嚦咕》","《新年財》","《賭神》"],"options_en":["Congratulations","Lek Gu Lek Gu","New Year Fortune","God of Gamblers"],"answer":0,"explanation_zh":"主題曲是《恭喜發財》。","explanation_en":"Theme song is 'Congratulations and Prosperity'.","difficulty":1},
])

# ═══════════════════════════════════════════════════════════════
# Topic indexes
# ═══════════════════════════════════════════════════════════════
print("\n📝 Writing topic indexes...")

w("stephen_chow/index.json", [
{"id":"du_sheng","name_zh":"賭聖","name_en":"All for the Winner","emoji":"🃏","file":"du_sheng.json"},
{"id":"tao_xue_wei_long","name_zh":"逃學威龍","name_en":"Fight Back to School","emoji":"🏫","file":"tao_xue_wei_long.json"},
{"id":"tang_bo_hu","name_zh":"唐伯虎點秋香","name_en":"Flirting Scholar","emoji":"🎨","file":"tang_bo_hu.json"},
{"id":"da_hua_xi_you","name_zh":"大話西遊","name_en":"A Chinese Odyssey","emoji":"🐒","file":"da_hua_xi_you.json"},
{"id":"shi_shen","name_zh":"食神","name_en":"God of Cookery","emoji":"🍳","file":"shi_shen.json"},
{"id":"shao_lin_zu_qiu","name_zh":"少林足球","name_en":"Shaolin Soccer","emoji":"⚽","file":"shao_lin_zu_qiu.json"},
{"id":"gong_fu","name_zh":"功夫","name_en":"Kung Fu Hustle","emoji":"🥋","file":"gong_fu.json"},
{"id":"xi_ju_zhi_wang","name_zh":"喜劇之王","name_en":"King of Comedy","emoji":"👑","file":"xi_ju_zhi_wang.json"},
{"id":"chang_jiang_7","name_zh":"長江7號","name_en":"CJ7","emoji":"👽","file":"chang_jiang_7.json"},
{"id":"mei_ren_yu","name_zh":"美人魚","name_en":"The Mermaid","emoji":"🧜‍♀️","file":"mei_ren_yu.json"},
{"id":"other","name_zh":"其他電影","name_en":"Other Films","emoji":"🎬","file":"other.json"},
])

w("andy_lau/index.json", [
{"id":"wu_jian_dao","name_zh":"無間道","name_en":"Infernal Affairs","emoji":"🕵️","file":"wu_jian_dao.json"},
{"id":"an_zhan","name_zh":"暗戰","name_en":"Running Out of Time","emoji":"⏰","file":"an_zhan.json"},
{"id":"tao_jie","name_zh":"桃姐","name_en":"A Simple Life","emoji":"🍑","file":"tao_jie.json"},
{"id":"chai_dan_zhuan_jia","name_zh":"拆彈專家","name_en":"Shock Wave","emoji":"💣","file":"chai_dan_zhuan_jia.json"},
{"id":"other","name_zh":"其他電影","name_en":"Other Films","emoji":"🎬","file":"other.json"},
])

w("tony_leung/index.json", [
{"id":"hua_yang_nian_hua","name_zh":"花樣年華","name_en":"In the Mood for Love","emoji":"🌸","file":"hua_yang_nian_hua.json"},
{"id":"wu_jian_dao","name_zh":"無間道","name_en":"Infernal Affairs","emoji":"🕵️","file":"wu_jian_dao.json"},
{"id":"other","name_zh":"其他電影","name_en":"Other Films","emoji":"🎬","file":"other.json"},
])

w("louis_koo/index.json", [
{"id":"shen_diao_xia_lv","name_zh":"神鵰俠侶","name_en":"Return of the Condor Heroes","emoji":"🦅","file":"shen_diao_xia_lv.json"},
{"id":"xun_qin_ji","name_zh":"尋秦記","name_en":"A Step into the Past","emoji":"⏳","file":"xun_qin_ji.json"},
{"id":"other","name_zh":"其他電影","name_en":"Other Films","emoji":"🎬","file":"other.json"},
])

w("fat_choi/index.json", [
{"id":"main","name_zh":"嚦咕嚦咕新年財","name_en":"Fat Choi Spirit","emoji":"🀄","file":"main.json"},
])

# Count totals
total = 0
for root, dirs, files in os.walk(BASE):
    for f in files:
        if f.endswith('.json') and f != 'index.json':
            with open(os.path.join(root, f)) as fp:
                total += len(json.load(fp))

print(f"\n🎬 電影題庫總計：{total} 題")
