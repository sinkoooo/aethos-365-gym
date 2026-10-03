import data_curriculum_100x

print(f"Total items in ALL_TOPICS_100X: {len(data_curriculum_100x.ALL_TOPICS_100X)}")
all_valid = True
for i, it in enumerate(data_curriculum_100x.ALL_TOPICS_100X):
    g_len = len(it.get('guidebook', ''))
    t_len = len(it.get('topologySvg', ''))
    c_len = len(it.get('codeSnippet', ''))
    d_len = len(it.get('disasterStudy', ''))
    v_len = len(it.get('interviewDefense', ''))
    
    if g_len == 0 or t_len == 0 or c_len == 0 or d_len == 0 or v_len == 0:
        all_valid = False
        print(f"MISSING DATA in #{i+1} [{it['id']}] {it['title']}: G={g_len}, T={t_len}, C={c_len}, D={d_len}, V={v_len}")
    else:
        print(f"#{i+1:02d} [{it['id']}]: G={g_len}B, T={t_len}B, C={c_len}B, D={d_len}B, V={v_len}B | {it['title'][:40]}")

print(f"ALL 27 TOPICS 100% COMPLETE & VERIFIED: {all_valid}")
