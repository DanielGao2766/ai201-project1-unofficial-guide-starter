# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

I chose to specalize in my university's on-campus first year housing options because opinions are varied and the official page lists all the options and amenities but nothing about the community experience surrounding each dorm. This combined with not knowing much about the University before attending leads to many not knowing which dormitory would be the best fit for them and what they should put in their rankings for preferred dorm options. 

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | New Hall Style Dorms | Official page | https://housing.virginia.edu/alderman-hall |
| 2 | New Suite Style Dorms | Official page | https://housing.virginia.edu/alderman-suite |
| 3 | Brown Residential College | Official page | https://housing.virginia.edu/brown |
| 4 | Hereford Residential College | Official page | https://housing.virginia.edu/hereford |
| 5 | International Residential College | Official page | https://housing.virginia.edu/irc |
| 6 | Gooch & Dillard Suite Dorm | Official page | https://housing.virginia.edu/gooch-dillard |
| 7 | Old Dorms (McCormick area) | Official page | https://housing.virginia.edu/mccormick |
| 8 | Reddit: UVA Dorms Ranked | Student forum discussion | https://www.reddit.com/r/UVA/comments/12y2smz/uva_dorms_ranked/ |
| 9 | College Confidential: Freshman Dorms | Student forum discussion | https://talk.collegeconfidential.com/t/freshman-dorms/1805679/2 |
| 11 | Roomsurf: UVA Dorms Ranked | Student ranking list | https://www.roomsurf.com/dorms-ranked/virginia |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 500 Characters

**Overlap:** 100 Characters

**Why these choices fit your documents:**

My sources are mostly short-from with forum comments being around 100 words and official page paragrahs being around 1-3 sentences meaning that a 500 character chunk size with a 100 chracter overlap aligns each chunk with at least one single coherent thought. 

**Final chunk count:** 150

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
all-MiniLM-L6-v2 via sentence-transformers

**Production tradeoff reflection:**

Given a no-cost constraint, I would choose a domain-specific, English-only embedding model with low context length and higher latency. A domain-specific model would better understand the university's location, surrounding areas, and housing nuances. A low context length would be sufficient since there are not a lot of specific ideas that need to be linked together, just raw fact-based information. Additionally, I would want high latency, because I care more about the quality of the information then the speed since any general LLM model (i.e. ChatGPT, Gemini) can give generic information about each dorm but not all the nuance. Finally, multilingual support is unnecessary given the relatively small international student population, allowing resources to be focused on improving performance in English.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

You are a helpful guide for UVA first-year students choosing housing.
Answer ONLY from the provided context chunks. Each chunk is labeled with its source.
If the context does not contain enough information to answer, say so clearly — do not guess.
Keep answers concise and factual.

**How source attribution is surfaced in the response:**

The model will cite the source based on the metadata within the chunk which contains the source. Additionally, all of the sources it pulls from will appear at the botttom for any user to do further investigation about the models answer. 

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What is the closest dorm to Newcomb Dining Hall? | Brown Residential College | According to [1] (brown_official), Brown Residential College is 1 minute from Central Grounds, and Newcomb Hall is implied to be on Central Grounds (as it has mail services and is mentioned alongside a distance to Central Grounds and bus routes). Therefore, Brown Residential College is near Newcomb Hall | Relevant | Accurate |
| 2 | What is the difference between Residential Colleges and other First-Year Dorm Options? | Residential Colleges have students from all years, while First-Year dorms have only First-Year students | The main difference is that students can apply for Residential Colleges, which gives them some say in their housing, whereas assignments in traditional buildings are random. Additionally, Residential Colleges may have a different room setup, with some having double rooms, and at least one (Brown) having a selective application process | Partially relevant | Partially accurate |
| 3 | Which dorms have personal bathrooms (i.e. non communal bathrooms)? | Any suite style dorm (Gooch Dillard, Alderman Road Suite Style Dorms) | Based on the provided context, it appears that there are no dorms with completely personal bathrooms (i.e., non-communal bathrooms) for first-year students. However, some dorms have suite-style arrangements where a private bathroom is shared among a few people (typically 3-4) | Relevant | Accurate |
| 4 | Which Dorm is closest to Runk Dining Hall? | Gooch-Dillard| The context does not contain enough information to answer which dorm is closest to Runk Dining Hall | Off-target | Inaccurate |
| 5 | Which Dorm has the most central location? | Brown Residential College |According to [1] (reddit_dorms_ranked), Brown has the best location of any dorm. | Relevant | Accurate | 

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
