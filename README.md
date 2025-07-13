# Aureus Engine

**Aureus Engine** is a modular, predictive crafting analysis tool built with Streamlit. It analyzes material sequences and predicts future crafting outcomes using pattern recognition, confidence scoring, and optional user-defined patterns.

---

## 🔍 Features

- 🧠 Pattern tracking and confidence-based prediction
- 🧩 User-submitted pattern storage with Firebase integration
- 📊 Gear-type and material-distribution aware prediction logic
- 💾 Session persistence with cloud sync via Firebase
- 🎛️ Modular Streamlit UI for real-time interaction

---

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io)
- **Backend**: Python (modular architecture)
- **Database**: Firebase Realtime Database
- **Auth/Secrets**: Streamlit Cloud Secrets Management

---

## 🚀 How to Run Locally

1. Clone the repo:
   ```bash
   git clone https://github.com/AureusEngine/AureusEngine.git
   cd AureusEngine
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Add your Firebase credentials:
   - Place `firebase_credentials.json` in the root directory
   - Or configure via `.streamlit/secrets.toml` for cloud deployment

4. Run the app:
   ```bash
   streamlit run main.py
   ```

---

## ☁️ Streamlit Cloud Deployment

1. Push your code to GitHub
2. Create a `.streamlit/secrets.toml` with your Firebase config:
   ```toml
   [firebase]
   type = "service_account"
   project_id = "aureusengine-433eb"
   private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
   ...
   ```
3. Deploy at [streamlit.io/cloud](https://streamlit.io/cloud)

---

## 🧠 Prediction Engine

The `predict_next_outcome()` function analyzes crafting history and pattern confidence to recommend the most likely next result, using both system-detected and user-defined patterns.

---

## 🔒 Security

Sensitive credentials (like `firebase_credentials.json`) are excluded via `.gitignore` and should never be committed to source control.

---

## 📁 Project Structure

- `main.py` – Streamlit entry point
- `modules/` – All core logic (prediction, pattern tracking, firebase, UI)
- `.streamlit/secrets.toml` – Secure secrets for Streamlit Cloud
- `requirements.txt` – All dependencies

---

## 📬 License

This project is in public beta. All rights reserved by AureusEngine™.