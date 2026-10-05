# Experimental Results: Word Representations and Embeddings

---

## 1. Experiment 1 — Word-Context Representation (Co-occurrence Matrix)

### 1.1. Statistics Across Different Window Sizes

| Metric | Window Size = 1 | Window Size = 2 | Window Size = 5 |
| :--- | :---: | :---: | :---: |
| **Vocabulary Size** | 29,381 words | 29,381 words | 29,381 words |
| **Matrix Size** | 29,381 × 29,381 | 29,381 × 29,381 | 29,381 × 29,381 |
| **Non-zero Values (nnz)** | 2,099,883 | 4,078,885 | 8,885,616 |
| **Matrix Sparsity** | 99.7567% | 99.5275% | 98.9707% |
| **Cosine Similarity (`doctor` - `physician`)** | 0.8355 | 0.8487 | 0.8940 |

---

### 1.2. Top-5 Most Similar Words (Co-occurrence Model)

| Rank | `doctor` | `hospital` | `car` | `computer` | `food` |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **1** | child (0.9456) | house (0.9404) | while (0.9744) | business (0.9407) | music (0.9656) |
| **2** | vehicle (0.9248) | public (0.9403) | house (0.9720) | home (0.9370) | water (0.9654) |
| **3** | plan (0.9242) | community (0.9373) | company (0.9693) | budget (0.9349) | local (0.9634) |
| **4** | or (0.9220) | office (0.9360) | after (0.9671) | account (0.9333) | other (0.9630) |
| **5** | home (0.9209) | school (0.9347) | game (0.9667) | journey (0.9327) | performance (0.9629) |

---

## 2. Experiment 2 — Word2Vec (Dense Embeddings)

### Top-5 Most Similar Words (`model.wv.most_similar`)

| Target Word | Rank 1 | Rank 2 | Rank 3 | Rank 4 | Rank 5 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`doctor`** | physician (0.7949) | spouse (0.7228) | child (0.7066) | novak (0.6359) | husband (0.6327) |
| **`hospital`** | clinic (0.7094) | indiana (0.6886) | cincinnati (0.6782) | yale (0.6694) | alabama (0.6691) |
| **`patient`** | patients (0.6474) | treatment (0.6458) | medication (0.6290) | diagnosis (0.6044) | child (0.5931) |
| **`disease`** | diseases (0.8057) | diabetes (0.8054) | syndrome (0.8039) | chronic (0.8030) | infection (0.7974) |
| **`computer`** | desktop (0.7840) | browser (0.7522) | device (0.7431) | laptop (0.7316) | server (0.6991) |
| **`football`** | baseball (0.8323) | basketball (0.8104) | soccer (0.7679) | championship (0.7237) | club (0.7149) |
| **`banana`** | peppers (0.8969) | onions (0.8944) | cabbage (0.8928) | mushrooms (0.8926) | pudding (0.8900) |

---

## 3. Experiment 3 — Context Window

### Effect of Context Window Size on Word Similarities

| # | Word Pair | Window = 2 | Window = 5 | Window = 10 |
| :-: | :--- | :---: | :---: | :---: |
| 0 | `doctor` - `physician` | **0.7542** | 0.6950 | 0.7472 |
| 1 | `doctor` - `hospital` | 0.4390 | 0.4876 | **0.5377** |
| 2 | `cat` - `dog` | 0.5619 | **0.6868** | 0.6441 |

---

## 4. Experiment 4 — Embedding Dimension

### Performance & Trade-offs Across Vector Dimensions

| # | Dimension | Training Time (s) | Vector Matrix Size | Sim (`doctor` - `physician`) | Analogy (`king` - `man` + `woman`) |
| :-: | :---: | :---: | :---: | :---: | :---: |
| 0 | **50** | 136.70 s | 1,469,050 | 0.7983 | `queen` |
| 1 | **100** | 133.61 s | 2,938,100 | 0.7595 | `queen` |
| 2 | **300** | 196.40 s | 8,814,300 | 0.5575 | `queen` |

---

## 5. Application — Semantic Search

### Query 1: `medical treatment`

* **Rank 1 (Score: 0.6350)**
  > a phase ii pilot study to evaluate use of intravenous lidocaine for opioid refractory pain in cancer patients kerala india status of cancer pain relief and palliative care nurse moral distress and cancer pain management an ethnography of oncology nurses in india

* **Rank 2 (Score: 0.5933)**
  > not all ultrasound systems are equal created equal truffles vein specialists has philips affinity ultrasound systems the state of the art cutting edge ultrasound system along with award winning experienced vascular staff enables truffles vein specialists to provide the highest level of vein diagnosis and treatment combining the highest level of medical vascular imaging with a patient centered approach to vein treatment truffles has raised the bar when it comes to vein treatment

