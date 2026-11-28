#!/usr/bin/env python3
"""Validate Test Case YAML files and generate TLCN_TestCases.xlsx (pure openpyxl).

Usage:
    python testing/scripts/build_testcases_xlsx.py
    python testing/scripts/build_testcases_xlsx.py --strict \
        --backend-root ../apt-workspace/backend \
        --frontend-root ../apt-workspace/frontend/frontend
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

VALID_CASE_TYPES = {"positive", "negative", "boundary"}
VALID_TEST_LEVELS = {"unit", "integration", "api", "e2e", "non-functional"}
VALID_AUTOMATION = {"auto", "manual"}
VALID_STATUSES = {"Not executed", "Pass", "Fail", "Suspended", "Crashed"}
VALID_PREFIXES = ("0.docs/", "backend/", "frontend/")

REQUIRED_FIELDS = (
    "id",
    "module",
    "srs_ref",
    "ac_ref",
    "case_type",
    "description",
    "created_by",
    "reviewed_by",
    "version",
    "test_level",
    "automation",
    "spec_ref",
    "test_name",
    "qa_log",
    "prerequisites",
    "test_data",
    "steps",
)

# Styling palette (consistent, print-friendly, zero external template dependency)
NAVY_FILL = PatternFill("solid", fgColor="1F4E78")
SUBHEADER_FILL = PatternFill("solid", fgColor="D9E1F2")
LABEL_FILL = PatternFill("solid", fgColor="F2F4F8")
PASS_FILL = PatternFill("solid", fgColor="E2EFDA")
FAIL_FILL = PatternFill("solid", fgColor="FCE4D6")
WARN_FILL = PatternFill("solid", fgColor="FFF2CC")
NEUTRAL_FILL = PatternFill("solid", fgColor="EDEDED")

HEADER_FONT = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
SUBHEADER_FONT = Font(name="Calibri", size=10, bold=True, color="1F4E78")
BOLD_FONT = Font(name="Calibri", size=10, bold=True, color="000000")
BODY_FONT = Font(name="Calibri", size=10, color="000000")
LINK_FONT = Font(name="Calibri", size=10, color="0563C1", underline="single")

THIN_SIDE = Side(style="thin", color="BFBFBF")
THIN_BORDER = Border(left=THIN_SIDE, right=THIN_SIDE, top=THIN_SIDE, bottom=THIN_SIDE)

ALIGN_LEFT = Alignment(horizontal="left", vertical="top", wrap_text=True)
ALIGN_CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
ALIGN_CENTER_TOP = Alignment(horizontal="center", vertical="top", wrap_text=True)


def status_fill(status: str) -> PatternFill:
    if status == "Pass":
        return PASS_FILL
    if status in {"Fail", "Crashed"}:
        return FAIL_FILL
    if status == "Suspended":
        return WARN_FILL
    return NEUTRAL_FILL


def load_yaml_cases(cases_dir: Path) -> list[tuple[Path, dict[str, Any]]]:
    yaml_files = sorted(
        p for p in cases_dir.glob("*.yaml") if not p.name.startswith("_")
    )
    records: list[tuple[Path, dict[str, Any]]] = []
    for path in yaml_files:
        data = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
        if data is None:
            continue
        if not isinstance(data, list):
            raise ValueError(f"{path.name}: top-level YAML must be a list of test cases.")
        for item in data:
            if not isinstance(item, dict):
                raise ValueError(f"{path.name}: every test case entry must be a mapping.")
            records.append((path, item))
    return records


def resolve_spec_path(
    spec_ref: str,
    docs_root: Path,
    backend_roots: list[Path],
    frontend_root: Path,
) -> Path | None:
    if spec_ref.startswith("0.docs/"):
        return docs_root / spec_ref.removeprefix("0.docs/")
    if spec_ref.startswith("backend/"):
        rel = spec_ref.removeprefix("backend/")
        for root in backend_roots:
            candidate = root / rel
            if candidate.exists():
                return candidate
        return backend_roots[0] / rel if backend_roots else None
    if spec_ref.startswith("frontend/"):
        return frontend_root / spec_ref.removeprefix("frontend/")
    return None


def validate_cases(
    records: list[tuple[Path, dict[str, Any]]],
    strict: bool,
    min_automation: float,
    docs_root: Path,
    backend_roots: list[Path],
    frontend_root: Path,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    seen_ids: set[str] = set()

    if not records:
        errors.append("No test case entries found in cases/*.yaml.")
        return errors, warnings

    for path, tc in records:
        tc_id = str(tc.get("id", "<missing-id>")).strip()
        prefix = f"[{path.name} :: {tc_id}]"

        for field in REQUIRED_FIELDS:
            if field not in tc:
                errors.append(f"{prefix} Missing required field '{field}'.")

        if not tc_id or tc_id == "<missing-id>":
            errors.append(f"[{path.name}] Empty 'id'.")
        elif tc_id in seen_ids:
            errors.append(f"{prefix} Duplicate Test Case ID '{tc_id}'.")
        else:
            seen_ids.add(tc_id)

        if len(tc_id) > 31:
            errors.append(f"{prefix} ID exceeds Excel sheet name limit (31 chars).")

        if tc.get("case_type") not in VALID_CASE_TYPES:
            errors.append(f"{prefix} Invalid case_type '{tc.get('case_type')}'.")

        if tc.get("test_level") not in VALID_TEST_LEVELS:
            errors.append(f"{prefix} Invalid test_level '{tc.get('test_level')}'.")

        automation = tc.get("automation")
        if automation not in VALID_AUTOMATION:
            errors.append(f"{prefix} Invalid automation '{automation}'.")

        if not str(tc.get("ac_ref", "")).strip():
            errors.append(f"{prefix} Empty 'ac_ref' (required for AC traceability).")

        qa_log = tc.get("qa_log")
        if not isinstance(qa_log, dict):
            errors.append(f"{prefix} 'qa_log' must be a mapping.")
        else:
            if qa_log.get("status") not in VALID_STATUSES:
                errors.append(f"{prefix} Invalid qa_log.status '{qa_log.get('status')}'.")

        for list_field in ("prerequisites", "test_data", "steps"):
            val = tc.get(list_field)
            if not isinstance(val, list) or len(val) == 0:
                errors.append(f"{prefix} '{list_field}' must be a non-empty list.")

        if isinstance(tc.get("steps"), list):
            for idx, step in enumerate(tc["steps"], start=1):
                if not isinstance(step, dict):
                    errors.append(f"{prefix} step #{idx} must be a mapping.")
                    continue
                for sf in ("step", "detail", "expected", "actual", "result"):
                    if sf not in step:
                        errors.append(f"{prefix} step #{idx} missing '{sf}'.")
                if step.get("result") not in VALID_STATUSES:
                    errors.append(
                        f"{prefix} step #{idx} invalid result '{step.get('result')}'."
                    )

        spec_ref = str(tc.get("spec_ref", "")).strip()
        test_name = str(tc.get("test_name", "")).strip()
        if automation == "auto":
            if not spec_ref:
                errors.append(f"{prefix} automation=auto requires non-empty 'spec_ref'.")
            elif not spec_ref.startswith(VALID_PREFIXES):
                errors.append(
                    f"{prefix} spec_ref '{spec_ref}' must start with one of {VALID_PREFIXES}."
                )
            if not test_name:
                errors.append(f"{prefix} automation=auto requires non-empty 'test_name'.")

            if strict and spec_ref and spec_ref.startswith(VALID_PREFIXES):
                resolved = resolve_spec_path(spec_ref, docs_root, backend_roots, frontend_root)
                if resolved is None or not resolved.exists():
                    errors.append(
                        f"{prefix} [--strict] spec_ref file not found on disk: {resolved}"
                    )
                elif test_name:
                    content = resolved.read_text(encoding="utf-8", errors="ignore")
                    if test_name not in content:
                        errors.append(
                            f"{prefix} [--strict] test_name '{test_name}' not found in {spec_ref}"
                        )

    total = len(records)
    auto_count = sum(1 for _, tc in records if tc.get("automation") == "auto")
    auto_pct = (auto_count / total * 100.0) if total else 0.0
    if auto_pct < min_automation:
        msg = (
            f"Automation rate is {auto_pct:.1f}% ({auto_count}/{total}), "
            f"below Rubric Mức 5 threshold ({min_automation:.1f}%)."
        )
        if strict:
            errors.append(f"[--strict] {msg}")
        else:
            warnings.append(msg)

    return errors, warnings


def style_range(ws: Any, cell_range: str, border: Border = THIN_BORDER) -> None:
    for row in ws[cell_range]:
        for cell in row:
            cell.border = border


def build_summary_sheet(wb: Workbook, cases: list[dict[str, Any]], min_auto: float) -> None:
    ws = wb.active
    ws.title = "Summary"
    ws.views.sheetView[0].showGridLines = True

    total = len(cases)
    status_counts = Counter(tc["qa_log"]["status"] for tc in cases)
    type_counts = Counter(tc["case_type"] for tc in cases)
    auto_count = sum(1 for tc in cases if tc["automation"] == "auto")
    manual_count = total - auto_count
    auto_pct = (auto_count / total * 100.0) if total else 0.0
    pass_count = status_counts["Pass"]
    executed_count = total - status_counts["Not executed"]
    pass_rate = (pass_count / executed_count * 100.0) if executed_count else 0.0

    # Title banner
    ws.merge_cells("A1:J1")
    ws["A1"] = "BÁO CÁO TỔNG HỢP TEST CASE — ADAPTIVE PLACEMENT TEST (CAT–RASCH v3.0)"
    ws["A1"].font = Font(name="Calibri", size=13, bold=True, color="FFFFFF")
    ws["A1"].fill = NAVY_FILL
    ws["A1"].alignment = ALIGN_CENTER
    ws.row_dimensions[1].height = 28

    ws.merge_cells("A2:J2")
    ws["A2"] = f"Sinh tự động từ 0.docs/testing/cases/*.yaml | Ngày xuất: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    ws["A2"].font = Font(name="Calibri", size=9, italic=True, color="333333")
    ws["A2"].alignment = ALIGN_CENTER

    # KPI Overview (Rows 4-7)
    kpi_headers = [
        ("A4", "Tổng Test Case"),
        ("B4", "Positive"),
        ("C4", "Negative"),
        ("D4", "Boundary"),
        ("E4", "Auto"),
        ("F4", "Manual"),
        ("G4", "% Automation"),
        ("H4", "Pass"),
        ("I4", "Fail"),
        ("J4", "Not executed"),
    ]
    for ref, text in kpi_headers:
        ws[ref] = text
        ws[ref].font = SUBHEADER_FONT
        ws[ref].fill = SUBHEADER_FILL
        ws[ref].alignment = ALIGN_CENTER

    kpi_values = [
        ("A5", total),
        ("B5", type_counts["positive"]),
        ("C5", type_counts["negative"]),
        ("D5", type_counts["boundary"]),
        ("E5", auto_count),
        ("F5", manual_count),
        ("G5", f"{auto_pct:.1f}%"),
        ("H5", pass_count),
        ("I5", status_counts["Fail"]),
        ("J5", status_counts["Not executed"]),
    ]
    for ref, val in kpi_values:
        ws[ref] = val
        ws[ref].font = BOLD_FONT
        ws[ref].alignment = ALIGN_CENTER

    ws["G5"].fill = PASS_FILL if auto_pct >= min_auto else WARN_FILL
    ws["H5"].fill = PASS_FILL if pass_count > 0 else NEUTRAL_FILL
    ws["I5"].fill = FAIL_FILL if status_counts["Fail"] > 0 else PASS_FILL
    style_range(ws, "A4:J5")

    ws.merge_cells("A6:J6")
    ws["A6"] = (
        f"Ngưỡng Rubric TC2.5 Mức 5: Automation ≥ {min_auto:.0f}% "
        f"({'ĐẠT' if auto_pct >= min_auto else 'CHƯA ĐẠT'}) | "
        f"Đã thực thi: {executed_count}/{total} | Tỉ lệ Pass trên ca đã chạy: {pass_rate:.1f}%"
    )
    ws["A6"].font = Font(name="Calibri", size=10, bold=True)
    ws["A6"].alignment = ALIGN_LEFT

    # Breakdown by Module (starts row 8)
    ws.merge_cells("A8:J8")
    ws["A8"] = "1. THỐNG KÊ THEO MODULE"
    ws["A8"].font = HEADER_FONT
    ws["A8"].fill = NAVY_FILL
    ws["A8"].alignment = ALIGN_LEFT

    mod_headers = [
        "Module", "Tổng TC", "Positive", "Negative", "Boundary",
        "Auto", "% Auto", "Pass", "Fail", "Not executed",
    ]
    for col_idx, text in enumerate(mod_headers, start=1):
        cell = ws.cell(row=9, column=col_idx, value=text)
        cell.font = SUBHEADER_FONT
        cell.fill = SUBHEADER_FILL
        cell.alignment = ALIGN_CENTER

    by_module: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for tc in cases:
        by_module[tc["module"]].append(tc)

    row_cursor = 10
    for mod, items in by_module.items():
        m_total = len(items)
        m_auto = sum(1 for x in items if x["automation"] == "auto")
        m_pct = (m_auto / m_total * 100.0) if m_total else 0.0
        vals = [
            mod,
            m_total,
            sum(1 for x in items if x["case_type"] == "positive"),
            sum(1 for x in items if x["case_type"] == "negative"),
            sum(1 for x in items if x["case_type"] == "boundary"),
            m_auto,
            f"{m_pct:.1f}%",
            sum(1 for x in items if x["qa_log"]["status"] == "Pass"),
            sum(1 for x in items if x["qa_log"]["status"] == "Fail"),
            sum(1 for x in items if x["qa_log"]["status"] == "Not executed"),
        ]
        for col_idx, val in enumerate(vals, start=1):
            c = ws.cell(row=row_cursor, column=col_idx, value=val)
            c.font = BODY_FONT
            c.alignment = ALIGN_LEFT if col_idx == 1 else ALIGN_CENTER
        row_cursor += 1
    style_range(ws, f"A9:J{row_cursor - 1}")

    # Traceability Index (RTM)
    row_cursor += 1
    ws.merge_cells(f"A{row_cursor}:J{row_cursor}")
    ws[f"A{row_cursor}"] = "2. DANH MỤC TEST CASE & MA TRẬN TRUY VẾT (RTM)"
    ws[f"A{row_cursor}"].font = HEADER_FONT
    ws[f"A{row_cursor}"].fill = NAVY_FILL
    ws[f"A{row_cursor}"].alignment = ALIGN_LEFT
    row_cursor += 1

    rtm_headers = [
        "Test Case ID", "Module", "SRS Ref", "AC Ref", "Case Type",
        "Level", "Automation", "Status", "Created By", "Reviewed By",
    ]
    header_row = row_cursor
    for col_idx, text in enumerate(rtm_headers, start=1):
        c = ws.cell(row=header_row, column=col_idx, value=text)
        c.font = SUBHEADER_FONT
        c.fill = SUBHEADER_FILL
        c.alignment = ALIGN_CENTER
    row_cursor += 1

    for tc in cases:
        tc_id = tc["id"]
        status = tc["qa_log"]["status"]
        row_vals = [
            tc_id,
            tc["module"],
            tc["srs_ref"],
            tc["ac_ref"],
            tc["case_type"],
            tc["test_level"],
            tc["automation"],
            status,
            tc["created_by"],
            tc["reviewed_by"],
        ]
        for col_idx, val in enumerate(row_vals, start=1):
            c = ws.cell(row=row_cursor, column=col_idx, value=val)
            if col_idx == 1:
                c.hyperlink = f"#'{tc_id}'!A1"
                c.font = LINK_FONT
                c.alignment = ALIGN_CENTER
            else:
                c.font = BODY_FONT
                c.alignment = ALIGN_LEFT if col_idx in (2, 3) else ALIGN_CENTER
            if col_idx == 8:
                c.fill = status_fill(status)
        row_cursor += 1
    style_range(ws, f"A{header_row}:J{row_cursor - 1}")

    col_widths = [18, 22, 20, 14, 12, 14, 13, 15, 13, 14]
    for idx, width in enumerate(col_widths, start=1):
        ws.column_dimensions[get_column_letter(idx)].width = width


def build_testcase_sheet(wb: Workbook, tc: dict[str, Any]) -> None:
    """Build 1 sheet matching the 25-row x 11-column reference template layout."""
    ws = wb.create_sheet(title=tc["id"])
    ws.views.sheetView[0].showGridLines = True

    # Column widths A..K (11 columns)
    col_widths = [8, 16, 16, 16, 14, 4, 8, 16, 18, 18, 18]
    for idx, width in enumerate(col_widths, start=1):
        ws.column_dimensions[get_column_letter(idx)].width = width

    # --- Header Block (Rows 1-6) ---
    ws.merge_cells("A1:B1")
    ws["A1"] = "Test Case ID"
    ws.merge_cells("C1:E1")
    ws["C1"] = tc["id"]
    ws.merge_cells("G1:K1")
    ws["G1"] = "QA Tester's Log"

    ws.merge_cells("A2:B2")
    ws["A2"] = "Test Case Description"
    ws.merge_cells("C2:E3")
    ws["C2"] = tc["description"]
    ws.merge_cells("G2:H2")
    ws["G2"] = "Tester's Name"
    ws.merge_cells("I2:K2")
    ws["I2"] = tc["qa_log"].get("tester", "")

    ws.merge_cells("A3:B3")
    ws["A3"] = "SRS / AC Ref"
    # Note: C2:E3 already merged for Description; put SRS/AC on Row 4 & Metadata on Rows 5-6
    ws.unmerge_cells("C2:E3")
    ws.merge_cells("C2:E2")
    ws["C2"] = tc["description"]
    ws.merge_cells("C3:E3")
    ws["C3"] = f"{tc['srs_ref']} | {tc['ac_ref']} | {tc['case_type']} | {tc['test_level']}"

    ws.merge_cells("G3:H3")
    ws["G3"] = "Date Tested"
    ws.merge_cells("I3:K3")
    ws["I3"] = tc["qa_log"].get("date_tested", "")

    ws.merge_cells("A4:B4")
    ws["A4"] = "Created By"
    ws.merge_cells("C4:E4")
    ws["C4"] = tc["created_by"]
    ws.merge_cells("G4:H4")
    ws["G4"] = "Test Case (Pass/Fail/Not executed)"
    ws.merge_cells("I4:K4")
    tc_status = tc["qa_log"]["status"]
    ws["I4"] = tc_status

    ws.merge_cells("A5:B5")
    ws["A5"] = "Reviewed By"
    ws.merge_cells("C5:E5")
    ws["C5"] = tc["reviewed_by"]
    ws.merge_cells("G5:H5")
    ws["G5"] = "Automation / Spec Ref"
    ws.merge_cells("I5:K5")
    spec_display = (
        f"{tc['automation']} | {tc['spec_ref']} :: {tc['test_name']}"
        if tc["automation"] == "auto"
        else "manual"
    )
    ws["I5"] = spec_display

    ws.merge_cells("A6:B6")
    ws["A6"] = "Version"
    ws.merge_cells("C6:E6")
    ws["C6"] = str(tc["version"])
    ws.merge_cells("G6:H6")
    ws["G6"] = "Module"
    ws.merge_cells("I6:K6")
    ws["I6"] = tc["module"]

    # Style header cells
    for r in range(1, 7):
        ws.row_dimensions[r].height = 22 if r != 2 else 34
        for c in (1, 7):
            cell = ws.cell(row=r, column=c)
            cell.font = BOLD_FONT
            cell.fill = LABEL_FILL
            cell.alignment = ALIGN_LEFT
        for c in (3, 9):
            cell = ws.cell(row=r, column=c)
            cell.font = BODY_FONT
            cell.alignment = ALIGN_LEFT

    ws["G1"].font = HEADER_FONT
    ws["G1"].fill = NAVY_FILL
    ws["G1"].alignment = ALIGN_CENTER
    ws["C1"].font = BOLD_FONT
    ws["I4"].fill = status_fill(tc_status)
    ws["I4"].font = BOLD_FONT
    ws["I4"].alignment = ALIGN_CENTER
    style_range(ws, "A1:E6")
    style_range(ws, "G1:K6")

    # --- Prerequisites & Test Data (Rows 8-12) ---
    ws["A8"] = "S #"
    ws.merge_cells("B8:E8")
    ws["B8"] = "Prerequisites:"
    ws["G8"] = "S #"
    ws.merge_cells("H8:K8")
    ws["H8"] = "Test Data"

    for ref in ("A8", "B8", "G8", "H8"):
        ws[ref].font = HEADER_FONT
        ws[ref].fill = NAVY_FILL
        ws[ref].alignment = ALIGN_CENTER if ref in ("A8", "G8") else ALIGN_LEFT

    prereqs = tc["prerequisites"]
    test_data = tc["test_data"]
    meta_rows = max(4, len(prereqs), len(test_data))
    for i in range(meta_rows):
        r = 9 + i
        ws.row_dimensions[r].height = 24
        ws.merge_cells(f"B{r}:E{r}")
        ws.merge_cells(f"H{r}:K{r}")
        if i < len(prereqs):
            ws[f"A{r}"] = i + 1
            ws[f"B{r}"] = prereqs[i]
        if i < len(test_data):
            ws[f"G{r}"] = i + 1
            ws[f"H{r}"] = test_data[i]
        ws[f"A{r}"].alignment = ALIGN_CENTER_TOP
        ws[f"G{r}"].alignment = ALIGN_CENTER_TOP
        ws[f"B{r}"].alignment = ALIGN_LEFT
        ws[f"H{r}"].alignment = ALIGN_LEFT
        for col_idx in (1, 2, 7, 8):
            ws.cell(row=r, column=col_idx).font = BODY_FONT

    meta_end = 8 + meta_rows
    style_range(ws, f"A8:E{meta_end}")
    style_range(ws, f"G8:K{meta_end}")

    # --- Test Steps Table (Starts at Row 14 or meta_end + 2) ---
    step_header_row = max(14, meta_end + 2)
    ws[f"A{step_header_row}"] = "Step #"
    ws.merge_cells(f"B{step_header_row}:D{step_header_row}")
    ws[f"B{step_header_row}"] = "Step Details"
    ws.merge_cells(f"E{step_header_row}:G{step_header_row}")
    ws[f"E{step_header_row}"] = "Expected Results"
    ws.merge_cells(f"H{step_header_row}:I{step_header_row}")
    ws[f"H{step_header_row}"] = "Actual Results"
    ws.merge_cells(f"J{step_header_row}:K{step_header_row}")
    ws[f"J{step_header_row}"] = "Pass / Fail / Not executed / Suspended / Crashed"
    ws.row_dimensions[step_header_row].height = 28

    for ref in (
        f"A{step_header_row}",
        f"B{step_header_row}",
        f"E{step_header_row}",
        f"H{step_header_row}",
        f"J{step_header_row}",
    ):
        ws[ref].font = HEADER_FONT
        ws[ref].fill = NAVY_FILL
        ws[ref].alignment = ALIGN_CENTER

    steps = tc["steps"]
    min_step_rows = max(11, len(steps))  # Guarantees >= 25 total rows
    for i in range(min_step_rows):
        r = step_header_row + 1 + i
        ws.row_dimensions[r].height = 30
        ws.merge_cells(f"B{r}:D{r}")
        ws.merge_cells(f"E{r}:G{r}")
        ws.merge_cells(f"H{r}:I{r}")
        ws.merge_cells(f"J{r}:K{r}")
        if i < len(steps):
            st = steps[i]
            ws[f"A{r}"] = st["step"]
            ws[f"B{r}"] = st["detail"]
            ws[f"E{r}"] = st["expected"]
            ws[f"H{r}"] = st.get("actual", "")
            res = st["result"]
            ws[f"J{r}"] = res
            ws[f"J{r}"].fill = status_fill(res)
            ws[f"J{r}"].font = BOLD_FONT
        for col_idx in (1, 2, 5, 8):
            ws.cell(row=r, column=col_idx).font = BODY_FONT
        ws[f"A{r}"].alignment = ALIGN_CENTER_TOP
        ws[f"B{r}"].alignment = ALIGN_LEFT
        ws[f"E{r}"].alignment = ALIGN_LEFT
        ws[f"H{r}"].alignment = ALIGN_LEFT
        ws[f"J{r}"].alignment = ALIGN_CENTER

    step_end = step_header_row + min_step_rows
    style_range(ws, f"A{step_header_row}:K{step_end}")


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    testing_dir = script_dir.parent
    docs_root_default = testing_dir.parent

    parser = argparse.ArgumentParser(
        description="Validate YAML test cases and generate TLCN_TestCases.xlsx."
    )
    parser.add_argument(
        "--cases-dir",
        type=Path,
        default=testing_dir / "cases",
        help="Directory containing *.yaml test case files.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=testing_dir / "output" / "TLCN_TestCases.xlsx",
        help="Output Excel workbook path.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Enforce Rubric Mức 5 gates: >=70%% automation + verify spec_ref & test_name on disk.",
    )
    parser.add_argument(
        "--min-automation",
        type=float,
        default=70.0,
        help="Minimum automation percentage required in --strict mode (default: 70.0).",
    )
    parser.add_argument("--docs-root", type=Path, default=docs_root_default)
    parser.add_argument(
        "--backend-root",
        type=Path,
        default=docs_root_default.parent / "apt-workspace" / "backend",
    )
    parser.add_argument(
        "--extra-backend-root",
        type=Path,
        action="append",
        default=[],
        help="Optional extra backend worktree root(s) to check before branch merge.",
    )
    parser.add_argument(
        "--frontend-root",
        type=Path,
        default=docs_root_default.parent / "apt-workspace" / "frontend" / "frontend",
    )
    args = parser.parse_args()

    try:
        records = load_yaml_cases(args.cases_dir)
    except Exception as exc:
        print(f"ERROR loading YAML: {exc}", file=sys.stderr)
        return 1

    backend_roots = [args.backend_root, *args.extra_backend_root]
    errors, warnings = validate_cases(
        records=records,
        strict=args.strict,
        min_automation=args.min_automation,
        docs_root=args.docs_root,
        backend_roots=backend_roots,
        frontend_root=args.frontend_root,
    )

    for w in warnings:
        print(f"WARNING: {w}")
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1

    cases = [tc for _, tc in records]
    wb = Workbook()
    build_summary_sheet(wb, cases, args.min_automation)
    for tc in cases:
        build_testcase_sheet(wb, tc)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    wb.save(args.output)

    auto_count = sum(1 for tc in cases if tc["automation"] == "auto")
    auto_pct = (auto_count / len(cases) * 100.0) if cases else 0.0
    print(
        f"OK: Generated {args.output} ({len(cases)} test cases, "
        f"automation {auto_count}/{len(cases)} = {auto_pct:.1f}%)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
