import os
import shutil

# Paths
dest_workspace = r"d:\Antigravity\Shivam_Staff_Engineer_Mastery_Roadmap.html"
dest_brain = r"C:\Users\shiva\.gemini\antigravity\brain\623354e4-df8d-442a-a628-1971c1a87479\Shivam_Staff_Engineer_Mastery_Roadmap.html"

# Read existing file
with open(dest_workspace, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Remove the HERO / MISSION BRIEF section completely
# It begins with <!-- HERO / MISSION BRIEF --> and ends before <!-- ========================================================================= --> <!-- CHAPTER 1
hero_start = text.find("<!-- HERO / MISSION BRIEF -->")
if hero_start != -1:
    hero_end = text.find("<!-- ========================================================================= -->\n      <!-- CHAPTER 1", hero_start)
    if hero_end != -1:
        text = text[:hero_start] + text[hero_end:]
        print("Successfully removed HERO / MISSION BRIEF section.")
    else:
        print("Hero end marker not found.")
else:
    print("Hero start marker not found.")

# Write updated file
with open(dest_workspace, "w", encoding="utf-8") as f:
    f.write(text)

shutil.copy2(dest_workspace, dest_brain)
print("Updated workspace and brain copies cleanly.")
