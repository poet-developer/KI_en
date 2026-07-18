"""Generate English KPoEM heatmaps and emotion-distribution charts.

This script consolidates the analysis performed in KPoEM_heatmap.ipynb and
poet_emotion_distribution.ipynb and applies the English KOTE labels used by
the frontend.
"""

from collections import Counter
import json
from pathlib import Path
import shutil

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


LINE_URL = "https://huggingface.co/datasets/AKS-DHLAB/KPoEM/resolve/main/KPoEM_line_dataset_v4.tsv"
POEM_URL = "https://huggingface.co/datasets/AKS-DHLAB/KPoEM/resolve/main/KPoEM_poem_dataset_v4.tsv"
OUTPUT_DIR = Path(__file__).parent / "english_analysis_html"
TITLE_CACHE = Path(__file__).parent / "poem_title_en.json"
ANNOTATOR_COLUMNS = [f"annotator_0{i}" for i in range(1, 6)]

POETS = {
    "김소월": ("Kim Sowol", "kim_sowol"),
    "윤동주": ("Yun Dong-ju", "yun_dongju"),
    "이상": ("Yi Sang", "yi_sang"),
    "임화": ("Im Hwa", "im_hwa"),
    "한용운": ("Han Yong-un", "han_yongun"),
}
SOURCE_DIRS = {
    "kim_sowol": ("kim", "heatmap_kim.html"),
    "yun_dongju": ("yun", "heatmap_yun.html"),
    "yi_sang": ("lee", "heatmap_lee.html"),
    "im_hwa": ("lim", "heatmap_lim.html"),
    "han_yongun": ("han", "heatmap_han.html"),
}

# The order and wording match frontend/js/wordcloud.js.
KOTE_LABELS = {
    "불평/불만": "Complaint / Dissatisfaction",
    "환영/호의": "Welcome / Favor",
    "감동/감탄": "Impressed / Admiration",
    "지긋지긋": "Fed up",
    "고마움": "Gratitude",
    "슬픔": "Sadness",
    "화남/분노": "Anger / Rage",
    "존경": "Respect",
    "기대감": "Anticipation",
    "우쭐댐/무시함": "Arrogance / Disregard",
    "안타까움/실망": "Pitifulness / Disappointment",
    "비장함": "Resolute",
    "의심/불신": "Doubt / Distrust",
    "뿌듯함": "Pride",
    "편안/쾌적": "Comfort / Cozy",
    "신기함/관심": "Curiosity / Interest",
    "아껴주는": "Caring",
    "부끄러움": "Shame",
    "공포/무서움": "Fear/Scary",
    "절망": "Despair",
    "한심함": "Pathetic ",
    "역겨움/징그러움": "Disgust / Repulsiveness",
    "짜증": "Irritation",
    "어이없음": "Preposterous ",
    "없음": "NO EMOTION",
    "패배/자기혐오": "Defeat / Self-hatred",
    "귀찮음": "Laziness",
    "힘듦/지침": "Fatigue / Exhaustion",
    "즐거움/신남": "Pleasure / Excitement",
    "깨달음": "Realization",
    "죄책감": "Guilt",
    "증오/혐오": "Loathing / Hatred",
    "흐뭇함(귀여움/예쁨)": "Pleased (Cute / Pretty)",
    "당황/난처": "Embarrassment / Awkwardness",
    "경악": "Shock",
    "부담/안_내킴": "Burden / Unwillingness",
    "서러움": "Sorrow",
    "재미없음": "Boredom",
    "불쌍함/연민": "Pity / Compassion",
    "놀람": "Surprise",
    "행복": "Happiness",
    "불안/걱정": "Anxiety / Worry",
    "기쁨": "Joy",
    "안심/신뢰": "Relief / Trust",
}


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    options = dict(sep="\t", encoding="utf-8", quoting=3)
    return pd.read_csv(LINE_URL, **options), pd.read_csv(POEM_URL, **options)


def clean_poem_title(title: object) -> str:
    """Return the individual poem title, excluding collection names."""
    value = str(title).strip()
    if "/" in value:
        value = value.rsplit("/", 1)[-1].strip()
    if value == "항전 애창 명주 딸기":
        value = "딸기"
    return value.replace("(시집)", "").strip()


def emotion_vector(value: object) -> np.ndarray:
    vector = np.zeros(len(KOTE_LABELS), dtype=float)
    if pd.isna(value):
        return vector
    index = {emotion: i for i, emotion in enumerate(KOTE_LABELS)}
    for emotion in str(value).split(","):
        emotion = emotion.strip()
        if emotion in index:
            vector[index[emotion]] = 1
    return vector


