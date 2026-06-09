CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
TOP_K = 5
EMBED_MODEL = "all-MiniLM-L6-v2"
CHROMA_COLLECTION = "uva_housing"
GENERATION_MODEL = "llama-3.3-70b-versatile"

# Keys are short labels stored as ChromaDB metadata.
# Values are the canonical source URLs shown to users as citations.
SOURCE_MAP = {
    "alderman_hall_official":  "https://housing.virginia.edu/alderman-hall",
    "alderman_suite_official": "https://housing.virginia.edu/alderman-suite",
    "brown_official":          "https://housing.virginia.edu/brown",
    "hereford_official":       "https://housing.virginia.edu/hereford",
    "irc_official":            "https://housing.virginia.edu/irc",
    "gooch_dillard_official":  "https://housing.virginia.edu/gooch-dillard",
    "mccormick_official":      "https://housing.virginia.edu/mccormick",
    "first_year_housing":      "https://housing.virginia.edu/first-year-housing",
    "reddit_dorms_ranked":     "https://www.reddit.com/r/UVA/comments/12y2smz/uva_dorms_ranked/",
    "college_confidential":    "https://talk.collegeconfidential.com/t/freshman-dorms/1805679/2",
    "roomsurf_ranking":        "https://www.roomsurf.com/dorms-ranked/virginia",
}

# Static UVA pages that can be scraped with requests + BeautifulSoup.
# JS-heavy sources (reddit, college_confidential, roomsurf) are loaded
# from .txt files in /documents instead.
SCRAPE_SOURCES = {
    "alderman_hall_official":  "https://housing.virginia.edu/alderman-hall",
    "alderman_suite_official": "https://housing.virginia.edu/alderman-suite",
    "brown_official":          "https://housing.virginia.edu/brown",
    "hereford_official":       "https://housing.virginia.edu/hereford",
    "irc_official":            "https://housing.virginia.edu/irc",
    "gooch_dillard_official":  "https://housing.virginia.edu/gooch-dillard",
    "mccormick_official":      "https://housing.virginia.edu/mccormick",
    "first_year_housing":      "https://housing.virginia.edu/first-year-housing",
}

SYSTEM_PROMPT = """You are a helpful guide for UVA first-year students choosing housing.
Answer ONLY from the provided context chunks. Each chunk is labeled with its source.
If the context does not contain enough information to answer, say so clearly — do not guess.
Keep answers concise and factual."""
