---
description: Guided setup for connecting external apps to Claude
argument-hint: "[app name]"
---

Help the user connect external apps to this Claude session.

1. If an app was named in `$ARGUMENTS`, focus on it. Otherwise ask which apps they want (e.g. Gmail, Slack, Google Drive, Canva, Zapier).
2. Use ToolSearch / ListConnectors to check which connectors are already connected and which are available.
3. For each requested app:
   - Already connected: confirm and show one example of what it can do.
   - Available but not connected: tell the user to authorize it in their claude.ai connector settings. Never ask for tokens, codes or callback URLs.
   - Not available: say so, and suggest Zapier as a bridge if it is connected.
4. Finish with a short summary table: app, status, next step.

Do not take actions in connected apps (sending, posting, deleting) during setup.
