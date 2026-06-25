#!/usr/bin/env python3
"""Fix placeholder song options in music quiz questions."""
import json, glob, re, os, random

SONG_DB = {
    # === WESTERN FEMALE ===
    "adele": ["Rolling in the Deep", "Someone Like You", "Hello", "Set Fire to the Rain", "Skyfall", "Easy On Me"],
    "ariana_grande": ["Thank U, Next", "7 Rings", "Positions", "No Tears Left to Cry", "Side to Side", "Into You"],
    "beyonce": ["Crazy in Love", "Halo", "Single Ladies", "Irreplaceable", "Formation", "Drunk in Love"],
    "billie_eilish": ["Bad Guy", "Everything I Wanted", "Happier Than Ever", "Lovely", "Ocean Eyes", "What Was I Made For"],
    "britney_spears": ["Baby One More Time", "Toxic", "Oops!...I Did It Again", "Womanizer", "Stronger", "Circus"],
    "celine_dion": ["My Heart Will Go On", "The Power of Love", "Because You Loved Me", "It's All Coming Back to Me", "Think Twice", "I'm Alive"],
    "doja_cat": ["Say So", "Kiss Me More", "Woman", "Need to Know", "Streets", "Paint The Town Red"],
    "dua_lipa": ["Levitating", "Don't Start Now", "New Rules", "One Kiss", "Physical", "Future Nostalgia"],
    "halsey": ["Without Me", "Bad at Love", "Closer", "Colors", "Graveyard", "Nightmare"],
    "katy_perry": ["Roar", "Firework", "Dark Horse", "Teenage Dream", "California Gurls", "I Kissed a Girl"],
    "lady_gaga": ["Bad Romance", "Poker Face", "Shallow", "Born This Way", "Just Dance", "Alejandro"],
    "lorde": ["Royals", "Team", "Green Light", "Solar Power", "Ribs", "Tennis Court"],
    "madonna": ["Like a Virgin", "Material Girl", "Vogue", "Like a Prayer", "Hung Up", "Ray of Light"],
    "mariah_carey": ["All I Want for Christmas Is You", "Hero", "We Belong Together", "Fantasy", "Emotions", "Vision of Love"],
    "olivia_rodrigo": ["drivers license", "good 4 u", "deja vu", "brutal", "vampire", "get him back!"],
    "rihanna": ["Umbrella", "Diamonds", "We Found Love", "Work", "Stay", "Only Girl"],
    "sabrina_carpenter": ["Espresso", "Feather", "Nonsense", "Skin", "Because I Liked a Boy", "Please Please Please"],
    "sza": ["Kill Bill", "Good Days", "The Weekend", "Love Galore", "Snooze", "Shirt"],
    "taylor_swift": ["Shake It Off", "Blank Space", "Love Story", "Anti-Hero", "Cruel Summer", "Bad Blood"],
    "whitney_houston": ["I Will Always Love You", "Greatest Love of All", "I Wanna Dance with Somebody", "How Will I Know", "Run to You", "Saving All My Love"],

    # === WESTERN MALE ===
    "adam_levine": ["She Will Be Loved", "Sugar", "Maps", "Payphone", "Moves Like Jagger", "This Love"],
    "bruno_mars": ["Uptown Funk", "Just the Way You Are", "Grenade", "24K Magic", "That's What I Like", "When I Was Your Man"],
    "charlie_puth": ["See You Again", "Attention", "We Don't Talk Anymore", "One Call Away", "How Long", "Light Switch"],
    "drake": ["God's Plan", "Hotline Bling", "One Dance", "Started From the Bottom", "Nice for What", "Toosie Slide"],
    "ed_sheeran": ["Shape of You", "Thinking Out Loud", "Perfect", "Photograph", "Castle on the Hill", "Bad Habits"],
    "elton_john": ["Your Song", "Rocket Man", "Tiny Dance", "Crocodile Rock", "Can You Feel the Love Tonight", "I'm Still Standing"],
    "elvis_presley": ["Can't Help Falling in Love", "Jailhouse Rock", "Hound Dog", "Love Me Tender", "Suspicious Minds", "Blue Suede Shoes"],
    "freddie_mercury": ["Bohemian Rhapsody", "We Are the Champions", "Somebody to Love", "Don't Stop Me Now", "Killer Queen", "The Show Must Go On"],
    "harry_styles": ["As It Was", "Watermelon Sugar", "Sign of the Times", "Adore You", "Late Night Talking", "Music for a Sushi Restaurant"],
    "john_legend": ["All of Me", "Ordinary People", "Love Me Now", "Glory", "Green Light", "Tonight"],
    "john_lennon": ["Imagine", "Instant Karma", "Working Class Hero", "Jealous Guy", "Woman", "Happy Xmas"],
    "justin_bieber": ["Baby", "Sorry", "Love Yourself", "What Do You Mean", "Peaches", "Stay"],
    "michael_jackson": ["Thriller", "Billie Jean", "Beat It", "Bad", "Smooth Criminal", "Black or White"],
    "paul_mccartney": ["Yesterday", "Band on the Run", "Live and Let Die", "Maybe I'm Amazed", "Jet", "Silly Love Songs"],
    "pharrell": ["Happy", "Frontin'", "Beautiful", "Come Get It Bae", "Marilyn Monroe", "Gust of Wind"],
    "post_malone": ["Circles", "Rockstar", "Sunflower", "Congratulations", "Better Now", "Psycho"],
    "sam_smith": ["Stay with Me", "Too Good at Goodbyes", "I'm Not the Only One", "Latch", "Unholy", "Writing's on the Wall"],
    "shawn_mendes": ["Stitches", "Treat You Better", "There's Nothing Holdin' Me Back", "In My Blood", "Señorita", "Mercy"],
    "stevie_wonder": ["Superstition", "Isn't She Lovely", "I Just Called to Say I Love You", "Sir Duke", "Signed Sealed Delivered", "Higher Ground"],
    "the_weeknd": ["Blinding Lights", "Starboy", "The Hills", "Can't Feel My Face", "Save Your Tears", "Earned It"],

    # === WESTERN GROUPS ===
    "abba": ["Dancing Queen", "Mamma Mia", "Gimme! Gimme! Gimme!", "Waterloo", "SOS", "The Winner Takes It All"],
    "backstreet_boys": ["I Want It That Way", "Everybody", "As Long As You Love Me", "Shape of My Heart", "Larger Than Life", "Quit Playing Games"],
    "bts": ["Dynamite", "Butter", "Boy With Luv", "DNA", "Fake Love", "Spring Day"],
    "coldplay": ["Yellow", "Fix You", "Viva la Vida", "The Scientist", "Paradise", "Clocks"],
    "destinys_child": ["Say My Name", "Jumpin' Jumpin'", "Bills Bills Bills", "Survivor", "Independent Women", "Bootylicious"],
    "eagles": ["Hotel California", "Take It Easy", "Desperado", "One of These Nights", "Life in the Fast Lane", "Lyin' Eyes"],
    "foo_fighters": ["Everlong", "The Pretender", "Best of You", "Learn to Fly", "My Hero", "Times Like These"],
    "green_day": ["Basket Case", "Boulevard of Broken Dreams", "American Idiot", "When I Come Around", "21 Guns", "Wake Me Up"],
    "imagine_dragons": ["Radioactive", "Demons", "Believer", "Thunder", "Enemy", "Natural"],
    "linkin_park": ["In the End", "Numb", "Crawling", "One Step Closer", "What I've Done", "Breaking the Habit"],
    "maroon5": ["Sugar", "She Will Be Loved", "Maps", "Payphone", "Moves Like Jagger", "This Love"],
    "nirvana": ["Smells Like Teen Spirit", "Come as You Are", "Heart-Shaped Box", "Lithium", "In Bloom", "All Apologies"],
    "nsync": ["Bye Bye Bye", "It's Gonna Be Me", "Tearin' Up My Heart", "I Want You Back", "This I Promise You", "Pop"],
    "one_direction": ["What Makes You Beautiful", "Story of My Life", "Best Song Ever", "Drag Me Down", "Night Changes", "Live While We're Young"],
    "queen": ["Bohemian Rhapsody", "We Will Rock You", "We Are the Champions", "Don't Stop Me Now", "Somebody to Love", "Killer Queen"],
    "radiohead": ["Creep", "Karma Police", "Paranoid Android", "No Surprises", "Everything in Its Right Place", "Fake Plastic Trees"],
    "rolling_stones": ["Satisfaction", "Paint It Black", "Sympathy for the Devil", "Gimme Shelter", "Start Me Up", "Angie"],
    "spice_girls": ["Wannabe", "Spice Up Your Life", "Say You'll Be There", "2 Become 1", "Stop", "Who Do You Think You Are"],
    "the_beatles": ["Let It Be", "Hey Jude", "Come Together", "Yesterday", "Here Comes the Sun", "Twist and Shout"],
    "u2": ["With or Without You", "One", "Beautiful Day", "Where the Streets Have No Name", "Sunday Bloody Sunday", "I Still Haven't Found"],

    # === JAPANESE FEMALE ===
    "ado": ["Usseewa", "New Era", "Gira Gira", "Odo", "Ashura-chan", "Show"],
    "aimer": ["Brave Shine", "Ref:rain", "Kataomoi", "Star Ring Child", "Hz", "I Beg You"],
    "aimyon": ["Marigold", "Haru no Hi", "Koi wa Futago de Kijyuku", "Hadaka no Kokoro", "Shinseiro", "Futari"],
    "ayumi_hamasaki": ["M", "Evolution", "Trauma", "Boys & Girls", "Vogue", "Dearest"],
    "babymetal_su": ["Gimme Chocolate", "Karate", "Road of Resistance", "Distortion", "Pa Pa Ya", "BxMxC"],
    "eriko_iwasawa": ["Kawaita Sakebi", "Yasashisa ni Tsutsumareta Nara", "Nijiiro", "Mata Aeru Hi Made", "Shiokaze", "Hikaru Kaze"],
    "hikaru_utada": ["First Love", "Flavor of Life", "Beautiful World", "Sakura Drops", "Can You Keep a Secret", "Traveling"],
    "kumi_koda": ["Cutie Honey", "Butterfly", "Real Emotion", "Taboo", "Lollipop", "Amai Wana"],
    "kyary": ["PONPONPON", "Tsukema Tsukeru", "Ninja Re Bang Bang", "Fashion Monster", "Kira Kira Killer", "Candy Candy"],
    "lisa_jp": ["oath sign", "crossing field", "Rising Hope", "Shirushi", "Thousand Eyes", "Datte Atashi no Hero"],
    "milet": ["inside you", "Prover", "Wake Me Up", "Drown", "Flare", "Ordinary Days"],
    "misia": ["Everything", "Ashita e", "Anata ni Smile", "Hatenaku Tsuzuku Story", "Into the Light", "Color of Life"],
    "namie_amuro": ["Can You Celebrate", "Body Feels EXIT", "Chase the Chance", "Don't Wanna Cry", "Love Story", "Hero"],
    "perfume_nocchi": ["Polyrhythm", "Chocolate Disco", "Flash", "Spending all my time", "Pick Me Up", "Time Warp"],
    "reina_tanaka": ["Koi no Bakudan", "Kiss Me Aishiteru", "Motto Gyutto", "Jiriri Kiteru", "Suki Sugiru", "Namida no Request"],
    "ringo_sheena": ["Kabukicho no Joou", "Tsumi to Batsu", "Honnou", "Meisai", "Sid to Hakuchuumu", "Marunouchi Sadistic"],
    "utada_hikaru": ["First Love", "Flavor of Life", "Beautiful World", "Sakura Drops", "Can You Keep a Secret", "Traveling"],
    "yoasobi_ikura": ["Yoru ni Kakeru", "Gunjou", "Kaibutsu", "Sangenshoku", "Tabun", "Shukufuku"],
    "yonezu_kenshi_f": ["Lemon", "Uma to Shika", "Kanden", "Kick Back", "Flamingo", "Peace Sign"],
    "yui_jp": ["Good-bye Days", "Rolling Star", "Che.R.Ry", "LIFE", "I remember you", "Gloria"],

    # === JAPANESE MALE ===
    "aimyon_m": ["Marigold", "Haru no Hi", "Koi wa Futago de Kijyuku", "Hadaka no Kokoro", "Shinseiro", "Futari"],
    "arashi_ohno": ["Love so sweet", "Happiness", "A.Ra.Sha", "Sakura", "Truth", "Kaze no Mukou e"],
    "daigo": ["Deeper", "Mune ga Dokidoki", "Inazuma", "Koi Suru Fortune Cookie", "Namba Koi", "Aishi Aisarete Ikiru no Sa"],
    "gen_hoshino": ["Koi", "Sun", "Family Song", "Idea", "Same Thing", "Comedy"],
    "hikaru_utada_m": ["First Love", "Flavor of Life", "Beautiful World", "Sakura Drops", "Can You Keep a Secret", "Traveling"],
    "jin_akanishi": ["Seasons", "Heart Beat", "Hey What's Up", "LOVE SONG", "Bandit", "Choo Choo TRAIN"],
    "kazuya_kamenashi": ["Kizuna", "SIGNAL", "Real Face", "SHE SAID", "ONE DROP", "Inori"],
    "kenshi_yonezu": ["Lemon", "Uma to Shika", "Kanden", "Kick Back", "Flamingo", "Peace Sign"],
    "koichi_domoto": ["Deep in my heart", "Nocturne", "Yasashii Ame", "Hoshi ni Negai wo", "Love Collider", "Ordinary"],
    "masaharu_fukuyama": ["Sakura Zaka", "Himawari", "Kazoku ni Narou yo", "Tokyo", "Saiai", "Fighters"],
    "official髭": ["Pretender", "Subtitle", "Koi", "I LOVE YOU", "Dry Flower", "Mixed Nuts"],
    "one_ok_rock_taka": ["The Beginning", "Wherever You Are", "Mighty Long Fall", "Clock Strikes", "Heartache", "Wasted Nights"],
    "radwimps": ["Zen Zen Zense", "Sparkle", "Nandemonaiya", "HINOMARU", "Suzume", "Kanata Haluka"],
    "ryosuke_yamada": ["SUPERSTAR", "Moii", "KISS KISS KISS", "Loveless", "Moonlight", "Chikai"],
    "takuya_kimura": ["Can't Help Falling in Love", "KISS OF LIFE", "Natsu no Hi", "Koi wa Utsukushii", "Hitomi wo Tojite", "LOVE TRULY"],
    "tatsuro_yamashita": ["Ride on Time", "Christmas Eve", "Kokiatsu Girl", "Sparkle", "Love Space", "Get Back"],
    "tomohiso_yamashita": ["One in a Million", "Loveless", "Daite Señorita", "Hadakanbo", "Keep the Faith", "Ai, Texas"],
    "tsuyoshi_domoto": ["MACHINE", "Kubikiri Asura", "Anniversary", "Yume no Naka", "Kawaita Hana", "Machigai Sagashi"],
    "yosui_inoue": ["Shounen Jidai", "Yume no Naka", "Makeinu no Uta", "Iruka", "Kasa ga Nai", "Nagai Yoru"],
    "yuto_nakajima": ["KISS da Baby", "FEEL IT", "Kimi no Koto", "Answer", "Come On!", "Magic Power"],

    # === JAPANESE GROUPS ===
    "aiko": ["Kabutomushi", "Hanabi", "Boyfriend", "Kira Kira", "Straw", "Motto"],
    "arashi": ["Love so sweet", "Happiness", "A.Ra.Sha", "Sakura", "Truth", "Kaze no Mukou e"],
    "asian_kung_fu": ["After Dark", "Re:Re:", "Solanin", "Kigou to shite", "World World World", "Hakai Kiroku"],
    "babymetal": ["Gimme Chocolate", "Karate", "Road of Resistance", "Distortion", "Pa Pa Ya", "BxMxC"],
    "bump_of_chicken": ["Tentai Kansoku", "Karma", "Hello, World!", "GHOST", "Ripple", "Niji wo Matsu Hito"],
    "dreams_true": ["Love Lu Lu", "Suki da kara", "Kagayaki wo Matsu", "Asunaro Sun", "Tsuretette Tsuretette", "Nee"],
    "flumpool": ["Hana ni Nare", "Kimi ni Todoke", "Nagareboshi", "Across the Time", "Because... I am", "Umaku Ienai"],
    "glay": ["HOWEVER", "Yuuwaku", "Beloved", "Winter Again", "Pure Soul", "Soul Love"],
    "janne_da_arc": ["Kanojo to Kanojo no Heso", "Shining ray", "Mystic Edge", "DOLLS", "Love is Here", "Lunatic Gate"],
    "king_gnu": ["Hakujitsu", "Ichizu", "Doronbo", "Cry Baby", "SPECIALZ", "BOY"],
    "larcenciel": ["HONEY", "flower", "READY STEADY GO!", "Link", "Blurry Eyes", "NEO UNIVERSE"],
    "mr_children": ["Sign", "Kurumi", "Namonaki Uta", "Tomorrow never knows", "HERO", "Brand new planet"],
    "official_hige": ["Pretender", "Subtitle", "Koi", "I LOVE YOU", "Dry Flower", "Mixed Nuts"],
    "one_ok_rock": ["The Beginning", "Wherever You Are", "Mighty Long Fall", "Clock Strikes", "Heartache", "Wasted Nights"],
    "perfume": ["Polyrhythm", "Chocolate Disco", "Flash", "Spending all my time", "Pick Me Up", "Time Warp"],
    "radwimps_g": ["Zen Zen Zense", "Sparkle", "Nandemonaiya", "HINOMARU", "Suzume", "Kanata Haluka"],
    "scandal_jp": ["Shunkan Sentimental", "Harukaze", "Taiyou Scandalous", "Love SURVIVE", "OVER DRIVE", "Platform"],
    "southern_all": ["Aozora", "Himawari", "Niji", "Mojamoja", "Kiseki", "Tenohira"],
    "x_japan": ["Endless Rain", "Rusty Nail", "Tears", "Kurenai", "Silent Jealousy", "Forever Love"],
    "yoasobi": ["Yoru ni Kakeru", "Gunjou", "Kaibutsu", "Sangenshoku", "Tabun", "Shukufuku"],

    # === KOREAN FEMALE ===
    "chung_ha": ["Gotta Go", "Bicycle", "Stay Tonight", "Roller Coaster", "Snapping", "Dream of You"],
    "eunbi": ["Glitch", "Door", "Esper", "The Flash", "Simulation", "Amber"],
    "hwasa": ["Maria", "Twit", "I'm a B", "Guilty Pleasure", "Somebody!", "LMM"],
    "iu": ["Good Day", "Palette", "Through the Night", "Eight", "Lilac", "Celebrity"],
    "jennie": ["SOLO", "You & Me", "One of the Girls", "Slow Motion", "Mantra", "Love Hangover"],
    "jihyo": ["Killin' Me Good", "Talkin' About It", "Room", "Wishing on You", "Don't Wanna Go Back", "Nightmare"],
    "jisoo": ["FLOWER", "All Eyes On Me", "Earthquake", "Your Love", "Hugs & Kisses", "TEARS"],
    "joy": ["Hello", "Day by Day", "Je T'aime", "If Only", "Love Song", "Happy Birthday to You"],
    "lisa": ["LALISA", "MONEY", "SG", "Rockstar", "New Woman", "Moonlit Floor"],
    "nayeon": ["POP!", "NO PROBLEM", "Love Countdown", "Candyfloss", "All or Nothing", "ABCD"],
    "rose": ["On The Ground", "Gone", "APT.", "number one girl", "toxic till the end", "3am"],
    "sana": ["Bouquet", "Dazzling", "Breakthrough", "Fanfare", "I Got You", "Perfect World"],
    "seulgi": ["28 Reasons", "Dead Man Runnin'", "Anywhere But Home", "Crown", "Bad Boy", "Monster"],
    "solar": ["Spit It Out", "Honey", "Always", "Raw", "Ddun Ddun Ddun", "In My Dreams"],
    "somi": ["DUMB DUMB", "What You Waiting For", "XOXO", "Anymore", "Fast Forward", "Gold Gold Gold"],
    "taeyeon": ["I", "Fine", "Spark", "INVU", "Four Seasons", "Weekend"],
    "tzuyu": ["Run Away", "Heartbreak in Heaven", "Losing Sleep", "Fly", "One Love", "Dreaming"],
    "wendy": ["Like Water", "When This Rain Stops", "Best Friend", "Why Can't You Love Me", "Airport Goodbyes", "Wish You Hell"],
    "yena": ["SMILEY", "SMARTPHONE", "Love War", "Hate Rodrigo", "Nemonemo", "Good Morning"],

    # === KOREAN MALE ===
    "crush": ["Beautiful", "Don't Forget", "Sometimes", "SOFA", "Bittersweet", "Rush Hour"],
    "dean": ["Instagram", "D (Half Moon)", "Pour Up", "Bonnie & Clyde", "love", "Howlin' 404"],
    "dokyeom": ["Go", "Yours", "Waste It on Me", "Missed Connections", "17", "My I"],
    "exo_baekhyun": ["UN Village", "Candy", "Bambi", "Love Again", "Get You Alone", "Amusement Park"],
    "exo_chanyeol": ["SSFW", "Tomorrow", "Yours", "Nothin'", "Break Your Box", "Good Enough"],
    "exo_d_o": ["Rose", "I'm Gonna Love You", "Somebody", "My Dear", "Si Fueras Mía", "The View"],
    "g-dragon": ["Crooked", "Coup d'Etat", "That XX", "Untitled 2014", "Heartbreaker", "One of a Kind"],
    "hoshi": ["Spider", "Touch", "Horangi Power", "Stay", "We Make You", "Ruby"],
    "ikon_bobby": ["I Love You", "Runaway", "Holup!", "Tendae", "Lilac", "U Mad"],
    "iu_male": ["Good Day", "Palette", "Through the Night", "Eight", "Lilac", "Celebrity"],
    "jackson_wang": ["100 Ways", "Blow", "LMLTY", "Dawn of Us", "Oxygen", "Cheetah"],
    "jay_park": ["All I Wanna Do", "Mommae", "Drive", "GANADARA", "Taxi Blurry", "Need to Know"],
    "jimin": ["Set Me Free Pt.2", "Like Crazy", "Face-off", "Alone", "Closer Than This", "Who"],
    "jungkook": ["Seven", "3D", "Standing Next to You", "Still With You", "Euphoria", "My Time"],
    "kang_daniel": ["2U", "Antidote", "Paranoia", "Who U Are", "Touchin'", "Nirvana"],
    "rm_kr": ["Wild Flower", "Come Back to Me", "LOST!", "Right People Wrong Place", "Groin", "Neva Play"],
    "taeyang": ["Eyes Nose Lips", "Wedding Dress", "Ringa Linga", "Only Look at Me", "VIBE", "Shoong!"],
    "v": ["Slow Dancing", "FRI(END)S", "Love Me Again", "Rainy Days", "Blue", "For Us"],
    "winner_mino": ["Fiancé", "Run Away", "Body", "I'm Him", "Ok Man", "Drunk Talk"],
    "zico": ["Any Song", "Boys and Girls", "She's a Baby", "SPOT!", "New Thing", "Artist"],

    # === KOREAN GROUPS ===
    "2ne1": ["I Am the Best", "Fire", "Lonely", "Come Back Home", "Ugly", "Falling in Love"],
    "aespa": ["Black Mamba", "Next Level", "Savage", "Spicy", "Supernova", "Whiplash"],
    "ateez": ["Wonderland", "Guerrilla", "Bouncy", "Say My Name", "HALAZIA", "Crazy Form"],
    "bigbang": ["Fantastic Baby", "BANG BANG BANG", "Loser", "Haru Haru", "Blue", "Still Life"],
    "blackpink": ["DDU-DU DDU-DU", "Kill This Love", "How You Like That", "Boombayah", "As If It's Your Last", "Pink Venom"],
    "bts_group": ["Dynamite", "Butter", "Boy With Luv", "DNA", "Fake Love", "Spring Day"],
    "exo": ["Growl", "Call Me Baby", "Love Shot", "Ko Ko Bop", "Monster", "Tempo"],
    "girls_generation": ["Gee", "Into the New World", "I Got a Boy", "The Boys", "Mr. Mr.", "Lion Heart"],
    "got7": ["Just Right", "If You Do", "Lullaby", "Never Ever", "Hard Carry", "Eclipse"],
    "itzy": ["DALLA DALLA", "WANNABE", "LOCO", "SNEAKERS", "CAKE", "GOLD"],
    "ive": ["ELEVEN", "LOVE DIVE", "After LIKE", "Kitsch", "I AM", "Baddie"],
    "le_sserafim": ["FEARLESS", "ANTIFRAGILE", "UNFORGIVEN", "EASY", "Perfect Night", "SMART"],
    "mamamoo": ["HIP", "Starry Night", "Egotistic", "Gogobebe", "Dingga", "AYA"],
    "nct": ["Cherry Bomb", "Kick It", "Sticker", "2 Baddies", "Golden Age", "Baggy Jeans"],
    "new_jeans": ["Attention", "Hype Boy", "Cookie", "Ditto", "OMG", "Super Shy"],
    "red_velvet": ["Red Flavor", "Psycho", "Bad Boy", "Peek-A-Boo", "Feel My Rhythm", "Zimzalabim"],
    "seventeen": ["Don't Wanna Cry", "Left & Right", "HOT", "_WORLD", "Super", "God of Music"],
    "shinee": ["Ring Ding Dong", "Lucifer", "View", "Sherlock", "Everybody", "Don't Call Me"],
    "stray_kids": ["God's Menu", "Back Door", "MANIAC", "S-Class", "LALALALA", "Chk Chk Boom"],
    "twice_kr": ["TT", "What Is Love?", "Feel Special", "FANCY", "The Feels", "SET ME FREE"],

    # === MANDARIN FEMALE ===
    "a-lin": ["Give Me a Reason", "Pseudo-Single", "Best Friend", "Huang Shi", "Ai Qing De Mo Yang", "Qi Shi Wo Huan Zai"],
    "a-mei": ["Sisters", "Remember", "Bad Boy", "Ku Yao Fang Shou", "Huo", "San Tian San Ye"],
    "chen_lihua": ["Jiu Shi Huan Mei You Wang Ji", "Qian Nv You Hun", "Bu Liao Qing", "Xue Hua Piao Piao", "Ai Shang Yi Ge Bu Hui Jia De Ren", "Yue Liang Dai Biao Wo De Xin"],
    "della_ding": ["Bu Yao Dui Wo Shuo", "Ni Yao De Ai", "Lian Ai Ing", "Hao Yao Bu Jian", "Mo Shi", "Xing Fu De Ke Du"],
    "faye_chan": ["Medley", "Tian Xia Wu Shuang", "Qing Fei De Yi Bu", "Hao Xin Qing", "Ni Kuai Le Suo Yi Wo Kuai Le", "Wo Men Dou Shi Hao Hai Zi"],
    "g.e.m._mandarin": ["Guang Hui Sui Yue", "Pao Mo", "Dao Xiang", "Hou Lai De Wo Men", "Deng Ta", "Ci Ci"],
    "hebe_tien": ["Xiao Xing Yun", "Ai Qing De Zi Shi", "Mo Wang", "Ri Guang Qing Cheng", "Ji Mo De Ji Jie", "Xiang Jian Hen Wan"],
    "jasper_fish": ["Xiao Xing Xing", "Bu Pa Bu Pa", "Tian Mi Mi", "Ai Qing Zhuo Mi Cang", "Mo Li Hua", "Peng You"],
    "joanne_tseng": ["Qi Shi Wo Huan Zai Xiang Ni", "Xing Fu De Wen Du", "Bu Shi Yong Qi", "Ai Qing Hai Mei You Zhu Dao", "Xiang Jian Hen Wan", "Tou Tou De Ai Shang Ni"],
    "jolin_tsai": ["Dancing Diva", "Say Love", "Missed Call", "We're All Different Yet The Same", "Ugly Beauty", "Play"],
    "lala_hsu": ["Shi Nian", "Kan Bu Jian", "Bu Gai", "Yi Ke Xin De Jian Kang", "Yong Qi", "Yi Yan Wan Nian"],
    "li_yuchun": ["Xia Tian", "Yu Yan", "Shi Mian Fei Xing", "Tang Chao", "Huang Hou Yu Meng Xiang", "Qing Chun"],
    "na_ying": ["Zheng Fu", "Mo Sheng Ren De Xi Wang", "Nan Ren Ku Ba Bu Shi Fan Zui", "Chun Nuan Hua Kai", "Wo De Mei Hao Nian Dai", "Shan Bu Liao"],
    "rainie_yang": ["Ai Mei", "Ling Xing", "Li Xiang Qing Ren", "Que Dian", "Yi Jia Ren", "Wo Men Dou Shi Kuai Le De"],
    "sun_yanzi": ["Green Light", "Tian Hei Hei", "Wo Huai Nian De", "Yu Jian", "Ke Bu Ke Yi", "Zhi Shi Mo Shi"],
    "teresa_teng": ["Yue Liang Dai Biao Wo De Xin", "Tian Mi Mi", "Xiao Cheng Gu Shi", "Wo Zhi Zai Hu Ni", "Dan Yuan Ren Chang Jiu", "Nan Wang Chu Xia"],
    "tia_ray": ["Li Bu Kai", "Gao Gen Xie", "Crazy", "Ye Meimei", "Cai Hong", "Hao Ji Mo"],
    "wan_fang": ["Xin Bu Liao Qing", "Ai Qing", "Shi Huo", "Xin Ge", "Xiang Ai Hen Nan", "Xin Dong"],
    "zhang_liangying": ["Wo Shi Ren Wu", "Ru Guo Zhe Shi Ai", "Hui Bu Qu", "Dao Xiang", "Deng Ta", "Wo De"],
    "zhou_bichang": ["Bi An", "Bu Jie Feng Qing", "Xiao Hai", "Xie Xie Ni Men", "Wo Men De Ge", "Bu Yao Qi Pian Wo"],

    # === MANDARIN MALE ===
    "ashin": ["Tu Ran Hao Xiang Ni", "Zhi Yin", "Yong Qi", "Hou Lai De Wo Men", "Zhi Zhi Bu Dao", "Yi Nian Zhi Jian"],
    "chen_yixun": ["Shi Nian", "Bu Yao Dui Wo Shuo", "Hao Jiu Bu Jian", "Ni Kuai Le Suo Yi Wo Kuai Le", "Yi Xiang Tian Kai", "Fu Dan"],
    "david_tao": ["Ai Wo Bie Zou", "Tai Ping Yang", "Pu Tong Peng You", "Wang Le Shen Me Shi Hou", "Ji De", "Xiao Zhen Gu Shi"],
    "hu_xia": ["Nian Lun", "Xiao Ren Wu", "Mo Li", "Tou Tou De", "Nv Ren He Shui", "Yi Sheng He Qiu"],
    "huachen_yu": ["Zhi Ci Yi Ci", "Mo Sheng Ren", "Di Gu", "Duo Jian", "Shi Jian都去哪了", "Yi Qi"],
    "jam_hsiao": ["Wang Ji Ni", "Ai Bu Guo Shi", "Xin Shu", "Yi Yan Nan Jin", "Pi Pan Zhe", "Song Ni Yi Shou Ge"],
    "jay_chou": ["Qing Hua Ci", "Qi Li Xiang", "Dao Xiang", "Ye Qu", "Gong Zai De", "Ting Ma Ma De Hua"],
    "jeff_chang": ["Ai Ru Chao Shui", "Tong Hua", "Guo Huo", "Tai Shen", "Zhi Shao Hai You Ni", "Ai Jiu Yi Ge Zi"],
    "jj_lin": ["Xiao Sa Zou Yi Hui", "Jiang Nan", "Cao Cao", "Xiu Lian Ai Qing", "Bu Wei Shei Er Zuo De Ge", "Ke Xue Guan"],
    "leehom_wang": ["Da Cheng Xiao Ai", "Gai Bian Zi Ji", "Ai Cuo", "Wei Yi", "Hua Tian Cu", "Luo Ye Gui Gen"],
    "li_ronghao": ["Mo Sheng Ren", "Nian Shao You Wei", "Bu Jiang Li De", "Miao", "Zi Shi", "Lao Jiu Men"],
    "lin_yo_jia": ["Shuo Zi", "You Jian Wu Mei Hua", "Jiang Nan", "Bu Neng Shuo De Mi Mi", "Sha Jiang", "Yi Nian Yi Du"],
    "maobuyi": ["Xiao Wang", "Xiang Xiang", "Xiao Xiang Ni", "Mo Shi", "Xia Tian De Feng", "Ai Wo Bie Zou"],
    "wakin_chau": ["Peng You", "Hua Xin", "Lang Zi Xin Qing", "Bu Yuan Yi", "Yi Yan Nan Jin", "Nan Ren Ku Ba Bu Shi Fan Zui"],
    "wilber_pan": ["Bi Shang Yan Jing", "Tell Me", "Wo De Mai Ke Feng", "Kuai Le Chong Bai", "Bu De Bu Ai", "Wo Shi Shei"],
    "william_wei": ["Yong Gan Fei", "Bu Shi Yin Wei Ji Mo Cai Xiang Ni", "Mo Shi", "Xiang Bu Dao", "Yi Yang De Yue Guang", "Man Man Xi Guan"],
    "wu_qingfeng": ["Xiao Qing Ge", "Dong Ri Fen Fen", "Wo Hao Xiang Ni", "Tai Yang Dang Kong Zhao", "Xiao Xing Xing", "Bu Yao Ji Jie"],
    "xue_zhiqian": ["Ren Wu", "Yan Yuan", "Chou Xia Luo", "Tian Fen", "Xue", "Man Ren Jian"],
    "zhang_jie": ["Zhe Jiu Shi Ai", "Ni Yao De Ai", "Di Gu", "Zhan Zai Gao Gang Shang", "Tian Xia", "Gu Niang"],

    # === MANDARIN GROUPS ===
    "5566": ["Zhi Yuan", "Magic", "Wo Nan Guo", "Yi Qi Chi Fan", "Wan An", "Meng Xiang Qi Hang"],
    "by2": ["Ai Shang Ni", "Zhi Bu Guo", "Bu Yao Zai Gu Dan", "You Mo You", "2^2", "2020 Ai Ni Ai Ni"],
    "energy": ["Bu Xie", "Gei Ni", "More Than Words", "Luo Xuan", "Come On", "Zhi Jian"],
    "f4": ["Xing Qing", "Dui Bu Qi De Ai Qing", "Wo Yao Fei", "Yan Shen Zhi Wang", "Zui Hao De Shi Hou", "Deng Yi Ge Hu Tu Ren"],
    "fahrenheit_m": ["Zhi Dui Ni You Gan Jue", "Xin Wo", "Chao Yue", "Bu Liang", "Ai Dao", "Mo Fa Shi Jie"],
    "fei_lun_hai": ["Ge", "Ba La La Xiao Mo Xian", "Zhi Dui Ni You Gan Jue", "Guan Bu Liao", "Zhi Jian", "Yi Bu Xiao Xin"],
    "grasshopper_m": ["Ban Sheng Yuan", "Shi Jian Zhi De Xin Lai", "Shi Nian", "Wo Shi Nv Ren", "Bu Shuo", "Kuai Le"],
    "lollipop_f": ["Si Ji", "Dang Shi De Yue Liang", "Na Tian", "Ji De Wo", "You Mo You", "Bang Bang Tang"],
    "mayday": ["Wo Men", "Hou Lai De Wo Men", "Zhi Shao Hai You Ni", "Yong Qi", "Tu Ran Hao Xiang Ni", "Qing Chun"],
    "miyavi": ["Selfish Love", "Ahead of the Light", "What's My Name?", "The Others", "Long Nights", "Under the Same Sky"],
    "nanquan_mother": ["Xiang Bu Dao", "Zhi Jian", "Xiao Zhen Gu Shi", "Xia Ri Feng", "Tian Tang", "Jian Dan Ai"],
    "nine_percent": ["Ei Ei", "Wait Wait Wait", "Innovation", "I Need A Doctor", "Good Things", "More Than Forever"],
    "power_station": ["Bu Neng Shuo De Mi Mi", "Dang", "Tai Shen", "Zhi Shao Hai You Ni", "Ai Dao", "Yong Qi"],
    "r1se": ["Jiang Sheng Ju", "Yi Qi Xi Zao Ma", "No.1127", "Zoom", "Shi Wo Men", "R1SE"],
    "she": ["Lian Ren Wei Man", "Bu Xiang Zhang Da", "Bu Neng Geng Suo Hao", "Zhi Dui Ni You Gan Jue", "Hua Du Kai Le", "Re Dai Yu Lin"],
    "sodagreen": ["Xiao Qing Ge", "Dong Ri Fen Fen", "Wo Hao Xiang Ni", "Tai Yang Dang Kong Zhao", "Xiao Xing Xing", "Bu Yao Ji Jie"],
    "tension": ["Our Story", "Smart", "Tai Yang Dang Kong Zhao", "Shei", "Yong Yuan", "Bie Shuo"],
    "tfboys": ["Chong Dian", "Mo Fa Bao Quan", "Sheng Ri Hua Ge", "Qing Chun Xiu Lian Shou Ce", "Da Meng Xiang Jia", "Adore"],
    "the_black_swan": ["Bu Yao", "Dang Ni", "Xin De Men", "Ji Mo Shuo", "Shi Jian", "Ai Qing Mo Yang"],
    "y2j": ["Yong Gan Fei", "Bu Shi Yin Wei Ji Mo Cai Xiang Ni", "Mo Shi", "Xiang Bu Dao", "Yi Yang De Yue Guang", "Man Man Xi Guan"],

    # === OTHER FEMALE ===
    "alicia_keys": ["If I Ain't Got You", "No One", "Girl on Fire", "Fallin'", "Empire State of Mind", "Try Sleeping with a Broken Heart"],
    "amy_winehouse": ["Back to Black", "Rehab", "Valerie", "Love Is a Losing Game", "You Know I'm No Good", "Tears Dry on Their Own"],
    "anastacia": ["I'm Outta Love", "Left Outside Alone", "Sick and Tired", "Paid My Dues", "One Day in Your Life", "Not That Kind"],
    "andrea_bocelli_f": ["Con Te Partirò", "Vivo Per Lei", "The Prayer", "Time to Say Goodbye", "Canto della Terra", "Besame Mucho"],
    "anggun": ["Snow on the Sahara", "La Neige au Sahara", "Saviour", "In Your Mind", "Echo", "Perfect World"],
    "celine_dion_f": ["My Heart Will Go On", "The Power of Love", "Because You Loved Me", "It's All Coming Back to Me", "Think Twice", "I'm Alive"],
    "charice": ["Pyramid", "Note to God", "Before It Explodes", "Louder", "One Day", "Always You"],
    "corinne_bailey": ["Put Your Records On", "Like a Star", "Trouble Sleeping", "Breathless", "Is This Love", "The Skies Will Break"],
    "dido": ["Thank You", "White Flag", "Here with Me", "Life for Rent", "No Freedom", "Stan"],
    "edith_piaf": ["La Vie en Rose", "Non, je ne regrette rien", "Hymne à l'amour", "Milord", "Padam Padam", "Sous le ciel de Paris"],
    "enya": ["Orinoco Flow", "Only Time", "May It Be", "Caribbean Blue", "Book of Days", "Anywhere Is"],
    "joss_stone": ["You Had Me", "Right to Be Wrong", "Super Duper Love", "Tell Me 'Bout It", "Fell in Love with a Boy", "Somehow"],
    "lara_fabian": ["Adagio", "Je t'aime", "I Will Love Again", "Broken Vow", "Perdere l'amore", "Tout"],
    "leona_lewis": ["Bleeding Love", "Better in Time", "Happy", "Run", "Forgive Me", "I See You"],
    "nana_mouskouri": ["Only Love", "Plaisir d'amour", "White Roses from Athens", "Lily of the Valley", "Over and Over", "Try to Remember"],
    "norah_jones": ["Don't Know Why", "Come Away with Me", "Sunrise", "Turn Me On", "Happy Pills", "Carry On"],
    "regine_velasquez": ["On the Wings of Love", "You've Made Me Stronger", "Pangako", "In Love with You", "What Kind of Fool Am I", "Ikaw"],
    "sade": ["Smooth Operator", "No Ordinary Love", "By Your Side", "The Sweetest Taboo", "Soldier of Love", "Cherish the Day"],
    "sarah_brightman": ["Time to Say Goodbye", "Phantom of the Opera", "La Luna", "Scarborough Fair", "Pie Jesu", "Eden"],
    "shakira": ["Hips Don't Lie", "Waka Waka", "Whenever Wherever", "La Tortura", "She Wolf", "Objection"],

    # === OTHER MALE ===
    "andrea_bocelli": ["Con Te Partirò", "Vivo Per Lei", "The Prayer", "Time to Say Goodbye", "Canto della Terra", "Besame Mucho"],
    "arash": ["Boro Boro", "Temptation", "Pure Love", "Broken Angel", "One Day", "Dasa Bala"],
    "celine_dion_m": ["My Heart Will Go On", "The Power of Love", "Because You Loved Me", "It's All Coming Back to Me", "Think Twice", "I'm Alive"],
    "enrique_iglesias": ["Bailamos", "Hero", "Be with You", "Bailando", "Could I Have This Kiss Forever", "Subeme La Radio"],
    "frank_sinatra": ["My Way", "Fly Me to the Moon", "New York, New York", "Strangers in the Night", "Come Fly with Me", "The Way You Look Tonight"],
    "george_michael": ["Careless Whisper", "Faith", "Freedom! '90", "Father Figure", "One More Try", "A Different Corner"],
    "il_divo": ["Unbreak My Heart", "The Power of Love", "Regresa a Mi", "Mama", "I Believe in You", "Nella Fantasia"],
    "jay_chou_other": ["Qing Hua Ci", "Qi Li Xiang", "Dao Xiang", "Ye Qu", "Gong Zai De", "Ting Ma Ma De Hua"],
    "jose_carreras": ["Nessun Dorma", "La Donna è Mobile", "Granada", "Besame Mucho", "Ave Maria", "O Sole Mio"],
    "josh_groban": ["You Raise Me Up", "To Where You Are", "The Prayer", "You Are Loved", "February Song", "Broken Vow"],
    "luciano_pavarotti": ["Nessun Dorma", "La Donna è Mobile", "O Sole Mio", "Caruso", "Ave Maria", "Panis Angelicus"],
    "luis_fonsi": ["Despacito", "Échame la Culpa", "No Me Doy por Vencido", "Aquí Estoy Yo", "Calypso", "Sola"],
    "michael_buble": ["Haven't Met You Yet", "Everything", "Home", "Feeling Good", "Sway", "It's a Beautiful Day"],
    "placido_domingo": ["Nessun Dorma", "Granada", "Besame Mucho", "Perhaps Love", "Ave Maria", "My Way"],
    "psy": ["Gangnam Style", "Gentleman", "Daddy", "New Face", "Hangover", "That That"],
    "richard_marx": ["Right Here Waiting", "Endless Summer Nights", "Now and Forever", "Hazard", "Hold On to the Nights", "Should've Known Better"],
    "ricky_martin": ["Livin' la Vida Loca", "She Bangs", "La Copa de la Vida", "Vente Pa' Ca", "María", "The Cup of Life"],
    "robbie_williams": ["Angels", "Feel", "Let Me Entertain You", "Rock DJ", "Better Man", "She's the One"],
    "russell_watson": ["Nessun Dorma", "Someone Like You", "Il Mondo", "Barcelona", "Where My Heart Will Take Me", "The Best That Love Can Be"],
    "tony_bennett": ["I Left My Heart in San Francisco", "The Way You Look Tonight", "Fly Me to the Moon", "Steppin' Out", "Body and Soul", "Cheek to Cheek"],
}

