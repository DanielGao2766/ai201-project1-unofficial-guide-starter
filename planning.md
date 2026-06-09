# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

I chose to specalize in my university's on-campus first year housing options because opinions are varied and the official page lists all the options and amenities but nothing about the community experience surrounding each dorm. This combined with not knowing much about the University before attending leads to many not knowing which dormitory would be the best fit for them and what they should put in their rankings for preferred dorm options. 

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
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
| 12 | UVA First-Year Housing Overview | Official overview with locations/neighborhoods | https://housing.virginia.edu/first-year-housing |


---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**
500 Characters
**Overlap:**
100 Characters
**Reasoning:**
I mostly have structured pages or forum discussions with structured text that are a max of around 200 words (~ 1000 characters), therefore a fixed size chunking would be better than recursive or semantic chunking because I don't have long text and I also don't have high level seperators in my sources.
---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
all-MiniLM-L6-v2 via sentence-transformers
**Top-k:**
5 Chunks since I need to pull the information about the dorm and the opnions on all the ranking lists. 
**Production tradeoff reflection:**

Given a no cost constraint, I would choose a more domain specific, low context length, high latency, English only embedding model.
I would want a more domain specific model regarding the location and knowing the area better to explain the services and distances to differnt areas. 
I would want a low context length since there are not a lot of specific ideas that need to be linked together, just raw information that must be embedded
I would want high latency, because I care more about the quality of the information then the speed since any general LLM model (i.e. ChatGPT, Gemini) can give generic information about each dorm but not all the nuance. 
Finally, I would choose to have no Multilingual Support because there is only a small population of International Students at my University which would make choosing reducing the efficiency for multiple languages not worth the trade off. 

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What is the closest dorm to Newcomb Dining Hall? | Brown Residential College
| 2 | What is the difference between Residential Colleges and other First-Year Dorm Options? | Res Colleges have students from all years, while First-Year dorms have only First-Year students
| 3 | Which dorms have personal bathrooms (i.e. non communal bathrooms)? | Any suite style dorm (Gooch Dillard, Alderman Road Suite Style Dorms) |
| 4 | Which Dorm is closest to Runk Dining Hall? | Gooch Dillard
| 5 | Which Dorm is closest to Rice Hall? | Page Dorm

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. All of my sources didn't come with the same format, meaning that although all of my sources have similar formats, there might be some issues with my fixed size chunking strategy regarding information being split amongst two different chunks. 
2. There might be a lack of information regarding different areas across campus outside of the dorms, meaning you would need to have background information about different buildings in order for the distances to matter (i.e. What does Shannon Library provide?)

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->


<!-- Need to use the command Ctrl + Z to make the diagram appear -->
<!-- Tutorial: https://jimmywongiot.com/2025/08/28/how-to-use-mermaid-in-visual-studio-code-a-step-by-step-guide-for-developers/ -->
<!-- Mermaid Editor: https://mermaid.ai/live/edit#pako:eNpVjk9PwzAMxb-K5ROIFbXr2q1FILENENK4AOLAukNo3DYiTaYshf3pvjvppiHIIbL9_HvPO8w1J0yxkPo7r5ixMHvOFLh3O39UJa2s0GoBnncD7b1YE_dexJZgUjXqU6gS2vHZqT4_cuPjMpPSexJKzJ68Wex99eGu_iDOO-bC4UbXbDqGN8qtNvDiPlZSO5n_3fovLo72k86-fdVL7xOuIbqCR1VoU7PuTuDCOEZuYNlISRwKFwO5VpaUhW9hK1jpxuS0amE6fyZrBH0x6aIeSJE5eLiYLgh7WBrBMbWmoR7W5CK6FnedmqGtqKYMU1dyKlgjbYaZ2jtsydS71vWJNLopK0wLJleua5acWZoKVhpW_04NKU5mohtlMQ36cXJwwXSHa0zD6NIPBtGwH0dJHIWduMG078aD2I8HcTgK_WEUhPsebg-5_mUS-2HiB9HIDwNXDPc_7rabuA -->


