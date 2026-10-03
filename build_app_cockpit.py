# build_app_cockpit.py
# Primary Cockpit OS Compiler - Delegates to build_cockpit_100x

from build_cockpit_100x import build_cockpit_100x

def build_cockpit_app():
    build_cockpit_100x()

if __name__ == "__main__":
    build_cockpit_app()
