# Sikho Smart Android APK project

This is a native Android WebView shell that loads the deployed HTTPS Streamlit app. It is source code, not a compiled APK. The final APK requires the real deployed URL and Android Studio/SDK.

## Build on Windows / Mac / Linux
1. Install Android Studio and Android SDK Platform 35.
2. Open this `SikhoSmartAndroid` folder in Android Studio.
3. Wait for Gradle sync to complete.
4. Deploy the Streamlit app first and copy its real URL, for example `https://your-app.streamlit.app`.
5. In `app/src/main/java/pk/edu/sikhosmart/learning/MainActivity.kt`, replace `https://YOUR-STREAMLIT-APP.streamlit.app` with the real URL.
6. Build → Build Bundle(s) / APK(s) → Build APK(s).
7. Android Studio creates a debug APK. For a public release, use Build → Generate Signed Bundle / APK and create a release keystore. Keep that keystore and password safe.
8. Install the APK on a test phone and verify login-free public access, chat, navigation, and back button.

The APK needs internet because the Streamlit app is hosted online. It is a wrapper, not a separate offline copy of the quiz.
