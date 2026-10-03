import re

with open("d:/Antigravity/generate_full_cockpit_html.py", encoding="utf-8") as f:
    code = f.read()

print("Search for whiteboard functions:")
for m in re.finditer(r"function\s+([a-zA-Z0-9_]+)\s*\([^)]*\)", code):
    name = m.group(1)
    if any(k in name.lower() for k in ["whiteboard", "canvas", "topology", "split", "stencil"]):
        print("  - Function:", name)

# Check whiteboard modal and split studio HTML
print("\nHTML elements for whiteboard:")
for m in re.finditer(r"id=['\"]([^'\"]*(?:whiteboard|canvas|split)[^'\"]*)['\"]", code, re.IGNORECASE):
    print("  - ID:", m.group(1))
