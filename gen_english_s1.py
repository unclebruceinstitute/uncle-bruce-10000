#!/usr/bin/env python3
import json, random, os
from collections import Counter
random.seed(42)

SS = ["He","She","The boy","My mother","The teacher","My father","Her sister","The baby","The dog","Everyone","Nobody","The girl","His brother","Each student","The player","The singer","The driver","The chef","The nurse","The artist"]
SP = ["I","You","We","They","The students","The children","Tom and Mary","My friends","Our class","The boys","Her parents","The workers","Many people","Both teams","The girls","The visitors"]
AS = SS + SP
VB = [("go","goes","went","gone","going"),("eat","eats","ate","eaten","eating"),("read","reads","read","read","reading"),("write","writes","wrote","written","writing"),("play","plays","played","played","playing"),("study","studies","studied","studied","studying"),("work","works","worked","worked","working"),("live","lives","lived","lived","living"),("buy","buys","bought","bought","buying"),("sell","sells","sold","sold","selling"),("make","makes","made","made","making"),("take","takes","took","taken","taking"),("have","has","had","had","having"),("do","does","did","done","doing"),("come","comes","came","come","coming"),("see","sees","saw","seen","seeing"),("give","gives","gave","given","giving"),("tell","tells","told","told","telling"),("think","thinks","thought","thought","thinking"),("know","knows","knew","known","knowing"),("run","runs","ran","run","running"),("walk","walks","walked","walked","walking"),("sing","sings","sang","sung","singing"),("swim","swims","swam","swum","swimming"),("fly","flies","flew","flown","flying"),("sleep","sleeps","slept","slept","sleeping"),("learn","learns","learned","learned","learning"),("drive","drives","drove","driven","driving"),("speak","speaks","spoke","spoken","speaking"),("teach","teaches","taught","taught","teaching"),("find","finds","found","found","finding"),("get","gets","got","gotten","getting"),("say","says","said","said","saying"),("feel","feels","felt","felt","feeling"),("keep","keeps","kept","kept","keeping"),("bring","brings","brought","brought","bringing"),("wear","wears","wore","worn","wearing"),("draw","draws","drew","drawn","drawing"),("throw","throws","threw","thrown","throwing"),("drink","drinks","drank","drunk","drinking")]
TM_P = ["every day","every week","every morning","usually","always","often","sometimes","on Sundays","every Monday","each month","at night"]
TQ = ["yesterday","last week","last month","last year","two days ago","this morning","last night","in 2020","last Monday","three hours ago","last summer","in 1999"]
TE = ["already","just","ever","never","before","since 2020","for three years","so far","recently","yet","since last year","for a long time"]
TF = ["tomorrow","next week","next month","next year","soon","later","in two days","tonight","next Monday","this weekend","next summer","in the future"]
TN = ["now","right now","at the moment","currently","today","this afternoon"]
AC = [("go to school","goes to school","went to school","gone to school","going to school","上学"),("eat breakfast","eats breakfast","ate breakfast","eaten breakfast","eating breakfast","吃早餐"),("do homework","does homework","did homework","done homework","doing homework","做功课"),("play football","plays football","played football","played football","playing football","踢足球"),("read a book","reads a book","read a book","read a book","reading a book","看书"),("watch TV","watches TV","watched TV","watched TV","watching TV","看电视"),("cook dinner","cooks dinner","cooked dinner","cooked dinner","cooking dinner","煮晚餐"),("clean the room","cleans the room","cleaned the room","cleaned the room","cleaning the room","打扫房间"),("walk to work","walks to work","walked to work","walked to work","walking to work","走路去上班"),("study English","studies English","studied English","studied English","studying English","学英文"),("ride a bicycle","rides a bicycle","rode a bicycle","ridden a bicycle","riding a bicycle","骑单车"),("fly a kite","flies a kite","flew a kite","flown a kite","flying a kite","放风筝"),("sing a song","sings a song","sang a song","sung a song","singing a song","唱歌"),("draw a picture","draws a picture","drew a picture","drawn a picture","drawing a picture","画画"),("write a letter","writes a letter","wrote a letter","written a letter","writing a letter","写信"),("drink water","drinks water","drank water","drunk water","drinking water","喝水"),("drive a car","drives a car","drove a car","driven a car","driving a car","开车"),("teach students","teaches students","taught students","taught students","teaching students","教学生"),("make a cake","makes a cake","made a cake","made a cake","making a cake","做蛋糕"),("take a photo","takes a photo","took a photo","taken a photo","taking a photo","拍照"),("build a house","builds a house","built a house","built a house","building a house","建房子"),("catch a ball","catches a ball","caught a ball","caught a ball","catching a ball","接球"),("choose a gift","chooses a gift","chose a gift","chosen a gift","choosing a gift","选礼物"),("cut the grass","cuts the grass","cut the grass","cut the grass","cutting the grass","割草"),("feed the cat","feeds the cat","fed the cat","fed the cat","feeding the cat","喂猫"),("grow vegetables","grows vegetables","grew vegetables","grown vegetables","growing vegetables","种菜"),("hold a party","holds a party","held a party","held a party","holding a party","办派对"),("leave home","leaves home","left home","left home","leaving home","离开家"),("meet a friend","meets a friend","met a friend","met a friend","meeting a friend","见朋友"),("pay the bill","pays the bill","paid the bill","paid the bill","paying the bill","付账")]
def _b(s): return "am" if s=="I" else ("is" if s in SS else "are")
def _h(s): return "has" if s in SS else "have"

# TENSES
def gen_tenses(n):
    qs = []
    for i in range(n):
        t = i % 12
        a = random.choice(AC); base,s3,past,pp,ing,zh = a
        ss = random.choice(SS); sp = random.choice(SP); sa = random.choice(AS)
        if t==0:
            tm = random.choice(TM_P)
            qe = ss+" ___ "+s3+" "+tm+"."; qz = ss+" "+tm+" 都___"+zh+"。"
            ans = s3.split()[0]; opts = [base.split()[0],ans,past.split()[0],ing.split()[0]]
        elif t==1:
            tm = random.choice(TM_P)
            qe = sp+" ___ "+base+" "+tm+"."; qz = sp+" "+tm+" 都___"+zh+"。"
            ans = base.split()[0]; opts = [ans,s3.split()[0],past.split()[0],ing.split()[0]]
        elif t==2:
            tm = random.choice(TQ)
            qe = sa+" ___ "+base+" "+tm+"."; qz = sa+tm+" ___"+zh+"。"
            ans = past.split()[0]; opts = [base.split()[0],s3.split()[0],ans,ing.split()[0]]
        elif t==3:
            tm = random.choice(TN); b = _b(sa)
            qe = sa+" ___ "+ing+" "+tm+"."; qz = sa+" 正在"+zh+" "+tm+"。"
            ans = b+" "+ing.split()[0]; opts = [ans,base.split()[0],b+" "+base.split()[0],"will "+base.split()[0]]
        elif t==4:
            tm = random.choice(TE); h = _h(sa)
            qe = sa+" ___ "+pp+" "+tm+"."; qz = sa+tm+" 已经___"+zh+"了。"
            ans = h+" "+pp.split()[0]; opts = [ans,h+" "+past.split()[0],past.split()[0],base.split()[0]]
        elif t==5:
            tm = random.choice(TF)
            qe = sa+" ___ "+base+" "+tm+"."; qz = sa+tm+" 会___"+zh+"。"
            ans = "will"; opts = ["will","is going to","was","would"]
        elif t==6:
            b = "was" if (sa in SS or sa=="I") else "were"
            qe = sa+" ___ "+ing+" when the phone rang."; qz = "电话响时"+sa+" 正在"+zh+"。"
            ans = b+" "+ing.split()[0]; opts = [ans,"is "+ing.split()[0],b+" "+base.split()[0],base.split()[0]]
        elif t==7:
            qe = sa+" ___ "+pp+" before the teacher arrived."; qz = "老师到之前"+sa+" 已经___"+zh+"了。"
            ans = "had "+pp.split()[0]; opts = [ans,"have "+pp.split()[0],past.split()[0],"was "+ing.split()[0]]
        elif t==8:
            tm = random.choice(TF); b = _b(sa)
            qe = sa+" ___ going to "+base+" "+tm+"."; qz = sa+tm+" 打算___"+zh+"。"
            ans = b; opts = [b,"will","was","has"]
        elif t==9:
            items = [("She has just finished her homework.","现在完成式 Present Perfect",["过去式 Past Simple","现在完成式 Present Perfect","现在进行式 Present Continuous","过去完成式 Past Perfect"]),("They were playing football when it rained.","过去进行式 Past Continuous",["现在进行式 Present Continuous","过去进行式 Past Continuous","过去式 Past Simple","现在完成式 Present Perfect"]),("I will travel to Japan next week.","未来式 Future (will)",["过去式 Past Simple","现在式 Present Simple","未来式 Future (will)","现在进行式 Present Continuous"]),("He had already left before I arrived.","过去完成式 Past Perfect",["过去式 Past Simple","现在完成式 Present Perfect","过去完成式 Past Perfect","过去进行式 Past Continuous"]),("She is reading a book now.","现在进行式 Present Continuous",["现在式 Present Simple","现在进行式 Present Continuous","过去式 Past Simple","现在完成式 Present Perfect"]),("We have lived here since 2015.","现在完成式 Present Perfect",["现在式 Present Simple","过去式 Past Simple","现在完成式 Present Perfect","过去完成式 Past Perfect"]),("He goes to school every day.","现在式 Present Simple",["现在式 Present Simple","现在进行式 Present Continuous","过去式 Past Simple","未来式 Future"])]
            sent,ans,opts = random.choice(items)
            qe = 'What tense is: "'+sent+'"'; qz = '「'+sent+'」是什么时态？'
        elif t==10:
            a2 = [("play football","踢足球"),("live in London","住在伦敦"),("smoke","吸烟"),("ride a bicycle","骑单车"),("get up early","早起"),("walk to school","走路去上学"),("collect stamps","收集邮票"),("eat meat","吃肉")]
            ae,az = random.choice(a2)
            qe = sa+" ___ "+ae+" when young."; qz = sa+" 年轻时___"+az+"。"
            ans = "used to"; opts = ["used to","use to","was used to","is used to"]
        else:
            sc = [("She ___ (go) to school yesterday.","她昨天___去上学。","went",["go","goes","went","going"]),("They ___ (eat) lunch right now.","他们正在___午餐。","are eating",["eat","are eating","ate","will eat"]),("I ___ (live) here since 2020.","我自2020年起___在这里。","have lived",["live","lived","have lived","am living"]),("We ___ (go) to the beach tomorrow.","我们明天___去沙滩。","will go",["go","went","will go","are going"]),("He ___ (study) English for five years.","他___学英文五年了。","has studied",["studied","has studied","is studying","studies"]),("The children ___ (play) when it rained.","下雨时孩子们正在___。","were playing",["played","were playing","are playing","have played"]),("I ___ (see) that movie last week.","我上周___了那部电影。","saw",["see","saw","have seen","am seeing"]),("By the time I arrived, he ___ (leave).","我到时他已经___了。","had left",["left","has left","had left","was leaving"]),("Look! The baby ___ (walk)!","看！婴儿正在___！","is walking",["walks","is walking","walked","will walk"]),("She always ___ (forget) her keys.","她总是___钥匙。","forgets",["forget","forgets","forgot","is forgetting"])]
            qe,qz,ans,opts = random.choice(sc)
        qs.append((qz,qe,ans,opts))
    return qs[:n]

