# 🚀 AI Web Summarizer: AI-Powered Text Summarization Pipeline
[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Type Checking](https://img.shields.io/badge/Mypy-Strict-informational.svg)](http://mypy-lang.org/)
[![Test Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen.svg)](https://damiankowalczykdk.github.io/ai-web-summarizer/docs/index.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📖 Overview
**Web Page Summarizer** is a Python-based automation pipeline that extracts text from web pages and generates structured summaries using Large Language Models (LLMs).  

The system eliminates manual summarization by combining web scraping, prompt-based AI text analysis, and flexible output formatting. Users can generate summaries in multiple languages and export them in different formats (TXT, JSON, CSV, YAML, HTML).  

---

## 🎯 Key Features
- **Automated Web Scraping:** Fetches and cleans text content from web pages, removing scripts, styles, navigation, and other non-essential elements.  
- **AI Summarization:** Multi-step summarization pipeline with modular LLM clients for analysis, formatting, and serialization.  
- **Flexible Output:** Save summaries in various formats with a single function call.  
- **Prompt Customization:** YAML-based prompt templates allow users to define system instructions and user messages.  
- **CLI Interface:** Easy command-line interface to summarize pages with custom parameters.  

---

## 🏗️ Architecture & Data Flow
The pipeline follows a modular, service-oriented design:  

1. **Scraper:** `fetch_page_text` extracts clean text from web pages, removing scripts, styles, navigation, and other non-content elements.  
2. **LLM Pipeline:** `SummaryService` orchestrates analysis, formatting, and serialization using multiple LLM clients (OpenAI or Ollama).  
3. **Prompt System:** Prompts are loaded from YAML and dynamically filled with:
   - **Page content** (`text`)  
   - **`count`** → the number of main points the summary will include.  
   - **`language`** → target language for all outputs.  
4. **Output Writer:** `FormatterWriterService` saves the final summary in the desired format (TXT, JSON, CSV, YAML, HTML, ...).  

---

## ✨ Technical Highlights & Best Practices

### ⚡ Performance & Text Processing
- **HTML Cleaning:** Uses BeautifulSoup to remove non-content tags efficiently.  
- **Memory Efficient:** Handles large pages without excessive memory usage.  

### 🛡️ Code Quality & Reliability
- **Unit Tested:** Core services and utilities covered with 100% test coverage.  
- **Static Typing:** Strict type checking with `mypy` ensures type safety.  

### ⚙️ AI Integration
- **OpenAI Client:** Easy integration with OpenAI Chat API for LLM generation.  
- **Ollama Client:** Optional local LLM endpoint support.  
- **Modular Design:** Supports swapping AI providers without changing pipeline logic.  

---

## 💻 Tech Stack
- **Language:** Python 3.13  
- **Web Scraping:** `httpx`, `BeautifulSoup4`  
- **LLM Integration:** OpenAI SDK, Ollama API  
- **Data Handling:** Dataclasses for prompt and model management  
- **Infrastructure & Quality:** Poetry, pytest, mypy, python-dotenv  

---

## 🚀 Getting Started

### 1. Clone Repository
```bash
git clone https://github.com/YourUsername/ai-web-summarizer.git
cd ai-web-summarizer
```

### 2. Environment Configuration
- **Configure your API keys and model settings:**
```bash
cp .env_example .env
# Edit .env with your OpenAI API key, model names, and temperature settings
```

### 3. Setup Dependencies
- **Configure your API keys and model settings:**
```bash
poetry install
poetry shell
```

### 4. Quality Checks
- **Configure your API keys and model settings:**
```bash
# Static type checking
poetry run mypy src tests main.py

# Run tests with coverage
poetry run pytest --cov=src --cov-report=term-missing
```

## 📝 Usage & Operations
- **Summarize a Web Page via CLI**
```bash
poetry run python main.py --url https://www.jetbrains.com/pycharm/ --count 10 --language English --format json
poetry run python main.py --url https://www.jetbrains.com/pycharm/ --count 10 --language English --format yaml
```
### 📝 Example Output
**You can check an example of the generated summary here:**
- [Click to view summary_output.json](docs/examples/summary_output.json)
- [Click to view summary_output.yaml](docs/examples/summary_output.yaml)

## 📂 Project Structure
```text
ai-web-summarizer/
├── src/
│   ├── llm/             # LLM clients, prompts, and model definitions
│   ├── scrapper/        # HTML text extractor
│   ├── service/         # Summary pipeline and file writer
│   └── settings.py      # Environment configuration & client factories
├── tests/               # Pytest suite
├── main.py              # CLI entry point
├── prompts/             # YAML prompt templates
├── pyproject.toml       # Poetry & linter configurations
├── env.py               # Empty .env
└── .env_example         # Template for API keys and settings
```

*Designed and engineered by [Damian Kowalczyk](https://github.com/DamianKowalczykDK).
Focus on automation, type safety, and clean architecture.*