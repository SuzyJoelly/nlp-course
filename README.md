# Natural Language Processing & LLMs – course material

Hands-on course (24 hours) on natural language processing, from text preprocessing to large language models. Each part of the course comes with a lab notebook to complete, and the course ends with a capstone project built in teams.

## Outline

| Part | Topic | Lab |
|------|-------|-----|
| 1 | Introduction, use cases, environment | – |
| 2 | Text preprocessing: strings, regular expressions, tokenization, stemming, lemmatization, stop words | [Lab 1](lab1/lab1_text_manipulation.ipynb), [Lab 2](lab2/lab2_preprocessing_pipeline.ipynb), [Assignment 1](assignments/1/) |
| 3 | Text representation: visualization, Bag of Words, TF-IDF, n-grams, Word2Vec, GloVe, BERT embeddings | [Lab 3.1](lab3/lab3_1_text_visualization_classical.ipynb), [Lab 3.2](lab3/lab3_2_word_embeddings.ipynb) |
| 4 | Core NLP tasks: POS tagging, NER, similarity, classification, sentiment analysis, topic modeling | [Lab 4.1](lab4/lab4_1_core_nlp_tasks.ipynb), [Lab 4.2](lab4/lab4_2_classification_sentiment_topics.ipynb) |
| 5 | Deep learning and LLMs: RNN, LSTM, GRU, transformers, prompting, RAG | [Lab 5](lab5/lab5_deep_learning_llms.ipynb) |
| 6 | Capstone project | [Capstone](capstone/) |

Every notebook has an *Open in Colab* badge. Datasets come from Hugging Face or public APIs; a local copy of each dataset is shipped in the `data/` folder of the lab and is used automatically when the download fails.

## Getting started

Read [SETUP.md](SETUP.md): it describes the three ways to work (Google Colab, GitHub Codespaces, local installation with `uv`), the accounts needed (GitHub, Hugging Face, Mistral AI for Lab 5) and the submission rules.

Short version for a local installation:

```bash
git clone https://github.com/ababacaryoro/nlp-course.git
cd nlp-course
uv sync
uv run python -m nltk.downloader punkt punkt_tab stopwords wordnet
```

## Repository layout

```
lab1/ ... lab5/        notebooks and data/ folders of the labs
assignments/1/         Assignment 1 (regular expressions, NLTK) and its data
capstone/              project brief, topics and application skeletons
SETUP.md               environment setup and submission rules
pyproject.toml         dependencies (uv); requirements.txt is the equivalent for pip / Colab
```

## Evaluation

- Labs: completed notebooks pushed to the student's repository after each session.
- Assignment 1: after Part 2.
- Capstone project: team presentation on the last day.
- Written exam.

## Submissions

One public GitHub repository per student, named `nlp-course-LASTNAME`, with the same folder names as this repository. After each lab: run all cells, commit the notebook with its outputs, push, and notify the teacher by e-mail (the repository link is only needed in the first e-mail).
