import streamlit as st
import random
import os
import re
from datetime import datetime

st.set_page_config(page_title="Sikho Smart", page_icon="🌟", layout="centered", initial_sidebar_state="collapsed")

# --------- Child-friendly multilingual content ---------
I18N = {
 "English": {
  "tag":"Learn • Play • Ask • Grow", "welcome":"Welcome, Young Learner!",
  "intro":"Choose a subject, answer fun questions and earn stars. Ask Sikho Dost when you need help.",
  "language":"Language", "class":"Choose your class", "home":"Home", "quiz":"Quiz Game", "friend":"Sikho Dost",
  "subject":"Choose a subject", "subjects":["Maths","English","Science","General Knowledge"],
  "start":"Start / New Quiz", "hint":"Show a hint", "submit":"Check answer", "next":"Next question",
  "correct":"Brilliant! You earned 10 points and ⭐", "wrong":"Good try! Read the explanation and learn for next time.",
  "finished":"Quiz complete!", "score":"Your score", "stars":"Stars", "points":"Points",
  "ask":"Ask Sikho Dost", "question":"Type your learning question", "send":"Ask",
  "privacy":"Safety first: never share your full name, phone number, home address, password or private photos.",
  "ai_note":"AI can make mistakes. Check important answers with your teacher or trusted adult.",
  "teacher":"Teacher corner", "teacher_note":"Use this screen for a supervised classroom demonstration. No student account is required.",
  "no_ai":"Live AI is not configured yet. Ask your teacher to add an API key in Streamlit Secrets. Quiz mode works without AI.",
  "placeholder":"For example: Why do plants need sunlight?",
  "progress":"Questions answered", "offline":"Quiz questions are built into the app. Internet is needed for live AI."
 },
 "سنڌي": {
  "tag":"سکو • کيڏو • پڇو • اڳتي وڌو", "welcome":"ڀلي ڪري آيا، پيارا شاگرد!",
  "intro":"مضمون چونڊيو، مزيدار سوالن جا جواب ڏيو ۽ تارا حاصل ڪريو. مدد لاءِ سکيو دوست کان پڇو.",
  "language":"ٻولي", "class":"پنهنجو ڪلاس چونڊيو", "home":"گهر", "quiz":"سوالن جي راند", "friend":"سکيو دوست",
  "subject":"مضمون چونڊيو", "subjects":["رياضي","انگريزي","سائنس","عام ڄاڻ"],
  "start":"نئين راند شروع ڪريو", "hint":"اشارو ڏسو", "submit":"جواب چيڪ ڪريو", "next":"اڳيون سوال",
  "correct":"شاباس! توهان 10 پوائنٽ ۽ ⭐ حاصل ڪيو", "wrong":"سٺي ڪوشش! وضاحت پڙهو ۽ سکندا رهو.",
  "finished":"سوالن جي راند مڪمل!", "score":"توهان جو اسڪور", "stars":"تارا", "points":"پوائنٽ",
  "ask":"سکيو دوست کان پڇو", "question":"پنهنجو سکيا وارو سوال لکو", "send":"پڇو",
  "privacy":"حفاظت پهرين: پنهنجو پورو نالو، فون نمبر، گهر جو پتو يا پاسورڊ نه ڏيو.",
  "ai_note":"AI کان غلطي ٿي سگهي ٿي. اهم جواب استاد کان ضرور چيڪ ڪرايو.",
  "teacher":"استاد جو حصو", "teacher_note":"هن حصي کي استاد جي نگراني ۾ ڪلاس جي مظاهري لاءِ استعمال ڪريو. شاگردن جي اڪائونٽ جي ضرورت ناهي.",
  "no_ai":"لائيو AI اڃا ترتيب ڏنل ناهي. استاد Streamlit Secrets ۾ API key شامل ڪري. سوالن جي راند AI کان سواءِ به ڪم ڪندي.",
  "placeholder":"مثال: ٻوٽن کي سج جي روشني ڇو گهرجي؟",
  "progress":"حل ڪيل سوال", "offline":"سوال ايپ ۾ موجود آهن. لائيو AI لاءِ انٽرنيٽ گهربل آهي."
 },
 "اردو": {
  "tag":"سیکھیں • کھیلیں • پوچھیں • آگے بڑھیں", "welcome":"خوش آمدید، پیارے طالب علم!",
  "intro":"مضمون منتخب کریں، دلچسپ سوال حل کریں اور ستارے حاصل کریں۔ مدد کے لیے سیکھو دوست سے پوچھیں۔",
  "language":"زبان", "class":"اپنی جماعت منتخب کریں", "home":"ہوم", "quiz":"کوئز کھیل", "friend":"سیکھو دوست",
  "subject":"مضمون منتخب کریں", "subjects":["ریاضی","انگریزی","سائنس","عام معلومات"],
  "start":"نیا کوئز شروع کریں", "hint":"اشارہ دیکھیں", "submit":"جواب چیک کریں", "next":"اگلا سوال",
  "correct":"شاباش! آپ نے 10 پوائنٹس اور ⭐ حاصل کیا", "wrong":"اچھی کوشش! وضاحت پڑھیں اور سیکھتے رہیں۔",
  "finished":"کوئز مکمل!", "score":"آپ کا اسکور", "stars":"ستارے", "points":"پوائنٹس",
  "ask":"سیکھو دوست سے پوچھیں", "question":"اپنا تعلیمی سوال لکھیں", "send":"پوچھیں",
  "privacy":"حفاظت پہلے: اپنا پورا نام، فون نمبر، گھر کا پتہ یا پاس ورڈ نہ بتائیں۔",
  "ai_note":"AI سے غلطی ہو سکتی ہے۔ اہم جواب استاد سے ضرور چیک کروائیں۔",
  "teacher":"استاد کا گوشہ", "teacher_note":"اس حصے کو استاد کی نگرانی میں کلاس کے مظاہرے کے لیے استعمال کریں۔ طالب علم کا اکاؤنٹ ضروری نہیں۔",
  "no_ai":"لائیو AI ابھی ترتیب نہیں دیا گیا۔ استاد Streamlit Secrets میں API key شامل کریں۔ کوئز AI کے بغیر بھی کام کرتا ہے۔",
  "placeholder":"مثال: پودوں کو سورج کی روشنی کیوں چاہیے؟",
  "progress":"حل شدہ سوالات", "offline":"سوالات ایپ میں موجود ہیں۔ لائیو AI کے لیے انٹرنیٹ ضروری ہے۔"
 }
}

