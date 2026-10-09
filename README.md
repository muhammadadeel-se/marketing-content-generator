# Batch Marketing Content Generator

A Flask-based web application that generates marketing copy (Headlines, Taglines, and Body Copy) using OpenAI's API. Supports both single-product copy generation and bulk processing via CSV upload, complete with an interactive review checklist and CSV export functionality.

## Live Deployment & Submission Links

* **Live Application URL:** [https://marketing-content-generator-cor3r75rc-muhammadadeel-se.vercel.app](https://marketing-content-generator-cor3r75rc-muhammadadeel-se.vercel.app)
* **GitHub Repository:** [https://github.com/muhammadadeel-se/marketing-content-generator](https://github.com/muhammadadeel-se/marketing-content-generator)

> **Note on Hosting Platform:** The application is deployed live on Vercel (`vercel.json` configured) to bypass Render's credit card verification requirement while ensuring 100% uptime, fast response times, and full serverless execution.

---

## Features

1. **Single Product Copy Generator (`/`):**
   * Input Product Name, Key Features, and Target Audience.
   * Generates tailored Headlines, Taglines, and Body Copy.

2. **Batch CSV Processing (`/batch`):**
   * Managed via `Flask-WTF` (`BatchForm`) with file extension validation (`.csv`) and CSRF protection.
   * Accepts CSV files with columns: `Product Name`, `Key Features`, and `Target Audience`.
   * Processes each product row concurrently through the OpenAI model.

3. **Interactive Review Checklist (`/batch` results):**
   * Displays generated copy in a structured table.
   * Allows non-technical reviewers to approve or disapprove individual sections (Headline, Tagline, Body Copy) via interactive checkboxes.

4. **Reviewed Data Export (`/export`):**
   * Downloads a updated `.csv` file containing the product details, copy, and approval status for each section.

---

## Hand-over Notes for Reviewers

* **Architecture Overview:**
  * `app.py`: Route definitions (`/`, `/batch`, `/export`) and Pandas batch handling.
  * `forms.py`: Centralized WTForms schema (`BatchForm`) with `FileAllowed(['csv'])` and `FileRequired` validators.
  * `generate_copy.py`: Utility module encapsulating OpenAI API calls and structured JSON response parsing.
  * `templates/`: Bootstrap 5 UI templates (`index.html`, `batch.html`, `batch_results.html`).

* **Environment Setup:**
  * Requires `OPENAI_API_KEY` and `SECRET_KEY` set in environment variables (or `.env` file locally).

* **Local Running Instructions:**
  ```bash
  git clone [https://github.com/muhammadadeel-se/marketing-content-generator.git](https://github.com/muhammadadeel-se/marketing-content-generator.git)
  cd marketing-content-generator
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  pip install -r requirements.txt
  python app.py