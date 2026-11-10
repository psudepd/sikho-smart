# Sikho Smart — Streamlit Website + Android APK source package

## Included
- `streamlit_app/`: deployable Streamlit app source, requirements and app-specific instructions.
- `android_wrapper/SikhoSmartAndroid/`: Android Studio project source that wraps the final Streamlit HTTPS URL.
- This package is not yet a live website or a compiled APK. Publishing needs your GitHub/Streamlit account; APK build needs the final website URL and Android Studio build/signing.

## 1. Publish the website
1. Create a GitHub repository named `sikho-smart`.
2. Upload the *contents* of `streamlit_app/` to the repository root (`app.py`, `requirements.txt`, `README.md`).
3. Sign in at https://share.streamlit.io/ with GitHub and choose Create app.
4. Select the repository, branch `main`, and entrypoint `app.py`; choose a simple public subdomain such as `sikho-smart-phuleli` if available.
5. Deploy and test the resulting `https://....streamlit.app` URL on phone and desktop.
6. Optional AI: in app settings → Secrets, add `OPENAI_API_KEY = "..."` and `OPENAI_MODEL = "gpt-4.1-mini"`. Keep keys out of GitHub. Set provider spending limits.

Official deployment instructions: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app

## 2. Build Android APK
1. Install Android Studio and Android SDK Platform 35.
2. Open `android_wrapper/SikhoSmartAndroid` in Android Studio.
3. Replace the placeholder URL in `MainActivity.kt` with the actual deployed Streamlit URL.
4. Wait for Gradle sync.
5. Use Build → Build Bundle(s) / APK(s) → Build APK(s) for a test APK.
6. For distribution, use Build → Generate Signed Bundle / APK and create a signed release APK.
7. Test the APK on several Android devices. Share only after confirming the URL, AI safety settings and app operation.

## Current features
- Mobile-friendly, child-friendly Streamlit layout.
- English / Sindhi / Urdu interface.
- Maths, English, Science and General Knowledge quizzes.
- Hints, explanations, stars, points and quiz progress.
- Sikho Dost chat integration using server-side API secrets.
- Teacher information tab and privacy reminders.
- Open public access; no child account or personal record collection.

## Current prototype limitations
- 20 starter questions (5 per subject).
- Sindhi and Urdu translations currently cover Maths and Science; English and General Knowledge questions remain English, although the main interface is translated.
- Class selector is present but questions are not yet differentiated by class difficulty.
- Progress is held in Streamlit session state, not a central persistent school database.
- AI chat is optional and requires a valid API key, internet, usage controls and adult supervision.
- Basic screening for obvious phone numbers/email addresses and a per-session chat cap are included, not a full moderation solution.
- APK is an online WebView wrapper and needs internet. It is not an offline APK.

## School launch checklist
- [ ] Confirm school permission and teacher supervision.
- [ ] Review translations and age appropriateness with teachers.
- [ ] Test all quiz answers in each supported language.
- [ ] Deploy website and test URL.
- [ ] Configure API secret only if live AI is approved.
- [ ] Build, sign and test APK.
- [ ] Generate QR code only after final URL is verified.
- [ ] Tell children not to share personal information and that AI can make mistakes.
