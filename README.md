# TLCN — Tài liệu & tracking (repo `docs`)

Tài liệu thiết kế và hệ thống tracking của đồ án Tiểu luận **Adaptive Placement Test (CAT-Rasch)**. Code nằm ở các repo `backend` và `frontend` trong cùng Organization (Quyết định #34).

> Người mới / AI Agent: đọc `CLAUDE.md`, rồi `process/HUONG_DAN_RUBRIC_VA_TRACKING.md`.

## Cấu trúc

```
docs/
├── README.md, INDEX.md, CLAUDE.md
├── requirements/      SRS v2.6 Final và v3.0, đặc tả Use Case (24 UC cũ, v3.0)
├── design/            Class Diagram, luồng CAT Engine, Use Case Diagram (.xml), draw.io
├── process/           Hướng dẫn rubric + tracking, playbook, quy trình nhóm
├── tracking/          AI_USAGE_LOG (nhật ký dùng AI), mẫu và hướng dẫn: GIT_CONVENTIONS, template, evidence-checklist
└── devkit/            Git hook + CI + ruleset chặn push sai chuẩn rubric (xem devkit/README.md)
```

## Không nằm trong repo (có chủ ý)

| File | Lý do | Lấy ở đâu |
|---|---|---|
| `Rubric_Do_An_Mon_Hoc_CNPM_sinhvien.docx` | Tài liệu nội bộ của Khoa | Bản local của nhóm / GVHD |
| `tracking/status-reports/*.docx` | Nhị phân nặng | Nộp qua kênh của Khoa |
| `PROJECT_STATUS_REPORT_TEMPLATE.docx` (plugin) | Nhị phân 6 MB | Bản local của nhóm |
| `_BACKUP_*` | Sao lưu tạm; git đã giữ lịch sử | — |
| Log thật: `DECISIONS_LOG`, `COMMITMENT_BASELINE`, `TRACKING`, `weekly-log/Tuan-*`, `feature-plans/*` (trừ mẫu) | Chỉ lưu máy của nhóm (Quyết định #37), nộp riêng khi hội đồng cần | Bản local của nhóm |
| `work/` (kế hoạch, phân tích, sequence diagram theo tuần) | Chỉ lưu máy | Bản local của nhóm |
| `workspace-setup/` (plugin tlcn-devkit) | Công cụ cá nhân của nhóm | Bản local của nhóm |

## Quy ước

Commit, nhánh và PR: `tracking/GIT_CONVENTIONS.md`. Diagram giữ tiếng Anh, tài liệu và tracking giữ tiếng Việt (CLAUDE.md, quy tắc #4).
