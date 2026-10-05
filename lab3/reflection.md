# Reflection: Từ Word2Vec đến Transformer

---

## 1. Bảng so sánh các phương pháp biểu diễn từ (Representation Comparison)

Dưới đây là bảng hoàn thành theo yêu cầu của **Mục 27** trong đề bài:

| Representation | Context-dependent? | Sparse/Dense | Một từ có nhiều vector? |
| :--- | :---: | :---: | :---: |
| **TF-IDF**  | **Không** | **Sparse** | **Không** |
| **Co-occurrence Matrix**  | **Không** | **Sparse** | **Không** |
| **Word2Vec**  | **Không** | **Dense** | **Không** |
| **Contextual Embedding** | **Có** | **Dense** | **Có** |

---

### Phân tích chi tiết từng tiêu chí:

1. **TF-IDF (LAB 01):**
   * *Context-dependent (Không):* Trọng số của từ chỉ phản ánh tần suất thống kê xuất hiện trong văn bản ($TF$) so với toàn bộ kho ngữ liệu ($IDF$). Nó không thay đổi ý nghĩa ngữ cảnh cụ thể của từ trong từng câu.
   * *Sparse/Dense (Sparse):* Vector tài liệu có số chiều bằng toàn bộ kích thước từ điển ($|V|$), trong đó phần lớn các vị trí đều bằng $0$.
   * *Một từ có nhiều vector? (Không):* Mỗi từ chỉ tương ứng với một chỉ mục  và một trọng số thống kê duy nhất.

2. **Co-occurrence Matrix (LAB 03 - Core):**
   * *Context-dependent (Không):* Vector được xây dựng bằng cách cộng dồn số lần đồng xuất hiện trên toàn bộ corpus. Vector của một từ là một hàng cố định trong ma trận $|V| \times |V|$.
   * *Sparse/Dense (Sparse):* Kích thước ma trận cực lớn ($29,381 \times 29,381$), nhưng độ thưa lên tới $> 98.9\% - 99.7\%$ là các giá trị $0$.
   * *Một từ có nhiều vector? (Không):* Mỗi từ vựng chỉ sở hữu đúng một hàng vector đếm duy nhất trong ma trận.

3. **Word2Vec (LAB 03 - Neural):**
   * *Context-dependent (Không):* Dù Word2Vec dùng cửa sổ ngữ cảnh trong lúc huấn luyện (CBOW/Skip-gram), nhưng sau khi hoàn thành huấn luyện, ma trận trọng số được "đóng băng" thành một bảng tra từ điển tĩnh. Bất kể từ xuất hiện trong câu nào, vector lấy ra từ `model.wv[word]` luôn giữ nguyên một bộ trọng số duy nhất.
   * *Sparse/Dense (Dense):* Vector đã được nén từ kích thước từ điển $|V|$ xuống số chiều nhỏ ($d = 50, 100, 300$), hầu hết các phần tử đều là số thực liên tục khác $0$.
   * *Một từ có nhiều vector? (Không):* Mỗi từ chỉ được biểu diễn bằng một vector tĩnh duy nhất.

4. **Contextual Embedding (Transformer, BERT, RoBERTa):**
   * *Context-dependent (Có):* Biểu diễn của từ được tính toán động tại thời điểm suy luận, dựa trên toàn bộ các từ xung quanh trong câu thông qua cơ chế **Self-Attention**.
   * *Sparse/Dense (Dense):* Các vector đầu ra có số chiều cố định (ví dụ $d = 768$ hoặc $1024$) chứa giá trị thực dày đặc.
   * *Một từ có nhiều vector? (Có):* Cùng một từ (cùng chuỗi ký tự) nhưng xuất hiện ở các câu khác nhau sẽ được mô hình sinh ra các vector biểu diễn hoàn toàn khác nhau tương ứng với từng ngữ nghĩa cụ thể.

---

## 2. Tại sao `bank` cần contextual representation?

### 2.1. Bản chất của vấn đề: Đa nghĩa (Polysemy / Homonymy)
Xét hai câu ví dụ kinh điển trong đề bài:
1. *Câu A (Tài chính):* `"I deposited money in the bank."`
   * Ngữ cảnh xung quanh: `deposited`, `money`, `account`, `cash`.
2. *Câu B (Địa lý / Tự nhiên):* `"We sat on the river bank."`
   * Ngữ cảnh xung quanh: `sat`, `river`, `water`, `boat`, `shore`.

Ở đây, từ `"bank"` là một từ đa nghĩa (homonym) mang hai khái niệm hoàn toàn tách biệt: **tổ chức tài chính (financial institution)** và **bờ sông/bờ đê (sloping land beside a body of water)**.

---

### 2.2. Giới hạn chết người của Static Word Embeddings (Word2Vec)
Trong Word2Vec và ma trận Co-occurrence (LAB 03):
* Mô hình chỉ gán duy nhất một vector $v_{bank} \in \mathbb{R}^d$ cho từ khóa `"bank"`.
* Trong quá trình tối ưu hàm mục tiêu, vector $v_{bank}$ bị "giằng co" giữa hai lực kéo đối nghịch:
  $$\mathcal{L} \propto \text{Context}(\text{money, deposit}) + \text{Context}(\text{river, water})$$
* **Hậu quả về mặt hình học vector:** Vector của `"bank"` buộc phải hội tụ về một vị trí trung bình có trọng số nằm lơ lửng ở giữa cụm từ tài chính và cụm từ sông nước.
* **Hệ quả trong ứng dụng thực tế:**
  * Vector của `"bank"` không còn thuần khiết đại diện cho bất kỳ nghĩa nào.
  * Khi người dùng tìm kiếm câu: *"river bank"* hoặc *"bank robbery"*, tích vô hướng cosine giữa từ `"bank"` và tài liệu sẽ bị nhiễu: tìm kiếm tài liệu địa lý nhưng hệ thống lại trả về bài viết ngân hàng và ngược lại.