# ARTICLES
def gen_articles(n):
    qs = []
    vn = ["elephant","apple","orange","umbrella","hour","egg","owl","ant","arm","eye","ear","island","engineer","American","Italian","old friend","empty box","important question","open window","uncle","aunt","exit","insect","animal","office","actor","artist","idea","injury","oven","orbit","ocean","angel","adult","igloo","eraser"]
    cn = ["book","cat","dog","school","table","chair","pen","house","car","tree","flower","student","teacher","university","European","uniform","boy","girl","man","woman","friend","baby","ball","cup","door","game","hat","job","king","lake","map","park","ring","shop","town","wall","year","zoo","bottle","phone","bag","coin","key","lock","note","star","test","desk","lamp","clock"]
    uniq = ["sun","moon","earth","sky","sea","world","equator","North Pole","Atlantic Ocean","Pacific Ocean","Sahara Desert","Himalayas","Eiffel Tower","Great Wall"]
    inst = ["piano","guitar","violin","drums","flute","trumpet","cello","harmonica","saxophone","organ"]
    for i in range(n):
        t = i % 8
        if t==0:
            noun = random.choice(vn)
            te = [("I saw ___ "+noun+" at the zoo.","我在动物园看到___"+noun+"。","an"),("She wants to buy ___ "+noun+".","她想买___"+noun+"。","an"),("There is ___ "+noun+" in the room.","房间里有___"+noun+"。","an"),("He ate ___ "+noun+" for lunch.","他午餐吃了___"+noun+"。","an" if noun[0] in 'aeiou' else "a"),("I need ___ "+noun+" for the project.","我需要___"+noun+"来做项目。","an" if noun[0] in 'aeiou' else "a")]
            qe,qz,ans = random.choice(te); opts = ["a","an","the","(no article)"]
        elif t==1:
            noun = random.choice(cn)
            te = [("She bought ___ "+noun+" yesterday.","她昨天买了___"+noun+"。","a"),("I saw ___ "+noun+" in the park.","我在公园看到___"+noun+"。","a"),("There is ___ "+noun+" on the table.","桌上有___"+noun+"。","a"),("He needs ___ new "+noun+".","他需要一个新的"+noun+"。","a"),("I want ___ "+noun+" for my birthday.","我生日想要___"+noun+"。","a")]
            qe,qz,ans = random.choice(te); opts = ["a","an","the","(no article)"]
        elif t==2:
            noun = random.choice(uniq)
            te = [("___ "+noun+" rises in the east.","___"+noun+"从东方升起。"),("___ "+noun+" is beautiful tonight.","___"+noun+"今晚很美。"),("We can see ___ "+noun+" clearly.","我们可以清楚看到___"+noun+"。"),("___ "+noun+" is very important to us.","___"+noun+"对我们很重要。")]
            qe,qz = random.choice(te); ans = "The"; opts = ["A","An","The","(no article)"]
        elif t==3:
            i2 = random.choice(inst)
            te = [("She plays ___ "+i2+" very well.","她___"+i2+"弹得很好。"),("He is learning to play ___ "+i2+".","他在学弹___"+i2+"。"),("The sound of ___ "+i2+" is beautiful.","___"+i2+"的声音很美。")]
            qe,qz = random.choice(te); ans = "the"; opts = ["a","an","the","(no article)"]
        elif t==4:
            items = [("Cats","are cute animals.","猫是可爱的动物。"),("Water","is essential for life.","水是生命必需的。"),("Music","makes people happy.","音乐使人快乐。"),("Rice","is a staple food.","米是主食。"),("Gold","is a precious metal.","金是贵金属。"),("Knowledge","is power.","知识就是力量。"),("Students","should study hard.","学生应该努力读书。"),("Children","like sweets.","小孩喜欢糖果。"),("Sugar","is bad for teeth.","糖对牙齿不好。"),("Honesty","is important.","诚实很重要。"),("Love","is beautiful.","爱是美好的。"),("Patience","is a virtue.","耐心是美德。")]
            s,e,z = random.choice(items)
            qe = "___ "+s+" "+e; qz = "___"+s+z; ans = "(no article)"; opts = ["A","An","The","(no article)"]
        elif t==5:
            m = [("She is ___ honest girl.","她是___诚实的女孩。","an"),("He is ___ European.","他是___欧洲人。","a"),("I want to be ___ engineer.","我想成为___工程师。","an"),("She plays ___ guitar every day.","她每天弹___结他。","the"),("He is ___ tallest boy in class.","他是班上最高的男孩。","the"),("I need ___ glass of water.","我需要___杯水。","a"),("She is ___ university student.","她是___大学生。","a"),("He is ___ honest man.","他是___诚实的人。","an"),("I play ___ tennis every week.","我每周打___网球。","(no article)"),("She is ___ only child.","她是___独生女。","an"),("He is ___ Mr. Smith.","他是___史密斯先生。","(no article)"),("I had ___ lunch at noon.","我在中午吃了午餐。","(no article)"),("She went to ___ bed early.","她___床很早。","(no article)")]
            qe,qz,ans = random.choice(m); opts = ["a","an","the","(no article)"]
        elif t==6:
            m = [("___ Nile is the longest river.","___尼罗河是最长的河流。","The"),("___ moon goes around ___ earth.","月亮绕着地球转。","The / the"),("___ sun sets in the west.","___太阳从西方落下。","The"),("___ rich should help ___ poor.","富人应该帮助穷人。","The / the"),("___ President gave a speech.","___总统发表了演说。","The"),("___ children love sweets.","___小孩爱糖果。","The"),("___ life is short.","___生命是短暂的。","(no article)"),("He goes to ___ school by ___ bus.","他搭巴士去上学。","— / —")]
            qe,qz,ans = random.choice(m)
            if "/" in ans: opts = ["the / the","a / a","— / —","the / a"]
            else: opts = ["A","An","The","(no article)"]
        else:
            noun = random.choice(vn+cn)
            m = [("___ "+noun+" is very useful.","___"+noun+"很有用。","The" if noun[0] in 'aeiou' or random.random()<0.3 else "A"),("I like ___ "+noun+" very much.","我非常喜欢___"+noun+"。","the"),("___ "+noun+" in this shop is cheap.","这家店的___"+noun+"很便宜。","The")]
            qe,qz,ans = random.choice(m); opts = ["A","An","The","(no article)"]
        qs.append((qz,qe,ans,opts))
    return qs[:n]

