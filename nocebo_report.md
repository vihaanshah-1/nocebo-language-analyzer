# Nocebo/Placebo Language Analyzer Project

## Introduction

Communication around medical procedures can influence how patients perceive and
experience treatment.  The **nocebo effect** is a psychobiological phenomenon
whereby adverse symptoms occur **independently of any active treatment
mechanism** and are driven by **patient expectations**【754516959382684†L175-L183】.
Negative wording and detailed lists of potential adverse events in consent
forms or patient leaflets can heighten anxiety and amplify adverse
responses【754516959382684†L231-L236】.  Conversely, reframing messages into
neutral, patient‑friendly language can minimise anxiety and uphold the
principles of beneficence and non‑maleficence【754516959382684†L239-L246】.  This
project applies natural language processing (NLP) to analyse medical
information leaflets, detect language that may provoke nocebo responses and
suggest neutral alternatives.


## Methods

### Data collection

Publicly available patient information documents were used as data sources.
Examples included:

- **Colonoscopy preparation leaflet** – emphasises bowel preparation and warns
  of frequent bowel movements and diarrhoea【58847115735023†L104-L107】.  It
  instructs patients not to eat or drink for a period before the procedure
  【58847115735023†L116-L119】 and provides detailed sedation instructions,
  including restrictions on driving, using machinery or making legal
  decisions for 24 hours after sedation【58847115735023†L223-L246】.
- **Sedation information sheet** – explains that moderate sedation reduces
  anxiety and pain, describes how medications are administered and lists
  potential side‑effects.  It warns of risks such as allergic reaction,
  aspiration, respiratory depression, heart attack, stroke, brain death or
  **death**, and notes that serious complications may require life‑support
  interventions【326708100393747†L49-L63】.
- **Contrast injection leaflet** – describes the use of contrast dye during
  CT scans, notes that mild allergic reactions (itching, wheezing or
  nausea) are rare and pass quickly, and lists rare delayed reactions such
  as nausea, vomiting, diarrhoea, abdominal pain and rash【644566700061463†L23-L49】.
- **Sedation explained brochure** – discusses oral and intravenous sedation,
  stresses the importance of clear thinking when signing consent forms and
  highlights practical preparations (bringing a responsible adult, fasting
  instructions and post‑procedure care).  It emphasises that sedation can
  replace general anaesthesia for certain procedures and usually has fewer
  side‑effects【629796228716192†L155-L172】.

These documents were manually extracted and split into sentences.  During this
iteration the dataset was **expanded substantially**.  In addition to the
colonoscopy, sedation information and contrast‑injection leaflets,
several **sedation‑specific patient leaflets and instruction sheets** were
mined.  New sources included:

- **Sedation explained** (Royal College of Anaesthetists) – emphasises
  planning for someone else to care for dependants and organising a capable
  adult to take the patient home by car and stay overnight【661294831003018†L197-L206】.
  It gives fasting instructions for moderate and deep sedation【661294831003018†L227-L236】,
  warns that sedation may impair decision‑making and coordination for up to
  24 hours【661294831003018†L303-L317】 and lists risks such as slowed
  breathing, low blood pressure and rare aspiration or allergic reactions【661294831003018†L371-L400】.
- **Intravenous sedation and local anaesthetic** (Queen Victoria Hospital
  NHS Trust) – states that a responsible adult must accompany the patient
  and stay with them for 24 hours【723963231179103†L32-L37】, forbids travel
  by public transport or driving oneself【723963231179103†L59-L60】,
  provides fasting guidelines and advises avoiding fizzy or milky drinks【723963231179103†L61-L66】,
  discourages smoking【723963231179103†L70-L74】 and instructs patients to
  avoid driving, operating machinery, drinking alcohol or making vital
  decisions for at least 24 hours【723963231179103†L78-L94】.
- **Caring for someone recovering from a general anaesthetic or sedation** –
  notes that sedation can make patients confused and unsteady, with
  impaired judgement for up to 24 hours【42350103563387†L9-L16】.  It advises
  carers to take patients home by car or taxi (public transport is discouraged)【42350103563387†L23-L31】
  and lists activities to avoid, such as looking after dependants, cooking,
  drinking alcohol, making important decisions or signing legal documents【42350103563387†L84-L102】.
- **Conscious sedation information** (British Association of Oral Surgeons)
  – highlights that sedation can remain in the body for up to 24 hours and
  requires adherence to specific instructions【464097700660924†L78-L86】.  It mandates
  having a responsible adult escort who stays during the procedure and drives
  the patient home【464097700660924†L88-L92】, allows light meals and fluids
  before oral/IV sedation but prohibits alcohol the day before or day of
  treatment【464097700660924†L101-L113】 and advises resting at home for 24 hours
  after the procedure and not travelling by public transport, driving or
  making important decisions while the sedative effects wear off【464097700660924†L139-L154】.
