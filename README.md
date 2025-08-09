# 🛡️ Guardrails in Agentic AI

This repository contains **Guardrail implementations** in Agentic AI using **Python**.  
A **guardrail** is a set of rules or boundaries that ensure an AI agent behaves **safely**, **ethically**, and **according to requirements**.  

In this project, I’ve built **three different guardrail scenarios** to demonstrate how AI agents can be **controlled, monitored, and restricted** in real-world applications.

---

## 📚 What Are Guardrails in AI?

In AI systems, **guardrails** act as **rules or constraints** that prevent an AI from:

- 🚫 Producing harmful, unsafe, or undesired outputs  
- 🚫 Breaking safety, ethical, or operational boundaries  
- 🚫 Ignoring specific requirements given by humans or systems  

**Examples:**
- If a chatbot is told **not** to share personal data → a guardrail **blocks** the response  
- If a recommender system must show **only certain products** → a guardrail **enforces compliance**

---

## 🏗 Project Scenarios Implemented

### 1️⃣ Class Timing Guardrail ⏰
**Goal:** Ensure students arrive for class only at the **scheduled time**.  
**Logic:** If a student is early or late, the AI **politely denies** entry.

---

### 2️⃣ Father Guardrail 👨‍👦
**Goal:** Allow a child to go outside **only if the weather is suitable**.  
**Logic:** If the temperature is **below 26°C** or unsafe, the AI **denies permission**.

---

### 3️⃣ Gatekeeper Guardrail 🚪
**Goal:** Restrict entry for students from **other schools**.  
**Logic:** Only students from **"Our School"** are allowed to pass.

---

## 📂 Project Structure
📦 **Guardrails Agentic AI**
├── class.py # Class timing guardrail
├── father.py # Father guardrail
├── gate_keeper.py # Gatekeeper guardrail
└── README.md # Documentation

---

## ⚙️ Technologies Used

- **Python 3.11+** 🐍  
- **OpenAI Agents Framework** 🤖  
- **dotenv** – Environment variable handling  
- **Custom Guardrail Logic** – Input & output restrictions  

---

## 🚀 How to Run the Project

1️⃣ **Clone the repository**  
- git clone https://github.com/RahatBano58/Guardrails-in-Agentic-AI.git
- cd Guardrails-in-Agentic-AI

2️⃣ **Run any guardrail file**
- class.py
- father.py
- gate_keeper.py

---

### ✨ Author
👩‍💻 **Rahat Bano** 💬 "AI should be powerful — but always responsible. Guardrails make sure of that."





