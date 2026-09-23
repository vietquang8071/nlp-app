# Reflection — Lab 1: TF-IDF Search Engine

---

## Part I — Error Analysis

### ✅ Good Query 1: `"car vehicle driving automotive auto insurance"`

- **Query ID:** 2
- **Expected relevant documents:** [2640, 3358, 2208, 26928, 13861]
- **Retrieved documents (Default Tokenizer):**
  1. Doc 1342
  2. Doc 16788
  3. Doc 2640 ✓
  4. Doc 18966
  5. Doc 25388
- **P@5 = 0.2 | R@5 = 0.2 | RR = 0.333**

**Analysis:**

1. Doc 1342 đứng đầu vì có cosine similarity cao nhất — khả năng document này chứa nhiều từ trùng trực tiếp với query như "car", "vehicle", "auto", "insurance" với tần suất cao và document ngắn (TF cao).
2. Các từ đóng góp nhiều nhất: **"automotive"**, **"insurance"** — đây là các từ có IDF tương đối cao vì không phải common word, kết hợp với TF tốt tạo ra TF-IDF weight lớn.
3. **Có lexical overlap** — doc 2640 (relevant, rank 3) chia sẻ trực tiếp nhiều từ với query. Đây là lý do query này hoạt động tốt hơn nhiều query khác.
4. 4 relevant documents bị bỏ sót (3358, 2208, 26928, 13861). Có thể các documents này dùng từ đồng nghĩa hoặc diễn đạt khác (ví dụ: "automobile" thay vì "car", "driving lessons" thay vì "driving").
5. Failure (cho 4 docs bị sót) xuất phát từ **lexical matching** — TF-IDF chỉ match được exact token.

---

### ✅ Good Query 2: `"health medical doctor patient disease hospital"`

- **Query ID:** 4
- **Expected relevant documents:** [28824, 15913, 13861, 16199, 14038]
- **Retrieved documents (Default Tokenizer):**
  1. Doc 7478
  2. Doc 9660
  3. Doc 17065
  4. Doc 4135
  5. Doc 28824 ✓
- **P@5 = 0.2 | R@5 = 0.2 | RR = 0.2**

**Analysis:**

1. Doc 7478 đứng đầu vì nó có nhiều từ y tế overlap trực tiếp với query, với document length phù hợp khiến TF không bị pha loãng.
2. Các từ đóng góp nhiều: **"medical"**, **"disease"**, **"hospital"** — đây là những domain-specific terms với IDF cao (không xuất hiện trong mọi document) và TF đáng kể trong các docs liên quan.
3. **Có lexical overlap** giữa query và doc 28824 (relevant, rank 5). Các từ "health", "medical", "patient" là những từ phổ biến trong domain y tế nên tạo ra match.
4. 4 relevant documents bị bỏ sót (15913, 13861, 16199, 14038). Các documents này có thể sử dụng thuật ngữ y tế chuyên biệt hơn (ví dụ: "clinic" thay vì "hospital", "physician" thay vì "doctor", "diagnosis" thay vì "disease").
5. Failure xuất phát từ **vocabulary** và **lexical matching** — query dùng các từ phổ thông trong lĩnh vực y tế, nhưng relevant documents có thể dùng thuật ngữ chuyên ngành khác.

---

### ❌ Bad Query 1: `"fashion clothing wardrobe outfit boutique apparel"`

- **Query ID:** 9
- **Expected relevant documents:** [28168, 6940, 18978, 24634, 10311]
- **Retrieved documents (Default Tokenizer):**
  1. Doc 17438
  2. Doc 3142
  3. Doc 12879
  4. Doc 21809
  5. Doc 25093
- **P@5 = 0.0 | R@5 = 0.0 | RR = 0.0**

**Analysis:**

1. Doc 17438 đứng đầu vì có cosine similarity cao nhất với query — nó chứa một số từ trùng nhưng **không nằm trong tập relevant**. Có thể document này nói về "clothing" hoặc "fashion" ở ngữ cảnh khác (ví dụ: review sản phẩm, bài viết về xu hướng nói chung).
2. Các từ đóng góp: **"boutique"**, **"apparel"**, **"wardrobe"** có IDF cao vì hiếm, nhưng chưa đủ để match đúng relevant docs.
3. **Không có lexical overlap đáng kể** giữa retrieved docs và relevant docs — hệ thống retrieve được documents có chứa vài từ giống query nhưng ở context hoàn toàn khác, hoặc relevant documents dùng các từ khác như "style", "designer", "wear", "dress" thay vì chính xác các từ trong query.
4. **Tất cả 5 relevant documents đều bị bỏ sót.** Đây là complete failure.
5. Failure xuất phát từ **lexical matching** và **vocabulary**: domain thời trang có rất nhiều từ đồng nghĩa và cách diễn đạt đa dạng. Một bài về "thời trang" có thể dùng "dress", "wear", "style", "collection" mà không chứa "clothing" hay "apparel".

