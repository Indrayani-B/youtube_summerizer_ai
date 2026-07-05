# run_app.py
import streamlit.web.cli as stcli
import sys
import os

if __name__ == "__main__":
    # Clear any cached modules
    for module in list(sys.modules.keys()):
        if module.startswith('tools.') or module.startswith('agents.') or module.startswith('graph.'):
            del sys.modules[module]
    
    # Run the Streamlit app
    sys.argv = ["streamlit", "run", "streamlit_app/ui.py"]
    sys.exit(stcli.main())