```mermaid
flowchart TD
    A["Document Ingestion\n(requests + BeautifulSoup for UVA pages;\nmanual .txt files for Reddit / CC / roomsurf)"]
    A --> |"Fixed-size chunking\n1000 chars / 200 overlap\nsource_label + source_url attached to each chunk"| B

    B["Chunking\n(ingest.py → chunk_text())"]
    B --> |"Encode with all-MiniLM-L6-v2\nStore vectors + metadata in ChromaDB"| C

    C["Embedding + Vector Store\n(embed.py → build_vector_store())"]
    C --> |"Query vector, top-k = 5\nReturn chunks with text + source metadata"| D

    D["Retrieval\n(embed.py → retrieve())"]
    D --> |"Numbered chunks injected into prompt\nclaude-sonnet-4-6 via Anthropic SDK"| E

    E["Generation\n(generate.py → generate_answer())"]
    E --> |"Answer + clickable source URLs\nStreamlit single-page UI"| F

    F["Interface\n(app.py — Streamlit)"]
```



  

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->
     

**Milestone 3 — Ingestion and chunking:**

- **Tool:** Claude Code (claude-sonnet-4-6)
- **Input:** The Documents table and Chunking Strategy section of this file, plus the `config.py` SOURCE_MAP
- **Prompt:** "Using the Documents table and Chunking Strategy section in my planning.md, implement two functions in `ingest.py`: (1) `load_documents() -> list[dict]` that scrapes each official UVA housing URL in SOURCE_MAP using requests + BeautifulSoup and loads manual `.txt` files from the `/documents` folder, returning `[{'text': str, 'source_label': str, 'source_url': str}]`; (2) `chunk_text(doc: dict, chunk_size=1000, overlap=200) -> list[dict]` that splits doc text into fixed-size character chunks with overlap, preserving source_label and source_url in each chunk dict."
- **Expected output:** Working `ingest.py` with both functions; running `python ingest.py` prints the first 3 chunks from each source showing text + source_label
- **Verification:** Manually confirm source_label is present on every chunk and that no chunk is empty or contains only nav/footer boilerplate

**Milestone 4 — Embedding and retrieval:**

- **Tool:** Claude Code (claude-sonnet-4-6)
- **Input:** The Retrieval Approach section of this file + the chunk dict structure `{'text', 'source_label', 'source_url'}` from Milestone 3
- **Prompt:** "Using the Retrieval Approach section of my planning.md, implement two functions in `embed.py`: (1) `build_vector_store(chunks: list[dict])` that encodes chunk texts with `sentence-transformers/all-MiniLM-L6-v2` and stores vectors plus metadata (`source_label`, `source_url`) in a ChromaDB PersistentClient collection named 'uva_housing'; (2) `retrieve(query: str, k: int = 5) -> list[dict]` that embeds the query and returns the top-k chunks as `[{'text', 'source_label', 'source_url'}]`."
- **Expected output:** Working `embed.py`; running it builds the ChromaDB collection on disk
- **Verification:** Call `retrieve("which dorm has suite-style bathrooms")` and confirm top results contain Gooch-Dillard and Alderman Suite chunks with source_label present

**Milestone 5 — Generation and interface:**

- **Tool:** Claude Code (claude-sonnet-4-6)
- **Input:** The system prompt design below + the `retrieve()` output format from Milestone 4
- **Prompt:** "Implement `generate_answer(query: str, chunks: list[dict]) -> str` in `generate.py` using the Groq Python SDK. System prompt: 'You are a helpful guide for UVA first-year students choosing housing. Answer ONLY from the provided context chunks. Each chunk is labeled with its source. If the context does not contain enough information to answer, say so clearly — do not guess.' Inject chunks into the user message as numbered blocks: `[1] (source_label)\n{text}\n\n[2] ...` followed by the question. Use model `llama-3.3-70b-versatile`. Then implement `app.py` as a Streamlit single-page app: text input → spinner → `st.markdown(answer)` → deduplicated clickable source URLs listed below the answer."
- **Expected output:** Working `generate.py` and `app.py`; `streamlit run app.py` opens the UI
- **Verification:** Run all 5 evaluation questions end-to-end; confirm answers are accurate, citations appear as clickable links, and asking "What does a meal plan cost?" returns a refusal rather than a hallucinated number
