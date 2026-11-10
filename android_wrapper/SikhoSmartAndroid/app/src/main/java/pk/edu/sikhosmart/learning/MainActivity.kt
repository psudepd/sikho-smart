package pk.edu.sikhosmart.learning

import android.annotation.SuppressLint
import android.graphics.Color
import android.os.Bundle
import android.view.Gravity
import android.view.View
import android.view.WindowManager
import android.webkit.CookieManager
import android.webkit.WebChromeClient
import android.webkit.WebResourceError
import android.webkit.WebResourceRequest
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.LinearLayout
import android.widget.ProgressBar
import android.widget.TextView
import androidx.activity.OnBackPressedCallback
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {

    // 🔴 IMPORTANT: Replace this with your real deployed Streamlit URL.
    // Example: "https://sikho-smart.streamlit.app"
    private val appUrl = "https://YOUR-STREAMLIT-APP.streamlit.app"

    private lateinit var webView: WebView
    private lateinit var progress: ProgressBar
    private lateinit var root: LinearLayout

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        window.statusBarColor = Color.rgb(50, 21, 109)
        window.navigationBarColor = Color.rgb(36, 16, 77)
        window.setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_ADJUST_RESIZE)

        root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setBackgroundColor(Color.rgb(250, 250, 255))
        }

        progress = ProgressBar(this, null, android.R.attr.progressBarStyleHorizontal).apply {
            max = 100
            visibility = View.VISIBLE
        }

        webView = WebView(this).apply {
            // JavaScript + storage
            settings.javaScriptEnabled = true
            settings.domStorageEnabled = true
            settings.databaseEnabled = true
            settings.loadsImagesAutomatically = true
            settings.javaScriptCanOpenWindowsAutomatically = false

            // Security
            settings.allowFileAccess = false
            settings.allowContentAccess = false
            settings.mixedContentMode = WebSettings.MIXED_CONTENT_NEVER_ALLOW
            // Cleartext HTTP is blocked via AndroidManifest (android:usesCleartextTraffic="false").
            // There is no WebSettings.usesCleartextTraffic property.

            // UX — Streamlit is already responsive; disable zoom to avoid layout issues
            settings.setSupportZoom(false)
            settings.builtInZoomControls = false
            settings.displayZoomControls = false

            // Cache + media
            settings.cacheMode = WebSettings.LOAD_DEFAULT
            settings.mediaPlaybackRequiresUserGesture = false

            // Identify the wrapper in server logs
            settings.userAgentString = settings.userAgentString + " SikhoSmartAndroid/1.0"

            webViewClient = object : WebViewClient() {
                override fun shouldOverrideUrlLoading(
                    view: WebView?,
                    request: WebResourceRequest?
                ): Boolean {
                    val url = request?.url ?: return false
                    // Allow HTTPS inside the WebView; block http, intent://, tel://, mailto:// etc.
                    return url.scheme != "https"
                }

                override fun onReceivedError(
                    view: WebView?,
                    request: WebResourceRequest?,
                    error: WebResourceError?
                ) {
                    if (request?.isForMainFrame == true) {
                        view?.loadDataWithBaseURL(
                            null,
                            """
                            <html><body style="font-family:sans-serif;text-align:center;padding:40px;color:#312e81;">
                              <h2>📶 No Internet</h2>
                              <p>Please connect to the internet and try again.</p>
                              <p><small>Sikho Smart needs internet to load lessons.</small></p>
                            </body></html>
                            """.trimIndent(),
                            "text/html", "UTF-8", null
                        )
                    }
                }
            }

            webChromeClient = object : WebChromeClient() {
                override fun onProgressChanged(view: WebView?, newProgress: Int) {
                    progress.progress = newProgress
                    progress.visibility = if (newProgress >= 100) View.GONE else View.VISIBLE
                }
            }
        }

        // Enable third-party cookies (needed by Streamlit's session handshake)
        CookieManager.getInstance().apply {
            setAcceptCookie(true)
            setAcceptThirdPartyCookies(webView, true)
        }

        root.addView(
            progress,
            LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, 5)
        )
        root.addView(
            webView,
            LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, 0, 1f)
        )
        setContentView(root)

        // Modern back-navigation handling
        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                if (::webView.isInitialized && webView.canGoBack()) {
                    webView.goBack()
                } else {
                    isEnabled = false
                    onBackPressedDispatcher.onBackPressed()
                }
            }
        })

        // If the URL is still a placeholder, show a friendly notice instead of a blank WebView
        if (appUrl.contains("YOUR-STREAMLIT-APP")) {
            showPlaceholderNotice()
        } else {
            // Restore state after process death; fall back to loading the URL
            savedInstanceState?.let {
                if (webView.restoreState(it) == null) {
                    webView.loadUrl(appUrl)
                }
            } ?: run {
                webView.loadUrl(appUrl)
            }
        }
    }

    private fun showPlaceholderNotice() {
        val notice = TextView(this).apply {
            text = "Sikho Smart\n\n" +
                "Set your deployed Streamlit URL in MainActivity.kt " +
                "(appUrl variable), then rebuild the APK."
            textSize = 20f
            gravity = Gravity.CENTER
            setTextColor(Color.rgb(49, 46, 129))
            setPadding(48, 48, 48, 48)
        }
        root.removeView(webView)
        root.addView(
            notice,
            LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT, 0, 1f)
        )
    }

    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        if (::webView.isInitialized) webView.saveState(outState)
    }

    override fun onDestroy() {
        if (::webView.isInitialized) {
            webView.stopLoading()
            webView.destroy()
        }
        super.onDestroy()
    }
}