* **Rank 3 (Score: 0.5858)**
  > on january 28 2016 food and drug administration fda has approved merck and co manufactured zepatier a new oral treatment for adult patients with chronic hepatitis c hcv virus genotype 1 and 4 infections zepatier is a once a day fixed dose oral combination product containing elbasvir hcv ns5a inhibitor and grazoprevir hcv ns3 4a protease inhibitor and indicated for use with or without ribavirin not requiring use of interferon zepatier was granted breakthrough therapy designation for the treatment of chronic hcv genotype 1 infection in patients with end stage renal disease on hemodialysis and for the treatment of chronic hcv genotype 4 infection breakthrough therapy designation is a program designed to expedite the development and review of drugs that are intended to treat a serious condition and have preliminary clinical evidence to indicate that the drug may demonstrate substantial improvement over available therapy on a clinically significant endpoint the cost of the 12 week therapy is 54 000 which is approximately 40 50 lower than currently existing therapies empirx health has added zepatier to the formularies with prior authorization requirements

* **Rank 4 (Score: 0.5768)**
  > the indiana hospital heart institute has one of the largest most experienced cardiac surgery team in south india over the last 2 1 2 years more than 200 patients have had their heart surgery performed at indiana hospital heart institute for ranging from valve surgery repairs to cabg s complex aortic and arch surgeries the indiana hospital heart institute performs coronary artery bypass operations with a success rate of over 99 even complex operations re do surgeries and aortic and great vessel surgeries are routinely performed at indiana hospital heart institute with excellent results department of cardiothoracic and vascular surgeries offer beating heart surgeries valve replacement repair surgeries for adults and pediatric patients the department of cardiothoracic and vascular surgeries is a tertiary care centre with specialized divisions cardiothoracic and vascular surgery cardiac anesthesiology and intensive care preventive cardiology cardiac rehabilitation and perfusion technology thoracic surgeries lung and mediastinal surgery surgeries for peripheral vascular disease like aorto bifemoral bypass femoro femoral bypass femoro popliteal bypass surgeries and as combined procedure with bypass surgery is being performed with excellent results

* **Rank 5 (Score: 0.5767)**
  > caused by pituitary adenomas ischemic necrosis pituitary surgery radiation or injury symptoms hypothyroidism hypogonadism and infertility hypocortisolism decreased prolactin and decreased growth hormone may also exhibit loss of lateral fields of vision owing to compression of optic chiasm treatment hormone replacement surgical removal of adenoma caused by pituitary lactotroph adenoma symptoms amenorrhea in women or impotence in men infertility galactorrhea spontaneous flow of milk from breast may exhibit visual disturbances due to compression of optic chasm treatment bromocriptine to suppress prolactin secretion surgery or radiation to remove adenoma caused by pituitary somatotropic adenoma symptoms gigantism in children acromegaly in adults resulting in enlargement of hands and feet skull and mandible weight gain insulin resistance hypertension cardiomegaly and cardiac failure possible visual disturbances due to compression of optic chiasm treatment octreotide to decrease gh release surgical removal of adenoma a benign tumor that develops near the pituitary gland occurs most commonly in childhood symptoms increased pressure on the brain damage to the optic nerve leading to visual disturbances can also lead to excessive thirst excessive urination and stunted growth and diabetes insipidus treatment surgical removal of the adenoma causes include pulmonary disorders trauma haemorrhage stroke pharmacologic agents or pain also through tumors symptoms fatigue and confusion treatment fluid restriction medications to reduce adh and fluid retention deficiency of adh secretion symptoms excessive and prolonged thirst needing to urinate frequently passing large amounts of urine treatment synthetic vasopressin low sodium diet

---

### Query 2: `delicious food recipe`

* **Rank 1 (Score: 0.7173)**
  > located on malop street geelong serving delicious fresh food coffee the restaurant printer is offline

* **Rank 2 (Score: 0.6955)**
  > gem home made meal simple fast lesson chinese dishes first dish chinese wedding toronto video photo services how to cook customize your mama shrimp thai tum yum instant noodles

* **Rank 3 (Score: 0.6858)**
  > spicy kung pao noodles with shrimp is inspired by the famous szechuan kung pao chicken the spicy savory sweet and tangy sauce is one of the elements that makes this dish addicting making stir fried noodles with this sauce is no exception

