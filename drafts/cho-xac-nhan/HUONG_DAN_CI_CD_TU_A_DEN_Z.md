# Hướng dẫn CI/CD từ A đến Z — kết nối server, pipeline, luồng làm việc, đánh giá rubric

> **Ngày lập:** 2026-10-09 (Tuần 4/12). **Đối tượng đọc:** hai thành viên nhóm và người tiếp nhận sau này.
> **Liên quan:** kế hoạch `KE_HOACH_CI_CD_VA_TRIEN_KHAI.md`, theo dõi `TRACKING_CI_CD_VA_TRIEN_KHAI.md`, quyết định `DECISIONS_LOG.md` #65–#74, feature-plan `ci-cd.md`.
>
> **Cách đọc các nhãn trạng thái trong file này:**
> ✅ **Đã làm và đã kiểm chứng** (có bằng chứng ở Mục 2) · 🟡 **Đã soạn/thiết kế nhưng chưa chạy thật** · ⛔ **Chưa làm**.
> Mọi đoạn mã mẫu YAML/lệnh trong Mục 4–5 là **mẫu chưa chạy thử trên GitHub thật**; khi làm thật phải kiểm cú pháp bằng `actionlint` và chạy thử trên nhánh nháp.
>
> **Phạm vi (quyết định #81): chỉ làm đúng điều rubric đòi để đạt Mức 5; đã gỡ CodeQL, Trivy, workflow E2E riêng, script kiểm hạn chứng chỉ vì ngoài rubric.**
>
> **Bảo mật:** file này **không chứa** mật khẩu, khóa SSH, token hay địa chỉ IP server. IP lưu ở GitHub Secret `STAGING_HOST`; trong file ghi là `<IP_SERVER>`.

---

## 1. Bức tranh tổng thể

```
 Máy lập trình viên                GitHub                                   Server staging (dùng chung)
 ─────────────────                ─────────                                ─────────────────────────────
  commit/push  ──► PR vào develop ─► CI: build, lint, test, bảo mật          Docker: nginx + frontend + backend
  (hook chặn lỗi)    (người kia        │                                       + postgres + redis
                      review)         ▼                                       Cổng mở ra ngoài: chỉ 8443
                                   merge vào develop                          (80/443/8080 là của farmnongviet)
                                      │
                                      ▼
                          CD: đóng gói Docker ─► GHCR (kho image)
                                      │
                                      ▼
                          deploy qua SSH ─────────────────────────────────►  kéo image mới, khởi động lại
                                      │                                       service tương ứng
                                      ▼
                          smoke test: gọi health ◄──────────────────────────  trả lời "khỏe" hay không
                          (hỏng ⇒ job đỏ, rollback thủ công bằng workflow)

 Giám sát ngoài (monitor ping /health, log tập trung, cảnh báo) — theo quyết định #69, ⛔ chưa làm.
```

**Địa chỉ staging:** `https://staging.adaptiveplacementtest.id.vn:8443` (cổng 8443 vì 80/443 đang thuộc về dự án khác trên cùng server — xem Mục 3.6).

**Hai kho mã tách riêng** (quyết định #34): `backend` và `frontend`, mỗi kho có pipeline riêng nhưng cùng deploy lên **một** server, **một** `docker-compose.yml`. Kho `docs` chỉ có kiểm tra của devkit, không deploy.

---

## 2. Trạng thái hiện tại (bằng chứng, không phải lời hứa)

| Hạng mục | Trạng thái | Bằng chứng / ghi chú |
|---|---|---|
| Khóa SSH riêng cho CI (`ci_staging`) | ✅ | File `ci_staging`, `ci_staging.pub` trong `~/.ssh` của máy bạn |
| User `deploy` trên server, đăng nhập bằng khóa | ✅ | Lệnh `ssh -i ... deploy@<IP_SERVER> whoami` trả về `deploy` |
| Docker + Compose trên server | ✅ | Docker 29.9.0, Compose v5.6.0 (kiểm bằng SSH) |
| `farmnongviet` không bị gián đoạn | ✅ | Cổng 80/443/8080 vẫn nghe; tiến trình Java giữ nguyên PID, chạy liên tục ~97 ngày |
| RAM server | ✅ (đo) / ⚠️ (đủ?) | Tổng 1919 MB, khả dụng ~989–1001 MB; chưa chạy stack thật nên chưa biết đủ không |
| Tên miền trỏ về server | ✅ | Bản ghi A `staging` đúng trên `ns1/ns2/ns3.bkdns.vn` |
| Chứng chỉ HTTPS thật | ✅ | Let's Encrypt (YE1), `staging.adaptiveplacementtest.id.vn`, hiệu lực đến **2027-01-07**, gia hạn **thủ công** |
| `docker-compose.yml` (có `vector`), `nginx` template, `.env` mẫu | 🟡 | `backend/backend/deploy/`; `docker compose config` hợp lệ (đã gồm `vector`); `nginx -t` và `vector validate` chưa chạy |
| Tổ chức GitHub + 3 repo, devkit chạy thật | ⛔ | Chưa tạo / chưa `git init` |
| Secrets/Environment `staging` | 🟡 | Bạn báo đã thêm; GitHub không cho đọc lại nên chưa kiểm được |
| Dockerfile BE và FE (+ `.dockerignore`) | 🟡 | Đã soạn (Mục 5.7); **chưa `docker build`** vì Docker cục bộ đang tắt |
| Workflow CI/CD (BE, FE): `pipeline.yml`, `rollback.yml` | 🟡 | Đã soạn; **`actionlint` v1.7.12 chạy sạch trên cả hai repo** (chưa có `shellcheck` nên phần shell trong `run:` chỉ kiểm bằng đọc); **chưa chạy trên GitHub** |
| Deploy (`deploy.sh`), smoke test, workflow `rollback` | 🟡 | Đã soạn; `bash -n deploy.sh` đúng cú pháp; **chưa chạy trên server** |
| Endpoint health (BE `/api/v1/health`, `/api/v1/ready`; FE `/api/health`, `/api/health/live`) | ✅ (đơn vị) | Có test: BE 6 test, FE 4 test, xanh; `npm run build` BE và FE thành công; **chưa kiểm khi chạy cùng DB/Redis thật** |
| Test BE | 🟡 | Hiện chỉ có 6 test của module health; phần lõi CAT vẫn chưa có test (kế hoạch BE P2, P8) |
| Monitor ngoài + log tập trung + cảnh báo | 🟡 | Chọn Better Stack (#79); form monitor đã xem qua ảnh chụp; container gửi log (`vector`) đã soạn trong compose, chưa chạy; bạn chưa tạo monitor/nguồn log |

---

## 3. Phần A — Kết nối và chuẩn bị server (đã làm, ghi lại để làm lại được)

### 3.1. Nguyên tắc an toàn (đọc trước)

1. **Không đụng `farmnongviet`** (quyết định của bạn, bộ nhớ dự án): không sửa/reload Nginx host, không chạy Certbot của host, không đổi luật UFW hiện có, không khởi động lại máy, không `apt upgrade`, không dừng tiến trình nào.
2. **Không gửi mật khẩu, khóa riêng, token qua chat hay commit vào repo.** Mật khẩu root từng bị dán vào chat ⇒ **phải đổi** (`passwd` trên server).
3. Docker **publish cổng bỏ qua UFW**: chỉ publish đúng cổng 8443 (như trong compose).
4. Khi nghi khóa SSH bị lộ: xóa dòng tương ứng trong `/home/deploy/.ssh/authorized_keys`, tạo khóa mới, cập nhật Secret.

### 3.2. Tạo khóa SSH riêng cho CI (trên máy bạn)

Trong **CMD** (không phải Git Bash; CMD không hiểu `~`):

```cmd
mkdir %USERPROFILE%\.ssh
ssh-keygen -t ed25519 -C "ci-staging" -f %USERPROFILE%\.ssh\ci_staging -N ""
```

- Sinh hai file: `ci_staging` (**khóa riêng**, không chia sẻ) và `ci_staging.pub` (khóa công khai).
- Không đặt passphrase vì pipeline chạy tự động không nhập được.

### 3.3. Tạo user `deploy` và cài Docker (trên server, bạn tự chạy với quyền root)

Lý do dùng user riêng: CI không cần quyền root; nếu khóa lộ, kẻ xấu chỉ có quyền của `deploy`. (Lưu ý: thuộc nhóm `docker` gần như tương đương root trên máy đó, nên khóa này vẫn phải giữ kín.)

```bash
PUB='<nội dung một dòng của ci_staging.pub>'
adduser --disabled-password --gecos "" deploy
install -d -m 700 -o deploy -g deploy /home/deploy/.ssh
echo "$PUB" >> /home/deploy/.ssh/authorized_keys
chown deploy:deploy /home/deploy/.ssh/authorized_keys; chmod 600 /home/deploy/.ssh/authorized_keys
# Docker từ kho chính thức (không dùng snap); đặt NEEDRESTART_MODE=l để apt KHÔNG tự khởi động lại dịch vụ nào
export DEBIAN_FRONTEND=noninteractive NEEDRESTART_MODE=l
# ... thêm kho apt của Docker, cài docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
usermod -aG docker deploy
```

Script đầy đủ đã được đưa trong hội thoại; kiểm trước/sau: cổng 80/443/8080 vẫn nghe và PID tiến trình Java không đổi.

### 3.4. Kiểm tra kết nối (chỉ đọc)

```cmd
ssh -i %USERPROFILE%\.ssh\ci_staging deploy@<IP_SERVER> "whoami; docker --version; docker compose version; free -m | sed -n 1,2p"
```

Phải thấy `deploy`, bản Docker, bản Compose và thông tin RAM.

### 3.5. Trỏ tên miền và cấp chứng chỉ HTTPS (nhà đăng ký BKNS)

**DNS.** Ở trang quản lý DNS của BKNS, thêm bản ghi **A**: tên `staging`, giá trị `<IP_SERVER>`, TTL 5 phút. Kiểm: `nslookup staging.adaptiveplacementtest.id.vn`.

**Chứng chỉ.** Cổng 80/443 thuộc dự án khác nên không dùng được cách xác thực thông thường; ta dùng **DNS-01 thủ công** (quyết định #74): Certbot chạy trong Docker trên server, bạn thêm một bản ghi TXT vào DNS để chứng minh quyền sở hữu tên miền.

```bash
# Trong phiên SSH tương tác (ssh -t ... deploy@<IP_SERVER>)
mkdir -p ~/letsencrypt/etc ~/letsencrypt/lib ~/letsencrypt/log
docker run -it --rm \
  -v ~/letsencrypt/etc:/etc/letsencrypt -v ~/letsencrypt/lib:/var/lib/letsencrypt -v ~/letsencrypt/log:/var/log/letsencrypt \
  certbot/certbot certonly --manual --preferred-challenges dns \
  -d staging.adaptiveplacementtest.id.vn --agree-tos -m <email-của-bạn> --no-eff-email
# (lần thử đầu nên thêm --test-cert để tránh giới hạn lượt; bản thử không được trình duyệt tin)
```

Lệnh dừng và in ra tên bản ghi và một **chuỗi ngẫu nhiên**. Làm đúng thứ tự:
1. Ở BKNS thêm bản ghi **TXT**: tên `_acme-challenge.staging` (**không** gõ đuôi tên miền, form tự thêm), nội dung = chuỗi (không gõ ngoặc kép), TTL 5 phút.
2. Kiểm trên **cả ba** máy chủ DNS của BKNS (không chỉ kiểm bằng DNS thường):
   ```cmd
   nslookup -type=TXT _acme-challenge.staging.adaptiveplacementtest.id.vn ns1.bkdns.vn
   nslookup -type=TXT _acme-challenge.staging.adaptiveplacementtest.id.vn ns2.bkdns.vn
   nslookup -type=TXT _acme-challenge.staging.adaptiveplacementtest.id.vn ns3.bkdns.vn
   ```
3. **Chỉ khi cả ba** in ra đúng chuỗi mới quay lại cửa sổ SSH và bấm Enter. Chờ lâu hơn bình thường là chuyện đã xảy ra (ns1 chậm đồng bộ).
4. Thấy `Successfully received certificate` là xong; chứng chỉ ở `~/letsencrypt/etc/live/staging.adaptiveplacementtest.id.vn/` (chỉ root đọc, Nginx trong container đọc được).

**Hạn dùng:** 90 ngày; chứng chỉ hiện tại hết hạn **2027-01-07**. **Gia hạn = làm lại đúng quy trình trên.** Đặt nhắc ngày **2026-12-08**.

### 3.6. Vì sao staging chạy cổng 8443 và backend không mở ra ngoài

- 80/443 là của `farmnongviet` (Nginx host). Ta không sửa cấu hình đó nên dùng 8443 với Nginx **trong container** riêng.
- Trình duyệt chỉ nói chuyện với Next.js (kiểu BFF, quyết định #50); Next gọi backend qua mạng nội bộ Docker. Vì vậy backend, Postgres, Redis **không** có cổng nào mở ra Internet.

### 3.7. Những lỗi đã gặp và cách xử lý

| Lỗi | Nguyên nhân | Cách xử lý |
|---|---|---|
| `ssh-keygen ... failed: No such file or directory` | CMD không hiểu `~`, thư mục `.ssh` chưa có | Dùng `%USERPROFILE%\.ssh\...` và `mkdir` trước |
| `ssh-keyscan: unsupported KEX method` | `ssh-keyscan` của Windows bản cũ | Dùng `ssh-keyscan` của Git Bash |
| Certbot: `NXDOMAIN looking up TXT` | Bản ghi TXT sai tên (`www`), hoặc chưa đồng bộ | Sửa tên thành `_acme-challenge.staging`, kiểm cả `ns1/ns2/ns3` trước khi Enter |
| `ns1.bkdns.vn` không có TXT dù `ns2/ns3` có | Đồng bộ chậm phía BKNS | Chờ; nếu quá lâu: xóa và thêm lại bản ghi, hoặc hỏi hỗ trợ BKNS |
| `Permission denied (publickey)` | Khóa chưa vào `authorized_keys` hoặc sai phân quyền | Làm lại bước 3.3, kiểm `chmod 700/600` |

---

## 4. Phần B — GitHub: tổ chức, nhánh, bảo vệ, Secrets

### 4.1. Tạo Organization và repo (làm một lần)

1. github.com → **New organization** → gói **Free**; bật **2FA bắt buộc**; **Base permissions = Read**.
2. Mời bạn còn lại làm **Owner**, mời GVHD quyền **Read** (hội đồng cần xem được — quy tắc G8).
3. Tạo 3 repo **public**, rỗng (không README/license): `backend`, `frontend`, `docs`.

### 4.2. Khởi tạo git và devkit (mỗi repo)

```bash
git init -b main
bash <đường-dẫn>/docs-repo/devkit/install.sh        # chép hook + workflow, bật core.hooksPath
git add .gitignore README.md .githooks .github .gitattributes
git commit -m "chore: khởi tạo repo với devkit và README"
git branch develop
git remote add origin https://github.com/<tổ-chức>/<repo>.git
DEVKIT_BOOTSTRAP=1 git push -u origin main develop    # lần push thẳng duy nhất
```

- **Trước `git add`**, quét secret: `gitleaks detect --no-git --redact`. Backend phải có `.gitignore` chứa `.env` **trước** khi `git add` (hiện thư mục BE có `.env` thật).
- Mã đưa vào bằng **Pull Request** (`feat/...` → `develop`), người kia review.
- Chạy ít nhất một PR để workflow `devkit-checks` chạy; **sau đó** mới chạy `apply-rulesets.sh` (nếu không ruleset sẽ chờ check chưa từng tồn tại).
- Bật **secret scanning**, **push protection**, **Dependabot**; để `GITHUB_TOKEN` mặc định chỉ đọc.

### 4.3. Mô hình nhánh (quyết định #36)

```
feat|fix|docs|chore|test|refactor/<ten-chuc-nang>  ──PR (squash)──►  develop  ──PR (merge commit)──►  main
hotfix/<ten>  ──PR──►  main   (sau đó merge ngược main vào develop)
```

- `develop` = nơi tích hợp; **mỗi lần merge vào `develop` sẽ tự deploy lên staging**.
- `main` = bản ổn định; gắn tag `vX.Y.Z` + GitHub Release (cùng image đã chạy ở staging, không build lại).

### 4.4. Environment `staging` và Secrets (mỗi repo BE và FE)

Repo → **Settings → Environments → New environment** tên đúng `staging`; giới hạn **Deployment branches** là `develop` (và `main`).

| Loại | Tên | Giá trị |
|---|---|---|
| Secret | `STAGING_HOST` | IP server |
| Secret | `STAGING_USER` | `deploy` |
| Secret | `STAGING_SSH_KEY` | nội dung file khóa riêng `ci_staging` (lấy bằng `type %USERPROFILE%\.ssh\ci_staging \| clip` để không hiện ra màn hình) |
| Secret | `STAGING_KNOWN_HOSTS` | một dòng khóa công khai của server (lấy bằng `ssh-keyscan -t ed25519 <IP_SERVER>` của Git Bash) |
| Variable | `STAGING_DOMAIN` | `staging.adaptiveplacementtest.id.vn` |

Dùng **Environment** (không chỉ Secret cấp repo) vì GitHub ghi lại mỗi lần deploy vào mục **Deployments** — đó là nguồn đếm "số lần deploy tự động" cho rubric TC2.6.

---

## 5. Phần C — Pipeline CI/CD: các chặng, công cụ, lý do

> Đây là **thiết kế**, ⛔ chưa có workflow nào trong repo. Mục này giải thích từng chặng làm gì, dùng công cụ gì và vì sao.

### 5.1. Khái niệm nhanh

| Từ | Nghĩa |
|---|---|
| **CI** (tích hợp liên tục) | Mỗi khi có thay đổi, máy chủ GitHub tự **build + kiểm tra** (lint, test, bảo mật) để phát hiện lỗi sớm |
| **CD** (triển khai liên tục) | Sau khi kiểm tra xanh, tự **đóng gói và đưa bản mới lên môi trường** |
| **Runner** | Máy ảo GitHub cấp để chạy các bước của workflow |
| **Image / Registry (GHCR)** | Image = gói đóng sẵn ứng dụng để Docker chạy; GHCR = kho GitHub chứa image |
| **Environment** | Một "nơi triển khai" đặt tên (ở đây `staging`), có Secrets riêng và lịch sử deploy |
| **Smoke test** | Kiểm tra nhanh sau deploy: ứng dụng có trả lời không |
| **Rollback** | Quay về phiên bản trước khi bản mới hỏng |

### 5.2. Pipeline gồm 6 chặng (đúng mô tả TC2.6 Mức 5)

| # | Chặng | Làm gì | Công cụ | Tại sao |
|---|---|---|---|---|
| 1 | **Build** | `npm ci` rồi build từ checkout sạch | GitHub Actions, npm, Next/Nest build | Chứng minh mã build được từ repo nộp (quy tắc **G8**) |
| 2 | **Lint / phân tích tĩnh** | Lint, typecheck, kiểm định dạng, đo trùng lặp mã; SonarCloud (tùy chọn, chạy khi có `SONAR_TOKEN`) | ESLint/oxlint, `tsc`, Prettier, `jscpd`, SonarCloud | TC2.4: 0 lỗi lint, trùng lặp ≤ 3%, 0 Blocker/Critical |
| 3 | **Test** | Unit + integration (BE chạy Postgres, Redis tạm); xuất báo cáo coverage | Vitest, supertest, service containers | TC2.5: coverage, tỉ lệ test pass |
| 4 | **Bảo mật** | Quét secret toàn lịch sử, lỗ hổng thư viện chạy thật, review phụ thuộc trên PR | gitleaks, `npm audit`, dependency-review | TC2.4: 0 secret; TC2.6: chặng quét bảo mật/phụ thuộc |
| 5 | **Đóng gói** | Build image Docker, đẩy lên GHCR, gắn tag = mã commit | `docker/build-push-action` + cache | Image giống hệt nhau từ staging đến bản phát hành; server 2 GB không tự build nổi |
| 6 | **Triển khai** | SSH vào server, cập nhật đúng service, chạy migration, rồi smoke test | `ssh`, `docker compose`, GitHub Environments | Deploy tự động; mỗi lần ghi vào Deployments |

Các chặng 1–4 là **CI** (chạy trên cả PR); 5–6 là **CD** (chỉ chạy khi merge vào `develop`). Chặng 5–6 chỉ chạy nếu 1–4 xanh (dùng `needs:`).

### 5.3. Mẫu workflow (🟡 chưa chạy thử — phải kiểm `actionlint` và thử trên nhánh nháp)

> **Cập nhật:** workflow thật đã được soạn trong repo (xem Mục 5.7). Các đoạn dưới đây giữ lại làm phác thảo để đọc nhanh; file thật mới là bản dùng.

**Frontend CI** (`.github/workflows/ci.yml`, phác thảo):

```yaml
name: ci
on:
  pull_request:
  push:
    branches: [develop, main]
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true
permissions:
  contents: read
jobs:
  build-test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 24, cache: npm }
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm run format:check
      - run: npm run test:cov
      - run: npm run build
        env:
          API_BASE_URL: http://localhost:3001/api/v1
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      # gitleaks toàn lịch sử, npm audit --omit=dev, dependency-review (trên PR)
```

**Đóng gói và deploy** (chạy sau CI, chỉ trên `develop`):

```yaml
  package:
    needs: [build-test, security]
    if: github.ref == 'refs/heads/develop' && github.event_name == 'push'
    runs-on: ubuntu-latest
    permissions: { contents: read, packages: write }
    steps:
      - uses: actions/checkout@v4
      - uses: docker/login-action@v3
        with: { registry: ghcr.io, username: ${{ github.actor }}, password: ${{ secrets.GITHUB_TOKEN }} }
      - uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:sha-${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
  deploy:
    needs: package
    environment: staging          # để GitHub ghi vào Deployments
    runs-on: ubuntu-latest
    steps:
      - name: Cấu hình SSH
        run: |
          install -m 700 -d ~/.ssh
          printf '%s\n' "${{ secrets.STAGING_SSH_KEY }}" > ~/.ssh/id; chmod 600 ~/.ssh/id
          printf '%s\n' "${{ secrets.STAGING_KNOWN_HOSTS }}" > ~/.ssh/known_hosts
      - name: Deploy
        run: |
          ssh -i ~/.ssh/id ${{ secrets.STAGING_USER }}@${{ secrets.STAGING_HOST }} \
            "flock /tmp/placement-deploy.lock sh -c 'cd ~/placement && ./deploy.sh ghcr.io/${{ github.repository }}:sha-${{ github.sha }}'"
```

Ghi chú về mẫu trên:
- `flock` làm hai repo (BE, FE) **deploy tuần tự**, không chạy chồng `docker compose up`.
- `deploy.sh` (⛔ chưa viết) sẽ: cập nhật biến image trong `.env` trên server, `docker compose pull <service>`, chạy migration (với BE), `docker compose up -d <service>`, rồi chờ service khỏe.
- Smoke test BE: backend không mở ra ngoài nên gọi từ trong server (`docker compose exec backend wget -qO- http://127.0.0.1:3001/health`); smoke test FE: `curl -fsS https://<STAGING_DOMAIN>:8443/api/health`.
- Không dùng self-hosted runner: repo public, PR từ bên ngoài có thể chạy mã tùy ý.
- Ghim phiên bản action; `permissions:` tối thiểu; không dùng `pull_request_target`.

### 5.4. Rollback và phát hành

- **Rollback:** workflow `rollback` (`workflow_dispatch`) nhận một tag image cũ và chạy lại bước deploy với tag đó. Chỉ an toàn nếu migration **tương thích ngược** (chính sách #68: migration chỉ thêm, không có migration "down" vì Prisma không hỗ trợ).
- **Phát hành:** merge `develop → main`, gắn tag `vX.Y.Z`, tạo GitHub Release từ cùng image.


### 5.6. Giám sát với Better Stack — các bước thiết lập (quyết định #79)

Mục tiêu (TC2.6 Mức 5): **health check + log tập trung + cảnh báo**. Gói free của Better Stack, theo ảnh bạn gửi: monitor hiện ghi "Checked every 5 minutes" (form có tùy chọn 3 phút nhưng gói free áp 5 phút), báo qua email; **kiểm từ khóa là tính phí** nên health phải trả mã **503** khi không khỏe; **cảnh báo hết hạn SSL/tên miền là tính phí** nên hạn chứng chỉ tự nhắc lịch (ngày 2026-12-08).

**A. Tạo monitor (làm ngay, rồi tạm dừng đến khi staging chạy)**

| Ô trong form | Đặt |
|---|---|
| Alert us when | `URL becomes unavailable` (mục duy nhất của gói free) |
| URL to monitor | `https://staging.adaptiveplacementtest.id.vn:8443/api/health` |
| How should we escalate | Notify the primary responder, tick **E-mail**; "Within 3 minutes alert all other team members" giữ nguyên |
| Check frequency | Gói free thực tế là 5 phút (chấp nhận được) |
| Confirmation period | `Immediate start` để dễ demo; đổi sang 1–2 phút nếu bị báo nhầm |
| IP version | **IPv4** (server chỉ có bản ghi IPv4) |
| SSL/TLS verification | On |
| SSL / Domain expiration | Không dùng được ("upgrade to use") |
| HTTP method, timeout | GET, 30 giây, tick Follow redirects |
| Request headers, proxy, basic auth, maintenance window | Để trống |
| Locations | Giữ 4 khu vực mặc định |

Bấm **Create monitor** rồi **Pause** ngay (staging chưa chạy sẽ báo down liên tục). Khi deploy xong thì **Resume**.

**B. Tạo nguồn nhận log (làm ngay, giữ kín)**
1. **Telemetry / Logs → Sources → Connect source**, chọn **Docker**, đặt tên `placement-staging`.
2. Chép **Source token** và **Ingesting host** vào chỗ kín (không gửi chat, không commit).
3. Trên server, thêm hai giá trị vào `~/placement/.env` (quyền 600): `BETTERSTACK_INGEST_HOST`, `BETTERSTACK_SOURCE_TOKEN` (mẫu ở `deploy/.env.staging.example`).
4. Đối chiếu `deploy/vector/vector.yaml` với đoạn cấu hình Better Stack hiển thị ở trang nguồn; nếu khác, sửa theo trang đó.

**C. Sau khi staging chạy: kiểm chứng và lấy minh chứng**
1. Resume monitor, chờ chuyển xanh.
2. Gây lỗi có chủ đích: `cd ~/placement && docker compose stop frontend`; chờ email báo "down"; `docker compose start frontend`; **chụp ảnh email**.
3. Mở trang chủ staging vài lần; vào Logs trên Better Stack, tìm dòng log; **chụp ảnh**.
4. Chụp ảnh cấu hình monitor. Log chỉ giữ 3 ngày (gói free) nên chụp ngay.

**D. Hạn chứng chỉ HTTPS (không có công cụ bổ sung):** chứng chỉ hết hạn **2027-01-07** và gia hạn thủ công (Mục 3.5). Tự đặt nhắc lịch ngày **2026-12-08**. Gói free của Better Stack không có cảnh báo hạn SSL; ta không thêm công cụ ngoài rubric để bù.

**Cách hoạt động của các health endpoint:** `GET /api/health` (FE, deep) trả `200` chỉ khi Next chạy **và** backend trả `/ready` thành công (Postgres + Redis), ngược lại `503`; không trả chi tiết lỗi nội bộ. `GET /api/health/live` (FE) và `GET /api/v1/health` (BE) chỉ kiểm "còn sống", dùng cho `HEALTHCHECK` của Docker.

### 5.7. Các file đã soạn trong repo (🟡 chưa chạy thật)

| File | Việc |
|---|---|
| `backend/backend/.gitignore` | Chặn `.env`, `node_modules`, `dist`… (làm **trước** `git add` đầu tiên) |
| `backend/backend/src/modules/health/**` + `app.module.ts` | Module health (liveness + readiness), kèm 6 test |
| `backend/backend/Dockerfile`, `.dockerignore` | Image backend 2 giai đoạn, chạy user `node`, có `HEALTHCHECK`; giữ `node_modules` đầy đủ để chạy `prisma migrate deploy` (kích thước chưa đo) |
| `backend/backend/.github/workflows/pipeline.yml` | 6 chặng: build+test → bảo mật → đóng gói GHCR → deploy; chỉ đóng gói/deploy khi push `develop` |
| `backend/backend/.github/workflows/rollback.yml` | Rollback thủ công (workflow_dispatch nhận image cũ) |
| `backend/backend/deploy/docker-compose.yml` | nginx, frontend, backend, postgres, redis, **vector** (gửi log); chỉ publish cổng 8443 |
| `backend/backend/deploy/nginx/staging.conf.template` | HTTPS cổng 8443 dùng chứng chỉ đã cấp |
| `backend/backend/deploy/vector/vector.yaml` | Gửi log container lên Better Stack, đọc **file log chỉ đọc** (không mount `docker.sock`), che chuỗi `Bearer …` |
| `backend/backend/deploy/deploy.sh` | Chạy trên server: đổi image trong `.env`, `compose pull`, migration (backend), `up -d`, smoke test từ trong container, in cách rollback khi hỏng |
| `backend/backend/deploy/.env.staging.example` | Mẫu `.env` trên server (chỉ có `CHANGE_ME`) |
| `frontend/src/app/api/health/{route.ts,live/route.ts}` + test | Health FE (4 test) |
| `frontend/Dockerfile`, `.dockerignore` | Image Next.js (`standalone`), user `node`, `HEALTHCHECK` |
| `backend/backend/scripts/ci-metrics.sh` | Đo tỉ lệ run xanh, thời gian chạy pipeline, số deploy, số tuần có commit bằng `gh` (cần `gh auth login`; **chưa chạy thử**, máy chưa cài `gh`) |
| `frontend/.github/workflows/{pipeline,rollback}.yml` | Tương tự backend; không có bước chép compose (pipeline backend lo việc đó) |

**Thứ tự bắt buộc khi deploy lần đầu:** deploy **backend trước** (nó chép `docker-compose.yml`, nginx, vector, `deploy.sh` lên server), sau đó mới deploy frontend. Trước đó phải có `~/placement/.env` thật trên server (từ `.env.staging.example`, đổi mọi `CHANGE_ME`).

**Những điều chưa kiểm chứng và rủi ro đã biết:**
- Các workflow chưa chạy trên GitHub (đã qua `actionlint`); tên action/phiên bản (`@v4`, `@v3`, `@v6`) ghim theo thẻ, chưa ghim theo SHA. **SonarCloud chưa thêm** (cần tài khoản và khóa dự án, task CD3.5).
- `docker build` chưa chạy được ở máy cục bộ (Docker tắt); Dockerfile chưa được kiểm, đặc biệt bước `prisma generate` trên `node:24-slim` và việc chạy `npx prisma migrate deploy` trong image.
- Package GHCR có thể ở chế độ **private**; pipeline đăng nhập GHCR trên server bằng `GITHUB_TOKEN` của chính lần chạy rồi đăng xuất. Nếu pull lỗi, đặt package ở chế độ Public hoặc dùng PAT.
- `vector.yaml` và nhãn log `labels-regex` chưa kiểm; cần `vector validate` và thử trên server.
- Tổng giới hạn RAM của compose nay là khoảng 736 MB (thêm `vector` 64 MB) so với ~989 MB khả dụng dùng chung với `farmnongviet`; phải đo bằng `docker stats` trước khi tin.
- Backend hiện vẫn còn nhiều lỗi 🔴 của kế hoạch BE (ví dụ đăng nhập chấp nhận mọi mật khẩu); **đừng mở staging công khai với dữ liệu thật** trước khi sửa.


### 5.8. SonarCloud (SonarQube Cloud) — tác dụng, đáp ứng rubric, các bước thiết lập (quyết định #67)

#### 5.8.1. Nó là gì và làm gì

SonarCloud là dịch vụ **phân tích tĩnh mã nguồn trên web**. Mỗi lần pipeline chạy, nó đọc mã (không chạy mã) và báo cáo:

| Nó đo | Ý nghĩa | Ví dụ |
|---|---|---|
| **Lỗi và lỗ hổng (issue)** theo mức độ | Chỗ mã dễ sai hoặc không an toàn | hàm bỏ sót xử lý lỗi, chuỗi nối SQL, mã không bao giờ chạy tới |
| **Mã trùng lặp (duplication)** | Phần trăm dòng bị chép đi chép lại | hai hàm gần giống hệt nhau |
| **Độ phủ test (coverage)** | Bao nhiêu dòng được test chạy qua (đọc từ file `lcov` của Vitest) | backend 2,8%, frontend 81% (số đo cục bộ) |
| **Quality Gate** | Cổng đạt/không đạt theo ngưỡng; hiển thị xanh/đỏ trên PR | "mã mới phải có coverage ≥ 80%" (theo mặc định, hiểu biết chung, chưa kiểm) |
| **Nợ kỹ thuật, mùi mã (code smell)** | Thời gian ước tính để sửa | hàm quá dài |

Tác dụng thực tế: phát hiện lỗi **trước khi merge**, có **báo cáo trực quan** để đưa vào slide và hồ sơ minh chứng, và là **cổng chất lượng** trên PR.

#### 5.8.2. Nó đáp ứng yêu cầu rubric nào

| Yêu cầu trong rubric | SonarCloud đáp ứng thế nào | Ghi chú |
|---|---|---|
| **TC2.4 Mức 5:** "Phân tích tĩnh (SonarQube/SpotBugs/ESLint/Pylint…): **0 issue Blocker/Critical**, tỉ lệ **mã trùng lặp ≤ 3%**" | Là công cụ phân tích tĩnh chính; báo cáo cho cả hai chỉ số | Lưu ý: giao diện Sonar mới gọi mức độ là **Blocker / High / Medium…** (mức "Critical" cũ nay là "High" theo mô hình mới, **chưa kiểm** trên tài khoản của bạn); khi báo cáo, ghi rõ cách quy đổi và hỏi GVHD nếu cần |
| Bảng metric Mục 5 TC2.4: "Số issue Blocker/Critical (báo cáo SonarQube…)", "Tỉ lệ mã trùng lặp (báo cáo phân tích tĩnh)" | Nguồn minh chứng cho hai dòng này | Ảnh màn hình dashboard + liên kết dự án |
| Minh chứng Mục 8 (mục 7): "Báo cáo phân tích tĩnh mã nguồn, báo cáo quét secret, tài liệu coding convention" | Cung cấp **báo cáo phân tích tĩnh** | Báo cáo quét secret là của gitleaks, không phải Sonar |
| TC2.5 (liên quan): báo cáo coverage | **Hiển thị** coverage trên dashboard | Số liệu gốc vẫn là báo cáo của Vitest (`coverage/lcov.info`) |
| TC3 Mức 5: "minh chứng trực quan cho pipeline CI/CD, báo cáo coverage…" | Ảnh dashboard dùng cho slide | |

**Không thay thế được:** lint (ESLint/oxlint, chỉ số "lỗi lint / 1000 dòng"), quét secret (gitleaks/truffleHog — rubric chỉ định tên hai công cụ này), kiểm thử, hay pipeline CI/CD. Nó chỉ phủ phần **phân tích tĩnh + trùng lặp**.

**Điều kiện để đạt ngưỡng Mức 5:** 0 Blocker/Critical **và** trùng lặp ≤ 3% của **toàn bộ mã** (Overall Code), không chỉ mã mới. Quality Gate mặc định của Sonar thường chỉ xét **mã mới**; bạn phải xem số liệu **Overall Code** khi báo cáo. Mã shadcn/ui sinh sẵn được loại trừ khỏi coverage và trùng lặp, **có ghi chép** trong `sonar-project.properties` để minh bạch với hội đồng.

#### 5.8.3. Các bước thiết lập (làm theo thứ tự)

Giá trị của dự án bạn: **Organization key** `adaptiveplacementtest`; **Project key** `AdaptivePlacementTest_backend`, `AdaptivePlacementTest_frontend` (phân biệt hoa/thường).

| # | Bước | Làm ở đâu | Trạng thái |
|---|---|---|---|
| 1 | Đăng nhập sonarcloud.io bằng GitHub; **Import an organization from GitHub** → chọn `AdaptivePlacementTest`; cài ứng dụng SonarCloud cho tổ chức; chọn repo `backend`, `frontend`; **chọn gói Free** | SonarCloud | ✅ (có tổ chức và 2 project) |
| 2 | **Analyze new project** cho từng repo → **Set up** → "Choose your Analysis Method" chọn **With GitHub Actions** (CI-based analysis) | SonarCloud | ✅ |
| 3 | **Tắt Automatic Analysis** của cả hai project (Administration → Analysis Method) vì ta phân tích bằng CI; để cả hai cùng bật thường gây xung đột (hiểu biết chung, chưa kiểm) | SonarCloud | ⛔ bạn kiểm |
| 4 | Tạo token và lưu thành secret **`SONAR_TOKEN`** (cấp **repo**, không phải Environment `staging`, vì job build-test không chạy trong environment) cho từng repo: Settings → Secrets and variables → Actions → New repository secret | GitHub | ✅ |
| 5 | Điền `sonar-project.properties` (đã có sẵn: `sonar.organization`, `sonar.projectKey`, thư mục nguồn/test, loại trừ file sinh sẵn, `sonar.javascript.lcov.reportPaths=coverage/lcov.info`) | Repo | ✅ |
| 6 | Workflow `pipeline.yml`, job `build-test`: checkout `fetch-depth: 0` → build → `npm run test:cov` (sinh `coverage/lcov.info`) → bước `SonarSource/sonarqube-scan-action@v7` với `SONAR_TOKEN`; bước tự bỏ qua nếu không có token (PR từ fork) | Repo | 🟡 đã soạn, `actionlint` sạch, chưa chạy |
| 7 | **Đẩy mã lên GitHub**, mở PR, để pipeline chạy lần đầu | Git/GitHub | ⛔ |
| 8 | Mở dashboard dự án trên SonarCloud, **đọc kết quả lần đầu**: Blocker/High, trùng lặp (Overall Code), coverage, Quality Gate | SonarCloud | ⛔ |
| 9 | Nếu Quality Gate đỏ: sửa mã hoặc ghi lý do + kế hoạch vào `TECH_DEBT.md`; **không** hạ ngưỡng để "làm xanh giả"; **chưa** đặt Sonar thành check bắt buộc để merge cho đến khi xanh ổn định (quyết định #68) | Repo + SonarCloud | ⛔ |
| 10 | **Chụp ảnh** dashboard (issue, trùng lặp, coverage, Quality Gate) làm minh chứng TC2.4/TC3 | — | ⛔ |

**Thêm vào README** của mỗi repo huy hiệu (badge) trạng thái Quality Gate (lấy từ SonarCloud: Project Information → Badges) để người xem thấy ngay.

#### 5.8.4. Những điều chưa chắc và rủi ro

- **Gói và token:** gói free của SonarCloud không hết hạn cho dự án private đến 50k dòng và repo public được phân tích; **gói dùng thử trả phí 14 ngày** là thứ khác. Một số loại token (ví dụ token phạm vi tổ chức) thuộc gói trả phí; nếu tổ chức bị hạ về Free thì bước Sonar có thể báo lỗi xác thực và phải đổi sang loại token mà gói Free hỗ trợ. Kiểm trang Billing của tổ chức để biết đang ở gói nào.
- **Phiên bản action:** ví dụ chính thức dùng `@v7`; ghi chú cập nhật có nhắc `v8`, **chưa rõ nên dùng bản nào**; kiểm trên GitHub Marketplace khi chạy thật.
- **Quality Gate backend nhiều khả năng đỏ** ở lần đầu vì coverage thấp (chỉ module health có test) và còn lỗi 🔴 trong kế hoạch BE; đây là số đo thật, không che.
- Các số về ngưỡng mặc định của Quality Gate, tên mức độ (Blocker/High/Critical) và chuyện xung đột với Automatic Analysis là **hiểu biết chung, chưa kiểm** trên tài khoản của bạn.


### 5.9. Phân tích tĩnh và trùng lặp chạy ngay trong CI (quyết định #80)

Đây là phần **không cần dịch vụ ngoài**, luôn chạy trong chặng "lint / phân tích tĩnh" của pipeline, nên có số liệu cho TC2.4 dù chưa dùng SonarCloud.

| Công cụ | Làm gì | Ngưỡng | Chạy ở đâu |
|---|---|---|---|
| **oxlint** (BE), **ESLint** (FE) | Lint và phân tích tĩnh cơ bản | 0 lỗi (rubric Mức 5: 0 lỗi lint) | `npm run lint`, bắt buộc để CI xanh |
| **TypeScript** (`tsc`) | Kiểm kiểu | 0 lỗi | `npm run typecheck` (FE), `npm run build` (BE) |
| **jscpd** | Đo tỉ lệ mã trùng lặp | **≤ 3%** (đúng rubric TC2.4 Mức 5); vượt thì lệnh thoát mã lỗi và CI đỏ | `npm run dup`; báo cáo HTML/JSON lưu thành artifact `jscpd-<repo>` |
| **SonarCloud** (tùy chọn) | Dashboard Blocker/High, trùng lặp, coverage | Quality Gate | Chỉ khi có `SONAR_TOKEN` (Mục 5.8) |

**Cấu hình:** `.jscpd.json` ở gốc mỗi repo (BE: `src/**/*.ts` bỏ file `*.spec.ts`; FE: `src/**/*.{ts,tsx}`; `minLines` 5, `minTokens` 50, `threshold` 3). Báo cáo ghi vào `reports/jscpd` (đã có trong `.gitignore`).

**Số đo thật lúc này (máy cục bộ, 2026-10-09; sẽ đổi khi mã tăng):**

| Repo | Dòng đã quét | Dòng trùng | Tỉ lệ | Ghi chú |
|---|---|---|---|---|
| backend | 2926 (69 file) | 16 | **0,55%** | 1 đoạn lặp trong `prisma-item.repository.ts` |
| frontend | 202 (6 file, không gồm mã shadcn) | 0 | **0,00%** | Đo cả mã shadcn (1119 dòng, 20 file) vẫn 0% |

Lint: backend (oxlint) và frontend (ESLint) đều **0 cảnh báo** ở lần kiểm gần nhất. Đây là số đo của mã scaffold nhỏ; không suy ra chất lượng của phần mã sẽ viết thêm.

**Hạn chế cần biết:** `jscpd` đo **trùng lặp theo chuỗi token**, không phát hiện lỗi logic hay lỗ hổng. Rubric chỉ nêu ví dụ SonarQube/SpotBugs/ESLint/Pylint; ESLint/oxlint được kể là công cụ phân tích tĩnh, nhưng chỉ số "Blocker/Critical" mà rubric nhắc chủ yếu là khái niệm của Sonar. Nếu hội đồng đòi báo cáo Blocker/Critical, cần dùng SonarCloud (Mục 5.8).

---

## 6. Luồng thực hiện hằng ngày (từ lúc code đến lúc chạy)

```
1.  git checkout -b feat/ten-chuc-nang                       (tên nhánh sai ⇒ hook chặn)
2.  Viết code + test; commit (Conventional Commits; hook chặn .env, secret, message chung chung)
3.  git push                                                  (hook pre-push chạy lint + test cục bộ)
4.  Mở Pull Request vào develop, tick checklist PR
5.  CI chạy: devkit-checks + build, lint, test, bảo mật       (đỏ ⇒ sửa rồi push lại)
6.  Người kia review & approve                                 (ruleset: bắt buộc 1 approval, admin cũng không bỏ qua)
7.  Squash merge vào develop
8.  CD tự chạy: đóng gói image → GHCR → deploy staging → smoke test
9.  Mở staging kiểm tay luồng vừa làm
10. Khi ổn: PR develop → main, gắn tag vX.Y.Z (phát hành)
```

**Khi pipeline đỏ:** xem log job đỏ trong tab Actions; nếu là deploy hỏng ⇒ chạy workflow `rollback` với tag trước.
**Mỗi tuần:** mỗi người ít nhất một commit thực chất (TC2.4: tuần có commit); tránh dồn merge vào cuối tuần để các lần deploy trải đều (TC2.6).

### 6.1. Runbook ngắn

| Việc | Cách |
|---|---|
| Xem tình trạng staging | SSH `deploy@<IP_SERVER>`, `cd ~/placement && docker compose ps` |
| Xem log một service | `docker compose logs --tail=100 backend` |
| Tắt nhanh staging (bảo vệ `farmnongviet` nếu máy quá tải) | `docker compose down` |
| Kiểm RAM | `free -m` và `docker stats --no-stream`; ngưỡng cần dừng: RAM khả dụng < ~200 MB hoặc swap tăng nhanh |
| Gia hạn chứng chỉ (≤ **2027-01-07**) | Lặp lại Mục 3.5 (TXT thủ công); sau đó `docker compose restart nginx` |
| Rollback | Workflow `rollback` + tag cũ |

---

## 7. Đánh giá mức đáp ứng rubric (trung thực)

> Căn cứ: rubric Mục 4, 5, 7, 8 (bản `Rubric_Do_An_Mon_Hoc_CNPM_sinhvien.docx`). Cột "Hiện tại" phản ánh **trạng thái ngày 2026-10-09**; "Nếu làm đủ kế hoạch" là **dự báo thiết kế**, không phải cam kết. Chưa có số đo thật nào trong cột đo (xem Mục 8).

### 7.1. TC2.6 — CI/CD và vận hành (5 điểm)

| Yêu cầu Mức 5 | Cách đáp ứng trong kế hoạch | Hiện tại | Nếu làm đủ | Rủi ro/ghi chú |
|---|---|---|---|---|
| ≥ 6 chặng (build → lint → test → bảo mật → Docker → deploy) | Mục 5.2 | ⛔ chưa có workflow | Đạt về thiết kế | Phải chạy thật, nối `needs:` để thấy rõ chuỗi |
| Build xanh ≥ 90% | Hook cục bộ chặn lỗi, `actionlint`, thử trên nhánh nháp, E2E chưa bắt buộc | ⛔ | Chưa chắc | Chưa biết Khoa tính cả run PR hay chỉ nhánh chính; những lần đỏ lúc mới dựng kéo tụt tỉ lệ |
| ≥ 10 deploy tự động, **trải đều** | Mỗi merge vào `develop` tự deploy, ghi vào Deployments | ⛔ 0 lần | Đạt nếu deploy chạy được sớm và merge đều | Deploy chỉ tính từ khi chạy được; mục tiêu lần đầu **trước cuối Tuần 5** |
| Commit → staging ≤ 15 phút | Build image trên Actions, server chỉ kéo về, cache | ⛔ chưa đo | Có thể đạt | Chỉ biết sau khi đo (nhiều khả năng bị Docker/Next build chi phối) |
| Secret qua cơ chế nền tảng | GitHub Environments + file `.env` trên server (quyền 600) | 🟡 Secrets đã thêm (chưa kiểm) | Đạt | Không đưa secret vào repo/workflow |
| Đánh số phiên bản + rollback | Tag = mã commit và `vX.Y.Z`; workflow `rollback` | ⛔ | Đạt về thiết kế | Phụ thuộc migration tương thích ngược |
| Health check + log tập trung + cảnh báo | `/health`, monitor ngoài, log hosted, cảnh báo (#69) | ⛔ | Đạt nếu chọn được dịch vụ miễn phí đáp ứng | Gói miễn phí các dịch vụ chưa kiểm chứng |
| **G6** (pipeline chạy được lúc bảo vệ) | Đóng băng `main` từ Tuần 11, chạy lại lần cuối | ⛔ | Tránh được nếu pipeline chạy | Nếu không có pipeline chạy lúc bảo vệ: TC2.6 tối đa Mức 2 |

**Điểm yếu chủ động chấp nhận:** gia hạn chứng chỉ thủ công (#74) làm "quy trình tự động" kém hơn; có thể nâng sau (CNAME ủy quyền hoặc Cloudflare) mà không phải làm lại phần khác. **Không sao lưu DB staging** (#70).

### 7.2. TC2.4 — Chất lượng mã và quản lý Git (10 điểm, phần liên quan CI/Git)

| Yêu cầu Mức 5 | Cách đáp ứng | Hiện tại | Rủi ro |
|---|---|---|---|
| 0 lỗi lint | Lint là điều kiện bắt buộc của CI | ✅ (cục bộ) oxlint (BE) và ESLint (FE) đều 0 cảnh báo; **chưa chạy trong CI trên GitHub** | BE còn lỗi 🔴 nghiệp vụ nhưng lint sạch |
| 0 Blocker/Critical; trùng lặp ≤ 3% | `jscpd` trong CI (Mục 5.9, đo thật: BE 0,55%, FE 0,00%) + SonarCloud tùy chọn (Mục 5.8) | 🟡 Đã tạo tổ chức/project, có token, file cấu hình sẵn; chưa chạy phân tích | Quality Gate backend nhiều khả năng đỏ lúc đầu; số liệu phải là Overall Code; mã shadcn sinh sẵn được loại trừ có ghi chép |
| ≥ 90% tuần có commit | Mỗi người ≥ 1 commit thực chất/tuần; script đo | ⛔ (chưa có git) | **Có thể không đạt Mức 5** vì repo bắt đầu muộn; không tạo commit lùi ngày; cần hỏi GVHD cách đếm |
| ≥ 90% thay đổi qua PR có review | Ruleset bắt buộc 1 approval, bypass rỗng | ⛔ | Một người vắng ⇒ PR kẹt; cần quy ước |
| 0 secret (gitleaks/truffleHog) | gitleaks ở hook và CI (toàn lịch sử), secret scanning, `.gitignore` | ⛔ | Backend phải có `.gitignore` **trước** commit đầu |
| README, sơ đồ triển khai, nợ kỹ thuật | README mỗi repo, Mục 1 của file này làm sơ đồ, `TECH_DEBT.md` | 🟡 README FE có; còn lại ⛔ | |

### 7.3. TC2.5 — Kiểm thử (5 điểm, phần liên quan CI)

| Yêu cầu | Hiện tại | Rủi ro |
|---|---|---|
| 100% test pass ở lần chạy CI cuối | ⛔ chưa có CI | Đóng băng `main` từ Tuần 11 |
| Coverage ≥ 70% mô-đun cốt lõi + báo cáo | FE có 12 test đơn vị, chưa đo coverage; **BE 0 test** | BE là khoảng trống lớn; không đặt ngưỡng cao khi chưa đạt (sẽ làm CI đỏ) |
| ≥ 4 tầng kiểm thử | FE: đơn vị + 1 E2E; BE chưa có | Cần integration, API, E2E, phi chức năng |

### 7.4. Các quy tắc chặn liên quan

| Mã | Điều kiện | Tình trạng |
|---|---|---|
| **G6** | Không có pipeline CI/CD chạy được lúc bảo vệ ⇒ TC2.6 ≤ Mức 2 | Nguy cơ cho đến khi pipeline chạy thật |
| **G8** | Repo không cấp quyền cho hội đồng/không build được ⇒ TC2.2 và TC2.4 mỗi tiêu chí −1 mức | Phòng bằng: repo public, mời GVHD, CI `build` từ checkout sạch, README đầy đủ |
| **G2** | Tần suất báo cáo tiến độ < 0,5 lần/tuần ⇒ TC2.2 và TC2.4 −1 mức | Không thuộc CI/CD nhưng ảnh hưởng TC2.4 |

### 7.5. Kết luận ngắn

- **Về thiết kế:** kế hoạch bao phủ đủ các yêu cầu Mức 5 của TC2.6 (6 chặng, deploy tự động, phiên bản + rollback, giám sát, secret qua nền tảng) và các yêu cầu CI của TC2.4/TC2.5. Điểm yếu đã biết: gia hạn chứng chỉ thủ công, không sao lưu DB, tỉ lệ tuần có commit.
- **Về thực tế hôm nay:** hạ tầng (server, Docker, tên miền, HTTPS) đã sẵn sàng, nhưng **phần CI/CD thật sự (workflow, Dockerfile, health, test BE, repo GitHub) chưa làm**. Nghĩa là các điểm rubric TC2.6 hiện chưa có bằng chứng nào để chấm.
- **Mức có thể đạt cuối kỳ phụ thuộc** vào việc deploy tự động chạy được sớm và đều, vào tỉ lệ build xanh, và vào cách Khoa đếm tuần commit. Không có số liệu nào ở đây là kết quả đo.

---

## 8. Cách thu số liệu thật (để điền vào minh chứng và `TRACKING.md`)

| Số liệu | Lệnh / nguồn |
|---|---|
| Tỉ lệ run xanh | `gh run list --limit 100 --json conclusion,createdAt,event,headBranch` |
| Số lần deploy tự động | `gh api repos/<tổ-chức>/<repo>/deployments` (do dùng `environment: staging`) |
| Thời gian commit → staging | Chênh lệch giữa thời điểm push `develop` và thời điểm smoke test xanh (log Actions) |
| Tuần có commit / PR có review | `git log --since=... --format=%ad`, `gh pr list --state merged --json reviews` |
| Coverage, lint, Blocker/Critical, trùng lặp, secret | Artifact của CI (báo cáo Vitest, Sonar (tùy chọn), jscpd, gitleaks) |
| RAM server | `free -m`, `docker stats --no-stream` (ghi cả `farmnongviet`) |

Ghi vào `TRACKING.md` **chỉ** số đo thật; chưa đo ⇒ "N/A".

---

## 9. Danh sách việc còn lại (theo thứ tự)

1. **Bạn:** đổi mật khẩu root trên server; tạo Organization + 3 repo; khởi tạo git, devkit, đẩy `main`/`develop`; thêm Environment và Secrets cho cả BE và FE; hỏi GVHD 4 câu (cách đếm tuần commit; "build xanh" tính run nào; staging nhóm có được chấp nhận; quyền hội đồng).
2. **Tôi (đã soạn, chờ chạy thật):** Dockerfile BE và FE; `deploy.sh`; workflow CI, đóng gói, deploy, rollback; endpoint health BE và FE (đã có test); cấu hình gửi log. Còn lại: chạy thử trên GitHub và server, đo, sửa lỗi.
3. **Cùng làm:** chọn dịch vụ monitor + log hosted; test BE tối thiểu để CI không chạy 0 test; thu bằng chứng theo Mục 8.
4. **Định kỳ:** nhắc 2026-12-08 để gia hạn chứng chỉ trước 2027-01-07.

---

## 10. Giới hạn của tài liệu này

- Tôi **chưa chạy** bất kỳ workflow nào; mọi YAML là phác thảo.
- Các nhận định về gói miễn phí (GitHub Actions/GHCR cho repo public, SonarCloud, dịch vụ log/monitor) và việc ruleset hoạt động với gói Free **chưa kiểm chứng**.
- Giới hạn bộ nhớ/CPU trong `docker-compose.yml` là đề xuất chưa đo; RAM khả dụng ~1 GB dùng chung với một ứng dụng đang chạy thật.
- Rubric không định nghĩa rõ "staging", cách tính "build xanh" và "trải đều"; cần hỏi GVHD.
