# DEV.to Submission Post
<!-- Publish at: https://dev.to/new -->
<!-- Required tags: devchallenge, notionchallenge, mcp, ai -->
<!-- Deadline: 2026-03-29 11:59 PM PST -->

---

## Title
FreelanceFlow: Auto-Generate Your Client SOW, Proposal & Invoice from a Single Brief using Notion MCP

## Tags
`devchallenge` `notionchallenge` `mcp` `ai`

## Cover image
[record demo video → screenshot the moment 4 docs appear]

---

## Post Body (paste below)

---

Every time I land a new freelance client, I spend 2–3 hours writing the same documents: a Statement of Work, a milestone tracker, a welcome message, and an invoice template. The brief is already there — why am I doing this manually?

**FreelanceFlow** is a Notion Custom Agent + MCP integration that eliminates that work entirely. Paste your client's brief into a Notion database. Four documents appear automatically. Done.

---

## What It Does

When a new entry is added to the "Client Pipeline" Notion database, FreelanceFlow:

1. **Parses the brief** — extracts project type, budget, timeline, deliverables, and red flags
2. **Generates a Statement of Work** — scope, out-of-scope, milestones table, revision policy
3. **Writes a client welcome message** — 150-200 words, names specifics from the brief, asks 3 clarifying questions
4. **Creates a milestone tracker** — Notion table, pre-populated with amounts and dates
5. **Produces an invoice template** — line items matching the milestones

It also auto-detects red flags (vague briefs, below-rate requests, prohibited work) and adds a warning callout at the top.

---

## How It Uses Notion MCP

The project has two parts:

### Part 1: The Notion Custom Agent (no-code)
The agent itself is an instruction set built in Notion's Custom Agents feature (launched Feb 2026). It triggers on database events, reads the brief, and writes structured documents as child pages.

### Part 2: The MCP CLI (Python)
For automated feeding, `notion_freelanceflow.py` uses the **Notion MCP server** (`https://mcp.notion.com/mcp`) to create Client Pipeline entries programmatically — from the command line, from other tools, or from other AI agents.

```python
# Create a pipeline entry via Notion MCP
result = mcp_call("notion-create-pages", {
    "parent": {"database_id": database_id},
    "properties": {
        "Name": {"title": [{"text": {"content": f"New Brief — {today}"}}]},
        "Status": {"select": {"name": "New Brief"}},
        "Brief": {"rich_text": [{"text": {"content": brief_text}}]},
    },
})
```

The MCP call creates the entry → the Custom Agent fires → documents appear.

```bash
# CLI usage
python notion_freelanceflow.py --brief "Need a Python scraper for competitor pricing, $800, 10 days"
python notion_freelanceflow.py --file client_brief.txt
python notion_freelanceflow.py --interactive
```

---

## Demo

[EMBED VIDEO HERE — 30-60 seconds]

Timestamps:
- 0:00 — Problem: "This takes 2-3 hours manually"
- 0:05 — Run CLI with a job description
- 0:12 — Watch Notion: entry appears, agent fires
- 0:20 — Open the generated documents: SOW, welcome message, milestones, invoice
- 0:28 — "FreelanceFlow. Available in the Notion Marketplace."

---

## Technical Stack

- **Notion Custom Agents** — the automation layer (instruction-based, no code)
- **Notion MCP** (`https://mcp.notion.com/mcp`) — Streamable HTTP transport, OAuth 2.0
- **Python** — `httpx` for MCP calls, `python-dotenv` for config
- **MCP tools used**: `notion-create-pages`, `notion-search`, `notion-fetch`

---

## Setup

```bash
git clone https://github.com/metaplansolutions/freelanceflow-notion
cd freelanceflow-notion
pip install httpx python-dotenv

# Copy .env.example → .env, fill in:
# NOTION_MCP_TOKEN=your_token_here (get from https://mcp.notion.com/mcp)
# NOTION_DATABASE_ID=your_database_id

python notion_freelanceflow.py --interactive
```

**Agent setup**: Import the [FreelanceFlow template from the Notion Marketplace](https://notion.so/marketplace) → configure to point at your Client Pipeline database → done.

---

## What I Learned

The most interesting constraint: **Notion Custom Agents are entirely instruction-driven**. You write natural language describing the workflow, not code. This means the quality of your output is a prompt engineering problem. The challenge was writing instructions precise enough that the agent consistently creates structured tables and callout blocks — not just prose.

The MCP CLI bridges the gap: once you have the MCP integration, FreelanceFlow becomes composable. You can feed it from Claude Code, from a cron job, from another agent — any tool that can run a Python script.

---

## Try It

- [GitHub repo](https://github.com/metaplansolutions/freelanceflow-notion)
- [FreelanceFlow on Notion Marketplace](https://notion.so/marketplace) ← link after publish
- Built for the [Notion MCP Challenge on DEV.to](https://dev.to/challenges/notion-2026-03-04)

---

*Built in 3 days. Saves 2-3 hours per client. Worth it.*

---

## Notes Before Publishing
- [ ] Replace [USERNAME] with actual GitHub username
- [ ] Add Notion Marketplace link once published
- [ ] Embed actual demo video (YouTube or direct)
- [ ] Add cover image screenshot
- [ ] Verify required tags are applied: `devchallenge`, `notionchallenge`, `mcp`, `ai`
