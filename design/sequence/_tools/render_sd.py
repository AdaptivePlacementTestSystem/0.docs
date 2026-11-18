"""Dựng ảnh PNG cho Sequence Diagram (SD_*.xml, Enterprise Architect XMI) bằng Pillow.

Dùng:  python _tools/render_sd.py            # dựng ảnh cho SD_01..SD_12
       python _tools/render_sd.py SD_08*.xml # chỉ một số file

Ảnh lưu cạnh file XML (cùng tên, đuôi .png). Đây là ảnh dựng từ nội dung XML để xem
nhanh/đính kèm báo cáo, KHÔNG phải ảnh xuất từ Enterprise Architect (bố cục tự động).

Quy ước vẽ:
- Hộp vàng = Actor, hộp xanh = đối tượng; đường đứt dọc = lifeline.
- XMI của EA không đánh dấu thông điệp trả về (tất cả là "Synchronous"), nên nét đứt dùng
  heuristic: nhãn bắt đầu bằng "Tra ve"/"Xac nhan", hoặc thông điệp gửi tới Actor.
- Số thứ tự được đánh lại liên tục 1..N theo seqno (seqno gốc có thể có khoảng trống).
"""
from __future__ import annotations

import glob
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
from sd_parse import parse  # noqa: E402

S = 1.35  # hệ số phóng ảnh
FONT = 'C:/Windows/Fonts/arial.ttf'
FONT_B = 'C:/Windows/Fonts/arialbd.ttf'

BG = (255, 255, 255)
INK = (30, 30, 30)
LIFE = (150, 150, 150)
OBJ_FILL = (219, 234, 254)
ACT_FILL = (254, 243, 199)
BORDER = (71, 85, 105)
ARROW = (30, 41, 59)
NOTE = (120, 53, 15)


def px(v: float) -> int:
    return int(round(v * S))


def font(size: float, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_B if bold else FONT, px(size))


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt, max_w: int) -> list[str]:
    lines: list[str] = []
    for para in text.split('\n'):
        cur = ''
        for word in para.split(' '):
            trial = word if not cur else cur + ' ' + word
            if draw.textlength(trial, font=fnt) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def dashed(draw, x1, y1, x2, y2, fill, width, dash=px(7), gap=px(5)):
    length = abs(x2 - x1) + abs(y2 - y1)
    if length == 0:
        return
    dx, dy = (x2 - x1) / length, (y2 - y1) / length
    pos = 0.0
    while pos < length:
        end = min(pos + dash, length)
        draw.line([(x1 + dx * pos, y1 + dy * pos), (x1 + dx * end, y1 + dy * end)], fill=fill, width=width)
        pos += dash + gap


def arrow_head(draw, x, y, direction: int, filled: bool):
    """direction: +1 mũi trỏ sang phải, -1 sang trái."""
    h, w = px(10), px(5)
    tip = (x, y)
    a = (x - direction * h, y - w)
    b = (x - direction * h, y + w)
    if filled:
        draw.polygon([tip, a, b], fill=ARROW)
    else:
        draw.line([a, tip, b], fill=ARROW, width=max(1, px(1.4)))


def is_return(msg, actor_ids: set[str]) -> bool:
    name = msg.name.lower()
    if name.startswith(('tra ve', 'xac nhan')):
        return True
    return msg.receiver in actor_ids and msg.sender not in actor_ids


