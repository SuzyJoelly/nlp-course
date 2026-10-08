"""Assistant web app: LLM chat with optional retrieval over your own documents (RAG) + Gradio.

    export MISTRAL_API_KEY=...            # or HF_TOKEN with --provider huggingface
    uv run python app.py --data faq.csv --column text [--share]

Without --data, the app is a plain chat. With --data, the k most similar documents are added to the prompt
and the answer must rely on them (the sources are shown).
"""
import argparse, os, time
import numpy as np
import pandas as pd
import requests
import gradio as gr

SYSTEM = ("You are a helpful assistant. Answer in the language of the question. "
          "When context documents are provided, base your answer on them and say when they do not contain the answer.")


def call_llm(messages, provider="mistral", max_tokens=400):
    if provider == "mistral":
        url, model, key = "https://api.mistral.ai/v1/chat/completions", "mistral-small-latest", os.environ.get("MISTRAL_API_KEY", "")
    else:
        url, model, key = "https://router.huggingface.co/v1/chat/completions", "Qwen/Qwen2.5-7B-Instruct", os.environ.get("HF_TOKEN", "")
    if not key:
        return "No API key found in the environment (MISTRAL_API_KEY or HF_TOKEN)."
    for attempt in range(5):
        r = requests.post(url, headers={"Authorization": f"Bearer {key}"}, timeout=60,
                          json={"model": model, "messages": messages, "max_tokens": max_tokens, "temperature": 0.2})
        if r.status_code == 429:
            time.sleep(2 * (attempt + 1)); continue
        if r.status_code != 200:
            return f"Error {r.status_code}: {r.text[:200]}"
        return r.json()["choices"][0]["message"]["content"]
    return "Rate limit reached, try again in a few seconds."


class Retriever:
    def __init__(self, df, column):
        from sentence_transformers import SentenceTransformer
        self.df, self.column = df.reset_index(drop=True), column
        self.model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
        self.emb = self.model.encode(self.df[column].astype(str).tolist(), normalize_embeddings=True, show_progress_bar=True)

    def top(self, query, k=4):
        q = self.model.encode([query], normalize_embeddings=True)[0]
        idx = np.argsort(self.emb @ q)[::-1][:k]
        return self.df.iloc[idx][self.column].astype(str).str[:1200].tolist()


def build_interface(retriever, provider):
    def respond(message, history):
        messages = [{"role": "system", "content": SYSTEM}]
        for turn in history[-6:]:
            messages.append({"role": turn["role"], "content": turn["content"]})
        sources = retriever.top(message) if retriever else []
        if sources:
            context = "\n\n".join(f"[{i + 1}] {s}" for i, s in enumerate(sources))
            messages.append({"role": "user", "content": f"Context documents:\n{context}\n\nQuestion: {message}"})
        else:
            messages.append({"role": "user", "content": message})
        answer = call_llm(messages, provider)
        if sources:
            answer += "\n\n---\nSources: " + " | ".join(f"[{i + 1}] {s[:80]}..." for i, s in enumerate(sources))
        return answer

    return gr.ChatInterface(respond, title="Assistant", description="LLM chat" + (" with retrieval over your documents" if retriever else ""))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", help="CSV of documents to search (optional)")
    parser.add_argument("--column", default="text")
    parser.add_argument("--provider", default="mistral", choices=["mistral", "huggingface"])
    parser.add_argument("--share", action="store_true")
    args = parser.parse_args()
    retriever = Retriever(pd.read_csv(args.data).dropna(subset=[args.column]), args.column) if args.data else None
    build_interface(retriever, args.provider).launch(share=args.share)
