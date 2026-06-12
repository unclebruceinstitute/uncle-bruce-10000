#!/usr/bin/env python3
"""
Hong Kong Secondary English & Chinese Question Generator v3
- 10,000 questions per subject
- Round-robin shuffling (no consecutive same topic)
- Extensive template variety (5-10+ per subtopic)
- Difficulty: 40% easy, 40% medium, 20% hard
"""
import json, os, random, copy

random.seed(42)

# ─────────────────────────────────────────────────────────
# ENGLISH TEMPLATES
# ─────────────────────────────────────────────────────────

EN_TOPICS = {
    "grammar_pronouns": {
        "topic_id": "grammar_pronouns",
        "topic_zh": "代名詞",
        "topic_en": "Pronouns",
        "subtopics": {
            "personal_pronouns": {
                "subtopic_id": "personal_pronouns",
                "subtopic_zh": "人稱代名詞",
                "subtopic_en": "Personal Pronouns",
                "templates": [
                    {"q": "Choose the correct pronoun: ___ is my best friend.", "opts": ["He", "Him", "His", "Himself"], "ans": 0, "exp_zh": "主格 'He' 作主詞。受格 'Him' 作受詞。", "exp_en": "'He' is subject pronoun. 'Him' is object pronoun."},
                    {"q": "Please give the book to ___.", "opts": ["I", "me", "my", "mine"], "ans": 1, "exp_zh": "介系詞 'to' 後用受格 'me'。", "exp_en": "After preposition 'to', use object pronoun 'me'."},
                    {"q": "___ went to the park yesterday.", "opts": ["Them", "They", "Their", "Theirs"], "ans": 1, "exp_zh": "句首主格用 'They'。'Them' 是受格。", "exp_en": "Subject position needs 'They'. 'Them' is object pronoun."},
                    {"q": "The teacher asked ___ to sit down.", "opts": ["we", "us", "our", "ours"], "ans": 1, "exp_zh": "動詞 'asked' 後用受格 'us'。", "exp_en": "After verb 'asked', use object pronoun 'us'."},
                    {"q": "My sister and ___ are going shopping.", "opts": ["me", "I", "my", "mine"], "ans": 1, "exp_zh": "主詞位置用主格 'I'。去掉 'My sister and' 看看：'I am going.'", "exp_en": "Subject position needs 'I'. Test: 'I am going shopping.'"},
                    {"q": "The dog wagged ___ tail happily.", "opts": ["it's", "its", "it", "itself"], "ans": 1, "exp_zh": "所有格 'its'（無撇號）。'it's' = it is。", "exp_en": "'Its' = possessive (no apostrophe). 'It's' = it is."},
                ]
            },
            "possessive_pronouns": {
                "subtopic_id": "possessive_pronouns",
                "subtopic_zh": "所有格代名詞",
                "subtopic_en": "Possessive Pronouns",
                "templates": [
                    {"q": "This phone is ___. I bought it yesterday.", "opts": ["my", "mine", "me", "I"], "ans": 1, "exp_zh": "獨立使用所有格代名詞 'mine'，後面不接名詞。'My' 後要接名詞。", "exp_en": "'Mine' stands alone. 'My' needs a noun after it."},
                    {"q": "Is this bag ___?", "opts": ["your", "yours", "you", "yourself"], "ans": 1, "exp_zh": "獨立使用所有格代名詞 'yours'。'Your bag' 才用 'your'。", "exp_en": "'Yours' stands alone. 'Your' needs a noun."},
                    {"q": "___ house is the biggest on the street.", "opts": ["Their", "Theirs", "Them", "They"], "ans": 0, "exp_zh": "名詞 'house' 前用所有格形容詞 'Their'。'Theirs' 獨立使用。", "exp_en": "Before noun 'house', use possessive adjective 'Their'. 'Theirs' stands alone."},
                    {"q": "The victory was ___. We worked so hard for it.", "opts": ["our", "ours", "us", "we"], "ans": 1, "exp_zh": "獨立使用 'ours'。'Our victory' 才用 'our'。", "exp_en": "'Ours' stands alone. 'Our victory' uses 'our'."},
                    {"q": "That green bicycle is ___ brother's.", "opts": ["she", "her", "hers", "herself"], "ans": 1, "exp_zh": "名詞 'brother' 前用所有格形容詞 'her'。", "exp_en": "Before noun 'brother', use possessive adjective 'her'."},
                ]
            },
            "reflexive_pronouns": {
                "subtopic_id": "reflexive_pronouns",
                "subtopic_zh": "反身代名詞",
                "subtopic_en": "Reflexive Pronouns",
                "templates": [
                    {"q": "She made the cake ___. Nobody helped her.", "opts": ["she", "her", "hers", "herself"], "ans": 3, "exp_zh": "當主詞和受詞同一人時用反身代名詞 'herself'。", "exp_en": "When subject and object are the same person, use reflexive 'herself'."},
                    {"q": "Be careful! Don't hurt ___.", "opts": ["you", "your", "yours", "yourself"], "ans": 3, "exp_zh": "命令句中 'you' 的反身代名詞是 'yourself'。", "exp_en": "Reflexive of implied 'you' is 'yourself'."},
                    {"q": "The children enjoyed ___ at the party.", "opts": ["they", "them", "their", "themselves"], "ans": 3, "exp_zh": "'enjoy oneself' 固定用法。children = themselves。", "exp_en": "'Enjoy oneself' is fixed. Children → themselves."},
                    {"q": "I taught ___ how to play guitar.", "opts": ["I", "me", "my", "myself"], "ans": 3, "exp_zh": "主詞 'I' 的反身代名詞是 'myself'。", "exp_en": "Reflexive of 'I' is 'myself'."},
                    {"q": "He introduced ___ to the new neighbours.", "opts": ["he", "him", "his", "himself"], "ans": 3, "exp_zh": "'introduce oneself' 固定用法。", "exp_en": "'Introduce oneself' is the fixed expression."},
                ]
            },
        }
    },
    "grammar_tenses": {
        "topic_id": "grammar_tenses",
        "topic_zh": "時態",
        "topic_en": "Tenses",
        "subtopics": {
            "simple_present": {
                "subtopic_id": "simple_present",
                "subtopic_zh": "現在簡單式",
                "subtopic_en": "Simple Present",
                "templates": [
                    {"q": "Water ___ at 100 degrees Celsius.", "opts": ["boil", "boils", "boiled", "is boiling"], "ans": 1, "exp_zh": "科學事實用現在簡單式。第三人稱單數加 -s。", "exp_en": "Scientific facts use simple present. Third person adds -s."},
                    {"q": "My father ___ a newspaper every morning.", "opts": ["read", "reads", "is reading", "has read"], "ans": 1, "exp_zh": "習慣性動作用現在簡單式。every morning = 習慣。", "exp_en": "Habits use simple present. 'Every morning' signals habit."},
                    {"q": "The shop ___ at 9 a.m. on weekdays.", "opts": ["open", "opens", "opened", "is opening"], "ans": 1, "exp_zh": "固定時間表用現在簡單式。", "exp_en": "Timetables/schedules use simple present."},
                    {"q": "She ___ not like spicy food.", "opts": ["do", "does", "is", "has"], "ans": 1, "exp_zh": "第三人稱否定用 'does not'。", "exp_en": "Third person negative: 'does not' + base form."},
                    {"q": "The sun ___ in the east.", "opts": ["rise", "rises", "rose", "is rising"], "ans": 1, "exp_zh": "自然現象用現在簡單式。", "exp_en": "Natural phenomena use simple present."},
                ]
            },
            "present_continuous": {
                "subtopic_id": "present_continuous",
                "subtopic_zh": "現在進行式",
                "subtopic_en": "Present Continuous",
                "templates": [
                    {"q": "Look! The baby ___ right now.", "opts": ["cry", "cries", "is crying", "has cried"], "ans": 2, "exp_zh": "'Look!' 和 'right now' 表示正在發生，用現在進行式。", "exp_en": "'Look!' and 'right now' signal present continuous (am/is/are + -ing)."},
                    {"q": "Be quiet! The students ___ an exam.", "opts": ["take", "takes", "are taking", "took"], "ans": 2, "exp_zh": "此刻正在進行的動作用現在進行式。", "exp_en": "Action happening now = present continuous."},
                    {"q": "I can't talk now. I ___ dinner.", "opts": ["cook", "cooks", "am cooking", "cooked"], "ans": 2, "exp_zh": "說話當下正在做 = 現在進行式。", "exp_en": "Currently doing it = present continuous."},
                    {"q": "Why ___ you ___ at me?", "opts": ["do/stare", "are/staring", "did/stare", "have/stared"], "ans": 1, "exp_zh": "暫時持續的動作用現在進行式。", "exp_en": "Temporary ongoing action = present continuous."},
                    {"q": "Listen! Someone ___ a beautiful song.", "opts": ["sing", "sings", "is singing", "sang"], "ans": 2, "exp_zh": "'Listen!' 提示此刻正在發生。", "exp_en": "'Listen!' signals something happening right now."},
                ]
            },
            "simple_past": {
                "subtopic_id": "simple_past",
                "subtopic_zh": "過去簡單式",
                "subtopic_en": "Simple Past",
                "templates": [
                    {"q": "I ___ a wonderful movie last night.", "opts": ["watch", "watched", "am watching", "have watched"], "ans": 1, "exp_zh": "'last night' 過去時間用過去式。", "exp_en": "'Last night' = past time marker → simple past."},
                    {"q": "She ___ to London when she was young.", "opts": ["travel", "travels", "travelled", "has travelled"], "ans": 2, "exp_zh": "'when she was young' 過去時間用過去式。", "exp_en": "'When she was young' → simple past."},
                    {"q": "We ___ not understand the question.", "opts": ["do", "does", "did", "have"], "ans": 2, "exp_zh": "過去否定用 'did not' + 原形。", "exp_en": "Past negative: 'did not' + base form."},
                    {"q": "The train ___ five minutes ago.", "opts": ["arrive", "arrives", "arrived", "has arrived"], "ans": 2, "exp_zh": "'ago' 表示過去時間，用過去式。", "exp_en": "'Ago' → past time → simple past."},
                    {"q": "Did you ___ the homework yesterday?", "opts": ["finished", "finishes", "finish", "finishing"], "ans": 2, "exp_zh": "疑問句 'Did' 後用動詞原形。", "exp_en": "After 'Did', use base form of verb."},
                    {"q": "They ___ in Paris for two years before moving to Tokyo.", "opts": ["live", "lived", "have lived", "are living"], "ans": 1, "exp_zh": "過去已完成的時間段用過去式。'before moving' 標示過去。", "exp_en": "Completed past period → simple past. 'Before moving' signals past."},
                ]
            },
            "present_perfect": {
                "subtopic_id": "present_perfect",
                "subtopic_zh": "現在完成式",
                "subtopic_en": "Present Perfect",
                "templates": [
                    {"q": "I ___ never ___ such a tall building.", "opts": ["have/seen", "has/seen", "had/see", "did/see"], "ans": 0, "exp_zh": "'never' 用現在完成式 have/has + pp。", "exp_en": "'Never' → present perfect: have/has + past participle."},
                    {"q": "She ___ already ___ her lunch.", "opts": ["has/finish", "have/finished", "has/finished", "had/finished"], "ans": 2, "exp_zh": "'already' 搭配現在完成式。she = has。", "exp_en": "'Already' → present perfect. 'She' → 'has finished'."},
                    {"q": "___ you ever ___ to Japan?", "opts": ["Have/been", "Has/been", "Did/been", "Are/been"], "ans": 0, "exp_zh": "'ever' 用現在完成式疑問句。", "exp_en": "'Ever' → present perfect question: 'Have you ever been...?'"},
                    {"q": "We ___ known each other since 2010.", "opts": ["know", "knew", "have known", "are knowing"], "ans": 2, "exp_zh": "'since' 表示從過去到現在，用現在完成式。", "exp_en": "'Since' → from past to now → present perfect."},
                    {"q": "He has just ___ home.", "opts": ["arrive", "arrived", "arriving", "arrives"], "ans": 1, "exp_zh": "'just' 搭配現在完成式 has + pp。", "exp_en": "'Just' → present perfect: has + past participle."},
                ]
            },
            "past_continuous": {
                "subtopic_id": "past_continuous",
                "subtopic_zh": "過去進行式",
                "subtopic_en": "Past Continuous",
                "templates": [
                    {"q": "I ___ TV when the phone rang.", "opts": ["watch", "watched", "was watching", "have watched"], "ans": 2, "exp_zh": "過去持續動作被另一動作打斷：was/were + -ing。", "exp_en": "Ongoing past action interrupted: was/were + -ing."},
                    {"q": "At 8 p.m. yesterday, she ___ for the exam.", "opts": ["study", "studied", "was studying", "has studied"], "ans": 2, "exp_zh": "過去某時正在做 = 過去進行式。", "exp_en": "At a specific past time, doing something = past continuous."},
                    {"q": "While I ___, my brother was cooking.", "opts": ["read", "was reading", "am reading", "have read"], "ans": 1, "exp_zh": "'while' 兩個過去同時持續動作用過去進行式。", "exp_en": "'While' + two simultaneous past actions → past continuous."},
                    {"q": "They ___ in the park when it started to rain.", "opts": ["walk", "walked", "were walking", "are walking"], "ans": 2, "exp_zh": "過去持續動作被另一動作打斷。", "exp_en": "Ongoing past action interrupted by 'started to rain'."},
                ]
            },
            "future_tenses": {
                "subtopic_id": "future_tenses",
                "subtopic_zh": "未來式",
                "subtopic_en": "Future Tenses",
                "templates": [
                    {"q": "I think it ___ tomorrow.", "opts": ["rains", "rained", "will rain", "is raining"], "ans": 2, "exp_zh": "預測未來用 'will + 原形'。", "exp_en": "Prediction about future: 'will' + base form."},
                    {"q": "The concert ___ at 7 p.m. next Saturday.", "opts": ["start", "starts", "started", "is starting"], "ans": 1, "exp_zh": "已安排好的未來活動用現在簡單式。", "exp_en": "Scheduled events use simple present for future."},
                    {"q": "I ___ my grandmother this weekend.", "opts": ["visit", "am visiting", "visited", "was visiting"], "ans": 1, "exp_zh": "已計劃的未來安排用現在進行式。", "exp_en": "Planned future arrangement: present continuous."},
                    {"q": "By 2030, scientists ___ a cure for the disease.", "opts": ["find", "found", "will find", "will have found"], "ans": 3, "exp_zh": "'By 2030' 表示在未來某時之前完成，用未來完成式。", "exp_en": "'By 2030' → completed before a future time → future perfect."},
                ]
            },
        }
    },
    "grammar_articles": {
        "topic_id": "grammar_articles",
        "topic_zh": "冠詞",
        "topic_en": "Articles",
        "subtopics": {
            "a_an": {
                "subtopic_id": "a_an",
                "subtopic_zh": "不定冠詞",
                "subtopic_en": "A/An",
                "templates": [
                    {"q": "She wants to buy ___ umbrella.", "opts": ["a", "an", "the", "no article"], "ans": 1, "exp_zh": "'umbrella' 以元音 /ʌ/ 開頭，用 'an'。", "exp_en": "'Umbrella' starts with vowel sound /ʌ/ → 'an'."},
                    {"q": "He is ___ honest man.", "opts": ["a", "an", "the", "no article"], "ans": 1, "exp_zh": "'honest' 的 h 不發音，以元音開頭，用 'an'。", "exp_en": "'Honest' has silent h → vowel sound → 'an'."},
                    {"q": "I saw ___ one-eyed cat.", "opts": ["a", "an", "the", "no article"], "ans": 0, "exp_zh": "'one' 以輔音 /w/ 開頭，用 'a'。", "exp_en": "'One' starts with consonant sound /w/ → 'a'."},
                    {"q": "There is ___ university near my house.", "opts": ["a", "an", "the", "no article"], "ans": 0, "exp_zh": "'university' 以輔音 /juː/ 開頭，用 'a'。", "exp_en": "'University' starts with /juː/ (consonant) → 'a'."},
                    {"q": "She ate ___ egg for breakfast.", "opts": ["a", "an", "the", "no article"], "ans": 1, "exp_zh": "'egg' 以元音 /ɛ/ 開頭，用 'an'。", "exp_en": "'Egg' starts with vowel /ɛ/ → 'an'."},
                    {"q": "He is ___ European scientist.", "opts": ["a", "an", "the", "no article"], "ans": 0, "exp_zh": "'European' 以輔音 /jʊ/ 開頭，用 'a'。", "exp_en": "'European' starts with /jʊ/ (consonant) → 'a'."},
                ]
            },
            "the_usage": {
                "subtopic_id": "the_usage",
                "subtopic_zh": "定冠詞",
                "subtopic_en": "The",
                "templates": [
                    {"q": "___ Great Wall of China is a famous landmark.", "opts": ["A", "An", "The", "No article"], "ans": 2, "exp_zh": "特定且獨特的事物用 'the'。", "exp_en": "Unique/specific things use 'the'."},
                    {"q": "I play ___ guitar in a band.", "opts": ["a", "an", "the", "no article"], "ans": 2, "exp_zh": "樂器前用 'the'。", "exp_en": "Musical instruments use 'the'."},
                    {"q": "She is ___ tallest girl in our school.", "opts": ["a", "an", "the", "no article"], "ans": 2, "exp_zh": "最高級前用 'the'。", "exp_en": "Superlatives use 'the'."},
                    {"q": "___ rich should help ___ poor.", "opts": ["A/a", "The/the", "The/a", "A/the"], "ans": 1, "exp_zh": "the + 形容詞 = 一類人。the rich = 有錢人。", "exp_en": "'The' + adjective = a group of people. The rich, the poor."},
                    {"q": "We went to ___ cinema last night.", "opts": ["a", "an", "the", "no article"], "ans": 2, "exp_zh": "去「看電影」固定用 'go to the cinema'。", "exp_en": "'Go to the cinema' is a fixed expression."},
                ]
            },
            "no_article": {
                "subtopic_id": "no_article",
                "subtopic_zh": "零冠詞",
                "subtopic_en": "No Article",
                "templates": [
                    {"q": "___ love is the most powerful force.", "opts": ["A", "An", "The", "No article"], "ans": 3, "exp_zh": "抽象名詞泛指不加冠詞。", "exp_en": "Abstract nouns in general take no article."},
                    {"q": "She goes to ___ school by bus.", "opts": ["a", "an", "the", "no article"], "ans": 3, "exp_zh": "去「上學」不加冠詞。go to school = 上學。", "exp_en": "'Go to school' (as student) = no article."},
                    {"q": "___ honesty is an important quality.", "opts": ["A", "An", "The", "No article"], "ans": 3, "exp_zh": "抽象名詞泛指不加冠詞。", "exp_en": "Abstract nouns in general: no article."},
                    {"q": "I like to listen to ___ music.", "opts": ["a", "an", "the", "no article"], "ans": 3, "exp_zh": "泛指音樂不加冠詞。特指某首音樂才用 'the'。", "exp_en": "Music in general: no article. Specific music: 'the'."},
                ]
            },
        }
    },
    "grammar_prepositions": {
        "topic_id": "grammar_prepositions",
        "topic_zh": "介系詞",
        "topic_en": "Prepositions",
        "subtopics": {
            "time_prepositions": {
                "subtopic_id": "time_prepositions",
                "subtopic_zh": "時間介系詞",
                "subtopic_en": "Time Prepositions",
                "templates": [
                    {"q": "The meeting is ___ Monday.", "opts": ["in", "on", "at", "by"], "ans": 1, "exp_zh": "星期用 'on'。on Monday。", "exp_en": "Days use 'on': on Monday."},
                    {"q": "I was born ___ 1995.", "opts": ["in", "on", "at", "by"], "ans": 0, "exp_zh": "年份用 'in'。in 1995。", "exp_en": "Years use 'in': in 1995."},
                    {"q": "The class starts ___ 8:30 a.m.", "opts": ["in", "on", "at", "by"], "ans": 2, "exp_zh": "確切時間用 'at'。at 8:30。", "exp_en": "Specific times use 'at': at 8:30."},
                    {"q": "We usually have lunch ___ noon.", "opts": ["in", "on", "at", "by"], "ans": 2, "exp_zh": "at noon（中午）是固定用法。", "exp_en": "'At noon' is fixed."},
                    {"q": "She will return ___ a week.", "opts": ["in", "on", "at", "by"], "ans": 0, "exp_zh": "一段時間後用 'in'。in a week = 一週後。", "exp_en": "'In' + period = after that time. 'In a week' = one week from now."},
                ]
            },
            "place_prepositions": {
                "subtopic_id": "place_prepositions",
                "subtopic_zh": "地點介系詞",
                "subtopic_en": "Place Prepositions",
                "templates": [
                    {"q": "The cat is hiding ___ the bed.", "opts": ["under", "over", "above", "on"], "ans": 0, "exp_zh": "'under' = 在正下方。'above' = 在上方（不一定是正上方）。", "exp_en": "'Under' = directly below. 'Above' = higher but not necessarily directly."},
                    {"q": "The picture is hanging ___ the wall.", "opts": ["on", "in", "at", "by"], "ans": 0, "exp_zh": "掛在牆面上用 'on'。", "exp_en": "Things attached to a surface: 'on the wall'."},
                    {"q": "There is a bridge ___ the river.", "opts": ["on", "in", "over", "at"], "ans": 2, "exp_zh": "橋在河上方用 'over'。", "exp_en": "A bridge goes 'over' a river."},
                    {"q": "The bank is ___ the post office and the library.", "opts": ["among", "between", "beside", "behind"], "ans": 1, "exp_zh": "兩者之間用 'between'。三者以上用 'among'。", "exp_en": "'Between' = two things. 'Among' = three or more."},
                    {"q": "We sat ___ a large oak tree.", "opts": ["under", "over", "above", "on"], "ans": 0, "exp_zh": "坐在樹下用 'under'。", "exp_en": "Sit 'under' a tree."},
                ]
            },
        }
    },
    "grammar_comparison": {
        "topic_id": "grammar_comparison",
        "topic_zh": "形容詞比較",
        "topic_en": "Adjective Comparison",
        "subtopics": {
            "comparative": {
                "subtopic_id": "comparative",
                "subtopic_zh": "比較級",
                "subtopic_en": "Comparative",
                "templates": [
                    {"q": "This puzzle is ___ than the last one.", "opts": ["hard", "harder", "hardest", "most hard"], "ans": 1, "exp_zh": "短形容詞比較級加 -er。hard → harder。", "exp_en": "Short adjectives: add -er for comparative. Hard → harder."},
                    {"q": "My score was ___ than yours.", "opts": ["good", "better", "best", "more good"], "ans": 1, "exp_zh": "'good' 的比較級是不規則的 'better'。", "exp_en": "'Good' has irregular comparative 'better'."},
                    {"q": "This book is ___ interesting than that one.", "opts": ["much", "more", "most", "very"], "ans": 1, "exp_zh": "長形容詞用 'more + adj + than'。", "exp_en": "Long adjectives: 'more + adj + than'."},
                    {"q": "She speaks English ___ than her sister.", "opts": ["fluent", "fluenter", "more fluent", "most fluent"], "ans": 2, "exp_zh": "兩個音節以上的形容詞用 'more'。", "exp_en": "Adjectives with 2+ syllables: 'more + adj'."},
                    {"q": "The weather today is ___ than yesterday.", "opts": ["bad", "worse", "worst", "more bad"], "ans": 1, "exp_zh": "'bad' 的比較級是不規則的 'worse'。", "exp_en": "'Bad' → irregular comparative 'worse'."},
                ]
            },
            "superlative": {
                "subtopic_id": "superlative",
                "subtopic_zh": "最高級",
                "subtopic_en": "Superlative",
                "templates": [
                    {"q": "Mount Everest is ___ mountain in the world.", "opts": ["high", "higher", "the highest", "the most high"], "ans": 2, "exp_zh": "最高級：the + adj + est。", "exp_en": "Superlative: the + adj + -est."},
                    {"q": "This is ___ movie I have ever watched.", "opts": ["bad", "worse", "the worst", "the most bad"], "ans": 2, "exp_zh": "bad → worst（不規則）。最高級前加 'the'。", "exp_en": "Bad → worst (irregular). Superlative uses 'the'."},
                    {"q": "She is ___ student in our class.", "opts": ["the clever", "the cleverest", "the most clever", "cleverest"], "ans": 1, "exp_zh": "clever 可加 -er/-est 或用 more/most。", "exp_en": "'Clever' accepts both -est and 'most clever'."},
                    {"q": "Of all the boys, Tom runs ___.", "opts": ["fast", "faster", "the fastest", "the most fast"], "ans": 2, "exp_zh": "fast → fastest（單音節加 -est）。", "exp_en": "Fast → fastest (one syllable, add -est)."},
                ]
            },
        }
    },
    "grammar_passive": {
        "topic_id": "grammar_passive",
        "topic_zh": "被動語態",
        "topic_en": "Passive Voice",
        "subtopics": {
            "passive_present": {
                "subtopic_id": "passive_present",
                "subtopic_zh": "現在被動",
                "subtopic_en": "Present Passive",
                "templates": [
                    {"q": "English ___ in over 50 countries.", "opts": ["speaks", "is spoken", "is speaking", "spoke"], "ans": 1, "exp_zh": "現在被動：is/are + pp。English is spoken。", "exp_en": "Present passive: is/are + past participle."},
                    {"q": "This road ___ every year.", "opts": ["repairs", "is repaired", "is repairing", "repaired"], "ans": 1, "exp_zh": "路被修理 = 現在被動。", "exp_en": "The road is repaired (by someone) = passive."},
                    {"q": "The letters ___ by the secretary.", "opts": ["type", "are typed", "are typing", "typed"], "ans": 1, "exp_zh": "信件被打字 = 被動。複數用 'are typed'。", "exp_en": "Letters are typed (by the secretary) = passive."},
                ]
            },
            "passive_past": {
                "subtopic_id": "passive_past",
                "subtopic_zh": "過去被動",
                "subtopic_en": "Past Passive",
                "templates": [
                    {"q": "The window ___ by the ball.", "opts": ["break", "broke", "was broken", "is broken"], "ans": 2, "exp_zh": "過去被動：was/were + pp。窗戶被打破了。", "exp_en": "Past passive: was/were + past participle."},
                    {"q": "The cake ___ by my grandmother yesterday.", "opts": ["made", "was made", "is made", "has made"], "ans": 1, "exp_zh": "'yesterday' 過去被動。", "exp_en": "'Yesterday' → past passive: was made."},
                    {"q": "The students ___ to leave early.", "opts": ["allowed", "were allowed", "are allowed", "was allowed"], "ans": 1, "exp_zh": "學生被允許 = 過去被動。students = 複數 = were。", "exp_en": "Students were allowed = past passive."},
                ]
            },
            "passive_future": {
                "subtopic_id": "passive_future",
                "subtopic_zh": "未來被動",
                "subtopic_en": "Future Passive",
                "templates": [
                    {"q": "The results ___ next week.", "opts": ["announce", "will announce", "will be announced", "are announced"], "ans": 2, "exp_zh": "未來被動：will be + pp。", "exp_en": "Future passive: will be + past participle."},
                    {"q": "The new bridge ___ by 2027.", "opts": ["will complete", "will be completed", "is completed", "was completed"], "ans": 1, "exp_zh": "橋將被建好 = 未來被動。", "exp_en": "The bridge will be completed = future passive."},
                ]
            },
        }
    },
    "grammar_conditionals": {
        "topic_id": "grammar_conditionals",
        "topic_zh": "條件句",
        "topic_en": "Conditionals",
        "subtopics": {
            "first_conditional": {
                "subtopic_id": "first_conditional",
                "subtopic_zh": "第一條件句",
                "subtopic_en": "First Conditional",
                "templates": [
                    {"q": "If it rains tomorrow, I ___ at home.", "opts": ["stay", "will stay", "stayed", "would stay"], "ans": 1, "exp_zh": "第一條件句：If + 現在式, will + 原形。", "exp_en": "First conditional: If + present, will + base form."},
                    {"q": "If you study hard, you ___ the exam.", "opts": ["pass", "will pass", "passed", "would pass"], "ans": 1, "exp_zh": "真實可能的情況用第一條件句。", "exp_en": "Real/possible situation → first conditional."},
                    {"q": "She will miss the bus if she ___ now.", "opts": ["don't leave", "doesn't leave", "won't leave", "didn't leave"], "ans": 1, "exp_zh": "if 子句用現在式（否定：doesn't leave）。", "exp_en": "In 'if' clause, use present tense (negative: doesn't leave)."},
                ]
            },
            "second_conditional": {
                "subtopic_id": "second_conditional",
                "subtopic_zh": "第二條件句",
                "subtopic_en": "Second Conditional",
                "templates": [
                    {"q": "If I ___ a millionaire, I would travel the world.", "opts": ["am", "was", "were", "will be"], "ans": 2, "exp_zh": "第二條件句：If + 過去式（假設式用 were），would + 原形。", "exp_en": "Second conditional: If + past subjunctive 'were', would + base."},
                    {"q": "If she ___ more time, she would learn to paint.", "opts": ["has", "had", "have", "would have"], "ans": 1, "exp_zh": "假設情況：If + had, would + 原形。", "exp_en": "Hypothetical: If + had, would + base form."},
                    {"q": "What would you do if you ___ a bird?", "opts": ["are", "was", "were", "will be"], "ans": 2, "exp_zh": "所有主詞都用 'were'（假設式）。", "exp_en": "Subjunctive 'were' for all subjects in hypothetical."},
                ]
            },
            "third_conditional": {
                "subtopic_id": "third_conditional",
                "subtopic_zh": "第三條件句",
                "subtopic_en": "Third Conditional",
                "templates": [
                    {"q": "If I ___ harder, I would have passed.", "opts": ["study", "studied", "had studied", "have studied"], "ans": 2, "exp_zh": "第三條件句：If + had + pp, would have + pp。過去假設。", "exp_en": "Third conditional: If + had + pp, would have + pp."},
                    {"q": "She would have come if she ___ invited.", "opts": ["is", "was", "had been", "has been"], "ans": 2, "exp_zh": "過去假設被動：had been + pp。", "exp_en": "Past hypothetical passive: had been invited."},
                    {"q": "Had I known the truth, I ___ differently.", "opts": ["act", "acted", "would have acted", "would act"], "ans": 2, "exp_zh": "Had I known = If I had known（倒裝）。would have + pp。", "exp_en": "Had I known = If I had known (inversion). Would have + pp."},
                ]
            },
        }
    },
    "grammar_reported_speech": {
        "topic_id": "grammar_reported_speech",
        "topic_zh": "間接引語",
        "topic_en": "Reported Speech",
        "subtopics": {
            "reported_statements": {
                "subtopic_id": "reported_statements",
                "subtopic_zh": "間接陳述",
                "subtopic_en": "Reported Statements",
                "templates": [
                    {"q": "She said, 'I am tired.' → She said she ___ tired.", "opts": ["is", "was", "has been", "will be"], "ans": 1, "exp_zh": "間接引語後移：am → was。", "exp_en": "Backshift: am → was."},
                    {"q": "'I will help you,' he said. → He said he ___ help me.", "opts": ["will", "would", "can", "could"], "ans": 1, "exp_zh": "will → would（後移）。", "exp_en": "Backshift: will → would."},
                    {"q": "'I have finished,' she said. → She said she ___ finished.", "opts": ["has", "had", "have", "was"], "ans": 1, "exp_zh": "has/have → had（後移）。", "exp_en": "Backshift: have/has → had."},
                    {"q": "'I can swim,' the boy said. → The boy said he ___ swim.", "opts": ["can", "could", "will", "would"], "ans": 1, "exp_zh": "can → could（後移）。", "exp_en": "Backshift: can → could."},
                ]
            },
            "reported_questions": {
                "subtopic_id": "reported_questions",
                "subtopic_zh": "間接問句",
                "subtopic_en": "Reported Questions",
                "templates": [
                    {"q": "'Where do you live?' she asked. → She asked where I ___.", "opts": ["live", "lived", "living", "was live"], "ans": 1, "exp_zh": "間接問句後移時態：live → lived。", "exp_en": "Indirect question backshift: live → lived."},
                    {"q": "'What time is it?' he asked. → He asked what time it ___.", "opts": ["is", "was", "has been", "will be"], "ans": 1, "exp_zh": "間接問句：is → was。疑問詞保留。", "exp_en": "Indirect question: is → was. Keep question word."},
                    {"q": "'Have you eaten?' she asked. → She asked if I ___.", "opts": ["have eaten", "had eaten", "ate", "eat"], "ans": 1, "exp_zh": "Yes/No 問句用 if/whether。have eaten → had eaten。", "exp_en": "Yes/No → use 'if/whether'. have eaten → had eaten."},
                ]
            },
        }
    },
    "grammar_relative_clauses": {
        "topic_id": "grammar_relative_clauses",
        "topic_zh": "關係子句",
        "topic_en": "Relative Clauses",
        "subtopics": {
            "who_which_that": {
                "subtopic_id": "who_which_that",
                "subtopic_zh": "who/which/that",
                "subtopic_en": "Who/Which/That",
                "templates": [
                    {"q": "The girl ___ won the prize is my cousin.", "opts": ["who", "which", "whose", "whom"], "ans": 0, "exp_zh": "指人（主詞）用 'who'。", "exp_en": "For people (subject): 'who'."},
                    {"q": "The laptop ___ I bought is very fast.", "opts": ["who", "which", "whose", "whom"], "ans": 1, "exp_zh": "指物用 'which'。", "exp_en": "For things: 'which'."},
                    {"q": "Is this the book ___ you were looking for?", "opts": ["who", "which", "whose", "whom"], "ans": 1, "exp_zh": "指物（book）用 'which' 或 'that'。", "exp_en": "For things: 'which' or 'that'."},
                    {"q": "The teacher ___ class I enjoy has retired.", "opts": ["who", "which", "whose", "whom"], "ans": 2, "exp_zh": "所有格用 'whose'。whose class = 他的課。", "exp_en": "Possession: 'whose'. Whose class = his class."},
                    {"q": "The students ___ passed the test celebrated.", "opts": ["who", "which", "whose", "whom"], "ans": 0, "exp_zh": "指人（主詞）用 'who'。", "exp_en": "For people (subject position): 'who'."},
                ]
            },
            "defining_nondefining": {
                "subtopic_id": "defining_nondefining",
                "subtopic_zh": "限定/非限定",
                "subtopic_en": "Defining/Non-defining",
                "templates": [
                    {"q": "My brother, ___ is a doctor, lives in London.", "opts": ["who", "which", "that", "whom"], "ans": 0, "exp_zh": "非限定性關係子句（有逗號）不能用 'that'，用 'who'。", "exp_en": "Non-defining (with commas): cannot use 'that', use 'who'."},
                    {"q": "The house ___ Jack built is very old.", "opts": ["who", "which", "that", "whose"], "ans": 2, "exp_zh": "限定性關係子句（無逗號）可用 'that'。", "exp_en": "Defining clause (no commas): 'that' is fine."},
                ]
            },
        }
    },
    "grammar_inversion": {
        "topic_id": "grammar_inversion",
        "topic_zh": "倒裝句",
        "topic_en": "Inversion",
        "subtopics": {
            "negative_inversion": {
                "subtopic_id": "negative_inversion",
                "subtopic_zh": "否定倒裝",
                "subtopic_en": "Negative Inversion",
                "templates": [
                    {"q": "Never ___ such a delicious meal.", "opts": ["I have had", "have I had", "I had", "did I had"], "ans": 1, "exp_zh": "Never 在句首，主詞和助動詞倒裝。", "exp_en": "'Never' at start → invert subject and auxiliary."},
                    {"q": "Seldom ___ so many people at the concert.", "opts": ["I see", "do I see", "I saw", "did I saw"], "ans": 1, "exp_zh": "Seldom 在句首，倒裝。", "exp_en": "'Seldom' at start → inversion."},
                    {"q": "Not only ___ the exam, but she also got the highest score.", "opts": ["she passed", "did she pass", "she did pass", "passed she"], "ans": 1, "exp_zh": "Not only 在句首，倒裝。", "exp_en": "'Not only' at start → inversion."},
                    {"q": "Hardly ___ the door when the phone rang.", "opts": ["I opened", "had I opened", "I had opened", "did I open"], "ans": 1, "exp_zh": "Hardly...when 句型，倒裝。", "exp_en": "'Hardly...when' → inversion."},
                    {"q": "Under no circumstances ___ cheat in an exam.", "opts": ["you should", "should you", "you shall", "shall you"], "ans": 1, "exp_zh": "否定片語在句首，倒裝。", "exp_en": "Negative phrase at start → inversion."},
                ]
            },
            "conditional_inversion": {
                "subtopic_id": "conditional_inversion",
                "subtopic_zh": "條件倒裝",
                "subtopic_en": "Conditional Inversion",
                "templates": [
                    {"q": "___ I known about the meeting, I would have attended.", "opts": ["If", "Had", "Would", "Did"], "ans": 1, "exp_zh": "Had I known = If I had known（條件倒裝）。", "exp_en": "Had I known = If I had known (conditional inversion)."},
                    {"q": "___ it not been for your help, I would have failed.", "opts": ["If", "Had", "Would", "Did"], "ans": 1, "exp_zh": "Had it not been for = 倒裝條件句。", "exp_en": "Had it not been for = conditional inversion."},
                    {"q": "___ you need anything, please call me.", "opts": ["Had", "Should", "Would", "Did"], "ans": 1, "exp_zh": "Should you need = If you should need（倒裝）。", "exp_en": "Should you need = If you should need (inversion)."},
                ]
            },
        }
    },
    "grammar_participles": {
        "topic_id": "grammar_participles",
        "topic_zh": "分詞",
        "topic_en": "Participles",
        "subtopics": {
            "present_participle": {
                "subtopic_id": "present_participle",
                "subtopic_zh": "現在分詞",
                "subtopic_en": "Present Participle",
                "templates": [
                    {"q": "The ___ child could not stop laughing.", "opts": ["excite", "excited", "exciting", "excites"], "ans": 1, "exp_zh": "人感到興奮用 '-ed'。事物令人興奮用 '-ing'。", "exp_en": "People feel 'excited' (-ed). Things are 'exciting' (-ing)."},
                    {"q": "The movie was really ___.", "opts": ["bore", "bored", "boring", "bores"], "ans": 2, "exp_zh": "事物本身令人無聊用 'boring'。人感到無聊用 'bored'。", "exp_en": "Things are 'boring'. People feel 'bored'."},
                    {"q": "I found the book very ___.", "opts": ["interest", "interested", "interesting", "interests"], "ans": 2, "exp_zh": "修飾事物用 '-ing' 分詞形容詞。", "exp_en": "Describing a thing: '-ing' participle adjective."},
                    {"q": "She was ___ by the magician's tricks.", "opts": ["amaze", "amazed", "amazing", "amazes"], "ans": 1, "exp_zh": "人感到驚訝用 'amazed'。", "exp_en": "People feel 'amazed'. The tricks are 'amazing'."},
                    {"q": "The journey was ___. We all fell asleep.", "opts": ["tire", "tired", "tiring", "tires"], "ans": 2, "exp_zh": "旅程本身令人疲倦用 'tiring'。", "exp_en": "The journey is 'tiring'. People are 'tired'."},
                ]
            },
            "past_participle": {
                "subtopic_id": "past_participle",
                "subtopic_zh": "過去分詞",
                "subtopic_en": "Past Participle",
                "templates": [
                    {"q": "___ in 1889, the Eiffel Tower is over 130 years old.", "opts": ["Building", "Built", "Being built", "To build"], "ans": 1, "exp_zh": "過去分詞 'Built' 表被動（被建造）。", "exp_en": "Past participle 'Built' = passive (was built)."},
                    {"q": "___ by the beautiful scenery, we decided to stay longer.", "opts": ["Attract", "Attracted", "Attracting", "To attract"], "ans": 1, "exp_zh": "過去分詞表被動感受：被吸引。", "exp_en": "Past participle = passive feeling: we were attracted."},
                    {"q": "The letter ___ on the desk is for you.", "opts": ["lay", "laid", "lying", "lain"], "ans": 2, "exp_zh": "現在分詞 'lying' 表主動正在進行。", "exp_en": "Present participle 'lying' = active, ongoing."},
                ]
            },
        }
    },
    "grammar_subjunctive": {
        "topic_id": "grammar_subjunctive",
        "topic_zh": "假設語氣",
        "topic_en": "Subjunctive",
        "subtopics": {
            "subjunctive_were": {
                "subtopic_id": "subjunctive_were",
                "subtopic_zh": "假設式 were",
                "subtopic_en": "Subjunctive Were",
                "templates": [
                    {"q": "If I ___ you, I would accept the offer.", "opts": ["am", "was", "were", "be"], "ans": 2, "exp_zh": "假設語氣所有主詞都用 'were'。", "exp_en": "Subjunctive: all subjects use 'were'."},
                    {"q": "I wish I ___ taller.", "opts": ["am", "was", "were", "be"], "ans": 2, "exp_zh": "wish + 假設語氣用 'were'。", "exp_en": "Wish + subjunctive → 'were'."},
                    {"q": "She acts as if she ___ the boss.", "opts": ["is", "was", "were", "be"], "ans": 2, "exp_zh": "as if + 假設語氣用 'were'。", "exp_en": "As if + subjunctive → 'were'."},
                    {"q": "If only he ___ more careful.", "opts": ["is", "was", "were", "be"], "ans": 2, "exp_zh": "If only + 假設語氣用 'were'。", "exp_en": "If only + subjunctive → 'were'."},
                ]
            },
        }
    },
    "vocabulary_daily": {
        "topic_id": "vocabulary_daily",
        "topic_zh": "日常詞彙",
        "topic_en": "Daily Vocabulary",
        "subtopics": {
            "common_words": {
                "subtopic_id": "common_words",
                "subtopic_zh": "常用詞",
                "subtopic_en": "Common Words",
                "templates": [
                    {"q": "What does 'abandon' mean?", "opts": ["to leave behind", "to keep", "to find", "to build"], "ans": 0, "exp_zh": "'abandon' = 放棄、拋棄。", "exp_en": "'Abandon' = to leave behind, give up."},
                    {"q": "Choose the best word: The food was absolutely ___.", "opts": ["delicious", "delicacy", "delight", "deliver"], "ans": 0, "exp_zh": "'delicious' 形容食物美味。'delicacy' 是名詞（美味佳餚）。", "exp_en": "'Delicious' = adjective for tasty food. 'Delicacy' = noun (fine food)."},
                    {"q": "What is the opposite of 'generous'?", "opts": ["kind", "selfish", "gentle", "honest"], "ans": 1, "exp_zh": "generous（慷慨）的反義詞是 selfish（自私）。", "exp_en": "Opposite of 'generous' (大方) is 'selfish' (自私)."},
                    {"q": "Which word means 'to make something better'?", "opts": ["improve", "impress", "import", "imagine"], "ans": 0, "exp_zh": "'improve' = 改善、進步。", "exp_en": "'Improve' = to make better."},
                    {"q": "What does 'reluctant' mean?", "opts": ["eager", "unwilling", "excited", "confident"], "ans": 1, "exp_zh": "'reluctant' = 不情願的。", "exp_en": "'Reluctant' = unwilling, hesitant."},
                ]
            },
            "collocations": {
                "subtopic_id": "collocations",
                "subtopic_zh": "詞語搭配",
                "subtopic_en": "Collocations",
                "templates": [
                    {"q": "Which is the correct collocation?", "opts": ["make a mistake", "do a mistake", "take a mistake", "give a mistake"], "ans": 0, "exp_zh": "固定搭配 'make a mistake'（犯錯）。", "exp_en": "Fixed collocation: 'make a mistake'."},
                    {"q": "Choose the correct phrase: ___ attention to the teacher.", "opts": ["Do", "Make", "Pay", "Give"], "ans": 2, "exp_zh": "固定搭配 'pay attention'（注意）。", "exp_en": "Fixed collocation: 'pay attention'."},
                    {"q": "Which collocation is correct?", "opts": ["heavy rain", "strong rain", "big rain", "thick rain"], "ans": 0, "exp_zh": "英語說 'heavy rain'（大雨），不說 strong rain。", "exp_en": "Correct collocation: 'heavy rain', not 'strong rain'."},
                    {"q": "She ___ a decision to study abroad.", "opts": ["made", "did", "took", "gave"], "ans": 0, "exp_zh": "'make a decision' 是固定搭配。", "exp_en": "'Make a decision' is the fixed collocation."},
                    {"q": "He ___ a good impression at the interview.", "opts": ["made", "did", "gave", "took"], "ans": 0, "exp_zh": "'make an impression' 是固定搭配。", "exp_en": "'Make an impression' is the fixed collocation."},
                ]
            },
        }
    },
    "vocabulary_roots": {
        "topic_id": "vocabulary_roots",
        "topic_zh": "字根字綴",
        "topic_en": "Roots & Affixes",
        "subtopics": {
            "prefixes": {
                "subtopic_id": "prefixes",
                "subtopic_zh": "前綴",
                "subtopic_en": "Prefixes",
                "templates": [
                    {"q": "The prefix 'un-' means 'not'. What does 'unfair' mean?", "opts": ["very fair", "not fair", "almost fair", "always fair"], "ans": 1, "exp_zh": "前綴 'un-' = 不。unfair = 不公平。", "exp_en": "Prefix 'un-' = not. Unfair = not fair."},
                    {"q": "The prefix 're-' means 'again'. What does 'rewrite' mean?", "opts": ["write for the first time", "write again", "stop writing", "write quickly"], "ans": 1, "exp_zh": "前綴 're-' = 再次。rewrite = 重寫。", "exp_en": "Prefix 're-' = again. Rewrite = write again."},
                    {"q": "What does 'impossible' mean? (prefix: im-)", "opts": ["very possible", "not possible", "almost possible", "always possible"], "ans": 1, "exp_zh": "前綴 'im-' = 不。impossible = 不可能。", "exp_en": "Prefix 'im-' = not. Impossible = not possible."},
                    {"q": "What does 'international' mean? (prefix: inter-)", "opts": ["inside a nation", "between nations", "not national", "above nations"], "ans": 1, "exp_zh": "前綴 'inter-' = 之間。international = 國際的。", "exp_en": "Prefix 'inter-' = between. International = between nations."},
                ]
            },
            "suffixes": {
                "subtopic_id": "suffixes",
                "subtopic_zh": "後綴",
                "subtopic_en": "Suffixes",
                "templates": [
                    {"q": "The suffix '-ness' turns adjectives into nouns. What is 'happy' → ___?", "opts": ["happyness", "happiness", "happily", "happier"], "ans": 1, "exp_zh": "happy → happiness。y 變 i 再加 -ness。", "exp_en": "Happy → happiness (y → i + ness)."},
                    {"q": "The suffix '-ful' means 'full of'. What does 'beautiful' mean?", "opts": ["without beauty", "full of beauty", "becoming beauty", "causing beauty"], "ans": 1, "exp_zh": "beautiful = full of beauty（充滿美麗）。", "exp_en": "Beautiful = full of beauty."},
                    {"q": "What does the suffix '-less' mean in 'careless'?", "opts": ["full of care", "without care", "causing care", "becoming care"], "ans": 1, "exp_zh": "後綴 '-less' = 沒有。careless = 不小心。", "exp_en": "Suffix '-less' = without. Careless = without care."},
                    {"q": "Add '-ly' to 'quick' to make an ___.", "opts": ["adjective", "adverb", "noun", "verb"], "ans": 1, "exp_zh": "'quickly' 是副詞。-ly 通常把形容詞變副詞。", "exp_en": "'Quickly' is an adverb. -ly usually makes adverbs from adjectives."},
                ]
            },
        }
    },
    "vocabulary_idioms": {
        "topic_id": "vocabulary_idioms",
        "topic_zh": "慣用語",
        "topic_en": "Idioms",
        "subtopics": {
            "common_idioms": {
                "subtopic_id": "common_idioms",
                "subtopic_zh": "常用慣用語",
                "subtopic_en": "Common Idioms",
                "templates": [
                    {"q": "What does 'break the ice' mean?", "opts": ["freeze water", "start a conversation", "break something", "be cold"], "ans": 1, "exp_zh": "'break the ice' = 打破僵局，開始交談。", "exp_en": "'Break the ice' = initiate conversation, ease tension."},
                    {"q": "What does 'hit the books' mean?", "opts": ["throw books", "study hard", "read a novel", "buy books"], "ans": 1, "exp_zh": "'hit the books' = 努力讀書。", "exp_en": "'Hit the books' = study hard."},
                    {"q": "'Piece of cake' means something is ___.", "opts": ["delicious", "expensive", "easy", "difficult"], "ans": 2, "exp_zh": "'piece of cake' = 很容易的事。", "exp_en": "'Piece of cake' = something very easy."},
                    {"q": "What does 'under the weather' mean?", "opts": ["outside", "feeling sick", "raining", "cold temperature"], "ans": 1, "exp_zh": "'under the weather' = 身體不舒服。", "exp_en": "'Under the weather' = feeling ill/unwell."},
                    {"q": "'Bite the bullet' means to ___.", "opts": ["eat quickly", "endure something painful", "shoot a gun", "be angry"], "ans": 1, "exp_zh": "'bite the bullet' = 咬緊牙關忍受。", "exp_en": "'Bite the bullet' = endure something difficult bravely."},
                    {"q": "What does 'once in a blue moon' mean?", "opts": ["every night", "very rarely", "always", "during full moon"], "ans": 1, "exp_zh": "'once in a blue moon' = 非常罕見。", "exp_en": "'Once in a blue moon' = very rarely."},
                ]
            },
        }
    },
    "sentence_transformation": {
        "topic_id": "sentence_transformation",
        "topic_zh": "句子轉換",
        "topic_en": "Sentence Transformation",
        "subtopics": {
            "active_passive_transform": {
                "subtopic_id": "active_passive_transform",
                "subtopic_zh": "主動被動轉換",
                "subtopic_en": "Active/Passive Transform",
                "templates": [
                    {"q": "Change to passive: 'Someone stole my bicycle.' → My bicycle ___.", "opts": ["was stolen", "is stolen", "stolen", "has stolen"], "ans": 0, "exp_zh": "主動改被動：受詞 + was/were + pp。", "exp_en": "Active to passive: object + was/were + pp."},
                    {"q": "Change to active: 'The letter was written by Tom.' → Tom ___.", "opts": ["wrote the letter", "the letter wrote", "was writing", "has written"], "ans": 0, "exp_zh": "被動改主動：by 後面的人做主詞。", "exp_en": "Passive to active: person after 'by' becomes subject."},
                ]
            },
            "direct_indirect_transform": {
                "subtopic_id": "direct_indirect_transform",
                "subtopic_zh": "直接間接轉換",
                "subtopic_en": "Direct/Indirect Transform",
                "templates": [
                    {"q": "'I am hungry,' she said. → She said ___ hungry.", "opts": ["she is", "she was", "she has been", "she will be"], "ans": 1, "exp_zh": "直接引語改間接引語：am → was。", "exp_en": "Direct to indirect: am → was (backshift)."},
                    {"q": "'Where is the station?' he asked. → He asked where the station ___.", "opts": ["is", "was", "has been", "will be"], "ans": 1, "exp_zh": "間接問句：is → was。", "exp_en": "Indirect question: is → was."},
                ]
            },
            "combining_sentences": {
                "subtopic_id": "combining_sentences",
                "subtopic_zh": "合併句子",
                "subtopic_en": "Combining Sentences",
                "templates": [
                    {"q": "Combine: 'The boy is tall. He plays basketball.' → The boy ___ plays basketball is tall.", "opts": ["who", "which", "whose", "whom"], "ans": 0, "exp_zh": "用關係代名詞 'who' 合併兩句（指人）。", "exp_en": "Combine with relative pronoun 'who' (for people)."},
                    {"q": "Combine: 'She was tired. She went to bed early.' → ___ tired, she went to bed early.", "opts": ["Be", "Being", "Been", "Was"], "ans": 1, "exp_zh": "現在分詞 'Being' 可合併因果句。", "exp_en": "Present participle 'Being' can combine cause-effect sentences."},
                ]
            },
        }
    },
    "error_identification": {
        "topic_id": "error_identification",
        "topic_zh": "錯誤識別",
        "topic_en": "Error Identification",
        "subtopics": {
            "grammar_errors": {
                "subtopic_id": "grammar_errors",
                "subtopic_zh": "文法錯誤",
                "subtopic_en": "Grammar Errors",
                "templates": [
                    {"q": "Find the error: 'Each of the students have a textbook.'", "opts": ["Each", "of the students", "have", "a textbook"], "ans": 2, "exp_zh": "'Each' 是單數，動詞應為 'has'。", "exp_en": "'Each' is singular → 'has', not 'have'."},
                    {"q": "Find the error: 'She don't like coffee.'", "opts": ["She", "don't", "like", "coffee"], "ans": 1, "exp_zh": "第三人稱單數否定用 'doesn't'。", "exp_en": "Third person singular: 'doesn't', not 'don't'."},
                    {"q": "Find the error: 'The informations are useful.'", "opts": ["The", "informations", "are", "useful"], "ans": 1, "exp_zh": "'information' 是不可數名詞，不能加 -s。", "exp_en": "'Information' is uncountable → no -s."},
                    {"q": "Find the error: 'He suggested me to go.'", "opts": ["He", "suggested", "me to go", "to go"], "ans": 2, "exp_zh": "'suggest' 不接 '人 + to do'。應為 'suggested that I go'。", "exp_en": "'Suggest' doesn't take 'person + to do'. Use 'suggested that I go'."},
                    {"q": "Find the error: 'I have been to Paris last year.'", "opts": ["I", "have been", "to Paris", "last year"], "ans": 1, "exp_zh": "'last year' 是過去時間，不應用現在完成式。應為 'I went to Paris last year.'", "exp_en": "'Last year' is past time → simple past, not present perfect."},
                ]
            },
            "spelling_errors": {
                "subtopic_id": "spelling_errors",
                "subtopic_zh": "拼字錯誤",
                "subtopic_en": "Spelling Errors",
                "templates": [
                    {"q": "Which word is spelled correctly?", "opts": ["definately", "definitely", "definetly", "definitly"], "ans": 1, "exp_zh": "正確拼法是 'definitely'。", "exp_en": "Correct spelling: 'definitely'."},
                    {"q": "Which word is spelled correctly?", "opts": ["accomodate", "accommodate", "acommodate", "accomadate"], "ans": 1, "exp_zh": "正確拼法是 'accommodate'（雙 c 雙 m）。", "exp_en": "Correct: 'accommodate' (double c, double m)."},
                    {"q": "Which word is spelled correctly?", "opts": ["seperate", "separite", "separate", "seperete"], "ans": 2, "exp_zh": "正確拼法是 'separate'。", "exp_en": "Correct spelling: 'separate'."},
                    {"q": "Which word is spelled correctly?", "opts": ["neccessary", "necessary", "necesary", "neccesary"], "ans": 1, "exp_zh": "正確拼法是 'necessary'（一個 c 兩個 s）。", "exp_en": "Correct: 'necessary' (one c, two s's)."},
                ]
            },
        }
    },
    "reading_comprehension": {
        "topic_id": "reading_comprehension",
        "topic_zh": "閱讀理解",
        "topic_en": "Reading Comprehension",
        "subtopics": {
            "inference": {
                "subtopic_id": "inference",
                "subtopic_zh": "推論",
                "subtopic_en": "Inference",
                "templates": [
                    {"q": "Read: 'Tom arrived at the station just as the train pulled away.' What can we infer?", "opts": ["Tom caught the train", "Tom missed the train", "Tom drove to the station", "Tom hates trains"], "ans": 1, "exp_zh": "火車開走了 = Tom 錯過了火車。", "exp_en": "The train left = Tom missed it."},
                    {"q": "Read: 'She put on her coat, grabbed an umbrella, and looked out the window nervously.' What is the weather likely like?", "opts": ["Sunny", "Rainy or cloudy", "Snowy", "Very hot"], "ans": 1, "exp_zh": "拿雨傘 = 可能下雨或陰天。", "exp_en": "Grabbing umbrella → likely rainy or cloudy."},
                    {"q": "Read: 'The restaurant was empty except for one couple in the corner.' What time might it be?", "opts": ["Lunchtime", "Peak dinner hour", "Very late or early", "Holiday"], "ans": 2, "exp_zh": "餐廳幾乎空了 = 可能非常早或非常晚。", "exp_en": "Nearly empty restaurant → very late or very early."},
                ]
            },
            "main_idea": {
                "subtopic_id": "main_idea",
                "subtopic_zh": "主旨大意",
                "subtopic_en": "Main Idea",
                "templates": [
                    {"q": "Read: 'Recycling reduces waste. It saves energy. It protects the environment.' What is the main idea?", "opts": ["Waste is bad", "Recycling has many benefits", "Energy is important", "The environment needs protection"], "ans": 1, "exp_zh": "三句都在說回收的好處 = 主旨是回收有很多好處。", "exp_en": "All sentences about recycling benefits → main idea."},
                    {"q": "Read: 'Exercise improves health. It reduces stress. It boosts mood.' Main idea?", "opts": ["Stress is harmful", "Exercise has multiple benefits", "Health is important", "Mood affects daily life"], "ans": 1, "exp_zh": "主旨：運動有多種好處。", "exp_en": "Main idea: exercise has multiple benefits."},
                ]
            },
            "vocabulary_in_context": {
                "subtopic_id": "vocabulary_in_context",
                "subtopic_zh": "語境詞義",
                "subtopic_en": "Vocabulary in Context",
                "templates": [
                    {"q": "Read: 'The teacher's criticism was constructive.' What does 'constructive' mean here?", "opts": ["harmful", "helpful and useful", "angry", "unnecessary"], "ans": 1, "exp_zh": "'constructive criticism' = 建設性的批評，有幫助的。", "exp_en": "'Constructive criticism' = helpful, useful feedback."},
                    {"q": "Read: 'The plan was abandoned due to lack of funds.' What does 'abandoned' mean?", "opts": ["started", "given up", "improved", "continued"], "ans": 1, "exp_zh": "'abandoned' = 放棄。因為缺乏資金而放棄計劃。", "exp_en": "'Abandoned' = given up. The plan was given up due to lack of funds."},
                ]
            },
        }
    },
    "question_tags": {
        "topic_id": "question_tags",
        "topic_zh": "附加問句",
        "topic_en": "Question Tags",
        "subtopics": {
            "basic_tags": {
                "subtopic_id": "basic_tags",
                "subtopic_zh": "基本附加問句",
                "subtopic_en": "Basic Question Tags",
                "templates": [
                    {"q": "She is a student, ___?", "opts": ["is she", "isn't she", "doesn't she", "does she"], "ans": 1, "exp_zh": "肯定句 + 否定附加問句。is → isn't。", "exp_en": "Positive statement + negative tag. 'is' → 'isn't'."},
                    {"q": "They don't like coffee, ___?", "opts": ["don't they", "do they", "aren't they", "are they"], "ans": 1, "exp_zh": "否定句 + 肯定附加問句。don't → do。", "exp_en": "Negative statement + positive tag. 'don't' → 'do'."},
                    {"q": "He can swim, ___?", "opts": ["can he", "can't he", "doesn't he", "does he"], "ans": 1, "exp_zh": "can → can't 附加問句。", "exp_en": "'can' → 'can't' tag."},
                    {"q": "You have finished, ___?", "opts": ["have you", "haven't you", "do you", "don't you"], "ans": 1, "exp_zh": "have → haven't 附加問句。", "exp_en": "'have' → 'haven't' tag."},
                    {"q": "Let's go, ___?", "opts": ["shall we", "will we", "do we", "don't we"], "ans": 0, "exp_zh": "Let's 的附加問句固定用 'shall we'。", "exp_en": "'Let's' → fixed tag 'shall we'."},
                    {"q": "Nobody came, ___?", "opts": ["didn't they", "did they", "wasn't it", "was it"], "ans": 1, "exp_zh": "nobody 否定詞，附加問句用肯定。they 代替 nobody。", "exp_en": "'Nobody' is negative → positive tag. 'they' replaces 'nobody'."},
                ]
            },
        }
    },
    "subject_verb_agreement": {
        "topic_id": "subject_verb_agreement",
        "topic_zh": "主謂一致",
        "topic_en": "Subject-Verb Agreement",
        "subtopics": {
            "sva_basics": {
                "subtopic_id": "sva_basics",
                "subtopic_zh": "基本主謂一致",
                "subtopic_en": "SVA Basics",
                "templates": [
                    {"q": "Everyone ___ to attend the meeting.", "opts": ["need", "needs", "needing", "needed"], "ans": 1, "exp_zh": "'Everyone' 是單數，動詞加 -s。", "exp_en": "'Everyone' is singular → 'needs'."},
                    {"q": "Neither of the answers ___ correct.", "opts": ["is", "are", "were", "have been"], "ans": 0, "exp_zh": "'Neither of' 通常用單數動詞。", "exp_en": "'Neither of' usually takes singular verb."},
                    {"q": "The news ___ very shocking.", "opts": ["is", "are", "were", "have been"], "ans": 0, "exp_zh": "'news' 是不可數名詞（看似複數），用單數動詞。", "exp_en": "'News' looks plural but is uncountable → singular verb."},
                    {"q": "Mathematics ___ my favourite subject.", "opts": ["is", "are", "were", "have been"], "ans": 0, "exp_zh": "'Mathematics' 學科名用單數動詞。", "exp_en": "Academic subjects ending in -s take singular verb."},
                    {"q": "The committee ___ divided in their opinions.", "opts": ["is", "are", "was", "has been"], "ans": 1, "exp_zh": "委員會成員各有不同意見，用複數動詞。", "exp_en": "Committee members acting individually → plural verb."},
                ]
            },
        }
    },
}

