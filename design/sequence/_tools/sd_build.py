"""Dựng file Sequence Diagram dạng Enterprise Architect XMI 1.1 (SD_*.xml) từ một đặc tả gọn.

Dùng khuôn lấy từ SD_08 (cùng cấu trúc với mọi SD khác trong thư mục): một Actor, các ClassifierRole
(boundary / control / entity) và các thông điệp đồng bộ. Mọi nhãn chỉ dùng ASCII (không dấu) vì file mã hóa windows-1252.

Đặc tả (dict):
    {
      'number': '13',                         # số thứ tự -> "sd 13 <title>"
      'title': 'Quan ly tai khoan SV/GV',
      'participants': [('Admin', 'actor'), ('Trang Tai khoan', 'boundary'), ('UserAdminController', 'control'), ('User', 'entity')],
      'messages': [(from_index, to_index, 'nhan thong diep'), ...],   # theo thứ tự thời gian
    }

Dùng thư viện:
    from sd_build import build, spec_from_xml, write_sd
Ảnh PNG dựng bằng render_sd.py (cùng thư mục).
"""
from __future__ import annotations

import os
import re
import uuid
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, '..', 'SD_08_QuenVaDatLaiMatKhau.xml')
ENCODING = 'cp1252'
LEFT0, STEP, WIDTH = 60, 170, 50  # toạ độ lifeline trên sơ đồ (như các SD hiện có)


def _id(prefix: str = 'EAID') -> str:
    h = uuid.uuid4().hex.upper()
    return f'{prefix}_{h[:8]}_{h[8:12]}_{h[12:16]}_{h[16:20]}_{h[20:32]}'


def _attr(value: str) -> str:
    return escape(value, {'"': '&quot;'})


class _Templates:
    """Các khối XML mẫu cắt ra từ SD_08."""

    def __init__(self, path: str = TEMPLATE):
        s = open(path, encoding=ENCODING).read()
        self.src = s
        first_role = s.index('<UML:ClassifierRole ')
        self.pre = s[:first_role]
        roles = list(re.finditer(r'<UML:ClassifierRole .*?</UML:ClassifierRole>', s, re.S))
        self.role_by_stereotype: dict[str, str] = {}
        for m in roles:
            st = re.search(r'<UML:Stereotype name="([^"]+)"', m.group(0)).group(1)
            self.role_by_stereotype.setdefault(st, m.group(0))
        self.role_sep = s[roles[0].end():roles[1].start()]
        first_msg = s.index('<UML:Message ')
        self.mid = s[roles[-1].end():first_msg]
        msgs = list(re.finditer(r'<UML:Message .*?</UML:Message>', s, re.S))
        self.msg = msgs[0].group(0)
        self.msg_sep = s[msgs[0].end():msgs[1].start()]
        actor = re.search(r'<UML:Actor .*?</UML:Actor>', s, re.S)
        self.actor = actor.group(0)
        self.tail1 = s[msgs[-1].end():actor.start()]
        first_de = s.index('<UML:DiagramElement ')
        self.tail2 = s[actor.end():first_de]
        des = list(re.finditer(r'<UML:DiagramElement [^>]*/>', s))
        self.de_sep = s[des[0].end():des[1].start()]
        self.after_des = s[des[-1].end():]
        self.pkg_name = re.search(r'<UML:Package name="([^"]+)"', s).group(1)
        self.pkg_id = re.search(r'<UML:Package name="[^"]+" xmi.id="(EAPK_[^"]+)"', s).group(1)
        self.diag_id = re.search(r'<UML:Diagram name="[^"]+" xmi.id="(EAID_[^"]+)"', s).group(1)
        self.root_id = re.search(r'<UML:Class name="EARootClass" xmi.id="(EAID_[^"]+)"', s).group(1)
        self.model_id = re.search(r'<UML:Model name="EA Model" xmi.id="(MX_[^"]+)"', s).group(1)
        # Diagram element mẫu cho thông điệp (chuẩn: "SX=0;SY=0;EX=0;EY=0;Path=;")
        self.de_msg = re.search(r'<UML:DiagramElement geometry="SX=0;SY=0;EX=0;EY=0;Path=;" subject="[^"]+" style=";Hidden=0;"/>', s).group(0)


