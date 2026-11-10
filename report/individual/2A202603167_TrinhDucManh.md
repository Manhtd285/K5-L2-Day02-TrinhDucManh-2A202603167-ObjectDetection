# Báo cáo cá nhân — Ngày 2 Object Detection

Đổi tên file theo `MSSV_HoTen.md`, ví dụ `20241234_NguyenVanAn.md`. Điền kết quả thật, xóa dòng hướng dẫn khi nộp. Xem [quy định nộp](../../SUBMISSION.md).

## 1. Thông tin học viên

- Họ tên: Trịnh Đức Mạnh
- MSSV: 2A202603167
- Email: trinhducmanh204@gmail.com
- Lớp: 2A-lec-c401
- Link repo bài làm:https://github.com/Manhtd285/K5-L2-Day02-TrinhDucManh-2A202603167-ObjectDetection
- Link Colab đã chạy:https://colab.research.google.com/drive/1zMgL2vBlLIDWPx9c1j6n2YkawHjIeJsJ?usp=sharing

## 2. Schema và mini guideline

Dẫn tới [GUIDELINE_MINI.md](../../GUIDELINE_MINI.md). Tóm tắt ba ca mơ hồ đã quyết định, cách áp dụng schema và phần cần giảng viên làm rõ.
- Xe ở rất xa, mờ nhòe (drive_002): Quyết định bỏ qua không vẽ box vì xe quá bé, không rõ đặc trưng, tránh tạo box nhiễu (FP).
- Xe bán tải pickup (drive_006): Quyết định gán nhãn car (class 0) theo đúng schema quy định của bài lab (pickup/cabin nhỏ thuộc car, không phải truck).
- Xe van hộp dễ nhầm với bus/car (drive_038): Gán van (class 3) do thân dạng khối liền có cửa trượt hông, kích thước nhỏ hơn chuẩn xe khách bus.
## 3. Annotation và self-QC

- Số file nhãn train: 50
- Kết quả checker và lỗi đã xử lý: check_yolo_labels.py chạy đạt 50/50 file hợp lệ
- Danh sách ít nhất 10 ảnh đã rà bằng mắt: drive_001, drive_003, drive_005, drive_006, drive_009, drive_015, drive_024, drive_027, drive_031, drive_041.
- Lỗi bỏ sót/box/class phát hiện khi rà và cách sửa: Bỏ bớt các box thừa ở góc xa phía trên do công cụ auto-label phát hiện nhầm. Vẽ thêm các box xe bị che khuất một phần ở tiền cảnh. Chỉnh lại các box bị lỏng hoặc chồng lấn để bám sát viền xe nhìn thấy được.
- Commit khóa nhãn ban đầu: 5cd41e1

## 4. Gold QC và rework

| Chỉ số | Trước sửa | Sau sửa nếu có |
|---|---:|---:|
| TP |476 |560 |
| FP |626 |144 |
| FN |177 |93 |
| Precision |0.4319 |0.7955 |
| Recall |0.7289 |0.8576 |
| F1 |0.5425 |0.8254 |
| mean_iou_of_matches |0.8471 |0.8531 |
| passed |false |true |

Dẫn tới `outputs/annotation_evaluation.json` trong repo. Nếu rework, ghi ảnh, lỗi đã kiểm, quyết định sửa/giữ và lý do. Không suy nguyên nhân chỉ từ FP/FN. Không có rework thì ghi rõ.
- Nguyên nhân chính trước sửa: đánh rất nhiều box cho Xe ở rất xa, mờ nhòe và bỏ qua 1 số xe bị cắt ở biên ảnh: khiến FP và FN tăng vọt
- Hành động: Rà soát trực quan trên CVAT dựa trên ảnh overlay, xóa bớt các box xe quá xa không thuộc diện gán nhãn ở drive_003, drive_031,... bổ sung các xe bị thiếu ở drive_027, drive_041,...

## 5. Kết quả YOLO

- Runtime, GPU/CPU, phiên bản Ultralytics và Torch: Chạy trên GPU T4, Ultralytics 8.4.208, PyTorch 2.11.0
- Các tham số thay đổi so với notebook nếu có và lý do: Giữ nguyên mặc định theo notebook
- Đường dẫn best checkpoint trong phiên chạy: assets/yolo26_runs/vehicle_annotation/weights/best.pt

| Chỉ số trên 10 ảnh eval | Giá trị |
|---|---:|
| Precision |0.596 (tại epoch 32) / 0.444 (tại epoch 50) |
| Recall |0.547 (tại epoch 32) / 0.677 (tại epoch 50) |
| mAP50 |0.629 (tại epoch 32) / 0.589 (tại epoch 50) |
| mAP50–95 |0.393 (tại epoch 32) / 0.376 (tại epoch 50) |