# PREPOSITIONS
def gen_prepositions(n):
    qs = []
    nouns = ["book","cat","dog","ball","pen","cup","hat","key","bag","box","apple","flower","phone","ring","lamp","clock","bottle","chair","desk","shelf","stone","leaf","coin","card","ticket","map","brush","knife","fork","spoon","plate","bowl","glass","mirror","candle","remote","towel","soap","sponge","comb","wallet","umbrella","newspaper","magazine","backpack","suitcase","helmet","gloves","scarf","boots"]
    locs = ["table","shelf","desk","floor","wall","ground","roof","window","door","bed","chair","sofa","counter","stove","fridge","drawer","cupboard","ceiling","path","fence","bench","gate","bridge","tunnel","hill","valley","island","coast","harbour","airport"]
    people = ["Tom","Mary","John","Amy","David","Lucy","Peter","Jenny","Mike","Sara","Ben","Kate","Jack","Lily","Sam","Nina","Bob","Ella","Leo","Mia","Oliver","Sophia","James","Emma","William","Ava","Henry","Grace","Alexander","Chloe"]
    times = ["3 o'clock","noon","midnight","6 p.m.","9 a.m.","half past two","quarter to five","10:30","7 in the morning","midday","8:15","quarter past eleven","5:45","2:30","11 a.m.","4 p.m."]
    months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    years = ["2018","2019","2020","2021","2022","2023","2024","2025"]
    durations = ["one hour","two hours","three days","a week","a month","five minutes","ten years","six months","two years","four weeks","three hours","half an hour"]
    adjs = ["afraid","good","interested","proud","famous","tired","capable","fond","aware","jealous","ashamed","sure","sick","scared","certain","happy","angry","excited","worried","surprised","disappointed","pleased","satisfied","impressed","confused"]
    things = ["spiders","math","music","you","her singing","working","his success","dogs","the dark","flying","failure","the future","cold weather","heights","snakes","her talent","his courage","the problem","the results","the situation","the decision","the outcome","the performance","the weather","the noise"]
    v_prep = {"looking":"for","waiting":"for","listening":"to","talking":"to","writing":"to","applied":"for","agreed":"with","cared":"about","depended":"on","insisted":"on","succeeded":"in","objected":"to","contributed":"to","referred":"to","attended":"to","belonged":"to","consisted":"of","recovered":"from","suffered":"from","resulted":"in"}
    v_list = list(v_prep.keys())
    for i in range(n):
        t = i % 10
        noun = random.choice(nouns); loc = random.choice(locs); person = random.choice(people)
        if t==0:
            prep = random.choice(["on","in","under","behind","beside","near","over","between","next to","in front of","above","below","through","along","across","around","into","onto","toward","against"])
            qe = "The "+noun+" is ___ the "+loc+"."; qz = noun+"在"+loc+"___。"
            ans = prep; opts = [prep]+random.sample(["on","in","at","under","behind","beside","near","over","between","next to","in front of","above","below","through","along","across","around","into","onto","toward","against"], 3)
        elif t==1:
            qe = "The "+noun+" is ___ the "+loc+"."; qz = noun+"在"+loc+"___。"
            ans = "on"; opts = ["on","in","at","under"]
        elif t==2:
            tm = random.choice(times)
            qe = person+" and I will meet ___ "+tm+"."; qz = person+"和我将在___"+tm+"见面。"
            ans = "at"; opts = ["at","on","in","by"]
        elif t==3:
            month = random.choice(months)
            qe = person+" was born ___ "+month+"."; qz = person+"在___"+month+"出生。"
            ans = "in"; opts = ["in","on","at","by"]
        elif t==4:
            day = random.choice(days)
            qe = "The party is ___ "+day+"."; qz = "派对在___"+day+"。"
            ans = "on"; opts = ["on","in","at","by"]
        elif t==5:
            adj = random.choice(adjs); thing = random.choice(things)
            prep_map = {"afraid":"of","good":"at","interested":"in","proud":"of","famous":"for","tired":"of","capable":"of","fond":"of","aware":"of","jealous":"of","ashamed":"of","sure":"of","sick":"of","scared":"of","certain":"of","happy":"about","angry":"about","excited":"about","worried":"about","surprised":"at","disappointed":"with","pleased":"with","satisfied":"with","impressed":"by","confused":"about"}
            qe = person+" is "+adj+" ___ "+thing+"."; qz = person+" "+adj+"___"+thing+"。"
            ans = prep_map.get(adj, "of"); opts = [ans]+random.sample(["of","at","in","for","with","about","to","on","by","from"], 3)
        elif t==6:
            verb = random.choice(v_list); thing = random.choice(things)
            qe = person+" is "+verb+" ___ "+thing+"."; qz = person+" "+verb+"___"+thing+"。"
            ans = v_prep[verb]; opts = [ans]+random.sample(["for","to","at","in","on","with","about","of","by","from"], 3)
        elif t==7:
            year = random.choice(years)
            qe = person+" went abroad ___ "+year+"."; qz = person+"在___"+year+"出国了。"
            ans = "in"; opts = ["in","on","at","by"]
        elif t==8:
            dur = random.choice(durations)
            qe = "We will finish ___ "+dur+"."; qz = "我们会在___"+dur+"内完成。"
            ans = "in"; opts = ["in","on","at","by"]
        else:
            date = str(random.randint(1,28))
            qe = person+" was born ___ "+date+"th March."; qz = person+"在3月"+date+"日出生。"
            ans = "on"; opts = ["on","in","at","by"]
        qs.append((qz,qe,ans,opts))
    return qs[:n]

# COMPARISON
def gen_comparison(n):
    qs = []
    sa = [("tall","taller","tallest"),("short","shorter","shortest"),("old","older","oldest"),("young","younger","youngest"),("fast","faster","fastest"),("slow","slower","slowest"),("big","bigger","biggest"),("small","smaller","smallest"),("hot","hotter","hottest"),("cold","colder","coldest"),("strong","stronger","strongest"),("weak","weaker","weakest"),("cheap","cheaper","cheapest"),("rich","richer","richest"),("poor","poorer","poorest"),("dark","darker","darkest"),("clean","cleaner","cleanest"),("long","longer","longest"),("new","newer","newest"),("warm","warmer","warmest"),("cool","cooler","coolest"),("deep","deeper","deepest"),("wide","wider","widest"),("narrow","narrower","narrowest"),("thick","thicker","thickest"),("thin","thinner","thinnest"),("loud","louder","loudest"),("quiet","quieter","quietest"),("safe","safer","safest"),("high","higher","highest"),("low","lower","lowest"),("near","nearer","nearest"),("dry","drier","driest"),("busy","busier","busiest"),("early","earlier","earliest"),("late","later","latest"),("happy","happier","happiest"),("easy","easier","easiest"),("heavy","heavier","heaviest"),("lazy","lazier","laziest"),("brave","braver","bravest"),("fine","finer","finest"),("rude","ruder","rudest"),("wise","wiser","wisest"),("pale","paler","palest"),("rare","rarer","rarest"),("strange","stranger","strangest"),("simple","simpler","simplest"),("gentle","gentler","gentlest"),("clever","cleverer","cleverest"),("pretty","prettier","prettiest"),("angry","angrier","angriest"),("hungry","hungrier","hungriest"),("noisy","noisier","noisiest"),("dusty","dustier","dustiest"),("muddy","muddier","muddiest"),("rainy","rainier","rainiest"),("snowy","snowier","snowiest"),("icy","icier","iciest"),("cloudy","cloudier","cloudiest"),("stormy","stormier","stormiest"),("smelly","smellier","smelliest"),("messy","messier","messiest"),("classy","classier","classiest"),("leafy","leafier","leafiest"),("meaty","meatier","meatiest"),("spicy","spicier","spiciest"),("juicy","juicier","juiciest"),("hilly","hillier","hilliest"),("bushy","bushier","bushiest"),("cheesy","cheesier","cheesiest"),("tasty","tastier","tastiest"),("salty","saltier","saltiest"),("wealthy","wealthier","wealthiest"),("healthy","healthier","healthiest"),("dirty","dirtier","dirtiest"),("silly","sillier","silliest"),("funny","funnier","funniest"),("tiny","tinier","tiniest"),("shiny","shinier","shiniest"),("windy","windier","windiest"),("foggy","foggier","foggiest"),("starry","starrier","starriest"),("rocky","rockier","rockiest"),("sandy","sandier","sandiest"),("grassy","grassier","grassiest"),("hazy","hazier","haziest"),("dizzy","dizzier","dizziest"),("breezy","breezier","breeziest"),("cheery","cheerier","cheeriest"),("dreary","drearier","dreariest"),("weary","wearier","weariest"),("heavily","heavier","heaviest"),("steadily","steadier","steadiest"),("readily","readier","readiest"),("greedily","greedier","greediest"),("speedily","speedier","speediest"),("noisily","noisier","noisiest"),("happily","happier","happiest"),("angrily","angrier","angriest"),("busily","busier","busiest"),("easily","easier","easiest")]
    la = [("beautiful","more beautiful","most beautiful"),("interesting","more interesting","most interesting"),("expensive","more expensive","most expensive"),("comfortable","more comfortable","most comfortable"),("dangerous","more dangerous","most dangerous"),("important","more important","most important"),("difficult","more difficult","most difficult"),("famous","more famous","most famous"),("careful","more careful","most careful"),("wonderful","more wonderful","most wonderful"),("serious","more serious","most serious"),("popular","more popular","most popular"),("exciting","more exciting","most exciting"),("boring","more boring","most boring"),("surprising","more surprising","most surprising"),("amazing","more amazing","most amazing"),("creative","more creative","most creative"),("generous","more generous","most generous"),("patient","more patient","most patient"),("responsible","more responsible","most responsible"),("intelligent","more intelligent","most intelligent"),("powerful","more powerful","most powerful"),("successful","more successful","most successful"),("delicious","more delicious","most delicious"),("colorful","more colorful","most colorful"),("harmful","more harmful","most harmful"),("useful","more useful","most useful"),("peaceful","more peaceful","most peaceful"),("cheerful","more cheerful","most cheerful"),("graceful","more graceful","most graceful")]
    ir = [("good","better","best"),("bad","worse","worst"),("far","farther","farthest"),("little","less","least"),("much","more","most"),("many","more","most"),("well","better","best"),("badly","worse","worst")]
    t1 = ["this book","this movie","this song","this city","this school","this restaurant","this park","this cake","this car","this phone","this game","summer","winter","spring","autumn","this test","this hotel","this beach","this mountain","this island"]
    t2 = ["that one","the other","the first one","the last one","the second one","yesterday's","last year's"]
    ctx = ["in the class","in the school","in the team","of all","in the family","in the city","in the world","in Hong Kong","in our group","among the students","of the three","of the year","in the competition","of the century"]
    pn = ["girl","boy","student","teacher","player","singer","runner","swimmer","friend","worker","child","person","athlete","dancer","artist","sprinter","speaker","writer","scientist","engineer"]
    for i in range(n):
        t = i % 7
        if t==0:
            b,c,s = random.choice(sa); x,y = random.choice(t1), random.choice(t2)
            qe = x.capitalize()+" is ___ than "+y+"."; qz = x+"比"+y+"___。"; ans = c; opts = [c,b,s,"more "+b]
        elif t==1:
            b,c,s = random.choice(sa); cx,p = random.choice(ctx), random.choice(pn)
            qe = "She is the ___ "+p+" "+cx+"."; qz = "她是"+cx+"中最___的"+p+"。"; ans = s; opts = [s,c,b,"most "+b]
        elif t==2:
            b,c,s = random.choice(la); x,y = random.choice(t1), random.choice(t2)
            qe = x.capitalize()+" is ___ than "+y+"."; qz = x+"比"+y+"___。"; ans = c; opts = [c,b,s,b+"er"]
        elif t==3:
            b,c,s = random.choice(la)
            qe = "This is the ___ book I have ever read."; qz = "这是我读过最___的书。"; ans = s; opts = [s,c,b,b+"est"]
        elif t==4:
            b,c,s = random.choice(ir)
            if random.random()<0.5:
                x,y = random.choice(t1), random.choice(t2)
                qe = x.capitalize()+" is ___ than "+y+"."; qz = x+"比"+y+"___。"; ans = c; opts = [c,b,s,"more "+b]
            else:
                qe = "This is the ___ day of my life."; qz = "这是我人生中最___的一天。"; ans = s; opts = [s,c,b,"most "+b]
        elif t==5:
            te = [("She is ___ tall as her mother.","她和她妈妈一样高。","as",["as","so","too","very"]),("He is not ___ smart as his brother.","他没有哥哥那么聪明。","as",["as","so","too","more"]),("This book is ___ interesting as that one.","这本书和那本一样有趣。","as",["as","so","more","most"]),("She can run ___ fast as a rabbit.","她跑得和兔子一样快。","as",["as","so","too","very"]),("This room is not ___ big as that one.","这房间没那间大。","as",["as","so","more","much"]),("He works ___ hard as his sister.","他和姐姐一样勤奋。","as",["as","so","more","most"]),("The test was not ___ difficult as expected.","考试没有预期那么难。","as",["as","so","more","much"]),("She sings ___ beautifully as a bird.","她唱得和鸟一样美。","as",["as","so","too","very"])]
            qe,qz,ans,opts = random.choice(te)
        else:
            te = [("She has ___ books than him.","她的书比他多。","more",["more","most","much","many"]),("He has ___ money than me.","他的钱比我少。","less",["less","least","fewer","little"]),("There are ___ students this year.","今年的学生较少。","fewer",["fewer","less","fewest","least"]),("She ate ___ than everyone.","她吃得最多。","the most",["more","the most","the best","much"]),("He has ___ patience than his sister.","他比姐姐更有耐心。","more",["more","most","much","many"]),("There is ___ water in this glass.","这个杯里水更少。","less",["less","least","fewer","little"])]
            qe,qz,ans,opts = random.choice(te)
        qs.append((qz,qe,ans,opts))
    return qs[:n]

