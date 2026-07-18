from pathlib import Path

ROOT = Path(__file__).parent

EMOTIONS = {
    "불평/불만": "Complaint / Dissatisfaction", "환영/호의": "Welcome / Favor",
    "감동/감탄": "Being moved / Admiration", "지긋지긋": "Weariness",
    "고마움": "Gratitude", "슬픔": "Sadness", "화남/분노": "Anger / Rage",
    "존경": "Respect", "기대감": "Anticipation", "우쭐댐/무시함": "Conceit / Disdain",
    "안타까움/실망": "Regret / Disappointment", "비장함": "Solemn resolve",
    "의심/불신": "Doubt / Distrust", "뿌듯함": "Pride", "편안/쾌적": "Comfort / Ease",
    "신기함/관심": "Wonder / Interest", "아껴주는": "Affection", "부끄러움": "Shame",
    "공포/무서움": "Fear", "절망": "Despair", "한심함": "Contempt",
    "역겨움/징그러움": "Disgust / Revulsion", "짜증": "Irritation", "어이없음": "Disbelief",
    "없음": "None", "패배/자기혐오": "Defeat / Self-loathing", "귀찮음": "Annoyance",
    "힘듦/지침": "Exhaustion", "즐거움/신남": "Enjoyment / Excitement",
    "깨달음": "Realization", "죄책감": "Guilt", "증오/혐오": "Hatred / Aversion",
    "흐뭇함(귀여움/예쁨)": "Delight (Cuteness / Beauty)", "당황/난처": "Embarrassment / Awkwardness",
    "경악": "Shock", "부담/안_내킴": "Reluctance / Burden", "부담/안내킴": "Reluctance / Burden",
    "서러움": "Sorrow", "재미없음": "Boredom", "불쌍함/연민": "Pity / Compassion",
    "놀람": "Surprise", "행복": "Happiness", "불안/걱정": "Anxiety / Worry",
    "기쁨": "Joy", "안심/신뢰": "Relief / Trust",
}

NAMES = {"김소월": "Kim Sowol", "윤동주": "Yun Dong-ju", "이상": "Yi Sang", "임화": "Im Hwa", "한용운": "Han Yong-un"}
TITLES = {
    "진달래꽃": "Azaleas", "산유화": "Mountain Flowers", "엄마야 누나야": "Mother, Sister",
    "서시": "Prologue", "새로운 길": "A New Road", "공상": "Reverie",
    "꽃나무": "Flowering Tree", "이런 시": "A Poem Like This", "보통기념": "Ordinary Commemoration",
    "현해탄": "The Korea Strait", "우리 오빠와 화로": "My Brother and the Brazier", "지상의 시": "Earthly Poetry",
    "나룻배와 행인": "The Ferryboat and the Traveler", "알 수 없어요": "I Do Not Know", "밤은 고요하고": "The Night Is Still",
}

UI = {
    "한국 근현대시 감정 시각화 인터페이스": "An Emotion-Visualization Interface for Modern Korean Poetry",
    "가까이 읽기": "Explore individual poems and line-level emotions",
    "멀리서 읽기": "Explore emotional patterns across poets and works",
    "함께 읽기(Co-Reading)": "Co-Reading", "함께 읽기": "Read Together",
    "감정 선택": "Select Emotion", "시 선택": "Select a Poem", "시 전문": "Poem Text",
    "선택해 주세요": "Choose a poem", "시를 선택하면 전문이 표시됩니다.": "Select a poem to display its full text.",
    "지우기": "Clear", "배경을 클릭하거나 ESC를 누르면 닫힙니다.": "Click outside the dialog or press Esc to close.",
    "태그 정보가 없습니다.": "No emotion-tag data is available.", "제시한 세가지 시는 샘플입니다.": "The three poems shown here are samples.",
    "단어가 클수록 해당 감정 예측에 더 크게 기여한 시인의 어휘를 의미한다.": "Larger words contributed more strongly to the model's prediction of the selected emotion.",
    "텍스트를 입력해주세요.": "Please enter text.", "이 프로토타입은 지정된 한 문장에만 반응합니다.": "This prototype responds only to the provided poem text.",
    "닫기": "Close",
}

for path in [ROOT / "index.html", *ROOT.joinpath("frontend").rglob("*.html")]:
    text = path.read_text(encoding="utf-8")
    text = text.replace('lang="ko"', 'lang="en"')
    for old, new in UI.items():
        text = text.replace(old, new)
    for old, new in NAMES.items():
        text = text.replace(f">{old}<", f">{new}<")
        text = text.replace(f"| {old}", f"| {new}")
    for old, new in TITLES.items():
        text = text.replace(f">{old}<", f">{new}<")
        text = text.replace(f"〈{old}〉", new).replace(f"<{old}>", new)
    for old, new in EMOTIONS.items():
        text = text.replace(f'"{old}"', f'"{new}"')
        text = text.replace(f'>{old}<', f'>{new}<')
        text = text.replace(old.replace('/', '\\u002f'), new.replace('/', '\\u002f'))
    path.write_text(text, encoding="utf-8")

for path in [ROOT / "frontend/js/app.js", ROOT / "frontend/js/wordcloud.js"]:
    text = path.read_text(encoding="utf-8")
    for old, new in EMOTIONS.items():
        text = text.replace(f'"{old}"', f'"{new}"')
    for old, new in UI.items():
        text = text.replace(f'"{old}"', f'"{new}"')
    text = text.replace('"초기화된"', '"reset"').replace('초기화된:', 'reset:')
    path.write_text(text, encoding="utf-8")

for path in ROOT.joinpath("frontend/close_reading").glob("close-*.html"):
    if "-menu" in path.name:
        continue
    text = path.read_text(encoding="utf-8")
    script = '<script src="../js/bilingual-poems.js"></script>'
    if script not in text:
        text = text.replace("</body>", f"{script}\n</body>")
    old_modal = '''function openModal(text) {
    modalLineText.textContent = `"${text}"`;
    overlay.classList.add("open");'''
    new_modal = '''function openModal(line) {
    const english = line.querySelector(".poem-line-en")?.textContent.trim() || line.textContent.trim();
    const korean = line.querySelector(".poem-line-ko")?.textContent.trim() || "";
    modalLineText.replaceChildren();

    const englishLine = document.createElement("span");
    englishLine.className = "modal-line-en";
    englishLine.textContent = english;
    modalLineText.appendChild(englishLine);

    if (korean) {
      const koreanLine = document.createElement("span");
      koreanLine.className = "modal-line-ko";
      koreanLine.lang = "ko";
      koreanLine.textContent = korean;
      modalLineText.appendChild(koreanLine);
    }

    overlay.classList.add("open");'''
    text = text.replace(old_modal, new_modal)
    text = text.replace("openModal(line.textContent.trim());", "openModal(line);")
    path.write_text(text, encoding="utf-8")

emotion_css = ROOT / "frontend/styles/emotion_tag.css"
text = emotion_css.read_text(encoding="utf-8")
for old, new in EMOTIONS.items():
    escaped = old.replace("/", r"\/").replace("(", r"\(").replace(")", r"\)")
    text = text.replace(f"#{escaped}", f'[id="{new}"]')
emotion_css.write_text(text, encoding="utf-8")