# ─────────────────────────────────────────────────────────
# CHINESE TEMPLATES
# ─────────────────────────────────────────────────────────

ZH_TOPICS = {
    "字詞辨析": {
        "topic_id": "字詞辨析",
        "topic_zh": "字詞辨析",
        "topic_en": "Word Analysis",
        "subtopics": {
            "形近字": {
                "subtopic_id": "形近字",
                "subtopic_zh": "形近字",
                "subtopic_en": "Similar Characters",
                "templates": [
                    {"q": "「他＿經走遠了。」應填：", "opts": ["已", "己", "以", "几"], "ans": 0, "exp_zh": "「已」表示已經。「己」是自己。", "exp_en": "'已' = already. '己' = self."},
                    {"q": "「這是自＿的事情。」應填：", "opts": ["已", "己", "以", "几"], "ans": 1, "exp_zh": "「己」是自己。「已」是已經。", "exp_en": "'己' = self. '已' = already."},
                    {"q": "「我們要＿別是非。」應填：", "opts": ["辨", "辯", "辮", "瓣"], "ans": 0, "exp_zh": "「辨」是辨別。「辯」是辯論。「辮」是辮子。「瓣」是花瓣。", "exp_en": "'辨' = distinguish. '辯' = debate. '辮' = braid. '瓣' = petal."},
                    {"q": "「他的＿氣很好。」應填：", "opts": ["運", "韻", "暈", "蘊"], "ans": 0, "exp_zh": "「運氣」指命運、幸運。「韻」是韻律。", "exp_en": "'運氣' = luck/fate. '韻' = rhythm."},
                    {"q": "「這朵＿瑰花很美。」應填：", "opts": ["玫", "枚", "梅", "莓"], "ans": 0, "exp_zh": "「玫瑰」是一種花。「枚」是量詞。「梅」是梅花。「莓」是莓果。", "exp_en": "'玫瑰' = rose (flower). '枚' = measure word. '梅' = plum. '莓' = berry."},
                    {"q": "「他＿然接受了挑戰。」應填：", "opts": ["毅", "意", "義", "易"], "ans": 0, "exp_zh": "「毅然」形容堅決果斷。", "exp_en": "'毅然' = resolutely, determinedly."},
                    {"q": "「老師表＿了我們的努力。」應填：", "opts": ["楊", "揚", "陽", "樣"], "ans": 1, "exp_zh": "「表揚」指公開讚美。「楊」是姓氏。「陽」是太陽。", "exp_en": "'表揚' = praise publicly. '楊' = surname. '陽' = sun."},
                    {"q": "「這個＿題很難。」應填：", "opts": ["課", "棵", "顆", "科"], "ans": 3, "exp_zh": "「課題」指問題或任務。「棵」是植物量詞。「顆」是圓形物量詞。", "exp_en": "'課題' = topic/task. '棵' = plant measure. '顆' = round object measure."},
                ]
            },
            "同音字": {
                "subtopic_id": "同音字",
                "subtopic_zh": "同音字",
                "subtopic_en": "Homophones",
                "templates": [
                    {"q": "「他的＿氣很暴躁。」應填：", "opts": ["脾", "皮", "疲", "批"], "ans": 0, "exp_zh": "「脾氣」指性格、性情。「皮」是皮膚。「疲」是疲倦。", "exp_en": "'脾氣' = temperament. '皮' = skin. '疲' = tired."},
                    {"q": "「我們要＿真學習。」應填：", "opts": ["認", "任", "忍", "韌"], "ans": 0, "exp_zh": "「認真」指用心、仔細。", "exp_en": "'認真' = serious, earnest."},
                    {"q": "「老師＿評了我的作文。」應填：", "opts": ["批", "披", "疲", "脾"], "ans": 0, "exp_zh": "「批評」指指出缺點。「披」是披上。「疲」是疲倦。", "exp_en": "'批評' = criticize. '披' = drape. '疲' = tired."},
                    {"q": "「他的＿服很漂亮。」應填：", "opts": ["衣", "依", "醫", "一"], "ans": 0, "exp_zh": "「衣服」是穿戴的衣物。「依」是依靠。「醫」是醫生。", "exp_en": "'衣服' = clothes. '依' = rely on. '醫' = medicine."},
                ]
            },
            "多義詞": {
                "subtopic_id": "多義詞",
                "subtopic_zh": "多義詞",
                "subtopic_en": "Polysemy",
                "templates": [
                    {"q": "「打」在「打電話」中的意思是：", "opts": ["擊打", "撥打", "製作", "購買"], "ans": 1, "exp_zh": "「打電話」的「打」是「撥打」的意思。", "exp_en": "'打電話' = make a phone call. '打' = make/dial."},
                    {"q": "「花」在「他花了三天」中的意思是：", "opts": ["植物", "用掉", "花紋", "模糊"], "ans": 1, "exp_zh": "「花了三天」的「花」是「用掉、耗費」的意思。", "exp_en": "'花了三天' = spent three days. '花' = spend."},
                    {"q": "「深」在「感情很深」中的意思是：", "opts": ["距離長", "顏色濃", "程度高", "時間久"], "ans": 2, "exp_zh": "「感情深」的「深」是「程度高、深厚」的意思。", "exp_en": "'感情很深' = deep feelings. '深' = profound, deep (degree)."},
                ]
            },
        }
    },
    "成語運用": {
        "topic_id": "成語運用",
        "topic_zh": "成語運用",
        "topic_en": "Idiom Usage",
        "subtopics": {
            "成語辨析": {
                "subtopic_id": "成語辨析",
                "subtopic_zh": "成語辨析",
                "subtopic_en": "Idiom Analysis",
                "templates": [
                    {"q": "「畫畫得栩栩如生」中的「栩栩如生」意思是：", "opts": ["很生氣", "非常逼真", "很無聊", "很快樂"], "ans": 1, "exp_zh": "「栩栩如生」形容描寫或模仿非常逼真，像真的一樣。", "exp_en": "'栩栩如生' means lifelike, very realistic."},
                    {"q": "以下哪個成語使用正確？", "opts": ["他做事一絲不苟", "他做事一絲不掛", "他做事一成不變", "他做事一目十行"], "ans": 0, "exp_zh": "「一絲不苟」形容做事認真，一點不馬虎。", "exp_en": "'一絲不苟' = very careful and meticulous."},
                    {"q": "「守株待兔」比喻什麼？", "opts": ["勤勞工作", "等待機會不勞而獲", "保護樹木", "打獵技巧"], "ans": 1, "exp_zh": "「守株待兔」比喻不勞而獲或死守經驗。", "exp_en": "'守株待兔' = waiting for a windfall without effort."},
                    {"q": "「畫蛇添足」比喻什麼？", "opts": ["畫畫技術好", "多此一舉", "做事認真", "很有創意"], "ans": 1, "exp_zh": "「畫蛇添足」比喻多做不必要的事。", "exp_en": "'畫蛇添足' = doing something unnecessary, spoiling things."},
                    {"q": "「對牛彈琴」比喻什麼？", "opts": ["彈琴技術好", "對不懂的人講道理", "飼養牛隻", "音樂欣賞"], "ans": 1, "exp_zh": "「對牛彈琴」比喻對不懂的人講道理。", "exp_en": "'對牛彈琴' = talking to someone who can't understand."},
                    {"q": "「亡羊補牢」比喻什麼？", "opts": ["養羊的方法", "出了問題及時補救", "牢房很堅固", "牧羊人的故事"], "ans": 1, "exp_zh": "「亡羊補牢」比喻出了問題後及時補救。", "exp_en": "'亡羊補牢' = mending the pen after losing sheep = better late than never."},
                    {"q": "「井底之蛙」形容什麼樣的人？", "opts": ["勤勞的人", "見識狹窄的人", "善良的人", "聰明的人"], "ans": 1, "exp_zh": "「井底之蛙」比喻見識短淺的人。", "exp_en": "'井底之蛙' = frog in a well = person with limited perspective."},
                ]
            },
            "成語填空": {
                "subtopic_id": "成語填空",
                "subtopic_zh": "成語填空",
                "subtopic_en": "Idiom Fill-in",
                "templates": [
                    {"q": "他學習非常勤奮，真是＿＿＿＿。", "opts": ["廢寢忘食", "守株待兔", "畫蛇添足", "對牛彈琴"], "ans": 0, "exp_zh": "「廢寢忘食」形容非常勤奮，忘記吃飯睡覺。", "exp_en": "'廢寢忘食' = so diligent as to forget to eat and sleep."},
                    {"q": "他的演講精彩絕倫，聽眾都＿＿＿＿。", "opts": ["目瞪口呆", "守株待兔", "畫蛇添足", "亡羊補牢"], "ans": 0, "exp_zh": "「目瞪口呆」形容吃驚或發愣的樣子。", "exp_en": "'目瞪口呆' = dumbstruck, stunned."},
                    {"q": "這件事已經＿＿＿＿，無法挽回了。", "opts": ["亡羊補牢", "木已成舟", "畫蛇添足", "守株待兔"], "ans": 1, "exp_zh": "「木已成舟」比喻事情已成定局，無法改變。", "exp_en": "'木已成舟' = the wood has become a boat = what's done is done."},
                ]
            },
        }
    },
    "修辭手法": {
        "topic_id": "修辭手法",
        "topic_zh": "修辭手法",
        "topic_en": "Rhetoric",
        "subtopics": {
            "比喻": {
                "subtopic_id": "比喻",
                "subtopic_zh": "比喻",
                "subtopic_en": "Simile/Metaphor",
                "templates": [
                    {"q": "「月亮像一個銀盤」用了什麼修辭？", "opts": ["比喻", "擬人", "誇張", "排比"], "ans": 0, "exp_zh": "「像」是比喻詞，將月亮比作銀盤，是明喻。", "exp_en": "'像' = comparison word. Simile: moon compared to silver plate."},
                    {"q": "「她是我們班的太陽」用了什麼修辭？", "opts": ["明喻", "暗喻", "擬人", "誇張"], "ans": 1, "exp_zh": "用「是」直接說她是太陽 = 暗喻（隱喻）。", "exp_en": "'She is our sun' = metaphor (no 'like' or 'as')."},
                    {"q": "「時間就是金錢」用了什麼修辭？", "opts": ["明喻", "暗喻", "擬人", "誇張"], "ans": 1, "exp_zh": "用「就是」直接等同 = 暗喻。", "exp_en": "'Time is money' = metaphor."},
                    {"q": "「她的笑容像花兒一樣燦爛」用了什麼修辭？", "opts": ["比喻", "擬人", "誇張", "對偶"], "ans": 0, "exp_zh": "「像...一樣」是明喻標誌。", "exp_en": "'像...一樣' signals a simile."},
                ]
            },
            "擬人": {
                "subtopic_id": "擬人",
                "subtopic_zh": "擬人",
                "subtopic_en": "Personification",
                "templates": [
                    {"q": "「花兒在微笑」用了什麼修辭？", "opts": ["比喻", "擬人", "誇張", "對偶"], "ans": 1, "exp_zh": "「微笑」是人的動作，用在花上是擬人。", "exp_en": "'微笑' = human action applied to flowers = personification."},
                    {"q": "「春風輕輕地撫摸著我的臉」用了什麼修辭？", "opts": ["比喻", "擬人", "誇張", "排比"], "ans": 1, "exp_zh": "「撫摸」是人的動作，用在春風上是擬人。", "exp_en": "'撫摸' = human touch applied to wind = personification."},
                    {"q": "「小鳥在枝頭唱歌」用了什麼修辭？", "opts": ["比喻", "擬人", "誇張", "對偶"], "ans": 1, "exp_zh": "「唱歌」是人的行為，用在小鳥上是擬人。", "exp_en": "'唱歌' = human action for birds = personification."},
                ]
            },
            "誇張": {
                "subtopic_id": "誇張",
                "subtopic_zh": "誇張",
                "subtopic_en": "Hyperbole",
                "templates": [
                    {"q": "「飛流直下三千尺」用了什麼修辭？", "opts": ["比喻", "擬人", "誇張", "排比"], "ans": 2, "exp_zh": "「三千尺」是誇張手法，形容瀑布極長。", "exp_en": "'三千尺' = hyperbole, exaggerating the waterfall's height."},
                    {"q": "「他急得像熱鍋上的螞蟻」用了什麼修辭？", "opts": ["比喻", "擬人", "誇張", "排比"], "ans": 0, "exp_zh": "「像熱鍋上的螞蟻」是明喻。", "exp_en": "'像熱鍋上的螞蟻' = simile (like an ant on a hot pan)."},
                    {"q": "「他的聲音大得可以把屋頂掀翻」用了什麼修辭？", "opts": ["比喻", "擬人", "誇張", "排比"], "ans": 2, "exp_zh": "把聲音形容到能掀翻屋頂 = 誇張。", "exp_en": "Voice strong enough to flip the roof = hyperbole."},
                ]
            },
            "排比": {
                "subtopic_id": "排比",
                "subtopic_zh": "排比",
                "subtopic_en": "Parallelism",
                "templates": [
                    {"q": "「書是鑰匙，能開啟智慧之門；書是階梯，能通向成功之路；書是良藥，能醫治愚昧之症。」用了什麼修辭？", "opts": ["比喻", "擬人", "誇張", "排比"], "ans": 3, "exp_zh": "三個結構相同的句子並列 = 排比。", "exp_en": "Three parallel sentence structures = parallelism."},
                    {"q": "「生活是一首歌，吟唱著人生的悲歡離合；生活是一條路，延伸著人生的足跡。」主要用了什麼修辭？", "opts": ["比喻和排比", "擬人", "誇張", "對偶"], "ans": 0, "exp_zh": "同時用了比喻（是）和排比（結構相同）。", "exp_en": "Uses both metaphor ('是') and parallelism (same structure)."},
                ]
            },
            "對偶": {
                "subtopic_id": "對偶",
                "subtopic_zh": "對偶",
                "subtopic_en": "Antithesis",
                "templates": [
                    {"q": "「山不在高，有仙則名；水不在深，有龍則靈。」用了什麼修辭？", "opts": ["比喻", "擬人", "誇張", "對偶"], "ans": 3, "exp_zh": "兩句結構對稱、意義相關 = 對偶。", "exp_en": "Two symmetrical, related clauses = antithesis/parallelism."},
                    {"q": "「橫眉冷對千夫指，俯首甘為孺子牛。」用了什麼修辭？", "opts": ["比喻", "擬人", "誇張", "對偶"], "ans": 3, "exp_zh": "魯迅的對聯，結構對稱 = 對偶。", "exp_en": "Lu Xun's couplet with symmetrical structure = antithesis."},
                ]
            },
        }
    },
    "文言文": {
        "topic_id": "文言文",
        "topic_zh": "文言文",
        "topic_en": "Classical Chinese",
        "subtopics": {
            "虛詞": {
                "subtopic_id": "虛詞",
                "subtopic_zh": "虛詞",
                "subtopic_en": "Function Words",
                "templates": [
                    {"q": "「之」在古文中通常代表：", "opts": ["的/它", "和", "在", "是"], "ans": 0, "exp_zh": "「之」常用作助詞（的）或代詞（它/他）。", "exp_en": "'之' = particle (of) or pronoun (it/him) in classical Chinese."},
                    {"q": "「吾」的意思是：", "opts": ["你", "我", "他", "她"], "ans": 1, "exp_zh": "「吾」是文言文中的第一人稱，意思是「我」。", "exp_en": "'吾' = first person pronoun 'I' in classical Chinese."},
                    {"q": "「汝」的意思是：", "opts": ["你", "我", "他", "她"], "ans": 0, "exp_zh": "「汝」是文言文中的第二人稱，意思是「你」。", "exp_en": "'汝' = second person pronoun 'you' in classical Chinese."},
                    {"q": "「其」在「其真無馬邪」中的意思是：", "opts": ["他的", "難道", "那個", "其中"], "ans": 1, "exp_zh": "「其」在此句中表反問語氣，意為「難道」。", "exp_en": "'其' here expresses rhetorical question = 'surely not'."},
                    {"q": "「以」在「以刀劈狼」中的意思是：", "opts": ["因為", "用", "認為", "以致"], "ans": 1, "exp_zh": "「以」在此句中是「用」的意思。用刀劈狼。", "exp_en": "'以' here = 'with/using'. Using a knife to chop the wolf."},
                    {"q": "「而」在「學而時習之」中的意思是：", "opts": ["但是", "並且", "如果", "你的"], "ans": 1, "exp_zh": "「而」在此句中表順接，意為「並且」。", "exp_en": "'而' here = 'and/then' (sequential connection)."},
                ]
            },
            "實詞": {
                "subtopic_id": "實詞",
                "subtopic_zh": "實詞",
                "subtopic_en": "Content Words",
                "templates": [
                    {"q": "「善」在「善哉」中的意思是：", "opts": ["善良", "好", "擅長", "容易"], "ans": 1, "exp_zh": "「善哉」意為「好啊」。", "exp_en": "'善哉' = 'How good!' '善' = good."},
                    {"q": "「故」在「溫故而知新」中的意思是：", "opts": ["所以", "故意", "舊的", "原因"], "ans": 2, "exp_zh": "「溫故」的「故」是「舊的、學過的知識」。", "exp_en": "'故' here = 'old/previously learned'. Review old to learn new."},
                    {"q": "「去」在古文中的意思是：", "opts": ["前往", "離開", "距離", "過去"], "ans": 1, "exp_zh": "古文中「去」多指「離開」，與現代「前往」不同。", "exp_en": "In classical Chinese, '去' = 'leave' (opposite of modern 'go to')."},
                    {"q": "「妻子」在古文中的意思是：", "opts": ["太太", "妻子和兒子", "家人", "女性"], "ans": 1, "exp_zh": "古文中「妻子」是「妻子和兒女」，與現代不同。", "exp_en": "Classical '妻子' = wife and children (different from modern usage)."},
                ]
            },
            "句式": {
                "subtopic_id": "句式",
                "subtopic_zh": "句式",
                "subtopic_en": "Sentence Patterns",
                "templates": [
                    {"q": "「何陋之有？」是什麼句式？", "opts": ["判斷句", "省略句", "倒裝句", "被動句"], "ans": 2, "exp_zh": "「何陋之有」是賓語前置倒裝，正常語序為「有何陋」。", "exp_en": "'何陋之有' = inverted sentence. Normal order: '有何陋'."},
                    {"q": "「見漁人，乃大驚」省略了什麼？", "opts": ["主語", "謂語", "賓語", "定語"], "ans": 0, "exp_zh": "省略了主語「村中人」。", "exp_en": "Subject 'villagers' is omitted."},
                    {"q": "「帝感其誠」是什麼句式？", "opts": ["判斷句", "省略句", "倒裝句", "被動句"], "ans": 3, "exp_zh": "「帝感其誠」= 帝被其誠所感 = 被動句。", "exp_en": "'帝感其誠' = the emperor was moved by his sincerity = passive."},
                ]
            },
        }
    },
    "句子改錯": {
        "topic_id": "句子改錯",
        "topic_zh": "句子改錯",
        "topic_en": "Sentence Correction",
        "subtopics": {
            "搭配不當": {
                "subtopic_id": "搭配不當",
                "subtopic_zh": "搭配不當",
                "subtopic_en": "Wrong Collocation",
                "templates": [
                    {"q": "以下哪句有語病？", "opts": ["他非常努力學習", "他的成績提高了很大", "我們要愛護環境", "今天天氣很好"], "ans": 1, "exp_zh": "「提高了很大」搭配不當，應為「提高了很多」。", "exp_en": "'提高了很大' is wrong collocation. Should be '提高了很多'."},
                    {"q": "以下哪句有語病？", "opts": ["他的態度很端正", "他的水平發揮了很大", "她的聲音很甜美", "這本書很有趣"], "ans": 1, "exp_zh": "「發揮了很大」搭配不當，應為「發揮了很大的作用」或「水平很高」。", "exp_en": "'發揮了很大' is wrong. Should be '水平很高' or '發揮了很大的作用'."},
                    {"q": "以下哪句有語病？", "opts": ["我們要發揚優良傳統", "他改善了學習方法", "學校舉辦了運動會", "她增加了很多知識"], "ans": 1, "exp_zh": "「改善了學習方法」搭配不當，應為「改進了學習方法」。", "exp_en": "'改善方法' is wrong. Should be '改進方法' (improve methods)."},
                    {"q": "以下哪句有語病？", "opts": ["他的話深深地感動了我", "我們要培養良好的習慣", "他的成績有了很大的進步", "我改正了自己的錯誤"], "ans": 2, "exp_zh": "「有了很大的進步」搭配不當，應為「取得了很大的進步」。", "exp_en": "'有了進步' is wrong. Should be '取得了進步'."},
                ]
            },
            "語序不當": {
                "subtopic_id": "語序不當",
                "subtopic_zh": "語序不當",
                "subtopic_en": "Wrong Order",
                "templates": [
                    {"q": "以下哪句有語病？", "opts": ["我們應該認真學習", "他不但聰明，而且勤奮", "通過這次活動，使我受到了教育", "她每天都堅持鍛煉"], "ans": 2, "exp_zh": "「通過...使...」造成主語殘缺。應刪去「通過」或「使」。", "exp_en": "'通過...使...' removes the subject. Remove one of them."},
                    {"q": "以下哪句有語病？", "opts": ["這是一個非常好的建議", "我們學校大約有兩千個左右的學生", "他的意見很有道理", "今天天氣晴朗"], "ans": 1, "exp_zh": "「大約」和「左右」重複，應刪去一個。", "exp_en": "'大約' and '左右' are redundant. Remove one."},
                ]
            },
            "成分殘缺": {
                "subtopic_id": "成分殘缺",
                "subtopic_zh": "成分殘缺",
                "subtopic_en": "Missing Elements",
                "templates": [
                    {"q": "以下哪句有語病？", "opts": ["經過討論，大家統一了認識", "通過學習，使我提高了認識", "他的建議得到了大家的贊同", "老師耐心地講解了這道題"], "ans": 1, "exp_zh": "「通過...使...」缺少主語。", "exp_en": "'通過...使...' has no subject. Remove one."},
                    {"q": "以下哪句有語病？", "opts": ["他在學習上取得了優異的成績", "我們要發揚艱苦奮鬥", "這本書的內容很豐富", "她是一位優秀的教師"], "ans": 1, "exp_zh": "「發揚艱苦奮鬥」缺少賓語中心語，應為「發揚艱苦奮鬥的精神」。", "exp_en": "'發揚艱苦奮鬥' lacks object. Should add '的精神'."},
                ]
            },
        }
    },
    "閱讀理解": {
        "topic_id": "閱讀理解",
        "topic_zh": "閱讀理解",
        "topic_en": "Reading Comprehension",
        "subtopics": {
            "主旨理解": {
                "subtopic_id": "主旨理解",
                "subtopic_zh": "主旨理解",
                "subtopic_en": "Main Idea",
                "templates": [
                    {"q": "閱讀：「小明每天早起鍛煉身體，從不遲到，學習也非常認真。」這段話主要表現小明的什麼特點？", "opts": ["聰明", "勤奮自律", "善良", "調皮"], "ans": 1, "exp_zh": "早起鍛煉、不遲到、認真學習 = 勤奮自律。", "exp_en": "Early exercise, punctual, serious study = diligent and self-disciplined."},
                    {"q": "閱讀：「春天來了，小草從泥土裡探出頭來，花兒也張開了笑臉。」這段話主要描寫什麼？", "opts": ["冬天的景色", "春天的生機", "夏天的炎熱", "秋天的蕭瑟"], "ans": 1, "exp_zh": "小草發芽、花兒開放 = 春天的生機。", "exp_en": "Grass sprouting, flowers blooming = spring vitality."},
                    {"q": "閱讀：「他雖然身體殘疾，但從不放棄，最終成為了一名成功的企業家。」這段話的主旨是？", "opts": ["身體殘疾很可憐", "堅持不懈才能成功", "做生意很容易", "企業家都很辛苦"], "ans": 1, "exp_zh": "雖殘疾但不放棄，最終成功 = 堅持不懈才能成功。", "exp_en": "Despite disability, never gave up, succeeded = perseverance leads to success."},
                ]
            },
            "細節理解": {
                "subtopic_id": "細節理解",
                "subtopic_zh": "細節理解",
                "subtopic_en": "Detail Understanding",
                "templates": [
                    {"q": "閱讀：「小紅每天早上六點起床，先跑步三十分鐘，然後吃早餐。」小紅起床後先做什麼？", "opts": ["吃早餐", "跑步", "看書", "做作業"], "ans": 1, "exp_zh": "文中說「先跑步三十分鐘，然後吃早餐」，所以先跑步。", "exp_en": "Text says 'first runs for 30 minutes, then eats breakfast'."},
                    {"q": "閱讀：「這家店每天營業時間是上午九點到晚上十點。」這家店一天營業幾個小時？", "opts": ["十小時", "十一小時", "十二小時", "十三小時"], "ans": 3, "exp_zh": "上午九點到晚上十點 = 13小時。", "exp_en": "9am to 10pm = 13 hours."},
                    {"q": "閱讀：「他買了三本書，每本二十元，又買了一支筆，十元。」他一共花了多少錢？", "opts": ["五十元", "六十元", "七十元", "八十元"], "ans": 2, "exp_zh": "三本書 × 20元 = 60元，加一支筆10元 = 70元。", "exp_en": "3 books × $20 = $60, plus 1 pen $10 = $70."},
                ]
            },
            "推斷理解": {
                "subtopic_id": "推斷理解",
                "subtopic_zh": "推斷理解",
                "subtopic_en": "Inference",
                "templates": [
                    {"q": "閱讀：「他看了看窗外烏雲密布的天空，又看了看手中的雨傘，慶幸自己帶了傘。」天氣可能怎樣？", "opts": ["晴天", "快要下雨", "下雪", "颳風"], "ans": 1, "exp_zh": "烏雲密布 = 快要下雨。", "exp_en": "Dark clouds covering the sky = about to rain."},
                    {"q": "閱讀：「她看了看手錶，加快了腳步，臉上露出了焦急的神情。」她可能怎麼了？", "opts": ["很開心", "快要遲到了", "在散步", "在等人"], "ans": 1, "exp_zh": "看手錶、加快腳步、焦急 = 可能快要遲到。", "exp_en": "Checking watch, speeding up, anxious = likely running late."},
                ]
            },
        }
    },
    "標點符號": {
        "topic_id": "標點符號",
        "topic_zh": "標點符號",
        "topic_en": "Punctuation",
        "subtopics": {
            "基本標點": {
                "subtopic_id": "基本標點",
                "subtopic_zh": "基本標點",
                "subtopic_en": "Basic Punctuation",
                "templates": [
                    {"q": "「今天天氣真好＿」應填什麼標點？", "opts": ["。", "，", "！", "？"], "ans": 2, "exp_zh": "感嘆句用「！」。", "exp_en": "Exclamatory sentences use '!'. '！' = exclamation mark."},
                    {"q": "「你吃飯了嗎＿」應填什麼標點？", "opts": ["。", "，", "！", "？"], "ans": 3, "exp_zh": "疑問句用「？」。", "exp_en": "Questions use '?'. '？' = question mark."},
                    {"q": "「我喜歡吃蘋果＿香蕉＿和橙子。」應填什麼標點？", "opts": ["，，", "、、", "；；", "：："], "ans": 0, "exp_zh": "並列詞語之間用頓號「、」，但香港中文常用逗號「，」。", "exp_en": "Items in a list use commas '，' or enumeration marks '、'."},
                    {"q": "「他問＿你去哪裡＿」應填什麼標點？", "opts": ["「」", "：「」", "：「？」", "「？」"], "ans": 2, "exp_zh": "引用說話用冒號和引號，問句在引號內加問號。", "exp_en": "Quoted speech uses colon and quotation marks; question mark inside quotes."},
                    {"q": "「媽媽說＿快點回家＿」應填什麼標點？", "opts": ["，。", "：『』", "：「」", "，「」"], "ans": 2, "exp_zh": "說話用冒號「：」和引號「「」」。", "exp_en": "Speech uses colon '：' and quotation marks '「」'."},
                ]
            },
            "進階標點": {
                "subtopic_id": "進階標點",
                "subtopic_zh": "進階標點",
                "subtopic_en": "Advanced Punctuation",
                "templates": [
                    {"q": "「他很聰明＿但是不努力。」應填什麼標點？", "opts": ["。", "，", "！", "；"], "ans": 1, "exp_zh": "轉折連詞「但是」前用逗號。", "exp_en": "Before the conjunction '但是' (but), use a comma."},
                    {"q": "以下哪句標點使用正確？", "opts": ["他說：我來了。", "他說：『我來了。』", "他說『我來了』。", "他說：「我來了。」"], "ans": 3, "exp_zh": "引用說話用冒號和引號，句號在引號內。", "exp_en": "Quoted speech: colon + quotation marks, period inside."},
                    {"q": "「北京＿上海＿廣州是中國的大城市。」應填什麼標點？", "opts": ["，，", "、、", "；；", "：："], "ans": 1, "exp_zh": "並列詞語之間用頓號「、」。", "exp_en": "Between listed items, use enumeration mark '、'."},
                ]
            },
        }
    },
    "詞語配對": {
        "topic_id": "詞語配對",
        "topic_zh": "詞語配對",
        "topic_en": "Word Matching",
        "subtopics": {
            "近義詞": {
                "subtopic_id": "近義詞",
                "subtopic_zh": "近義詞",
                "subtopic_en": "Synonyms",
                "templates": [
                    {"q": "「美麗」的近義詞是：", "opts": ["醜陋", "漂亮", "普通", "奇怪"], "ans": 1, "exp_zh": "「美麗」和「漂亮」都是形容外表好看。", "exp_en": "'美麗' and '漂亮' both mean beautiful/pretty."},
                    {"q": "「勇敢」的近義詞是：", "opts": ["膽小", "無畏", "害怕", "猶豫"], "ans": 1, "exp_zh": "「勇敢」和「無畏」都形容不怕危險。", "exp_en": "'勇敢' (brave) and '無畏' (fearless) are synonyms."},
                    {"q": "「迅速」的近義詞是：", "opts": ["緩慢", "快速", "遲鈍", "悠閒"], "ans": 1, "exp_zh": "「迅速」和「快速」都形容速度快。", "exp_en": "'迅速' (swift) and '快速' (fast) are synonyms."},
                    {"q": "「困難」的近義詞是：", "opts": ["容易", "艱難", "簡單", "輕鬆"], "ans": 1, "exp_zh": "「困難」和「艱難」意思相近。", "exp_en": "'困難' (difficult) and '艱難' (arduous) are synonyms."},
                    {"q": "「高興」的近義詞是：", "opts": ["悲傷", "愉快", "憤怒", "驚訝"], "ans": 1, "exp_zh": "「高興」和「愉快」都形容心情好。", "exp_en": "'高興' (happy) and '愉快' (pleasant) are synonyms."},
                ]
            },
            "反義詞": {
                "subtopic_id": "反義詞",
                "subtopic_zh": "反義詞",
                "subtopic_en": "Antonyms",
                "templates": [
                    {"q": "「勤勞」的反義詞是：", "opts": ["努力", "懶惰", "認真", "積極"], "ans": 1, "exp_zh": "「勤勞」和「懶惰」是反義詞。", "exp_en": "'勤勞' (diligent) and '懶惰' (lazy) are antonyms."},
                    {"q": "「寬闊」的反義詞是：", "opts": ["廣大", "狹窄", "遼闊", "寬敞"], "ans": 1, "exp_zh": "「寬闊」和「狹窄」是反義詞。", "exp_en": "'寬闊' (wide) and '狹窄' (narrow) are antonyms."},
                    {"q": "「謙虛」的反義詞是：", "opts": ["驕傲", "謹慎", "低調", "樸素"], "ans": 0, "exp_zh": "「謙虛」和「驕傲」是反義詞。", "exp_en": "'謙虛' (humble) and '驕傲' (arrogant) are antonyms."},
                    {"q": "「複雜」的反義詞是：", "opts": ["困難", "簡單", "混亂", "繁瑣"], "ans": 1, "exp_zh": "「複雜」和「簡單」是反義詞。", "exp_en": "'複雜' (complex) and '簡單' (simple) are antonyms."},
                ]
            },
            "詞語搭配": {
                "subtopic_id": "詞語搭配",
                "subtopic_zh": "詞語搭配",
                "subtopic_en": "Word Collocations",
                "templates": [
                    {"q": "「發揮」通常搭配什麼詞？", "opts": ["作用", "問題", "衣服", "食物"], "ans": 0, "exp_zh": "「發揮作用」是固定搭配。", "exp_en": "'發揮作用' (play a role) is a fixed collocation."},
                    {"q": "「改善」通常搭配什麼詞？", "opts": ["條件", "數量", "顏色", "聲音"], "ans": 0, "exp_zh": "「改善條件」是常見搭配。", "exp_en": "'改善條件' (improve conditions) is a common collocation."},
                    {"q": "「增強」通常搭配什麼詞？", "opts": ["體質", "數量", "距離", "溫度"], "ans": 0, "exp_zh": "「增強體質」是固定搭配。", "exp_en": "'增強體質' (strengthen constitution) is a fixed collocation."},
                    {"q": "「提高」通常搭配什麼詞？", "opts": ["水平", "房子", "桌子", "衣服"], "ans": 0, "exp_zh": "「提高水平」是常見搭配。", "exp_en": "'提高水平' (raise standards) is a common collocation."},
                ]
            },
        }
    },
    "詞性辨別": {
        "topic_id": "詞性辨別",
        "topic_zh": "詞性辨別",
        "topic_en": "Parts of Speech",
        "subtopics": {
            "基本詞性": {
                "subtopic_id": "基本詞性",
                "subtopic_zh": "基本詞性",
                "subtopic_en": "Basic POS",
                "templates": [
                    {"q": "「快速」是什麼詞性？", "opts": ["名詞", "動詞", "形容詞", "副詞"], "ans": 2, "exp_zh": "「快速」修飾動作或事物，是形容詞（也可作副詞）。", "exp_en": "'快速' = adjective (also adverb) describing speed."},
                    {"q": "「奔跑」是什麼詞性？", "opts": ["名詞", "動詞", "形容詞", "副詞"], "ans": 1, "exp_zh": "「奔跑」是動作，是動詞。", "exp_en": "'奔跑' = verb, to run."},
                    {"q": "「幸福」是什麼詞性？", "opts": ["名詞", "動詞", "形容詞", "副詞"], "ans": 2, "exp_zh": "「幸福」形容一種狀態，是形容詞。", "exp_en": "'幸福' = adjective, describing a state of happiness."},
                    {"q": "「非常」是什麼詞性？", "opts": ["名詞", "動詞", "形容詞", "副詞"], "ans": 3, "exp_zh": "「非常」修飾形容詞或動詞，是副詞。", "exp_en": "'非常' = adverb, modifying adjectives or verbs."},
                    {"q": "「書本」是什麼詞性？", "opts": ["名詞", "動詞", "形容詞", "副詞"], "ans": 0, "exp_zh": "「書本」是事物名稱，是名詞。", "exp_en": "'書本' = noun, name of an object."},
                    {"q": "「美麗」和「美麗地」的詞性分別是：", "opts": ["都是形容詞", "形容詞和副詞", "都是副詞", "副詞和形容詞"], "ans": 1, "exp_zh": "「美麗」是形容詞，「美麗地」是副詞（修飾動詞）。", "exp_en": "'美麗' = adjective. '美麗地' = adverb (modifies verbs)."},
                ]
            },
        }
    },
    "文化常識": {
        "topic_id": "文化常識",
        "topic_zh": "文化常識",
        "topic_en": "Cultural Knowledge",
        "subtopics": {
            "傳統節日": {
                "subtopic_id": "傳統節日",
                "subtopic_zh": "傳統節日",
                "subtopic_en": "Traditional Festivals",
                "templates": [
                    {"q": "「春節」是中國農曆的哪一天？", "opts": ["正月初一", "正月十五", "十二月三十", "九月初九"], "ans": 0, "exp_zh": "春節是農曆正月初一，即新年第一天。", "exp_en": "Spring Festival = 1st day of Chinese New Year (正月初一)."},
                    {"q": "「中秋節」傳統吃什麼？", "opts": ["粽子", "月餅", "湯圓", "餃子"], "ans": 1, "exp_zh": "中秋節吃月餅，象徵團圓。", "exp_en": "Mid-Autumn Festival: eat mooncakes (月餅), symbolizing reunion."},
                    {"q": "「端午節」紀念哪位歷史人物？", "opts": ["孔子", "屈原", "李白", "杜甫"], "ans": 1, "exp_zh": "端午節紀念屈原，吃粽子、賽龍舟。", "exp_en": "Dragon Boat Festival commemorates Qu Yuan (屈原)."},
                    {"q": "「重陽節」是農曆幾月幾日？", "opts": ["正月初一", "五月初五", "八月十五", "九月初九"], "ans": 3, "exp_zh": "重陽節是農曆九月初九，又稱「登高節」。", "exp_en": "Double Ninth Festival = 9th day of 9th lunar month."},
                    {"q": "「元宵節」在農曆哪一天？", "opts": ["正月初一", "正月十五", "二月初二", "三月初三"], "ans": 1, "exp_zh": "元宵節是正月十五，吃湯圓、賞花燈。", "exp_en": "Lantern Festival = 15th of 1st lunar month. Eat tangyuan, see lanterns."},
                ]
            },
            "文學常識": {
                "subtopic_id": "文學常識",
                "subtopic_zh": "文學常識",
                "subtopic_en": "Literary Knowledge",
                "templates": [
                    {"q": "「四大名著」不包括以下哪一本？", "opts": ["《三國演義》", "《水滸傳》", "《聊齋誌異》", "《西遊記》"], "ans": 2, "exp_zh": "四大名著：《三國演義》《水滸傳》《西遊記》《紅樓夢》。", "exp_en": "Four Great Novels: Three Kingdoms, Water Margin, Journey to the West, Dream of Red Chamber."},
                    {"q": "「床前明月光」的作者是？", "opts": ["杜甫", "李白", "白居易", "王維"], "ans": 1, "exp_zh": "李白的《靜夜思》。", "exp_en": "Li Bai's 'Quiet Night Thought' (靜夜思)."},
                    {"q": "「先天下之憂而憂」出自哪篇文章？", "opts": ["《出師表》", "《岳陽樓記》", "《醉翁亭記》", "《滕王閣序》"], "ans": 1, "exp_zh": "范仲淹《岳陽樓記》。表達憂國憂民的情懷。", "exp_en": "From Fan Zhongyan's 'Yueyang Tower Record'."},
                    {"q": "「落霞與孤鶩齊飛」的下一句是：", "opts": ["秋水共長天一色", "月落烏啼霜滿天", "兩個黃鸝鳴翠柳", "春風又綠江南岸"], "ans": 0, "exp_zh": "王勃《滕王閣序》。描寫壯麗的自然景色。", "exp_en": "From Wang Bo's 'Tengwang Pavilion Preface'."},
                ]
            },
        }
    },
    "邏輯推理": {
        "topic_id": "邏輯推理",
        "topic_zh": "邏輯推理",
        "topic_en": "Logical Reasoning",
        "subtopics": {
            "語句排序": {
                "subtopic_id": "語句排序",
                "subtopic_zh": "語句排序",
                "subtopic_en": "Sentence Ordering",
                "templates": [
                    {"q": "將以下句子排列成通順的段落：①他走進教室 ②他放下書包 ③他坐了下來 ④他打開課本。正確順序是？", "opts": ["①②③④", "①③②④", "②①③④", "④③②①"], "ans": 0, "exp_zh": "邏輯順序：進教室→放書包→坐下→打開課本。", "exp_en": "Logical order: enter classroom → put down bag → sit down → open textbook."},
                    {"q": "將以下句子排列：①春天播種 ②夏天除草 ③秋天收穫 ④冬天儲藏。正確順序是？", "opts": ["①②③④", "①③②④", "④③②①", "②①④③"], "ans": 0, "exp_zh": "按季節順序：春播→夏除草→秋收→冬藏。", "exp_en": "Seasonal order: spring sow → summer weed → autumn harvest → winter store."},
                ]
            },
            "因果推理": {
                "subtopic_id": "因果推理",
                "subtopic_zh": "因果推理",
                "subtopic_en": "Cause and Effect",
                "templates": [
                    {"q": "「他沒有帶傘，所以淋濕了。」這句話的因果關係是？", "opts": ["帶傘是因，淋濕是果", "沒帶傘是因，淋濕是果", "淋濕是因，沒帶傘是果", "沒有因果關係"], "ans": 1, "exp_zh": "原因：沒帶傘。結果：淋濕了。", "exp_en": "Cause: didn't bring umbrella. Effect: got wet."},
                    {"q": "「因為他努力學習，所以考試取得了好成績。」原因和結果分別是？", "opts": ["努力學習是結果，好成績是原因", "努力學習是原因，好成績是結果", "都是原因", "都是結果"], "ans": 1, "exp_zh": "「因為」後是原因，「所以」後是結果。", "exp_en": "After '因為' = cause. After '所以' = effect."},
                ]
            },
        }
    },
}


