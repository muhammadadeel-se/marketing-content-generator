# Marketing Content Generator with Review for TaskFlow Software

A reusable, prompt-driven CLI tool that generates structured marketing content based on brand voice guidelines using AI.

## Project Overview
This project loads brand guidelines from `brand_voice.json` and uses LLM API integration to generate structured JSON copy (headline, tagline, and body) for given product descriptions.

## Project Structure
```text
marketing-content-generator/
├── .env                  # Environment variables (API Key - ignored by Git)
├── .gitignore            # Git ignore configuration
├── brand_voice.json      # Brand guidelines and style configuration
├── generate_copy.py      # Main CLI generator script
├── tests/
│   └── test_generate.py # Pytest suite with 3 sample product tests
└── README.md             # Project documentation