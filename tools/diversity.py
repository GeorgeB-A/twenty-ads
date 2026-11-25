"""Effective semantic diversity (k_eff) of a set of ad variants: the Vendi score of the cosine-similarity matrix.

k_eff answers "how many genuinely different ads does this set contain?": 1 for twenty copies of one ad,
20 for twenty unrelated ads. The dataset reports q = 1 (Shannon) and q = 2 (collision) orders, computed on
OpenAI text-embedding-3-small embeddings of "headline — body".

    from diversity import vendi, keff_from_texts
    vendi(cosine_matrix, q=1)
    keff_from_texts(["Ad one ...", "Ad two ..."], embed=my_embedding_function)

`embed` is any function list[str] -> array (n, d). Numbers are comparable to the dataset only with the
same embedding model."""
from __future__ import annotations
import numpy as np


def vendi(K, q=1):
    """K: n x n similarity matrix with ones on the diagonal (cosine similarities of unit vectors)."""
    K = np.asarray(K, dtype=float)
    n = K.shape[0]
    w = np.linalg.eigvalsh(K / n)
    w = w[w > 1e-12]
    if q == 1:
        return float(np.exp(-(w * np.log(w)).sum()))
    if q == 2:
        return float(1.0 / (w ** 2).sum())
    return float(((w ** q).sum()) ** (1.0 / (1 - q)))


def cosine_matrix(X):
    X = np.asarray(X, dtype=float)
    X = X / np.linalg.norm(X, axis=1, keepdims=True)
    return X @ X.T


def keff_from_texts(texts, embed, q=1):
    return vendi(cosine_matrix(embed(list(texts))), q=q)


def openai_embed(texts, model="text-embedding-3-small"):
    """The embedding model used in the dataset. Needs OPENAI_API_KEY."""
    from openai import OpenAI
    r = OpenAI().embeddings.create(model=model, input=list(texts))
    return np.array([d.embedding for d in r.data])


if __name__ == "__main__":
    import json, sys
    path = sys.argv[1] if len(sys.argv) > 1 else "../data/sets.jsonl"
    s = json.loads(open(path, encoding="utf-8").readline())
    print(s["set_id"], "stored k_eff (q=1):", s["diversity"].get("keff_vendi_q1"))
    print("identity check, 20 identical ads ->", round(vendi(np.ones((20, 20))), 3), "; 20 orthogonal ads ->", round(vendi(np.eye(20)), 3))
