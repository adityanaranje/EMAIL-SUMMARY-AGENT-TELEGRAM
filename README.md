# 📧 AI Email Job Agent → Telegram Bot

![Python](https://img.shields.io/badge/Python-3.11-blue) ![GitHub
Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-success)
![OpenAI](https://img.shields.io/badge/LLM-OpenAI-orange) ![Telegram
Bot](https://img.shields.io/badge/Notifications-Telegram-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Automation](https://img.shields.io/badge/Automation-Email%20Agent-purple)

An **AI-powered automation system** that monitors Gmail for job emails,
extracts structured job information using LLMs, and sends formatted
alerts to Telegram.

The system runs automatically via **GitHub Actions every 15 minutes**.

------------------------------------------------------------------------

# 🚀 Features

### 📬 Gmail Monitoring

-   Reads unread emails via Gmail API
-   Filters recent emails
-   Marks processed emails as **read**

### 🤖 AI Email Analysis

Uses LLMs to:

-   Classify job emails
-   Extract job details
-   Identify skills
-   Summarize email content

### 📲 Telegram Job Alerts

Example notification:

    🚨 Software Engineer - Morningstar

    📍 Location: Mumbai
    💼 Experience: 2–4 years

    🛠 Skills
    • Python
    • SQL
    • AWS

    🧠 Summary
    • Build AI agents for data automation
    • Deliver client-ready analytics reports

------------------------------------------------------------------------

# 🏗 Architecture Diagram

``` mermaid
flowchart LR
    Gmail[Gmail Inbox] --> Fetch[Email Reader]
    Fetch --> LLM[LLM Job Extractor]
    LLM --> Parser[JSON Parser]
    Parser --> Telegram[Telegram Bot]
    Telegram --> User[User Notification]
```

------------------------------------------------------------------------

# ⚙️ Workflow Diagram

``` mermaid
flowchart TD
    Start[GitHub Actions Scheduler] --> GmailCheck[Check Unread Gmail]
    GmailCheck --> Decision{Emails Found?}
    Decision -- No --> Stop[End Run]
    Decision -- Yes --> FetchEmails[Fetch Email Content]
    FetchEmails --> LLMAnalyze[LLM Analysis]
    LLMAnalyze --> Extract[Extract Job + Skills]
    Extract --> SendTelegram[Send Telegram Alert]
    SendTelegram --> MarkRead[Mark Email Read]
    MarkRead --> Stop
```

------------------------------------------------------------------------

# 🎬 Animated Pipeline

``` mermaid
sequenceDiagram
    participant GitHub
    participant Gmail
    participant AI
    participant Telegram
    participant User

    GitHub->>Gmail: Check unread emails
    Gmail-->>GitHub: Return messages
    GitHub->>AI: Send email content
    AI-->>GitHub: Extract job info
    GitHub->>Telegram: Send alert
    Telegram-->>User: Job notification
```

------------------------------------------------------------------------

# 📂 Project Structure

    email-job-agent-telegram
    │
    ├── app
    │   ├── main.py
    │   ├── gmail_auth.py
    │   ├── email_reader.py
    │   ├── job_extractor.py
    │   └── telegram_sender.py
    │
    ├── config
    │   └── settings.py
    │
    ├── requirements.txt
    └── .github/workflows/bot.yml

------------------------------------------------------------------------

# ⚡ Automation

The bot runs automatically:

    Every 15 minutes
    6 AM → 12 AM

Pipeline:

    GitHub Actions
          ↓
    Check Gmail
          ↓
    LLM email analysis
          ↓
    Extract job details
          ↓
    Send Telegram alert

------------------------------------------------------------------------

# 🛠 Tech Stack

-   Python
-   Gmail API
-   OpenAI / LangChain
-   Telegram Bot API
-   GitHub Actions
-   OAuth2

------------------------------------------------------------------------

# 🔐 Required GitHub Secrets

Add in:

`Repo → Settings → Secrets → Actions`

    OPENAI_API_KEY
    TELEGRAM_BOT_TOKEN
    TELEGRAM_CHAT_ID
    GMAIL_TOKEN

------------------------------------------------------------------------

# 💡 Future Improvements

-   Job relevance scoring
-   Resume-job matching
-   Skill trend analysis
-   Daily job digest

------------------------------------------------------------------------

# 👨‍💻 Author

**Aditya Naranje**\
AI / ML Engineer\
Generative AI \| LLM Applications \| Automation Systems

------------------------------------------------------------------------