# Question bank: one set per subject; class selector is available, with grade-aware content to be expanded.
BANK = {
 "Maths":[
  ("What is 7 + 5?",["10","11","12","13"],2,"Count five steps after seven.","7 + 5 = 12."),
  ("What is 3 × 4?",["7","12","14","16"],1,"Think of 3 groups of 4.","3 groups of 4 make 12."),
  ("Which number is even?",["9","13","16","21"],2,"An even number can be split into two equal groups.","16 is even because it divides by 2."),
  ("How many sides does a triangle have?",["2","3","4","5"],1,"Tri means three.","A triangle has 3 sides."),
  ("What is 20 − 8?",["10","11","12","13"],2,"Count back eight from twenty.","20 − 8 = 12.")
 ],
 "English":[
  ("Which word names an animal?",["Run","Cat","Blue","Quickly"],1,"Think of a pet that says meow.","Cat is the name of an animal."),
  ("Choose the correct spelling.",["Skool","School","Scool","Schol"],1,"A place where children learn.","The correct spelling is School."),
  ("What is the opposite of hot?",["Warm","Cold","Big","Fast"],1,"Think about ice.","Cold is the opposite of hot."),
  ("Which is a naming word (noun)?",["Jump","Beautiful","Book","Slowly"],2,"You can hold it and read it.","Book is a noun."),
  ("Choose the plural of child.",["Childs","Childes","Children","Child"],2,"This is an irregular plural.","Children is the plural of child.")
 ],
 "Science":[
  ("Which part of a plant takes in water?",["Flower","Root","Fruit","Leaf"],1,"It grows under the soil.","Roots take in water from the soil."),
  ("Which planet do we live on?",["Mars","Venus","Earth","Jupiter"],2,"It is our home planet.","We live on planet Earth."),
  ("What do humans use to breathe?",["Lungs","Ears","Teeth","Hair"],0,"These organs are inside your chest.","Lungs help us breathe."),
  ("Which one is a source of light?",["Stone","Sun","Chair","Book"],1,"It shines in the daytime.","The Sun gives us light and heat."),
  ("Water becomes ice when it…",["Gets colder","Gets louder","Gets bigger","Gets darker"],0,"Think about a freezer.","Water freezes when it gets cold enough.")
 ],
 "General Knowledge":[
  ("How many days are in a week?",["5","6","7","8"],2,"Count Monday through Sunday.","There are 7 days in a week."),
  ("Which is Pakistan's national language?",["Arabic","Urdu","Chinese","French"],1,"It is widely used across Pakistan.","Urdu is Pakistan's national language."),
  ("Mixing red and yellow paint makes…",["Green","Purple","Orange","Blue"],2,"Think of a fruit with this colour.","Red and yellow make orange."),
  ("Which animal is commonly called king of the jungle?",["Lion","Rabbit","Goat","Horse"],0,"It has a mane.","The lion is commonly called king of the jungle."),
  ("What should you do before eating?",["Wash hands","Play in mud","Touch your eyes","Skip water"],0,"Clean hands help keep germs away.","Wash hands before eating.")
 ]
}