---

### ❌ Bad Query 2: `"investment finance stock market portfolio banking"`

- **Query ID:** 10
- **Expected relevant documents:** [23661, 16358, 2279, 19024, 6300]
- **Retrieved documents (Default Tokenizer):**
  1. Doc 10601
  2. Doc 19701
  3. Doc 18668
  4. Doc 8284
  5. Doc 14408
- **P@5 = 0.0 | R@5 = 0.0 | RR = 0.0**

**Analysis:**

1. Doc 10601 đứng đầu vì có similarity cao nhất — có thể chứa các từ "market", "stock", "finance" nhưng trong ngữ cảnh khác (ví dụ: "market research", "stock management" thay vì "stock market").
2. Các từ đóng góp nhiều: **"portfolio"**, **"banking"**, **"investment"** — các từ này có IDF trung bình khá (không quá phổ biến trong corpus tổng thể nhưng cũng không quá hiếm).
3. **Có lexical overlap cục bộ** — một số retrieved docs có thể chứa "market" hoặc "finance" nhưng ở context khác, không phải tài chính đầu tư.
4. **Tất cả 5 relevant documents đều bị bỏ sót.** Hoàn toàn thất bại.
5. Failure xuất phát từ nhiều yếu tố:
   - **Lexical matching**: "stock market" là cụm 2 từ nhưng TF-IDF xử lý từng token riêng biệt, nên "stock" match với bất kỳ document nào chứa "stock" (kho hàng, cổ phiếu, v.v.)
   - **IDF**: "market" và "finance" có thể xuất hiện trong nhiều document nên IDF thấp, giảm khả năng phân biệt
   - **Vocabulary**: relevant documents có thể sử dụng thuật ngữ chuyên ngành như "equity", "bond", "dividend", "asset allocation" — hoàn toàn khác biệt về mặt từ vựng

---

### 🔴 Failure Case Quan Trọng Nhất

**Query:** `"investment finance stock market portfolio banking"`

Đây là failure case nghiêm trọng nhất vì:

- P@5 = 0.0, R@5 = 0.0, RR = 0.0 trên **cả hai tokenizers** (Default và BERT).
- Domain tài chính rất giàu **synonym** và **polysemy**:
  - "stock" có thể nghĩa là cổ phiếu hoặc hàng tồn kho
  - "market" có thể là chợ, thị trường, hoặc marketing
  - Relevant documents có thể nói về "returns", "equity", "bonds", "mutual funds" — không overlap từ vựng với query
- TF-IDF không thể phân biệt **polysemy** (một từ nhiều nghĩa) nên "stock" match cả documents về kho hàng lẫn cổ phiếu.
- TF-IDF cũng không nhận ra **synonymy**: "investment" ≈ "putting money into assets" ≈ "capital allocation" — tất cả đều nói về đầu tư nhưng không share token nào.
- Quan trọng hơn, query chứa 6 từ riêng biệt, mỗi từ được xử lý độc lập (bag-of-words). Hệ thống không hiểu rằng "stock market" là một **phrase có nghĩa khác** với "stock" + "market" riêng lẻ.

Kết luận: Failure này cho thấy TF-IDF dựa trên lexical statistics hoàn toàn bất lực khi query và relevant documents không chia sẻ token chung. Cần một representation có khả năng nắm bắt **semantic similarity** thay vì chỉ **lexical overlap**.

---

## Part J — From Failure to the Next NLP Representation

### Hạn chế của TF-IDF

TF-IDF biểu diễn mỗi document là một sparse vector trong không gian từ vựng. Mỗi chiều tương ứng với một token duy nhất, và giá trị phản ánh mức độ quan trọng thống kê (TF × IDF) của token đó trong document. Điều này dẫn đến:

- `"heart attack"` ≠ `"myocardial infarction"` vì hai cụm từ không chia sẻ token nào
- `"car"` ≠ `"automobile"` vì lexical form khác nhau hoàn toàn
- `"investment"` ≠ `"capital allocation"` mặc dù cùng nghĩa

