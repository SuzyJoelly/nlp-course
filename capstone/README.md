# Capstone project

The capstone is the last part of the course. Teams of 2 or 3 build a **working application** on **real data** with the techniques seen in the labs, and present it on the last day.

## Deliverables

1. **A public GitHub repository** (one per team, named `nlp-capstone-<team>`), with:
   - `README.md`: problem, data source, pipeline, results, how to run the app, who did what;
   - the code (notebooks for exploration and evaluation, a Python app for the demo);
   - no data file above 50 MB and no API key (keys go in environment variables).
2. **A running application** with a web interface (Gradio or Streamlit), launched locally during the presentation or published on Hugging Face Spaces.
3. **A 10-minute presentation** (8 minutes + questions): the problem and who it is for, the data, the pipeline and the choices made, the results with their limits, a live demo.

## Rules

- Real data only: a public dataset, a public API, or data collected by the team (scraping within the terms of the site). Synthetic or toy data is not accepted.
- At least one **evaluation**: a held-out test set with a metric, or a comparison between two approaches (for example TF-IDF + linear model vs sentence embeddings, or a small model vs an LLM).
- AI assistants (ChatGPT, Copilot, Claude...) may be used. Every member must be able to explain and modify any part of the project; questions during the presentation are asked to each member individually.
- Teams and topics are declared before the end of the Part 4 session (one e-mail per team to the teacher: team members, topic, data source, repository link).

## Grading (/20)

| Criterion | Points | What is assessed |
|-----------|--------|------------------|
| Problem and data | 4 | Clear use case and users; real data, understood and explored (size, quality, biases) |
| NLP pipeline | 6 | Preprocessing adapted to the data, sensible choice of representation and model, evaluation with a metric, error analysis |
| Working application | 5 | Runs during the demo, usable interface, handles unexpected input |
| Presentation and understanding | 5 | Clear story in 8 minutes, honest about limits, every member answers questions about the code |

## Suggested topics

Each topic names a real data source that has been checked. Teams may combine topics or propose their own (see *Free topic*).

| # | Topic | Data | Suggested pipeline | Skeleton |
|---|-------|------|--------------------|----------|
| 1 | **Job market explorer** – search job offers in natural language and see the skills in demand for a role | [lukebarousse/data_jobs](https://huggingface.co/datasets/lukebarousse/data_jobs) (785k data-related job postings, 2023) or [jacob-hugging-face/job-descriptions](https://huggingface.co/datasets/jacob-hugging-face/job-descriptions) | sentence embeddings + semantic search; NER / keyword extraction of skills; topic modeling by role | `semantic_search_app` |
| 2 | **Resume matcher** – upload a resume, get the closest job offers and the missing skills | [ahmedheakl/resume-atlas](https://huggingface.co/datasets/ahmedheakl/resume-atlas) (13k resumes with categories) + job postings of topic 1 | resume classification (TF-IDF or embeddings), similarity resume ↔ offers, skill gap extraction with an LLM | `semantic_search_app`, `text_classifier_app` |
| 3 | **Administrative assistant for newcomers in France** – answer questions about visas, residence permits, housing, health insurance | the public pages of [service-public.fr](https://www.service-public.fr/) (official dump on [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/?q=service-public.fr+fiches), XML) or pages collected by the team | chunking, multilingual embeddings, retrieval-augmented generation with sources; evaluation on 30 questions written by the team | `llm_assistant_app` |
| 4 | **Scam SMS and phishing detector** – flag fraudulent messages (parcel delivery, bank, tax scams) | [ucirvine/sms_spam](https://huggingface.co/datasets/ucirvine/sms_spam) (5.5k SMS) + messages collected by the team in French or other languages | classification with character n-grams, comparison with an LLM zero-shot, explanation of the decision | `text_classifier_app` |
| 5 | **Multilingual sentiment monitor** – track opinions in several languages (Arabic, French, Hindi, Portuguese, Spanish...) | [mteb/tweet_sentiment_multilingual](https://huggingface.co/datasets/mteb/tweet_sentiment_multilingual) (8 languages) or [SetFit/amazon_reviews_multi_fr](https://huggingface.co/datasets/SetFit/amazon_reviews_multi_fr) (French reviews) | per-language classifiers vs one multilingual embedding model; dashboard of sentiment by language or product | `text_classifier_app` |
| 6 | **African news classifier** – classify and search news in Hausa, Swahili, Yoruba, Igbo, Amharic... | [masakhane/masakhanews](https://huggingface.co/datasets/masakhane/masakhanews) (16 African languages, 7 categories) | TF-IDF vs multilingual embeddings on low-resource languages; semantic search across languages | `text_classifier_app`, `semantic_search_app` |
| 7 | **Fake news detector** | [GonzaloA/fake_news](https://huggingface.co/datasets/GonzaloA/fake_news) (40k articles) | classification, analysis of the most predictive words, test on recent articles collected by the team | `text_classifier_app` |
| 8 | **App review analyzer** – what users complain about in an app they use (transport, banking, delivery, learning apps) | reviews collected with the `google-play-scraper` package (public Google Play reviews, any app, any language) | sentiment + topic modeling over time, summary of the main complaints with an LLM | `text_classifier_app`, `llm_assistant_app` |
| 9 | **Topic explorer for your language** – what Wikipedia or the news talk about in a given language | [wikimedia/wikipedia](https://huggingface.co/datasets/wikimedia/wikipedia) (one configuration per language, e.g. `20231101.ar`, `20231101.hi`, `20231101.sw`) | tokenization and preprocessing for a non-English language, topic modeling, embedding visualization | `semantic_search_app` |
| 10 | **Free topic** – any use case with real data and a working application | to be validated by the teacher | | |

## Skeletons

`skeletons/` contains three single-file Gradio applications (text classifier, semantic search, LLM assistant with retrieval). See [skeletons/README.md](skeletons/README.md). They run with the course environment and can be published on Hugging Face Spaces for free.

## Timeline

| When | Milestone |
|------|-----------|
| End of Part 4 | Team, topic, data source and repository declared by e-mail |
| Part 5 session | Checkpoint: data loaded and explored, first baseline model, interface started |
| Last day | Presentations and demos |
