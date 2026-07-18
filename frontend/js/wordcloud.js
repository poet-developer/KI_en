// KOTE 44 (인덱스 0~43)
const KOTE_44 = [
  "Complaint / Dissatisfaction",
  "Welcome / Favor",
  "Impressed / Admiration",
  "Fed up",
  "Gratitude",
  "Sadness",
  "Anger / Rage",
  "Respect",
  "Anticipation",
  "Arrogance / Disregard",
  "Pitifulness / Disappointment",
  "Resolute",
  "Doubt / Distrust",
  "Pride",
  "Comfort / Cozy",
  "Curiosity / Interest",
  "Caring",
  "Shame",
  "Fear/Scary",
  "Despair",
  "Pathetic ",
  "Disgust / Repulsiveness",
  "Irritation",
  "Preposterous ",
  "NO EMOTION",
  "Defeat / Self-hatred",
  "Laziness",
  "Fatigue / Exhaustion",
  "Pleasure / Excitement",
  "Realization",
  "Guilt",
  "Loathing / Hatred",
  "Pleased (Cute / Pretty)",
  "Embarrassment / Awkwardness",
  "Shock",
  "Burden / Unwillingness",
  "Sorrow",
  "Boredom",
  "Pity / Compassion",
  "Surprise",
  "Happiness",
  "Anxiety / Worry",
  "Joy",
  "Relief / Trust",
];

// 기본값
let selected = "Complaint / Dissatisfaction";

let currentScript = document.currentScript;

let poet = currentScript.dataset.poet;

const poetDirMap = {
  김소월: "kim",
  윤동주: "yun",
  이상: "lee",
  임화: "lim",
  한용운: "han",
};

let dir = poetDirMap[poet];
console.log("Selected poet:", poet, "Directory:", dir);

const dropdown = document.getElementById("emotionDropdown");
const toggleBtn = document.getElementById("toggleBtn");
const menu = document.getElementById("menu");
const selectedText = document.getElementById("selectedText");
const activeAuthor = document.querySelector(".author-btn.active");

// const debugOut = document.getElementById("debugOut");
// 이미지 변경 함수
const desc = document.querySelector(".emotion-description");

function setSelected(value) {
  selected = value;
  selectedText.textContent = value;
  // debugOut.textContent = value;

  // ✅ 선택된 감정의 idx 찾기
  const idx = KOTE_44.indexOf(value);

  // ✅ idx로 이미지 로드: img/{idx}.jpg
  const imgPath = `../img/${dir}/${idx}.png`;

  // ✅ description 영역에 이미지 삽입
  desc.innerHTML = `
            <img src="${imgPath}" alt="emotion-${idx}" onerror="this.remove();">
        `;

  // aria-selected 업데이트
  [...menu.querySelectorAll(".item")].forEach((btn) => {
    btn.setAttribute("aria-selected", String(btn.dataset.value === value));
  });
}

function openMenu() {
  dropdown.classList.add("open");
  toggleBtn.setAttribute("aria-expanded", "true");
}
function closeMenu() {
  dropdown.classList.remove("open");
  toggleBtn.setAttribute("aria-expanded", "false");
}
function toggleMenu() {
  dropdown.classList.contains("open") ? closeMenu() : openMenu();
}

// 메뉴 렌더
function renderMenu() {
  menu.innerHTML = "";
  KOTE_44.forEach((emo, idx) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "item";
    btn.dataset.value = emo;
    btn.setAttribute("role", "option");
    btn.setAttribute("aria-selected", String(emo === selected));
    btn.innerHTML = `<span class="idx">${idx}</span> <span style="color:black;">${emo}</span>`;
    btn.addEventListener("click", () => {
      setSelected(emo);
      updateWordcloudDescription();
      closeMenu();
    });
    menu.appendChild(btn);
  });
}

// 버튼 클릭
toggleBtn.addEventListener("click", toggleMenu);

// 바깥 클릭하면 닫기
document.addEventListener("click", (e) => {
  if (!dropdown.contains(e.target)) closeMenu();
});

// ESC로 닫기
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") closeMenu();
});

function updateWordcloudDescription() {
  const selectedEmotion = selected || "selected emotion";

  const description = document.getElementById("wordcloudDescription");

  description.innerHTML = `
    This word cloud visualizes the words in <b>${activeAuthor.textContent.trim()}</b>'s
    poetry that are most strongly associated with <b>${selectedEmotion}</b>.
  `;
}

// 초기화
renderMenu();
updateWordcloudDescription();
setSelected(selected);
