# KPoEM Interface

KPoEM Interface is a web-based environment designed for the visual exploration of Korean poetic texts. It uses the **KPoEM (Korean Poetry Emotion Dataset)** and its associated emotion-classification model to present emotion analysis through multiple forms of visualization.

By combining computational emotion analysis with visual representation, the project allows readers to explore literary works from several perspectives. The interface consists of three primary modules: **Close Reading**, **Distant Reading**, and **Co-Reading**.

- **Close Reading** supports the exploration of emotion-analysis results in individual poems and their lines.
- **Distant Reading** visualizes emotional distributions and patterns across poets and their collected works.
- **Co-Reading (Lim, 2026, forthcoming)** is an experimental environment in which humans and artificial intelligence read and interpret literary works together. It translates emotion-analysis results into colors and other visual elements.

For more information about Co-Reading and its source code, visit the [Co-Reading repository](https://github.com/poet-developer/Co-Reading).

> **Note**
>
> KPoEM Interface is a static web prototype developed to support the arguments and conceptual validation of a doctoral dissertation. It is not intended as a production service or as a fully implemented user-interaction system. The current version demonstrates the potential of the reading methods and visualization methodology proposed by the research.

## Project Structure

### `backend/`

Contains the code used to perform emotion analysis and generate visualization outputs.

- `shap/`
  - Stores SHAP-based analyses of influential words.
- `KPoEM_heatmap.ipynb`
  - Generates emotion heatmaps.
- `KPoEM_wordcloud.ipynb`
  - Generates emotion-based word clouds.
- `poet_emotion_distribution.ipynb`
  - Analyzes emotion distributions by poet.
- `poet_SHAP_batched_run.ipynb`
  - Performs batched SHAP analysis.

### `frontend/`

Contains the web interface through which users explore the emotion-analysis results.

- `close_reading/`
  - Provides bilingual, line-level exploration of individual poems and their emotion annotations.
- `distant_reading/`
  - Presents broader emotional tendencies across a poet's works.
- `co_reading/`
  - Provides the Co-Reading interface for reading poetry with AI.
  - Displays a selected poem in full.
  - Translates emotion-analysis results into color gradients and visual legends.
- `source/`
  - Stores generated HTML files used for distant-reading visualizations.
- `styles/`
  - Contains the CSS stylesheets for the interface.
- `js/`
  - Contains JavaScript for interface behavior and interaction.
- `img/`
  - Stores generated word-cloud images.

## Features

### Close Reading

- Explore emotion-analysis results for individual poems.
- Inspect line-level emotion annotations and primary emotions.
- Read English translations alongside the original Korean text.

### Distant Reading

- Visualize emotion distributions by poet and literary work.
- Explore emotional patterns through emotion heatmaps.
- Examine emotion-related vocabulary using SHAP word clouds.

### Co-Reading

- Read literary works through a collaborative human–AI interface.
- Transform emotion-analysis results into color visualizations.
- Explore literary interpretation and AI-generated analysis together.

### Emotion Visualization

- Emotion heatmaps
- Emotion-distribution visualizations
- Emotion–color mapping
- Color gradients and visual legends

### Explainable AI

- SHAP-based analysis of influential words
- Word-cloud visualizations of emotion-related vocabulary

### Interactive Exploration

- Web-based exploration of poets, literary works, and emotions
- Integration of multiple reading methods within a digital-humanities environment

## Featured Poets

- Han Yong-un (한용운)
- Kim Sowol (김소월)
- Yi Sang (이상)
- Im Hwa (임화)
- Yun Dong-ju (윤동주)

## Objective

KPoEM Interface aims to provide a digital-humanities research environment for reading and exploring modern Korean poetry in new ways through emotion datasets and artificial-intelligence analysis.

## Resources

### 📖 KPoEM Dataset

**Contributors:** IRO LIM · Ji Haein · Koo Sul · Jung Song-yi · Yun Jonghoon · Byungjun Kim

- [Zenodo](https://zenodo.org/records/15598092)
- [Hugging Face](https://huggingface.co/datasets/AKS-DHLAB/KPoEM)

### 🤖 KPoEM Emotion Classification Model

**Contributors:** IRO LIM · Ji Haein · Byungjun Kim

- [Hugging Face](https://huggingface.co/AKS-DHLAB/KPoEM)

> The KPoEM dataset and emotion-classification model were developed through collaborative research. For further details, see the following publication:
>
> Lim, I., Ji, H., & Kim, B. (2026). KPoEM: A human-annotated dataset for emotion classification and RAG-based poetry generation in Korean modern poetry. *The Review of Korean Studies, 29*(1), 161–206. [10.25024/review.2026.29.1.006](https://doi.org/10.25024/review.2026.29.1.006)

### 🎨 KCoEM Dataset

**Contributor:** IRO LIM

- [Zenodo](https://zenodo.org/records/19464212)

### 🌈 Co-Reading

**Contributor:** IRO LIM

- [GitHub](https://github.com/poet-developer/Co-Reading)
