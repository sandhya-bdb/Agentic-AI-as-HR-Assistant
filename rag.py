"""
rag.py — HR Policy RAG module using Docling's native API.

Flow:
  1. DocumentConverter  → parse the PDF
  2. ResultPostprocessor → fix heading hierarchy
  3. HierarchicalChunker → chunk with full H1 > H2 > H3 headings
  4. SentenceTransformer  → embed chunks
  5. retrieve()           → cosine-similarity search at query time
"""

import sys
import numpy as np
from docling.document_converter import DocumentConverter
from docling_core.transforms.chunker import HierarchicalChunker
from hierarchical.postprocessor import ResultPostprocessor
from sentence_transformers import SentenceTransformer

# ── Config ──────────────────────────────────────────────────────────────────
HR_POLICY_SOURCE = (
    "https://raw.githubusercontent.com/tnahddisttud/sample-doc"
    "/refs/heads/main/AtliqAI_HR_Policies.pdf"
)
EMBED_MODEL = "all-MiniLM-L6-v2"


# ── Load & chunk (runs once at import / server startup) ───────────────────
def _build_knowledge_base(source: str) -> list[dict]:
    """Parse PDF with Docling and return list of structured chunks."""
    print(f"[RAG] Loading document: {source}", file=sys.stderr)
    converter = DocumentConverter()
    result = converter.convert(source)
    ResultPostprocessor(result).process()   # fixes heading hierarchy
    doc = result.document

    chunker = HierarchicalChunker()
    doc_chunks = list(chunker.chunk(doc))
    print(f"[RAG] Total chunks: {len(doc_chunks)}", file=sys.stderr)

    chunks = []
    for c in doc_chunks:
        headings   = c.meta.headings or []
        content    = c.text.strip()
        if not content:
            continue
        breadcrumb = " > ".join(headings)
        chunk_text = f"{breadcrumb}\n\n{content}" if breadcrumb else content
        chunks.append({
            "headings":   headings,       # e.g. ['HR Policies', 'Leave', 'Casual Leave']
            "content":    content,        # raw paragraph text
            "chunk_text": chunk_text,     # breadcrumb + content (what gets embedded)
        })
    return chunks


print("[RAG] Initialising knowledge base …", file=sys.stderr)
_embedder   = SentenceTransformer(EMBED_MODEL)
CHUNKS      = _build_knowledge_base(HR_POLICY_SOURCE)
_EMBEDDINGS = _embedder.encode([c["chunk_text"] for c in CHUNKS], show_progress_bar=False)
print("[RAG] Knowledge base ready.", file=sys.stderr)


# ── Public API ───────────────────────────────────────────────────────────────
def retrieve(query: str, top_k: int = 3) -> list[dict]:
    """
    Embed the query and return the top-k most similar chunks.

    Each returned dict has:
        headings   : list[str]  — full hierarchical heading path
        content    : str        — paragraph text
        chunk_text : str        — breadcrumb + content
        score      : float      — cosine similarity
    """
    q_vec  = _embedder.encode(query)
    scores = np.dot(_EMBEDDINGS, q_vec) / (
        np.linalg.norm(_EMBEDDINGS, axis=1) * np.linalg.norm(q_vec) + 1e-9
    )
    top_idx = np.argsort(scores)[::-1][:top_k]
    return [{**CHUNKS[i], "score": round(float(scores[i]), 4)} for i in top_idx]


def format_context(results: list[dict]) -> str:
    """Format retrieved chunks into a readable context block."""
    parts = []
    for i, r in enumerate(results, 1):
        heading_path = " > ".join(r["headings"]) if r["headings"] else "General"
        parts.append(f"[Source {i} — {heading_path}]\n{r['content']}")
    return "\n\n---\n\n".join(parts)