_T: _Templates | None = None


def templates() -> _Templates:
    global _T
    if _T is None:
        _T = _Templates()
    return _T


def _set_tag(block: str, tag: str, value: str) -> str:
    pat = re.compile(r'(<UML:TaggedValue tag="%s" value=")[^"]*(")' % re.escape(tag))
    if not pat.search(block):
        return block
    return pat.sub(lambda m: m.group(1) + _attr(value) + m.group(2), block, count=1)


def build(spec: dict) -> str:
    t = templates()
    number, title = str(spec['number']), spec['title']
    pkg_name = f'sd {number} {title}'
    pkg_id = _id('EAPK')
    diag_id = _id()
    parts = spec['participants']
    ids = [_id() for _ in parts]

    def retarget(block: str) -> str:
        # Đổi mọi tham chiếu gói / sơ đồ / tên gói của khuôn sang gói mới
        block = block.replace(t.pkg_id, pkg_id).replace(t.diag_id, diag_id)
        block = block.replace(f'value="{t.pkg_name}"', f'value="{_attr(pkg_name)}"')
        block = block.replace(f'name="{t.pkg_name}"', f'name="{_attr(pkg_name)}"')
        return block

    out = [retarget(t.pre)]
    out[0] = out[0].replace(t.model_id, 'MX_' + _id('X')[5:])

    actor_idx = next((i for i, (_, k) in enumerate(parts) if k == 'actor'), None)
    role_indices = [i for i, (_, k) in enumerate(parts) if k != 'actor']
    local = {}  # chỉ số người tham gia -> ea_localid
    next_local = 3
    # Actor đứng trước (như khuôn: ea_localid 3), rồi các role theo thứ tự
    order = ([actor_idx] if actor_idx is not None else []) + role_indices
    for i in order:
        local[i] = next_local
        next_local += 1

    role_blocks = []
    for i in role_indices:
        name, kind = parts[i]
        base = t.role_by_stereotype.get(kind)
        if base is None:
            raise ValueError(f'Không có khuôn cho kiểu {kind!r}; dùng actor/boundary/control/entity')
        b = retarget(base)
        b = re.sub(r'(<UML:ClassifierRole name=")[^"]*(" xmi.id=")[^"]*(")', lambda m: m.group(1) + _attr(name) + m.group(2) + ids[i] + m.group(3), b, count=1)
        b = _set_tag(b, 'ea_localid', str(local[i]))
        b = re.sub(r'\{[0-9A-Fa-f-]{36}\}', lambda m: '{' + str(uuid.uuid4()).upper() + '}', b)
        role_blocks.append(b)
    out.append(t.role_sep.join(role_blocks))
    out.append(retarget(t.mid))

    msg_blocks = []
    msg_ids = []
    for seq, (src, dst, text) in enumerate(spec['messages'], start=1):
        mid = _id()
        msg_ids.append(mid)
        label = text  # giữ nguyên nhãn như đặc tả (nhãn trả về thường kết thúc bằng "()" theo quy ước hiện có)
        sname, skind = parts[src]
        dname, dkind = parts[dst]
        b = retarget(t.msg)
        b = re.sub(r'(<UML:Message name=")[^"]*(" xmi.id=")[^"]*(" visibility="public" sender=")[^"]*(" receiver=")[^"]*(")',
                   lambda m: m.group(1) + _attr(label) + m.group(2) + mid + m.group(3) + ids[src] + m.group(4) + ids[dst] + m.group(5), b, count=1)
        for tag, value in [
            ('seqno', str(seq)), ('ea_localid', str(seq)),
            ('ea_sourceName', sname), ('ea_targetName', dname),
            ('ea_sourceType', 'Actor' if skind == 'actor' else 'Sequence'),
            ('ea_targetType', 'Actor' if dkind == 'actor' else 'Sequence'),
            ('ea_sourceID', str(local[src])), ('ea_targetID', str(local[dst])),
            ('mt', label), ('diagram', diag_id),
        ]:
            b = _set_tag(b, tag, value)
        msg_blocks.append(b)
    out.append(t.msg_sep.join(msg_blocks))
    out.append(retarget(t.tail1))

    if actor_idx is not None:
        name, _ = parts[actor_idx]
        a = retarget(t.actor)
        a = re.sub(r'(<UML:Actor name=")[^"]*(" xmi.id=")[^"]*(")', lambda m: m.group(1) + _attr(name) + m.group(2) + ids[actor_idx] + m.group(3), a, count=1)
        a = _set_tag(a, 'ea_localid', str(local[actor_idx]))
        out.append(a)
    out.append(retarget(t.tail2))

    elems = []
    for pos, i in enumerate(order):
        left = LEFT0 + STEP * pos
        elems.append(f'<UML:DiagramElement geometry="Left={left};Top=50;Right={left + WIDTH};Bottom={1410 + 40 * max(0, len(msg_ids) - 21)};" subject="{ids[i]}" seqno="{pos + 1}" style="DUID={uuid.uuid4().hex[:8].upper()};"/>')
    for mid in msg_ids:
        elems.append(re.sub(r'subject="[^"]+"', f'subject="{mid}"', t.de_msg))
    out.append(t.de_sep.join(elems))
    out.append(retarget(t.after_des))
    return ''.join(out)


