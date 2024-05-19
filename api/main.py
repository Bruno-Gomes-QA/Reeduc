import os
from app import create_app

debug_mode = os.environ.get('DEBUG', 'false').lower() == 'true'
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
