{
    "web": {
        "client_id": "632677687643-jqh4vulu2ms50unfamh1ivspedkvdsr8.apps.googleusercontent.com",
        "project_id": "acecoder-489714",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "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",
        "redirect_uris": [
            "http://127.0.0.1:8000",
            "http://127.0.0.1:8000/accounts/google/login/callback/"
        ],
        "javascript_origins": [
            "https://acecoderbeta.onrender.com"
        ]
    }
}