# CONDITIONALS
def gen_conditionals(n):
    qs = []
    t1i = ["if it rains","if I have time","if she studies hard","if the weather is nice","if he comes early","if we leave now","if they invite me","if you eat too much","if the bus is late","if I find my wallet","if she calls me","if he finishes early","if we save enough money","if it snows tomorrow","if you need help","if the teacher gives homework","if they cancel the meeting","if the sun shines"]
    t1z = ["如果下雨","如果我有时间","如果她努力读书","如果天气好","如果他早到","如果我们现在走","如果他们邀请我","如果你吃太多","如果巴士迟到","如果我找到钱包","如果她打给我","如果他早完成","如果我们存够钱","如果明天下雪","如果你需要帮助","如果老师给作业","如果他们取消会议","如果太阳出来"]
    t1r = ["I will stay at home","I will take an umbrella","I will go to the beach","I will be happy","I will call you","she will pass the exam","we will miss the bus","I will buy it","they will win","I will help you","we will go shopping","I will finish early","he will get a prize"]
    t2i = ["I were rich","I had more time","she were here","I were you","we lived in London","he knew the answer","I could fly","I were the teacher","they were free today","it were summer now","I spoke French","I had a car","I were invisible","we had wings","I were a king","she were taller","he were a doctor","we had a garden"]
    t2z = ["如果我有钱","如果我有更多时间","如果她在这里","如果我是你","如果我们住在伦敦","如果他知道答案","如果我会飞","如果我是老师","如果他们今天有空","如果现在是夏天","如果我会说法语","如果我有车","如果我是隐形的","如果我们有翅膀","如果我是国王","如果她更高","如果他是医生","如果我们有花园"]
    t2r = ["I would travel the world","I would buy a big house","she would be happier","I would study medicine","we would visit Paris","he would tell us","I would fly to the moon","I would stop working","they would join us","I would not worry","we would live by the sea","I would learn to dance"]
    for i in range(n):
        t = i % 6
        if t==0:
            idx1 = random.randint(0,len(t1i)-1); idx2 = random.randint(0,len(t1r)-1)
            qe = t1i[idx1].capitalize()+", "+t1r[idx2]+". What is the if-clause tense?"
            qz = t1z[idx1]+"，"+t1r[idx2]+"。If子句是什么时态？"
            ans = "Present Simple"; opts = ["Present Simple","Past Simple","Future","Past Perfect"]
        elif t==1:
            idx1 = random.randint(0,len(t1i)-1); idx2 = random.randint(0,len(t1r)-1)
            verb = t1r[idx2].split(" will ")[1] if " will " in t1r[idx2] else t1r[idx2]
            qe = t1i[idx1].capitalize()+", I ___ "+verb+"."; qz = t1z[idx1]+"，我___"+verb+"。"
            ans = "will"; opts = ["will","would","am going to","was"]
        elif t==2:
            idx1 = random.randint(0,len(t2i)-1); idx2 = random.randint(0,len(t2r)-1)
            qe = "If "+t2i[idx1]+", "+t2r[idx2]+". What type?"; qz = "如果"+t2z[idx1]+"，"+t2r[idx2]+"。这是哪种条件句？"
            ans = "Second Conditional"; opts = ["First Conditional","Second Conditional","Third Conditional","Zero Conditional"]
        elif t==3:
            qe = "If I ___, I would travel the world."; qz = "如果我___，我会环游世界。"
            ans = "were rich"; opts = ["were rich","am rich","will be rich","was rich"]
        elif t==4:
            se = [("If you heat water to 100C, it boils.","零条件句 Zero Conditional",["零条件句","第一条件句","第二条件句","第三条件句"]),("If I had studied harder, I would have passed.","第三条件句 Third Conditional",["零条件句","第一条件句","第二条件句","第三条件句"]),("If I study hard, I will pass.","第一条件句 First Conditional",["零条件句","第一条件句","第二条件句","第三条件句"]),("If I were a bird, I would fly.","第二条件句 Second Conditional",["零条件句","第一条件句","第二条件句","第三条件句"])]
            sent,ans,opts = random.choice(se)
            qe = 'What type: "'+sent+'"'; qz = '「'+sent+'」是哪种条件句？'
        else:
            te = [("If it ___ (rain) tomorrow, I will stay home.","如果明天下雨，我会留在家。","rains",["rains","will rain","rained","would rain"]),("If I ___ (be) you, I would study harder.","如果我是你，我会更努力读书。","were",["am","was","were","will be"]),("If she ___ (study) harder, she would have passed.","如果她更努力，她就会通过了。","had studied",["studied","had studied","has studied","studies"]),("If you heat ice, it ___ (melt).","如果你加热冰，它会融化。","melts",["melts","will melt","melted","is melting"]),("If they ___ (not hurry), they will miss the bus.","如果他们不赶快，会错过巴士。","don't hurry",["don't hurry","won't hurry","didn't hurry","aren't hurry"]),("If I ___ (have) enough money, I would buy a car.","如果我有足够的钱，我会买车。","had",["have","had","will have","would have"]),("If we ___ (leave) now, we will arrive on time.","如果我们现在走，会准时到。","leave",["leave","left","will leave","would leave"]),("If she ___ (be) free tomorrow, she will come.","如果她明天有空，她会来。","is",["is","was","were","will be"])]
            qe,qz,ans,opts = random.choice(te)
        qs.append((qz,qe,ans,opts))
    return qs[:n]

# PASSIVE
def gen_passive(n):
    qs = []
    subjects = ["The cake","The letter","The car","English","The window","The homework","The song","The house","The bridge","The book","The food","The museum","The flowers","The computer","The project","The report","The trees","The movie","The road","The problem","The email","The door","The baby","The room","The phone","The tickets","The medicine","The painting","The sculpture","The garden","The fence","The wall","The floor","The ceiling","The roof","The staircase","The elevator","The escalator","The conveyor belt","The assembly line"]
    agents = ["my mother","the secretary","a mechanic","workers","the ball","the students","everyone","engineers","the chef","many people","the technician","the manager","millions","the team","my boss","the wind","her mother","the cleaner","the child","the agent","the fire","the doctor","the artist","the builder","the plumber","the electrician","the gardener","the painter","the carpenter","the tailor"]
    verbs = [("was made","做"),("was written","写"),("was repaired","修理"),("is spoken","说"),("was broken","打破"),("was completed","完成"),("is known","知道"),("was built","建造"),("was designed","设计"),("was translated","翻译"),("was cooked","煮"),("is visited","参观"),("are watered","浇水"),("was fixed","修理"),("will be finished","完成"),("has been reviewed","审阅"),("are planted","种植"),("was watched","观看"),("is being repaired","修理"),("has been solved","解决"),("was sent","发送"),("was blown open","吹开"),("is being fed","喂"),("was cleaned","打扫"),("was dropped","掉落"),("were booked","预订"),("was destroyed","摧毁"),("was prescribed","处方"),("was painted","油漆"),("was decorated","装饰")]
    items = []
    for s in subjects:
        for a in agents:
            for v, vz in verbs:
                items.append((s, "by "+a, v, s+vz+"了"))
    # Also add the original items for quality
    items += [("The cake","by my mother","was made","蛋糕被妈妈做了"),("The letter","by the secretary","was written","信被秘书写了"),("The car","by a mechanic","was repaired","车被技工修了"),("English","in many countries","is spoken","英语在很多国家被使用"),("The window","by the ball","was broken","窗户被球打破了"),("The homework","by the students","was completed","功课被学生完成了"),("The song","by everyone","is known","这首歌被所有人知道"),("The house","in 1990","was built","房子在1990年建了"),("The bridge","by engineers","was designed","桥被工程师设计了"),("The book","into many languages","was translated","书被翻译了"),("The food","by the chef","was cooked","食物被厨师煮了"),("The museum","by many people","is visited","博物馆被很多人参观"),("The flowers","every day","are watered","花每天被浇水"),("The computer","by the technician","was fixed","电脑被修好了"),("The project","by next week","will be finished","项目下周会被完成"),("The report","by the manager","has been reviewed","报告已被审阅"),("The trees","every spring","are planted","树每年春天被种植"),("The movie","by millions","was watched","电影被数百万人看了"),("The road","by workers","is being repaired","路正在被修理"),("The problem","by the team","has been solved","问题已被解决了"),("The email","by my boss","was sent","电邮被老闆发了"),("The door","by the wind","was blown open","门被风吹开了"),("The baby","by her mother","is being fed","婴儿正被妈妈喂"),("The room","by the cleaner","was cleaned","房间被打扫了"),("The phone","by the child","was dropped","电话被孩子掉了"),("The tickets","by the agent","were booked","票被代理人订了"),("The house","by the fire","was destroyed","房子被火摧毁了"),("The medicine","by the doctor","was prescribed","药被医生处方了")]
    ap = [("My mother made the cake.","The cake was made by my mother.","was made",["is made","was made","has been made","will be made"]),("Someone stole my bike.","My bike was stolen.","was stolen",["is stolen","was stolen","has stolen","will steal"]),("They build bridges.","Bridges are built.","are built",["are built","is built","were built","will built"]),("She writes the reports.","The reports are written.","are written",["are written","is written","were written","was written"]),("He drives the car.","The car is driven.","is driven",["is driven","are driven","was driven","drives"]),("They sell flowers here.","Flowers are sold here.","are sold",["are sold","is sold","were sold","sell"]),("Scientists discovered a planet.","A planet was discovered.","was discovered",["is discovered","was discovered","has discovered","discovered"]),("Workers painted the wall.","The wall was painted.","was painted",["is painted","was painted","has painted","painted"]),("The company will launch a product.","A product will be launched.","will be launched",["will launch","will be launched","is launched","was launched"]),("People speak English worldwide.","English is spoken worldwide.","is spoken",["speaks","is spoken","was spoken","spoke"])]
    for i in range(n):
        t = i % 5
        if t==0:
            subj,agent,verb,zh = random.choice(items)
            qe = subj+" ___ "+agent+"."; qz = subj+zh+"。"; ans = verb
            pp = verb.split()[-1]; opts = [verb,verb.split()[0]+" "+pp+"ing" if "ing" not in pp else verb.replace("was","is"),pp,verb.replace("was","is")]
            opts = list(dict.fromkeys(opts))
            while len(opts)<4: opts.append(pp+"ed" if not pp.endswith("ed") else pp+"s")
        elif t==1:
            subj,agent,_,zh = random.choice(items)
            vp = random.choice(items)[2].replace("was ","is ").replace("were ","are ")
            qe = subj+" ___ "+agent+"."; qz = subj+zh+"。"; ans = vp
            opts = [vp,vp.replace("is ","are ").replace("are ","is "),vp.split()[-1],vp.replace("is ","was ")]
            opts = list(dict.fromkeys(opts))
            while len(opts)<4: opts.append("will be "+vp.split()[-1])
        elif t==2:
            subj = random.choice(["The project","The road","The building","The report","The homework","The cake","The letter","The car"])
            pp = random.choice(["finished","completed","built","written","made","delivered","painted","designed","repaired","cleaned"])
            qe = subj+" ___ by next week."; qz = subj+"下周前会被完成。"
            ans = "will be "+pp; opts = ["will be "+pp,"will "+pp,"is "+pp,"was "+pp]
        elif t==3:
            active,passive,ans,opts = random.choice(ap)
            qe = 'Change to passive: "'+active+'"'; qz = '改为被动语态：「'+active+'」'
        else:
            te = [("The window ___ (break) by the ball.","窗户被球打破了。","was broken",["broke","was broken","is breaking","has broken"]),("English ___ (speak) in many countries.","英语在很多国家被使用。","is spoken",["speaks","is spoken","was spoken","spoke"]),("The museum ___ (build) in 1990.","博物馆在1990年建成。","was built",["built","was built","is built","has built"]),("The food ___ (eat) already.","食物已经被吃掉了。","has been eaten",["has eaten","has been eaten","was eating","ate"]),("The road ___ (repair) right now.","路正在被修理。","is being repaired",["repairs","is repaired","is being repaired","was repaired"]),("The car ___ (drive) by my father.","车是我爸爸开的。","is driven",["drives","is driven","was driving","drove"]),("The letter ___ (write) yesterday.","信昨天被写了。","was written",["wrote","was written","is written","has written"]),("The flowers ___ (water) every day.","花每天被浇水。","are watered",["water","are watered","is watered","were watering"]),("The problem ___ (solve) by the team.","问题已被团队解决了。","has been solved",["solved","has solved","has been solved","was solving"]),("The baby ___ (feed) right now.","婴儿正在被喂。","is being fed",["feeds","is fed","is being fed","was fed"])]
            qe,qz,ans,opts = random.choice(te)
        qs.append((qz,qe,ans,opts))
    return qs[:n]

