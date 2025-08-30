# Mood Journal - AI-Powered Emotion Tracker

A simple yet powerful mood tracking application that helps young people and young adults monitor their emotional well-being through journaling and AI-powered sentiment analysis.

## 🌟 Features

- **Daily Journaling**: Write and save your thoughts and feelings each day
- **AI Emotion Analysis**: Automatically detects emotions in your entries using Hugging Face's sentiment analysis API
- **Visual Trends**: View your mood patterns over time with interactive charts
- **Privacy-Focused**: Your journal entries are stored securely in your personal database
- **Simple Interface**: Clean, intuitive design that's easy to use

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (with Chart.js for visualizations)
- **Backend**: Python with Flask framework
- **Database**: MySQL for data storage
- **AI**: Hugging Face Sentiment Analysis API (no machine learning coding required)

## 📋 How It Works

1. **Write**: Enter your journal entry through the simple web form
2. **Analyze**: Our system sends your text to the Hugging Face API for emotion detection
3. **Store**: Your entry and emotion scores are saved in your personal MySQL database
4. **Visualize**: View your emotional trends over time through interactive charts

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- MySQL Server
- Hugging Face API account (free)

## 📊 Database Schema

The application uses a simple database structure:

- **users**: User information (id, username, created_at)
- **entries**: Journal entries (id, user_id, content, created_at)
- **emotions**: Emotion scores linked to entries (id, entry_id, emotion, score)

## 🎯 Learning Benefits

This project is perfect for beginners because it:

1. **Teaches Full CRUD Operations**: Create, Read, Update, and Delete database entries
2. **Uses API Integration**: Learn how to work with external APIs without complex AI math
3. **Provides Visual Feedback**: Instant gratification through charts and visualizations
4. **Covers Full-Stack Development**: Frontend, backend, and database integration

## 🔧 API Endpoints

- `GET /` - Home page with journal form
- `POST /entry` - Save a new journal entry
- `GET /entries` - Retrieve all journal entries
- `GET /stats` - Get emotion statistics for charting

## 📈 Emotion Detection

The application uses Hugging Face's sentiment analysis model to detect:

- Joy 😊
- Sadness 😢
- Anger 😠
- Fear 😨
- Surprise 😲
- Love ❤️

Each entry receives a score for these emotions, allowing you to track your emotional patterns over time.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [Hugging Face](https://huggingface.co/) for providing the sentiment analysis API
- [Chart.js](https://www.chartjs.org/) for the visualization library
- [Flask](https://flask.palletsprojects.com/) for the web framework

---

**Note**: This application is designed for educational purposes and personal use. It is not intended to replace professional mental health advice or treatment.
