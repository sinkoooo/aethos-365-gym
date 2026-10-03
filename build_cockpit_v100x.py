# build_cockpit_v100x.py
# Compiles the 100x Enhanced Google Staff & Principal Engineering Cockpit
# Includes all 14 user enhancement requests

import os
import shutil
import json
import modules_data
import system_design_data
import learning_resources_data
import modules_tech
import interactive_stages_data

print("Starting 100x Cockpit Compilation...")
print(f"Loaded {len(modules_data.MODULES_LIST)} technical modules.")
print(f"Loaded {len(system_design_data.SYSTEM_DESIGNS)} system design blueprints.")
print(f"Loaded {len(learning_resources_data.RESOURCES_DATA)} learning resource suites.")
print(f"Loaded {len(modules_tech.MODULES)} deep tech specifications.")
