# Claude Code MCP Server Setup

## Overview

This project uses Model Context Protocol (MCP) servers to extend Claude Code's capabilities. The configuration is in `.mcp.json` at the project root and uses environment variables for API keys.

## MCP Servers Configured

1. **Context7** - Up-to-date library documentation and code examples
2. **Perplexity** - AI-powered search, research, and reasoning
3. **Firecrawl** - Web scraping and content extraction

## Setup (New Team Members)

### 1. Set up environment variables (ONE-TIME SETUP)

**Get the API keys:**
- The actual API keys are in `.mcp-keys.txt` in the project root (gitignored, share via secure channel)
- Or contact Keegan for the keys

Add them to your shell profile (`~/.zshrc` for zsh, `~/.bashrc` for bash):

```bash
# ===== MCP Server API Keys =====
export CONTEXT7_API_KEY="your-context7-key-here"
export PERPLEXITY_API_KEY="your-perplexity-key-here"
export FIRECRAWL_API_KEY="your-firecrawl-key-here"
# ================================
```

**Tip:** You can copy the export commands directly from `.mcp-keys.txt` and paste into your `~/.zshrc`.

### 2. Reload your shell

```bash
source ~/.zshrc  # or source ~/.bashrc
```

### 3. Verify environment variables

```bash
echo $CONTEXT7_API_KEY
echo $PERPLEXITY_API_KEY
echo $FIRECRAWL_API_KEY
```

### 4. Clone and run

```bash
git clone <repo-url>
cd Arp
claude
```

The `.mcp.json` file will automatically use your environment variables.

## Why Environment Variables?

While this is a private repo, GitHub's push protection blocks commits with API keys for security. Using environment variables:
- ✅ Keeps GitHub happy (no blocked pushes)
- ✅ One-time setup per machine
- ✅ Works across all projects using the same keys
- ✅ Easy to update keys without changing code

## File Structure

```
/Cursor/prisme/
├── .mcp.json                          # MCP server config (uses ${ENV_VARS})
├── .claude/
│   ├── commands/                      # Custom slash commands
│   │   └── start.md                   # Includes MCP setup reminder
│   └── settings.local.json            # Personal permissions (gitignored)
└── docs/
    └── CLAUDE_CODE_SETUP.md           # This file
```

## Configuration

### `.mcp.json` (Project-level, committed)

Contains all MCP server definitions using environment variables:

```json
{
  "mcpServers": {
    "context7": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest", "--api-key", "${CONTEXT7_API_KEY}"],
      "env": {}
    },
    "perplexity": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@perplexity-ai/mcp-server"],
      "env": {
        "PERPLEXITY_API_KEY": "${PERPLEXITY_API_KEY}"
      }
    },
    "firecrawl": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "firecrawl-mcp"],
      "env": {
        "FIRECRAWL_API_KEY": "${FIRECRAWL_API_KEY}"
      }
    }
  }
}
```

### `.claude/settings.local.json` (Personal, NOT committed)

Contains your personal permissions and settings. Auto-generated and specific to your machine.

## Verify Setup

After starting Claude Code, run:

```
/mcp
```

You should see all 3 MCP servers listed: context7, perplexity, and firecrawl.

If they're not showing up, check:
1. Environment variables are set: `echo $CONTEXT7_API_KEY`
2. Shell profile was reloaded: `source ~/.zshrc`
3. Claude Code was started from a terminal that has the variables

## Managing MCP Servers

### Check Status
```
/mcp
```

### Enable/Disable a Server
@-mention the server name to toggle it on/off in the current session.

### Add/Remove Servers
Edit `.mcp.json` and commit the changes. Team members will get updates on their next `git pull`.

## Troubleshooting

### MCP Servers Not Loading

1. **Check environment variables are set:**
   ```bash
   echo $CONTEXT7_API_KEY
   echo $PERPLEXITY_API_KEY
   echo $FIRECRAWL_API_KEY
   ```
   If empty, add them to `~/.zshrc` and run `source ~/.zshrc`

2. **Restart Claude Code** after setting environment variables

3. **Check server status:**
   ```
   /mcp
   ```

4. **Verify npx is available:**
   ```bash
   which npx
   ```

### Permission Issues

Personal permissions are in `.claude/settings.local.json`. Use `/permissions` in Claude Code to manage them.

### Environment Variables Not Loading

Make sure you:
- Added the exports to the correct shell profile (`~/.zshrc` for zsh, `~/.bashrc` for bash)
- Reloaded the shell: `source ~/.zshrc`
- Started Claude Code from a terminal (not from Dock/Finder)

## Adding New MCP Servers

1. Find the MCP server package (usually on npm)
2. Add it to `.mcp.json` following the existing pattern
3. If it needs API keys, add them to your `~/.zshrc`:
   ```bash
   export NEW_SERVICE_API_KEY="your-key-here"
   ```
4. Reload shell and restart Claude Code
5. Commit `.mcp.json` changes
6. Document the new key in this file for team members

## Quick Reference

### Get API Keys
- Context7: https://upstash.com/docs/context7/overall/getstarted
- Perplexity: https://www.perplexity.ai/settings/api
- Firecrawl: https://www.firecrawl.dev/app/api-keys

### Resources
- Context7 Docs: https://upstash.com/docs/context7
- Perplexity API: https://docs.perplexity.ai/
- Firecrawl Docs: https://docs.firecrawl.dev/
- MCP Protocol: https://modelcontextprotocol.io/
- Claude Code Docs: https://docs.claude.com/en/docs/claude-code

## For Other Machines

If you work on multiple machines, you only need to:
1. Add the 3 export lines to `~/.zshrc` on each machine (ONE TIME)
2. Clone the repo
3. Run `claude`

The API keys stay in your shell profile, work across all projects, and never need to be entered again.
