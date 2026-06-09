import os
from groq import Groq
from dotenv import load_dotenv
from config import GENERATION_MODEL, SYSTEM_PROMPT

load_dotenv()

_client = None


def _get_client() -> Groq:
    global _client
    if _client is None:
        _client = Groq(api_key=os.environ["GROQ_API_KEY"])
    return _client


def _build_context(chunks: list[dict]) -> str:
    lines = []
    for i, chunk in enumerate(chunks, 1):
        lines.append(f"[{i}] ({chunk['source_label']})\n{chunk['text']}")
    return "\n\n".join(lines)


def generate_answer(query: str, chunks: list[dict]) -> str:
    context = _build_context(chunks)
    user_message = f"Context:\n{context}\n\nQuestion: {query}"

    response = _get_client().chat.completions.create(
        model=GENERATION_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,
        max_tokens=512,
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    from embed import retrieve

    query = "Which dorms have suite-style bathrooms?"
    chunks = retrieve(query)
    answer = generate_answer(query, chunks)
    print(f"Q: {query}\n\nA: {answer}\n")
    print("Sources:")
    seen = set()
    for c in chunks:
        if c["source_url"] not in seen:
            print(f"  - {c['source_label']}: {c['source_url']}")
            seen.add(c["source_url"])
