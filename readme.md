Here’s a well-structured `README.md` for your **email summarizer desktop app using FastAPI, Gmail API, and Ollama**:

---

```markdown
# 📨 Email Summarizer Desktop App

This project is a lightweight desktop application that connects to your Gmail inbox, reads emails received **today**, extracts important details (like **sender**, **subject**, and **body**) and generates concise summaries using a **locally hosted LLM** via **Ollama**.

## 🚀 Features

- ✅ Authenticate and read today's emails from Gmail
- ✅ Automatically extract and clean email content
- ✅ Summarize multiple emails in bulk using a local LLM model (e.g. `llama3.2`)
- ✅ Built with modular Python structure and FastAPI
- ✅ Can be extended into a full desktop GUI (e.g. with Tauri or PyQt)

---

## 🧰 Tech Stack

- **Python 3.10+**
- **FastAPI** – For API backend
- **Google API Client** – To access Gmail
- **Ollama** – Locally hosted LLM inference
- **Requests** – For making POST requests to the LLM
- **Rich** (optional) – For pretty terminal outputs

---

## 📁 Project Structure

```

email-summarizer/
│
├── main.py                 # Entry point of the app
├── auth.py                 # Handles Gmail OAuth
├── gmail\_reader.py         # Reads and parses emails
├── summarizer.py           # Calls Ollama to summarize
├── app.py                  # FastAPI routes
├── requirements.txt        # Dependencies
└── README.md               # You're here!

````

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/email-summarizer.git
cd email-summarizer
````

### 2. Install Dependencies

It’s recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 3. Setup Gmail API

* Go to [Google Cloud Console](https://console.cloud.google.com/)
* Create a project → Enable **Gmail API**
* Download `credentials.json` into your project directory

The app will prompt you to authenticate when you run it the first time.

### 4. Start Ollama

Make sure Ollama is installed and running a supported model:

```bash
ollama run llama3
```

Ensure Ollama is listening at: `http://localhost:11434/api/generate`

### 5. Run the App

```bash
python main.py
```

---

## 📝 Example Output

```json
[
  {
    "from": "HR Department <hr@example.com>",
    "subject": "Team Meeting Summary",
    "summary": "A team meeting is scheduled for Monday at 10AM. Attendance is mandatory. Topics include Q3 planning and department updates."
  },
  ...
]
```

---

## 🛡️ Privacy Notice

This app runs entirely **locally**. No email content or summaries are sent to any cloud service. All LLM processing happens via Ollama on your machine.

---

## 💡 Future Enhancements

* Add a GUI with Tauri or PyQt
* Support other email providers (e.g. Outlook)
* Save summaries to file
* Schedule summaries automatically (via cron or background jobs)

---

## 📄 License

MIT License. See `LICENSE` file for details.

---

## ✨ Credits

* [FastAPI](https://fastapi.tiangolo.com/)
* [Ollama](https://ollama.com/)
* [Google API Python Client](https://github.com/googleapis/google-api-python-client)

---

```
```