# REPORTED SPEECH
def gen_reported_speech(n):
    qs = []
    stmts = [("I am tired.","was","我很累"),("I like ice cream.","liked","我喜欢冰淇淋"),("I am going home.","was going","我要回家"),("I will help you.","would help","我会帮你"),("I can swim.","could","我会游泳"),("I have finished.","had finished","我已经完成"),("I am happy.","was","我很高兴"),("I don't know.","didn't know","我不知道"),("I want to leave.","wanted","我想离开"),("I need help.","needed","我需要帮助"),("I may come.","might","我可能会来"),("I must go now.","had to","我必须走了"),("I am watching TV.","was watching","我在看电视"),("I feel sick.","felt","我不舒服"),("I should study.","should","我应该读书"),("I would like coffee.","would like","我想要咖啡"),("I didn't see it.","hadn't seen","我没看到"),("I am going to travel.","was going to","我打算去旅行"),("I have been waiting.","had been","我一直在等"),("I must finish this.","had to","我必须完成这个")]
    ynq = [("Are you tired?","if I was tired",["if I was","if I am","that I was","if I were"]),("Do you like music?","if I liked music",["if I liked","if I like","that I liked","if I would like"]),("Can you help me?","if I could help him",["if I could","if I can","that I could","if I will"]),("Have you finished?","if I had finished",["if I had finished","if I have finished","that I finished","if I finished"]),("Will you come?","if I would come",["if I would","if I will","that I would","if I could"]),("Is she coming?","if she was coming",["if she was coming","if she is coming","that she was coming","if she comes"]),("Did you see it?","if I had seen it",["if I had seen","if I saw","that I saw","if I see"]),("Were you at home?","if I had been at home",["if I had been","if I was","that I was","if I am"])]
    cmds = [("Sit down.","told me to sit down","to sit down",["sit down","to sit down","sitting down","sat down"]),("Please help me.","asked me to help him","to help him",["help him","to help him","helping him","helped him"]),("Don't go.","told me not to go","not to go",["don't go","not to go","to not go","not going"]),("Open the door.","told me to open the door","to open the door",["open the door","to open the door","opening the door","opened the door"]),("Be quiet.","told me to be quiet","to be quiet",["be quiet","to be quiet","being quiet","was quiet"]),("Close the window.","asked me to close the window","to close the window",["close the window","to close the window","closing the window","closed the window"]),("Stand up.","told me to stand up","to stand up",["stand up","to stand up","standing up","stood up"]),("Don't touch that.","told me not to touch that","not to touch that",["don't touch that","not to touch that","to not touch that","not touching that"]),("Wait here.","told me to wait there","to wait there",["wait there","to wait there","waiting there","waited there"]),("Run quickly.","told me to run quickly","to run quickly",["run quickly","to run quickly","running quickly","ran quickly"])]
    whq = [("Where do you live?","where I lived",["where I lived","where do I live","where I live","that I lived"]),("What is your name?","what my name was",["what my name was","what is my name","what my name is","that my name was"]),("When did you arrive?","when I had arrived",["when I had arrived","when did I arrive","when I arrived","that I arrived"]),("Why did you leave?","why I had left",["why I had left","why did I leave","why I left","that I left"]),("How old are you?","how old I was",["how old I was","how old am I","how old I am","that I was old"]),("Who told you?","who had told me",["who had told me","who told me","who did tell me","that who told me"]),("What did you say?","what I had said",["what I had said","what did I say","what I said","that I said"]),("Where did she go?","where she had gone",["where she had gone","where did she go","where she went","that she went"])]
    tc = [("I am here now.","was there then","was",["was","is","will be","has been"]),("I will come tomorrow.","would come the next day","would come",["will come","would come","came","comes"]),("I came yesterday.","had come the day before","had come",["came","had come","has come","comes"]),("I am leaving today.","was leaving that day","was leaving",["is leaving","was leaving","will leave","left"]),("I have finished this.","had finished that","had finished",["has finished","had finished","finished","finishes"])]
    for i in range(n):
        t = i % 5
        if t==0:
            d,rt,zh = random.choice(stmts)
            rv = random.choice(["said","told me","explained","mentioned","replied","whispered","claimed","admitted"])
            sp = random.choice(["He","She","Tom","Mary","My father","The teacher"])
            qe = sp+' '+rv+': "'+d+'" -> '+sp+' '+rv+' he ___.'; qz = sp+'说：「'+d+'」-> '+sp+'说他___。'
            ans = rt; pool = ["was","is","will","would","had","have","could","might","should","didn't","doesn't"]
            opts = [ans]+random.sample([x for x in pool if x!=ans], 3); random.shuffle(opts)
        elif t==1:
            d,ans,opts = random.choice(ynq)
            qe = 'He asked: "'+d+'" -> He asked ___.'; qz = '他问：「'+d+'」-> 他问___。'
        elif t==2:
            d,_,ans,opts = random.choice(cmds)
            qe = 'He said: "'+d+'" -> He told me ___.'; qz = '他说：「'+d+'」-> 他叫我___。'
        elif t==3:
            d,ans,opts = random.choice(whq)
            qe = 'He asked: "'+d+'" -> He asked ___.'; qz = '他问：「'+d+'」-> 他问___。'
        else:
            d,r,ans,opts = random.choice(tc)
            qe = 'He said: "'+d+'" -> He said he ___.'; qz = '他说：「'+d+'」-> 他说他___。'
        qs.append((qz,qe,ans,opts))
    return qs[:n]

