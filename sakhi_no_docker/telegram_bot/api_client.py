# telegram_bot/api_client.py
# All HTTP calls to the Node.js backend go through this module.

import os
import httpx

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:3001")
API_KEY = os.getenv("API_KEY", "sakhi_secret_key_change_this")

HEADERS = {"X-API-Key": API_KEY, "Content-Type": "application/json"}


def _client():
    return httpx.AsyncClient(base_url=BACKEND_URL, headers=HEADERS, timeout=15.0)


# ── Member ─────────────────────────────────────────────────────────────────────

async def get_member_by_telegram_id(telegram_id: int):
    """Look up a member by their Telegram user ID (stored in phoneNumber field)."""
    async with _client() as c:
        r = await c.get(f"/api/members/by-telegram/{telegram_id}")
        if r.status_code == 200:
            return r.json()
        return None


async def get_member(member_id: str):
    async with _client() as c:
        r = await c.get(f"/api/members/{member_id}")
        if r.status_code == 200:
            return r.json()
        return None


async def update_member_state(member_id: str, state: str, context: dict):
    async with _client() as c:
        await c.patch(f"/api/members/{member_id}", json={
            "conversationState": state,
            "conversationContext": context,
        })


# ── Transactions ───────────────────────────────────────────────────────────────

async def save_contribution(member_id: str, group_id: str, amount: float):
    async with _client() as c:
        await c.post("/api/transactions", json={
            "memberId": member_id,
            "groupId": group_id,
            "type": "CONTRIBUTION",
            "amount": amount,
            "daysLate": 0,
            "verifiedByMember": True,
        })


async def save_repayment(member_id: str, group_id: str, amount: float, outstanding: float):
    async with _client() as c:
        # Save repayment transaction
        await c.post("/api/transactions", json={
            "memberId": member_id,
            "groupId": group_id,
            "type": "LOAN_REPAYMENT",
            "amount": amount,
            "daysLate": 0,
            "verifiedByMember": True,
        })
        # Update outstanding loan amount
        new_outstanding = max(0, outstanding - amount)
        await c.patch(f"/api/members/{member_id}", json={
            "outstandingLoanAmount": new_outstanding,
        })


async def update_total_contributed(member_id: str, increment: float):
    async with _client() as c:
        # Get current value then increment
        r = await c.get(f"/api/members/{member_id}")
        if r.status_code == 200:
            current = r.json().get("totalContributed", 0)
            await c.patch(f"/api/members/{member_id}", json={
                "totalContributed": current + increment,
            })


# ── Credit Score ───────────────────────────────────────────────────────────────

async def recalculate_score(member_id: str):
    async with _client() as c:
        await c.post(f"/api/members/{member_id}/recalculate-score")


# ── Loans ──────────────────────────────────────────────────────────────────────

async def create_loan_request(member_id: str, group_id: str, amount: float,
                               purpose: str, repayment_months: int):
    async with _client() as c:
        r = await c.post("/api/loans", json={
            "memberId": member_id,
            "groupId": group_id,
            "amount": amount,
            "purpose": purpose,
            "repaymentMonths": repayment_months,
            "status": "PENDING",
        })
        if r.status_code in (200, 201):
            return r.json()
        return None


async def get_active_loans(member_id: str):
    async with _client() as c:
        r = await c.get(f"/api/loans/member/{member_id}")
        if r.status_code == 200:
            return r.json()
        return []


# ── Group ──────────────────────────────────────────────────────────────────────

async def get_group(group_id: str):
    async with _client() as c:
        r = await c.get(f"/api/groups/{group_id}")
        if r.status_code == 200:
            return r.json()
        return None


# ── Schemes ────────────────────────────────────────────────────────────────────

async def get_eligible_schemes(member_id: str):
    async with _client() as c:
        r = await c.get(f"/api/members/{member_id}/schemes")
        if r.status_code == 200:
            return r.json()
        return []


# ── Aggregate stats ────────────────────────────────────────────────────────────

async def get_total_savings(member_id: str) -> float:
    async with _client() as c:
        r = await c.get(f"/api/transactions/member/{member_id}")
        if r.status_code == 200:
            txns = r.json()
            return sum(t["amount"] for t in txns if t["type"] == "CONTRIBUTION")
        return 0.0
