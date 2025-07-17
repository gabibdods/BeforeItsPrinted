# 🧠 BIP — AI-Powered Practice Exam Generator

BIP (*Before It's Printed*) is a machine learning-powered tool that generates custom practice exams based on uploaded exam files and user preferences. It is designed to be fast, modular, and progressively intelligent — starting with OpenAI's GPT and transitioning to a fully self-hosted PyTorch model as usage data accumulates.

---

## 🔍 Problem Statement

I discovered that one of the most effective ways to study for exams is to **try to predict the exam questions** in advance and practice answering them. Even when the predicted questions aren't exact matches, they often turn out to be **very similar** to the actual exam — making it excellent targeted practice.

This project is designed to bring that strategy to life through automation and AI.

---

## 🎯 Project Goals:

- ✅ Build a robust **file parser using FastAPI** and popular Python packages (`pdfplumber`, `python-docx`, `pytesseract`, etc.)
- ✅ Integrate the system with my **existing Django server** and allow users to upload practice materials
- ✅ Use **OpenAI's GPT API** initially to generate high-quality practice questions
- 🔜 Gradually transition to a **self-trained PyTorch model** for cost-efficient, offline question generation
- ✅ Provide exam customization controls (length, difficulty, topic, format) for users

---

## 🚀 Features

- ✅ Upload `.pdf`, `.docx`, `.png`, `.jpg`, `.webp`, or `.txt` exam files
- ✅ Automatically extract questions using OCR and NLP preprocessing
- ✅ Receive structured JSON output (question format, difficulty, type)
- 🔜 Generate high-quality exam questions using OpenAI's GPT API
- 🔜 Collect anonymized usage and feedback data for ML training
- 🔜 Fine-tune and self-host a PyTorch-based question generation model

---

## 🧪 Current Capabilities

| Component      | Status       | Description                                                |
|----------------|--------------|------------------------------------------------------------|
| Django Frontend| ✅ Completed | File upload form with fetch API integration               |
| FastAPI Server | ✅ Completed | Handles file uploads, parses content, returns JSON        |
| Parsers        | ✅ Completed | `.pdf`, `.docx`, `.txt`, `.png`, `.jpg`, `.webp` supported |
| CORS + API     | ✅ Completed | Cross-origin requests supported between Django ↔ FastAPI  |
| CI/CD Pipeline | ✅ Completed | GitHub Actions + Terraform + Docker Compose               |

---

## 🧠 Upcoming Components

### 🔮 OpenAI Integration (`/generate/` endpoint)

- Use OpenAI’s GPT-4o to:
  - Generate multiple-choice, short-answer, and development-style questions
  - Match exam style, topic, and difficulty based on uploaded content
- Configurable via frontend (topics, length, format, difficulty)
- Logged usage will build a dataset for later ML training

### 🧠 PyTorch NLP Trainer (Long-term self-hosted AI)

- Collect labeled data (prompt-response pairs, user feedback)
- Preprocess into training format (JSONL, Hugging Face Datasets)
- Fine-tune a base LLM (e.g. Phi-2, Mistral, LLaMA 3 8B) for question generation
- Train using PyTorch/Transformers + evaluate with BLEU/F1/etc.
- Deploy via ONNX or Hugging Face Inference stack

---

## 💡 Tech Stack

| Layer            | Tech                                     |
|------------------|------------------------------------------|
| Frontend         | HTML + JavaScript (Django template)      |
| API Gateway      | Django + Fetch API                       |
| NLP Service      | FastAPI                                  |
| File Parsing     | pdfplumber, python-docx, pytesseract     |
| Containerization | Docker Compose                           |
| CI/CD            | GitHub Actions + Terraform               |
| LLM (phase 1)    | OpenAI GPT-4o via API                    |
| LLM (phase 2)    | PyTorch + Hugging Face Transformers      |

---

## 📁 Project Structure

```plaintext
BIP/
├── backend/ # Django frontend + file uploader
├── fastapi/ # FastAPI microservice (file parser)
│ ├── main.py # Entry point and upload API
│ ├── pdf.py # PDF parser
│ ├── image.py # Image parser (OCR)
│ ├── word.py # Word (.docx) parser
│ ├── txt.py # Plaintext parser
│ ├── models.py # Pydantic schema
├── docker-compose.yaml # Multi-service container orchestration
├── .github/workflows/deploy.yml # GitHub Actions CI/CD pipeline
├── infra/ # Terraform infra (Cloudflare tunnel, SSH deploy)

```

---

## ⚙️ Current Architecture Overview

```plaintext
+------------------+         +---------------------+         +--------------------+
|  User Interface  |  --->   |   Django Web Server |  --->   |  FastAPI Parser    |
| (HTML/JS upload) |         |  (Main web backend) |         | (File → JSON)      |
+------------------+         +---------------------+         +--------------------+
        |                            |                                |
        |   1️⃣ File selected        |                                |
        |   2️⃣ Form submitted via JS fetch                          |
        |                            |                                |
        |                            |                                |
        |                            | 3️⃣ POST file to FastAPI       |
        |                            |     /parse/                    |
        |                            |                                |
        |                            | <--- 4️⃣ JSON Response --------+
        | <--- 5️⃣ Render JSON preview                               |
        |
        |
        |        +----------------------------------+
        |        | Optional: User selects settings  |
        |        | (Topics, Difficulty, Format...)  |
        |        +----------------------------------+
        |
        |                            |
        |                            | 6️⃣ Send config + JSON → /generate/
        |                            |     (LLM question generation)
        |                            |
        |                            | 7️⃣ Uses OpenAI API to generate questions
        |                            |
        |                            | 8️⃣ Returns generated exam questions
        |                            |
        | <--- 9️⃣ Final exam delivered to user

```

---

## ⚙️ Long-Term Architecture Overview

```plaintext
+---------------------------+
|     User Feedback Loop    |
+---------------------------+
             |
             v
+---------------------------+     +-------------------------+
|   Logging Prompt/Response | --> |  Training Data Pipeline |
+---------------------------+     +-------------------------+
                                            |
                                            v
                              +------------------------------+
                              |   PyTorch Fine-Tuning Model  |
                              |  (Trained on collected data) |
                              +------------------------------+
                                            |
                                            v
                           Used in place of OpenAI to generate questions

```

---

## 🔐 Deployment & Infrastructure

- Hosted locally using Docker Compose
- Cloudflare Tunnel exposed via Terraform-managed DNS
- SSH deploys with GitHub Actions runner

---

## 📥 Future Enhancements

- [ ] Admin dashboard to view user activity & feedback
- [ ] Question quality voting/rating system
- [ ] AI feedback: explain why each answer is correct/incorrect
- [ ] Support for scanned handwritten input (OCR tuning)
- [ ] Custom question formatting templates (LaTeX, Canvas, Moodle)

