# Marketing Content Generator - TaskFlow Software

A prompt-driven CLI, Web Application, and Batch Processing tool that generates structured marketing content (Headline, Tagline, and Body Copy) based on brand voice guidelines using OpenAI API.

---

## 🛠️ Project Structure
```text
marketing-content-generator/
│
├── templates/
│   ├── index.html          # Single Product UI
│   ├── batch.html          # CSV File Upload UI
│   └── batch_results.html  # Batch Review & Export Table UI
├── tests/
│   └── test_generate.py    # Unit tests for core generator logic
├── app.py                  # Flask web application server & routes
├── brand_voice.json        # Brand voice configuration & rules
├── generate_copy.py        # Core OpenAI generator function & CLI entrypoint
├── test_products.csv       # Sample batch CSV file for testing
├── vercel.json             # Vercel deployment configuration
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation