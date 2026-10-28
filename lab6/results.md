# Tại sao phép trừ max(x) không làm thay đổi kết quả softmax?

Phép trừ `max(x)` không làm thay đổi kết quả **Softmax** vì \(e^{-\max(x)}\) xuất hiện ở cả tử và mẫu nên có thể triệt tiêu. Mục đích của phép trừ này là đảm bảo **Numerical Stability (ổn định số học)**, tránh hiện tượng **overflow** khi tính hàm mũ với các giá trị lớn. Sau khi trừ `max(x)`, mọi phần tử đều không dương, giúp tính toán Softmax ổn định hơn mà không làm thay đổi phân phối xác suất về mặt toán học.

## Experiment 1 - Attention distribution

|   | Token | Score | Attention |
|---:|---|---:|---:|
| 0 | The | 2.540950 | 0.037225 |
| 1 | movie | 4.158792 | 0.187698 |
| 2 | was | -0.610697 | 0.001593 |
| 3 | surprisingly | -7.351800 | 0.000002 |
| 4 | good | 0.522541 | 0.004946 |
| 5 | despite | -1.575245 | 0.000607 |
| 6 | a | -0.260621 | 0.002260 |
| 7 | very | 4.165400 | 0.188942 |
| 8 | slow | 4.976555 | 0.425215 |
| 9 | beginning. | 3.944623 | 0.151512 |

## Experiment 2: Change Query vector

|   | Token | Score2 | Attention2 |
|---:|---|---:|---:|
| 0 | The | 0.426322 | 0.049030 |
| 1 | movie | 2.850984 | 0.553964 |
| 2 | was | 0.633943 | 0.060344 |
| 3 | surprisingly | 1.195883 | 0.105847 |
| 4 | good | 0.443467 | 0.049878 |
| 5 | despite | 1.110184 | 0.097154 |
| 6 | a | -1.201532 | 0.009627 |
| 7 | very | 0.739957 | 0.067093 |
| 8 | slow | -1.607075 | 0.006418 |
| 9 | beginning. | -3.905030 | 0.000645 |

## Experiment 3: Attention Visualization

### Query token: cat

|   | Key Token | Attention Weight |
|---:|---|---:|
| 4 | i | 0.144744 |
| 7 | is | 0.131080 |
| 6 | yesterday | 0.118888 |
| 10 | [SEP] | 0.103104 |
| 8 | sleeping | 0.097081 |
| 9 | . | 0.090027 |
| 5 | adopted | 0.089179 |
| 3 | that | 0.064227 |
| 2 | cat | 0.061458 |
| 0 | [CLS] | 0.053746 |
| 1 | the | 0.046466 |

### Query token: adopted

|   | Key Token | Attention Weight |
|---:|---|---:|
| 6 | yesterday | 0.212031 |
| 7 | is | 0.125877 |
| 4 | i | 0.103351 |
| 8 | sleeping | 0.098437 |
| 2 | cat | 0.096061 |
| 5 | adopted | 0.081968 |
| 3 | that | 0.080235 |
| 10 | [SEP] | 0.061069 |
| 9 | . | 0.057831 |
| 0 | [CLS] | 0.042726 |
| 1 | the | 0.040413 |

### Query token: sleeping

|   | Key Token | Attention Weight |
|---:|---|---:|
| 10 | [SEP] | 0.160421 |
| 7 | is | 0.135738 |
| 6 | yesterday | 0.123593 |
| 2 | cat | 0.105415 |
| 9 | . | 0.097660 |
| 5 | adopted | 0.085815 |
| 4 | i | 0.085544 |
| 3 | that | 0.062235 |
| 8 | sleeping | 0.054081 |
| 0 | [CLS] | 0.046492 |
| 1 | the | 0.043005 |

## Experiment 4 — RNN context vs Attention context

|   | Model | Accuracy | F1 | Training time (s) | Parameters |
|---:|---|---:|---:|---:|---:|
| 0 | LSTM | 0.8334 | 0.8328 | 78.53 | 1,313,410 |
| 1 | Attention | 0.8362 | 0.8356 | 40.35 | 1,296,770 |

Trong Experiment 4, khác biệt nằm ở cách hai model tạo **vector đại diện cho cả câu**:

| Model | Cách tạo representation |
|---|---|
| **LSTM** | Đọc token theo thứ tự; lấy hidden state cuối `h_n[-1]` làm vector đại diện câu, rồi đưa vector đó vào classifier. |
| **Attention** | Tạo một vector đã ngữ cảnh hóa cho từng token bằng self-attention; sau đó lấy trung bình các vector của token không phải padding để đại diện câu. |

LSTM mã hóa thứ tự qua quá trình đọc tuần tự. Attention trong notebook cho mỗi token nhìn tới các token khác, nhưng phần cài đặt không thêm positional encoding; sau bước mean pooling, representation của câu không giữ thông tin thứ tự trực tiếp. Cả hai đều tạo vector 64 chiều trước classifier.

## Application:

|   | Sentence | Prediction | Probability | Expected | Correct |
|---:|---|---|---:|---|---|
| 0 | I like this movie. | Negative | 0.9891 | Positive | False |
| 1 | I do not like this movie. | Negative | 0.9991 | Negative | True |
| 2 | I thought this movie would be bad, but it was actually excellent. | Negative | 0.6613 | Positive | False |
