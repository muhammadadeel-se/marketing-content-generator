# Marketing Content Generator with Review for TaskFlow Software

A prompt-driven CLI & Web tool that generates structured marketing content based on brand voice guidelines using OpenAI AI.

## Project Overview
This project loads brand guidelines from `brand_voice.json` and uses LLM API integration to generate structured JSON copy (headline, tagline, and body) for given product descriptions. It includes both a CLI tool and a Flask-based Web Interface.

## Project Structure
```text
marketing-content-generator/
│
├── templates/
│   └── index.html          # Web UI interface built with Bootstrap
├── tests/
│   └── test_generate.py    # Unit tests for generator logic
├── app.py                  # Flask web application server
├── brand_voice.json        # Brand voice configuration
├── generate_copy.py        # Core OpenAI generator function & CLI entrypoint
├── requirements.txt        # Python dependencies
└── README.md