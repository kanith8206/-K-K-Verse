<div align="center">
  <img width="1200" height="475" alt="GHBanner" src="https://ai.google.dev/static/site-assets/images/share-ais-513315318.png" style="border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.2);" />

  <br />
  <br />

  <h1>🌌 KKVerse AI Platform</h1>
  <p><b>Next-Generation Cognitive Business Intelligence & Analytics</b></p>
  
  <p>
    <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.9+-blue.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python" /></a>
    <a href="https://nicegui.io"><img src="https://img.shields.io/badge/NiceGUI-UI%20Framework-orange.svg?style=for-the-badge&logo=fastapi&logoColor=white" alt="NiceGUI" /></a>
    <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-Backend-009688.svg?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" /></a>
    <a href="https://ai.google.dev/"><img src="https://img.shields.io/badge/Google%20Gemini-AI%20Engine-8E75B2.svg?style=for-the-badge&logo=google&logoColor=white" alt="Gemini" /></a>
  </p>
</div>

<hr />

## ✨ About KKVerse AI

**KKVerse AI** is an enterprise-grade, full-stack Business Intelligence dashboard powered by Google's **Gemini AI Neural Engine**. Designed to replace traditional static dashboards, KKVerse brings cognitive capabilities to your fingertips—from predicting customer churn and forecasting future sales, to having dynamic conversations with your very own AI Copilot about your business data.

Whether you're tracking daily sales volume or planning long-term inventory growth, KKVerse gives you the tools to make data-driven decisions effortlessly.

<br />

## 🚀 Key Features

| Feature | Description |
| :--- | :--- |
| 📊 **Real-time Dashboard** | Overview of your business with dynamic KPI cards, calculating total revenue, profit margins, and active products. |
| 🤖 **AI Copilot** | Your personal business assistant. Ask questions in plain English about your data and receive instant, cognitive insights powered by Gemini 3.5. |
| 🔮 **Sales Forecasting** | Machine Learning projections for future sales trends based on historical aggregate data. |
| 👥 **Customer Analytics** | Track Customer Lifetime Value (CLV), monthly spend, and customer acquisition dates. |
| ⚠️ **Churn Prediction** | Identify at-risk customers with predictive retention scores before they leave. |
| 📦 **Inventory Management** | Monitor stock levels, track "Out of Stock" or "Low Stock" alerts, and optimize supply chain operations. |
| 📑 **Interactive Reports** | Generate beautiful, exportable multi-dimensional business reports on the fly. |

<br />

## 🛠️ Technology Stack

KKVerse AI is built to be blindingly fast, completely asynchronous, and visually stunning.

- **Frontend & UI:** [NiceGUI](https://nicegui.io/) (A Python-based UI framework built on Vue.js & Tailwind CSS)
- **Backend Server:** [FastAPI](https://fastapi.tiangolo.com/) & Uvicorn
- **Artificial Intelligence:** Google Gemini Pro API (via `google-generativeai`)
- **Styling:** Custom CSS & Tailwind integration with Glassmorphism themes
- **Environment:** Node.js (for runner scripts) & Python 3.9+

<br />

## ⚙️ Getting Started

Follow these steps to deploy KKVerse AI locally on your machine.

### Prerequisites
- Python 3.9 or higher
- Node.js (Optional, used for `npm run dev` scripts)
- A Google Gemini API Key. Get one for free at [Google AI Studio](https://aistudio.google.com/).

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kanith8206/-K-K-Verse.git
   cd -K-K-Verse
   ```

2. **Create and activate a virtual environment (Recommended):**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your Environment:**
   - Copy the `.env.example` file to `.env` or `.env.local`.
   - Add your Google Gemini API Key:
   ```env
   GEMINI_API_KEY="your_api_key_here"
   PORT=3000
   ```

### Running the App

You can run the application directly through Python or via npm:

**Option 1 (Python):**
```bash
python server.py
```

**Option 2 (NPM):**
```bash
npm run dev
```

Open your browser and navigate to **[http://localhost:3000](http://localhost:3000)** to view the platform!

<br />

## 💡 How to Use the AI Copilot

Once logged into the dashboard, navigate to the **Copilot** tab. The AI context window is automatically injected with your current metrics (Total Revenue, Active Customers, Stock Levels). 

Try asking:
- *"Which of my products is running low on stock?"*
- *"Give me a summary of my profit margins for this month."*
- *"Which customers are at the highest risk of churning?"*

<br />

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/kanith8206/-K-K-Verse/issues).

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<br />

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

<hr />
<div align="center">
  <sub>Built with ❤️ for cognitive business empowerment.</sub>
</div>
