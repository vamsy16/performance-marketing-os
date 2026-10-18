# Quick Start — Do These 5 Things This Week

Forget everything else. Complete this checklist and you'll have a working agency.

---

## Day 1 (Today — 45 minutes)

### 1. Set up your CRM (5 min)
```bash
cd "05-CRM"
python crm.py
```
Choose "1. Add lead" and add any solar company you already know.
This is your command center. Everything goes here.

### 2. Install Python dependencies (2 min)
```bash
pip install -r 01-LEADS/requirements.txt
```

### 3. Discover live advertisers (one command)
Ask Arena: *"Run the ads-audit skill: discover leads for 'solar <your city>' limit 5, then review"*
It finds active advertisers from the live Meta Ad Library, audits each, and writes PDFs + `leads.csv`.

---

## Day 2 (30 minutes)

### 4. Review your first leads (20 min)
Open `01-LEADS/leads.csv`. Star the 10 most promising companies (owner-operated, active, small).

They're already in the CRM:
```bash
cd "05-CRM"
python crm.py import ../01-LEADS/leads.csv
```

### 5. Research your top 3 leads (20 min)
For each of the top 3:
- Google their name — note their rating and review count
- Check if they're in the Google Map Pack for "solar installer [your city]"
- Look at their website for 10 seconds — note one obvious improvement
- Write these observations down (you'll use them in emails)

---

## Day 3 (45 minutes)

### 6. Send your first 10 cold emails (45 min)
1. Open `02-OUTREACH/templates/cold_email_1.md`
2. For each of your top 10 leads, copy the template into Gmail
3. **Personalize:** company name, owner name, city, ONE specific observation
4. Send. Don't overthink. Done > perfect.

**🎯 MILESTONE: You're now doing outreach. Most people never start.**

---

## Day 4 (30 minutes)

### 7. Set up your free content engine (30 min)
1. Open Arena → Agent Mode
2. Copy the "Instagram carousel" prompt from `03-CONTENT/arena-prompts/prompt-library.md`
3. Fill in a solar company's details (use one of your leads as practice)
4. Save the output to a Google Drive folder named "Content — [Company]"

You just created content in 5 minutes. That's your delivery superpower.

---

## Day 5 (30 minutes)

### 8. Weekly review (15 min)
Answer in a notebook:
- How many emails sent? 
- How many replies?
- What went well?
- What felt hard?

### 9. Plan next week (15 min)
- Block 3 time slots on your calendar (even 30 min each)
- Pick your #1 goal (e.g., "5 audits booked" or "1st paying client")
- Schedule Day 6's outreach session

---

## After Week 1 — You're Live

At this point you have:
- ✅ A CRM with real leads
- ✅ An outreach system running
- ✅ An AI content engine ready
- ✅ Templates for everything
- ✅ A daily system that works in any time slot

**The only thing left is consistency. Show up. Send emails. Book audits. Close clients.**

---

## When You Get Stuck

| Problem | Solution |
|---|---|
| "No one is replying" | You need more volume. Send 20/day, not 5. Also check spam folder requirements (SPF/DKIM). |
| "They say too expensive" | Frame against their deal value. "One closed deal = 6 months of my fee." |
| "I don't know how to deliver SEO" | Read `04-DELIVERY/playbooks/seo.md` — it's step by step. |
| "I have no time this week" | Do the 15-min minimum: 3 emails. Keep the habit alive. |
| "This feels overwhelming" | Forget everything except: find leads → email them → book audits → close. That's the whole business. |
