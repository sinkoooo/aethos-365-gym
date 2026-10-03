with open('god_level_system_design.html', 'r', encoding='utf-8') as f:
    text = f.read()

for v in ['view-reader', 'view-tracer', 'view-finops', 'view-ring', 'view-limiter', 'view-interview']:
    pos = text.find('id="' + v + '"')
    print(v, 'position:', pos)
    if pos != -1:
        chunk = text[pos:pos+300]
        print('   ', repr(chunk[:100]))

# Check if tab-tracer, tab-capacity-cost exist
print("\nChecking simulator containers:")
for s in ['tab-tracer', 'tab-capacity-cost', 'tab-hash-ring', 'tab-rate-limiter', 'tab-interview-studio']:
    print(s, 'found:', s in text)

# Check sidebar items list
print("\nChecking sidebar items in text:")
print('sidebar-items-list found:', 'sidebar-items-list' in text)
print('NAV_ITEMS length in script:', text.count('"stageId":'))