- **Intravenous sedation pre/post‑operative instructions** (Hannigan Dental
  Care) – requires patients to bring an escort over 18 who stays during the
  appointment and takes them home by car or taxi; the escort must not be
  responsible for children or dependants【279827083262922†L27-L43】.  It
  advises wearing loose clothing and flat shoes, abstaining from alcohol or
  recreational drugs for 24 hours before the appointment【279827083262922†L51-L69】,
  recommends a light meal two hours before if fasting is not required【279827083262922†L72-L78】,
  and notes that dehydration can complicate cannula placement【279827083262922†L82-L85】.  Post‑operative
  instructions include going straight home and resting, not returning to work,
  not driving or operating machinery, not caring for dependants, abstaining
  from alcohol or sleeping tablets and avoiding important decisions for
  24 hours【279827083262922†L148-L176】.  Patients are reminded to contact the
  surgery or NHS 24 if they have any concerns【279827083262922†L177-L183】.

Sentences from these new sources were manually extracted and labelled.  The
expanded dataset now contains **285 sentences**; roughly one‑third are
moderate or high‑anxiety statements (e.g., instructions not to drive or
warnings about rare complications).

### Labelling rubric

To assess anxiety‑inducing language, sentences were annotated using a
four‑category rubric:

| Category             | Example triggers                                             |
|---------------------|--------------------------------------------------------------|
| **Threat intensity**| words suggesting severe harm or fatality (e.g. “death”,
"stroke", “heart attack”, “paralysis”)【326708100393747†L49-L63】 |
| **Uncertainty**     | expressions of unpredictability (“possible”, “may”,
“rarely”, “if it does happen”) |
| **Vivid side‑effects** | vivid descriptions of unpleasant symptoms (nausea,
vomiting, diarrhoea, pain, rash, dizziness)【644566700061463†L23-L49】 |
| **Directive harshness** | imperative language (“must not”, “do not”, “stop
 taking”)【58847115735023†L116-L119】 |

Each sentence was labelled with a **severity score** (0 = neutral, 1 = mild,
2 = moderate, 3 = high) based on the number of categories triggered.
Labels were assigned heuristically using keyword lists (see rubric file).

### Plain‑language guidelines

The project drew on plain‑language guidance to inform rewriting.  The US
Institutional Review Board style guide recommends using **simple, common
words** and avoiding medical jargon, long multi‑syllable words, unnecessary
adjectives and legal terms【111783343424908†L23-L60】.  Sentences should be
short (8–10 words), conversational and in active voice【111783343424908†L65-L95】.
These principles informed the replacement dictionary used to generate
neutral phrasing.

### Model training

A baseline classifier was built to recognise anxiety‑provoking sentences.  The
approach used:

- **Vectorisation** – Sentences were converted to TF‑IDF features (unigrams
  and bigrams).
- **Classifier** – A multiclass **logistic regression** with balanced class
weights was trained.  The expanded dataset of 285 sentences was split into
80 % training and 20 % test sets.  Because the class distribution remained
imbalanced (few sentences were labelled as high anxiety), the logistic
regression used **balanced class weights** to mitigate bias toward the
majority classes.

A pickled model and vectoriser were saved for reuse and are loaded by the
Python module `nocebo_analyzer.py`.


## Results

### Dataset overview

The final dataset now contains **285 sentences**.  Roughly one‑third were
labelled as containing mild or moderate anxiety triggers; neutral sentences
included factual descriptions of preparation or administrative instructions
(e.g., “Arrange to have an adult drive you to your test”).  The newly
added sedation leaflets and escort information contributed many moderate‑risk
sentences because they instruct patients not to drive, not to care for
dependants or avoid certain activities for up to 24 hours.

### Model performance

With the larger dataset and balanced class weights, the logistic regression
achieved an overall **accuracy of 61 %** on the held‑out test set (weighted
F1 ≈ 0.61).  Performance improved compared with the earlier iteration but
remained modest because of the small sample and diverse phrasing of patient
leaflets.  The classifier performed reasonably well on neutral and moderate
sentences but still struggled with the very few high‑severity examples.  The
classification report is summarised below, showing precision (P), recall (R)
and F1 score for each label:

