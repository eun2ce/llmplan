import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ==== 설정 ====
ACTIONS_JSON = "results/1921c65e-38c4-4aec-a298-f7d8a8635197/1921c65e-38c4-4aec-a298-f7d8a8635197_actions.json"
OUTPUT_DIR = Path("coord_test_outputs")
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

try:
    FONT = ImageFont.truetype("arial.ttf", 16)
except:
    FONT = None

# ==== 로드 ====
with open(ACTIONS_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

# ==== 처리 ====
for i, step in enumerate(data, 1):
    img_path = Path(step["image"])
    actions = step.get("actions", [])
    caption = step.get("caption", "")

    if not img_path.exists():
        print(f"image not found: {img_path}")
        continue

    im = Image.open(img_path).convert("RGB")
    draw = ImageDraw.Draw(im)
    W, H = im.size

    for j, act in enumerate(actions, 1):
        if "xy" in act:
            x_rel, y_rel = act["xy"]
            x, y = int(x_rel * W), int(y_rel * H)
            # 빨간 원
            r = 8
            draw.ellipse((x - r, y - r, x + r, y + r), outline="red", width=3)
            # 라벨
            label = f"{act.get('type')}"
            if act.get("text"):
                label += f' "{act["text"]}"'
            draw.text((x + r + 2, y - r), label, fill="red", font=FONT)

    out_path = OUTPUT_DIR / f"step{i}.jpg"
    im.save(out_path)
    print(f"done: {out_path}")
