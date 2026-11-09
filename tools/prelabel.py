"""Pre-label ảnh train bằng YOLO COCO pretrained, xuất YOLO 1.1 để import vào CVAT.

COCO: car=2, bus=5, truck=7 -> schema lab: car=0, truck=1, bus=2. `van` phải gán tay.
Kết quả: prelabels/obj_train_data/*.txt và prelabels_cvat.zip (import: YOLO 1.1).
Chạy: python tools/prelabel.py [--model yolo11x.pt] [--conf 0.25]
"""
import argparse
import zipfile
from pathlib import Path

from ultralytics import YOLO

COCO_TO_LAB = {2: 0, 7: 1, 5: 2}
NAMES = ["car", "truck", "bus", "van"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="yolo11x.pt")
    ap.add_argument("--conf", type=float, default=0.25)
    ap.add_argument("--images", default="dataset/images/train")
    ap.add_argument("--out", default="prelabels")
    a = ap.parse_args()

    images = sorted(Path(a.images).glob("*.jpg"))
    out = Path(a.out)
    data = out / "obj_train_data"
    data.mkdir(parents=True, exist_ok=True)
    model = YOLO(a.model)

    for img in images:
        res = model.predict(str(img), conf=a.conf, verbose=False)[0]
        lines = []
        for c, xywhn in zip(res.boxes.cls.tolist(), res.boxes.xywhn.tolist()):
            c = int(c)
            if c in COCO_TO_LAB:
                x, y, w, h = xywhn
                lines.append(f"{COCO_TO_LAB[c]} {x:.6f} {y:.6f} {w:.6f} {h:.6f}")
        (data / f"{img.stem}.txt").write_text("\n".join(lines) + ("\n" if lines else ""))

    (out / "obj.names").write_text("\n".join(NAMES) + "\n")
    (out / "obj.data").write_text(
        f"classes = {len(NAMES)}\ntrain = train.txt\nnames = obj.names\nbackup = backup/\n")
    (out / "train.txt").write_text(
        "".join(f"data/obj_train_data/{i.name}\n" for i in images))

    zpath = Path("prelabels_cvat.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in ("obj.names", "obj.data", "train.txt"):
            z.write(out / f, f)
        for t in sorted(data.glob("*.txt")):
            z.write(t, f"obj_train_data/{t.name}")
    print(f"Done: {len(images)} ảnh -> {zpath}")


if __name__ == "__main__":
    main()

