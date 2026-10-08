# Working environment

Three ways to run the labs. Pick one and keep it for the whole course.

| Option | When to choose it | Requirements |
|--------|-------------------|--------------|
| **A. Google Colab** | No installation, free GPU for Lab 5. Recommended if your laptop is slow or has less than 8 GB of RAM. | Google account |
| **B. GitHub Codespaces** | Full VS Code in the browser, environment pre-configured by `.devcontainer/`. Free tier: 60 hours/month with 2 cores. | GitHub account |
| **C. Local VS Code + uv** | You want to work offline and keep everything on your machine. | Python 3.11+, 5 GB of disk, 8 GB of RAM |

In all cases you also need:

- a **GitHub account** and one public repository for your submissions (see [Submissions](#submissions)),
- a **Hugging Face account** with an access token (https://huggingface.co/settings/tokens), used in Lab 5,
- for Lab 5 only, a **Mistral AI** account with an API key (https://console.mistral.ai/, free "Experiment" plan).

---

## A. Google Colab

1. Open the notebook from GitHub: `File > Open notebook > GitHub`, paste `ababacaryoro/nlp-course` and select the lab. Each notebook also has an *Open in Colab* badge at the top.
2. Run the first code cell of the notebook. It installs the few libraries that Colab does not ship:

   ```python
   !pip install -q -r https://raw.githubusercontent.com/ababacaryoro/nlp-course/main/requirements.txt
   ```

3. Save a copy in your Google Drive (`File > Save a copy in Drive`) so that your work is kept.
4. To submit, download the notebook (`File > Download > .ipynb`) and commit it in your GitHub repository, or use `File > Save a copy in GitHub` directly.

Notes:
- The runtime is reset after a few hours of inactivity: re-run the install cell.
- Lab 5 benefits from a GPU: `Runtime > Change runtime type > T4 GPU`.
- Data files shipped with a lab (for example `lab4/data/NikeProductDescriptions.csv`) are downloaded automatically by the notebook when they are missing.

---

## B. GitHub Codespaces

1. Fork `https://github.com/ababacaryoro/nlp-course` to your account (button *Fork*).
2. On your fork, click `Code > Codespaces > Create codespace on main`.
3. Wait for the container to build (about 3 minutes the first time). The `postCreateCommand` installs everything with `uv` and downloads the NLTK data.
4. Open a notebook, click *Select Kernel* and choose `.venv/bin/python`.
5. Commit and push from the *Source Control* panel. Your fork is your submission repository.

Notes:
- Stop the codespace when you are done (`Codespaces > Stop`) to save your free hours.
- Model downloads (GloVe, sentence-transformers, BERT NER) are cached inside the codespace; they are lost if the codespace is deleted, not if it is stopped.

---

## C. Local installation with uv

`uv` manages the Python version, the virtual environment and the dependencies from `pyproject.toml`.

### 1. Install uv

macOS / Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Close and reopen the terminal, then check: `uv --version`.

### 2. Get the course material

```bash
git clone https://github.com/ababacaryoro/nlp-course.git
cd nlp-course
```

### 3. Create the environment

```bash
uv sync
```

This command downloads Python 3.11 if needed, creates `.venv/` and installs every library listed in `pyproject.toml` with the exact versions of `uv.lock` (about 1.5 GB, mostly PyTorch; the CPU build of PyTorch is installed on every platform). Run it again after a `git pull` if `pyproject.toml` changed.

Windows notes:
- Use PowerShell or Windows Terminal (not the old `cmd`). If PowerShell refuses to run scripts, the install command above already bypasses the execution policy for that command only.
- No activation is needed: `uv run ...` always uses `.venv`. To activate anyway: `.venv\Scripts\activate`.
- If `git clone` or `uv sync` fails with a message about long file names, enable long paths once (PowerShell as administrator): `git config --system core.longpaths true` and `New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force`.
- Antivirus software can make the first `uv sync` slow (several thousand files are written). Wait for it to finish rather than restarting it.

### 4. Download the NLTK data once

```bash
uv run python -m nltk.downloader punkt punkt_tab stopwords wordnet
```

### 5. Use the environment in VS Code

1. Install the extensions *Python* and *Jupyter* (Microsoft).
2. Open the `nlp-course` folder in VS Code.
3. Open a notebook, click *Select Kernel* (top right) and pick the interpreter located in `.venv` (`.venv/bin/python` on macOS/Linux, `.venv\Scripts\python.exe` on Windows).

To run a script instead of a notebook: `uv run python my_script.py`.

### Troubleshooting

| Symptom | Fix |
|---------|-----|
| `uv: command not found` after installation | Reopen the terminal, or add `~/.local/bin` (macOS/Linux) / `%USERPROFILE%\.local\bin` (Windows) to the PATH. |
| `OSError: [E050] Can't find model 'en_core_web_sm'` | The spaCy model is part of `uv sync`. If it is still missing: `uv run python -m spacy download en_core_web_sm`. |
| `LookupError: Resource punkt_tab not found` | Run step 4. |
| A notebook cannot load a Hugging Face dataset (no network, proxy) | Every lab has a local fallback in its `data/` folder; the notebook switches to it automatically and prints a message. |
| PyTorch on an Intel Mac | The last PyTorch release for Intel macOS is 2.2.2; `pyproject.toml` already pins it with NumPy 1.x on that platform. Prefer Colab for Lab 5 if training is slow. |
| `uv sync` fails on `pyarrow` on macOS | Make sure Python comes from uv (`uv python install 3.11`, then delete `.venv/` and run `uv sync` again). Python builds from Anaconda report an old macOS version and refuse recent wheels. |
| Windows: `error: Failed to build ...` during `uv sync` | Every library of the course has a pre-built Windows package; a build error means a wrong Python (32-bit, or a Microsoft Store Python). Delete `.venv/`, run `uv python install 3.11` then `uv sync` again. |
| Windows: `UnicodeDecodeError` when opening a text file | Add `encoding="utf-8"` to `open(...)`. The course notebooks already do it. |

---

## Submissions

1. Create **one public GitHub repository** for the whole course, named `nlp-course-LASTNAME` (for example `nlp-course-DUPONT`). Keep the same folder names as the course repository: `lab1/`, `lab2/`, `lab3/`, `lab4/`, `lab5/`, `assignments/`, `capstone/`.
2. After each lab or assignment, commit the completed notebook **with its outputs** (run all cells first: `Kernel > Restart & Run All`) and push.
3. Send an e-mail to the teacher to say that the work is ready. Put the link to your repository in the **first** e-mail only; later e-mails only need the name of the lab.
4. Grading uses the content of the repository at the deadline. A notebook that does not run from top to bottom loses points.
