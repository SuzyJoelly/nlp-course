"""Text classifier web app (TF-IDF + logistic regression + Gradio).

Train on a CSV with two columns, `text` and `label`, then serve a small web interface.

    uv run python app.py --data my_dataset.csv            # train and launch
    uv run python app.py --data my_dataset.csv --share    # public link (Colab / demo)

Replace the model by anything that has fit/predict/predict_proba (a sentence-transformer + logistic
regression, a fine-tuned transformer...) and the interface keeps working.
"""
import argparse
import pandas as pd
import gradio as gr
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report


def train(csv_path):
    df = pd.read_csv(csv_path).dropna(subset=["text", "label"])
    X_train, X_test, y_train, y_test = train_test_split(df["text"], df["label"], test_size=0.2, random_state=42, stratify=df["label"])
    model = make_pipeline(TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True), LogisticRegression(max_iter=1000))
    model.fit(X_train, y_train)
    print(classification_report(y_test, model.predict(X_test)))
    return model


def build_interface(model):
    classes = list(model.classes_)
    vectorizer, clf = model.steps[0][1], model.steps[-1][1]

    def predict(text):
        probs = model.predict_proba([text])[0]
        scores = {str(c): float(p) for c, p in zip(classes, probs)}
        # words that pushed the decision (works for linear models on TF-IDF features)
        explanation = ""
        if hasattr(clf, "coef_"):
            x = vectorizer.transform([text])
            idx = probs.argmax() if len(classes) > 2 else 0
            contrib = x.toarray()[0] * clf.coef_[idx]
            top = contrib.argsort()[::-1][:8]
            names = vectorizer.get_feature_names_out()
            explanation = ", ".join(f"{names[i]} ({contrib[i]:+.2f})" for i in top if contrib[i] != 0)
        return scores, explanation

    return gr.Interface(
        fn=predict,
        inputs=gr.Textbox(lines=5, label="Text"),
        outputs=[gr.Label(num_top_classes=5, label="Prediction"), gr.Textbox(label="Most influential words")],
        title="Text classifier",
        description="Type or paste a text; the model returns the probability of each class.",
        examples=[["This product stopped working after two days, very disappointed."], ["Great value, fast delivery, I would buy again."]],
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="CSV file with columns text,label")
    parser.add_argument("--share", action="store_true", help="create a public link")
    args = parser.parse_args()
    build_interface(train(args.data)).launch(share=args.share)