SD_TRANSLATIONS = {
 "Maths":[
  ("7 + 5 ڪيترو ٿيندو؟",["10","11","12","13"],"7 کان پوءِ پنج ڳڻيو.","7 + 5 = 12."),
  ("3 × 4 ڪيترو ٿيندو؟",["7","12","14","16"],"چار جا ٽي گروپ سوچيو.","چار جا ٽي گروپ 12 ٿين ٿا."),
  ("ڪهڙو عدد جفت آهي؟",["9","13","16","21"],"جفت عدد ٻن برابر حصن ۾ ورهائجي ٿو.","16 جفت عدد آهي."),
  ("ٽڪنڊي جا ڪيترا پاسا آهن؟",["2","3","4","5"],"ٽري جو مطلب ٽي آهي.","ٽڪنڊي جا 3 پاسا آهن."),
  ("20 − 8 ڪيترو ٿيندو؟",["10","11","12","13"],"20 کان اٺ پوئتي ڳڻيو.","20 − 8 = 12.")
 ],
 "Science":[
  ("ٻوٽي جو ڪهڙو حصو پاڻي جذب ڪري ٿو؟",["گل","پاڙ","ميوو","پن"],"اهو زمين اندر وڌي ٿو.","پاڙ پاڻي جذب ڪري ٿي."),
  ("اسان ڪهڙي سياري تي رهون ٿا؟",["مريخ","زهره","ڌرتي","مشتري"],"هي اسان جو گهر آهي.","اسان ڌرتيءَ تي رهون ٿا."),
  ("ساهه کڻڻ لاءِ ڪهڙا عضوا ڪم اچن ٿا؟",["ڦڦڙ","ڪن","ڏند","وار"],"اهي سيني اندر هوندا آهن.","ڦڦڙ ساهه کڻڻ ۾ مدد ڪن ٿا."),
  ("روشني جو ذريعو ڪهڙو آهي؟",["پٿر","سج","ڪرسي","ڪتاب"],"ڏينهن ۾ چمڪي ٿو.","سج روشني ۽ گرمي ڏئي ٿو."),
  ("پاڻي ٿڌو ٿيڻ سان ڇا بڻجي ٿو؟",["برف","آواز","مٽي","دونهون"],"فريزر بابت سوچيو.","پاڻي ڄمي برف بڻجي ٿو.")
 ]
}
UR_TRANSLATIONS = {
 "Maths":[
  ("7 + 5 کتنے ہوتے ہیں؟",["10","11","12","13"],"سات کے بعد پانچ گنیں۔","7 + 5 = 12۔"),
  ("3 × 4 کتنے ہوتے ہیں؟",["7","12","14","16"],"چار کے تین گروپ سوچیں۔","چار کے تین گروپ 12 ہوتے ہیں۔"),
  ("کون سا عدد جفت ہے؟",["9","13","16","21"],"جفت عدد دو برابر حصوں میں تقسیم ہوتا ہے۔","16 جفت عدد ہے۔"),
  ("مثلث کے کتنے کنارے ہوتے ہیں؟",["2","3","4","5"],"مثلث میں تین کا مطلب ہے۔","مثلث کے 3 کنارے ہوتے ہیں۔"),
  ("20 − 8 کتنے ہیں؟",["10","11","12","13"],"20 سے آٹھ قدم پیچھے گنیں۔","20 − 8 = 12۔")
 ],
 "Science":[
  ("پودے کا کون سا حصہ پانی جذب کرتا ہے؟",["پھول","جڑ","پھل","پتا"],"یہ مٹی کے اندر بڑھتا ہے۔","جڑ پانی جذب کرتی ہے۔"),
  ("ہم کس سیارے پر رہتے ہیں؟",["مریخ","زہرہ","زمین","مشتری"],"یہ ہمارا گھر ہے۔","ہم زمین پر رہتے ہیں۔"),
  ("سانس لینے کے لیے کون سے اعضا کام کرتے ہیں؟",["پھیپھڑے","کان","دانت","بال"],"یہ سینے کے اندر ہوتے ہیں۔","پھیپھڑے سانس لینے میں مدد دیتے ہیں۔"),
  ("روشنی کا ذریعہ کون سا ہے؟",["پتھر","سورج","کرسی","کتاب"],"یہ دن میں چمکتا ہے۔","سورج روشنی اور حرارت دیتا ہے۔"),
  ("پانی ٹھنڈا ہو کر کیا بنتا ہے؟",["برف","آواز","مٹی","دھواں"],"فریزر کے بارے میں سوچیں۔","پانی جم کر برف بنتا ہے۔")
 ]
}