def render(path: str) -> str:
    d = parse(path)
    parts = d.participants
    n = len(parts)
    actor_ids = {p.id for p in parts if p.kind == 'Actor'}
    idx = {p.id: i for i, p in enumerate(parts)}

    probe = ImageDraw.Draw(Image.new('RGB', (10, 10)))
    f_lbl, f_hdr, f_title = font(12.5), font(13, True), font(16, True)

    gap = 215 if n <= 6 else 195
    box_w = gap - 28
    margin = 60
    last_self = any(m.sender == m.receiver == parts[-1].id for m in d.messages)
    width = px(margin * 2 + box_w + gap * (n - 1) + (220 if last_self else 0))  # chừa lề cho nhãn tự gọi ở cột cuối
    xs = [px(margin + box_w / 2 + i * gap) for i in range(n)]

    # tiêu đề + đầu cột
    title_h = px(44)
    hdr_lines = [wrap(probe, p.name, f_hdr, px(box_w) - px(14)) for p in parts]
    hdr_h = max(len(h) for h in hdr_lines) * px(17) + px(18)
    top = title_h + px(10)

    # bố cục từng thông điệp
    rows = []
    for m in d.messages:
        if m.sender not in idx or m.receiver not in idx:
            continue
        i, j = idx[m.sender], idx[m.receiver]
        selfmsg = i == j
        if selfmsg:
            max_w = px(300)
        else:
            span = abs(xs[j] - xs[i])
            max_w = max(span - px(16), px(230))
        lines = wrap(probe, m.name, f_lbl, max_w)
        label_h = len(lines) * px(16)
        rows.append((m, i, j, selfmsg, lines, label_h))

    y = top + hdr_h + px(26)
    placed = []
    for (m, i, j, selfmsg, lines, label_h) in rows:
        h = max(label_h + px(24), px(44)) if not selfmsg else max(label_h, px(34)) + px(22)
        placed.append((y, h))
        y += h
    height = y + px(30)

    img = Image.new('RGB', (width, height), BG)
    dr = ImageDraw.Draw(img)

    dr.text((px(margin), px(12)), d.title, font=f_title, fill=INK)

    # lifeline
    for k, x in enumerate(xs):
        dashed(dr, x, top + hdr_h, x, height - px(14), LIFE, max(1, px(1)))
    # đầu cột
    for k, p in enumerate(parts):
        x0, x1 = xs[k] - px(box_w) // 2, xs[k] + px(box_w) // 2
        dr.rounded_rectangle([x0, top, x1, top + hdr_h], radius=px(6),
                             fill=ACT_FILL if p.kind == 'Actor' else OBJ_FILL, outline=BORDER, width=max(1, px(1.2)))
        ty = top + (hdr_h - len(hdr_lines[k]) * px(17)) // 2
        for line in hdr_lines[k]:
            w = dr.textlength(line, font=f_hdr)
            dr.text((xs[k] - w / 2, ty), line, font=f_hdr, fill=INK)
            ty += px(17)

    # thông điệp
    for no, ((m, i, j, selfmsg, lines, label_h), (y0, h)) in enumerate(zip(rows, placed), start=1):
        ret = is_return(m, actor_ids)
        lw = max(1, px(1.3))
        if selfmsg:
            x = xs[i]
            loop_w, loop_h = px(34), px(20)
            ya = y0 + h - px(12) - loop_h
            yb = ya + loop_h
            dr.line([(x, ya), (x + loop_w, ya), (x + loop_w, yb), (x, yb)], fill=ARROW, width=lw)
            arrow_head(dr, x, yb, -1, not ret)
            tx = x + loop_w + px(8)
            ty = y0 + px(6)
        else:
            x1, x2 = xs[i], xs[j]
            ya = y0 + h - px(12)
            direction = 1 if x2 > x1 else -1
            end = x2 - direction * px(1)
            if ret:
                dashed(dr, x1, ya, end, ya, ARROW, lw)
            else:
                dr.line([(x1, ya), (end, ya)], fill=ARROW, width=lw)
            arrow_head(dr, end, ya, direction, not ret)
            mid = (x1 + x2) / 2
            tx = None
            ty = y0 + px(4)
        # nhãn (kèm số thứ tự), nền trắng để dễ đọc trên lifeline
        for li, line in enumerate(lines):
            text = (f'{no}. ' if li == 0 else '   ') + line
            tw = dr.textlength(text, font=f_lbl)
            xx = tx if selfmsg else max(px(6), min(mid - tw / 2, width - tw - px(6)))
            dr.rectangle([xx - px(2), ty - px(1), xx + tw + px(2), ty + px(16)], fill=BG)
            dr.text((xx, ty), text, font=f_lbl, fill=NOTE if '[cho xac nhan' in line else INK)
            ty += px(16)

    out = os.path.splitext(path)[0] + '.png'
    img.save(out, optimize=True)
    return out


if __name__ == '__main__':
    files = sys.argv[1:] or sorted(glob.glob(os.path.join(os.path.dirname(__file__), '..', 'SD_*.xml')))
    for f in files:
        out = render(f)
        print(os.path.basename(out), os.path.getsize(out) // 1024, 'KB')
