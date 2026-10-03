with open('god_level_system_design.html', 'r', encoding='utf-8') as f:
    html = f.read()

checks = [
    'id="cost-dau"',
    'id="architecture-tracer-svg"',
    'id="live-rl-terminal"',
    'id="pipe-active"',
    'id="trace-packet-dot"',
    'id="live-hash-ring-svg"',
    'id="studio-timer-display"'
]
for c in checks:
    print(c, '->', c in html)