Trong khi đó, con người nhận ra: `heart attack ≈ myocardial infarction` về mặt ngữ nghĩa.

### Hypothesis: Dense Semantic Embeddings

**Giả thuyết:** Để biểu diễn similarity về nghĩa thay vì chỉ similarity về từ, ta cần chuyển từ **sparse lexical representation** sang **dense semantic representation**.

Cụ thể, thay vì biểu diễn mỗi document bằng vector thưa trong không gian |V| chiều (V = vocabulary size), ta nên biểu diễn mỗi document bằng một **dense vector** trong không gian d chiều nhỏ hơn nhiều (d ≈ 128–768), nơi:

- Các từ/cụm từ có nghĩa tương tự nằm gần nhau trong không gian vector
- Vector được học từ context (distributional semantics): "You shall know a word by the company it keeps" (J.R. Firth)
- Hai documents cùng chủ đề nhưng dùng từ khác nhau vẫn có vector gần nhau

Các phương pháp có thể thực hiện điều này:

1. **Word2Vec / GloVe**: Tạo word embeddings, rồi lấy trung bình vector của các từ trong document
2. **Sentence-BERT / Transformer-based embeddings**: Encode toàn bộ document thành một dense vector, có khả năng nắm bắt context và nghĩa tổng thể

---

## Câu hỏi cuối buổi

### Question 1: Tại sao TF-IDF tạo ra sparse representation?

Vì mỗi document chỉ chứa một tập nhỏ các từ so với toàn bộ vocabulary. Vector TF-IDF có kích thước |V| (vocabulary size = 254,766 với default tokenizer), nhưng mỗi document trung bình chỉ có ~361 token (với nhiều token trùng lặp). Do đó, phần lớn các chiều có giá trị 0, tạo ra matrix sparsity ~99.96%.

### Question 2: Tại sao một term xuất hiện trong hầu hết documents có IDF thấp?

Công thức IDF = log((1 + N) / (1 + df)) + 1. Khi df (document frequency) tiến gần đến N (tổng số documents), tỉ lệ (1+N)/(1+df) tiến về 1, nên log tiến về 0. Điều này hợp lý: một term xuất hiện ở mọi nơi (như "the", "is", "and") không mang lại thông tin phân biệt giữa các documents, nên nên có trọng số thấp.

### Question 3: Tại sao một term có IDF cao chưa chắc có TF-IDF cao trong một document?

Vì TF-IDF = TF × IDF. Một term hiếm trong corpus (IDF cao) nhưng chỉ xuất hiện 1 lần trong một document dài (TF thấp) sẽ có TF-IDF thấp. Ví dụ: từ "boutique" có IDF cao vì hiếm, nhưng nếu document có 1000 token và "boutique" chỉ xuất hiện 1 lần, TF = 1/1000 = 0.001, TF-IDF vẫn nhỏ.

### Question 4: Tại sao cosine similarity phù hợp với document vectors?

Vì cosine similarity đo **góc** giữa hai vectors, không phải **độ lớn**. Điều này quan trọng vì documents có độ dài khác nhau: một document dài sẽ có vector TF-IDF lớn hơn document ngắn, nhưng nếu hai documents nói về cùng chủ đề, vector của chúng sẽ cùng hướng. Cosine similarity bỏ qua sự khác biệt về độ dài, chỉ so sánh hướng — phản ánh đúng hơn sự tương đồng về nội dung.

### Question 5: Tại sao preprocessing có thể thay đổi search result?

Preprocessing thay đổi cách text được tokenize, ảnh hưởng trực tiếp đến vocabulary, TF, DF, và IDF. Trong thí nghiệm:

- Pipeline 1 (whitespace split): vocab = 473,388 → OOV rate = 24%
- Pipeline 2 (regex normalized): vocab = 193,837 → OOV rate = 24%
- Pipeline 3 (BERT subword): vocab = 28,339 → OOV rate = 0%

Khác biệt lớn: Pipeline 1 giữ dấu câu gắn liền với token (ví dụ "Missoula!" ≠ "Missoula"), tạo ra vocabulary lớn và nhiều spurious tokens. Pipeline 3 tách từ thành subwords nên vocabulary nhỏ hơn và OOV = 0%. Tuy nhiên, kết quả search (Mean P@5) lại tương đương nhau (0.06), cho thấy preprocessing một mình chưa đủ để cải thiện khi vấn đề cốt lõi là lexical matching.