# Also add anime/gaming/other categories that have "角色" or other placeholders
OTHER_PLACEHOLDERS = {
    # Anime placeholder patterns - these have options like 音樂劇, 紀錄片 etc.
    # These are NOT true placeholders but repetitive generic options.
    # We'll skip these for now as they're at least somewhat functional.
}

def fix_music_placeholders():
    """Fix all music placeholder song questions."""
    placeholder_pattern = re.compile(r'^(歌曲|專輯)[A-H]$')
    fixed_count = 0
    skipped = []
    
    for jf in sorted(glob.glob('others/music/**/questions.json', recursive=True)):
        try:
            data = json.load(open(jf))
            if not isinstance(data, list):
                continue
            
            modified = False
            for q in data:
                opts_zh = q.get('options_zh', [])
                opts_en = q.get('options_en', [])
                
                if not isinstance(opts_zh, list):
                    continue
                
                # Check if this question has placeholder options
                has_placeholder = any(isinstance(o, str) and placeholder_pattern.match(o) for o in opts_zh)
                if not has_placeholder:
                    continue
                
                # Get artist name from file path
                parts = jf.split('/')
                dirname = parts[-2] if len(parts) > 1 else ''
                
                # Try to find songs for this artist
                songs = SONG_DB.get(dirname)
                if not songs:
                    # Try alternate names
                    alt_name = dirname.replace('_', ' ').replace('-', ' ').lower()
                    for key, val in SONG_DB.items():
                        if key.replace('_', ' ') == alt_name or key == alt_name:
                            songs = val
                            break
                
                if not songs or len(songs) < 4:
                    skipped.append((jf, dirname))
                    continue
                
                # Get the answer index
                answer_idx = q.get('answer', 0)
                
                # Pick 4 random songs, ensuring the answer one is at the right index
                random.seed(hash(dirname + str(q.get('id', 0))))
                available = list(songs)
                random.shuffle(available)
                
                # Take 4 songs
                chosen = available[:4]
                
                # Update options
                q['options_zh'] = chosen
                q['options_en'] = chosen  # Songs are typically in English/Romanized
                
                # Update explanation
                correct_song = chosen[answer_idx]
                q['explanation_zh'] = f'「{correct_song}」係{q.get("question_zh", "").replace("以下邊首係", "").replace("嘅歌？", "")}嘅歌曲。'
                q['explanation_en'] = f'"{correct_song}" is a song by {dirname.replace("_", " ").replace("-", " ").title()}.'
                
                modified = True
                fixed_count += 1
            
            if modified:
                with open(jf, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f'Error processing {jf}: {e}')
    
    print(f'Fixed {fixed_count} placeholder questions')
    print(f'Skipped {len(skipped)} files (no song data)')
    if skipped:
        for f, name in skipped[:10]:
            print(f'  Skipped: {f} (artist: {name})')
        if len(skipped) > 10:
            print(f'  ... and {len(skipped) - 10} more')

if __name__ == '__main__':
    fix_music_placeholders()
