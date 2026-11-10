# Sikho Smart — Streamlit live app

## Deploy on Streamlit Community Cloud
1. Create a GitHub repository and upload `app.py` and `requirements.txt` from this folder.
2. Sign in at https://share.streamlit.io/ using GitHub.
3. Choose the repository, branch and `app.py`, then deploy.
4. Your public app will receive a `*.streamlit.app` URL.

## Optional live AI
In Streamlit Community Cloud, open app settings → Secrets and add:
```toml
OPENAI_API_KEY = "your-secret-api-key"
OPENAI_MODEL = "gpt-4.1-mini"
```
Never put API keys in the GitHub repository or front-end. Keep usage limits enabled. If no key is set, the quiz and other app sections still work.

## Current prototype limits
- 20 starter questions (5 each for Maths, English, Science and General Knowledge).
- Sindhi and Urdu translations currently cover Maths and Science; English and General Knowledge questions remain in English. The core interface is translated.
- Class selector is present but does not yet change question difficulty.
- Scores use Streamlit session state and are not a persistent school-wide student record.
- Public access is open; supervise children and do not request personal information. Basic email/phone-number input screening and a per-session chat cap are included, but these are not a substitute for adult supervision or a full safety moderation service.
