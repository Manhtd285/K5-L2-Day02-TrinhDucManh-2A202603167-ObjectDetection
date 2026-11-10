# Mini guideline — bài làm cá nhân

> Điền nội dung này trước khi bắt đầu gán nhãn. Giữ lại các quyết định sau khi self-QC.

## Định nghĩa lớp

| Lớp | Định nghĩa của bạn | Ví dụ/điểm phân biệt |
| --- | --- | --- |
| `car` |xe con, sedan, SUV, taxi, xe bán tải |Phân biệt với truck: xe bán tải nhỏ hoặc SUV chở người vẫn xếp vào car. Phân biệt với van: các dòng xe con 5-7 chỗ thông thường. |
| `truck` |xe tải chở hàng, xe đầu kéo |Có thùng chở hàng riêng biệt phía sau hoặc phần đầu kéo chuyên dụng; không gán cho xe bán tải thùng nhỏ/cabin đơn thuộc car. |
| `bus` |xe buýt, minibus chở khách |Thân xe dài, nhiều hàng ghế chở khách cỡ lớn. Phân biệt với van: bus có kích thước lớn hơn hẳn minivan/van chở hàng. |
| `van` |xe van, minivan chở hàng hoặc chở người |Thân xe dạng hộp liền khối, nhỏ hơn xe buýt nhưng lớn hơn hoặc có form dáng đặc thù khác xe sedan/SUV; thường có cửa trượt bên hông. |

## Quy tắc chung

- Box bám sát vật thể nghĩa là: Bounding box phải ôm sát các cạnh mép nhìn thấy được của thân xe
- Vật thể bị che khuất:Nếu xe bị che khuất một phần nhưng phần nhìn thấy vẫn đủ để nhận diện được loại xe thì vẽ box ôm trọn toàn bộ phần nhìn thấy đó. Nếu che quá 80-90% không còn nhận dạng được thì bỏ qua.
- Vật thể bị cắt bởi rìa ảnh:Kéo box chạm sát mép biên của ảnh (tọa độ giới hạn ở rìa ảnh 0 hoặc 1); không tự ý tưởng tượng hoặc vẽ lấn phần khuất ngoài ảnh.
- Vật thể rất nhỏ/mơ hồ: Các xe ở quá xa phía trên đường chân trời (kích thước quá nhỏ, mờ nhòe không phân biệt được hình dáng hoặc bánh xe) thì bỏ qua không gán nhãn để tránh gây nhiễu (False Positive) cho mô hình.

## Ghi lại quyết định cho ít nhất ba ca mơ hồ

| Ảnh | Tình huống | Quyết định cuối | Lý do theo schema |
| --- | --- | --- | --- |
| `drive_002` |Các xe ở rất xa phía ngã tư/chân trời phía trên ảnh, chỉ nhìn thấy một vệt mờ vài pixel. |Không gán nhãn (bỏ qua). |Kích thước quá nhỏ, mờ nhòe không đủ đặc trưng để nhận diện chắc chắn loại phương tiện; tránh tạo box nhiễu (FP). |
| `drive_006` |Xe bán tải (pickup) có thùng hở phía sau và cabin lái phía trước. |Gán nhãn car (Class 0). |Theo quy định schema: xe bán tải (pickup truck cabin nhỏ) thuộc nhóm car, không xếp vào truck. |
| `drive_038` |Xe van chở hàng dạng hộp nhưng kích thước hơi to, dễ phân vân giữa van và xe buýt nhỏ (bus). |Gán nhãn van (Class 3). |Form xe dạng hình hộp chữ nhật liền khối, chiều dài ngắn và chiều cao không đạt chuẩn xe buýt lớn; phù hợp với định nghĩa van. |
