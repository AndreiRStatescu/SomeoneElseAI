# Vercel Deployment Guide

## Full Stack Deployment (Frontend + Backend on Vercel)

The project is configured to deploy both the React frontend and FastAPI backend on Vercel.

### Files Created:

- `vercel.json` - Configuration for both frontend and backend
- `api/index.py` - Serverless function entry point using Mangum adapter
- `api/requirements.txt` - Python dependencies for serverless function
- `frontend/.vercelignore` - Frontend-specific ignore rules
- `.vercelignore` - Root-level ignore rules

### Architecture:

- **Frontend**: Static React app built with Vite, served from `/frontend/dist`
- **Backend**: FastAPI app wrapped with Mangum adapter for serverless deployment
- **Routes**: API routes (`/healthz`, `/random_parrot`, `/chat/*`) proxy to backend, all other routes serve frontend

### Important Notes on Streaming:

⚠️ **Vercel Serverless Functions have limitations with streaming responses**:

- Maximum execution time: 10 seconds (Hobby), 60 seconds (Pro), 300 seconds (Enterprise)
- Streaming may be buffered or interrupted
- The `/random_parrot` and `/chat/stream` endpoints may not work as smoothly as on a traditional server

### Alternative: Hybrid Deployment

For better streaming support, consider:

1. Deploy **frontend** to Vercel
2. Deploy **backend** to Railway/Render/Fly.io (supports long-lived connections)
3. Update frontend to use environment variable for backend URL

### Steps to Deploy to Vercel:

1. **Install dependencies**:

   ```bash
   pip install mangum
   ```

2. **Set up environment variables in Vercel dashboard**:

   - `OPENAI_API_KEY` - Your OpenAI API key
   - Any other environment variables your backend needs

3. **Deploy**:

   ```bash
   vercel
   ```

4. **For production**:
   ```bash
   vercel --prod
   ```

### File Structure:

```
/
├── api/
│   ├── index.py          # Serverless function entry point
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── dist/            # Built frontend (generated)
│   └── ...
├── src/                 # Backend source code
└── vercel.json          # Vercel configuration
```

### Environment Variables:

Set these in your Vercel project settings:

- `OPENAI_API_KEY` - Your OpenAI API key
- Character files are included in the deployment (from `data/characters/`)

### Testing Locally:

Backend:

```bash
source venv/bin/activate
uvicorn src.api.api:app --reload --port 8000
```

Frontend:

```bash
cd frontend
npm run dev
```

### Troubleshooting:

1. **Streaming not working**: Vercel may buffer streaming responses. Consider deploying backend separately.
2. **Timeout errors**: Increase timeout limits in Vercel settings (Pro/Enterprise plans).
3. **Import errors**: Make sure all dependencies are in `api/requirements.txt`.
4. **Character files not found**: Ensure `data/characters/` is not in `.vercelignore`.
