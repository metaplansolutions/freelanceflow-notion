# FreelanceFlow

**Auto-generate your client SOW, proposal & invoice from a single brief — using Notion Custom Agents + MCP.**

Every time you land a new freelance client, you spend 2–3 hours writing the same documents: Statement of Work, milestone tracker, welcome message, invoice template. FreelanceFlow eliminates that work. Paste the client's brief into Notion. Four documents appear automatically.

---

## What It Does

When a new entry is added to your "Client Pipeline" Notion database, FreelanceFlow:

1. **Parses the brief** — extracts project type, budget, timeline, deliverables, red flags
2. **Generates a Statement of Work** — scope, out-of-scope items, milestones table, revision policy
3. **Writes a client welcome message** — 150–200 words, names specifics from the brief, 3 clarifying questions
4. **Creates a milestone tracker** — pre-populated Notion table with amounts and target dates
5. **Produces an invoice template** — line items matching milestones

Red flags (vague brief, below-rate, prohibited work) are detected automatically and surfaced as a warning callout at the top of the document.

---

## How It Works

### Part 1 — Notion Custom Agent (no-code)

The agent is a prompt/instruction set built in Notion's Custom Agents feature. It triggers on the `Page added` database event, reads the brief, and writes structured documents as child pages. No code runs — it's all instruction-driven.

Import the [FreelanceFlow template from the Notion Marketplace](#) to get the agent pre-configured.

### Part 2 — Python MCP Client

`notion_freelanceflow.py` feeds briefs into Notion programmatically via the [Notion MCP server](https://mcp.notion.com/mcp). This makes FreelanceFlow composable: feed it from the CLI, from Claude Code, from a cron job, or from any tool that can run Python.

```
CLI brief → Notion MCP → Client Pipeline database → Custom Agent fires → 4 docs generated
```

---

## Setup

### Prerequisites

- Notion account on **Business or Enterprise** plan (or 30-day free trial)
- Python 3.8+
- `httpx` and `python-dotenv`

### 1. Clone and install

```bash
git clone https://github.com/metaplansolutions/freelanceflow-notion
cd freelanceflow-notion
pip install -r requirements.txt
```

### 2. Get your Notion MCP token

1. Go to [https://mcp.notion.com/mcp](https://mcp.notion.com/mcp)
2. Click **Connect** and authorize your Notion workspace
3. Copy the OAuth token that appears

### 3. Configure

```bash
cp .env.example .env
# Edit .env and add your token + database ID
```

| Variable | Where to find it |
|---|---|
| `NOTION_MCP_TOKEN` | [https://mcp.notion.com/mcp](https://mcp.notion.com/mcp) after OAuth |
| `NOTION_DATABASE_ID` | In your Client Pipeline database URL (the UUID segment) |

### 4. Set up the Notion agent

1. In Notion: **Sidebar → Agents → + New agent**
2. Name it **FreelanceFlow**
3. Paste the contents of [`AGENT_INSTRUCTIONS.md`](AGENT_INSTRUCTIONS.md) into the Instructions field
4. Set **Trigger** → Database → `@Client Pipeline` → "Page added"
5. Set **Access** → `@Client Pipeline` (read + write)
6. Set **Model** → Auto

### 5. Run it

```bash
# Inline brief
python notion_freelanceflow.py --brief "Need a Python scraper for competitor pricing, $800, 10 days"

# From a file
python notion_freelanceflow.py --file client_brief.txt

# Interactive mode
python notion_freelanceflow.py --interactive
```

---

## Testing

Five test briefs are included in [`demo_briefs.txt`](demo_briefs.txt):

- **Brief 1** — Python scraper, clear scope ($800)
- **Brief 2** — LangChain support agent, medium complexity ($2k–$3k)
- **Brief 3** — ETL pipeline, well-specified ($4k)
- **Brief 4** — Vague brief (tests red flag detection)
- **Brief 5** — Streamlit app, realistic Contra job ($600)

---

## MCP Tools Used

| Tool | Purpose |
|---|---|
| `notion-create-pages` | Create the Client Pipeline entry |
| `notion-search` | Find the database when no ID is configured |

**Transport**: Streamable HTTP
**Auth**: OAuth 2.0 Bearer token
**Rate limits**: 180 req/min general, 30 req/min search

---

## Technical Stack

- **Notion Custom Agents** — instruction-driven automation layer
- **Notion MCP** (`https://mcp.notion.com/mcp`) — Streamable HTTP, OAuth 2.0
- **Python** — `httpx` for HTTP, `python-dotenv` for config

---

## Built For

[Notion MCP Challenge on DEV.to](https://dev.to/challenges/notion-2026-03-04) + [Contra Custom Agent Buildathon](https://contra.com/community/topic/notioncustomagentbuildathon)

*Built in 3 days. Saves 2–3 hours per client.*
