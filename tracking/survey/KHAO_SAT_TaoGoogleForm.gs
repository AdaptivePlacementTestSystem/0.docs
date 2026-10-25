/**
 * KHẢO SÁT: Thực trạng bài kiểm tra tiếng Anh đầu vào / xếp lớp ở bậc Cao đẳng – Đại học
 * (phục vụ đề tài Adaptive Placement Test – CAT-Rasch, SRS v2.6)
 *
 * CÁCH DÙNG
 *  1. Mở https://script.google.com → Dự án mới → dán toàn bộ file này vào Code.gs.
 *  2. Chạy hàm createSurveyForm → cấp quyền (Google Forms + Drive).
 *  3. Xem Execution log: link chỉnh sửa, link gửi khảo sát và BẢNG ÁNH XẠ câu hỏi ↔ mã vấn đề.
 *  Mỗi lần chạy tạo MỘT FORM MỚI trong Drive của tài khoản đang chạy.
 *
 * ĐỐI TƯỢNG (khớp SRS Mục 1.1, 1.3): sinh viên CĐ/ĐH (chủ yếu năm nhất) và giảng viên/cán bộ khảo thí.
 *  - Sinh viên  : Phần 2 → (Phần 3 → 4 → 5 nếu đã từng thi bằng phần mềm) → Phần 6 → nộp.
 *  - Giảng viên : Phần 7 → nộp.
 *
 * MÃ VẤN ĐỀ dùng để gắn nhãn từng câu hỏi (không hiển thị cho người trả lời):
 *  P1  Đề cố định: dài, không hợp trình độ                       (SRS 1.1 – gạch đầu dòng 1)
 *  P2  Kết quả chỉ là điểm, không biết yếu ở đâu                  (SRS 1.1 – gạch đầu dòng 2)
 *  P3  Thiếu dữ liệu có cấu trúc để LMS/EduZ cá nhân hóa lộ trình (SRS 1.1 – gạch đầu dòng 3)
 *  RQ2 AI giải thích có cải thiện trải nghiệm / tự nhận biết điểm yếu không
 *  RQ3 Hồ sơ năng lực có đủ thông tin cho LMS/EduZ không
 *  SEC Lộ đề / công bằng / bảo mật (động lực của Randomized Top-5)
 *  CTX Bối cảnh người trả lời (để chia nhóm khi phân tích)
 *  NEED Nhu cầu / kỳ vọng tính năng (chỉ là bằng chứng nhu cầu, KHÔNG chứng minh hệ thống tốt hơn)
 *
 * GIỚI HẠN: khảo sát này KHÔNG trả lời RQ1 (CAT có chính xác ngang bài thi cố định dài gấp đôi không).
 * RQ1 cần dữ liệu thực nghiệm từ User Study (Tuần 9–11). Khảo sát này chỉ làm bằng chứng cho
 * Mục 1.1 (bối cảnh – động lực) và định hướng RQ2/RQ3.
 */

const SURVEY_TITLE = 'Khảo sát thực trạng bài kiểm tra tiếng Anh đầu vào / xếp lớp (Cao đẳng – Đại học)';
const SURVEY_DESCRIPTION =
  'Nhóm đang nghiên cứu hệ thống kiểm tra xếp lớp tiếng Anh thích ứng (CAT). ' +
  'Khảo sát tìm hiểu trải nghiệm thực tế của sinh viên và giảng viên với các bài kiểm tra tiếng Anh đầu vào hiện có. ' +
  'Thời gian: khoảng 5–7 phút. Câu trả lời ẩn danh, chỉ dùng cho mục đích học thuật; ' +
  'không có câu trả lời đúng hay sai. Câu có dấu * là bắt buộc.';
const CONFIRMATION_MESSAGE = 'Cảm ơn bạn đã dành thời gian tham gia khảo sát!';

const LIKERT_SATISFACTION = ['1 - Rất kém', '2 - Kém', '3 - Bình thường', '4 - Tốt', '5 - Rất tốt'];
const LIKERT_AGREE = ['1 - Hoàn toàn không đồng ý', '2 - Không đồng ý', '3 - Trung lập', '4 - Đồng ý', '5 - Hoàn toàn đồng ý'];

