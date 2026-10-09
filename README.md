# Marketing Content Generator - TaskFlow Software

A prompt-driven CLI & Web application that generates structured marketing content (Headline, Tagline, and Body Copy) based on brand voice guidelines using OpenAI API.

---

## 🛠️ Project Structure
```text
marketing-content-generator/
│
├── templates/
│   └── index.html          # Web UI interface built with Bootstrap 5
├── tests/
│   └── test_generate.py    # Unit tests for core generator logic
├── app.py                  # Flask web application server
├── brand_voice.json        # Brand voice configuration & rules
├── generate_copy.py        # Core OpenAI generator function & CLI entrypoint
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation