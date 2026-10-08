# Application skeletons

Three small Gradio applications to start from. Each one is a single file, runs locally with the course environment (`uv sync`), and can be published for free on Hugging Face Spaces (`gradio deploy` from the app folder, or upload `app.py` + a `requirements.txt`).

| Folder | What it does | Typical topics |
|--------|--------------|----------------|
| `text_classifier_app/` | Trains TF-IDF + logistic regression on a CSV (`text,label`) and serves predictions with the most influential words | sentiment, spam/scam detection, news categories, ticket routing |
| `semantic_search_app/` | Encodes a CSV of documents with a sentence-transformer and answers natural-language queries | job offers, FAQ pages, product catalogue, articles |
| `llm_assistant_app/` | Chat with an LLM API, optionally grounded on your documents (retrieval-augmented generation) | administrative assistant, study helper, customer support |

Run an app:

```bash
cd capstone/skeletons/text_classifier_app
uv run python app.py --data path/to/data.csv
```

`--share` creates a temporary public link (useful from Colab). The apps are starting points: change the model, the features, the interface, add evaluation and error analysis. A capstone is not graded on the skeleton but on what was built on top of it.