* **Rank 4 (Score: 0.6833)**
  > please note all our house specials contain coconut tandoori chicken marinated in pakistani spices fried in butter and served in curry sliced lamb in a special minced lamb sauce with sultanas indian style meatballs in a superbly spiced tomato and onion bhuna sauce cooked with mint fresh herbs and selected spices with a sweet and tangy taste prepared with potato and egg medium taste topped with korma sauce medium chicken tikka tossed over iron skillet with exotic herbs and spices crushed garlic and ginger root covered in a sauce of tomatoes spring onions and capsicums chicken or lamb in a delicious preparation of yoghurt cream coconut mushrooms and spices very mild but rich creamy texture choice of chicken lamb or prawn cooked in a mild sauce with apricot slices topped with honey marinated pieces of chicken lamb king prawn and sheek kebab skewered and barbecued with onions and tomatoes medium very tasty dish chicken or lamb cooked with garlic and coriander with a cheese topping medium chicken or lamb cooked with eggs and spices chicken or lamb cooked with green chillies garlic onion tomato capsicum and lemon slightly hot dish tender chicken or lamb cooked with minced meat and egg in a thick spicy sauce fairly hot freshly chopped chicken stir fried with chillies and tomatoes hot dish extremely hot but flavoursome a tasty alternative for those who live phall dishes

* **Rank 5 (Score: 0.6798)**
  > fresh ginger root is dried then ground and used in desserts and savory dishes ginger ground is readily available in standard supermarkets it is an acceptable but not always desirable substitution for fresh ginger roast chicken pradesh from northern india is a flavorful indian recipe for roasted chicken the chicken is basted with a marinade of yogurt spices cream and butter then finished with sliced roasted onions these pretty little bars are made with sweet pastry crust flavored with ginger the filling uses fresh lime juice and lemon extract

---

### Query 3: `implement linear regression`

* **Rank 1 (Score: 0.7070)**
  > with a combination of analytical techniques we can determine or confirm the solid state molecular structure for a chemical entity these techniques include mass spectrometry nmr spectroscopy infrared spectroscopy elemental analysis and single crystal x ray diffraction we combine these techniques to address complex structural problems mass spectrometry ms is the preferred technique to determine molecular weight and fragmentation data to support structure elucidation the use of lc ms enables the collection of structural data for many components in a complex mixture we can use mass spectrometry to further characterize impurities observed using the lc procedure the lc ms data can be collected using different ionization techniques depending upon the nature of the sample we can perform lc ms lc ms ms and lc ms ms ms analyses using a linear ion trap instrument the mass spectrometry data can be used for both quantitative and qualitative purposes we use high resolution 1d and 2d nmr spectroscopy to determine the atomic connectivity and structural conformation of molecules in solution both 1h and 13c nmr spectroscopy provide detailed information about molecules various 2d proton nmr correlation experiments such as cosy tocsy and noesy enable the determination of the relative locations of protons or the conformation of a molecule in solution we also can conduct additional 2d proton carbon nmr correlation experiments such as hmqc hsqc and hmbc to connect the carbon backbone of complex molecules these nmr techniques are used to determine the assignments of all resonances for a molecule and knowledge of the relative position of each nucleus permits the determination of the molecular conformation in solution we can perform variable temperature multinuclear and gradient selected nmr analyses quantitative and qualitative data can be obtained using nmr spectroscopy we use an in house rigaku supernova diffractometer equipped with a copper anode microfocus sealed x ray tube and a dectris pilatus3 r 200k hybrid pixel array detector the calculated powder x ray pattern is generated from the determined crystal structure as a reference x ray powder diffraction xrpd pattern for that particular form this pattern can also be compared to the as received powder material xrpd to assess the purity of the bulk material and confirm its form

* **Rank 2 (Score: 0.6934)**
  > grok is an ai operations aiops platform that proactively resolves it incidents using machine intelligence and automation it senses behaviors that lead to downtime using anomaly detection then triggers actions based on those insights its features include customizable dashboards script based automation and intranet embeddable dashboards

