(function () {
  const poemSelect = document.getElementById("poemSelect");
  const textarea = document.getElementById("userText");
  const revealingValue = document.getElementById("revealingValue");
  const gradientBox = document.getElementById("gradientBox");
  const analyzingEl = document.getElementById("analyzing");
  const swatch1 = document.getElementById("swatch1");
  const swatch2 = document.getElementById("swatch2");
  const legend1 = document.getElementById("legend1");
  const legend2 = document.getElementById("legend2");
  const btn = document.getElementById("analyzeButton");
  const resetBtn = document.getElementById("analyzeResetButton");
  const gradientFill = document.getElementById("gradientFill");

  const PALETTES = {
    김소월01: [
      {
        emotions: ["Melancholic", "Sadness", "Sorrow"],
        primary: { rgb: "hsla(214, 14%, 78%, 1.00)", hex: "#bec5ceff" },
        secondary: { rgb: "rgb(140, 108, 153)", hex: "#8c6c99ff" },
      },
      {
        emotions: ["Dignified", "Sadness", "Sorrow"],
        primary: { rgb: "rgb(24, 40, 61)", hex: "#18283dff" },
        secondary: { rgb: "rgb(111, 89, 119)", hex: "#6f5977ff" },
      },
    ],
    윤동주01: [
      {
        emotions: ["Pure", "Sadness", "Sorrow"],
        primary: { rgb: "rgb(237,229,225)", hex: "#ede5e1ff" },
        secondary: { rgb: "rgb(169,161,173)", hex: "#a9a1adff" },
      },
      {
        emotions: ["Delicate", "Sadness", "Sorrow"],
        primary: { rgb: "rgb(190,204,221)", hex: "#beccddff" },
        secondary: { rgb: "rgb(223,222,224)", hex: "#dfdee0ff" },
      },
    ],

    이상01: [
      {
        emotions: ["Profound", "Sorrow", "Sadness"],
        primary: { rgb: "rgb(172, 163, 175)", hex: "#aca3afff" },
        secondary: { rgb: "rgb(217, 218, 219)", hex: "#d9dadbff" },
      },
      {
        emotions: ["Melancholic", "Sorrow", "Sadness"],
        primary: { rgb: "rgb(201, 190, 206)", hex: "#c9beceff" },
        secondary: { rgb: "rgb(108, 127, 153)", hex: "#6c7f99ff" },
      },
    ],

    임화01: [
      {
        emotions: ["Resilient", "Resolute", "Sadness"],
        primary: { rgb: "rgb(204, 99, 20)", hex: "#cc6314ff" },
        secondary: { rgb: "rgb(22, 71, 135)", hex: "#164787ff" },
      },
      {
        emotions: ["Vigorous", "Resolute", "Sadness"],
        primary: { rgb: "rgb(204, 99, 20)", hex: "#cc6314ff" },
        secondary: { rgb: "rgb(26, 117, 237)", hex: "#1a75edff" },
      },
    ],

    한용운01: [
      {
        emotions: ["Melancholic", "Sadness", "Sorrow"],
        primary: { rgb: "rgb(111, 115, 119)", hex: "#6f7377ff" },
        secondary: { rgb: "rgb(64, 19, 81)", hex: "#401351ff" },
      },
      {
        emotions: ["Melancholic", "Sadness", "Sorrow"],
        primary: { rgb: "rgb(78, 89, 104)", hex: "#4e5968ff" },
        secondary: { rgb: "rgb(177, 135, 193)", hex: "#b187c1ff" },
      },
    ],

    신석정01: [
      {
        emotions: ["Pure", "Pleased (Cute / Pretty)", "Joy"],
        primary: { rgb: "rgb(203, 216, 215)", hex: "#cbd8d7ff" },
        secondary: { rgb: "rgb(224, 249, 236)", hex: "#e0f9ecff" },
      },
      {
        emotions: ["Sensuous", "Pleased (Cute / Pretty)", "Joy"],
        primary: { rgb: "rgb(78, 102, 99)", hex: "#4e6663ff" },
        secondary: { rgb: "rgb(139, 196, 166)", hex: "#8bc4a6ff" },
      },
    ],

    김수영01: [
      {
        emotions: ["Deep", "Pitifulness / Disappointment", "Sadness"],
        primary: { rgb: "rgb(76, 26, 30)", hex: "#4c1a1eff" },
        secondary: { rgb: "rgb(153, 141, 134)", hex: "#998e86ff" },
      },
      {
        emotions: ["Deep", "Pitifulness / Disappointment", "Sadness"],
        primary: { rgb: "rgb(91, 35, 62)", hex: "#701340ff" },
        secondary: { rgb: "rgb(144, 137, 147)", hex: "#998e86ff" },
      },
    ],

    백석01: [
      {
        emotions: ["Lovely", "Pleased (Cute / Pretty)", "Affection"],
        primary: { rgb: "rgb(249, 220, 164)", hex: "#f9dca4ff" },
        secondary: { rgb: "rgb(193, 128, 124)", hex: "#c1807cff" },
      },
      {
        emotions: ["Lovely", "Pleased (Cute / Pretty)", "Affection"],
        primary: { rgb: "rgb(124, 193, 185)", hex: "#7cc1b9ff" },
        secondary: { rgb: "rgb(249, 164, 196)", hex: "#f9a4c4ff" },
      },
    ],
  };

  if (!btn) return;

  // ✅ 시 데이터 (추가)
  const POEMS = {
    김소월01: `When you leave,
weary of seeing me,
I shall let you go gently, without a word.

From Mount Yaksan in Yeongbyeon,
I shall gather armfuls of azaleas
and scatter them along your path.

Step by step as you depart,
please tread softly
on the flowers laid before you.

When you leave,
weary of seeing me,
though I die, I shall not shed a tear.`,

    윤동주01: `Until the day I die,
may I look up at the sky without a trace of shame.
Even the wind stirring the leaves caused me anguish.
With a heart that sings of the stars,
I shall love all things that are dying
and walk the road given to me.

Tonight again, the stars are brushed by the wind.`,

    이상01: `In the middle of a field stands one flowering tree. There is not another flowering tree nearby. The tree stands in earnest bloom, as earnestly as it thinks of the tree in its thoughts. It cannot go to the tree it imagines. I suddenly ran away. As though I did it for that one tree, I made that truly strange gesture.`,

    임화01: `Even on a day of bitter burial
when all the joy and hope of youth
are laid deep beneath the earth,
the Korea Strait has never once lowered
a black mourning curtain before the young.

Today again, young people
cross this sea and return without rest,
like diligent children;
and tomorrow again,
the Korea Strait will be the strait of youth.

Forever, the Korea Strait is our strait.`,

    한용운01: `I am the ferryboat;
you are the traveler.

You trample me with muddy feet.
I carry you across the water.
Holding you, I cross every current—deep or shallow, swift or still.

If you do not come, I wait from night to day, exposed to wind, rain, and snow.
Once across, you leave without even looking back.

Yet I know that someday you will return.
Waiting for you, I weather day after day.

I am the ferryboat;
you are the traveler.`,

    신석정01: `From your eyes comes the scent
of green May
and white wild roses.

Your bright, shining eyes
hold within them
the stories of the stars.`,

    백석01: `Snow falls thick and deep.
Beautiful Natasha loves me,
and somewhere a white donkey, delighted by tonight, will bray aloud.`,

    김수영01: `Anyone who has ever taken flight
for freedom will know:
what the skylark sees
when it sings,
why the scent of blood
is mingled with freedom,
and why revolution
is a lonely thing.
`,
  };

  let CURRENT_POEM_KEY = "김소월01";
  let TARGET_SENTENCE = POEMS[CURRENT_POEM_KEY].trim();

  // ✅ select → textarea 연결 (추가)
  if (poemSelect) {
    poemSelect.addEventListener("change", function () {
      const selectedKey = this.value;
      CURRENT_POEM_KEY = selectedKey;

      if (!selectedKey) {
        textarea.value = "";
        return;
      }

      const poem = POEMS[selectedKey] || "";

      textarea.value = poem;

      // ✅ TARGET_SENTENCE 변경
      TARGET_SENTENCE = poem.trim();

      console.log(TARGET_SENTENCE);
    });
  }

  btn.addEventListener("mouseover", () => btn.classList.add("hovered"));
  btn.addEventListener("mouseout", () => btn.classList.remove("hovered"));

  btn.addEventListener("click", (e) => {
    btn.classList.add("clicked");
    setTimeout(() => btn.classList.remove("clicked"), 150);
    btn.classList.add("active");
    resetBtn.classList.remove("active");

    const text = textarea.value.trim();

    if (!text) {
      alert("Please enter text.");
      return;
    }

    // ✅ 분석중 모션 표시
    analyzingEl.classList.add("visible");

    // ✅ 기존 결과 초기화
    revealingValue.textContent = "";
    gradientBox.style.background = "#ccc";

    // ✅ 3초 딜레이 후 결과 출력
    setTimeout(() => {
      const result = analyzeText(text, CURRENT_POEM_KEY);

      if (!result) {
        analyzingEl.classList.remove("visible");
        return;
      }

      applyEmotionResult(result);
    }, 3000);
  });

  resetBtn.addEventListener("click", () => {
    // ✅ 버튼 active 토글
    resetBtn.classList.add("active");
    btn.classList.remove("active");

    // ✅ 입력 / 텍스트 초기화
    poemSelect.value = "";
    textarea.value = "";
    revealingValue.textContent = "-";
    analyzingEl.classList.remove("visible");

    // ✅ wipe 애니메이션으로 회색 되돌리기
    const initialGray = emotionColors["reset"];

    gradientFill.style.transition = "none";
    gradientFill.style.transform = "translateX(-100%)";

    gradientFill.style.background = `linear-gradient(90deg, ${initialGray}, ${initialGray})`;

    requestAnimationFrame(() => {
      gradientFill.style.transition = "transform 0.9s cubic-bezier(.4,0,.2,1)";
      gradientFill.style.transform = "translateX(0)";
    });

    // ✅ 하단 legend & swatch 초기화
    swatch1.style.background = initialGray;
    swatch2.style.background = initialGray;

    legend1.innerHTML = `RGB: 229, 229, 229<br>HEX: ${initialGray}`;
    legend2.innerHTML = `RGB: 229, 229, 229<br>HEX: ${initialGray}`;
  });
  // ✅ 감정 → 색상 매핑
  const emotionColors = {
    reset: "#e5e5e5",
  };

  function applyEmotionResult(result) {
    const { emotions, startColor, endColor } = result;

    const text = `${emotions[0]}, ${emotions[1]}, and ${emotions[2]}`;
    revealingValue.textContent = text;

    // ⭐ 핵심 추가 (wipe 방식 유지)
    gradientFill.style.transition = "none";
    gradientFill.style.transform = "translateX(-100%)";

    gradientFill.style.background = `linear-gradient(90deg,
    ${startColor.rgb} 0%,
    ${startColor.rgb} 60%,
    ${endColor.rgb} 60%,
    ${endColor.rgb} 100%
  )`;

    gradientBox.style.background = `linear-gradient(90deg, ${startColor.rgb}, ${endColor.rgb})`;

    swatch1.style.background = startColor.rgb;
    swatch2.style.background = endColor.rgb;

    // legend1.innerHTML = `RGB: 158, 193, 230<br>HEX: ${startColor}`;
    // legend2.innerHTML = `RGB: 103, 152, 124<br>HEX: ${endColor}`;
    legend1.innerHTML = `
      RGB: ${startColor.rgb}<br>
      HEX: ${startColor.hex}
    `;

    legend2.innerHTML = `
      RGB: ${endColor.rgb}<br>
      HEX: ${endColor.hex}
    `;

    analyzingEl.classList.remove("visible");
  }

  // ✅ 초기 상태
  gradientBox.style.background = `linear-gradient(90deg, ${emotionColors["reset"]}, ${emotionColors["reset"]})`;
  swatch1.style.background = emotionColors["reset"];
  swatch2.style.background = emotionColors["reset"];
  legend1.innerHTML = `RGB: 229, 229, 229<br>HEX: #e5e5e5`;
  legend2.innerHTML = `RGB: 229, 229, 229<br>HEX: #e5e5e5`;

  function analyzeText(text, poet) {
    // ✅ 지정된 문장이 아니면 반응 안 함
    if (text !== TARGET_SENTENCE) {
      alert("This prototype responds only to the provided poem text.");

      return null;
    }

    // ✅ 시인별 팔레트 가져오기
    const poetPalettes = PALETTES[poet];

    // ✅ 랜덤 선택
    const selected =
      poetPalettes[Math.floor(Math.random() * poetPalettes.length)];

    return {
      emotions: selected.emotions,

      startColor: { rgb: selected.primary.rgb, hex: selected.primary.hex },

      endColor: { rgb: selected.secondary.rgb, hex: selected.secondary.hex },
    };
  }
})();
