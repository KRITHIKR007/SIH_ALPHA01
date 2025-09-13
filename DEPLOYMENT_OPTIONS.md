# 🚀 MINDPIECE Deployment Guide

## Free Deployment Options

### 1. 🤗 HuggingFace Spaces (Recommended for AI Apps)

**Steps:**
1. Go to [HuggingFace Spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Fill in details:
   - **Space name**: `mindpiece-dyslexia-screening`
   - **License**: MIT
   - **SDK**: Streamlit
   - **Hardware**: CPU (free)
4. Upload files:
   - `streamlit_app.py` (main app)
   - `requirements_hf.txt` → rename to `requirements.txt`
   - `README_HUGGINGFACE.md` → rename to `README.md`
   - `assets/` folder (if exists)
5. The app will auto-deploy in ~2-3 minutes

**✅ Pros**: 
- Perfect for AI/ML apps
- Permanent URLs
- Good free tier
- Community focused

**❌ Cons**: 
- Limited resources on free tier
- CPU only (free tier)

### 2. ☁️ Streamlit Cloud

**Steps:**
1. Push code to GitHub (already done)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect GitHub account
4. Select repository: `KRITHIKR007/SIH_ALPHA01`
5. Main file path: `streamlit_app.py`
6. Deploy

**✅ Pros**: 
- Native Streamlit support
- Easy GitHub integration
- Fast deployment

### 3. 🌐 Render.com

**Steps:**
1. Go to [render.com](https://render.com)
2. Connect GitHub
3. Create "Web Service"
4. Select repository
5. Configure:
   - **Build Command**: `pip install -r requirements_hf.txt`
   - **Start Command**: `streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0`

### 4. 🐙 GitHub Codespaces (Development)

**Steps:**
1. Go to your GitHub repository
2. Click "Code" → "Codespaces" → "Create codespace"
3. Wait for environment setup
4. Run: `streamlit run streamlit_app.py`
5. Forward port 8501
6. Access via provided URL

## Environment Variables

For any deployment platform, you can set these optional variables:

```bash
# Force demo mode (useful for deployments without backend)
STREAMLIT_CLOUD=true

# Custom API backend URL (if you have a hosted backend)
API_BASE_URL=https://your-backend-api.com

# HuggingFace Spaces (auto-detected)
SPACE_ID=username/space-name
```

## Files for Deployment

### Required Files:
- `streamlit_app.py` - Main application
- `requirements.txt` - Dependencies (use `requirements_hf.txt` for minimal deps)

### Optional Files:
- `README.md` - Project description
- `assets/` - Logo and images
- `.streamlit/config.toml` - Streamlit configuration
- `packages.txt` - System packages (for some platforms)

## Recommended: HuggingFace Spaces

For your AI-powered dyslexia screening app, I recommend **HuggingFace Spaces** because:

1. **AI-Focused Community**: Perfect audience for your app
2. **Permanent URLs**: No expiration like some free tiers
3. **Easy Deployment**: Just upload files
4. **Good Performance**: Decent resources on free tier
5. **Professional**: Great for showcasing AI projects

## Next Steps

1. Choose your preferred platform
2. Follow the deployment steps above
3. Test the deployed app
4. Share the public URL

The app will run in demo mode on all these platforms (since they don't include your backend), but users can still experience the full UI and see sample AI analysis results.