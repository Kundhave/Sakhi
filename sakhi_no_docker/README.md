# 🌸 Sakhi — WhatsApp-first SHG Financial Platform

Sakhi digitizes SHG financial records via a WhatsApp chatbot, builds a dynamic credit score for each member, and generates bank-ready PDF credit reports — all without requiring members to use a smartphone app.

---

## Architecture

```
WhatsApp (Member) ←→ whatsapp-web.js bot ←→ Node.js + Prisma ←→ PostgreSQL
                                                   ↕
                                     React Dashboard (SHG Leader)
```

---

## Prerequisites

- Node.js 18+
- Docker + Docker Compose (for recommended setup)
- Git
- A smartphone with WhatsApp installed (for the leader/bot account)

---

## 🐳 Setup with Docker (Recommended)

### Step 1 — Clone the repository

```bash
git clone <your-repo-url>
cd sakhi
```

### Step 2 — Set up environment

```bash
cp .env.example .env
# Edit .env if you want to change API keys or passwords
```

### Step 3 — Start all services

```bash
docker-compose up --build
```

This will:
- Start PostgreSQL on port 5432
- Run database migrations automatically
- Start the backend on port 3001
- Start the React frontend on port 5173

Wait until you see:
```
🚀 Sakhi backend running on http://localhost:3001
```

### Step 4 — Scan WhatsApp QR Code

1. Open your browser to **http://localhost:3001/qr**
2. You'll see a QR code on screen
3. On the leader's smartphone: WhatsApp → Settings → Linked Devices → Link a Device
4. Scan the QR code
5. Wait for "✅ WhatsApp client ready. Bot is live!" in backend logs

> **Important**: The WhatsApp session is saved in `.wwebjs_auth/` folder. You only need to scan once. If this folder is deleted, you must scan again.

### Step 5 — Access the Dashboard

1. Open **http://localhost:5173**
2. Enter the leader's WhatsApp number (with country code, no + or spaces, e.g. `919876543210`)
3. If first time: Click "Register SHG Group" to create your group
4. Add members with their WhatsApp numbers

### Step 6 — Test the chatbot

From a member's phone, send any message to the leader's WhatsApp number. The bot menu will appear in the member's language.

---

## 🛠️ Manual Setup (Without Docker)

### Prerequisites for manual setup

