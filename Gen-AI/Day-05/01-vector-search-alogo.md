# Vector-Search Algorithms: One-Block Deep-Dive Reference

Common notation:  
- **N** = collection size  
- **d** = vector dimensionality  
- **Distance**: cosine or L2  
- **Recall@k**: fraction of true top-k returned  

---

## 1. Brute-Force (Exact Nearest-Neighbour)
Store vectors as-is; compute distance to **every** vector for each query.  
**Complexity**: O(N·d) per query.  
**Pros**: 100 % recall, trivial code.  
**Cons**: 1 B vectors ⇒ 1.5 trillion multiply-adds; unusable for real-time.  
**Use**: offline baseline or tiny datasets (< 1 M).

---

## 2. Inverted File Index (IVF) = Clustering Speed-Up
**Training**: run K-means to obtain **k** centroids (k ≈ √N).  
Each vector is assigned to its closest centroid → inverted lists `L[i]`.  
**Search**: find **nprobe** closest centroids to query **q**, scan only those lists.  
**Complexity**: centroid scan O(k·d) + list scan O((N/k)·nprobe·d).  
**Knob**: raise **nprobe** → higher recall, slower; typical values 8–64.  
**Edge case**: true neighbour may sit just across a cluster border → probe multiple lists or use **Adaptive IVF**.  
**Code** (FAISS):  
```python
index = faiss.IndexIVFFlat(quantizer, d, nlist=4096)
index.train(xb); index.add(xb)
index.nprobe = 16
D, I = index.search(xq, k)
```

---

## 3. Binary Space Partitioning (KD-Tree & friends)
Recursively split space along axes until leaves contain ≤ **leaf_size** vectors.  
Search traverses to a leaf, then back-tracks when bounding boxes could hide a closer point.  
**Complexity**: O(log N) only in low dimension; in high-d most branches must be visited → degrades to O(N).  
Spotify used **Annoy** (random-projection trees) until 2023, then switched to quantization-based methods.  
Still useful for **d < 30** and read-only, memory-mapped indices.

---

## 4. Hierarchical Navigable Small World (HNSW) – Industry Default
Treats vectors as nodes in a **multi-layer graph**.  
**Layer 0** (ground) keeps all vectors with short edges; higher layers = sparse “highway” nodes for long jumps.  
**Insertion**: random level = floor(−ln(rand)·mL); connect to M nearest neighbours at each layer; trim edges to keep strongest.  
**Search**: start at top-layer entry point, greedy best-first towards query; drop to next layer; repeat until layer 0; collect **ef** candidates.  
**Complexity**: O(log N) hops, sub-millisecond for 100 M vectors.  
**Memory**: ~(M + 1)·N·4 bytes + raw vectors.  
**Pros**: fastest latency, incremental updates, no re-training.  
**Cons**: RAM heavy; hyper-params (M, efConstruction, efSearch) need tuning.  
Open-source winners: hnswlib, FAISS-HNSW, Vespa, Weaviate, Pinecone, Milvus.

---

## 5. Product Quantization (PQ) – Memory Squeezer
**Problem**: 1 B × 1536 dims × 4 bytes = 6 TB RAM.  
**Idea**: split vector into **m** sub-vectors (e.g. 32), run k-means (k = 256) on each chunk → centroid id fits in **1 byte**.  
Storage drops from 6 KB to **m bytes** (192× compression).  
**Distance**: pre-compute table of query-chunk to all centroids, then sum look-ups.  
**Loss**: Recall@1 drops ~1–3 % with 8-bit PQ; coarser quant (4-bit) ~5–10 %.  
**Variants**: OpQ (rotated PQ), RQ (residual quantizers) for better quality.  
**Hybrid**: IVF-PQ – IVF finds clusters, PQ inside clusters gives sub-millisecond search on 1 B+ vectors.  
FAISS one-liner:  
```python
index = faiss.IndexIVFPQ(quantizer, d, nlist=4096, m=32, bits=8)
```

---

## 6. Production Recipe
| Size | Algorithm | RAM | p99 Latency | Recall@10 |
|------|-----------|-----|-------------|-----------|
| < 1 M | HNSW or IVF-flat | 4–8 GB | 1–3 ms | 0.995 |
| 1 M–100 M | IVF-PQ | 20–40 GB | 5–10 ms | 0.96 |
| 100 M–1 B | IVF-PQ + disk | 100 GB | 10–20 ms | 0.94 |
| 1 B+ | Sharded IVF-PQ on GPU | 500 GB | < 50 ms | 0.92 |

**Tuning**: benchmark Recall-vs-QPS on real query distribution; start with IVF-PQ (fastest to train), move to HNSW if memory allows and online updates are required; combine hot-shard HNSW with cold-shard IVF-PQ for cost balance.