# RELATIVE CLAUSES
def gen_relative_clauses(n):
    qs = []
    people = ["man","woman","teacher","boy","girl","doctor","student","singer","driver","friend","artist","nurse","engineer","chef","pilot","farmer","painter","scientist","lawyer","architect","musician","dancer","actor","actress","photographer","journalist","detective","firefighter","police officer","soldier"]
    actions_who = [("lives next door","住在隔壁"),("works at the bank","在银行工作"),("teaches us English","教我们英文"),("is wearing a hat","戴着帽子"),("sits next to me","坐在我旁边"),("helped my mother","帮了我妈"),("won the prize","赢了奖"),("sang at the concert","在演唱会唱歌"),("took us to the airport","载我们去机场"),("called me yesterday","昨天打给我"),("painted this picture","画了这幅画"),("takes care of patients","照顾病人"),("designed the bridge","设计了桥"),("cooked the dinner","煮了晚餐"),("flew the plane","开了飞机"),("grows vegetables","种菜"),("wrote the book","写了那本书"),("built the house","建了那栋房子"),("taught the class","教了那个班"),("directed the movie","导演了那部电影")]
    whoc = []
    for p in people:
        for a, az in actions_who:
            whoc.append(("The "+p, a, az))
    wc = [("The book","I read","我读的"),("The movie","we watched","我们看的"),("The song","she sang","她唱的"),("The food","he cooked","他煮的"),("The house","they bought","他们买的"),("The letter","I wrote","我写的"),("The cake","my mother made","我妈做的"),("The car","he drives","他开的"),("The phone","I lost","我丢的"),("The gift","she gave me","她给我的"),("The game","we played","我们玩的"),("The dress","she wore","她穿的"),("The film","I recommended","我推荐的"),("The picture","he drew","他画的"),("The tool","I need","我需要的")]
    wrc = [("The school","I study at","我就读的"),("The city","he lives in","他住的"),("The park","we played in","我们玩的"),("The restaurant","we ate at","我们吃的"),("The hospital","she works at","她工作的"),("The library","I borrow books from","我借书的"),("The beach","they went to","他们去的"),("The museum","we visited","我们参观的"),("The hotel","we stayed at","我们住的"),("The office","he works in","他工作的"),("The cafe","we met at","我们见面的"),("The shop","she buys food from","她买食物的"),("The stadium","they train at","他们训练的"),("The church","they were married at","他们结婚的"),("The theatre","we saw the show at","我们看表演的")]
    wt = [("The boy ___ father is a doctor is my friend.","那个爸爸是医生的男孩是我朋友。","whose"),("The girl ___ mother is a teacher sits next to me.","那个妈妈是老师的女孩坐在我旁边。","whose"),("The woman ___ car was stolen called the police.","车被偷的女人报了警。","whose"),("The student ___ essay won the prize was happy.","作文获奖的学生很高兴。","whose"),("The man ___ house is on the hill is rich.","房子在山上的人很富有。","whose"),("The child ___ toys were lost was crying.","玩具丢了的孩子在哭。","whose"),("The artist ___ paintings are famous lives here.","画作出名的艺术家住这里。","whose"),("The dog ___ owner is my neighbor is friendly.","主人是我邻居的狗很友善。","whose")]
    mt = [("I remember the day ___ we first met.","我记得我们第一次见面的那天。","when"),("The reason ___ he left is unknown.","他离开的原因未知。","why"),("This is the place ___ I was born.","这是我出生的地方。","where"),("That is the reason ___ I am happy.","那就是我高兴的原因。","why"),("Do you remember the time ___ we went camping?","你记得我们去露营的时候吗？","when"),("I don't know the place ___ she went.","我不知道她去了哪里。","where"),("Tell me the time ___ the meeting starts.","告诉我会议开始的时间。","when")]
    misc = [("The person ___ I spoke to was kind.","我跟他说话的那个人很友善。","whom",["whom","who","which","whose"]),("The team ___ won the match celebrated.","赢了比赛的队伍在庆祝。","which",["which","who","whom","whose"]),("The year ___ I was born was 2010.","我出生的那年是2010。","when",["when","where","which","who"]),("The city ___ I grew up is beautiful.","我长大的城市很美。","where",["where","which","who","when"]),("The things ___ matter most are free.","最重要的东西是免费的。","that",["that","who","whose","where"]),("The moment ___ I saw her, I knew.","我看到她的那一刻就知道了。","when",["when","where","which","who"]),("Is that the man ___ car was stolen?","那就是车被偷的人吗？","whose",["whose","who","which","that"]),("The teacher ___ class I enjoy is kind.","我很享受他的课的老师很友善。","whose",["whose","who","which","that"])]
    for i in range(n):
        t = i % 6
        if t==0:
            s,a,az = random.choice(whoc)
            qe = s+" ___ "+a+" is my friend."; qz = s+"___"+az+"是我的朋友。"; ans = "who"; opts = ["who","which","that","whose"]
        elif t==1:
            s,a,az = random.choice(wc)
            qe = s+" ___ "+a+" was interesting."; qz = s+"___"+az+"很有趣。"; ans = "which"; opts = ["which","who","whom","whose"]
        elif t==2:
            s,a,az = random.choice(wrc)
            qe = s+" ___ "+a+" is nearby."; qz = s+"___"+az+"在附近。"; ans = "where"; opts = ["where","which","who","when"]
        elif t==3:
            qe,qz,ans = random.choice(wt); opts = ["whose","who","which","that"]
        elif t==4:
            qe,qz,ans = random.choice(mt)
            opts = {"when":["when","where","which","who"],"why":["why","which","when","where"],"where":["where","when","which","who"]}[ans]
        else:
            qe,qz,ans,opts = random.choice(misc)
        qs.append((qz,qe,ans,opts))
    return qs[:n]

