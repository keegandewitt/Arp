# Claude Code MCP Server Setup

## Overview

This project uses Model Context Protocol (MCP) servers to extend Claude Code's capabilities. The configuration is split between **shared project settings** (committed to git) and **personal settings** (local only).

## MCP Servers Used

1. **Context7** - Provides up-to-date library documentation
2. **Perplexity** - AI-powered search and research capabilities
3. **Firecrawl** - Web scraping and content extraction

## File Structure

```
/Cursor/Arp/
├── .mcp.json                          # ✓ COMMITTED - Shared MCP server config
├── .claude/
│   ├── commands/                      # ✓ COMMITTED - Custom slash commands
│   ├── settings.json                  # ✓ COMMITTED - Shared project settings (if exists)
│   └── settings.local.json            # ✗ NOT COMMITTED - Personal permissions/settings
└── .gitignore                         # Updated to handle Claude Code files
```

## Initial Setup (One-time per machine)

### 1. Set up environment variables

Add these to your shell profile (`~/.zshrc` for zsh, `~/.bashrc` for bash):

```bash
# ===== MCP Server API Keys =====
export CONTEXT7_API_KEY="your-context7-key-here"
export PERPLEXITY_API_KEY="your-perplexity-key-here"
export FIRECRAWL_API_KEY="your-firecrawl-key-here"
# ================================
```

**Get your API keys:**
- Context7: https://upstash.com/docs/context7/overall/getstarted
- Perplexity: https://www.perplexity.ai/settings/api
- Firecrawl: https://www.firecrawl.dev/app/api-keys

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

### 4. Clone the repo and start Claude Code

```bash
git clone <repo-url>
cd Arp
claude
```

The `.mcp.json` file will automatically configure the MCP servers using your environment variables.

## Configuration Files Explained

### `.mcp.json` (Project-level, committed)

Defines which MCP servers to use and their configuration. Uses environment variables for API keys so they're not committed to git:

```json
{
  "mcpServers": {
    "context7": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest", "--api-key", "${CONTEXT7_API_KEY}"],
      "env": {}
    },
    // ... other servers
  }
}
```

### `.claude/settings.local.json` (Personal, NOT committed)

Contains your personal permissions and settings. This is auto-generated and specific to your machine:

```json
{
  "permissions": {
    "allow": ["Bash(python3:*)", "WebSearch", ...],
    "deny": [],
    "ask": []
  }
}
```

## Team Collaboration

When a team member clones this repo:

1. They set up their environment variables **once** in their shell profile
2. The `.mcp.json` automatically works with their credentials
3. They can customize their personal permissions in `.claude/settings.local.json`
4. Any changes to MCP server configuration are shared via `.mcp.json` in git

## Troubleshooting

### MCP servers not loading

```bash
# Check environment variables are set
echo $CONTEXT7_API_KEY

# Re-source your shell profile
source ~/.zshrc

# Check MCP server status in Claude Code
/mcp
```

### Permission issues

Personal permissions are stored in `.claude/settings.local.json`. Edit this file or use `/permissions` in Claude Code.

### Adding/Removing MCP Servers

Edit `.mcp.json` and commit the changes. Team members will get the updates on their next `git pull`.

## Security Notes

- ✅ API keys are stored in environment variables (not committed)
- ✅ `.mcp.json` uses `${VAR}` syntax for secure key injection
- ✅ `.claude/settings.local.json` is gitignored (personal settings)
- ✅ Keys are set once per machine in shell profile
- ❌ Never hardcode API keys in `.mcp.json`
- ❌ Never commit `.claude/settings.local.json`

## Advanced: Per-Project API Keys

If you need different API keys per project, you can set them in the project directory:

```bash
# In your project directory
export FIRECRAWL_API_KEY="project-specific-key"
claude
```

Or create a `.env` file (add to `.gitignore`!) and source it before starting Claude Code.
