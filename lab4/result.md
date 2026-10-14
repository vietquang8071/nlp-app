# Báo Cáo Kết Quả Thực Nghiệm: Sentiment Classification (IMDB)

---

## 1. Experiment 1 — Dataset Inspection & Tiền Xử Lý Trùng Lặp

### 1.1. Thống kê tập dữ liệu ban đầu
* **Total samples**: 50,000
* **Number of classes**: 2
* **Classes**: `['positive', 'negative']`

#### Phân bố nhãn ban đầu (Class Distribution)
| Sentiment | Count | Percentage (%) |
| :--- | :---: | :---: |
| `positive` | 25,000 | 50.0% |
| `negative` | 25,000 | 50.0% |

---

### 1.2. Thống kê độ dài văn bản (Document Length Statistics)
*Đơn vị tính: số lượng từ (words)*

| Chỉ số (Metric) | Giá trị (Value) |
| :--- | :---: |
| **Count** | 50,000.00 |
| **Mean** | 231.16 |
| **Std** | 171.34 |
| **Min** | 4.00 |
| **25%** | 126.00 |
| **50% (Median)** | 173.00 |
| **75%** | 280.00 |
| **Max** | 2,470.00 |

---

### 1.3. Đánh giá chất lượng dữ liệu & Xử lý trùng lặp
* **Empty/whitespace-only reviews**: `0`
* **Missing reviews**: `0` (0.00%)
* **Missing labels**: `0` (0.00%)
* **Rows belonging to duplicate review groups**: `824`
* **Duplicate occurrences (excluding first copies)**: `418`

> [!IMPORTANT]
> **Xử lý làm sạch trùng lặp**: Đã thực hiện loại bỏ 418 bản sao trùng lặp bằng lệnh `df.drop_duplicates(subset=["review"])`.
> * **Số lượng mẫu sau khi xóa trùng lặp**: **49,582 mẫu**.
> * **Phân chia Train / Test (80% - 20%)**:
>   * **Tập Train (80%)**: 39,665 mẫu.
>   * **Tập Test (20%)**: **9,917 mẫu** (giúp loại bỏ hoàn toàn nguy cơ rò rỉ dữ liệu giữa tập train và test).

