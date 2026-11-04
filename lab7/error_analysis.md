# 26. Error analysis

Các xác suất dưới đây được làm tròn đến bốn chữ số thập phân.

## Ba dự đoán đúng

### 1. Cảm xúc tiêu cực rõ ràng

> “the acting was terrible”

- Nhãn mong đợi: **negative**
- Dự đoán: **negative**; P(positive) = 0,0000

Từ `terrible` thể hiện đánh giá tiêu cực trực tiếp về diễn xuất. Câu ngắn và không có phủ định hay ý kiến trái chiều, nên tín hiệu cảm xúc khá rõ ràng. Mô hình đưa ra nhãn phù hợp với cách hiểu này.

### 2. Tương phản giữa hai khía cạnh

> “the actors were excellent but the story was terrible and disappointing”

- Nhãn mong đợi: **negative**
- Dự đoán: **negative**; P(positive) = 0,0000

Câu khen diễn viên là `excellent` nhưng chê câu chuyện là `terrible and disappointing`. Mô hình dự đoán đúng nhãn tiêu cực của toàn câu dù có cả hai sắc thái. Các từ `actors` và `story` chỉ hai khía cạnh thuộc lĩnh vực phim; cảm xúc gắn với chúng đến từ các từ đánh giá xung quanh. Dự đoán đúng chưa cho biết mô hình đã xử lý mối quan hệ giữa hai vế như thế nào.

### 3. Review dài có ý kiến trái chiều

> “i watched this movie last night ... the story begins slowly but gradually becomes more interesting ...”

- Nhãn mong đợi: **positive**
- Dự đoán: **positive**; P(positive) = 1,0000

Review có 114 token và chỉ 100 token đầu được đưa vào mô hình. Trong phần được giữ, người viết đã đưa ra nhiều nhận xét tích cực như `enjoyed`, `convincing performances` và `beautiful`, dù cũng nói một số cảnh có thể ngắn hơn. Mô hình vẫn dự đoán đúng khi phần cuối bị cắt. Phần đầu chứa các tín hiệu tích cực, nhưng dự đoán này không chứng minh phần bị cắt không có ích.

## Ba dự đoán sai

### 1. Phủ định của từ tích cực

> “this movie is not good”

- Nhãn mong đợi: **negative**
- Dự đoán: **positive**; P(positive) = 0,9982

Theo cách hiểu thông thường, `not` đảo ý nghĩa tích cực của `good`, nên cả cụm mang sắc thái tiêu cực. Mô hình lại dự đoán positive với xác suất rất cao. Một khả năng là tín hiệu từ `good` lấn át tác dụng của phủ định, nhưng chỉ từ dự đoán này chưa thể xác định nguyên nhân bên trong mô hình.

### 2. Phủ định của từ tiêu cực

> “this movie is not bad at all”

- Nhãn mong đợi: **positive**
- Dự đoán: **negative**; P(positive) = 0,0000

Ở đây, `not bad at all` là lời đánh giá tích cực. Mô hình lại chọn negative, phù hợp với sắc thái của `bad` khi đứng riêng nhưng không phù hợp với cả cụm. Cùng với ví dụ trước, kết quả cho thấy hai trường hợp phủ định này đều bị phân loại sai; chưa thể từ đó kết luận rằng mô hình luôn bỏ qua `not`.

### 3. Review dài bị cắt mất phần kết

> “the movie starts with an interesting idea ... but the main performances are strong and the story remains engaging ...”

- Nhãn mong đợi: **positive**
- Dự đoán: **negative**; P(positive) = 0,2960

Review dài 130 token, với nhiều ý khen và chê xen kẽ. Mô hình chỉ nhận 100 token đầu; phần bị cắt bao gồm kết luận tích cực `its emotional depth and satisfying conclusion make it a rewarding experience overall`. Việc mất phần kết có thể góp phần làm dự đoán sai, nhất là khi phần đầu cũng chứa các nhận xét như `not particularly impressed` và `predictable`. Tuy nhiên, vẫn có ý tích cực trong phần được giữ; cần so sánh với dự đoán khi có thêm ngữ cảnh để biết việc cắt ảnh hưởng đến kết quả như thế nào.

## Những hiện tượng khác

**Contrast.** Với câu `the beginning was boring but the ending was absolutely wonderful`, mô hình dự đoán negative trong khi nhãn mong đợi là positive. Câu này cùng với ví dụ dự đoán đúng về `actors` và `story` cho thấy kết quả thay đổi giữa các câu có ý kiến trái chiều. Không thể kết luận chỉ từ hai câu rằng mô hình luôn ưu tiên vế trước hay vế sau `but`.

**Ambiguous sentiment.** Câu `some scenes were enjoyable while others were disappointing` chứa cả khen lẫn chê mà không nêu rõ đánh giá chung. Mô hình dự đoán negative, nhưng người đọc có thể xem câu này là cảm xúc pha trộn. Vì không có nhãn mong đợi cho câu này, không thể xếp dự đoán vào nhóm đúng hay sai.

**Rare word và domain-specific term.** Các thuật ngữ phim như `cinematography`, `screenplay`, `actors` và `story` cần được hiểu trong ngữ cảnh đánh giá. Một từ hiếm hoặc bị chuyển thành `<UNK>` có thể làm mất thông tin, nhưng chưa thể gắn lỗi của các ví dụ trên với một từ hiếm cụ thể nếu chưa kiểm tra token và tần suất của nó.

**Noise.** Review có thể chứa thẻ HTML, dấu câu hoặc ký hiệu biểu cảm. Khi tiền xử lý loại bỏ các ký hiệu này, một phần sắc thái có thể bị mất. Những ví dụ đã chọn chưa cho thấy noise là nguyên nhân gây lỗi, nên đây là khả năng cần kiểm tra thêm trên từng review.

## Attention của Transformer

Trong một attention pattern đã quan sát, token `sucks` nổi bật ở head 3: nhiều query gán trọng số tương đối cao cho token này. Người đọc cũng có thể xem `sucks` là từ quan trọng vì nó mang sắc thái tiêu cực. Với sáu câu được phân tích ở trên, chưa có quan sát attention tương ứng để xác nhận các token như `not`, `good`, `bad` hay `but` có nổi bật trong pattern hay không.

Cần phân biệt **model behavior** với **human interpretation**: dự đoán là hành vi mô hình; việc con người xem một từ là quan trọng là cách diễn giải. Attention visualization chỉ cho thấy phân phối attention weights giữa các token. Một trọng số cao không chứng minh token đó gây ra dự đoán, vì vậy không thể đồng nhất attention với lời giải thích cho quyết định của mô hình.
