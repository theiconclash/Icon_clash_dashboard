# Icon Clash Arena

A Python-based interactive particle simulation where each particle represents a player. Particles move around, collide, and lose health based on collision force. The last particle alive wins!

## 🎮 Features

- **Particle Battle Simulation**: Instagram followers battle it out in a physics-based arena
- **Interactive Dashboard**: Streamlit web app with battle statistics and leaderboards
- **Real-time Analytics**: Track kills, damage, and battle outcomes
- **Beautiful Visuals**: Neon effects and smooth animations

## 🚀 Deployment

### Local Development
1. Run simulation: `python simulation.py`
2. Start dashboard: `streamlit run streamlit_app2.py`

### Streamlit Cloud Deployment
1. Upload these files to GitHub:
   - `streamlit_app2.py`
   - `requirements.txt`
   - `data/daily_stats.db`
   - `config.yaml`
   - `README.md`
   - `.gitignore`

2. Connect your GitHub repo to Streamlit Cloud
3. Deploy and enjoy!

## 📊 Data Management

- **Simulation**: Run locally to generate battle data
- **Database**: Manually update `data/daily_stats.db` with new results
- **Dashboard**: Automatically displays latest battle statistics

## 🔧 Configuration

Edit `config.yaml` to customize:
- Screen dimensions
- Particle properties
- Battle parameters 
