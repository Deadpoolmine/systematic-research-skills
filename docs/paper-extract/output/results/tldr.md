# TLDR — The Clustering Strikes Back: Building Cost-Effective and High-Performance ANNS at Scale with Helmsman

**Authors:** Yuchen Huang, Baiteng Ma, Yiping Sun, Yang Shi, Xiao Chen, Xiaocheng Zhong, Zhiyong Wang, Yao Hu, Erci Xu, Chuliang Weng
**Venue:** OSDI 2026

## Overview
(1) RedNote's in-DRAM graph-based ANNS infrastructure has scaled to petabyte-level DRAM, incurring prohibitively high CapEx and OpEx as user base and content volume grow.
(2) HELMSMAN is a clustering-based ANNS system on all-flash servers that uses a custom userspace storage stack, learned adaptive pruning, and GPU-accelerated construction to replace in-DRAM HNSW.
(3) HELMSMAN saves over 90% of hardware costs — 40 machines with ~30-40 TB DRAM now sustain workloads that previously required ~35,000 CPU cores and ~0.35 PB DRAM.

## Big Background
(1) The rapid growth of vector data in search, recommendation, and advertising systems is pushing in-memory ANNS deployments to unsustainable petabyte-scale DRAM consumption.
(2) Modern NVMe SSDs (PCIe Gen5, ~12 GB/s per device, at ~1/40 the cost per GB of DRAM) have reached a performance/cost inflection point that enables SSD-backed ANNS.
(3) Production throughput SLAs only require ~32-43% of what in-DRAM deployments provision — the rest is capacity headroom for workload bursts, not throughput demand.

## Small Background
(1) Graph-based DRAM-SSD ANNS (DiskANN, Starling, PipeANN) fail to meet latency SLAs because their serialized, dependency-chain I/O during greedy graph traversal cannot exploit high SSD bandwidth, resulting in 10-25× throughput gaps to in-DRAM HNSW.
(2) SPANN, a clustering-based DRAM-SSD ANNS, uses batched, dependency-free I/O and can approach latency SLAs, but its throughput remains at only ~12-14% of in-DRAM HNSW due to kernel I/O stack overhead, fixed pruning, and slow construction.

## Problems
(1) Insufficient throughput: under production latency SLAs (5-10ms), clustering-based SPANN achieves only 12-14% of in-DRAM HNSW throughput even with 12 PCIe Gen5 SSDs.
(2) Unstable search quality: SPANN's fixed distance-based pruning cannot adapt to varying top-k (100-3,000) across different services, causing over 40% of queries to miss target recall.
(3) Slow index construction: single-node CPU-only construction takes hours to days for billion-scale datasets, incompatible with daily rebuild requirements.

## Root Cause
(1) The traditional kernel I/O stack imposes excessive software overhead (up to 58% of end-to-end latency) for batched, fixed-size reads characteristic of clustering-based ANNS.
(2) Existing pruning strategies rely on intermediate search results and iterative probe-compute-decide loops, which serialize I/O and conflict with SSD-friendly batched access.
(3) Single-node CPU-only k-means on high-dimensional vectors is computationally bound and cannot scale with data volume.

## Key Idea
(1) Clustering-based ANNS with batched, dependency-free I/O can match in-DRAM performance on modern NVMe SSDs if the storage stack, pruning, and construction are co-designed for ANNS-specific access patterns rather than relying on general-purpose system software.
(2) Unlike graph traversal which suffers from serialized I/O dependency chains, clustering-based search issues all cluster reads in parallel batches, making it fundamentally more SSD-friendly as SSD bandwidth grows.
(3) This insight is counter to the prevailing consensus that graph-based methods are superior — the authors argue that the hardware landscape has shifted enough to make clustering competitive again.

## Design Points
(1) ANNS-oriented userspace storage stack on SPDK that bypasses the kernel, places cluster lists as contiguous raw blocks on NVMe SSDs, and submits batched I/O commands with a single PCIe doorbell knock per batch.
(2) Leveling-learned search pruning (LLSP) using GBDT models: a router model predicts a coarse nprobe upper bound from query vector and top-k, then a level-specific pruning model refines it using centroid-distance distribution, without intermediate search results.
(3) GPU-accelerated elastic construction pipeline: GPUs generate coarse centroids, elastic CPU workers perform fine-grained balancing, and multi-core servers merge final indexes — enabling sub-hour 0.1B builds and hour-level 10B builds.

## System & Experiment
(1) Implemented as a production system on all-flash servers (96-core AMD EPYC, 12×96 GB DDR5, 12×PCIe Gen5 NVMe SSDs), deployed at Xiaohongshu for several months and actively rolling out.
(2) Evaluated on SIFT (0.1B, 10B) and five production datasets (RedSrch, RedRec, RedAds, RedCM, RedRAG) against HNSW, DiskANN, Starling, PipeANN, and SPANN.
(3) HELMSMAN achieves 2-16× throughput of other DRAM-SSD systems, up to 85% of in-DRAM HNSW throughput, while meeting latency SLAs — with 8.3× better throughput-per-dollar at 10B scale.
