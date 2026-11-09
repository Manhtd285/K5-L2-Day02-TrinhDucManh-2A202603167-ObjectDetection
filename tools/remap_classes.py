"""Đổi ID lớp trong nhãn YOLO sang thư mục mới (không ghi đè nguồn).

Mặc định: 1->2, 2->3, 3->1 (CVAT đang để thứ tự car, bus, van, truck).
Chạy: python tools/remap_classes.py --src dataset/labels/train --dst outputs/labels_remapped
"""
import argparse
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="dataset/labels/train")
    ap.add_argument("--dst", default="outputs/labels_remapped")
    ap.add_argument("--map", default="0:0,1:2,2:3,3:1", help="old:new,...")
    a = ap.parse_args()
    m = {int(k): int(v) for k, v in (p.split(":") for p in a.map.split(","))}
    dst = Path(a.dst)
    dst.mkdir(parents=True, exist_ok=True)
    n = 0
    for f in sorted(Path(a.src).glob("*.txt")):
        out = []
        for line in f.read_text().splitlines():
            p = line.split()
            if p:
                out.append(" ".join([str(m[int(p[0])]), *p[1:]]))
        (dst / f.name).write_text("\n".join(out) + ("\n" if out else ""))
        n += 1
    print(f"Đã đổi lớp {n} file -> {dst}")


if __name__ == "__main__":
    main()

