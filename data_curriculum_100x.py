# data_curriculum_100x.py
# Aggregates all 6 Stages (15 Chapters) + 12 Master Blueprints (27 Total Premier Topics)
# Every single topic provides all 5 Dimensions:
# 1. guidebook (Deep first principles, formulas, hardware physics)
# 2. topologySvg (Vector SVG component schematic)
# 3. codeSnippet (Production code implementation)
# 4. disasterStudy (Real production outage post-mortem)
# 5. interviewDefense (FAANG Staff trap question & verbal script)
# 6. simulatorKey (Matching interactive simulator key: tracer, finops, ring, limiter, interview)

import curriculum_stage1_data
import curriculum_stage2_data
import curriculum_stage3_data
import curriculum_stage4_data
import curriculum_stage5_data
import curriculum_stage6_data
import curriculum_blueprints_data

STAGE_METADATA = [
    {
        "id": "stage-1",
        "num": "STAGE 01",
        "title": "Day 1 Beginner: Foundations of Web & Servers",
        "badge": "Day 1 Scratch",
        "color": "emerald",
        "chapters": curriculum_stage1_data.STAGE_1_CHAPTERS,
    },
    {
        "id": "stage-2",
        "num": "STAGE 02",
        "title": "Junior to Mid: Horizontal Scalability & Data Layers",
        "badge": "Junior / Mid",
        "color": "cyan",
        "chapters": curriculum_stage2_data.STAGE_2_CHAPTERS,
    },
    {
        "id": "stage-3",
        "num": "STAGE 03",
        "title": "Senior Engineer: Distributed Sharding & Event Streaming",
        "badge": "Senior Engineer",
        "color": "indigo",
        "chapters": curriculum_stage3_data.STAGE_3_CHAPTERS,
    },
    {
        "id": "stage-4",
        "num": "STAGE 04",
        "title": "Senior to Staff: Consistency Models & Transactions",
        "badge": "Senior / Staff",
        "color": "amber",
        "chapters": curriculum_stage4_data.STAGE_4_CHAPTERS,
    },
    {
        "id": "stage-5",
        "num": "STAGE 05",
        "title": "Staff Principal: Consensus Protocols & High Availability",
        "badge": "Staff Principal",
        "color": "rose",
        "chapters": curriculum_stage5_data.STAGE_5_CHAPTERS,
    },
    {
        "id": "stage-6",
        "num": "STAGE 06",
        "title": "God-Level Architect: Low-Latency Physics & Planet-Scale",
        "badge": "God Level",
        "color": "fuchsia",
        "chapters": curriculum_stage6_data.STAGE_6_CHAPTERS,
    },
]

ALL_TOPICS_100X = []

# Add all 15 stage chapters
for s in STAGE_METADATA:
    for ch in s["chapters"]:
        item = dict(ch)
        item["type"] = "chapter"
        ALL_TOPICS_100X.append(item)

# Add all 12 Master Blueprints
for bp in curriculum_blueprints_data.BLUEPRINT_CHAPTERS:
    item = dict(bp)
    item["type"] = "blueprint"
    ALL_TOPICS_100X.append(item)

print(f"Total 100x Enhanced Topics loaded: {len(ALL_TOPICS_100X)} (15 Curriculum Chapters + 12 Blueprints)")
