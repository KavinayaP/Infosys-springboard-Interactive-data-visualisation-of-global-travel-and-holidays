<<<<<<< HEAD
📌 Global Travel Insights — Dashboard + AI Voice Assistant

A complete travel analytics web application featuring interactive dashboards, real-time insights, user authentication, quizzes and a fully functional AI Chatbot + Voice Assistant (STT + TTS) powered by FastAPI + OpenAI GPT-4o.

🚀 Features
🔹 Dashboard & Insights

✔ Destination popularity
✔ Travel spending
✔ Arrivals/Departures
✔ Recovery index
✔ Data storytelling

🤖 AI Assistant

✔ Text Chat (GPT-4o-mini)
✔ Voice Chat — STT (Speech → Text)
✔ TTS (Text → Speech audio reply)
✔ Animated typing indicator
✔ Saves chat history

🔐 Authentication

✔ Register / Login / JWT Token
✔ Protected sections
✔ Auto UI updates

🔔 Notifications

✔ Toast alerts
✔ Saved history
✔ Mobile-friendly

📝 Quiz Module

✔ World travel quiz
✔ Score tracking

🏗 Tech Stack
Frontend

HTML5

Tailwind CSS

JavaScript

AOS Animations

Backend

FastAPI

SQLAlchemy

SQLite

Python 3

OpenAI API

global_app/
│
├── backend/
│   ├── main.py
│   ├── chat.py
│   ├── voice.py
│   ├── quiz.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── database.py
│   ├── app.db
|   ├── test.py
│
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboards.html
│   ├── insights.html
│   ├── feedback.html
│   ├── chatbot.html
│   └── profile.html
|
├── app.db
├── .env
├── requirements.txt
└── README.md



⚙️ Setup Instructions


1. Install dependencies
pip install -r requirements.txt

2. Create .env file
OPENAI_API_KEY=your_api_key_here

3. Run backend
uvicorn backend.main:app --reload


Backend URL:
👉 http://127.0.0.1:8000

5. Open frontend

Just open:

frontend/index.html

🎤 Voice Assistant API
Speech → Text (STT)

POST /api/voice/stt

Send audio as:

audio: file(webm)

Text → Speech (TTS)

POST /api/voice/tts

{
  "text": "Hello user"
}


🧪 Testing STT (Optional)

Place a sample file voice.webm then run:

curl -X POST -F "audio=@voice.webm" http://127.0.0.1:8000/api/voice/stt


⭐ Support

If you like this project, please ⭐ the repo!
=======
# Infosys-Springboard-Virtual-internship-_Interactive-data-visualization-of-global-travel-and-holidays
An interactive web application that visualizes global travel and holiday trends using dynamic dashboards, filters, and KPIs for data-driven insights.
>>>>>>> 2d07ad6b373d4106cc78b7d274788b47a0758724
