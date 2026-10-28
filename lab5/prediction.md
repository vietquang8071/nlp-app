# Prediction 1: Giữa TF-IDF + Logistic Regression và RNN + Embedding, model nào có khả năng xử lý word order trực tiếp hơn?
Answer: RNN + Embedding.
Reason: RNN xử lý văn bản theo thứ tự từng token và cập nhật hidden state dựa trên các token trước đó, giúp mô hình học thông tin về word order. Ngược lại, TF-IDF chủ yếu dựa trên tần suất và mức độ quan trọng của từ, không trực tiếp lưu giữ thứ tự từ khi sử dụng unigram.
Confidence: High.
# Prediction 2: Giữa RNN và LSTM model nào có khả năng xử lý dependency dài tốt hơn?
Answer: LSTM.
Reason: LSTM sử dụng cell state và các cổng (input, forget, output gates) để kiểm soát việc lưu trữ và loại bỏ thông tin. Nhờ đó, LSTM giảm ảnh hưởng của vanishing gradient và có khả năng học long-term dependencies tốt hơn RNN thông thường.
Confidence: High.
# Prediction 3: Nếu sequence length tăng từ 50 → 200 training của RNN sẽ thay đổi như thế nào?
Answer: Training sẽ chậm hơn, tiêu tốn nhiều bộ nhớ hơn và có thể khó hội tụ hơn.
Reason: Khi sequence length tăng gấp 4 lần, RNN phải thực hiện nhiều bước tính toán tuần tự hơn. Điều này làm tăng chi phí tính toán và khiến quá trình Backpropagation Through Time (BPTT) dài hơn, làm tăng nguy cơ vanishing hoặc exploding gradients.
Confidence: High
# Prediction 4: Nếu truncate toàn bộ review về 30 tokens, thông tin classification có thể bị ảnh hưởng không?
Answer: Ảnh hưởng hay không phụ thuộc vào thông tin chính của review có nằm ở 30 tokens đầu không.
Reason: Truncation có thể loại bỏ những từ hoặc câu quan trọng thể hiện sentiment, đặc biệt khi thông tin quyết định nằm ở cuối review. Tuy nhiên, nếu phần lớn thông tin quan trọng nằm trong 30 tokens đầu tiên, ảnh hưởng có thể không đáng kể. Truncation cũng có thể loại bỏ nhiễu trong một số trường hợp.
Confidence: High
# Prediction 5: LSTM có chắc chắn cho accuracy cao hơn RNN trên mọi dataset không?
Answer: Không.
Reason: Accuracy còn phụ thuộc vào nhiều yếu tố như dataset, hyperparameters chứ không chỉ phụ thuộc vào mô hình.
Confidence: High.