def spec_from_xml(path: str) -> dict:
    """Đọc lại một SD hiện có thành đặc tả (giữ kiểu stereotype từng đối tượng)."""
    s = open(path, encoding=ENCODING).read()
    title_full = re.search(r'<UML:Package name="([^"]+)"', s).group(1)
    m = re.match(r'sd (\d+) (.*)', title_full)
    number, title = (m.group(1), m.group(2)) if m else ('00', title_full)
    de = {mm.group(2): int(mm.group(1)) for mm in re.finditer(r'<UML:DiagramElement geometry="Left=(-?\d+);[^"]*" subject="([^"]+)"', s)}
    people = []  # (left, id, name, kind)
    for mm in re.finditer(r'<UML:ClassifierRole name="([^"]*)" xmi.id="([^"]+)".*?</UML:ClassifierRole>', s, re.S):
        st = re.search(r'<UML:Stereotype name="([^"]+)"', mm.group(0))
        people.append((de[mm.group(2)], mm.group(2), _unesc(mm.group(1)), st.group(1) if st else 'boundary'))
    for mm in re.finditer(r'<UML:Actor name="([^"]*)" xmi.id="([^"]+)"', s):
        people.append((de[mm.group(2)], mm.group(2), _unesc(mm.group(1)), 'actor'))
    people.sort()
    index = {pid: i for i, (_, pid, _, _) in enumerate(people)}
    msgs = []
    for mm in re.finditer(r'<UML:Message name="([^"]*)" xmi.id="[^"]+" visibility="public" sender="([^"]+)" receiver="([^"]+)">(.*?)</UML:Message>', s, re.S):
        seq = int(re.search(r'tag="seqno" value="(\d+)"', mm.group(4)).group(1))
        msgs.append((seq, index[mm.group(2)], index[mm.group(3)], _unesc(mm.group(1))))
    msgs.sort()
    return {'number': number, 'title': title, 'participants': [(n, k) for _, _, n, k in people],
            'messages': [(a, b, t) for _, a, b, t in msgs]}


def _unesc(v: str) -> str:
    return v.replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&amp;', '&')


def write_sd(spec: dict, path: str) -> None:
    text = build(spec)
    bad = [c for c in text if ord(c) > 127]
    if bad:
        raise ValueError('Nhãn còn ký tự ngoài ASCII: ' + ''.join(sorted(set(bad))))
    with open(path, 'w', encoding=ENCODING, newline='') as f:
        f.write(text)
