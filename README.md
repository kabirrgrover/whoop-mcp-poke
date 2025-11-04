# WHOOP MCP Server for Poke

Connect your WHOOP fitness data to Poke AI assistant using the Model Context Protocol (MCP).

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

---

## 🎯 What This Does

This MCP server lets you query your WHOOP fitness data through Poke AI assistant using natural language:

- **"What's my recovery score today?"** - Get your daily recovery metrics
- **"How did I sleep last night?"** - Analyze your sleep performance  
- **"Show me my strain data"** - View workout strain and heart rate zones
- **"What's my biological age?"** - Check your WHOOP Age and healthspan metrics

---

## ✨ Features

- 🏃 **5 WHOOP Data Tools**: Overview, Sleep, Recovery, Strain, Healthspan
- 🔄 **Automatic Token Refresh**: Handles authentication seamlessly
- 🌐 **Cloud Ready**: Deploy to Render with one click
- 🤖 **Poke Compatible**: Works out of the box with Poke AI

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- [WHOOP account](https://www.whoop.com) with active subscription
- [Poke account](https://poke.com) (for AI assistant integration)
- [Render account](https://render.com) (free tier works)

### Option 1: Deploy to Render (Recommended)

1. **Click the "Deploy to Render" button above**

2. **Configure your deployment:**
   - Name: `whoop-mcp-server` (or your choice)
   - Branch: `main`

3. **Set environment variables:**
   - `WHOOP_EMAIL`: Your WHOOP account email
   - `WHOOP_PASSWORD`: Your WHOOP account password

4. **Wait for deployment** (~5-10 minutes)

5. **Get your MCP URL:**
   ```
   https://your-service-name.onrender.com/mcp
   ```

6. **Connect to Poke:**
   - Go to https://poke.com/settings/connections/integrations/new
   - Add your MCP URL
   - Start asking questions!

### Option 2: Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kabirrgrover/whoop-mcp-poke.git
   cd whoop-mcp-poke
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your WHOOP credentials
   ```

5. **Run the server:**
   ```bash
   python src/server.py
   ```

6. **Server runs at:** `http://localhost:8000/mcp`

---

## 🔧 Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `WHOOP_EMAIL` | ✅ Yes | Your WHOOP account email |
| `WHOOP_PASSWORD` | ✅ Yes | Your WHOOP account password |
| `PORT` | ❌ No | Server port (default: 8000, auto-set by Render) |

### WHOOP Credentials

Get your WHOOP credentials:
1. Sign up at https://www.whoop.com
2. Ensure you have an active WHOOP subscription
3. Use your login email and password

**Security Note:** Your credentials are stored securely in environment variables and never logged or exposed.

---

## 📱 Using with Poke

### Connect to Poke

1. Deploy your server to Render (or run locally with ngrok)
2. Go to https://poke.com/settings/connections/integrations/new
3. Add your MCP server URL
4. Test the connection

### Testing the Connection

After connecting to Poke, test with:
```
"Use the test_connection tool"
```

You should see: ✅ MCP Server is working! Connection successful.

### Available Tools

#### 1. Overview Data
Ask Poke: *"What's my WHOOP data for today?"*

Returns:
- Recovery score
- Day strain
- Sleep hours
- Calories burned
- HRV, RHR trends
- Today's activities

#### 2. Sleep Analysis
Ask Poke: *"How did I sleep last night?"*

Returns:
- Sleep performance score
- Hours slept vs needed
- Sleep consistency
- Sleep efficiency
- Insights and recommendations

#### 3. Recovery Metrics
Ask Poke: *"What's my recovery score?"*

Returns:
- Recovery score (0-100%)
- HRV with trends
- RHR with trends
- Respiratory rate
- Coach insights

#### 4. Strain Tracking
Ask Poke: *"Show me my strain data"*

Returns:
- Strain score
- Heart rate zone distribution
- Strength activity time
- Steps
- Individual workouts

#### 5. Healthspan
Ask Poke: *"What's my biological age?"*

Returns:
- WHOOP Age (biological age)
- Age comparison vs chronological
- Pace of aging
- Weekly trends

### Example Conversation

```
User: What's my recovery score today?

Poke: [Calls whoop_get_recovery tool]

Response: Your recovery is 72% (Green - Ready to perform)

📊 Key Metrics:
  • HRV: 65ms (↑ 8% vs baseline)
  • RHR: 52bpm (↓ 3% vs baseline)
  • Sleep Performance: 85%

💡 Coach Insight: "Your recovery is in the green. Your body 
is ready for a high-intensity workout today."

User: Should I do a hard workout?

Poke: Based on your 72% recovery (green zone), yes! Your HRV 
is trending up 8% and your RHR is down 3%, indicating your 
body has recovered well. Your sleep was also strong at 85%. 
This is a great day for high-intensity training.
```

---

## 🏗️ Architecture

```
Poke AI ←→ MCP Server (Render) ←→ WHOOP API
         HTTPS/MCP              HTTPS/AWS Cognito
```

### Technology Stack

- **FastMCP 2.0** - MCP server framework
- **Python 3.10+** - Runtime
- **httpx** - Async HTTP client
- **Render** - Cloud hosting
- **AWS Cognito** - WHOOP authentication

---

## 🛠️ Development

### Project Structure

```
whoop-mcp-poke/
├── src/
│   ├── server.py           # FastMCP server
│   ├── whoop_client.py     # WHOOP API client
│   ├── config.py           # Configuration
│   └── tools/
│       └── whoop.py        # Tool handlers
├── requirements.txt        # Python dependencies
├── render.yaml            # Render configuration
└── README.md              # This file
```

### Running Tests

Test your MCP server with the MCP Inspector:

```bash
# Start your server
python src/server.py

# In another terminal
npx @modelcontextprotocol/inspector
```

Open http://localhost:3000 and connect to `http://localhost:8000/mcp` using "HTTP" transport.

---

## 🔒 Security

- ✅ Credentials stored in environment variables only
- ✅ WHOOP tokens auto-refresh (24-hour lifetime)
- ✅ No credentials in code or logs
- ✅ HTTPS for all API calls
- ✅ AWS Cognito authentication

**Best Practices:**
- Never commit `.env` file
- Use strong WHOOP password
- Rotate credentials if exposed
- Use Render's environment variable encryption

---

## 🐛 Troubleshooting

### "Authentication failed" Error

**Solution:**
1. Verify your WHOOP email and password in Render environment variables
2. Try logging into https://app.whoop.com with the same credentials
3. Ensure your WHOOP subscription is active

### "Invalid MCP server URL" in Poke

**Solution:**
1. Verify your URL is exactly: `https://your-service-name.onrender.com/mcp`
2. Check that your Render service is running (green status)
3. Test the endpoint in a browser - you should see JSON response

### Deployment Timeout on Render

**Solution:**
1. Check Render logs for specific errors
2. Verify all environment variables are set
3. Ensure `requirements.txt` has all dependencies

### Server responds but no data returned

**Solution:**
1. Verify your WHOOP subscription is active
2. Check you have recent WHOOP data (wear your strap!)
3. Try querying data from a specific date: "What was my recovery on 2025-11-01?"

### "No module named 'fastmcp'" Error

**Solution:**
1. Verify `requirements.txt` has `fastmcp>=2.0.0`
2. On Render, trigger a manual deploy to reinstall dependencies
3. Check Render logs for failed dependency installation

---

## 📚 Resources

### Documentation
- [FastMCP Documentation](https://gofastmcp.com)
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)
- [MCP Protocol](https://modelcontextprotocol.io)
- [Poke Integration Guide](https://poke.com/settings/connections)
- [WHOOP](https://www.whoop.com)
- [Render Documentation](https://render.com/docs)

### Related Projects
- [WHOOP MCP (TypeScript)](https://github.com/JedPattersonn/whoop-mcp) - Original TypeScript implementation
- [Poke MCP Template](https://github.com/InteractionCo/mcp-server-template) - Official Poke template
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector) - Tool for testing MCP servers

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

MIT License - feel free to use this for your own projects!

---

## ⭐ Acknowledgments

- Built with [FastMCP 2.0](https://github.com/jlowin/fastmcp)
- Inspired by [WHOOP MCP TypeScript implementation](https://github.com/JedPattersonn/whoop-mcp)
- Designed for [Poke AI Assistant](https://poke.com)

---

## 💬 Support

If you have questions or issues:
1. Check the [Troubleshooting](#-troubleshooting) section above
2. [Open an issue](https://github.com/kabirrgrover/whoop-mcp-poke/issues) on GitHub
3. Review [FastMCP documentation](https://gofastmcp.com)
4. Check [Poke's integration guide](https://poke.com/settings/connections)

---

## 🚀 Quick Links

- **Live Example:** https://mcp-server-ct3l.onrender.com/mcp (demo server)
- **Use This Template:** Click "Use this template" button above
- **Report Issues:** [GitHub Issues](https://github.com/kabirrgrover/whoop-mcp-poke/issues)
- **Star on GitHub:** Show your support! ⭐

---

**Made with ❤️ for the WHOOP and Poke communities**

*This is an open-source project. Contributions, issues, and feature requests are welcome!*

