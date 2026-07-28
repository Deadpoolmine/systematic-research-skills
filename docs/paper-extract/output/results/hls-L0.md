# HLS-L0 — 7+1 Core Points Decomposition

**Paper:** The Clustering Strikes Back: Building Cost-Effective and High-Performance ANNS at Scale with Helmsman (Operational Systems)
**Authors:** Yuchen Huang, Baiteng Ma, Yiping Sun, Yang Shi, Xiao Chen, Xiaocheng Zhong, Zhiyong Wang, Yao Hu, Erci Xu, Chuliang Weng
**Venue:** 20th USENIX Symposium on Operating Systems Design and Implementation (OSDI 2026)

---

## 1. Overview

This paper presents HELMSMAN, a clustering-based ANNS (Approximate Nearest Neighbor Search) system deployed on all-flash servers at Xiaohongshu (RedNote) that replaces the company's previous petabyte-scale in-DRAM graph-based (HNSW) infrastructure. By combining a custom userspace storage stack that bypasses the kernel I/O path, a leveling-learned pruning module that adapts to varying top-k and query distributions, and GPU-accelerated elastic index construction pipelines, HELMSMAN achieves up to 85% of the throughput of in-DRAM ANNS while reducing hardware costs by over 90% (40 machines with ~30-40 TB DRAM replacing ~35,000 CPU cores and ~0.35 PB DRAM).

**Evidence:** Abstract ("HELMSMAN saves over 90% of hardware costs...40 machines now host ANNS workloads that previously required about 35,000 cores and 0.35 PB DRAM"), §1 Introduction ("HELMSMAN can use only 40 machines...saving more than 90% device costs").

---

## 2. Big Background — What broad research wave/trend enables this work?

The explosive growth of vector data in industrial-scale search, recommendation, and advertising systems has pushed in-memory ANNS infrastructure to petabyte-scale DRAM consumption, incurring prohibitively high CapEx and OpEx. Simultaneously, the rapid advancement of NVMe SSDs — particularly PCIe Gen5 drives delivering ~12 GB/s bandwidth per device at roughly 1/40th the cost per GB of DRAM — has created an opportunity to shift ANNS from pure in-memory deployments to SSD-backed architectures. This hardware inflection point, combined with the observation that production throughput requirements are only ~32-43% of what in-DRAM deployments actually provision (the rest being capacity headroom), motivates rethinking the ANNS storage hierarchy.

**Evidence:** §1 Introduction ("the ever-growing user base and content volume have led to an explosive increase in memory footprint and consequently huge CapEx and OpEx"), §3.1 ("the in-DRAM HNSW indexes...have already consumed PB-level DRAM in practice"), Table 1 (DRAM $8/GB vs. Gen5 SSD $0.2/GB, bandwidth 12×38 GB/s vs. 12×12 GB/s), §3.1 ("only ~32-43% is actually needed to maintain the required latency SLAs").

---

## 3. Small Background — What specific prior work does this directly extend?

HELMSMAN directly extends SPANN [17], a clustering-based DRAM-SSD ANNS that organizes vectors into size-balanced clusters with centroids in DRAM and posting lists on SSD. SPANN demonstrated that clustering-based ANNS can achieve low latency via batched, dependency-free I/O, but it suffers from three critical deficiencies: (1) low SSD bandwidth utilization (only ~20-60%) due to traditional kernel I/O stack overhead, (2) a fixed distance-based pruning rule that cannot adapt to varying top-k values or query distributions, and (3) single-node CPU-only index construction that takes hours to days for large datasets.

**Evidence:** §3.3 ("SPANN [17], a representative clustering-based ANNS, uses a clustered layout"), §3.4 ("SPANN uses only ~26-59% of the available bandwidth"), §3.4 ("SPANN's current strategy...relies on a fixed distance-based pruning rule"), §3.4 ("the existing implementation constructs the clustering structures on a standalone CPU node...construction time escalates from several hours to multiple days").

---

## 4. Problems — What concrete problems does this paper solve?

1. **Insufficient throughput for online SLAs.** Under latency SLAs (5-10ms), SPANN with 12 PCIe Gen5 SSDs achieves only ~12-14% of in-DRAM HNSW throughput, failing to serve as a viable replacement. (§3.4, Figure 7a)

2. **Unstable search quality due to fixed pruning.** SPANN's fixed distance-based pruning rule (Equation 1) cannot adapt to varying top-k (100-3,000) across different services, causing either wasted I/O from overscanning or recall degradation from underscannning. Over 40% of queries fail to meet the target recall. (§3.4, §5.4)

3. **Prohibitively slow index construction.** SPANN's single-node CPU-only construction takes tens of hours to multiple days for billion-scale datasets, incompatible with production requirements of daily rebuilds for search and up to tens of thousands of rebuilds per day for recommendation. (§3.4, Figure 7d)

4. **Low SSD bandwidth utilization.** The traditional Linux kernel I/O stack (libaio) consumes up to 58% of end-to-end I/O latency as software overhead, preventing clustering-based ANNS from exploiting modern high-bandwidth NVMe SSDs. (§4.2, Figure 9a)

**Evidence:** See per-problem citations above.

---

## 5. Root Cause — What fundamental bottleneck underlies all problems?

