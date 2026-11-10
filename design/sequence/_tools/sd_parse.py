"""Đọc file Sequence Diagram dạng Enterprise Architect XMI 1.1 (SD_*.xml).

Trả về tiêu đề, danh sách đối tượng (lifeline) theo thứ tự trái -> phải và danh sách
thông điệp theo seqno. Dùng chung cho script dựng ảnh và script rà soát nội dung.
File XMI mã hóa windows-1252; nhãn hiện tại chỉ dùng ASCII (không dấu).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from lxml import etree


@dataclass
class Participant:
    id: str
    name: str
    kind: str  # 'Actor' | 'Object'
    left: int = 0


@dataclass
class Message:
    id: str
    seqno: int
    name: str
    sender: str
    receiver: str
    is_return: bool = False


@dataclass
class Diagram:
    title: str
    participants: list[Participant] = field(default_factory=list)
    messages: list[Message] = field(default_factory=list)


def _tag(el: etree._Element, name: str) -> str | None:
    for tv in el.iter('TaggedValue'):
        if tv.get('tag') == name:
            return tv.get('value')
    return None


def parse(path: str) -> Diagram:
    raw = open(path, 'rb').read()
    root = etree.fromstring(raw, etree.XMLParser(recover=True))
    for el in root.iter():  # bỏ namespace "{omg.org/UML1.3}Tên" -> "Tên"
        if isinstance(el.tag, str) and el.tag.startswith('{'):
            el.tag = el.tag.split('}', 1)[1]

    diagram = root.find('.//Diagram')
    title = diagram.get('name', '') if diagram is not None else ''

    lefts: dict[str, int] = {}
    if diagram is not None:
        for de in diagram.iter('DiagramElement'):
            m = re.search(r'Left=(-?\d+)', de.get('geometry', ''))
            if m and de.get('subject'):
                lefts[de.get('subject')] = int(m.group(1))

    parts: list[Participant] = []
    for el in root.iter():
        if el.tag in ('ClassifierRole', 'Actor') and el.get('xmi.id') in lefts:
            parts.append(
                Participant(
                    id=el.get('xmi.id'),
                    name=el.get('name', ''),
                    kind='Actor' if el.tag == 'Actor' else 'Object',
                    left=lefts[el.get('xmi.id')],
                )
            )
    parts.sort(key=lambda p: p.left)

    msgs: list[Message] = []
    for m in root.iter('Message'):
        seq = int(_tag(m, 'seqno') or 0)
        ptype = (_tag(m, 'privatedata1') or '').lower()
        msgs.append(
            Message(
                id=m.get('xmi.id'),
                seqno=seq,
                name=m.get('name', ''),
                sender=m.get('sender'),
                receiver=m.get('receiver'),
                is_return=('return' in ptype) or (_tag(m, 'style') == '4'),
            )
        )
    msgs.sort(key=lambda x: x.seqno)
    return Diagram(title=title, participants=parts, messages=msgs)


if __name__ == '__main__':
    import sys

    d = parse(sys.argv[1])
    names = {p.id: p.name for p in d.participants}
    print(d.title)
    print('  Participants:', ' | '.join(f'{p.name}' for p in d.participants))
    for m in d.messages:
        print(
            f'  {m.seqno:>2}. {names.get(m.sender, "?")} -> {names.get(m.receiver, "?")}'
            f'{" (return)" if m.is_return else ""}: {m.name}'
        )