def get_qset(subject, language):
    data = BANK[subject]
    translated = SD_TRANSLATIONS if language == "سنڌي" else UR_TRANSLATIONS if language == "اردو" else {}
    return translated.get(subject, data)

def init_state():
    defaults = {"stars":0,"points":0,"answered":0,"quiz_items":[],"q_index":0,"q_score":0,
                "chosen_subject":"Maths","grade":"Class 3","last_result":None,"chat_history":[],"quiz_lang":"English","chat_count":0}
    for k,v in defaults.items():
        if k not in st.session_state: st.session_state[k]=v
init_state()

# Friendly visual styling
st.markdown("""
<style>
.stApp{background:linear-gradient(145deg,#fff7ed 0%,#eff6ff 48%,#f0fdf4 100%)}
.block-container{max-width:850px;padding-top:1.1rem;padding-bottom:2rem}
.hero{background:linear-gradient(115deg,#3b1678,#1d4ed8);color:white;border-radius:24px;padding:22px 20px;text-align:center;box-shadow:0 8px 22px #312e8122}
.hero h1{font-size:clamp(2rem,6vw,3rem);font-weight:950;margin:0}
.hero p{color:#fde68a;font-weight:750;margin:.3rem 0}
.stButton>button{border-radius:14px;font-weight:800;min-height:2.8rem;border:1px solid #c4b5fd}
div[data-testid="stMetric"]{background:#fff;border:1px solid #e9d5ff;padding:12px;border-radius:15px}
div[data-testid="stChatMessage"]{border-radius:15px}
.smallnote{font-size:.82rem;color:#64748b}
</style>
""", unsafe_allow_html=True)

