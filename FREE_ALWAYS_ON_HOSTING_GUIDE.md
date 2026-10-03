# 🌐 Free 24/7 "Always-On" Cloud Hosting Guide

This guide will walk you through hosting your **Aethos 365 Gym Platform** for **100% free** on a cloud server that stays **active 24/7 (never sleeps)**.

---

## 🚀 Recommended Architecture: Render.com + UptimeRobot (Free Forever)

- **Cloud Host**: [Render.com](https://render.com) (Free Web Service)
- **Always-On Pinger**: [UptimeRobot.com](https://uptimerobot.com) (Free 5-min health pings to prevent sleep)
- **Database / Storage**: Built-in multi-tenant user storage with automatic state isolation.

---

### Step 1: Create a GitHub Repository

1. Initialize git and commit your project (in `d:\Antigravity`):
   ```bash
   git init
   git add .
   git commit -m "feat: multi-tenant aethos 365 gym platform"
   ```
2. Create a new repository on [GitHub](https://github.com/new) (e.g. `aethos-gym-app`).
3. Push your code:
   ```bash
   git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/aethos-gym-app.git
   git branch -M main
   git push -u origin main
   ```

---

### Step 2: Deploy to Render for Free

1. Go to [Render.com](https://dashboard.render.com/) and sign up / log in with your GitHub account.
2. Click **New +** $\rightarrow$ **Web Service**.
3. Select your repository `aethos-gym-app` and click **Connect**.
4. Configure the service settings:
   - **Name**: `aethos-gym` (or any custom name)
   - **Region**: Closest to you (e.g., Singapore, Frankfurt, or Oregon)
   - **Branch**: `main`
   - **Runtime**: `Node`
   - **Build Command**: `npm install`
   - **Start Command**: `node server.mjs`
   - **Instance Type**: **Free** ($0 / month)
5. Click **Deploy Web Service**.
6. In ~1–2 minutes, Render will provide your public URL:
   `https://aethos-gym.onrender.com`

---

### Step 3: Keep It Always On (Prevent Sleep Mode)

Render's free tier enters sleep mode after 15 minutes of inactivity. To make it **permanently stay awake 24/7**:

1. Sign up for free at [UptimeRobot.com](https://uptimerobot.com/) (or [cron-job.org](https://cron-job.org/)).
2. Click **+ Add New Monitor**:
   - **Monitor Type**: `HTTP(s)`
   - **Friendly Name**: `Aethos 365 Gym Ping`
   - **URL (or IP)**: `https://<YOUR-RENDER-APP-NAME>.onrender.com/api/health`
   - **Monitoring Interval**: Every `5 minutes`
3. Click **Create Monitor**.

🎉 **Result:** UptimeRobot pings your `/api/health` endpoint every 5 minutes. Render detects continuous traffic and **never sleeps**, ensuring instant loads for you and your trainees 24 hours a day, 365 days a year!

---

## 👥 How User Profiles & Isolation Work

1. **Default Head Coach (Admin) Account:**
   - **Username**: `admin`
   - **Password**: `admin123`
   - *Note: You can change the password or register your personal username first.*
   - All your existing Day 5 workout logs, sets, and progress photos are automatically linked to this account.

2. **New Trainee Registration:**
   - Send your public URL `https://<your-app>.onrender.com` to anyone.
   - When a new trainee opens the link, they click the top profile pill or `🏆 Leaderboard` $\rightarrow$ **Create Profile**.
   - They choose their Username, Password, Display Name, and Avatar (⚡, 🦁, 🥋, 🦅, 🔥, etc.).
   - **100% Data Isolation:** Their workouts, sets, and body logs are saved in their own private user file. They **cannot** view your photos, weights, or notes, and other trainees cannot view theirs.

3. **🏆 Community Leaderboard:**
   - Accessible by clicking `🏆 Leaderboard` in the top bar.
   - Shows public ranking (Gold 🥇, Silver 🥈, Bronze 🥉), Levels, Streaks, Workouts Completed, and Total XP.
   - Personal photos and private body metrics are strictly omitted from the leaderboard.

4. **🛡️ Head Coach Admin Cockpit:**
   - Log in as `admin`.
   - The top navigation displays the `🛡️ Admin` button.
   - Clicking it opens the **Admin Oversight Cockpit**:
     - View all registered trainees in one table.
     - View total workouts, current active day, and last active date.