Đặt cả 2 folder `assets/eval_predictions/` và `assets/yolo26_runs/` (giải nén từ `day2_colab_outputs.zip`) cạnh báo cáo và dẫn link tương đối. Không chỉ ghi số; chỉ ra ít nhất một ảnh và vật thể cụ thể.

Trả lời bốn câu hỏi cuối notebook:

1. Lớp nào recall thấp nhất? Ảnh nào minh họa?
- Lớp có Recall thấp nhất là truck (chỉ nhận diện đúng 1/5 mẫu, 4 mẫu còn lại bị nhận nhầm thành car).
- Ảnh minh họa: assets/eval_predictions/visuals/drive_052.jpg hoặc drive_059.jpg, nơi xe tải thùng bị mô hình dự đoán thành car do mất cân bằng dữ liệu và góc chụp xa.
2. Nếu mAP50 cao nhưng mAP50–95 thấp, cần kiểm điều gì trên box?
- Cần kiểm tra độ ôm sát và độ chặt chẽ (tightness) của bounding box. mAP50 chỉ đòi hỏi IoU 
≥
0.5
≥0.5, trong khi mAP50-95 tính trung bình các ngưỡng IoU khắt khe lên tới 0.95. Nếu box vẽ bị thừa viền, lỏng hoặc lệch mép xe, IoU thực tế sẽ thấp và kéo mAP50-95 xuống mạnh.
3. Lỗi class nào có thể liên quan guideline? Dữ kiện nào hỗ trợ nhận xét?
- Lỗi nhầm lẫn giữa truck và car.
- Dữ kiện: Ma trận nhầm lẫn cho thấy 4/5 mẫu truck bị gán thành car. Trong thực tế tập train, các loại xe tải nhỏ, xe bán tải cabin đơn/kép rất dễ bị gán nhầm lẫn với dòng SUV/xe con nếu guideline định nghĩa ranh giới giữa xe bán tải (car) và xe tải chở hàng (truck) chưa đủ rõ ràng.
4. Vì sao không dùng 10 ảnh eval để train? Vai trò validation của chúng trong notebook là gì?
- Không được dùng 10 ảnh eval để train vì cần giữ dữ liệu độc lập để đánh giá khách quan khả năng tổng quát hóa (generalization) của mô hình trên dữ liệu chưa từng thấy. Nếu đem train, mô hình sẽ bị data leakage và điểm số cao ảo (overfitting).
- Vai trò của 10 ảnh eval trong notebook: Đóng vai trò tập Validation giúp theo dõi sự hội tụ của mô hình qua từng epoch và dùng làm tiêu chí để lưu checkpoint tốt nhất (best.pt).
## 6. Khó khăn và cách xử lý

| Bước/thời điểm | Lỗi quan sát | Cách đã thử | Kết quả/còn thiếu |
|---|---|---|---|
|Import/Export CVAT |Đánh quá nhiều xe li ti ở chân trời |Mở trực quan trên CVAT, đặt ngưỡng xóa box siêu nhỏ |Giảm False Positive, tăng Precision |

## 7. Tự đánh giá theo rubric

Đối chiếu [RUBRIC.md](../../RUBRIC.md): phần nào đã có kết quả, phần nào còn thiếu hoặc chưa kiểm được. Không tự nhận hoàn thành bước chưa chạy.
- Đạt đầy đủ 50/50 file nhãn train, vượt qua checker cấu trúc.
- Đạt F1 (0.825 >= 0.80) và Mean IoU (0.853 >= 0.70) trên tập Gold.
- Hoàn thành chạy notebook Colab, xuất đầy đủ metrics và visuals.
- Báo cáo phân tích đầy đủ các câu hỏi theo yêu cầu bài học.
## 8. Công cụ AI và tài liệu tham khảo

Ghi công cụ đã dùng, dùng ở bước nào và phần đã tự kiểm tra; không dùng thì ghi rõ. Liệt kê nguồn ngoài repo được sử dụng. Không ghi mật khẩu/token hoặc đính kèm gold train.
- Sử dụng trợ lý AI agent (Antigravity) để hỗ trợ:
- Viết script tools/prelabel.py (sử dụng YOLO11x pretrained) để hỗ trợ gán nhãn sơ bộ ban đầu.
- Tạo ảnh overlay trực quan để đối chiếu nhanh các ca lỗi.
- Toàn bộ việc kiểm tra, gán nhãn chi tiết và nghiệm thu từng ảnh đều được tự tay thực hiện và rà soát trên CVAT.