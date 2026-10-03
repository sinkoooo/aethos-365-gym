import re

with open("d:/Antigravity/generate_full_cockpit_html.py", encoding="utf-8") as f:
    text = f.read()

modals = re.findall(r'id=["\']([a-zA-Z0-9_-]*modal[a-zA-Z0-9_-]*)["\']', text)
print("Modals found in generator:", sorted(set(modals)))

funcs = re.findall(r'function\s+([a-zA-Z0-9_]*Modal[a-zA-Z0-9_]*)\s*\(', text)
print("Modal functions found:", sorted(set(funcs)))
