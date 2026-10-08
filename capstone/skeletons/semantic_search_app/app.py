"""Semantic search web app (sentence embeddings + cosine similarity + Gradio).

Index a CSV of documents (column `text`, optional `title`), then search it with natural-language queries.

    uv run python app.py --data documents.csv [--column text] [--share]

Ideas: job offers, administrative FAQ pages, product catalogue, course notes, news articles.
Swap the model for a multilingual one ("paraphrase-multilingual-MiniLM-L12-v2") for non-English documents.
"""
import argparse
import numpy as np
import pandas as pd
import gradio as gr
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"


class SearchEngine:
    def __init__(self, df, column):
        self.df = df.reset_index(drop=True)
        self.column = column
        self.model = SentenceTransformer(MODEL_NAME)
        print(f"Encoding {len(df)} documents...")
        self.embeddings = self.model.encode(self.df[column].astype(str).tolist(), normalize_embeddings=True, show_progress_bar=True)

    def search(self, query, k=5):
        q = self.model.encode([query], normalize_embeddings=True)[0]
        scores = self.embeddings @ q                      # cosine similarity (vectors are normalized)
        top = np.argsort(scores)[::-1][:k]
        rows = self.df.iloc[top].copy()
        rows.insert(0, "score", scores[top].round(3))
        return rows


def build_interface(engine):
    def run(query, k):
        res = engine.search(query, int(k))
        cols = ["score"] + [c for c in ("title", engine.column) if c in res.columns]
        res[engine.column] = res[engine.column].astype(str).str[:300]
        return res[cols]

    return gr.Interface(
        fn=run,
        inputs=[gr.Textbox(label="Query"), gr.Slider(1, 20, value=5, step=1, label="Number of results")],
        outputs=gr.Dataframe(label="Results"),
        title="Semantic search",
        description="Results are ranked by the similarity of their embedding with the query, not by shared keywords.",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--column", default="text")
    parser.add_argument("--share", action="store_true")
    args = parser.parse_args()
    df = pd.read_csv(args.data).dropna(subset=[args.column])
    build_interface(SearchEngine(df, args.column)).launch(share=args.share)
