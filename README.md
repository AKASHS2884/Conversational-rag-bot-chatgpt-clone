# 🚀 Conversational AI Chatbot

A beautiful, memory-enabled conversational AI chatbot built with Streamlit and NVIDIA AI APIs.

![Chatbot Interface](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![NVIDIA](https://img.shields.io/badge/NVIDIA-AI-76B900?style=for-the-badge&logo=nvidia&logoColor=white)

## ✨ Features

- 🧠 **Smart Memory System** - Remembers your name, preferences, and conversation history
- 💬 **Multi-Chat Support** - Create and manage multiple conversation threads
- 📚 **Knowledge Base** - Automatically builds a searchable FAQ from your questions
- 🎨 **Beautiful UI** - Modern gradient design with smooth animations
- ⚡ **Fast Responses** - Powered by NVIDIA's Llama 3.3 Nemotron model
- 🔄 **Fallback System** - Intelligent offline responses when API is unavailable

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI Model**: NVIDIA Llama 3.3 Nemotron Super 49B
- **Language**: Python 3.8+
- **APIs**: OpenAI-compatible NVIDIA API

## 📋 Prerequisites

- Python 3.8 or higher
- NVIDIA API key (Get it from [NVIDIA AI](https://build.nvidia.com/))
- Git installed on your system

## 🚀 Installation & Setup

### 1. Clone the repository
git clone https://github.com/AKASHS2884/Conversational-rag-bot-chatgpt-clone.git
cd conversational-ai-chatbot

text

### 2. Create a virtual environment (recommended)
Windows
python -m venv venv
venv\Scripts\activate

Mac/Linux
python3 -m venv venv
source venv/bin/activate

text

### 3. Install dependencies
pip install -r requirements.txt

text

### 4. Set up environment variables
Copy the example env file
cp .env.example .env

Edit .env and add your NVIDIA API key
OPENAI_API_KEY=your_actual_nvidia_api_key_here
text

### 5. Run the application
streamlit run app.py

text

The app will open in your browser at `http://localhost:8501`

## 🔑 Getting Your API Key

1. Visit [NVIDIA AI Catalog](https://build.nvidia.com/)
2. Sign up or log in
3. Navigate to the API section
4. Generate your API key
5. Copy it to your `.env` file

## 📁 Project Structure

conversational-ai-chatbot/
├── app.py # Main application file
├── .env # Environment variables (not in repo)
├── .env.example # Example env file (safe to share)
├── .gitignore # Git ignore rules
├── requirements.txt # Python dependencies
└── README.md # This file

text

## 🎯 Usage

1. **Start a conversation** - Type your message in the chat input
2. **Introduce yourself** - Say "My name is [Your Name]" to personalize your experience
3. **Ask questions** - Your Q&A pairs are saved for quick retrieval
4. **Create new chats** - Click "✨ New Conversation" to start fresh
5. **View memory** - Check the sidebar to see what the AI remembers

## 🧠 Memory Features

The chatbot remembers:
- Your name and title
- Location information
- Previous Q&A pairs (last 20)
- Conversation history across multiple chats

## 🔒 Security Best Practices

- ✅ Never commit `.env` files to GitHub
- ✅ Use `.env.example` as a template
- ✅ Keep your API keys private
- ✅ Regenerate keys if accidentally exposed
- ✅ Use `.gitignore` to prevent sensitive file uploads

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Akash Subramani**
- GitHub: [@akashsubramani](https://github.com/akashsubramani)
- LinkedIn: [Akash Subramani](https://linkedin.com/in/akashsubramani)

## 🙏 Acknowledgments

- NVIDIA for their powerful AI APIs
- Streamlit for the amazing framework
- OpenAI for API compatibility

## 📞 Support

If you encounter any issues or have questions:
1. Check existing [Issues](https://github.com/AKASHS2884/Conversational-rag-bot-chatgpt-clone.git)
2. Create a new issue with detailed information
3. Reach out via LinkedIn

## 🔮 Future Enhancements

- [ ] Voice input/output
- [ ] Multi-language support
- [ ] Export conversation history
- [ ] Custom AI personality settings
- [ ] Image generation support
- [ ] File upload and analysis

---

⭐ If you found this project helpful, please give it a star!