* **Rank 3 (Score: 0.6907)**
  > the electroforce systems group םכ ta corporation provides materials testing and durability simulation instruments to research institutions universities medical device companies and engineering organizations worldwide electroforce test instruments are superior test systems for mechanical fatigue and dynamic characterization by incorporating proprietary of motor technologies and wintest controls electroforce instruments provide exceptional fidelity precision and versatility for a variety of test applications the electroforce linear motor utilizes a simple and durable moving magnet design that provides excellent dynamic performance and years of reliable operation for researchers and test engineers as a result electroforce test instruments have set a new standard for performance simplicity and elegance in a single test system for more on the electroforce system advantage please contact us at tetra sense electroforce stent graft test sgt instruments have set the standard of performance for the fatigue testing of a variety of stents and endovascular grafts ten year fda in vitro tests take only weeks with electroforce instruments due to their reliable accelerated dynamic performance specific sgt instrument designs are available for coronary and neural stents abdominal stents aaa bifurcations and thoracic stents for multi mode peripheral and coronary stent fatigue testing electroforce multiaxial test instruments provide realistic motion simulation to effectively reproduce in vivo conditions for multiple stents the instruments are capable of testing an accelerated 10 year simulated life performing fatigue to fracture studies or evaluating worst case conditions for a stent design ef9210 drug eluting stent test instrument this system provides a new standard of performance resulting in expedited time to market and improved testing accuracy through a combination of new and existing proprietary technologies the 9210 instrument allows a user to test twelve specimens simultaneously provides increased distention uniformity along the stent profile and combines high frequency performance with the necessary precision for particle capture electroforce multi specimen fatigue testing systems can be used for high cycle fatigue life characterization of coronary and vascular device structures and evaluation of device materials for s n curve development the test systems provide displacement controlled loading for small soft structures and devices such as stents stent segments vena cava filters septal closure structures and annuloplasty devices by incorporating proprietary electroforce motor technologies and wintest controls electroforce instruments provide exceptional fidelity precision and versatility for a variety of test applications the electroforce linear motor utilizes a simple and durable moving magnet design that provides excellent dynamic performance and years of reliable operation for researchers and test engineers wintest controls provide data acquisition waveform generation and instrument control in one comprehensive package as a result electroforce test instruments have set a new standard for performance simplicity and elegance in a single test system exploring the viscoelastic properties of materials and components a ta electroforce test instrument is an attractive platform for advanced viscoelastic property measurements of elastomers plastics films biomaterials gels and foods as well as many additional materials control for electroforce instruments is provided by the wintest digital control system this pc based system features an intuitive interface and powerful test generation and data acquisition capabilities the software s flexible design enables electroforce instruments to perform a wide range of tests such as tension compression bending and shear under a wide variety of load strain frequency and temperature conditions wintest dynamic mechanical analysis dma software along with environmental chambers and our new dma tensile grips tests can be used to determine material properties such as tan delta complex storage and loss moduli or to determine component properties such as dynamic stiffness phase storage or loss stiffness and dampening wintest dma software allows the user to define a series of test conditions that are automatically reproduced on the test system the user can also step through a series of conditions to explore changes in material or component properties with respect to a controlled parameter ta electroforce dma data analysis software also makes it easy to look at the requested and actual test conditions and the original channel data fft analysis is used to convert this data to viscoelastic properties and components and the user can plot the data in a wide variety of ways or if preferred export the data to a text file for analysis in other third party tools the ta electroforce series iii test instruments feature up to 7 5kn maximum force with the versatility of static and up to 300 hz frequency response the table top or floor configuration is adaptable to a variety of biomedical research and engineered materials test applications including torsion testing creep under dynamic loading and special environments hot cold chambers the adhesion analyser lumifrac is the new benchmark for determining adhesive and tensile strengths winner of the berlin brandenburg 2012 innovation award watch video here the lumifrac employs centrifugal forces to stress multiple samples at once it provides adhesive and tensile strength as an absolute physical quantity in n mm² the analyzer accomplishes this by directly applying an incrementally increasing radial centrifugal force to the specimen being tested it determines with high resolution the rpm at the moment of fracturing all data is transmitted to the well known and popular operating software sepview which automatically calculates and displays the critical force strength of failure in real time furthermore with the unique feature of being able to probe thermal conductivity as a function of sample depth structural probe module the tps 2500 s can e g be used to determine whether a sample is homogeneous or not in addition to these applications the tps 2500 s can also be employed for dedicated specific heat capacity testing of large compared to conventional methods e g dsc solid samples such as complex composites

* **Rank 4 (Score: 0.6864)**
  > this paper presents a novel approach to capture light field in camera arrays based on the tensor recovery framework light fields are acquired by a linear array of cameras with overlapping field of view we represent the light fields in shape of a tensor to exploit both local and non local correlated structures of cameras image the methodology is inspired by the recent research on matrix completion we extend the affine matrix rank minimization to low rank tensor recovery for light field acquisition using a convex relaxation technique of the matrix rank finally we develop a quantitative evaluation on a synthetic scene to assess our method with low n rank tensor recovery algorithm to assure the accuracy of our scheme with far less computational cost

* **Rank 5 (Score: 0.6823)**
  > the next frontier in cell biology is to implement multidisciplinary approaches to question various aspects of life in a dynamic and quantitative manner from synthetic biology to multi cellular development this meeting will bring together the best experts in these multi disciplinary approaches to share their latest data and models time will be devoted for debate to generate new ideas and new concepts innopsys presents its full automated cell array platform with innostamp 40 a microcontact printing instrument and innoscan 1100 al a digital imager