The fundamental bottleneck is the **mismatch between ANNS access patterns and the conventional system software/hardware stack**: (1) The kernel I/O stack is optimized for general-purpose workloads, not for the batched, fixed-size, dependency-free reads characteristic of clustering-based ANNS, causing excessive software overhead that prevents SSDs from being driven at near-hardware speeds. (2) Existing pruning strategies are designed for in-DRAM iterative search (checking intermediate results per step), conflicting with SSD-friendly batched I/O. (3) Single-node CPU-only construction cannot scale with data volume because k-means on high-dimensional vectors is computationally bound and lacks parallelism. All three share the same deeper cause: system components (storage stack, pruning, construction) were not co-designed with the specific I/O and computation patterns of clustering-based ANNS.

**Evidence:** §4.2 ("the overhead of the traditional I/O stack with libaio dominates the end-to-end path (up to 58% of the total)"), §4.3 ("Such iterative probe–compute–decide loops serialize cluster I/Os, and thus are unfriendly to the batched SSD reads"), §4.4 ("k-means on large-scale datasets incurs repeated distance calculations on high-dimensional vectors and thus places a heavy load which is beyond the capability of a CPU").

---

## 6. Key Idea — What is the ONE core insight? (≤1 sentence)

**Clustering-based ANNS, when paired with a co-designed userspace storage stack, learned adaptive pruning, and heterogeneous acceleration, can match the latency SLAs of in-DRAM graph-based ANNS at a fraction of the hardware cost, because its batched, dependency-free I/O pattern is fundamentally better suited to modern high-bandwidth NVMe SSDs than the serialized, dependency-chain I/O of graph traversal.**

**Evidence:** §4.1 ("The key idea is eliminating overhead from I/O software and introducing adaptive learning-based models"), Abstract ("clustering-based ANNS...can be expected to achieve low latency that meets our SLA and also be scaled for throughput by adding more SSDs"), §3.3 caption ("the clustering-based SPANN shows nearly qualified search latency and scalable throughput under the large top-k values").

---

## 7. Design Points — What are the 2-5 technical contributions?

1. **ANNS-oriented userspace storage stack (§4.2).** Built on SPDK to bypass the kernel I/O stack entirely. Cluster lists are placed as contiguous logical blocks on raw NVMe SSDs with a chunk-based allocator. I/O commands are batched and submitted directly to hardware queues with a single PCIe doorbell knock per batch, eliminating per-command overhead. Metadata (index name, cluster-to-LBA mapping, pruning models, centroid index) is stored as regular files on a separate SATA SSD. This achieves ~70-85% SSD bandwidth utilization vs. ~20-55% for baselines.

2. **Leveling-learned search pruning (LLSP) (§4.3).** A two-stage GBDT-based pruning pipeline: (a) a router model predicts a coarse upper-bound nprobe level based on query vector and top-k; (b) a level-specific pruning model further refines nprobe using query vector, top-k, and centroid-distance distribution features, without relying on intermediate search results. This keeps I/O batched while adapting to per-query difficulty. Yields 5-25% throughput improvement over fixed pruning and ensures >80% of queries meet target recall (vs. <60% for fixed pruning).

3. **GPU-accelerated and elastic index construction (§4.4).** A three-step pipeline: (1) Multi-GPU servers run coarse k-means to generate initial centroids; (2) local CPUs or elastic CPU workers perform fine-grained cluster splitting, balancing, and boundary padding; (3) multi-core servers merge shards, build centroid graphs, and train pruning models. GPU acceleration provides up to ~10× speedup for 0.1B-scale builds (under 1 hour), and elastic scaling to 10^4 CPU cores enables 10B-scale builds within ~4-7 hours.

4. **Production deployment with operational robustness (§6).** Redundant cluster-list copies mitigate SSD die-level conflicts from query hotspots (1.5-2× throughput ceiling improvement). QoS policy ensures online traffic always preempts offline construction tasks. A hybrid freshness design maintains recent insertions in an auxiliary in-memory index with tombstone bitmap for deletions.

**Evidence:** See per-point section citations above.

---

## +1. System & Experiment — How was it implemented and evaluated?

**Implementation:** HELMSMAN is implemented as a production system deployed at Xiaohongshu (RedNote). The serving nodes are all-flash servers with 96-core AMD EPYC 9654 CPUs, 12×96 GB DDR5 DRAM, and 12×1.92 TB PCIe Gen5 NVMe SSDs. The userspace storage stack is built on SPDK [14]. The pruning module uses GBDT (LightGBM). GPU acceleration uses NVIDIA L20 GPUs with Faiss-based k-means. An open-source proof-of-concept is available at https://github.com/Red-EAD/helmsman.

**Datasets:** SIFT (0.1B, 10B), plus five production datasets: RedSrch (0.5B, 10B), RedRec (0.1B), RedAds (20M), RedCM (0.1B), RedRAG (4M), spanning 64-1024 dimensions and top-k ranges of 10-3,000.

**Baselines:** In-DRAM HNSW (production reference), DiskANN, Starling, PipeANN, SPANN (DRAM-SSD clustering baseline).

**Key results:**
- 2-16× higher throughput than existing DRAM-SSD ANNS; up to 85% of in-DRAM HNSW throughput, meeting latency SLAs (§5.2).
- 1.6-7.5× SSD bandwidth utilization improvement; up to 87% throughput gain from SSD hardware upgrades (§5.3).
- >80% of queries individually meet target recall vs. <60% for fixed pruning (§5.4).
- 0.1B index built within 1 hour; 10B index within 4-7 hours with elastic scaling (§5.5).
- >90% DRAM reduction; 8.3× throughput-per-dollar improvement for 10B-scale deployment (§5.6).
- Production: 40 machines replace ~35,000 CPU cores and ~0.35 PB DRAM, operating stably for several months (§6.1).

**Evidence:** §5 Evaluation, §6 Deployment.