lang = st.sidebar.selectbox("🌐 Language / ٻولي / زبان", list(I18N.keys()), index=0)
t = I18N[lang]
st.markdown(f'<div class="hero"><h1>🌟 SIKHO SMART 🤖</h1><p>{t["tag"]}</p><div>G.G.H.S. Phuleli, Hyderabad · Classes 1–5</div></div>', unsafe_allow_html=True)
st.caption("AI & Digital Solutions · Stream Muqablo 2026–27")

c1,c2,c3=st.columns(3)
c1.metric("⭐ "+t["stars"],st.session_state.stars)
c2.metric("🏆 "+t["points"],st.session_state.points)
c3.metric("📚 "+t["progress"],st.session_state.answered)

tabs=st.tabs(["🏠 "+t["home"],"🎮 "+t["quiz"],"🤖 "+t["friend"],"👩‍🏫 "+t["teacher"]])

with tabs[0]:
    st.title(t["welcome"])
    st.write(t["intro"])
    st.info(t["privacy"])
    st.write("### "+t["subject"])
    display_subjects = list(zip(BANK.keys(), t["subjects"]))
    cols=st.columns(2)
    for i,(key,label) in enumerate(display_subjects):
        if cols[i%2].button(["➗ ","🔤 ","🔬 ","🌍 "][i]+label, key="home_"+key, use_container_width=True):
            st.session_state.chosen_subject=key
            st.session_state.quiz_items=get_qset(key,lang)
            st.session_state.quiz_lang=lang
            st.session_state.q_index=0;st.session_state.q_score=0;st.session_state.last_result=None
            st.rerun()
    st.selectbox(t["class"],["Class 1","Class 2","Class 3","Class 4","Class 5"],key="grade")
    st.caption(t["offline"])

with tabs[1]:
    st.title("🎯 "+t["quiz"])
    st.selectbox(t["class"],["Class 1","Class 2","Class 3","Class 4","Class 5"],key="grade_quiz")
    st.session_state.grade=st.session_state.grade_quiz
    if st.session_state.quiz_lang != lang:
        st.session_state.quiz_items=get_qset(st.session_state.chosen_subject,lang)
        st.session_state.q_index=0; st.session_state.q_score=0; st.session_state.last_result=None
        st.session_state.quiz_lang=lang
    labels=t["subjects"]
    subject_label=st.selectbox(t["subject"],labels,index=list(BANK.keys()).index(st.session_state.chosen_subject))
    subject=list(BANK.keys())[labels.index(subject_label)]
    if subject != st.session_state.chosen_subject or not st.session_state.quiz_items:
        st.session_state.chosen_subject=subject
        st.session_state.quiz_lang=lang
        st.session_state.quiz_items=get_qset(subject,lang)
        st.session_state.quiz_lang=lang
        st.session_state.q_index=0;st.session_state.q_score=0;st.session_state.last_result=None
    if st.button("🔄 "+t["start"],use_container_width=True):
        st.session_state.quiz_items=get_qset(subject,lang)
        st.session_state.quiz_lang=lang
        st.session_state.q_index=0;st.session_state.q_score=0;st.session_state.last_result=None
        st.rerun()
    items=st.session_state.quiz_items
    if items and st.session_state.last_result is None:
        idx=st.session_state.q_index
        if idx < len(items):
            q=items[idx]
            st.progress(idx/len(items),text=f"{idx+1} / {len(items)}")
            st.subheader(q[0])
            st.caption("💡 "+q[3])
            answer=st.radio("Choose one answer",q[1],index=None,key=f"ans_{lang}_{subject}_{st.session_state.grade}_{idx}")
            if st.button("✅ "+t["submit"],disabled=answer is None,key=f"submit_{idx}"):
                if q[1].index(answer)==q[2]:
                    st.session_state.q_score+=10
                    st.session_state.points+=10
                    st.session_state.stars+=1
                    st.success(t["correct"])
                else:
                    st.warning(t["wrong"])
                st.info(q[4])
                st.session_state.answered+=1
                st.session_state.q_index+=1
                if st.session_state.q_index>=len(items):
                    st.session_state.last_result=st.session_state.q_score
                st.rerun()
        else:
            st.session_state.last_result=st.session_state.q_score
    if st.session_state.last_result is not None:
        st.balloons()
        st.success(t["finished"])
        st.metric(t["score"],f'{st.session_state.last_result} / {len(items)*10}')
        if st.button("🔁 "+t["start"],key="restart_finished"):
            st.session_state.q_index=0;st.session_state.q_score=0;st.session_state.last_result=None
            st.rerun()

