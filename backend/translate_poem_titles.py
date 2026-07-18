"""Build the English poem-title cache used by KPoEM heatmaps."""

import json
from pathlib import Path
import time

import pandas as pd
import requests


URL = "https://huggingface.co/datasets/AKS-DHLAB/KPoEM/resolve/main/KPoEM_poem_dataset_v4.tsv"
OUTPUT = Path(__file__).with_name("poem_title_en.json")
POETS = ["김소월", "윤동주", "이상", "임화", "한용운"]
OVERRIDES = {
    "진달래꽃": "Azaleas", "서시": "Prologue", "꽃나무": "Flowering Tree",
    "산유화": "Mountain Flowers", "엄마야 누나야": "Mother, Sister",
    "새로운 길": "A New Road", "현해탄": "The Korea Strait",
    "나룻배와 행인": "The Ferryboat and the Traveler",
    "알 수 없어요": "I Do Not Know", "밤은 고요하고": "The Night Is Still",
    "봄비": "Spring Rain", "못 잊어": "Cannot Forget",
    "가갸날": "Hangul Day", "딸기": "Strawberry",
}


def translate_batch(titles: list[str]) -> list[str]:
    response = requests.get(
        "https://translate.googleapis.com/translate_a/single",
        params={"client": "gtx", "sl": "ko", "tl": "en", "dt": "t", "q": "\n".join(titles)},
        timeout=60,
    )
    response.raise_for_status()
    translated = "".join(part[0] for part in response.json()[0]).splitlines()
    if len(translated) != len(titles):
        raise RuntimeError(f"Translation count mismatch: {len(titles)} titles, {len(translated)} results")
    return [text.strip() for text in translated]


def main() -> None:
    data = pd.read_csv(URL, sep="\t", encoding="utf-8", quoting=3)
    titles = sorted({str(x).strip() for x in data[data["poet"].isin(POETS)]["title"].dropna()})
    cache = json.loads(OUTPUT.read_text(encoding="utf-8")) if OUTPUT.exists() else {}
    pending = [title for title in titles if title not in cache]
    for start in range(0, len(pending), 30):
        batch = pending[start : start + 30]
        for source, target in zip(batch, translate_batch(batch)):
            cache[source] = target
        OUTPUT.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Translated {min(start + 30, len(pending))}/{len(pending)} pending titles")
        time.sleep(0.25)
    cache.update(OVERRIDES)
    OUTPUT.write_text(json.dumps(dict(sorted(cache.items())), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Saved {len(cache)} English titles to {OUTPUT}")


if __name__ == "__main__":
    main()
