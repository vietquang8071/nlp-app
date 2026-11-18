# Phân tích lỗi

Mình đã xem kết quả trích xuất thông tin trong `results/ie_evaluation/ie_metrics.csv` và `results/ie_evaluation/ie_errors.csv`. Trên 30 câu tin tức này, F1 vi mô là 0,909. Lỗi dễ thấy nhất là mô hình đôi khi tách tên người thành nhiều phần nhỏ. Vì tập đánh giá khá nhỏ, các ví dụ dưới đây chỉ phản ánh kết quả trên tập này.

## Dự đoán thừa (FP)

Đây là các thực thể được dự đoán nhưng không khớp với một thực thể hoàn chỉnh trong nhãn đúng. Mình chọn 5 trong số 7 đoạn dự đoán thừa có trong kết quả.

| Văn bản | Nhãn đúng | Dự đoán | Loại lỗi | Giải thích |
|---|---|---|---|---|
| Elon Musk met officials in Berlin. | PERSON: Elon Musk | PERSON: El | Dự đoán thừa; sai ranh giới | Mô hình chỉ gán hai chữ đầu của tên là một thực thể người. |
| Elon Musk met officials in Berlin. | PERSON: Elon Musk | PERSON: on Musk | Dự đoán thừa; sai ranh giới | Đoạn này bắt đầu giữa tên, nên riêng nó không khớp với thực thể đúng. |
| Cristiano Ronaldo traveled to Madrid. | PERSON: Cristiano Ronaldo | PERSON: rist | Dự đoán thừa; sai ranh giới | Mô hình chỉ dự đoán một phần của tên. |
| Cristiano Ronaldo traveled to Madrid. | PERSON: Cristiano Ronaldo | PERSON: C | Dự đoán thừa; sai ranh giới | Mô hình trả về mỗi ký tự đầu tiên như một thực thể. |
| Cristiano Ronaldo traveled to Madrid. | PERSON: Cristiano Ronaldo | PERSON: iano Ronaldo | Dự đoán thừa; sai ranh giới | Đoạn dự đoán bị thiếu phần đầu của tên đúng. |

## Bỏ sót thực thể (FN)

Ở các trường hợp này, mô hình không dự đoán được toàn bộ thực thể đúng thành một đoạn. Trong ba trường hợp, mô hình chỉ trả về các mảnh của tên.

| Văn bản | Nhãn đúng | Dự đoán | Loại lỗi | Giải thích |
|---|---|---|---|---|
| Elon Musk met officials in Berlin. | PERSON: Elon Musk | PERSON: El; PERSON: on Musk | Bỏ sót thực thể; sai ranh giới | Không mảnh nào khớp với toàn bộ tên, nên thực thể người bị bỏ sót khi đánh giá theo đoạn chính xác. |
| Sam Altman spoke at an OpenAI event in San Francisco. | ORG: OpenAI | Không dự đoán ORG | Bỏ sót thực thể | Mô hình không trích xuất tổ chức này khỏi câu. |
| Cristiano Ronaldo traveled to Madrid. | PERSON: Cristiano Ronaldo | PERSON: C; PERSON: rist; PERSON: iano Ronaldo | Bỏ sót thực thể; sai ranh giới | Tên bị tách thành nhiều mảnh thay vì được dự đoán thành một thực thể hoàn chỉnh. |
| Satya Nadella met officials in Washington. | PERSON: Satya Nadella | PERSON: Sa; PERSON: tya Nadella | Bỏ sót thực thể; sai ranh giới | Mô hình tách tên, nên không có đoạn nào khớp với toàn bộ tên đúng. |
| Jensen Huang presented NVIDIA technology in Taipei. | ORG: NVIDIA | Không dự đoán ORG | Bỏ sót thực thể | NVIDIA có trong câu nhưng không được nhận diện là tổ chức. |

## Lỗi ranh giới

Các ví dụ này cho thấy điểm bắt đầu hoặc kết thúc của đoạn dự đoán chưa đúng. Một số trường hợp cũng xuất hiện ở hai bảng trên: khi tên bị tách, các mảnh có thể tạo thành dự đoán thừa, còn tên đầy đủ lại bị bỏ sót.

| Văn bản | Nhãn đúng | Dự đoán | Loại lỗi | Giải thích |
|---|---|---|---|---|
| Elon Musk met officials in Berlin. | PERSON: Elon Musk | PERSON: El | Sai ranh giới; có thể do căn chỉnh các mảnh từ (subword) | Đoạn dự đoán kết thúc trước khi hết tên đúng. |
| Elon Musk met officials in Berlin. | PERSON: Elon Musk | PERSON: on Musk | Sai ranh giới; có thể do căn chỉnh các mảnh từ (subword) | Đoạn dự đoán bắt đầu sau khi tên đúng đã bắt đầu. |
| Cristiano Ronaldo traveled to Madrid. | PERSON: Cristiano Ronaldo | PERSON: C | Sai ranh giới; có thể do căn chỉnh các mảnh từ (subword) | Đoạn chỉ gồm ký tự đầu tiên của tên đúng. |
| Cristiano Ronaldo traveled to Madrid. | PERSON: Cristiano Ronaldo | PERSON: iano Ronaldo | Sai ranh giới; có thể do căn chỉnh các mảnh từ (subword) | Đoạn bắt đầu giữa từ “Cristiano”, nên bị thiếu phần đầu. |
| Satya Nadella met officials in Washington. | PERSON: Satya Nadella | PERSON: tya Nadella | Sai ranh giới; có thể do căn chỉnh các mảnh từ (subword) | Đoạn dự đoán bị thiếu phần đầu của “Satya”. |

Nhìn chung, lỗi rõ nhất trong các ví dụ này là ranh giới của tên người. Mô hình thường tìm được đúng khu vực trong câu, nhưng đôi khi chỉ trả về một phần tên. OpenAI và NVIDIA là hai trường hợp khác: mô hình bỏ sót hoàn toàn các tổ chức này.
