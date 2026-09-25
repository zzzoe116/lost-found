# -*- coding: utf-8 -*-
"""用 Pillow 绘制《校园失物招领小程序》的三条主流程图。

运行：python draw_flow.py
输出：flow-1-browse.png / flow-2-publish.png / flow-3-search.png
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "C:/Windows/Fonts/msyh.ttc"
FONT_BOLD = "C:/Windows/Fonts/msyhbd.ttc"

STEP = dict(fill="#eaf2ff", border="#2b7cf6")
START = dict(fill="#e6f8f6", border="#14b8a6")
END = dict(fill="#f0eeff", border="#7a6cf6")
DECIDE = dict(fill="#fff4e8", border="#ff8f1f")
LINE = "#8b93a1"
TEXT = "#1f2329"

W = 980


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT, size)


def text_size(draw, text, f):
    lines = text.split("\n")
    w = max(draw.textbbox((0, 0), ln, font=f)[2] for ln in lines)
    h = len(lines) * int(f.size * 1.35)
    return w, h


def draw_text(draw, cx, cy, text, f, color=TEXT):
    lines = text.split("\n")
    lh = int(f.size * 1.35)
    total = len(lines) * lh
    y = cy - total / 2
    for ln in lines:
        w = draw.textbbox((0, 0), ln, font=f)[2]
        draw.text((cx - w / 2, y), ln, font=f, fill=color)
        y += lh


def box(draw, cx, cy, w, h, text, style=STEP, size=22):
    r = 14
    draw.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2],
                           radius=r, fill=style["fill"], outline=style["border"], width=2)
    draw_text(draw, cx, cy, text, font(size))


def diamond(draw, cx, cy, w, h, text, size=22):
    pts = [(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)]
    draw.polygon(pts, fill=DECIDE["fill"], outline=DECIDE["border"], width=2)
    draw_text(draw, cx, cy, text, font(size))


def arrow(draw, pts, label=None, label_pos=None):
    """折线箭头，箭头画在最后一段的终点。"""
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i + 1]], fill=LINE, width=2, joint="curve")
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    dx, dy = x2 - x1, y2 - y1
    length = (dx * dx + dy * dy) ** 0.5 or 1
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    head, half = 13, 6
    draw.polygon([(x2, y2),
                  (x2 - ux * head + px * half, y2 - uy * head + py * half),
                  (x2 - ux * head - px * half, y2 - uy * head - py * half)], fill=LINE)
    if label:
        lx, ly = label_pos or ((x1 + x2) / 2, (y1 + y2) / 2 - 16)
        f = font(19)
        w = draw.textbbox((0, 0), label, font=f)[2]
        draw.rectangle([lx - w / 2 - 4, ly - 2, lx + w / 2 + 4, ly + f.size + 4], fill="#ffffff")
        draw.text((lx - w / 2, ly), label, font=f, fill="#5f6672")


def new_canvas(height, title):
    img = Image.new("RGB", (W, height), "#ffffff")
    d = ImageDraw.Draw(img)
    d.text((40, 26), title, font=font(26, True), fill="#1f2329")
    return img, d


def save(img, name):
    path = os.path.join(HERE, name)
    img.save(path)
    print("saved", path, img.size)


MAIN_X, MAIN_W = 340, 600
LOOP_X = 905

# ============ 图 1：浏览信息 → 查看详情 → 联系发布者 ============
img, d = new_canvas(1010, "图 1  浏览信息 → 查看详情 → 联系发布者")
box(d, MAIN_X, 90, MAIN_W, 62, "进入小程序首页", START)
box(d, MAIN_X, 190, MAIN_W, 62, "按「全部 / 寻物 / 招领」筛选信息列表")
box(d, MAIN_X, 292, MAIN_W, 86, "浏览物品卡片\n物品名称 · 地点 · 时间")
box(d, MAIN_X, 416, MAIN_W, 62, "点击卡片进入信息详情页")
diamond(d, MAIN_X, 540, 360, 120, "是我的东西吗？")
box(d, MAIN_X, 694, MAIN_W, 62, "查看发布者联系方式并联系发布者")
box(d, MAIN_X, 796, MAIN_W, 86, "线下核对物品并归还 / 领回")
box(d, MAIN_X, 942, MAIN_W, 86, "发布者在「我的发布」中把状态改为「已完成」", END)
arrow(d, [(MAIN_X, 121), (MAIN_X, 159)])
arrow(d, [(MAIN_X, 221), (MAIN_X, 249)])
arrow(d, [(MAIN_X, 335), (MAIN_X, 385)])
arrow(d, [(MAIN_X, 447), (MAIN_X, 495)])
arrow(d, [(MAIN_X, 600), (MAIN_X, 663)], label="是", label_pos=(MAIN_X + 26, 618))
arrow(d, [(MAIN_X, 725), (MAIN_X, 753)])
arrow(d, [(MAIN_X, 839), (MAIN_X, 899)])
arrow(d, [(MAIN_X + 180, 540), (LOOP_X, 540), (LOOP_X, 190), (MAIN_X + MAIN_W / 2, 190)],
      label="不是（继续浏览）", label_pos=(LOOP_X - 130, 356))
save(img, "flow-1-browse.png")

# ============ 图 2：发布信息 → 发布成功 ============
img, d = new_canvas(1010, "图 2  发布信息 → 发布成功")
box(d, MAIN_X, 90, MAIN_W, 62, "首页点击「发布寻物」或「发布招领」", START)
box(d, MAIN_X, 190, MAIN_W, 62, "进入发布信息页并选择信息类型")
box(d, MAIN_X, 292, MAIN_W, 62, "填写物品名称、类别、地点、时间")
box(d, MAIN_X, 392, MAIN_W, 86, "补充描述物品特征\n（可选：上传物品照片，最多 3 张）")
box(d, MAIN_X, 516, MAIN_W, 62, "填写联系方式")
diamond(d, MAIN_X, 640, 380, 120, "必填项是否填写完整？")
box(d, MAIN_X, 794, MAIN_W, 62, "点击「发布」")
box(d, MAIN_X, 894, MAIN_W, 62, "跳转发布成功页", END)
box(d, 800, 640, 230, 86, "提示补全\n对应字段", DECIDE)
arrow(d, [(MAIN_X, 121), (MAIN_X, 159)])
arrow(d, [(MAIN_X, 221), (MAIN_X, 261)])
arrow(d, [(MAIN_X, 323), (MAIN_X, 349)])
arrow(d, [(MAIN_X, 435), (MAIN_X, 485)])
arrow(d, [(MAIN_X, 547), (MAIN_X, 580)])
arrow(d, [(MAIN_X, 700), (MAIN_X, 763)], label="是", label_pos=(MAIN_X + 26, 718))
arrow(d, [(MAIN_X, 825), (MAIN_X, 863)])
arrow(d, [(MAIN_X + 190, 640), (800 - 115, 640)])
arrow(d, [(800 - 115, 600), (800 - 115, 292), (MAIN_X + MAIN_W / 2, 292)],
      label="否（回去补全）", label_pos=(700, 300))
save(img, "flow-2-publish.png")

# ============ 图 3：搜索物品 → 查看搜索结果 ============
img, d = new_canvas(1010, "图 3  搜索物品 → 查看搜索结果")
box(d, MAIN_X, 90, MAIN_W, 62, "首页点击顶部搜索栏", START)
box(d, MAIN_X, 190, MAIN_W, 62, "进入搜索页")
box(d, MAIN_X, 292, MAIN_W, 86, "输入物品关键词\n（如 校园卡 / 耳机 / 雨伞）")
box(d, MAIN_X, 416, MAIN_W, 62, "在名称、类别、地点、描述中匹配")
diamond(d, MAIN_X, 540, 360, 120, "是否有匹配结果？")
box(d, 800, 540, 230, 86, "提示「换个\n关键词试试」", DECIDE)
box(d, MAIN_X, 694, MAIN_W, 86, "展示搜索结果列表\n并提示命中条数（找到 N 条）")
box(d, MAIN_X, 818, MAIN_W, 62, "用「全部 / 寻物 / 招领 / 已完成」进一步筛选")
box(d, MAIN_X, 942, MAIN_W, 62, "点击结果卡片进入信息详情页", END)
arrow(d, [(MAIN_X, 121), (MAIN_X, 159)])
arrow(d, [(MAIN_X, 221), (MAIN_X, 249)])
arrow(d, [(MAIN_X, 335), (MAIN_X, 385)])
arrow(d, [(MAIN_X, 447), (MAIN_X, 495)])
arrow(d, [(MAIN_X, 600), (MAIN_X, 653)], label="有", label_pos=(MAIN_X + 26, 616))
arrow(d, [(MAIN_X, 737), (MAIN_X, 787)])
arrow(d, [(MAIN_X, 849), (MAIN_X, 911)])
arrow(d, [(MAIN_X + 180, 540), (800 - 115, 540)])
arrow(d, [(800 - 115, 497), (800 - 115, 292), (MAIN_X + MAIN_W / 2, 292)],
      label="无（重新输入）", label_pos=(700, 300))
arrow(d, [(MAIN_X + MAIN_W / 2, 818), (LOOP_X, 818), (LOOP_X, 694), (MAIN_X + MAIN_W / 2, 694)],
      label="切换筛选条件", label_pos=(LOOP_X - 120, 740))
save(img, "flow-3-search.png")