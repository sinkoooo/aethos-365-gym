with open('god_level_system_design.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos_finops = text.find('id="view-finops"')
pos_ring = text.find('id="view-ring"')
print("=== CONTENT OF VIEW-FINOPS ===")
print(text[pos_finops:pos_ring])

pos_tracer = text.find('id="view-tracer"')
print("=== CONTENT OF VIEW-TRACER ===")
print(text[pos_tracer:pos_finops])
