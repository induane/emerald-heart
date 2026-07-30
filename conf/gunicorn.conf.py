workers = 2
theads = 16
bind = "unix:/var/run/gunicorn/gunicorn.sock"
secure_scheme_headers = {"X-FORWARDED-PROTOCOL": "http", "X-FORWARDED-PROTO": "https", "X-FORWARDED-SSL": "off"}