Install PostgreSQL locally or use [Supabase](https://supabase.com) (free tier).

### Backend

```bash
cd backend

# Install dependencies
npm install

# Set environment variables
cp ../.env.example .env
# Edit .env:
# DATABASE_URL=postgresql://username:password@localhost:5432/sakhi
# PORT=3001
# API_KEY=your_secret_key

# Run database migrations
npx prisma migrate dev --name init

# Generate Prisma client
npx prisma generate

# Start the backend
node src/index.js
```

### Frontend (new terminal)

```bash
cd frontend

# Install dependencies
npm install

# Create env file
echo "VITE_API_URL=http://localhost:3001" > .env

# Start the dev server
npm run dev
```

Open **http://localhost:5173** in your browser.

---

## Project Structure

```
sakhi/
├── docker-compose.yml          # All services
├── Dockerfile.backend          # Backend + Chromium for Puppeteer
├── Dockerfile.frontend         # React dev server
├── .env.example                # Environment template
│
├── backend/
│   ├── prisma/schema.prisma    # Database schema
│   └── src/
│       ├── index.js            # Express server entry point
│       ├── whatsapp/
│       │   ├── client.js       # WhatsApp client + QR handling
│       │   ├── stateMachine.js # Message router (state machine)
│       │   └── flows/          # Contribution, loan, score, verify flows
│       ├── api/routes/         # REST API endpoints
│       └── services/
│           ├── creditScore.js  # 7-factor credit scoring engine
│           ├── schemeEligibility.js  # Govt scheme checker
│           ├── pdfReport.js    # Puppeteer PDF generator
│           └── notifications.js  # WhatsApp notification sender
│
└── frontend/
    └── src/
        ├── pages/              # Dashboard, Members, Loans, Reports
        └── components/         # CreditScoreCard, TransactionHistory, etc.
```

---

## Chatbot Flow

```
Member sends any message
         ↓
   Is member registered? → No → "Contact your SHG leader"
         ↓ Yes
   Read state from DB
         ↓
   IDLE → Show main menu (in member's language)
         ↓
   1 → Contribution flow → Save transaction → Recalculate credit score
   2 → Loan request flow → Notify leader on WhatsApp
   3 → Show credit score summary
   4 → Show loan details
   5 → Show leader's contact info
   6 → Show eligible government schemes
```

Type `menu` or `0` at any point to reset to the main menu.

---

## Credit Score Engine

The score (0-100) is calculated from 7 weighted factors:

| Factor | Weight | Description |
|--------|--------|-------------|
| Repayment on time | 25% | % of loan repayments made on or before due date |
| Savings behavior | 20% | Contribution frequency + amount consistency |
| Tenure & growth | 15% | SHG tenure + trend in contribution amounts |
| Repayment speed | 15% | Average days early/late for repayments |
| Loan utilization | 10% | Outstanding vs total savings + loan purpose type |
| Meeting attendance | 10% | % of SHG meetings attended |
| Group health bonus | 5% | Overall group repayment rate |

**Score Bands:**
- 80-100: EXCELLENT (green)
- 60-79: GOOD (blue)
- 40-59: FAIR (amber)
- 0-39: NEEDS IMPROVEMENT (red)

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /qr | WhatsApp QR code scan page |
| GET | /api/groups/by-leader/:phone | Login / lookup group |
| POST | /api/groups | Register new SHG group |
| GET | /api/members/group/:groupId | List members |
| POST | /api/members | Add member |
| GET | /api/members/:id | Member detail with transactions |
| GET | /api/dashboard/:groupId | Dashboard analytics |
| GET | /api/loans/group/:groupId | Loan requests |
| PATCH | /api/loans/:id/approve | Approve loan + notify member |
| PATCH | /api/loans/:id/reject | Reject loan + notify member |
| GET | /api/reports/group/:groupId | Download group PDF report |
| GET | /api/reports/member/:memberId | Download member PDF report |

All API endpoints require `X-API-Key` header matching the `API_KEY` environment variable.

---

## Environment Variables

```env
# Database
DATABASE_URL=postgresql://sakhi_user:sakhi_password@localhost:5432/sakhi

# Backend
PORT=3001
API_KEY=sakhi_secret_key_change_this

# Frontend (.env in frontend/)
VITE_API_URL=http://localhost:3001
```

---

## Troubleshooting

### QR Code not appearing

- Check backend logs: `docker-compose logs backend`
- Make sure port 3001 is not in use: `lsof -i :3001`
- Restart backend: `docker-compose restart backend`
- Visit `http://localhost:3001/qr` — if WhatsApp is already connected it shows a success message

### WhatsApp session expired

```bash
# Delete the session folder and re-scan
rm -rf .wwebjs_auth
docker-compose restart backend
# Visit http://localhost:3001/qr and scan again
```

### Database connection errors

```bash
# Check if PostgreSQL is running
docker-compose logs postgres

# If tables don't exist, run migrations manually
docker-compose exec backend npx prisma migrate deploy

# Reset database completely (CAUTION: deletes all data)
docker-compose exec backend npx prisma migrate reset
```

### Puppeteer / PDF generation failing in Docker

The Dockerfile installs Chromium system-wide. If PDF fails:

```bash
# Check if Chromium is installed
docker-compose exec backend which chromium

# Test Puppeteer directly
docker-compose exec backend node -e "const p = require('puppeteer'); p.launch({executablePath: '/usr/bin/chromium', args: ['--no-sandbox']}).then(b => { console.log('OK'); b.close(); })"
```

For local (non-Docker) setup: Puppeteer will download its own Chromium during `npm install`.

### Tamil/Hindi characters not rendering in PDF

The Dockerfile installs `fonts-noto`, `fonts-noto-cjk`, and `fonts-indic`. If characters show as boxes:

```bash
docker-compose exec backend fc-list | grep -i noto
```

If fonts are missing, rebuild the image:

```bash
docker-compose build --no-cache backend
```

### Member not found errors

- Phone numbers must be stored WITHOUT `@c.us` suffix and WITHOUT `+` prefix
- Example: store `919876543210`, not `+919876543210` or `919876543210@c.us`
- Check the member's phone in the database matches exactly what WhatsApp sends

### Port conflicts

```bash
# Check what's using the ports
lsof -i :3001
lsof -i :5173
lsof -i :5432

# Change ports in docker-compose.yml or .env as needed
```

### Frontend can't connect to backend (CORS)

The backend allows all origins by default. If you see CORS errors:
- Make sure `VITE_API_URL` in `frontend/.env` points to the correct backend URL
- In production, update the CORS config in `backend/src/index.js`

### WhatsApp client disconnects frequently

- This can happen due to phone being offline or WhatsApp Web session limits
- The bot will attempt to reconnect automatically
- If it persists, delete `.wwebjs_auth` and re-scan the QR code

---

## Languages Supported

| Language | Code | Coverage |
|----------|------|----------|
| Tamil | `TAMIL` | Full — all bot messages |
| Hindi | `HINDI` | Full — all bot messages |
| Telugu | `TELUGU` | Full — all bot messages |
| English | `ENGLISH` | Full — default fallback |

Set `member.language` when adding a member via the dashboard.

---

## Government Schemes Checked

| Scheme | Eligibility |
|--------|-------------|
| PM Jan Dhan Yojana | No bank account |
| PMJJBY (Life Insurance) | Has bank account |
| PMSBY (Accident Insurance) | Has bank account |
| PM Mudra Shishu | Score ≥ 70 + business/agriculture loan history |
| PM SVANidhi | Score ≥ 60 + business loan history |
| NABARD SHG Linkage | Group 6+ months active + positive corpus |

Members are notified via WhatsApp when they become eligible for a new scheme.

---

## License

MIT
