"""Dựng SD_13, SD_14, SD_15 và cập nhật SD_01, SD_06 theo thiết kế đã chốt 14/11/2026 (Quyết định #136).

Chạy:  python _tools/build_sd_20261114.py
Mọi nhãn ASCII (không dấu) theo quy ước của các SD hiện có. Nội dung bám mã đã chạy thật (backend `feat/user-admin`,
`feat/user-import`), không phải thiết kế dự kiến.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SD_DIR = os.path.normpath(os.path.join(HERE, '..'))
ARCHIVE = r'D:\TLCN\_ARCHIVE_20261114'
sys.path.insert(0, HERE)
from sd_build import spec_from_xml, write_sd  # noqa: E402
import render_sd  # noqa: E402

A, B, C, E = 'actor', 'boundary', 'control', 'entity'

# ───────────── SD_13: Quan ly tai khoan SV/GV (UCADM09): danh sach, tao, sua ─────────────
SD13 = {
    'number': '13',
    'title': 'Quan ly tai khoan SV/GV (danh sach, tao, sua)',
    'participants': [
        ('Admin', A), ('Trang Tai khoan (S24)', B), ('UserAdminController', C), ('AccountUseCases', C),
        ('TemporaryPasswordGenerator', C), ('User', E), ('MailPort', E),
    ],
    'messages': [
        (0, 1, 'Mo tab Sinh vien hoac Giang vien, nhap tu khoa tim kiem()'),
        (1, 2, 'GET /students hoac /teachers ?q&page&pageSize (JWT, chi ADMIN; GV/SV bi 403)'),
        (2, 3, 'ListAccounts.execute(kind, q, page, pageSize)'),
        (3, 5, 'findAccounts(kind, q, page): tim theo MSSV/ma GV, email, ho ten; tab Giang vien gom ca Admin'),
        (5, 3, 'Tra ve trang tai khoan kem role va ma ho so (khong co mat khau, khong co ma bam)()'),
        (2, 1, 'Tra ve 200 {items, total, page, pageSize}()'),
        (1, 0, 'Hien bang: ho ten, MSSV/ma GV, email, trang thai, da doi mat khau; nut Sua/Khoa/Gui lai MK()'),
        (0, 1, 'Bam Them sinh vien (hoac Them giang vien), nhap MSSV/ma GV, ho ten, email, bam Luu()'),
        (1, 2, 'POST /students hoac /teachers {studentCode|teacherCode, fullName, email}'),
        (2, 2, 'Kiem DTO: truong la bi tu choi, email dung dinh dang (400 VALIDATION_FAILED)'),
        (2, 3, 'CreateAccount.execute(input): chuan hoa email chu thuong, cat khoang trang'),
        (3, 5, 'findByEmail + findByStudentCode (hoac findByTeacherCode) - kiem trung BR-02'),
        (5, 3, 'Khong trung (trung: 409 CONFLICT kem details.field = email | studentCode | teacherCode)()'),
        (3, 4, 'generate(): mat khau tam 12 ky tu du chu thuong, chu hoa, so, ky tu dac biet (crypto.randomInt)'),
        (3, 3, 'Bam argon2; tao User role STUDENT hoac TEACHER, authProvider LOCAL, mustChangePassword = true'),
        (3, 5, 'createAccount(user, profile): ghi user va ho so MSSV/ma GV trong MOT lenh ghi (dua ghi trung: DuplicateAccountError => 409)'),
        (5, 3, 'Xac nhan da luu()'),
        (3, 6, 'sendTemporaryPassword(email, ho ten, mat khau tam, MSSV) SAU KHI luu; loi gui chi ghi log, khong rollback (BR-05, #120)'),
        (3, 2, 'Tra ve tai khoan vua tao (khong kem mat khau)()'),
        (2, 1, 'Tra ve 201 Created()'),
        (1, 0, 'Thong bao "Da tao tai khoan. Mat khau tam da duoc gui qua email" va lam moi danh sach; trung email/MSSV bao ngay duoi o nhap()'),
        (0, 1, 'Bam Sua, doi ho ten hoac email (MSSV/ma GV chi doc), bam Luu()'),
        (1, 2, 'PATCH /students/:id hoac /teachers/:id {fullName?, email?}'),
        (2, 3, 'UpdateAccount.execute(kind, id, fullName, email)'),
        (3, 5, 'findAccountById(id, kind): sai loai hoac khong co => 404; email moi => findByEmail (trung => 409)'),
        (5, 3, 'Tai khoan hien tai()'),
        (3, 5, 'updateAccount(id, kind, {fullName?, email?})'),
        (3, 2, 'Tra ve tai khoan da cap nhat()'),
        (2, 1, 'Tra ve 200()'),
        (1, 0, 'Thong bao "Da cap nhat tai khoan" va lam moi danh sach()'),
    ],
}

# ───────────── SD_14: Thao tac tai khoan: khoa/mo khoa, gui lai mat khau tam, nang/thu hoi Admin ─────────────
SD14 = {
    'number': '14',
    'title': 'Thao tac tai khoan (khoa, gui lai mat khau, nang/thu hoi Admin)',
    'participants': [
        ('Admin', A), ('Trang Tai khoan (S24)', B), ('AccountActionsController', C), ('AccountUseCases', C),
        ('User', E), ('MailPort', E), ('JwtStrategy', C),
    ],
    'messages': [
        (0, 1, 'Bam Khoa (xac nhan) hoac Mo khoa tai khoan()'),
        (1, 2, 'POST /users/:id/lock hoac /users/:id/unlock (JWT, chi ADMIN)'),
        (2, 3, 'SetAccountActive.execute(actorId, targetId, isActive)'),
        (3, 4, 'findAccountByUserId(targetId): khong co => 404'),
        (4, 3, 'Tai khoan dich kem role()'),
        (3, 3, 'Khi KHOA: chan tu khoa chinh minh va khoa tai khoan Admin (403 FORBIDDEN); mo khoa khong bi chan; da dung trang thai thi khong ghi lai'),
        (3, 4, 'setActive(targetId, isActive)'),
        (3, 2, 'Tra ve tai khoan voi isActive moi()'),
        (2, 1, 'Tra ve 200()'),
        (1, 0, 'Hien trang thai Da khoa hoac Hoat dong; nut Khoa/Mo khoa doi theo()'),
        (0, 1, 'Bam Gui lai mat khau tam (xac nhan)()'),
        (1, 2, 'POST /users/:id/resend-temporary-password'),
        (2, 3, 'ResendTemporaryPassword.execute(targetId)'),
        (3, 4, 'findAccountByUserId(targetId): Admin => 403; cho phep ca khi da doi mat khau (BR-19)'),
        (4, 3, 'Tai khoan dich()'),
        (3, 3, 'Sinh mat khau tam 12 ky tu moi, bam argon2'),
        (3, 4, 'updatePassword(hash, mustChangePassword = true): passwordChangedAt = now nen token va mat khau cu mat hieu luc'),
        (3, 5, 'sendTemporaryPassword(...) sau khi luu; loi gui chi ghi log, khong rollback'),
        (3, 2, 'Tra ve tai khoan (khong kem mat khau)()'),
        (2, 1, 'Tra ve 200()'),
        (1, 0, 'Thong bao "Da dat lai mat khau tam va gui qua email"()'),
        (0, 1, 'Tab Giang vien: bam Nang len Admin hoac Thu hoi Admin (xac nhan)()'),
        (1, 2, 'PATCH /users/:id/role {role: ADMIN | TEACHER}'),
        (2, 3, 'ChangeAccountRole.execute(actorId, targetId, role)'),
        (3, 4, 'findAccountByUserId(targetId)'),
        (4, 3, 'Tai khoan dich kem role hien tai()'),
        (3, 3, 'Chi TEACHER <-> ADMIN (sinh vien: 400); Admin khong tu thu hoi minh (403) nen khong the mat Admin cuoi (BR-18)'),
        (3, 4, 'updateRole(targetId, role)'),
        (3, 3, 'Nhat ky kiem toan BR-18: chua co noi luu, hoan (no dong bo 14/11/2026)'),
        (3, 2, 'Tra ve tai khoan voi role moi()'),
        (2, 1, 'Tra ve 200()'),
        (1, 0, 'Thong bao Da nang len Admin hoac Da thu hoi quyen; danh sach doi huy hieu Admin()'),
        (6, 4, 'Request tiep theo cua nguoi bi khoa/doi quyen (token cu): findById(sub) doc isActive va role tu co so du lieu, khong tin role trong token'),
        (4, 6, 'Tra ve User (khoa => 401 ngay; role moi co hieu luc ngay; token cap truoc lan doi mat khau => 401)()'),
    ],
}

# ───────────── SD_15: Tong quan he thong cho Admin (UCADM05, F-29) ─────────────
SD15 = {
    'number': '15',
    'title': 'Tong quan he thong cho Admin (dashboard)',
    'participants': [
        ('Admin', A), ('Trang Tong quan (S36)', B), ('ReportingController', C), ('GetSystemOverviewUseCase', C),
        ('ExamRound', E), ('TestSession va LanguageProfile', E), ('Item va ItemBatch', E),
    ],
    'messages': [
        (0, 1, 'Mo Tong quan, hoac chon mot ky thi (chip Ky thi), hoac bam Lam moi()'),
        (1, 2, 'GET /reports/overview?examRoundId= (JWT, chi ADMIN; GV/SV bi 403; examRoundId phai la UUID, sai => 400)'),
        (2, 3, 'execute(examRoundId, now)'),
        (3, 4, 'Neu co examRoundId: findUnique(examRoundId); khong ton tai => 404 NOT_FOUND'),
        (4, 3, 'Ky thi()'),
        (3, 5, 'SV da thi: groupBy studentId, status = COMPLETED (gom TIMEOUT, khong gom ABANDONED), loc theo ky neu co'),
        (3, 5, 'Phan phoi CEFR: ho so moi nhat moi SV (distinct studentId, completedAt giam dan), loc theo ky neu co'),
        (5, 3, 'So SV da thi va so SV theo 6 muc CEFR (PRE_A1, A1, A2, B1, B2, C1_PLUS)()'),
        (3, 6, 'Thong ke trang thai cau: groupBy status (6 gia tri); cau vao ngan hang = FINAL_APPROVED'),
        (3, 6, 'Lo can xu ly: dem ItemBatch o READY_TO_ASSIGN, READY_TO_FINALIZE, FAILED, PARTIAL (IN_REVIEW cho GV nen khong tinh)'),
        (6, 3, 'So cau theo trang thai va so lo can xu ly (khong phu thuoc ky thi, BR-13)()'),
        (3, 4, 'findMany ky SCHEDULED/OPEN trong khung gio, kem so SV va cac phien (studentId, status)'),
        (4, 3, 'Cac ky thi ung vien()'),
        (3, 3, 'effectiveStatus(round, now) = OPEN (khong doc cot status, BR-10); chua thi = tong - dang thi - hoan thanh (SV bo do van tinh chua thi)'),
        (3, 2, 'Tra ve SystemOverview {4 so, cefrDistribution, itemStatusCounts, openRounds, generatedAt}()'),
        (2, 1, 'Tra ve 200()'),
        (1, 0, 'Hien 4 the so, thanh ngang CEFR va trang thai cau (chuyen Bieu do/Bang), bang ky thi dang mo; khong tu cap nhat theo chu ky()'),
    ],
}


def new_sd06():
    return {
        'number': '06',
        'title': 'Import tai khoan SV/GV (luoi tam, Luu chay nen)',
        'participants': [
            ('Admin', A), ('Trang Import tai khoan', B), ('UserImportController', C), ('ImportUseCases', C),
            ('ImportSaveWorker', C), ('Redis', E), ('PostgreSQL', E), ('MailQueue', E), ('SMTP Server', E),
        ],
        'messages': [
            (0, 1, 'Chon loai tai khoan (SV/GV), chon mot hoac nhieu file .xlsx (mau tai tu GET /users/import/template)()'),
            (1, 2, 'POST /users/import/upload?kind=STUDENT|TEACHER (multipart, tung file mot)'),
            (2, 2, 'Guard JWT va chi ADMIN; multer gioi han 2 MB (vuot: 413 IMPORT_FILE_INVALID)'),
            (2, 3, 'UploadImportFile.execute(adminId, kind, file)'),
            (3, 3, 'Doc .xlsx bang exceljs: kiem chu ky zip, tieu de cot dung loai, <= 1000 dong, chi lay van ban o; sai => 400 IMPORT_FILE_INVALID'),
            (3, 3, 'Kiem BR-03: thieu cot, sai email, trung trong file => rejected (loai khoi luoi, bao popup)'),
            (3, 5, 'load grid import:accounts:adminId:kind; dong da co trong grid bi bo qua (ignoredDuplicates)'),
            (5, 3, 'Tra ve grid hien tai (hoac chua co)()'),
            (3, 6, 'findTakenEmails + findTakenCodes(kind) cho cac dong con lai'),
            (6, 3, 'Tra ve email/MSSV/ma GV da ton tai => existing (popup rieng, khong vao grid, khong chan Luu)()'),
            (3, 5, 'store grid = grid cu + dong moi, lam moi TTL 30 phut; grid + dong moi > 1000 => 400, giu nguyen grid'),
            (3, 1, 'Tra ve {grid, rejected[{row, code, reason}], existing[{row, field, value}], added, ignoredDuplicates}()'),
            (1, 0, 'Hien luoi + popup dong bi loai + popup tai khoan da ton tai()'),
            (0, 1, 'Tai them file khac (lap lai tu upload), xoa tung dong hoac xoa ca luoi()'),
            (1, 2, 'DELETE /users/import/grid/:rowKey hoac DELETE /users/import/grid'),
            (2, 5, 'Xoa dong khoi grid (xoa het dong van giu khoa de phan biet voi het han)'),
            (0, 1, 'Click Luu()'),
            (1, 2, 'POST /users/import/save?kind='),
            (2, 3, 'SaveImport.execute(adminId, kind)'),
            (3, 5, 'load grid (khong co/het han: 410 IMPORT_GRID_EXPIRED; rong: 422 IMPORT_GRID_EMPTY); giu cho tac vu SET NX (dang chay: 409)'),
            (3, 4, 'run(adminId, kind, rows) chay nen, khong cho ket thuc'),
            (3, 1, 'Tra ve 202 {total}()'),
            (1, 2, 'GET /users/import/save-status?kind= (hoi moi 1 giay trong luc xu ly)'),
            (4, 6, 'Kiem trung lai email/MSSV; co trung => job FAILED CONFLICT kem dong trung, khong tao gi, giu grid'),
            (4, 4, 'Sinh mat khau tam 12 ky tu, bam argon2 song song (4 luong); mat khau chi o bo nho'),
            (4, 5, 'set trang thai job {PROCESSING, processed, total} moi 25 tai khoan (khong chua mat khau)'),
            (4, 6, 'createAccounts: tao TAT CA tai khoan va ho so trong MOT transaction (STUDENT hoac TEACHER, LOCAL, mustChangePassword = true)'),
            (6, 4, 'Xac nhan transaction thanh cong (loi => job FAILED UNKNOWN, khong tao tai khoan nao)()'),
            (4, 5, 'Xoa grid; set job DONE {created, queued}'),
            (4, 7, 'enqueueTemporaryPasswords(...) chi sau khi ghi DB thanh cong'),
            (2, 1, 'Tra ve trang thai {status, processed, total, created, queued}()'),
            (1, 0, 'Hien tien do, roi "Da tao N tai khoan, M email da xep hang gui" (ket qua cu con trong Redis khong hien lai khi mo trang)()'),
            (7, 8, 'Gui email mat khau tam (SmtpMailAdapter), song song nho, thu lai khi loi; that bai sau thu lai: ghi log, khong rollback (Admin dung Gui lai mat khau tam)'),
            (8, 7, 'Ket qua gui()'),
        ],
    }


def new_sd01():
    spec = spec_from_xml(os.path.join(SD_DIR, 'SD_01_DangNhapHeThong.xml'))
    names = [n for n, _ in spec['participants']]
    prov, user = names.index('AuthProvider'), names.index('User')
    spec['messages'] += [
        (prov, user, 'Moi request co token (JwtStrategy.validate): findById(sub) doc isActive, role, passwordChangedAt tu co so du lieu, khong tin role trong token'),
        (user, prov, 'Tra ve User (khoa => 401 ngay; role moi co hieu luc ngay; token cap truoc lan doi mat khau => 401)()'),
    ]
    return spec


def main():
    os.makedirs(ARCHIVE, exist_ok=True)
    for stem in ('SD_01_DangNhapHeThong', 'SD_06_ImportTaiKhoanSinhVien'):
        for ext in ('xml', 'png'):
            src = os.path.join(SD_DIR, f'{stem}.{ext}')
            dst = os.path.join(ARCHIVE, f'{stem}_truoc_20261114.{ext}')
            if os.path.exists(src) and not os.path.exists(dst):
                shutil.copy(src, dst)
    outputs = {
        'SD_13_QuanLyTaiKhoan.xml': SD13,
        'SD_14_ThaoTacTaiKhoan.xml': SD14,
        'SD_15_TongQuanHeThong.xml': SD15,
        'SD_06_ImportTaiKhoanSinhVien.xml': new_sd06(),
        'SD_01_DangNhapHeThong.xml': new_sd01(),
    }
    for name, spec in outputs.items():
        path = os.path.join(SD_DIR, name)
        write_sd(spec, path)
        png = render_sd.render(path)
        print(name, len(spec['messages']), 'thong diep ->', os.path.basename(png))


if __name__ == '__main__':
    main()
