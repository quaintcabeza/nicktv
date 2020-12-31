import os

bind = f"0.0.0.0:{os.environ.get('APP_PORT', 5000)}"
workers = 4

if os.environ.get('APP_ENV') == 'dev':
    reload = True