### Question 6: Một failure case của TF-IDF search mà em quan sát được là gì?

Query `"investment finance stock market portfolio banking"` trả về P@5 = 0.0 trên cả hai engine. Không một relevant document nào được tìm thấy trong top-5, mặc dù query chứa 6 từ rất rõ ràng thuộc domain tài chính. Nguyên nhân: relevant documents sử dụng thuật ngữ khác (synonym) và "stock" bị polysemy (cổ phiếu vs. hàng tồn kho).

### Question 7: Failure case đó gợi ý nhu cầu về representation nào tiếp theo?

Cần **dense semantic representation** (word embeddings hoặc sentence embeddings) có khả năng:

- Nắm bắt synonym: "investment" ≈ "capital allocation"
- Giải quyết polysemy: phân biệt "stock (cổ phiếu)" vs. "stock (hàng tồn kho)" dựa trên context
- Biểu diễn similarity về **nghĩa** thay vì chỉ **từ vựng**

---

## 16. Reflection

### 1. Prediction nào của em sai?

Em dự đoán rằng BERT subword tokenizer sẽ cải thiện đáng kể kết quả search so với default tokenizer, vì nó có OOV rate = 0% và vocabulary nhỏ hơn (28,339 vs. 254,766). Tuy nhiên, kết quả thực tế cho thấy cả hai tokenizer đều có Mean P@5 = 0.06 và Mean R@5 = 0.06, thậm chí MRR của BERT (0.065) còn thấp hơn Default (0.078). Subword tokenization giải quyết được vấn đề OOV nhưng không giải quyết được vấn đề cốt lõi: **lexical mismatch** giữa query và relevant documents.

### 2. Kết quả nào bất ngờ nhất?

Bất ngờ nhất là Mean P@5 chỉ đạt 0.06 — tức trung bình chỉ tìm được 0.3 relevant document trong top 5 trên 10 queries. 7/10 queries có P@5 = 0.0 hoàn toàn. Điều này cho thấy TF-IDF search trên corpus tổng hợp (C4 web crawl) với các query chủ đề rộng hoạt động rất kém. Hệ thống retrieve được documents có chứa từ giống query nhưng hoàn toàn không relevant.

### 3. Experiment nào cung cấp evidence mạnh nhất?

Part H (Evaluation) cung cấp evidence mạnh nhất. Việc đánh giá hệ thống trên 10 queries với ground-truth relevant documents cho thấy bằng chứng định lượng rõ ràng: TF-IDF search engine có performance rất thấp (Mean P@5 = 0.06, MRR < 0.08) trên cả hai tokenizer. Đây là evidence không thể phản bác rằng lexical matching có giới hạn nghiêm trọng.

### 4. Failure case quan trọng nhất là gì?

Query `"investment finance stock market portfolio banking"` (Query 10) — P@5 = 0.0 trên cả hai engines. Đây là failure điển hình nhất của TF-IDF: domain tài chính có vocabulary đa dạng, nhiều synonym và polysemy, khiến lexical matching hoàn toàn thất bại.

### 5. Nếu được xây lại search engine, em sẽ thay đổi điều gì?

- Thêm **query expansion** (mở rộng query bằng synonym từ WordNet hoặc word embeddings) để giảm lexical mismatch.
- Sử dụng **BM25** thay TF-IDF (xử lý tốt hơn document length normalization).
- Kết hợp **hybrid search**: dùng TF-IDF cho lexical matching và dense embeddings (Sentence-BERT) cho semantic matching, sau đó combine scores.
- Thêm **stemming/lemmatization** trong preprocessing để nhóm các biến thể từ (ví dụ: "driving" → "drive", "banking" → "bank").

### 6. AI đã được sử dụng ở những phần nào và đóng góp cụ thể là gì?

AI (Antigravity/Claude) đã hỗ trợ ở phần chỉnh sửa reflection.md này: phân tích error cases từ dữ liệu results.csv, tổng hợp insights từ experiments.ipynb, và phân tích sâu hơn các câu hỏi để  trả lời cho 7 câu hỏi cuối buổi. Toàn bộ code implementation (MyTfIdfVectorizer.py), thí nghiệm (experiments.ipynb), và việc chạy evaluation đều do em tự thực hiện. AI giúp cấu trúc hóa phân tích và diễn đạt rõ ràng các observations.
