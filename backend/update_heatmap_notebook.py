"""Update KPoEM_heatmap.ipynb to generate five English source heatmaps."""

import json
from pathlib import Path


path = Path(__file__).with_name("KPoEM_heatmap.ipynb")
notebook = json.loads(path.read_text(encoding="utf-8"))
code = '''# Generate five English heatmaps with translated poem titles and square cells
from pathlib import Path
import sys

repo_root = Path.cwd()
if repo_root.name == "backend":
    backend_dir = repo_root
else:
    backend_dir = repo_root / "backend"
sys.path.insert(0, str(backend_dir))

from generate_english_analysis import build_heatmap, POETS, SOURCE_DIRS

output_dir = backend_dir / "english_analysis_html"
output_dir.mkdir(parents=True, exist_ok=True)

for poet_ko, (poet_en, slug) in POETS.items():
    fig = build_heatmap(df_all, poet_ko, poet_en)
    standalone = output_dir / f"{slug}_emotion_heatmap.html"
    source_folder, source_name = SOURCE_DIRS[slug]
    source = repo_root / "frontend" / "source" / source_folder / source_name
    if repo_root.name == "backend":
        source = repo_root.parent / "frontend" / "source" / source_folder / source_name
    fig.write_html(standalone, include_plotlyjs=True, full_html=True)
    fig.write_html(source, include_plotlyjs=True, full_html=True)
    print(f"Saved {poet_en}: {standalone} and {source}")
'''

# Preserve the package/import and two dataset-loading cells through df_all.
notebook["cells"] = notebook["cells"][:6] + [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": ["## English heatmaps for five poets\n", "\n", "Poem titles and KOTE labels are displayed in English. Each 44 × 44 window preserves square heatmap cells.\n"],
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": code.splitlines(keepends=True),
    },
]
path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(f"Updated {path}")
