# Quy ước Git/PR — phục vụ TC2.4 (Chất lượng mã nguồn) và G8

Ngưỡng rubric cần nhắm tới (Mục 5 — TC2.4):

| Metric | Mức 3 | Mức 4 | Mức 5 |
|---|---|---|---|
| Lỗi lint / 1000 dòng | ≤20 | ≤5 | 0 |
| Issue Blocker/Critical (static analysis) | ≤5 | ≤2 | 0 |
| Tỉ lệ trùng lặp mã | ≤10% | ≤5% | ≤3% |
| Tỉ lệ tuần có commit | ≥50% | ≥75% | ≥90% |
| Tỉ lệ thay đổi qua PR có review | ≥30% | ≥60% | ≥90% |
| Secret lộ trong repo | ≤2 | ≤1 | 0 |

## Quy tắc bắt buộc từ Tuần 1

1. **`git init` ngay khi có source code đầu tiên** — repo trống không tính là "tuần có commit".
2. **Mỗi thành viên commit ít nhất 1 lần thực chất mỗi tuần**, kể cả tuần chỉ làm tài liệu/thiết kế (commit docs/SRS cũng tính).
3. **Không commit thẳng vào `main`.** Luồng: `feature/<ten-module>` → Pull Request → **thành viên còn lại review** → merge. Với nhóm 2 người, review chéo bắt buộc 100% để đạt ngưỡng ≥90%.
4. **Commit message theo Conventional Commits:** `feat:`, `fix:`, `docs:`, `test:`, `chore:`, `refactor:` + mô tả ngắn có ý nghĩa (không dùng "update", "fix bug").
5. **Không bao giờ commit `.env` thật.** Chỉ commit `.env.example`. Bật `gitleaks` hoặc `git-secrets` trong pre-commit hook và trong CI (xem TC2.6).
6. **Checklist review PR (đặc biệt với PR chứa code do AI sinh):**
   - [ ] Đã đối chiếu thuật toán/công thức với tài liệu chính thức nếu liên quan đến CAT/EAP/Rasch.
   - [ ] Có unit test đi kèm cho logic mới, đặc biệt `cat-engine`.
   - [ ] Không có secret/API key hardcode.
   - [ ] Đã cập nhật `tracking/AI_USAGE_LOG.md` nếu PR có phần AI sinh.
   - [ ] Lint pass, không có issue Blocker/Critical mới.
7. **Danh mục nợ kỹ thuật:** duy trì file `TECH_DEBT.md` (hoặc issue label `tech-debt`) — Mức 5 của TC2.4 yêu cầu "danh mục nợ kỹ thuật kèm kế hoạch xử lý".

## Mô hình nhánh (Quyết định #36)

`feat|fix|docs|chore|test|refactor/<ten-chuc-nang>` → PR (squash) → `develop` → PR (merge commit) → `main`. `hotfix/<ten>` → PR vào `main`, sau đó merge ngược về `develop`. Không commit/push thẳng vào `main` và `develop`. Công cụ ép quy tắc: `devkit/` (git hook + CI + ruleset), xem `devkit/README.md`.

## Setup gợi ý (Tuần 1–2)

- ESLint + Prettier cho cả NestJS (backend) và Next.js (frontend), fail CI nếu có lỗi.
- Husky + lint-staged: chạy lint/format trước mỗi commit.
- SonarCloud (miễn phí cho repo public) hoặc CodeQL (GitHub) cho static analysis + duplication.
- README.md gốc: hướng dẫn cài đặt, chạy dev, chạy test, biến môi trường cần thiết — bắt buộc cho cả Mức 3 trở lên.