with tabs[2]:
    st.title("🤖 "+t["ask"])
    st.write(t["privacy"])
    st.caption(t["ai_note"])
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]): st.write(msg["content"])
    prompt=st.chat_input(t["placeholder"])
    if prompt:
        # Basic guardrail: avoid sending obvious contact details to the AI service.
        contains_contact = bool(re.search(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b", prompt) or
                                re.search(r"(?:\+?\d[\d\s().-]{7,}\d)", prompt))
        if contains_contact:
            st.warning("Please do not share phone numbers or email addresses. Keep personal information private and ask a trusted teacher for help.")
            st.stop()
        st.session_state.chat_count += 1
        if st.session_state.chat_count > 15:
            st.warning("This demo has a small daily-style chat limit per session. Please continue learning with the quiz or ask your teacher.")
            st.stop()
        st.session_state.chat_history.append({"role":"user","content":prompt})
        answer=None
        api_key = None
        try:
            api_key=st.secrets.get("OPENAI_API_KEY",None)
        except Exception:
            api_key=os.environ.get("OPENAI_API_KEY")
        if api_key:
            try:
                from openai import OpenAI
                client=OpenAI(api_key=api_key)
                language_name={"English":"English","سنڌي":"Sindhi","اردو":"Urdu"}[lang]
                response=client.responses.create(
                    model=os.getenv("OPENAI_MODEL","gpt-4.1-mini"),
                    instructions=("You are Sikho Dost, a kind, age-appropriate learning helper for children in Classes 1-5. "
                    f"Reply in {language_name}, using short simple sentences and step-by-step explanations. "
                    "Do not ask for personal information. If a child shares personal information, gently tell them not to share it "
                    "and to speak with a trusted teacher or guardian. Decline dangerous, sexual, violent or self-harm requests. "
                    "If unsure, say so and suggest asking a teacher. AI can make mistakes."),
                    input=prompt,
                    max_output_tokens=250
                )
                answer=response.output_text
            except Exception:
                answer="Sikho Dost is temporarily unavailable. Please ask your teacher and try again later."
        else:
            answer=t["no_ai"]
        st.session_state.chat_history.append({"role":"assistant","content":answer})
        st.rerun()

with tabs[3]:
    st.title("👩‍🏫 "+t["teacher"])
    st.write(t["teacher_note"])
    st.info("This public prototype does not collect student names or personal records.")
    st.metric("Questions in starter bank",sum(len(v) for v in BANK.values()))
    st.metric("Subjects",len(BANK))
    st.metric("Languages",3)
    st.warning("Current prototype: question content is a starter set; class-specific question difficulty, central student records and teacher analytics are future upgrades.")
    if st.button("Reset this browser session progress"):
        for k in ["stars","points","answered","quiz_items","q_index","q_score","last_result","chat_history"]:
            if k in st.session_state: del st.session_state[k]
        st.rerun()

st.divider()
st.caption("🌈 Sikho Smart · Learn safely · Play fairly · Ask your teacher when unsure.")
