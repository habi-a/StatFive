"""Main Module"""

from src.launcher import create_app

if __name__ == '__main__':
    app = create_app('docker')
    app.run(host='0.0.0.0')