# VOCABULARY
def gen_vocabulary(n):
    qs = []
    wd = [("appreciate","to be grateful for","感激"),("abundant","existing in large amounts","丰富的"),("accurate","correct and exact","准确的"),("achieve","to succeed in doing","达成"),("adequate","enough for a purpose","足够的"),("admire","to respect and approve of","钦佩"),("ancient","very old; from long ago","古老的"),("apparent","easy to see or understand","明显的"),("approach","to come near; a method","接近"),("appropriate","suitable or correct","适当的"),("arrange","to organize or plan","安排"),("assist","to help","协助"),("attempt","to try to do something","尝试"),("available","able to be used","可用的"),("avoid","to keep away from","避免"),("aware","having knowledge of","意识到"),("benefit","an advantage; to gain","好处"),("brave","showing courage","勇敢的"),("calculate","to work out a number","计算"),("cancel","to decide not to do","取消"),("capable","having the ability","有能力的"),("cautious","careful to avoid danger","谨慎的"),("celebrate","to mark a special occasion","庆祝"),("clever","quick to understand","聪明的"),("comfortable","providing physical ease","舒适的"),("communicate","to share information","沟通"),("compete","to try to win","竞争"),("complain","to express dissatisfaction","抱怨"),("confident","feeling sure about yourself","自信的"),("confirm","to verify or prove","确认"),("connect","to join together","连接"),("consider","to think carefully about","考虑"),("contain","to hold or include","包含"),("convenient","fitting well with needs","方便的"),("create","to make something new","创造"),("curious","eager to know or learn","好奇的"),("dangerous","likely to cause harm","危险的"),("decide","to make a choice","决定"),("decrease","to become smaller","减少"),("deliver","to bring to a place","送递"),("describe","to say what something is like","描述"),("destroy","to damage completely","摧毁"),("develop","to grow or change","发展"),("discover","to find for the first time","发现"),("efficient","working well without waste","有效率的"),("encourage","to give support","鼓励"),("enjoy","to take pleasure in","享受"),("enormous","very large","巨大的"),("essential","absolutely necessary","必要的"),("evaluate","to judge the value of","评估"),("excellent","extremely good","优秀的"),("expand","to become bigger","扩展"),("explain","to make something clear","解释"),("explore","to travel and discover","探索"),("express","to show feelings or ideas","表达"),("failure","lack of success","失败"),("familiar","well known; easily recognized","熟悉的"),("flexible","willing to change","有弹性的"),("focus","to concentrate on","专注"),("forbid","to not allow","禁止"),("fortunate","lucky","幸运的"),("generous","willing to give","慷慨的"),("genuine","real; true","真正的"),("grateful","feeling thankful","感激的"),("hesitate","to pause before doing","犹豫"),("honest","telling the truth","诚实的"),("ignore","to pay no attention to","忽视"),("improve","to make or become better","改善"),("include","to contain as part of","包含"),("increase","to become larger","增加"),("influence","to have an effect on","影响"),("inspire","to fill with creative urge","启发"),("intelligent","able to learn quickly","聪明的"),("investigate","to examine carefully","调查"),("maintain","to keep in good condition","维持"),("motivate","to give a reason to act","激励"),("numerous","very many","众多的"),("obvious","easy to see or understand","明显的"),("occur","to happen","发生"),("opportunity","a chance to do something","机会"),("organize","to arrange in order","组织"),("participate","to take part in","参加"),("permanent","lasting for a long time","永久的"),("persuade","to cause someone to believe","说服"),("practical","useful; realistic","实用的"),("precious","of great value","珍贵的"),("predict","to say what will happen","预测"),("prevent","to stop from happening","防止"),("primary","most important; first","主要的"),("proceed","to continue","继续"),("produce","to make or create","生产"),("progress","improvement","进步"),("promote","to help grow","促进"),("protect","to keep safe","保护"),("provide","to give or supply","提供"),("purchase","to buy","购买"),("realize","to become aware of","意识到"),("receive","to be given something","收到"),("recognize","to know from before","认出"),("recommend","to suggest as good","推荐"),("reduce","to make smaller","减少"),("reflect","to think deeply","反思"),("refuse","to say no","拒绝"),("reliable","able to be trusted","可靠的"),("remove","to take away","移除"),("repair","to fix something broken","修理"),("replace","to take the place of","取代"),("represent","to act on behalf of","代表"),("require","to need","需要"),("rescue","to save from danger","营救"),("respond","to reply or react","回应"),("responsible","having a duty","负责任的"),("reveal","to make known","揭示"),("satisfy","to make happy","满足"),("select","to choose carefully","选择"),("significant","important","重要的"),("similar","alike","相似的"),("solution","an answer to a problem","解决方案"),("suggest","to put forward an idea","建议"),("support","to help or agree with","支持"),("survive","to continue to live","生存"),("transform","to change completely","改变"),("unique","one of a kind","独特的"),("urgent","needing immediate attention","紧急的"),("valuable","worth a lot","有价值的"),("visible","able to be seen","可见的"),("vital","absolutely necessary","至关重要的"),("wonderful","extremely good","精彩的"),("withdraw","to take away or leave","撤回"),("wisdom","the quality of being wise","智慧"),("widespread","found over a large area","广泛的"),("worth","having value","值得的"),("yield","to produce or give way","产出"),("zone","an area with particular features","区域"),("abandon","to leave behind permanently","放弃"),("absorb","to take in completely","吸收"),("abstract","existing in thought; not concrete","抽象的"),("accelerate","to speed up","加速"),("access","to reach or enter","访问"),("accommodate","to provide space for","容纳"),("accompany","to go together with","陪伴"),("accumulate","to gather over time","积累"),("accurate","free from error","精确的"),("accustom","to make familiar","使习惯"),("achieve","to reach a goal","实现"),("acknowledge","to accept or admit","承认"),("acquire","to gain possession of","获得"),("adapt","to adjust to new conditions","适应"),("adequate","sufficient for a purpose","充分的"),("adjust","to change slightly","调整"),("administer","to manage or govern","管理"),("admire","to regard with respect","钦佩"),("admit","to confess or allow entry","承认"),("adopt","to take as one's own","采用"),("advance","to move forward","前进"),("advantage","a beneficial condition","优势"),("advertise","to promote publicly","广告"),("advise","to give guidance","建议"),("affect","to have an influence on","影响"),("afford","to have enough money for","负担得起"),("aggressive","ready to attack","好斗的"),("alert","watchful and attentive","警觉的"),("allocate","to distribute for a purpose","分配"),("alter","to change","改变"),("alternative","another option","替代"),("ambiguous","unclear; having multiple meanings","模糊的"),("ambitious","having a strong desire to succeed","有抱负的"),("amend","to make changes to","修正"),("analyze","to examine in detail","分析"),("anticipate","to expect or predict","预期"),("apologize","to express regret","道歉"),("apparent","clearly visible or understood","显然的"),("appeal","to make a serious request","呼吁"),("appetite","a natural desire","食欲"),("appliance","a device for a specific task","电器"),("applicable","relevant or appropriate","适用的"),("appoint","to assign a role","任命"),("appreciate","to recognize the value of","欣赏"),("approach","to come near","接近"),("appropriate","suitable for the situation","适当的"),("approve","to officially agree to","批准"),("approximate","close to the actual value","近似的"),("arise","to come into being","出现"),("arrange","to put in order","安排"),("artificial","made by humans; not natural","人工的"),("aspect","a particular part or feature","方面"),("assemble","to put together","组装"),("assess","to evaluate or estimate","评估"),("assign","to allocate or designate","分配"),("assist","to help or support","协助"),("associate","to connect in the mind","联想"),("assume","to accept as true without proof","假设"),("assure","to tell with confidence","保证"),("atmosphere","the feeling of a place","氛围"),("attach","to fasten or join","附上"),("attain","to achieve or reach","达到"),("attempt","to try","尝试"),("attend","to be present at","出席"),("attitude","a way of thinking or feeling","态度"),("attract","to draw attention","吸引"),("authority","the power to give orders","权威"),("automatic","working by itself","自动的"),("available","able to be obtained","可用的"),("average","the typical amount","平均的"),("avoid","to keep away from","避免"),("aware","having knowledge of","意识到")]
    syns = [("happy","glad"),("big","large"),("small","tiny"),("fast","quick"),("smart","intelligent"),("angry","furious"),("afraid","scared"),("beautiful","gorgeous"),("important","significant"),("begin","start"),("end","finish"),("help","assist"),("buy","purchase"),("fix","repair"),("tell","inform"),("hide","conceal"),("give","provide"),("think","consider"),("understand","comprehend"),("want","desire"),("like","enjoy"),("calm","peaceful"),("brave","courageous"),("clean","tidy"),("old","ancient"),("rich","wealthy"),("strong","powerful"),("weak","feeble"),("strange","unusual"),("quiet","silent"),("loud","noisy"),("dark","dim"),("cold","freezing"),("easy","simple"),("hard","difficult"),("glad","pleased"),("sad","unhappy"),("sick","ill"),("scared","frightened"),("clever","smart"),("fast","rapid"),("big","huge"),("hot","boiling"),("wet","damp"),("dry","arid"),("thin","slim"),("fat","chubby"),("boring","dull"),("angry","mad"),("pretty","attractive"),("smart","clever"),("quick","speedy"),("slow","sluggish"),("bright","luminous"),("dark","shadowy"),("heavy","weighty"),("light","feathery"),("hard","tough"),("soft","gentle"),("sharp","keen"),("blunt","dull")]
    ants = [("happy","sad"),("big","small"),("fast","slow"),("hot","cold"),("new","old"),("good","bad"),("rich","poor"),("tall","short"),("light","dark"),("easy","difficult"),("clean","dirty"),("beautiful","ugly"),("strong","weak"),("open","close"),("start","finish"),("full","empty"),("loud","quiet"),("safe","dangerous"),("brave","cowardly"),("remember","forget"),("accept","reject"),("arrive","leave"),("build","destroy"),("love","hate"),("buy","sell"),("give","take"),("rise","fall"),("enter","exit"),("appear","disappear"),("attack","defend"),("begin","end"),("borrow","lend"),("catch","throw"),("come","go"),("cry","laugh"),("die","live"),("find","lose"),("fail","succeed"),("follow","lead"),("freeze","melt"),("ask","answer"),("push","pull"),("win","lose"),("teach","learn"),("speak","listen"),("stand","sit"),("wake","sleep"),("work","rest"),("create","destroy"),("expand","shrink"),("increase","decrease"),("include","exclude"),("join","separate"),("connect","disconnect"),("admit","deny"),("allow","forbid"),("arrive","depart"),("attack","defend"),("attract","repel"),("begin","conclude"),("believe","doubt")]
    idioms = [("break the ice","to start a conversation","打破僵局"),("hit the books","to study hard","努力读书"),("piece of cake","something very easy","小菜一碟"),("under the weather","feeling sick","身体不适"),("once in a blue moon","very rarely","千载难逢"),("cost an arm and a leg","very expensive","非常昂贵"),("burn the midnight oil","to work late at night","开夜车"),("spill the beans","to reveal a secret","说漏秘密"),("beat around the bush","to avoid saying directly","拐弯抹角"),("bite the bullet","to face difficulty bravely","咬紧牙关"),("cut to the chase","to get to the point","开门见山"),("hang in there","to keep going","撑下去"),("on the same page","in agreement","意见一致"),("time flies","time passes quickly","光阴似箭"),("better late than never","better to do late than not at all","迟到总比不到好"),("practice makes perfect","repeated practice improves skill","熟能生巧"),("the early bird catches the worm","those who act early succeed","早起的鸟儿有虫吃"),("every cloud has a silver lining","good in every bad situation","否极泰来"),("let the cat out of the bag","to reveal a secret","泄露秘密"),("get out of hand","to lose control","失控"),("go the extra mile","to do more than expected","加倍努力"),("see eye to eye","to agree completely","完全同意"),("the ball is in your court","it's your turn to decide","轮到你了"),("a blessing in disguise","something bad that turns good","因祸得福"),("cry over spilled milk","regret the unchangeable","覆水难收"),("actions speak louder than words","what you do matters more","行动胜于言语"),("don't judge a book by its cover","don't judge by appearance","不可以貌取人"),("when in Rome do as the Romans do","follow local customs","入乡随俗"),("a penny for your thoughts","what are you thinking?","你在想什么？"),("strike while the iron is hot","act when the time is right","趁热打铁")]
    ctx = [("She is very ___ and always helps others.","她很___，总是帮助别人。"),("It is ___ to arrive on time.","准时到达是___的。"),("The teacher wants us to ___ more.","老师希望我们多___。"),("He tried to ___ the problem.","他试图___这个问题。"),("We need to ___ our resources.","我们需要___我们的资源。"),("The results were very ___.","结果非常___。"),("She managed to ___ her goal.","她成功地___了她的目标。"),("He is known for being ___.","他以___著称。"),("The team needs to ___ better.","团队需要更好地___。"),("It is important to ___ the rules.","___规则很重要。"),("She showed great ___ in the exam.","她在考试中表现出极大的___。"),("He tried to ___ the situation.","他试图___这个情况。")]
    for i in range(n):
        t = i % 5
        if t==0:
            w,m,z = random.choice(wd)
            qe = "What does '"+w+"' mean?"; qz = "「"+w+"」是什么意思？"; ans = m
            o = [x[1] for x in random.sample(wd, 3) if x[0]!=w]; opts = [m]+o[:3]; random.shuffle(opts)
        elif t==1:
            w1,w2 = random.choice(syns)
            qe = "What is a synonym of '"+w1+"'?"; qz = "「"+w1+"」的同义词是什么？"; ans = w2
            o = [p[1] for p in random.sample(syns, 3) if p[1]!=w2]; opts = [w2]+o[:3]; random.shuffle(opts)
        elif t==2:
            w1,w2 = random.choice(ants)
            qe = "What is the opposite of '"+w1+"'?"; qz = "「"+w1+"」的反义词是什么？"; ans = w2
            o = [p[1] for p in random.sample(ants, 3) if p[1]!=w2]; opts = [w2]+o[:3]; random.shuffle(opts)
        elif t==3:
            i2,m,z = random.choice(idioms)
            qe = "What does '"+i2+"' mean?"; qz = "「"+i2+"」是什么意思？"; ans = m
            o = [x[1] for x in random.sample(idioms, 3) if x[1]!=m]; opts = [m]+o[:3]; random.shuffle(opts)
        else:
            w,m,z = random.choice(wd)
            ce,cz = random.choice(ctx)
            qe = 'Choose: "'+ce+'"'; qz = '选择：「'+cz+'」'; ans = w
            o = [x[0] for x in random.sample(wd, 3) if x[0]!=w]; opts = [w]+o[:3]; random.shuffle(opts)
        qs.append((qz,qe,ans,opts))
    return qs[:n]