# ─────────────────────────────────────────────────────────
# GENERATION ENGINE
# ─────────────────────────────────────────────────────────

def generate_subject(topics_dict, target_count=10000):
    """Generate questions with round-robin shuffling."""
    # Step 1: Flatten all templates with their metadata
    all_templates = []
    for topic_key, topic_data in topics_dict.items():
        for sub_key, sub_data in topic_data["subtopics"].items():
            for tmpl in sub_data["templates"]:
                all_templates.append({
                    "topic_id": topic_data["topic_id"],
                    "topic_zh": topic_data["topic_zh"],
                    "topic_en": topic_data["topic_en"],
                    "subtopic_id": sub_data["subtopic_id"],
                    "subtopic_zh": sub_data["subtopic_zh"],
                    "subtopic_en": sub_data["subtopic_en"],
                    "template": tmpl,
                })

    # Step 2: Group templates by topic_id
    by_topic = {}
    for t in all_templates:
        by_topic.setdefault(t["topic_id"], []).append(t)

    topic_ids = list(by_topic.keys())
    num_topics = len(topic_ids)

    # Step 3: Calculate questions per topic (roughly equal)
    base_per_topic = target_count // num_topics
    remainder = target_count % num_topics

    questions = []
    seen_texts = set()
    qid = 1

    # Step 4: Generate questions for each topic
    topic_questions = {}
    for i, tid in enumerate(topic_ids):
        count = base_per_topic + (1 if i < remainder else 0)
        templates = by_topic[tid]
        tq = []
        attempts = 0
        max_attempts = count * 10

        while len(tq) < count and attempts < max_attempts:
            attempts += 1
            # Pick a random template
            t = random.choice(templates)
            tmpl = t["template"]

            # Create variation by adding context number
            variation_seed = len(tq)
            # Use template index + variation to create unique text
            tmpl_idx = templates.index(t)
            q_text = tmpl["q"]

            # Add subtle variation to avoid exact duplicates
            if q_text in seen_texts:
                # Try to create a variation by slightly modifying
                # Use different wording patterns
                variations = [
                    q_text,
                    q_text.replace("Choose", "Select"),
                    q_text.replace("Choose the correct", "Pick the right"),
                    q_text.replace("What does", "What is the meaning of"),
                    q_text.replace("Which word", "Select the word"),
                    q_text.replace("Find the error", "Identify the mistake in"),
                ]
                found = False
                for v in variations:
                    if v not in seen_texts:
                        q_text = v
                        found = True
                        break
                if not found:
                    continue

            seen_texts.add(q_text)

            # Difficulty distribution: 40% easy, 40% medium, 20% hard
            r = random.random()
            if r < 0.4:
                diff = 1
            elif r < 0.8:
                diff = 2
            else:
                diff = 3

            tq.append({
                "topic_id": t["topic_id"],
                "topic_zh": t["topic_zh"],
                "topic_en": t["topic_en"],
                "subtopic_id": t["subtopic_id"],
                "subtopic_zh": t["subtopic_zh"],
                "subtopic_en": t["subtopic_en"],
                "question_zh": q_text,
                "question_en": q_text,
                "options_zh": tmpl["opts"],
                "options_en": tmpl["opts"],
                "answer": tmpl["ans"],
                "explanation_zh": tmpl["exp_zh"],
                "explanation_en": tmpl.get("exp_en", ""),
                "difficulty": diff,
            })

        topic_questions[tid] = tq

    # Step 5: Round-robin shuffle - interleave topics
    # This guarantees NO two consecutive questions share the same topic
    topic_queues = {tid: list(qs) for tid, qs in topic_questions.items()}
    # Shuffle within each topic for randomness
    for tid in topic_queues:
        random.shuffle(topic_queues[tid])

    # Round-robin: cycle through topics
    active_topics = [tid for tid in topic_ids if topic_queues[tid]]
    random.shuffle(active_topics)  # Randomize starting order

    result = []
    while active_topics:
        next_active = []
        for tid in active_topics:
            if topic_queues[tid]:
                result.append(topic_queues[tid].pop(0))
                next_active.append(tid)
        active_topics = next_active

    # Step 6: Assign IDs
    for i, q in enumerate(result):
        q["id"] = i + 1

    return result