const SOFTWARE_OPTIONS = [
  'Hệ thống thi tự xây dựng của trường (nội bộ)',
  'Bài thi trên LMS (Moodle, Google Classroom…)',
  'Biểu mẫu trực tuyến (Google Forms…)',
  'VSTEP (đề thi trên máy)',
  'Aptis / Aptis ESOL',
  'TOEIC / TOEFL / IELTS trên máy',
  'Cambridge English Placement Test / Linguaskill',
];

function createSurveyForm() {
  const form = FormApp.create(SURVEY_TITLE);
  const questionTags = [];
  // Gắn nhãn cho câu vừa được thêm cuối form. Không phụ thuộc giá trị trả về của chuỗi setter
  // (một số setter của FormApp trả về undefined) và không dùng biến toàn cục.
  const tag = function (_ignored, codes) {
    const items = form.getItems();
    questionTags.push(codes + '  |  ' + items[items.length - 1].getTitle());
  };
  form.setDescription(SURVEY_DESCRIPTION)
    .setConfirmationMessage(CONFIRMATION_MESSAGE)
    .setCollectEmail(false)
    .setAllowResponseEdits(false)
    .setProgressBar(true)
    .setShowLinkToRespondAgain(false);

  // ========== PHẦN 1: Vai trò (rẽ nhánh sinh viên / giảng viên) ==========
  form.addSectionHeaderItem().setTitle('Phần 1. Bạn là ai?');
  const roleQ = form.addMultipleChoiceItem()
    .setTitle('Vai trò của bạn *')
    .setRequired(true);
  tag(roleQ, 'CTX');

  // ========== NHÁNH SINH VIÊN ==========
  const pbSV1 = form.addPageBreakItem().setTitle('Phần 2. Thông tin và kinh nghiệm của sinh viên');
  tag(form.addMultipleChoiceItem()
    .setTitle('Bạn đang học năm mấy? *')
    .setChoiceValues(['Năm 1', 'Năm 2', 'Năm 3', 'Năm 4 trở lên', 'Vừa trúng tuyển / chưa nhập học'])
    .setRequired(true), 'CTX');
  tag(form.addMultipleChoiceItem()
    .setTitle('Bậc đào tạo *')
    .setChoiceValues(['Cao đẳng', 'Đại học'])
    .setRequired(true), 'CTX');
  tag(form.addMultipleChoiceItem()
    .setTitle('Trình độ tiếng Anh tự đánh giá (khung CEFR) *')
    .setChoiceValues(['Dưới A2', 'A2', 'B1', 'B2', 'C1 trở lên', 'Chưa biết'])
    .setRequired(true), 'CTX');
  form.addTextItem().setTitle('Trường của bạn (không bắt buộc)');
  tag(form.addMultipleChoiceItem()
    .setTitle('Thiết bị bạn thường dùng khi làm bài thi trên phần mềm')
    .setChoiceValues(['Máy tính trong phòng máy của trường', 'Laptop cá nhân', 'Điện thoại', 'Máy tính bảng'])
    .showOtherOption(true), 'CTX');

  const screenQ = form.addMultipleChoiceItem()
    .setTitle('Bạn đã từng làm bài kiểm tra tiếng Anh đầu vào / xếp lớp BẰNG PHẦN MỀM (máy tính hoặc điện thoại) chưa? *')
    .setRequired(true);
  tag(screenQ, 'CTX');

  // ----- Phần 3: Phần mềm / hình thức đã dùng -----
  const pbSV2 = form.addPageBreakItem().setTitle('Phần 3. Bài kiểm tra bạn đã làm');
  tag(form.addCheckboxItem()
    .setTitle('Bạn đã dùng phần mềm / hình thức nào? (chọn nhiều) *')
    .setChoiceValues(SOFTWARE_OPTIONS)
    .showOtherOption(true)
    .setRequired(true), 'CTX');
  form.addTextItem()
    .setTitle('Tên bài kiểm tra / phần mềm GẦN ĐÂY NHẤT của bạn (các câu sau đánh giá bài này) *')
    .setRequired(true);
  tag(form.addMultipleChoiceItem()
    .setTitle('Bài đó thuộc dạng nào?')
    .setChoiceValues([
      'Mọi người làm cùng một đề cố định',
      'Mỗi người một đề khác nhau nhưng cùng độ khó',
      'Câu sau thay đổi theo kết quả các câu trước (thích ứng)',
      'Không rõ',
    ])
    .setRequired(true), 'P1');
  tag(form.addMultipleChoiceItem()
    .setTitle('Bài đó có bao nhiêu câu hỏi?')
    .setChoiceValues(['Dưới 20 câu', '20–30 câu', '31–50 câu', 'Trên 50 câu', 'Không nhớ']), 'P1');
  tag(form.addMultipleChoiceItem()
    .setTitle('Bạn làm bài hết khoảng bao lâu?')
    .setChoiceValues(['Dưới 20 phút', '20–30 phút', '31–45 phút', '46–60 phút', 'Trên 60 phút', 'Không nhớ']), 'P1');
  tag(form.addScaleItem()
    .setTitle('Độ dài bài thi so với mong đợi của bạn?')
    .setBounds(1, 5)
    .setLabels('Quá ngắn', 'Quá dài'), 'P1');
  tag(form.addMultipleChoiceItem()
    .setTitle('Bạn có nhận thấy có bạn khác đã biết trước câu hỏi / đề bị lặp lại không?')
    .setChoiceValues(['Có, rõ ràng', 'Có thể có', 'Không', 'Không biết']), 'SEC');

  // ----- Phần 4: Trải nghiệm -----
  form.addPageBreakItem().setTitle('Phần 4. Đánh giá trải nghiệm');
  tag(form.addGridItem()
    .setTitle('Mức hài lòng của bạn với bài kiểm tra gần đây nhất ở từng tiêu chí *')
    .setRows([
      'Đăng nhập / vào phòng thi dễ dàng',
      'Hướng dẫn trước khi thi rõ ràng',
      'Giao diện làm bài dễ dùng',
      'Tốc độ và độ ổn định (không treo, mất kết nối)',
      'Độ khó các câu hỏi phù hợp với trình độ của tôi',
      'Kết quả phản ánh đúng trình độ thật của tôi',
      'Tính công bằng và bảo mật',
    ])
    .setColumns(LIKERT_SATISFACTION)
    .setRequired(true), 'P1');
  tag(form.addCheckboxItem()
    .setTitle('Bạn đã gặp vấn đề nào? (chọn nhiều)')
    .setChoiceValues([
      'Mất kết nối / treo giữa chừng',
      'Không khôi phục được bài làm sau sự cố',
      'Giao diện khó dùng trên điện thoại',
      'Nhiều câu quá dễ làm tôi mất thời gian',
      'Nhiều câu quá khó làm tôi nản',
      'Đề lặp lại / bị lộ đề',
      'Không rõ cách tính điểm, xếp loại',
      'Không có vấn đề đáng kể',
    ])
    .showOtherOption(true), 'P1,SEC');
  tag(form.addScaleItem()
    .setTitle('Bạn có sẵn lòng giới thiệu bài kiểm tra / phần mềm này cho bạn bè không? (0–10) *')
    .setBounds(0, 10)
    .setLabels('Chắc chắn không', 'Chắc chắn có')
    .setRequired(true), 'P1');
  tag(form.addParagraphTextItem().setTitle('Điều bạn không hài lòng nhất hoặc muốn cải thiện nhất là gì?'), 'P1');

  // ----- Phần 5: Kết quả và phản hồi -----
  form.addPageBreakItem().setTitle('Phần 5. Kết quả bạn nhận được');
  tag(form.addMultipleChoiceItem()
    .setTitle('Bạn nhận kết quả khi nào?')
    .setChoiceValues(['Ngay sau khi nộp bài', 'Trong vòng 24 giờ', 'Sau 1–7 ngày', 'Sau hơn 7 ngày', 'Không nhận được']), 'P2'
  );
  tag(form.addCheckboxItem()
    .setTitle('Kết quả bạn nhận có những nội dung nào? (chọn nhiều)')
    .setChoiceValues([
      'Điểm số tổng',
      'Xếp loại theo CEFR (A1–C1…)',
      'Điểm theo từng kỹ năng (từ vựng, ngữ pháp…)',
      'Xem lại câu đã làm và đáp án đúng',
      'Giải thích vì sao đúng / sai',
      'Gợi ý nội dung cần học thêm',
      'Chỉ có kết quả đạt / không đạt hoặc điểm số',
    ]), 'P2,RQ2');
  tag(form.addGridItem()
    .setTitle('Mức đồng ý của bạn với các nhận định sau về kết quả bạn nhận được')
    .setRows([
      'Sau khi nhận kết quả, tôi biết rõ mình yếu ở mảng kiến thức nào',
      'Tôi biết mình mắc lỗi sai lặp lại ở dạng câu nào',
      'Kết quả giúp tôi biết nên học gì tiếp theo',
      'Kết quả giúp tôi chọn / được xếp vào lớp phù hợp',
    ])
    .setColumns(LIKERT_AGREE), 'P2,RQ2');

  // ----- Phần 6: Kỳ vọng (sinh viên) -----
  const pbExpectSV = form.addPageBreakItem().setTitle('Phần 6. Mong muốn của sinh viên');
  tag(form.addGridItem()
    .setTitle('Mức đồng ý của bạn với các nhận định sau')
    .setRows([
      'Tôi muốn bài kiểm tra ngắn hơn nhưng vẫn cho kết quả chính xác',
      'Tôi muốn được giải thích vì sao câu mình làm sai',
      'Lời giải thích do AI tạo, có giảng viên kiểm duyệt, là đáng tin',
      'Tôi muốn xem lại bài sau khi thi xong',
      'Tôi muốn nhận gợi ý lộ trình học cụ thể sau kiểm tra',
    ])
    .setColumns(LIKERT_AGREE)
    .setRequired(true), 'NEED,RQ2');
  tag(form.addMultipleChoiceItem()
    .setTitle('Thời lượng tối đa bạn chấp nhận cho một bài kiểm tra xếp lớp?')
    .setChoiceValues(['Dưới 20 phút', '20–30 phút', '30–45 phút', '45–60 phút', 'Trên 60 phút']), 'P1,NEED');
  tag(form.addCheckboxItem()
    .setTitle('Bạn lo ngại điều gì khi bài thi dùng thuật toán thích ứng và AI? (chọn nhiều)')
    .setChoiceValues([
      'Không hiểu vì sao bị hỏi câu này hoặc chấm như vậy',
      'Thiếu minh bạch về cách tính kết quả',
      'Lời giải thích của AI có thể sai',
      'Bảo mật dữ liệu cá nhân và kết quả thi',
      'Không thể quay lại sửa câu đã trả lời',
      'Không lo ngại gì',
    ])
    .showOtherOption(true), 'RQ2,NEED');
  form.addParagraphTextItem().setTitle('Góp ý thêm (không bắt buộc)');
  form.addTextItem()
    .setTitle('Email nếu bạn đồng ý để nhóm liên hệ mời tham gia thử nghiệm hệ thống (không bắt buộc)')
    .setValidation(FormApp.createTextValidation().requireTextIsEmail().build());
  pbExpectSV.setGoToPage(FormApp.PageNavigationType.SUBMIT); // sinh viên nộp tại đây, bỏ qua phần giảng viên

  // ========== NHÁNH GIẢNG VIÊN / CÁN BỘ KHẢO THÍ ==========
  const pbGV = form.addPageBreakItem().setTitle('Phần 7. Dành cho giảng viên / cán bộ khảo thí / quản trị');
  tag(form.addMultipleChoiceItem()
    .setTitle('Công việc chính của bạn trong kỳ kiểm tra đầu vào *')
    .setChoiceValues(['Giảng viên tiếng Anh', 'Cán bộ khảo thí / đào tạo', 'Quản trị / cán bộ CNTT vận hành phần mềm thi'])
    .showOtherOption(true)
    .setRequired(true), 'CTX');
  tag(form.addMultipleChoiceItem()
    .setTitle('Quy mô một đợt kiểm tra tiếng Anh đầu vào của đơn vị bạn')
    .setChoiceValues(['Dưới 50 sinh viên', '50–200', '201–500', 'Trên 500']), 'CTX');
  tag(form.addCheckboxItem()
    .setTitle('Hiện nay đơn vị bạn dùng hình thức nào? (chọn nhiều)')
    .setChoiceValues(['Thi giấy', 'Đề cố định trên phần mềm nội bộ', 'Trên LMS (Moodle…)', 'Google Forms', 'Chứng chỉ bên ngoài (VSTEP, Aptis…)', 'Đề thích ứng'])
    .showOtherOption(true), 'P1');
  tag(form.addCheckboxItem()
    .setTitle('Kết quả được dùng để làm gì? (chọn nhiều)')
    .setChoiceValues(['Xếp lớp theo trình độ', 'Miễn học phần tiếng Anh', 'Tư vấn lộ trình học cho sinh viên', 'Báo cáo cho nhà trường', 'Chỉ lưu trữ'])
    .showOtherOption(true), 'P2,P3');
  tag(form.addMultipleChoiceItem()
    .setTitle('Từ lúc thi xong đến lúc có danh sách xếp lớp mất bao lâu?')
    .setChoiceValues(['Ngay trong ngày', '1–3 ngày', '4–7 ngày', 'Hơn 7 ngày']), 'P3');
  tag(form.addGridItem()
    .setTitle('Mức đồng ý của bạn với các khó khăn hiện tại')
    .setRows([
      'Chấm và tổng hợp kết quả tốn nhiều công sức',
      'Điểm số không cho biết sinh viên yếu ở mảng nào',
      'Đề bị lặp hoặc lộ giữa các đợt, các nhóm',
      'Bài thi quá dài khiến sinh viên mệt hoặc nản',
      'Khó đưa dữ liệu kết quả vào LMS / hệ thống quản lý học tập',
      'Khó xây dựng và cập nhật ngân hàng câu hỏi chất lượng',
    ])
    .setColumns(LIKERT_AGREE)
    .setRequired(true), 'P1,P2,P3,SEC');
  tag(form.addCheckboxItem()
    .setTitle('Hồ sơ năng lực của sinh viên cần có thông tin nào để bạn dùng được? (chọn nhiều) *')
    .setChoiceValues([
      'Xếp loại CEFR tổng',
      'Điểm theo từng kỹ năng',
      'Các chủ điểm sinh viên hay sai',
      'Độ tin cậy của kết quả',
      'Thời gian làm bài và số câu đã làm',
      'Tỷ lệ phân bố trình độ của cả lớp / khóa',
      'Gợi ý học tập cho từng sinh viên',
    ])
    .showOtherOption(true)
    .setRequired(true), 'RQ3');
  tag(form.addCheckboxItem()
    .setTitle('Bạn muốn nhận dữ liệu kết quả theo hình thức nào? (chọn nhiều)')
    .setChoiceValues(['Xem trên bảng điều khiển (dashboard)', 'Tệp CSV / Excel', 'Tệp PDF', 'Tự động đưa vào LMS qua API / JSON'])
    .showOtherOption(true), 'RQ3,P3');
  tag(form.addMultipleChoiceItem()
    .setTitle('Bạn chấp nhận lời giải thích do AI tạo cho câu hỏi ở mức nào?')
    .setChoiceValues([
      'Chấp nhận nếu giảng viên có thể xem và sửa trước khi sinh viên thấy',
      'Chấp nhận nếu có ghi chú đây là nội dung do AI tạo',
      'Chỉ chấp nhận giải thích do giảng viên tự soạn',
      'Không chấp nhận dùng AI',
    ]), 'RQ2,SEC');
  tag(form.addMultipleChoiceItem()
    .setTitle('Thời lượng tối đa bạn chấp nhận cho một bài kiểm tra xếp lớp?')
    .setChoiceValues(['Dưới 20 phút', '20–30 phút', '30–45 phút', '45–60 phút', 'Trên 60 phút']), 'P1,NEED');
  form.addParagraphTextItem().setTitle('Góp ý thêm (không bắt buộc)');
  form.addTextItem()
    .setTitle('Email nếu bạn đồng ý để nhóm liên hệ phỏng vấn thêm (không bắt buộc)')
    .setValidation(FormApp.createTextValidation().requireTextIsEmail().build());

  // ========== Gán rẽ nhánh (sau khi mọi trang đã được tạo) ==========
  roleQ.setChoices([
    roleQ.createChoice('Sinh viên Cao đẳng / Đại học', pbSV1),
    roleQ.createChoice('Giảng viên / cán bộ khảo thí / quản trị', pbGV),
  ]);
  screenQ.setChoices([
    screenQ.createChoice('Rồi', pbSV2),
    screenQ.createChoice('Chưa (bỏ qua Phần 3–5)', pbExpectSV),
  ]);

  Logger.log('Link CHỈNH SỬA     : ' + form.getEditUrl());
  Logger.log('Link GỬI KHẢO SÁT  : ' + form.getPublishedUrl());
  Logger.log('--- BẢNG MÃ VẤN ĐỀ | CÂU HỎI (dùng khi phân tích) ---\n' + questionTags.join('\n'));
}