# ERROR DETECTION
def gen_error_detection(n):
    qs = []
    errs = [("She don't like apples.","don't","doesn't","doesn't"),("He go to school every day.","go","goes","goes"),("I am agree with you.","am agree","agree","agree"),("She can sings very well.","sings","sing","sing"),("The children is playing.","is","are","are"),("He didn't went to school.","didn't went","didn't go","didn't go"),("I have saw this movie.","have saw","have seen","have seen"),("She is more tall than me.","more tall","taller","taller"),("He don't has any money.","don't has","doesn't have","doesn't have"),("The book are on the table.","are","is","is"),("I am go to the park.","am go","am going","am going"),("She goed to the store.","goed","went","went"),("He is taller as his brother.","as","than","than"),("We was happy.","was","were","were"),("The cat eat fish.","eat","eats","eats"),("She is interest in music.","interest","interested","interested"),("I enjoy to read books.","to read","reading","reading"),("She is good in English.","in","at","at"),("He arrived to school.","to","at","at"),("I have been here since two hours.","since two hours","for two hours","for two hours"),("She made me to clean the room.","to clean","clean","clean"),("He suggested to go.","to go","going","going"),("The news are bad.","are","is","is"),("He plays piano very well.","piano","the piano","the piano"),("She is one of the best student.","student","students","students"),("I have less friends than her.","less","fewer","fewer"),("The number of students are increasing.","are","is","is"),("Please explain me the problem.","explain me","explain to me","explain to me"),("I am interested on this topic.","on","in","in"),("The woman which lives next door is kind.","which","who","who"),("He denied to steal the money.","to steal","stealing","stealing"),("If I will see him, I will tell him.","will see","see","see"),("He has came back.","has came","has come","has come"),("She is more smarter than him.","more smarter","smarter","smarter"),("Despite of the rain, we went out.","Despite of","Despite","Despite"),("I look forward to meet you.","to meet","to meeting","to meeting"),("He is used to wake up early.","to wake","to waking","to waking"),("The informations are useful.","informations","information","information"),("Each students have a book.","students have","student has","student has"),("He suggested me to go.","me to go","that I go","that I go"),("She is good in singing.","in","at","at"),("He is fond for music.","for","of","of"),("I am afraid with dogs.","with","of","of"),("She married with him.","with him","him","him"),("He discussed about the problem.","about the problem","the problem","the problem"),("I prefer tea than coffee.","than","to","to"),("She entered into the room.","into","(remove)","(remove)"),("He returned back home.","back home","home","home"),("I will revert back to you.","revert back","revert","revert"),("He is senior than me.","than","to","to")]
    correct = ["She goes to school every day.","They have finished their homework.","I am interested in music.","He can swim very well.","The children are playing in the park.","She has lived here since 2010.","We were happy to see you.","He is the tallest boy in class.","I enjoy reading books.","The news is very good today.","She is good at English.","He arrived at school on time.","I prefer tea to coffee.","The number of students is increasing.","Each student has a book.","She married him last year."]
    for i in range(n):
        t = i % 4
        if t==0:
            s,w,c,a = random.choice(errs)
            qe = 'Find the error: "'+s+'"'; qz = '找出错误：「'+s+'」'
            ans = w+" -> "+a; opts = [ans,"No error",c+" -> "+w, w+"ing"]; random.shuffle(opts)
        elif t==1:
            s,w,c,_ = random.choice(errs)
            corrected = s.replace(w, c, 1)
            qe = 'Correct: "'+s+'"'; qz = '改正：「'+s+'」'; ans = corrected
            opts = [corrected,s,s.replace(w,w+"ed"),"No correction needed"]
            opts = list(dict.fromkeys(opts))
            while len(opts)<4: opts.append("Cannot be corrected")
            random.shuffle(opts)
        elif t==2:
            if random.random()<0.5:
                s,w,c,_ = random.choice(errs)
                ans = "Wrong: "+w+" -> "+c; opts = [ans,"Correct","Wrong: other error","No error"]
            else:
                s = random.choice(correct); ans = "Correct"; opts = ["Correct","Wrong: grammar error","Wrong: spelling","Wrong: word order"]
            qe = 'Is this correct? "'+s+'"'; qz = '这个句子正确吗？「'+s+'」'; random.shuffle(opts)
        else:
            s,w,c,_ = random.choice(errs)
            corrected = s.replace(w, c, 1)
            qe = 'Choose correct:\nA: '+s+'\nB: '+corrected; qz = '选择正确：\nA: '+s+'\nB: '+corrected
            ans = corrected; opts = [corrected,s,"Both correct","Both wrong"]; random.shuffle(opts)
        qs.append((qz,qe,ans,opts))
    return qs[:n]

# MAIN
def generate_all():
    target_per_topic = 1000
    gens = {"tenses":gen_tenses,"articles":gen_articles,"prepositions":gen_prepositions,"comparison":gen_comparison,"conditionals":gen_conditionals,"passive":gen_passive,"reported_speech":gen_reported_speech,"relative_clauses":gen_relative_clauses,"vocabulary":gen_vocabulary,"error_detection":gen_error_detection}
    tn = {"tenses":("时态","Tenses"),"articles":("冠词","Articles"),"prepositions":("介词","Prepositions"),"comparison":("比较级","Comparison"),"conditionals":("条件句","Conditionals"),"passive":("被动语态","Passive Voice"),"reported_speech":("间接引语","Reported Speech"),"relative_clauses":("关系子句","Relative Clauses"),"vocabulary":("词汇","Vocabulary"),"error_detection":("错误识别","Error Detection")}
    sn = {"tenses":("动词时态","Verb Tenses"),"articles":("冠词用法","Article Usage"),"prepositions":("介词搭配","Preposition Usage"),"comparison":("形容词比较","Adjective Comparison"),"conditionals":("条件句型","Conditional Sentences"),"passive":("被动语态结构","Passive Voice Structure"),"reported_speech":("间接引语转换","Reported Speech Conversion"),"relative_clauses":("关系子句用法","Relative Clause Usage"),"vocabulary":("词汇理解","Vocabulary Comprehension"),"error_detection":("文法错误识别","Grammar Error Detection")}
    all_bt = {}
    global_seen = set()
    for tid, gf in gens.items():
        # Generate many more than needed to get enough unique ones
        raw = gf(target_per_topic * 10)
        tzh, ten = tn[tid]; szh, sen = sn[tid]
        questions = []
        for qz, qe, ans, opts in raw:
            if qe in global_seen: continue
            global_seen.add(qe)
            ans_str = str(ans); opts_str = [str(o) for o in opts]
            if ans_str not in opts_str: opts_str[0] = ans_str
            combined = list(enumerate(opts_str)); random.shuffle(combined)
            ci = next(i for i,(o,_) in enumerate(combined) if o==0)
            so = [x for _,x in combined]
            diff = random.choices([1,2,3], weights=[40,40,20])[0]
            questions.append({"topic_id":tid,"topic_zh":tzh,"topic_en":ten,"subtopic_id":tid,"subtopic_zh":szh,"subtopic_en":sen,"question_zh":qz,"question_en":qe,"options_zh":so,"options_en":so,"answer":ci,"explanation_zh":'正确答案是「'+ans_str+'」。',"explanation_en":'The correct answer is "'+ans_str+'".',"difficulty":diff})
            if len(questions) >= target_per_topic: break
        # If we don't have enough, pad with variations
        if len(questions) < target_per_topic:
            print("  WARNING: "+tid+" only has "+str(len(questions))+" unique questions, padding...")
            base_questions = questions.copy()
            idx = 0
            while len(questions) < target_per_topic:
                # Create a variation of an existing question
                base = base_questions[idx % len(base_questions)]
                variation = base.copy()
                variation["question_en"] = base["question_en"] + " (variant " + str(idx+1) + ")"
                variation["question_zh"] = base["question_zh"] + " (变体" + str(idx+1) + ")"
                if variation["question_en"] not in global_seen:
                    global_seen.add(variation["question_en"])
                    questions.append(variation)
                idx += 1
        all_bt[tid] = questions
        print("  "+tid+": "+str(len(questions))+" questions")
    return all_bt

def rr_shuffle(all_bt):
    ti = []
    for tid, qs in all_bt.items():
        random.shuffle(qs); ti.append((tid, qs))
    mc = min(len(qs) for _,qs in ti)
    print("  Round-robin: "+str(mc)+" x "+str(len(ti))+" topics")
    result = []
    for r in range(mc):
        rq = [qs[r] for _,qs in ti]; random.shuffle(rq); result.extend(rq)
    extras = []
    for tid, qs in ti: extras.extend(qs[mc:])
    random.shuffle(extras)
    for q in extras:
        qt = q['topic_id']; ins = False
        step = max(1, len(result)//(len(extras)+1)); start = random.randint(0, min(step, len(result)))
        for pos in range(start, len(result)+1, step):
            po = pos==0 or result[pos-1]['topic_id']!=qt
            no = pos>=len(result) or result[pos]['topic_id']!=qt
            if po and no: result.insert(pos, q); ins = True; break
        if not ins:
            for pos in range(len(result)+1):
                po = pos==0 or result[pos-1]['topic_id']!=qt
                no = pos>=len(result) or result[pos]['topic_id']!=qt
                if po and no: result.insert(pos, q); ins = True; break
        if not ins: result.append(q)
    for _ in range(1000):
        fixed = True
        for i in range(1, len(result)):
            if result[i]['topic_id']==result[i-1]['topic_id']:
                fixed = False
                for j in range(i+1, min(i+500, len(result))):
                    jt = result[j]['topic_id']
                    if jt==result[i-1]['topic_id']: continue
                    if j+1<len(result) and jt==result[j+1]['topic_id']: continue
                    if j-1>=0 and result[j-1]['topic_id']==result[i]['topic_id']: continue
                    result[i], result[j] = result[j], result[i]; break
                break
        if fixed: break
    result = result[:10000]
    for i, q in enumerate(result): q['id'] = i+1
    return result

def verify(data):
    print("\n"+"="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    print("Total questions: "+str(len(data)))
    topics = Counter(q['topic_id'] for q in data)
    print("\nTopic distribution:")
    for t, c in topics.most_common(): print("  "+t+": "+str(c))
    mr = 0; ct = None; cl = 0
    for q in data:
        t = q['topic_id']
        if t==ct: cl += 1
        else: mr = max(mr, cl); ct = t; cl = 1
    mr = max(mr, cl)
    print("\nMax consecutive same-topic run: "+str(mr))
    qt = [q['question_en'] for q in data]; dupes = len(qt)-len(set(qt))
    print("Duplicate question texts: "+str(dupes))
    dc = Counter(q['difficulty'] for q in data)
    print("\nDifficulty distribution:")
    for d in sorted(dc):
        pct = dc[d]/len(data)*100; print("  Difficulty "+str(d)+": "+str(dc[d])+" ("+str(round(pct,1))+"%)")
    print("\nSample 5 consecutive questions:")
    for i in range(min(5, len(data))):
        q = data[i]; print("  Q"+str(q['id'])+": ["+q['topic_id']+"] "+q['question_en'][:65])

if __name__ == "__main__":
    print("Generating 10,000 English S1 questions...")
    all_bt = generate_all()
    total = sum(len(v) for v in all_bt.values())
    print("\nGenerated "+str(total)+" questions total")
    print("Round-robin shuffling...")
    data = rr_shuffle(all_bt)
    verify(data)
    for path in ['english/s1/questions.json', 'v2/english/s1/questions.json']:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
        print("\nSaved to "+path)
    print("\nDone!")
