<div align="center">

# 🌸 Sakhi — सखी — சகி

### *Financial Identity for Every Rural Woman*

**India has 33 million SHG women. Banks don't know they exist.**

---

[![Node.js](https://img.shields.io/badge/Node.js-22+-339933?style=flat-square&logo=node.js&logoColor=white)](https://nodejs.org)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)](https://reactjs.org)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Telegram](https://img.shields.io/badge/Bot-Telegram-26A5E4?style=flat-square&logo=telegram&logoColor=white)](https://telegram.org)

</div>

---

## The Problem

India has **2.2 million Self Help Groups** with **33 million women members** who pool savings, give internal loans, and repay them — often without missing a single payment for years.

Yet when they walk into a bank, they're invisible.

Their records live in **handwritten notebooks**. Those notebooks get damaged, lost, or stay behind when leadership changes. There is no way to verify what happened, no audit trail, and no credit history that a bank will accept.

> A woman who has saved ₹500 every month for 5 years without fail **cannot get a ₹10,000 loan** — not because she's a bad borrower, but because she has no way to prove she's a good one.

**Over 50% of SHG bank loan applications are rejected** — not due to default, but due to poor documentation.

---

## The NABARD Connection

**NABARD's SHG-Bank Linkage Programme** is India's largest microfinance initiative, enabling banks to give collateral-free loans directly to Self Help Groups — yet over **46% of SHGs, nearly 67 lakh groups, remain credit-unlinked** as of March 2024, largely because their financial records exist only in handwritten notebooks that banks won't accept.

Sakhi is built specifically to close this gap. By digitally recording every contribution and repayment through a chatbot and generating a verified, timestamped PDF credit report, Sakhi gives any SHG the documentation they need to qualify for NABARD bank linkage and access the formal credit system — many for the first time.

---

## Our Solution

**Sakhi digitizes SHG financial records through tools these women already use** — and turns years of disciplined saving into a verifiable credit identity.

No new habits required. No smartphones needed for members. No complicated onboarding.

```
Member sends a message
         ↓
Sakhi records the transaction
         ↓
Credit score updates automatically
         ↓
Leader downloads a bank-ready PDF report
         ↓
Bank sees verified financial history
         ↓
Loan approved
```

Two interfaces. Two user types. One connected system.

| SHG Members | SHG Leader |
|---|---|
| Chatbot (Telegram) | Web dashboard |
| Record monthly contributions | Register group and add members |
| Request loans | Approve or reject loans |
| Check credit score | View group analytics |
| View government scheme eligibility | Download PDF credit report for banks |

---

## Why Telegram — and Why Not WhatsApp

The honest answer: **we wanted WhatsApp, and we couldn't get it to work reliably.**

WhatsApp has no official open bot API. The only way to automate it is through unofficial reverse-engineered libraries that depend on running a headless browser — fragile, unstable, and requires the leader's actual WhatsApp account to stay permanently linked. We tried. It crashed repeatedly.

So we made a deliberate decision.

**Telegram has a real, official, free Bot API.** No browser. No linked device. No QR codes. A token from @BotFather and it works instantly, reliably, at scale. The member experience is identical to what we designed for WhatsApp — numbered menus, multilingual replies, step-by-step flows, conversation state persisted in the database.

**WhatsApp is the production goal.** WhatsApp Business API (Meta's official API) supports exactly this kind of bot. The moment we have access, the bot layer swaps out with zero changes to the Node.js backend or the React dashboard — because all the logic lives in the backend, not the bot. The architecture was built for this from day one.

---

## The Credit Score

Sakhi builds a **0–100 credit score** for each member from her SHG behavior alone. No CIBIL. No bank account required. No formal credit history needed.

**9 factors, each weighted by financial significance:**

| Factor | Weight | What It Measures |
|--------|--------|-----------------|
| Repayment on time | 25% | Did she pay back loans when due? |
| Growth | 15% | Is her contribution amount increasing over time? |
| Speed of repayment | 15% | How early or late does she repay? |
| Contribution frequency | 13% | Does she contribute every single month? |
| Contribution amount | 12% | Is she consistent in how much she contributes? |
| Connections | 5% | How strong is her group's overall repayment culture? |
| Attendance | 5% | Does she show up to meetings? |
| Tenure | 5% | How long has she been a member? |
| Loan purpose | 5% | Is she borrowing for productive reasons? |

New members get a **Founding Score** based on the leader's onboarding inputs until enough live transaction data builds up. A confidence indicator — LOW / MEDIUM / HIGH — tells banks exactly how the score was computed.

| Score | Band | What It Unlocks |
|-------|------|----------------|
| 80–100 | 🟢 Excellent | NABARD bank linkage + Mudra loans |
| 60–79 | 🔵 Good | Favorable internal SHG loans |
| 40–59 | 🟡 Fair | Building history |
| 0–39 | 🔴 Needs Improvement | Intervention recommended |

---

## How the Chatbot Works

The bot is a **state machine**. Every member's current step in a conversation is saved to the database. When they send a message — even hours later — the bot picks up exactly where they left off.

**Monthly Contribution Flow:**
```
Bot:    How much are you contributing this month?
Member: 500
Bot:    Do you have a loan repayment? 1. Yes  2. No
Member: 2
Bot:    Confirm: Contribution ₹500, Repayment: None. 1. Confirm  2. Re-enter
Member: 1
Bot:    Thank you! Your record has been updated ✅
        → Transaction saved to Supabase
        → Credit score recalculated
```

**Loan Request Flow:**
```
Bot:    How much loan are you requesting?
Bot:    Reason? 1.Agriculture 2.Business 3.Education 4.Medical 5.Home Repair...
Bot:    How many months to repay?
Bot:    Your loan request has been sent to your leader 🌸
        → LoanRequest saved with status PENDING
        → Leader sees it instantly on the dashboard
```

Supported languages: **Tamil · Hindi · Telugu · English**
The leader sets each member's language at registration. Every message, menu, confirmation, and error is fully translated.

---

## Architecture

```
┌─────────────────┐        ┌──────────────────────┐        ┌──────────────────┐
│  Telegram Bot   │──HTTP──▶   Node.js Backend    ◀──HTTP──│  React Dashboard │
│  (Python)       │        │  Express + Prisma     │        │  Vite + Tailwind │
└─────────────────┘        └──────────┬───────────┘        └──────────────────┘
                                      │
                           ┌──────────▼───────────┐
                           │  PostgreSQL           │
                           │  (Supabase)           │
                           └──────────────────────┘
```

The Telegram bot and React dashboard both talk to the same backend API. All business logic — credit scoring, scheme eligibility, PDF generation — lives in the backend. Swapping Telegram for WhatsApp Business API means changing only the bot layer.

---

## Future Scope

- **WhatsApp Business API** — the intended production channel, same flows, zero backend changes
- **NABARD bank integration** — direct digital submission of PDF credit reports
- **UPI payment tracking** — auto-record contributions from UPI transaction data
- **Voice bot** — IVR interaction for members without any smartphone
- **Scheme application assist** — guided scheme application through the bot, not just eligibility alerts

---

## Setup

### Prerequisites
Node.js 22+, Python 3.10+, a Supabase account (free at supabase.com)

### 1. Install
```bash
cd backend && npm install
cd ../frontend && npm install
cd ../telegram_bot && pip install -r requirements.txt
```

### 2. Environment variables

**`backend/.env`**
```
DATABASE_URL=postgresql://postgres:password@db.xxxx.supabase.co:5432/postgres
PORT=3001
API_KEY=sakhi_secret_key_change_this
```

**`telegram_bot/.env`**
```
TELEGRAM_BOT_TOKEN=your_token_from_botfather
BACKEND_URL=http://localhost:3001
API_KEY=sakhi_secret_key_change_this
```

### 3. Database
```bash
cd backend
npx prisma migrate deploy && npx prisma generate
```

### 4. Run (three terminals)
```bash
cd backend && npm run dev        # Terminal 1 → http://localhost:3001
cd frontend && npm run dev       # Terminal 2 → http://localhost:5173
cd telegram_bot && python bot.py # Terminal 3 → Telegram polling
```

### 5. Register a member
1. Leader registers the SHG group on the dashboard
2. Member sends `/start` to the bot → bot replies with their Telegram ID
3. Leader adds member in dashboard with phone number as `TG_<their_telegram_id>`
4. Member can now use all bot features immediately

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Node.js 22, Express, Prisma 5.7 |
| Database | PostgreSQL via Supabase |
| Bot | Python 3, python-telegram-bot 21.6, httpx |
| Frontend | React 18, Vite, Tailwind CSS |
| PDF Reports | Puppeteer |

---

<div align="center">

**Built for the women who keep communities together.**

*We're not asking them to change their behavior.*
*We're making what they already do count.*

</div>