#### Ví dụ các bài đánh giá bị trùng lặp (Examples of duplicate reviews):
| # | Số lần trùng | Nội dung đánh giá (Review text) |
| :-: | :---: | :--- |
| **1** | 5 | Loved today's show!!! It was a variety and not solely cooking (which would have been great too). Very stimulating and captivating, always keeping the viewer peeking around the corner to see what was coming up next. She is as down to earth and as personable as you get, like one of us which made the show all the more enjoyable. Special guests, who are friends as well made for a nice surprise too. Loved the 'first' theme and that the audience was invited to play along too. I must admit I was shocked to see her come in under her time limits on a few things, but she did it and by golly I'll be writing those recipes down. Saving time in the kitchen means more time with family. Those who haven't tuned in yet, find out what channel and the time, I assure you that you won't be disappointed. |
| **2** | 4 | Hilarious, clean, light-hearted, and quote-worthy. What else can you ask for in a film? This is my all-time, number one favorite movie. Ever since I was a little girl, I've dreamed of owning a blue van with flames and an observation bubble.<br /><br />The cliché characters in ridiculous situations are what make this film such great fun. The wonderful comedic chemistry between Stephen Furst (Harold) and Andy Tennant (Melio) make up most of my favorite parts of the movie. And who didn't love the hopeless awkwardness of Flynch? Don't forget the airport antics of Leon's cronies, dressed up as Hari Krishnas: dancing, chanting and playing the tambourine--unbeatable! The clues are genius, the locations are classic, and the plot is timeless.<br /><br />A word to the wise, if you didn't watch this film when you were little, it probably won't win a place in your heart today. But nevertheless give it a chance, you may find that "It doesn't matter what you say, it doesn't matter what you do, you've gotta play." |
| **3** | 3 | When i got this movie free from my job, along with three other similar movies.. I watched then with very low expectations. Now this movie isn't bad per se. You get what you pay for. It is a tale of love, betrayal, lies, sex, scandal, everything you want in a movie. Definitely not a Hollywood blockbuster, but for cheap thrills it is not that bad. I would probably never watch this movie again. In a nutshell this is the kind of movie that you would see either very late at night on a local television station that is just wanting to take up some time, or you would see it on a Sunday afternoon on a local television station that is trying to take up some time. Despite the bad acting, cliché lines, and sub par camera work. I didn't have the desire to turn off the movie and pretend like it never popped into my DVD player. The story has been done many times in many movies. This one is no different, no better, no worse. <br /><br />Just your average movie. |
| **4** | 3 | Nickelodeon has gone down the toilet. They have kids saying things like "Oh my God!" and "We're screwed"<br /><br />This show promotes hate for people who aren't good looking, or aren't in the in crowd. It say that sexual promiscuity is alright, by having girls slobbering over shirtless boys. Not to mention the overweight boy who takes off his shirt. The main characters basically shun anyone out of the ordinary. Carly's friend Sam, who may be a lesbian, beats the snot out of anybody that crosses her path, which says it's alright to be a b**ch. This show has so much negativity in it that nobody should watch it! I give it a 0 out of 10!!! |
| **5** | 3 | I see that C. Thomas Howell has appeared in many movies since his heyday in the 80s as an accomplished young actor.<br /><br />I bought this DVD because it was cheap and in part for the internet-related plot and to see how much older C. Thomas Howell is; I do not recall seeing him in any movies since the 1980s.<br /><br />In just a few words: what a very big disappointment. I give some low budget movies a chance, but this one started out lame. Within the first 15 minutes of the movie, this elusive woman is chatting with an Asian guy in a chatroom. They basically stimulate themselves to their own chat, she then insists on meeting the participant in person. She meets him, has sex, ties him up and then murders him in cold blood. The plot then deteriorates further.<br /><br />The plot is thin and flimsy and the acting is very stiff. Do not bother renting it much less purchasing it, even if it is in the $1 DVD bin. I plan to take my copy of the DVD to Goodwill. I am truly amazed that any of the prior reviewers here gave this movie a bad rating. |
| **6** | 3 | You do realize that you've been watching the EXACT SAME SHOW for eight years, right? I could understand the initial curiosity of seeing strangers co-exist on an Island, but you'd think that after watching unkempt, stink-ladened heroes run roughshod through the bush with an egg on a spoon for half a decade would be enough to get you to commit to something a little more original (and interesting).<br /><br />And I'm not even speaking of the shows validity which for the record I find questionable. It's just hard to suspend disbelief for "Bushy Bill" eating a rat when the entire crew of producers and camera people are housed in an air conditioned make-shift bio-dome sipping frosty mochcinno's with moxy.<br /><br />What's the appeal here? I don't care about these people or their meandering lives. I just don't get it. But if you DO find yourself being captivated by hairy, unwashed people, I suggest you turn off your TV and just take a trip to your local bus station where you can see people like this in their TRUE habitat. They call them HOMELESS PEOPLE, and free of charge, you can sit back and marvel in their uncanny ability to retrieve various cigarette debris from a plethora of garbage canisters, eventually striking "pay-dirt" and fashioning a homemade Dr. Frankenstein-styled cancer-stick, all the while begging people for change for food when the stink of "Aqua Velva" on their breath is enough to suggest otherwise. And the best part? Much like Survivor, every week one member of the tribe "Leaves" the "Island" when they are unceremoniously sent packing to the local Institution when the frightening unmedicated state of full-blown schizophrenia kicks into gear! Now THAT'S ENTERTAINMENT! |
| **7** | 3 | This show comes up with interesting locations as fast as the travel channel. It is billed as reality but in actuality it is pure prime time soap opera. It's tries to use exotic locales as a facade to bring people into a phony contest & then proceeds to hook viewers on the contestants soap opera style.<br /><br />It also borrows from an early CBS game show pioneer- Beat The Clock- by inventing situations for its contestants to try & overcome. Then it rewards the winner money. If they can spice it up with a little interaction between the characters, even better. While the game format is in slow motion versus Beat The Clock- the real accomplishment of this series is to escape reality. <br /><br />This show has elements of several types of successful past programs. Reality television, hardly, but if your hooked on the contestants, locale or contest, this is your cup of tea. If your not, this entire series is as I say, drivel dripping with gravy. It is another show hiding behind the reality label which is the trend it started in 2000.<br /><br />It is slick & well produced, so it might last a while yet. After all, so do re-runs of Gilligan's Island, Green Acres, The Beverly Hillbillies & The Brady Bunch. This just doesn't employ professional actors. The intelligence level is about the same. |
| **8** | 3 | Robert Jordan is a television star. Robert Jordan likes things orderly, on time and properly executed. In his world children are to be seen, not heard. So why would Mr. Jordan want to become the master of a rambunctious band of Boy Scouts? Ratings. His staff figures that if learns how to interact with the youth, they will be more inclined to watch his show. Of course watching Jordan cope comprises most of the fun.<br /><br />Like Mr. Belvedere and Mr. Belvedere Goes to College this one is sure to please.<br /><br />ANYONE INTERESTED IN OBTAINING A COPY OF THIS FILM PLEASE WRITE TO ME AT: IAMASEAL2@YAHOO.COM |
| **9** | 3 | How has this piece of crap stayed on TV this long? It's terrible. It makes me want to shoot someone. It's so fake that it is actually worse than a 1940s sci-fi movie. I'd rather have a stroke than watch this nonsense. I remember watching it when it first came out. I thought, hey this could be interesting, then I found out how absolutely, insanely, ridiculously stupid it really was. It was so bad that I actually took out my pocket knife and stuck my hand to the table.<br /><br />Please people, stop watching this and all other reality shows, they're the trash that is jamming the networks and canceling quality programming that requires some thought to create. |
| **10** | 2 | The sun was not shining, it was too wet to play, so I went to the movies, that cold, cold, wet date day.<br /><br />"The Cat in the Hat" was the name of the flick, and when it was over, my stomach was sick.<br /><br />Mike Myers played the Cat, his humor was lame, and kids needn't see this, the humor was not tame.<br /><br />the film was like drinking milk, from a rabid cow, so it IS fun to have fun, yet the filmmakers didn't know how.<br /><br />This film, in short is atrocious. The acting was bad, the plot was tweaked too much, and the humor was surprisingly very crude.<br /><br />It starts with Conrad and Sally, A rule breaker and a future sheriff. When their Mother has to go to work, she gets Mrs. Kwan to babysit. Possibly the lone funny part in the movie is when Mrs. Kwan is watching a Taiwanese court room, a `la C-SPAN. She soon falls asleep, and here comes the Cat.<br /><br />The film starts to spiral out of control. The Cat came to try to let the kids have some fun. He's got Thing 1 and Thing 2, Who suddenly start trashing the house. He improvises a TV Infomercial, and accidentally slices his tail off. And when the Cat goes full Carmen Miranda, it's not funny. Possibly his only funny disguise is as a hippie activist. And there's a fish who tries warning the kids about the Cat.<br /><br />Too bad he didn't warn us this film was as much fun as sour milk, or chopping your tail off.<br /><br />Soon the kids are outside looking for the family dog, who has the key to a crate on his collar. If the crate is not locked soon, their house will be home to the Cat's universe. Here it gets a little more interesting, but not enough to save the film.<br /><br />The acting, overall, is horrible. Mike Meyers brings his brand of irreverent Austin Powers humor to the Cat, Saying things like "You dirty ho" and imagining himself as a woman for the rest of his life after a whack in the testicles while posing as a pinata. Spencer Breslin is great as the trouble-making Conrad, and Dakota Fanning is cute as Sally, though they alone are not enough to save this horrendous Aortic Dissection waiting to kill John Ritter(accident waiting to happen). Alec Baldwin's slick and slimey Lawrence Quinn is disgusting, ever trying to woo the kids mom, who is played by Kelly Preston. And Sean Hayes is Mr. Humberfloob, Mom's boss, and is also the voice of the fish. The latter three are also bland.<br /><br />Overall, if I were a parent I would not take my kids who are into potty humor, cause there's plenty of it and more. Save your $7.00 and see something else. As the late great Dr. Seuss once said,<br /><br />It is fun to have fun, But you have to know how. Really, Universal, stop! Theodore's already turning over in his grave.<br /><br />Like my Mom always says, "Curiousity killed the Cat".- The Cat In The Hat * out of ***** |

---

### Câu hỏi: Dataset có imbalance không?
> **Trả lời:** Không. Tập dữ liệu hoàn toàn cân bằng với tỷ lệ chính xác là 50% nhãn `positive` (25,000 mẫu) và 50% nhãn `negative` (25,000 mẫu).

---

## 2. Experiment 2 — Baseline: TF-IDF + Logistic Regression

### Báo cáo phân loại (Classification Report)
*Đánh giá trên tập kiểm thử sau khi xóa trùng lặp: **9,917 mẫu**.*

| Lớp (Class) | Precision | Recall | F1-Score | Support |
| :--- | :---: | :---: | :---: | :---: |
| `negative` | 0.87 | 0.84 | 0.86 | 4,939 |
| `positive` | 0.85 | 0.87 | 0.86 | 4,978 |
| **Accuracy** | | | **0.86** | **9,917** |
| **Macro Avg** | 0.86 | 0.86 | 0.86 | 9,917 |
| **Weighted Avg** | 0.86 | 0.86 | 0.86 | 9,917 |

---

## 3. Experiment 3 — Representation Comparison

### 3.1. Word2Vec + Logistic Regression

| Lớp (Class) | Precision | Recall | F1-Score | Support |
| :--- | :---: | :---: | :---: | :---: |
| `negative` | 0.86 | 0.85 | 0.85 | 4,939 |
| `positive` | 0.85 | 0.86 | 0.86 | 4,978 |
| **Accuracy** | | | **0.86** | **9,917** |
| **Macro Avg** | 0.86 | 0.86 | 0.86 | 9,917 |
| **Weighted Avg** | 0.86 | 0.86 | 0.86 | 9,917 |

---

### 3.2. TF-IDF + Linear SVC

| Lớp (Class) | Precision | Recall | F1-Score | Support |
| :--- | :---: | :---: | :---: | :---: |
| `negative` | 0.90 | 0.89 | 0.90 | 4,939 |
| `positive` | 0.89 | 0.90 | 0.90 | 4,978 |
| **Accuracy** | | | **0.90** | **9,917** |
| **Macro Avg** | 0.90 | 0.90 | 0.90 | 9,917 |
| **Weighted Avg** | 0.90 | 0.90 | 0.90 | 9,917 |

---

### 3.3. Bảng so sánh hiệu năng các mô hình

| # | Representation | Classifier | Accuracy | Precision | Recall | F1 |
| :-: | :--- | :--- | :---: | :---: | :---: | :---: |
| **0** | TF-IDF | Logistic Regression | 0.8582 | 0.8585 | 0.8582 | 0.8582 |
| **1** | Avg Word2Vec | Logistic Regression | 0.8555 | 0.8556 | 0.8555 | 0.8555 |
| **2** | **TF-IDF** | **Linear SVM** | **0.8961** | **0.8962** | **0.8961** | **0.8961** |

---

### Câu hỏi: Tại sao hai representation tạo ra kết quả khác nhau?
> **Trả lời:**
> 
> Kết quả thực nghiệm cho thấy TF-IDF kết hợp với Linear SVC đạt hiệu năng tốt nhất trong ba cấu hình, với accuracy khoảng 89.6% (~90%) và F1-score của hai lớp đạt 0.90. Một nguyên nhân có thể là TF-IDF giữ lại các đặc trưng từ vựng có giá trị phân biệt cao, đặc biệt là những từ và cụm từ biểu thị cảm xúc. Linear SVC có khả năng học ranh giới phân loại hiệu quả trên không gian đặc trưng văn bản sparse.
> 
> Trong khi đó, Word2Vec Average tạo ra biểu diễn dense có khả năng phản ánh sự tương đồng ngữ nghĩa giữa các từ. Tuy nhiên, phép lấy trung bình làm mất thông tin thứ tự từ và không trực tiếp mô hình hóa các quan hệ như phủ định. Vì vậy, những đặc trưng quan trọng đối với phân loại cảm xúc có thể bị làm mờ. Kết quả cho thấy biểu diễn ngữ nghĩa không nhất thiết vượt trội hơn biểu diễn từ vựng trong mọi bài toán; hiệu quả phụ thuộc vào đặc tính của dữ liệu và phương pháp phân loại.

---

## 4. Experiment 4 — Word Order

### 4.1. Độ tương đồng Cosine (Cosine Similarity)

| Cặp câu kiểm thử | Nội dung kiểm thử | Cosine Similarity |
| :--- | :--- | :---: |
| **$S_1$ vs $S_2$** | `"this movie is good"` vs `"this movie is not good"` | **0.9633** |
| **$S_3$ vs $S_4$** | `"not bad it is good"` vs `"not good it is bad"` | **1.0000** |

---

### 4.2. Kết quả dự đoán của các mô hình

| # | Câu (Sentence) | Nội dung văn bản (Text) | Avg W2V Predict | W2V P(Positive) | W2V P(Negative) | TF-IDF Predict | TF-IDF P(Positive) |
| :-: | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **0** | S1 (Positive) | `this movie is good` | `positive` | 81.5% | 18.5% | `positive` | 80.3% |
| **1** | S2 (Negative) | `this movie is not good` | `negative` | 11.7% | 88.3% | `negative` | 35.3% |
| **2** | S3 (Positive - Đảo từ) | `not bad it is good` | `negative` | 0.0% | 100.0% | `negative` | 26.0% |
| **3** | S4 (Negative - Đảo từ) | `not good it is bad` | `negative` | 0.0% | 100.0% | `negative` | 4.3% |

---

### Câu hỏi: Representation này có hiểu được vai trò của not không?
> **Trả lời:**
> 
> Word2Vec Average có thể phản ứng với từ phủ định “not”, nhưng chưa thực sự hiểu được vai trò ngữ nghĩa của từ này. Cụ thể, với câu “This movie is good”, mô hình dự đoán Positive với xác suất 81.5%, trong khi với câu “This movie is not good”, xác suất Positive giảm xuống 11.7% và xác suất Negative tăng lên 88.3%. Điều này cho thấy mô hình có khả năng học được các tín hiệu thống kê liên quan đến từ phủ định. Tuy nhiên, cosine similarity giữa hai câu vẫn đạt 0.9633, cho thấy vector biểu diễn của chúng có hướng rất gần nhau. Đặc biệt, mô hình dự đoán sai câu “not bad it is good” thành Negative với xác suất 100%, mặc dù câu này được gán nhãn Positive. 
> 
> Nguyên nhân có thể là phép lấy trung bình các word embedding không giữ được thứ tự từ và không mô hình hóa trực tiếp mối quan hệ phủ định giữa các từ, khiến các tín hiệu cảm xúc như “not”, “bad” và “good” bị kết hợp mà không thể hiện đầy đủ ý nghĩa của cả câu. Vì vậy, Word2Vec Average có thể học được một số đặc trưng liên quan đến phủ định, nhưng chưa biểu diễn hiệu quả các quan hệ ngữ nghĩa phức tạp trong câu.

---

## 5. Experiment 5 — n-gram Features

### Bảng kết quả so sánh Unigram vs Bigram

| # | Features | Vocabulary | F1 (Macro) | Training Time (s) |
| :-: | :--- | :---: | :---: | :---: |
| **0** | **Unigram** | 33,549 | 0.8955 | 15.51s |
| **1** | **Uni + Bigram** | **224,227** | **0.9069** | **37.03s** |

---

### Câu hỏi: Vì sao bigram có thể giúp classification nhưng đồng thời làm feature space lớn hơn?
> **Trả lời:**
> 
> Bigram có thể cải thiện khả năng phân loại văn bản vì nó biểu diễn các cặp từ liên tiếp, giúp mô hình nắm bắt một phần ngữ cảnh mà unigram không thể hiện được. Ví dụ, với hai câu “this movie is good” và “this movie is not good”, nếu chỉ sử dụng unigram, mô hình chỉ ghi nhận các từ riêng lẻ như not và good, nên khó xác định chính xác mối quan hệ phủ định giữa chúng. Khi sử dụng bigram, mô hình có thể tạo ra đặc trưng not good, giúp nhận diện cụm từ thường biểu thị cảm xúc tiêu cực và cải thiện khả năng phân loại. 
> 
> Tuy nhiên, việc bổ sung bigram cũng làm feature space lớn hơn vì mỗi cặp từ liên tiếp có thể trở thành một đặc trưng mới. Chẳng hạn, với từ vựng gồm $V$ từ, số unigram tối đa là $V$, còn số bigram có thể lên đến $V^2$ nếu xét mọi cặp từ có thể có. Trong thực tế, số bigram phụ thuộc vào các cặp từ xuất hiện trong dữ liệu. Feature space lớn hơn làm tăng bộ nhớ cần thiết, chi phí tính toán và nguy cơ overfitting khi dữ liệu huấn luyện không đủ lớn. Vì vậy, bigram tạo ra sự đánh đổi giữa khả năng biểu diễn ngữ cảnh tốt hơn và chi phí xử lý do số lượng đặc trưng tăng lên.

---

## 6. Inspect Model Weights

### Bảng Top Features và Trọng số tương ứng (Logistic Regression + TF-IDF)

| # | Top Positive Feature | Pos Weight | Top Negative Feature | Neg Weight |
| :-: | :--- | :---: | :--- | :---: |
| **0** | `excellent` | +7.7282 | `worst` | -8.4852 |
| **1** | `great` | +7.1857 | `bad` | -8.3688 |
| **2** | `perfect` | +5.8706 | `awful` | -8.3431 |
| **3** | `amazing` | +5.7590 | `waste` | -8.0053 |
| **4** | `wonderful` | +5.4254 | `boring` | -7.6966 |
| **5** | `brilliant` | +4.9527 | `terrible` | -7.2306 |
| **6** | `loved` | +4.7572 | `poor` | -6.6487 |
| **7** | `today` | +4.4583 | `the worst` | -6.3194 |
| **8** | `enjoyed` | +4.0046 | `nothing` | -5.3013 |
| **9** | `highly` | +3.9591 | `worse` | -5.1658 |
| **10** | `favorite` | +3.9568 | `horrible` | -5.0623 |
| **11** | `hilarious` | +3.8235 | `unfortunately` | -4.8907 |
| **12** | `fun` | +3.6408 | `annoying` | -4.8813 |
| **13** | `beautiful` | +3.5800 | `stupid` | -4.6929 |
| **14** | `well` | +3.5405 | `minutes` | -4.5494 |

---

### Câu hỏi: Những feature này có thực sự có ý nghĩa đối với task không?
> **Trả lời:**
> 
> Có, phần lớn các feature trong bảng có ý nghĩa đối với bài toán phân loại cảm xúc phim (sentiment analysis), vì chúng thể hiện những từ ngữ mang sắc thái tích cực hoặc tiêu cực rõ ràng. Với mô hình Logistic Regression, trọng số dương lớn cho thấy feature có xu hướng đẩy dự đoán về lớp Positive, trong khi trọng số âm lớn đẩy dự đoán về lớp Negative, giả sử mô hình mã hóa Positive là lớp đích có hệ số dương.
> 
> Cụ thể, các từ như `excellent`, `great`, `perfect`, `wonderful`, `amazing` có trọng số dương cao, phù hợp với những nhận xét khen ngợi phim. Ngược lại, `worst`, `bad`, `awful`, `waste`, `boring` có trọng số âm lớn, phù hợp với những nhận xét tiêu cực. Điều này cho thấy mô hình đã học được các tín hiệu từ vựng có khả năng phân biệt hai lớp. 
> 
> Tuy nhiên, không phải feature nào cũng có ý nghĩa rõ ràng khi đứng riêng lẻ. Chẳng hạn, `today` thường không biểu thị cảm xúc trực tiếp, còn `highly` và `well` phụ thuộc vào từ đi kèm; chúng có thể mang trọng số lớn do xuất hiện thường xuyên trong một số ngữ cảnh tích cực của tập huấn luyện. Tương tự, cụm `the worst` là một bigram có ý nghĩa tiêu cực rõ ràng hơn khi xét trong ngữ cảnh. Ngoài ra, trọng số lớn không đồng nghĩa với feature đó luôn quan trọng nhất trong mọi dự đoán, vì đóng góp thực tế còn phụ thuộc vào giá trị TF-IDF của feature trong từng văn bản. Vì vậy, bảng trọng số cho thấy mô hình đã học được nhiều đặc trưng hợp lý, nhưng cần kiểm tra thêm các ví dụ dự đoán cụ thể để đánh giá liệu mô hình có thực sự dựa vào tín hiệu cảm xúc có ý nghĩa hay đang khai thác những tương quan ngẫu nhiên trong dữ liệu.

---

## 7. Application

### Bảng tổng hợp so sánh dự đoán 3 mô hình trên tập Test nhỏ (`df_app`)

| # | Nội dung Review | Ground Truth | TF-IDF + LR | Word2Vec + LR | TF-IDF + SVM |
| :-: | :--- | :---: | :---: | :---: | :---: |
| **0** | The characters were dull and the ending was disappointing. | `negative` | **`positive`** *(sai)* | `negative` | `negative` |
| **1** | I loved the story and the brilliant acting. | `positive` | `positive` | `positive` | `positive` |
| **2** | The movie was boring and terribly disappointing. | `negative` | `negative` | `negative` | `negative` |
| **3** | The movie was absolutely amazing and captivating! | `positive` | `positive` | `positive` | `positive` |
| **4** | A terrible film with a weak and predictable plot. | `negative` | `negative` | `negative` | `negative` |
| **5** | An excellent film with beautiful cinematography. | `positive` | `positive` | `positive` | `positive` |
| **6** | This is one of the worst movies I have ever watched. | `negative` | `negative` | `negative` | `negative` |
| **7** | This is one of the best movies I have ever watched. | `positive` | `positive` | `positive` | `positive` |
| **8** | The characters were great and the ending was satisfying. | `positive` | `positive` | `positive` | `positive` |
| **9** | I hated the story and the acting was awful. | `negative` | `negative` | `negative` | `negative` |

> [!NOTE]
> * **Độ chính xác trên `df_app`**:
>   * `TF-IDF + Logistic Regression`: **90.0%** (9/10 câu đúng, đoán sai câu 0).
>   * `Avg Word2Vec + Logistic Regression`: **100.0%** (10/10 câu đúng).
>   * `TF-IDF + Linear SVM`: **100.0%** (10/10 câu đúng).
