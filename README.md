# BeforeItsPrinted

# AI-Powered Practice Exam Generator

### Description

- Before It's Printed (BIP) is a machine learning-powered tool that generates custom practice exams based on uploaded exam files and user preferences
- It is designed to be fast, modular, and progressively intelligent with a fully self-hosted PyTorch model as usage data accumulates

---

## NOTICE

- Please read through this `README.md` to better understand the project's source code and setup instructions
- Also, make sure to review the contents of the `License/` directory
- Your attention to these details is appreciated — enjoy exploring the project!

---

## Problem Statement

- I discovered that one of the most effective ways to study for exams is to try to predict the exam questions in advance and practice answering them
- Even when the predicted questions aren't exact matches, they often turn out to be very similar to the actual exam, making it excellent targeted practice
- This project is designed to bring that strategy to life through automation and AI

---

## Project Goals

### Integrate the system with my **existing Django server** and allow users to upload practice materials

- Seamlessly embed the frontend file upload interface into the Django web platform, enabling authenticated users to submit their study documents for processing

### Build a robust **file parser using FastAPI** and popular Python packages (`pdfplumber`, `python-docx`, `pytesseract`, etc.)

- Develop a modular and high-accuracy parsing service to extract structured question data from multiple file formats, including PDFs, Word documents, scanned images, and plain text

### Use a **self-trained PyTorch model** to generate high-quality practice questions for cost-efficient, offline question generation

- Fine-tune and deploy a local language model trained on curated exam datasets, eliminating API costs while preserving privacy and inference speed

### Provide exam customization controls (length, difficulty, topic, format) for users

- Implement a dynamic interface that allows users to configure question generation parameters, tailoring the output to specific study goals and testing formats

---

## Tools, Materials & Resources

### Tools

- Django, FastAPI, Docker Compose, GitHub Actions, Terraform

### Materials

- Past exams in `.pdf`, `.docx`, `.png`, `.jpg`, `.txt`, `.webp`

### Resources

- OpenAI GPT API, Hugging Face Transformers, PyTorch, Cloudflare Tunnel

---

## Design Decision

### Microservice Architecture

- FastAPI used as a separate parser service with Django frontend integration

### Cloudflare Tunnel for Access

- Enables secure public access without exposing server IP

### CI/CD with GitHub Actions

- Ensures automated, reproducible deployments with Terraform for infra

---

## Features

### Multi-format File Parsing

- Upload `.pdf`, `.docx`, `.png`, `.jpg`, `.webp`, or `.txt` files and automatically extract question content
- Automatically extract questions using OCR and NLP preprocessing

### AI-Powered Question Generation

- Receive structured JSON output (question format, difficulty, type)
- Fine-tune and self-host a PyTorch-based question generation model
- Collect anonymized usage and feedback data for ML training

### Modular Architecture

- Cross-origin requests supported between Django and FastAPI
- File upload form with fetch API integration
- Frontend, API, and parser are decoupled for scalability and independent updates

---

## Block Diagram

```plaintext
┌──────────────────┐        ┌──────────────────────┐        ┌─────────────────┐        ┌─────────────────────────────────┐
│  User Interface  ├── → ───┤  Django Web Server   ├── → ───┤     FastAPI     ├── → ───┤    PyTorch Fine-Tuning Model    │
│ (HTML/JS upload) ├─── ← ──┤  (Main web backend)  ├─── ← ──┤  (File → JSON)  ├─── ← ──┤    (Trained on collected data)  │
└──────────────────┘        └──────────────────────┘        └─────────────────┘        └─────────────────────────────────┘
```

---

## Functional Overview

- Hosted locally using Docker Compose
- Exposed to the internet via a Cloudflare Tunnel with Terraform-managed DNS
- Deployed via GitHub Actions and secure SSH automation
- Users upload past exams
- The system extracts content, runs it through NLP preprocessing, and generates practice questions
- Final exam is downloadable or displayed on-screen

---

## Challenges & Solutions

### Challenge: File Format Inconsistencies

- Solution: Implement separate parsers for each file type using specialized libraries

### Challenge: Cost of AI APIs

- Solution: Long-term migration to a fine-tuned, self-hosted PyTorch model

---

## Lessons Learned

### Lesson 1

- Fast iteration and clean microservices are key to managing scope in AI projects

### Lesson 2

- Cloudflare Tunnel and Terraform simplify secure deployments and DNS integration

---

## Project Structure

```plaintext
root/
├── License/
│   ├── LICENSE.md
│   │
│   └── NOTICE.md
│
├── .gitattributes
│
├── .gitignore
│
├── README.md
│
├── .github/
│   └── workflows
│       └── deploy.yml
│
├── desktop/
│   ├── src
│   │   └── index.ts
│   │
│   ├── package-lock.json
│   │
│   ├── package.json
│   │
│   └── tsconfig.json
│
├── fastapi/
│   ├── Dockerfile
│   │
│   ├── __init__.py
│   │
│   ├── core.py
│   │
│   ├── image.py
│   │
│   ├── main.py
│   │
│   ├── models.py
│   │
│   ├── pdf.py
│   │
│   ├── requirements.txt
│   │
│   ├── txt.py
│   │
│   └── word.py
│
├── proxy/ 
│   ├── bin/
│   │   └── www
│   │
│   ├── public/
│   │   └── stylesheets/
│   │       └── style.css
│   │
│   ├── routes/
│   │   ├── index.js
│   │   │
│   │   └── users.js
│   │
│   ├── app.js
│   │
│   ├── package-lock.json
│   │
│   └── package.json
│
├── .terraform.lock.hcl
│
├── docker-compose.yaml
│
└── main.tf

```

---

## Future Enhancements

- Admin dashboard to view user activity & feedback
- Question quality rating system
- AI answer explanations
- Support for scanned handwritten input
- LaTeX/Canvas/Moodle export templates