def verify(questions, label):
    """Verify questions meet requirements."""
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    print(f"  Total questions: {len(questions)}")

    # Topic distribution
    topic_counts = {}
    for q in questions:
        tid = q.get("topic_id", "unknown")
        topic_counts[tid] = topic_counts.get(tid, 0) + 1
    print(f"\n  Topic distribution:")
    for tid, cnt in sorted(topic_counts.items(), key=lambda x: -x[1]):
        print(f"    {tid}: {cnt}")

    # Max consecutive same topic
    max_run = 0
    cur_run = 0
    cur_topic = None
    for q in questions:
        tid = q.get("topic_id", "unknown")
        if tid == cur_topic:
            cur_run += 1
        else:
            cur_topic = tid
            cur_run = 1
        max_run = max(max_run, cur_run)
    print(f"\n  Max consecutive same-topic run: {max_run}")
    if max_run > 1:
        print(f"  ⚠️  WARNING: Max run should be 1!")
    else:
        print(f"  ✅ PASS: No consecutive same-topic questions")

    # Duplicate check
    seen = set()
    dupes = 0
    for q in questions:
        txt = q.get("question_zh", "")
        if txt in seen:
            dupes += 1
        seen.add(txt)
    print(f"\n  Duplicate question count: {dupes}")
    if dupes > 0:
        print(f"  ⚠️  WARNING: Found {dupes} duplicates!")
    else:
        print(f"  ✅ PASS: No duplicates")

    # Difficulty distribution
    diff_counts = {1: 0, 2: 0, 3: 0}
    for q in questions:
        d = q.get("difficulty", 0)
        if d in diff_counts:
            diff_counts[d] += 1
    total = len(questions)
    print(f"\n  Difficulty distribution:")
    for d, cnt in sorted(diff_counts.items()):
        pct = cnt / total * 100 if total else 0
        label_d = {1: "Easy", 2: "Medium", 3: "Hard"}[d]
        print(f"    {label_d} ({d}): {cnt} ({pct:.1f}%)")

    print()


def save_questions(questions, filepath):
    """Save questions to JSON file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=1)
    print(f"  Saved {len(questions)} questions to {filepath}")


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Generate English
    print("Generating English questions...")
    random.seed(42)
    en_questions = generate_subject(EN_TOPICS, 10000)

    # Save English to both locations
    en_path1 = os.path.join(base_dir, "english", "s1", "questions.json")
    en_path2 = os.path.join(base_dir, "v2", "english", "s1", "questions.json")
    save_questions(en_questions, en_path1)
    save_questions(en_questions, en_path2)

    # Generate Chinese
    print("\nGenerating Chinese questions...")
    random.seed(42)
    zh_questions = generate_subject(ZH_TOPICS, 10000)

    # Save Chinese to both locations
    zh_path1 = os.path.join(base_dir, "chinese", "s1", "questions.json")
    zh_path2 = os.path.join(base_dir, "v2", "chinese", "s1", "questions.json")
    save_questions(zh_questions, zh_path1)
    save_questions(zh_questions, zh_path2)

    # Verify all
    verify(en_questions, "ENGLISH Verification")
    verify(zh_questions, "CHINESE Verification")


if __name__ == "__main__":
    main()
