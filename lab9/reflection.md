# Reflection

```text
Pretrained Transformer
          ↓
Contextual representations
       ↙       ↘
   [CLS]       Mỗi token
      ↓            ↓
Classification   Token classifier
      ↓            ↓
Nhãn cho câu     Nhãn cho từng token (NER)
```

Một pretrained Transformer có thể dùng cho cả sequence classification và token classification vì phần lớn kiến thức ngôn ngữ đã được học trong Transformer encoder. Trong giai đoạn pretraining, mô hình được huấn luyện trên lượng văn bản lớn để dự đoán hoặc khôi phục thông tin trong ngữ cảnh. Nhờ vậy, encoder học được cách biểu diễn từ và quan hệ giữa các từ trước khi được giao một tác vụ cụ thể.

Khi đưa một câu vào encoder, mỗi token nhận được một vector biểu diễn. Đây là contextual representation: vector của một từ phụ thuộc vào những từ xung quanh, chứ không chỉ là một mã cố định cho từ đó. Ví dụ, cùng một từ có thể mang ý nghĩa khác nhau trong hai câu khác nhau. Cơ chế self-attention giúp mỗi vị trí sử dụng thông tin từ các vị trí còn lại để tạo biểu diễn phù hợp với cả câu.

Với sequence classification, mô hình cần đưa ra một nhãn cho toàn bộ câu hoặc đoạn văn, chẳng hạn câu tích cực hay tiêu cực. BERT thường thêm token đặc biệt `[CLS]` ở đầu đầu vào. Sau khi đi qua Transformer, vector cuối cùng tại vị trí `[CLS]` đã tổng hợp thông tin từ toàn bộ câu. Ta đưa vector này vào một classification head, thường là một lớp tuyến tính, để tính điểm cho từng nhãn. Nhãn có điểm cao nhất trở thành kết quả của cả sequence.

Với token classification, mô hình cần dự đoán một nhãn cho từng từ, như nhãn BIO trong nhận dạng thực thể. Thay vì chỉ lấy vector `[CLS]`, ta dùng vector contextual representation ở từng vị trí token. Một token classifier dùng chung được áp dụng lên mỗi vector để tạo ra nhãn tương ứng. Các token đặc biệt như `[CLS]` và `[SEP]` không phải từ trong câu nên thường bị bỏ qua khi tính loss. Nếu tokenizer tách một từ thành nhiều subword, nhãn cũng cần được căn chỉnh với các mảnh đó; một cách phổ biến là chỉ tính loss trên subword đầu tiên.

Vì vậy, cùng một encoder pretrained có thể phục vụ hai tác vụ: kiến trúc Transformer và các trọng số đã học vẫn được giữ lại, còn prediction head thay đổi theo dạng đầu ra cần thiết. Với sequence classification, head đọc một vector đại diện cho cả câu; với token classification, head đọc vector của từng token. Khi fine-tuning, loss từ head sẽ cập nhật cả head lẫn encoder, giúp biểu diễn ngôn ngữ chung thích nghi với dữ liệu và nhãn của tác vụ mới.