def build_heatmap(all_data: pd.DataFrame, poet_ko: str, poet_en: str) -> go.Figure:
    poet_data = all_data[all_data["poet"] == poet_ko].copy()
    for annotator in ANNOTATOR_COLUMNS:
        poet_data[f"{annotator}_vec"] = poet_data[annotator].apply(emotion_vector)

    rows = []
    for poem_id, group in poet_data.groupby("poem_id", sort=True):
        annotator_means = [
            np.stack(group[f"{annotator}_vec"].to_numpy()).mean(axis=0)
            for annotator in ANNOTATOR_COLUMNS
        ]
        rows.append((poem_id, np.stack(annotator_means).mean(axis=0)))

    title_map = (
        poet_data[["poem_id", "title"]]
        .drop_duplicates("poem_id")
        .set_index("poem_id")["title"]
        .to_dict()
    )
    poem_ids = [row[0] for row in rows]
    title_translations = json.loads(TITLE_CACHE.read_text(encoding="utf-8"))
    titles = []
    for poem_id in poem_ids:
        individual_title = clean_poem_title(title_map.get(poem_id, poem_id))
        titles.append(title_translations.get(individual_title, individual_title))
    matrix = np.stack([row[1] for row in rows], axis=1)
    english_emotions = list(KOTE_LABELS.values())
    window = 44

    def window_data(start: int) -> tuple[list[str], np.ndarray]:
        x = titles[start : start + window]
        z = matrix[:, start : start + window]
        missing = window - len(x)
        if missing > 0:
            x = x + [""] * missing
            z = np.pad(z, ((0, 0), (0, missing)), constant_values=np.nan)
        return x, z

    starts = list(range(max(1, len(titles) - window + 1)))
    initial_x, initial_z = window_data(0)
    frames = []
    for start in starts:
        frame_x, frame_z = window_data(start)
        frames.append(
            go.Frame(
                name=str(start),
                data=[go.Heatmap(z=frame_z, x=frame_x, y=english_emotions)],
            )
        )

    fig = go.Figure(
        data=[go.Heatmap(
            z=initial_z, x=initial_x, y=english_emotions,
            colorscale="Blues", zmin=0, zmax=1, xgap=0.5, ygap=0.5,
            colorbar=dict(title="Mean score"),
            hovertemplate="Poem: %{x}<br>Emotion: %{y}<br>Mean score: %{z:.3f}<extra></extra>",
        )],
        frames=frames,
    )
    fig.update_layout(
        title=dict(text=f"KPoEM — Emotion Heatmap by Work: {poet_en}", x=0.5),
        xaxis_title="Poem",
        yaxis_title="KOTE Emotion",
        width=1050,
        height=1100,
        autosize=False,
        margin=dict(l=210, r=48, t=70, b=238),
        font=dict(family="Arial, sans-serif", size=11),
        paper_bgcolor="white",
        plot_bgcolor="white",
        sliders=[dict(
            active=0,
            currentvalue=dict(prefix="Poem window: ", visible=True),
            pad=dict(t=28),
            steps=[dict(
                method="animate", label=str(start + 1),
                args=[[str(start)], dict(
                    mode="immediate",
                    frame=dict(duration=0, redraw=True),
                    transition=dict(duration=0),
                )],
            ) for start in starts],
        )],
    )
    fig.update_xaxes(tickangle=55, automargin=False, fixedrange=True)
    fig.update_yaxes(autorange="reversed", automargin=True)
    return fig


def build_distribution(all_data: pd.DataFrame, poet_ko: str, poet_en: str) -> go.Figure:
    poet_data = all_data[all_data["poet"] == poet_ko]
    counts: Counter[str] = Counter()
    for value in poet_data[ANNOTATOR_COLUMNS].to_numpy().ravel():
        if pd.isna(value):
            continue
        counts.update(item.strip() for item in str(value).split(",") if item.strip())

    distribution = pd.DataFrame(
        {
            "Emotion": list(KOTE_LABELS.values()),
            "Count": [counts[emotion] for emotion in KOTE_LABELS],
        }
    ).sort_values(["Count", "Emotion"], ascending=[False, True])

    fig = px.bar(
        distribution,
        x="Emotion",
        y="Count",
        color="Count",
        color_continuous_scale=px.colors.sequential.Plasma,
        title=f"KPoEM — Emotion Distribution: {poet_en}",
    )
    fig.update_traces(
        hovertemplate="Emotion: %{x}<br>Annotations: %{y:,}<extra></extra>"
    )
    fig.update_layout(
        xaxis_title="KOTE Emotion",
        yaxis_title="Annotation Count",
        autosize=True,
        height=540,
        margin=dict(l=65, r=35, t=75, b=155),
        font=dict(family="Arial, sans-serif", size=11),
        title=dict(x=0.5),
        coloraxis_colorbar=dict(title="Count"),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )
    fig.update_xaxes(tickangle=55, automargin=True, tickfont=dict(size=9))
    fig.update_yaxes(gridcolor="#e5e7eb", rangemode="tozero")
    return fig


def main() -> None:
    line_data, poem_data = load_data()
    all_data = pd.concat([line_data, poem_data], ignore_index=True)

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    for poet_ko, (poet_en, slug) in POETS.items():
        heatmap = build_heatmap(all_data, poet_ko, poet_en)
        distribution = build_distribution(all_data, poet_ko, poet_en)
        heatmap.write_html(
            OUTPUT_DIR / f"{slug}_emotion_heatmap.html",
            include_plotlyjs=True,
            full_html=True,
        )
        source_folder, source_name = SOURCE_DIRS[slug]
        heatmap.write_html(
            Path(__file__).parent.parent / "frontend" / "source" / source_folder / source_name,
            include_plotlyjs=True,
            full_html=True,
        )
        distribution.write_html(
            OUTPUT_DIR / f"{slug}_emotion_distribution.html",
            include_plotlyjs=True,
            full_html=True,
        )
        print(f"Generated heatmap and distribution for {poet_en}")

    outputs = sorted(OUTPUT_DIR.glob("*.html"))
    if len(outputs) != 10:
        raise RuntimeError(f"Expected 10 HTML files, generated {len(outputs)}")
    print(f"Generated {len(outputs)} HTML files in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
