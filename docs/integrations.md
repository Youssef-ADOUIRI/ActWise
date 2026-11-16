# Integrations

Step 11 connects ActWise to Slack, to MCP clients and to a Google Sheets register. All three are thin clients of the HTTP API (decision [014](decisions/014-integrations.md)):

| Client | Speaks | Runs | Code |
|---|---|---|---|
| `/actwise` in Slack | Slack's Socket Mode | On the laptop, beside the API | `integrations/slack_bot.py` |
| MCP tools `ask_ai_act`, `classify_ai_system` | MCP over stdio | Started by the MCP client | `integrations/mcp_server.py` |
| The AI system register | Google Sheets API | Inside the API, after each `/classify` and `/upload` | `integrations/sheets.py` |
| The Streamlit UI and `/upload` (step 8) | HTTP | Beside the API | `ui/app.py` |

They all reach the API through `integrations/client.py`: `ACTWISE_API_URL` (default `http://localhost:8000`) and `ACTWISE_API_KEY` when the API needs one. Start the API first with `make serve`.

Secrets go in `.env` only. `.env.example` lists every variable.

## Slack: `/actwise`

1. **Workspace:** create a free one at https://slack.com/get-started.
2. **App:** at https://api.slack.com/apps, **Create New App → From a manifest**, pick the workspace and paste [`slack_manifest.yaml`](../src/actwise/integrations/slack_manifest.yaml). It turns on Socket Mode, so Slack needs no public URL, and asks for the `commands` scope only.
3. **App token:** **Basic Information → App-Level Tokens → Generate**, with the scope `connections:write`. Copy the `xapp-…` token into `SLACK_APP_TOKEN`.
4. **Bot token:** **Install App → Install to Workspace**. Copy the `xoxb-…` token into `SLACK_BOT_TOKEN`.
5. **Run:** `make serve` in one terminal, `make slack` in another. In any channel, type:
   - `/actwise ask Which AI practices are prohibited?`
   - `/actwise classify A tool that ranks job applicants from their CVs and rejects the lowest.`

Slack needs an answer within 3 seconds, so the bot acknowledges at once ("Reading the law…") and replies when the API has answered. **Replies are ephemeral:** only the user who typed the command sees them, so a pasted system description stays private.

Socket Mode keeps a connection open, which doesn't suit Cloud Run's scale-to-zero. The bot runs on the laptop for the demo, against the local or the deployed API.

## MCP: VS Code

[`.vscode/mcp.json`](../.vscode/mcp.json) declares the server; VS Code starts it with `uv run --extra integrations` when a chat needs it.

1. **Check the protocol** with the MCP Inspector:
   ```
   npx @modelcontextprotocol/inspector uv run --extra integrations python -m actwise.integrations.mcp_server
   ```
   **Connect → Tools → List Tools** shows `ask_ai_act` and `classify_ai_system`. Call each from there.
2. **VS Code:** open the repo, run **MCP: List Servers → actwise → Start**, then open the chat in Agent mode. Ask, for example, "Use classify_ai_system on: a chatbot that answers customers of a bank". The chat asks before each tool call.

A tool returns the same text as Slack: the answer or the tier, the cited articles under their labels, and the notice. An API error, for example the daily cap, comes back as a tool error with the API's message.

## Google Sheets: the AI system register

Each classification appends one row:

| timestamp | description_hmac | tier | confidence | citations | model |
|---|---|---|---|---|---|
| 2026-11-16T09:30:00+00:00 | 3f9a0c51d2e7 | high_risk | 0.80 | AIA-Art6-2, AIA-AnnexIII-4 | gemini-3.5-flash-lite |

The description is never stored. `description_hmac` is HMAC-SHA-256 with `REGISTER_KEY`, first 12 hex characters: the same description always gets the same id, and whoever reads the sheet can't test a guessed description without the key.

**Setup, in the Google Cloud console** (the project step 13 deploys to; the Sheets API needs no billing account):

1. **Project:** https://console.cloud.google.com → **New project**, for example `actwise`.
2. **API:** **APIs & Services → Library → Google Sheets API → Enable**. The Drive API is not needed: the register opens its sheet by id, with the `spreadsheets` scope only.
3. **Service account:** **IAM & Admin → Service Accounts → Create**, for example `actwise-register`, with no role. It reaches only the sheets shared with it.
4. **Key:** on the account, **Keys → Add key → Create new key → JSON**. Put the file's content on one line, in single quotes, in `.env`:
   ```
   uv run python -c "import json, sys; print(json.dumps(json.load(open(sys.argv[1]))))" key.json
   ```
   Then `GSHEETS_SA_JSON='<that line>'`, and delete the downloaded file.
5. **Sheet:** create a Google Sheet, for example "ActWise register". **Share** it with the service account's email (`client_email` in the key) as **Editor**. Put the id from its URL (between `/d/` and `/edit`) in `GSHEETS_REGISTER_ID`. The API writes the header row into an empty sheet.
6. **Hash key:** `uv run python -c "import secrets; print(secrets.token_hex(32))"` into `REGISTER_KEY`.
7. **Run:** restart `make serve`; each `/classify` and `/upload` now adds a row.

A Sheets outage never costs the user an answer: the API logs the failure and returns the classification. Each Sheets call times out after 5 seconds.

## Upload

`POST /upload` (step 8) classifies a `.txt`, `.md`, `.pdf` or `.docx` description of up to 2 MB, cut at 8,000 characters. The demo file describes a CV-ranking tool:

```
curl -F "file=@data/demo/talentsort.docx" http://localhost:8000/upload
```

The Streamlit UI (`make ui`) sends files through the same route.
