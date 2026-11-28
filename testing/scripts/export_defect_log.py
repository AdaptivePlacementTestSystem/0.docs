#!/usr/bin/env python3
"""Export GitHub Defect Issues (AdaptivePlacementTestSystem/0.docs) to DEFECT_LOG.md (Bảng 6.2).

Usage:
    # Fetch live issues using GitHub CLI (requires `gh auth login`)
    python testing/scripts/export_defect_log.py --repo AdaptivePlacementTestSystem/0.docs

    # Offline mode from exported JSON (for local verification/CI)
    python testing/scripts/export_defect_log.py --input sample_issues.json --output testing/DEFECT_LOG.md
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

SECTION_RE = re.compile(r"^###\s+(.+?)\s*$", re.MULTILINE)
BULLET_FIELD_RE = re.compile(r"^\s*-\s*\*\*(.+?):\*\*\s*(.+?)\s*$", re.MULTILINE)


def parse_form_sections(body: str) -> dict[str, str]:
    """Parse GitHub Issue Form markdown (`### Label\\n\\nValue`) into a dict."""
    if not body:
        return {}
    matches = list(SECTION_RE.finditer(body))
    sections: dict[str, str] = {}
    for idx, m in enumerate(matches):
        key = m.group(1).strip()
        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(body)
        val = body[start:end].strip()
        if val == "_No response_":
            val = ""
        sections[key] = val
    return sections


def parse_resolution_from_comments(comments: list[dict[str, Any]]) -> dict[str, str]:
    """Extract the latest `### Resolution & Regression` block from issue comments."""
    result = {
        "Fix PR / Commit": "",
        "Root Cause": "",
        "Regression Test Ref": "",
        "Verified By & Date": "",
        "CI Run Link": "",
    }
    for comment in comments or []:
        body = comment.get("body", "") or ""
        if "Resolution & Regression" not in body:
            continue
        for m in BULLET_FIELD_RE.finditer(body):
            k = m.group(1).strip()
            v = m.group(2).strip()
            if k in result:
                result[k] = v
    return result


def extract_label_value(labels: list[dict[str, Any]], prefix: str, default: str = "") -> str:
    for lbl in labels or []:
        name = lbl.get("name", "") if isinstance(lbl, dict) else str(lbl)
        if name.startswith(prefix):
            return name.removeprefix(prefix)
    return default


def normalize_status(issue: dict[str, Any]) -> str:
    lbl_status = extract_label_value(issue.get("labels", []), "status:")
    mapping = {
        "open": "Open",
        "in-progress": "In Progress",
        "fixed": "Fixed",
        "verified": "Verified",
    }
    if lbl_status in mapping:
        return mapping[lbl_status]
    return "Verified" if str(issue.get("state", "")).upper() == "CLOSED" else "Open"


def fetch_issues_via_gh(repo: str, label: str) -> list[dict[str, Any]]:
    cmd = [
        "gh",
        "issue",
        "list",
        "--repo",
        repo,
        "--label",
        label,
        "--state",
        "all",
        "--limit",
        "500",
        "--json",
        "number,title,state,author,assignees,labels,createdAt,closedAt,url,body,comments",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if proc.returncode != 0:
        raise RuntimeError(f"gh issue list failed: {proc.stderr.strip()}")
    return json.loads(proc.stdout or "[]")


def md_escape(text: str) -> str:
    return (text or "").replace("|", "\\|").replace("\r", "").replace("\n", " ").strip()


def load_historical_defects(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else []


def render_markdown(
    repo: str,
    issues: list[dict[str, Any]],
    historical: list[dict[str, Any]],
) -> str:
    sorted_issues = sorted(issues, key=lambda x: int(x.get("number", 0)))

    total = len(sorted_issues)
    status_counts = {"Open": 0, "In Progress": 0, "Fixed": 0, "Verified": 0}
    open_critical_blocker = 0

    parsed_rows: list[dict[str, Any]] = []
    for iss in sorted_issues:
        sections = parse_form_sections(iss.get("body", ""))
        resolution = parse_resolution_from_comments(iss.get("comments", []))
        status = normalize_status(iss)
        status_counts[status] = status_counts.get(status, 0) + 1

        severity = (
            sections.get("Severity")
            or extract_label_value(iss.get("labels", []), "severity:", "Major").capitalize()
        )
        priority = (
            sections.get("Priority")
            or extract_label_value(iss.get("labels", []), "priority:", "Medium").capitalize()
        )
        module = extract_label_value(iss.get("labels", []), "module:", "N/A").upper()

        if status in {"Open", "In Progress"} and severity.lower() in {"blocker", "critical"}:
            open_critical_blocker += 1

        author = (iss.get("author") or {}).get("login", "")
        assignees = ", ".join(a.get("login", "") for a in (iss.get("assignees") or [])) or "Chưa gán"
        created_date = str(iss.get("createdAt", ""))[:10]

        parsed_rows.append(
            {
                "number": iss.get("number"),
                "defect_id": f"DEF-{int(iss.get('number', 0)):03d}",
                "title": iss.get("title", ""),
                "url": iss.get("url", ""),
                "testcase_id": sections.get("TestCase ID", "N/A"),
                "summary": sections.get("Summary") or iss.get("title", ""),
                "endpoint": sections.get("URL / Endpoint", "N/A"),
                "platform": sections.get("Platform", "N/A"),
                "os": sections.get("Operating System", "N/A"),
                "browser": sections.get("Browser", "N/A"),
                "severity": severity,
                "priority": priority,
                "module": module,
                "reporter": author,
                "assigned_to": assignees,
                "submit_date": created_date,
                "status": status,
                "description": sections.get("Description", ""),
                "steps": sections.get("Steps to Reproduce", ""),
                "expected": sections.get("Expected Result", ""),
                "actual": sections.get("Actual Result", ""),
                "screenshot": sections.get("Screenshot / Log", "N/A") or "N/A",
                "notes": sections.get("Notes", "N/A") or "N/A",
                "resolution": resolution,
            }
        )

    lines: list[str] = [
        "# Danh sách Defect & Báo cáo lỗi chi tiết (Rubric TC2.5 — Bảng 6.2)",
        "",
        f"- **Nguồn Bug Tracker:** GitHub Issues `{repo}` (label `type:defect`)",
        f"- **Thời điểm tổng hợp:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## 1. Tổng hợp trạng thái Defect",
        "",
        "| Tổng số Defect | Open | In Progress | Fixed (chờ verify) | Verified (đã đóng) | Blocker / Critical còn mở |",
        "|---:|---:|---:|---:|---:|---:|",
        f"| **{total}** | {status_counts['Open']} | {status_counts['In Progress']} | {status_counts['Fixed']} | {status_counts['Verified']} | **{open_critical_blocker}** |",
        "",
        "## 2. Bảng theo dõi Defect (Bug Tracker Summary)",
        "",
        "| Defect ID | Issue | TestCase ID | Module | Summary | Severity | Priority | Reporter | Assigned To | Status | Fix PR / Commit | Regression Test Ref | Verified By & Date |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]

    if not parsed_rows:
        lines.append("| *(chưa có Issue nào có nhãn `type:defect`)* | — | — | — | — | — | — | — | — | — | — | — | — |")
    else:
        for r in parsed_rows:
            issue_link = f"[#{r['number']}]({r['url']})" if r["url"] else f"#{r['number']}"
            res = r["resolution"]
            lines.append(
                "| {defect_id} | {issue} | {tc} | {mod} | {summary} | {sev} | {pri} | {rep} | {asg} | {st} | {fix} | {reg} | {ver} |".format(
                    defect_id=r["defect_id"],
                    issue=issue_link,
                    tc=md_escape(r["testcase_id"]),
                    mod=md_escape(r["module"]),
                    summary=md_escape(r["summary"]),
                    sev=md_escape(r["severity"]),
                    pri=md_escape(r["priority"]),
                    rep=md_escape(r["reporter"]),
                    asg=md_escape(r["assigned_to"]),
                    st=md_escape(r["status"]),
                    fix=md_escape(res["Fix PR / Commit"]) or "—",
                    reg=md_escape(res["Regression Test Ref"]) or "—",
                    ver=md_escape(res["Verified By & Date"]) or "—",
                )
            )

    lines.extend(["", "## 3. Phiếu báo cáo lỗi chi tiết (14 trường chuẩn Bảng 6.2)", ""])
    if not parsed_rows:
        lines.append("_Chưa có phiếu lỗi chi tiết._")
    else:
        for r in parsed_rows:
            res = r["resolution"]
            lines.extend(
                [
                    f"### {r['defect_id']} — {r['title']}",
                    "",
                    "| Trường (Bảng 6.2) | Nội dung |",
                    "|---|---|",
                    f"| **TestCase ID** | {md_escape(r['testcase_id'])} |",
                    f"| **Name** | {md_escape(r['title'])} |",
                    f"| **Reporter** | {md_escape(r['reporter'])} |",
                    f"| **Submit Date** | {md_escape(r['submit_date'])} |",
                    f"| **Summary** | {md_escape(r['summary'])} |",
                    f"| **URL** | {md_escape(r['endpoint'])} |",
                    f"| **Screenshot** | {md_escape(r['screenshot'])} |",
                    f"| **Platform** | {md_escape(r['platform'])} |",
                    f"| **Operating System** | {md_escape(r['os'])} |",
                    f"| **Browser** | {md_escape(r['browser'])} |",
                    f"| **Severity** | {md_escape(r['severity'])} |",
                    f"| **Assigned to** | {md_escape(r['assigned_to'])} |",
                    f"| **Priority** | {md_escape(r['priority'])} |",
                    f"| **Status** | **{md_escape(r['status'])}** |",
                    f"| **Fix PR / Commit** | {md_escape(res['Fix PR / Commit']) or '—'} |",
                    f"| **Regression Test Ref** | {md_escape(res['Regression Test Ref']) or '—'} |",
                    f"| **CI Run Link** | {md_escape(res['CI Run Link']) or '—'} |",
                    "",
                    f"**Description:** {r['description'] or '—'}",
                    "",
                    "**Steps to Reproduce:**",
                    r["steps"] or "—",
                    "",
                    f"**Expected Result:** {r['expected'] or '—'}",
                    "",
                    f"**Actual Result:** {r['actual'] or '—'}",
                    "",
                    f"**Notes:** {r['notes'] or '—'}",
                    "",
                    "---",
                    "",
                ]
            )

    if historical:
        lines.extend(
            [
                "## 4. Lịch sử lỗi đã phát hiện & sửa trước 28/11/2026 (Truy vết Git — không tạo Issue lùi ngày)",
                "",
                "| Mã | Ngày phát hiện | Module | Tóm tắt lỗi | Commit sửa | Ghi chú kiểm chứng |",
                "|---|---|---|---|---|---|",
            ]
        )
        for item in historical:
            lines.append(
                "| {id} | {date} | {mod} | {sum} | `{sha}` | {note} |".format(
                    id=md_escape(str(item.get("id", ""))),
                    date=md_escape(str(item.get("date", ""))),
                    mod=md_escape(str(item.get("module", ""))),
                    sum=md_escape(str(item.get("summary", ""))),
                    sha=md_escape(str(item.get("commit", ""))),
                    note=md_escape(str(item.get("note", ""))),
                )
            )
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    testing_dir = script_dir.parent

    parser = argparse.ArgumentParser(
        description="Export GitHub Defect Issues to DEFECT_LOG.md (Bảng 6.2)."
    )
    parser.add_argument(
        "--repo",
        default="AdaptivePlacementTestSystem/0.docs",
        help="GitHub repository slug (owner/repo).",
    )
    parser.add_argument(
        "--label",
        default="type:defect",
        help="Label filter for defect issues.",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=None,
        help="Optional local JSON file (same schema as `gh issue list --json`) for offline export.",
    )
    parser.add_argument(
        "--historical",
        type=Path,
        default=testing_dir / "evidence" / "historical_defects.yaml",
        help="Optional YAML file listing pre-28/11 Git-verified defects.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=testing_dir / "DEFECT_LOG.md",
        help="Destination markdown file.",
    )
    args = parser.parse_args()

    try:
        if args.input is not None:
            issues = json.loads(args.input.read_text(encoding="utf-8-sig"))
        else:
            issues = fetch_issues_via_gh(args.repo, args.label)
    except Exception as exc:
        print(f"ERROR fetching issues: {exc}", file=sys.stderr)
        return 1

    historical = load_historical_defects(args.historical)
    md = render_markdown(args.repo, issues, historical)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(md, encoding="utf-8")
    print(f"OK: Exported {len(issues)} defect issue(s) to {args.output}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
