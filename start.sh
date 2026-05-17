#!/bin/bash
# Ailyn Construction Management - Auto Start Script

echo "🏗️ Starting Ailyn Construction Management..."

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Install requirements if needed
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# Install streamlit-pwa if not installed
pip install streamlit-pwa

# Start the app with all features enabled
streamlit run aps.py \
    --server.enableCORS false \
    --server.enableXsrfProtection false \
    --server.enableStaticServing true \
    --server.port 8501 \
    --server.address 0.0.0.0

echo "✅ App started successfully!"
echo "🌐 Access at: http://localhost:8501"
echo "📱 Offline version: http://localhost:8501/static/index.html"