| Label | Meaning           | Support |    P |    R |   F1 |
|-----:|------------------|--------:|----:|----:|----:|
|   0  | Neutral          |      22 | 0.68| 0.68| 0.68|
|   1  | Mild anxiety     |      16 | 0.47| 0.44| 0.45|
|   2  | Moderate anxiety |      18 | 0.65| 0.72| 0.68|
|   3  | High anxiety     |       1 | 0.00| 0.00| 0.00|

The following confusion matrix (rows = true labels, columns = predicted labels)
shows that neutral and mild sentences were sometimes confused and the
single high‑severity sentence was misclassified:

```
[[15  5  2  0]
 [ 5  7  4  0]
 [ 2  3 13  0]
 [ 0  0  1  0]]
```

Despite its limitations, the model captured patterns such as imperative
phrases (“must not”, “do not drink alcohol”) and explicit warnings about
rare risks, which tended to increase the predicted anxiety level.
“reaction” and “extravasation” were indicative of higher risk sentences.

### Trigger detection and rewrite suggestions

To provide actionable feedback, the `nocebo_analyzer` module highlights
trigger categories and offers neutral rephrasing.  For example:

- **Original:** “You should expect frequent bowel movements and diarrhoea.”  
  **Rewrite:** “You should expect frequent bowel movements and loose stools.”  
  *Explanation:* Replaces the vivid term “diarrhoea” with the less visceral
  “loose stools” and maintains factual content.

- **Original:** “Then, you must not eat or drink anything until after your test”【58847115735023†L116-L119】.  
  **Rewrite:** “Then, you should not eat or drink anything until after your
  test.”  
  *Explanation:* Softens the imperative “must not” into “should not”, which
  conveys importance without reprimanding the patient.

- **Original:** “The risks associated with sedation include … respiratory
  depression, cardiac arrest, heart attack, stroke, brain death, paralysis,
  or death”【326708100393747†L49-L63】.  
  **Rewrite:** “Potential issues associated with sedation include respiratory
  depression, serious cardiac conditions, serious medical conditions,
  loss of brain function, loss of movement or very serious complications.”  
  *Explanation:* Consolidates rare catastrophic outcomes into neutral phrases
  while still informing the reader.

These rewrites are generated by a simple dictionary and serve as examples.
They do not replace clinical judgement and should be reviewed by health
professionals.


## Discussion

### Implications for practice

The study confirms that many patient information documents contain language
likely to amplify anxiety—particularly long lists of severe side‑effects and
imperative instructions.  Psychology research shows that warning patients
about a “painful injection” can itself increase pain and distress【754516959382684†L254-L259】.
Alternatives such as describing the goal of the procedure (e.g., “I am about
to inject local anaesthetic that numbs the skin”) can maintain transparency
while minimising nocebo effects【754516959382684†L265-L271】.

Plain‑language best practices—such as using common words, short sentences
and active voice—help make consent forms more understandable【111783343424908†L23-L60】.  Adopting these
principles aligns with the “layered consent” approach, where patients are
allowed to choose how much detail they want【754516959382684†L239-L247】.

### Limitations

  - **Dataset size.**  The dataset now contains 285 sentences, which is still
    modest for training an NLP model.  A much larger and more diverse
    corpus—ideally annotated by clinicians—would improve the classifier’s
    ability to discriminate between mild, moderate and high‑risk sentences.
- **Heuristic labelling.**  Labels were assigned using keyword lists rather
  than expert annotations, which may misrepresent nuance or context.
- **Simple model.**  Logistic regression with TF‑IDF features is a baseline;
  transformer‑based models (e.g., BERT) could capture semantic context
  better and deliver higher accuracy.
- **Rewrite quality.**  The replacement dictionary is simplistic; some
  rewrites may sound awkward or fail to preserve meaning (e.g., “please
  avoid please stop taking”).  Human review is essential.

### Ethical considerations

The analyzer is intended as an educational aid.  It should **not** be used
on clinical documents without oversight.  Informed consent requires
disclosing material risks, and any reduction of risk wording must not
compromise patient autonomy.  The goal is to *reframe* information rather
than hide it.


## Conclusion and next steps

This project demonstrates that even a small, student‑led effort can apply
NLP techniques to identify anxiety‑inducing language in medical documents.
It produced a labelled dataset, a baseline classifier and a prototype tool
capable of highlighting triggers and suggesting neutral alternatives.  The
work underscores the importance of compassionate communication and plain
language in healthcare.  Future improvements should focus on expanding the
dataset, incorporating expert annotations, and testing modern language
models for improved performance.  Collaborating with clinicians to refine
rewrite suggestions and piloting the tool with real users (e.g., as part
of a “layered consent” process) would strengthen its impact.
