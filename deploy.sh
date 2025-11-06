#!/bin/bash
cd /home/mauayala/apps/SifenConnect
echo "🚀 Haciendo pull del repo..."
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart fastapi
echo "✅ Deploy completado."
