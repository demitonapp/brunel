# Raw Cloud GPU Instance Pricing — 2026 Research

Method note: official pricing pages for AWS, Azure, RunPod, CoreWeave, Vast.ai, Modal and GCP are JS-heavy. Where the official page did not render, I used the **Azure Retail Prices API** (`prices.azure.com/api/retail/prices`, the official API behind Azure's calculator), **Vantage's instances.vantage.sh** (machine-readable mirror of the AWS/GCP/Azure price lists), the **official GCP accelerator-optimized pricing page** (rendered via a text proxy), and **gputracker.dev** (secondary aggregator, marked lower confidence). AWS/Azure/GCP/DigitalOcean/Lambda/Replicate/Modal figures below are from first-party sources.

---

## 1. AWS — [aws.amazon.com/ec2/pricing/on-demand](https://aws.amazon.com/ec2/pricing/on-demand/)

Source: AWS price list via [instances.vantage.sh](https://instances.vantage.sh/aws/ec2/g5.xlarge) (updated 2026-09-17). Prices are Linux, US East (N. Virginia). **Confidence: high** for on-demand/reserved; **medium** for spot (spot is regional/dynamic).

| Instance | GPU | On-demand $/hr | $/GPU-hr | Spot (listed) | 1yr / 3yr reserved |
|---|---|---|---|---|---|
| g5.xlarge | 1× A10G 24GB | **$1.0060** | $1.0060 | $0.636 (obs. us-east-1 $0.5291) | $0.634 / $0.435 |
| **g5.12xlarge** (render node) | 4× A10G 96GB | **$5.672** | $1.418 | $4.546 listed — **flag:** observed us-east-1 spot for g5.4xl/g5.8xl was $0.5637 / $0.7062, so the real g5.12xl spot is materially lower than $4.546 | $3.573 / $2.450 |
| g6.xlarge | 1× L4 24GB | **$0.8048** | $0.8048 | $0.629 listed; observed us-east-1 **$0.1879** (large discrepancy, flag) | $0.524 / $0.369 |
| g6e.xlarge | 1× L40S 48GB | **$1.861** | $1.861 | $1.701 | $1.172 / $0.804 |
| p3.2xlarge | 1× V100 16GB | **$3.06** | $3.06 | **$0.428** | n/a |
| p4d.24xlarge | 8× A100 40GB | **$21.957642** | **$2.7447** | $16.298 → $2.037/GPU-hr | $13.921 / $9.374 → $1.172/GPU-hr |
| p5.48xlarge | 8× H100 80GB | **$55.04** | **$6.88** | $20.788 → $2.5985/GPU-hr (p5.4xlarge 1-GPU spot obs. $1.9458) | n/a / $23.777 → $2.972/GPU-hr |

Spot is a market: us-east-1 g5.xlarge spot has been observed at $0.5291 and g6.xlarge at $0.1879 ([gputracker.dev/provider/aws](https://gputracker.dev/provider/aws)). Treat list spot prices as upper bounds.

## 2. Azure — [azure.microsoft.com/pricing/details/virtual-machines](https://azure.microsoft.com/en-us/pricing/details/virtual-machines/linux/)

Source: **official Azure Retail Prices API**, East US, Linux (`type: Consumption`). **Confidence: high** (spot = medium; Azure Spot prices are dynamic and the Low Priority meters are legacy).

| SKU | GPU | On-demand $/hr | $/GPU-hr | Spot $/hr |
|---|---|---|---|---|
| `Standard_NC4as_T4_v3` | 1× T4 16GB | **$0.526** | $0.526 | $0.1694 (US-East, gputracker) |
| `Standard_NC64as_T4_v3` | 4× T4 | $4.352 (Linux) | $1.088 | — |
| `Standard_NC24ads_A100_v4` | 1× A100 80GB | **$3.673** | $3.673 | **$0.67877** |
| `Standard_NC48ads_A100_v4` | 2× A100 80GB | **$7.346** | $3.673 | **$1.357541** |
| `Standard_NC40ads_H100_v5` | 1× H100 80GB NVL | **$6.98** | $6.98 | **$1.289904** |
| `Standard_NC80adis_H100_v5` | 2× H100 | **$13.96** | $6.98 | $2.579808 |
| `Standard_ND96isr_H100_v5` | 8× H100 | $98.32 | $12.29 | $18.169536 (Windows meter) |
| `NVadsA10_v5` (A10) | fractional vGPU | **price not found** | — | NV6ads 4GB slice **$0.0839**; NV12ads 8GB **$0.1678** (US-East) |

**Flag:** NVadsA10_v5 is *vGPU-partitioned* (4/8/12/24 GB slices), so a $/GPU-hour comparison vs a full A10 is misleading. Its product name did not appear in the Retail Prices API under `A10 v5`; on-demand not verified. Also available (not requested): NCads A100 v4 Low Priority East US meters at $0.735–$1.469/hr — legacy, not Spot.

## 3. GCP — [cloud.google.com/products/compute/pricing/accelerator-optimized](https://cloud.google.com/products/compute/pricing/accelerator-optimized)

Source: **official GCP accelerator-optimized pricing page**, Iowa (us-central1). **Confidence: high** for on-demand; medium for Spot (variable, changes up to daily). Note GCP's own page states it excludes GPU cost from the VM pricing pages — GPU line items are separate.

| Machine type | GPU | On-demand $/hr (whole VM) | $/GPU-hr | Spot $/hr (whole VM) | $/GPU-hr spot |
|---|---|---|---|---|---|
| g2-standard-4 | 1× L4 24GB | **$0.706832276** | $0.7068 | $0.424056 | $0.4241 |
| g2-standard-48 | 4× L4 | $4.001665392 | $1.0004 | $2.400672 | $0.6002 |
| a2-highgpu-1g | 1× A100 40GB | **$3.673385** | $3.6734 | **$2.20401** | $2.2040 |
| a2-highgpu-8g | 8× A100 40GB | $29.38708 | $3.6734 | $17.63208 | $2.2040 |
| a2-ultragpu-1g | 1× A100 80GB | **$5.06879789** | $5.0688 | $3.041237534 | $3.0412 |
| a3-highgpu-8g | 8× H100 80GB | **$88.490000119** | **$11.0613** | $52.962296548 | $6.6203 |
| a3-megagpu-8g | 8× H100 | $93.400712807 | $11.6751 | $55.894488548 | $6.9868 |
| a3-ultragpu-8g | 8× H200 | $84.806908493 | $10.6009 | $50.874449096 | $6.3593 |
| a4-highgpu-8g | 8× B200 | **N/A** (DWS only, $64.44–$90.22) | — | $39.6336 | $4.9542 |
| g4-standard-48 | 1× RTX PRO 6000 | $4.49993 | $4.4999 | $1.7429 | $1.7429 |

GPU-attachment (older, `n1`): T4 **$0.35/hr**, V100 **$2.48/hr**, P100 $1.46/hr, P4 $0.60/hr. Discounts: 1-yr resource CUD ≈37–55%, 3-yr up to 70%; sustained-use up to 30%; Spot up to 91% off but preemptible. A3/A4 are *not* eligible for SUD or flexible CUDs. **Flag:** Vantage's GCP pages show machine-only prices (e.g. a3-highgpu-1g $1.273/hr) and must not be read as GPU-inclusive.

## 4. Lambda — [lambda.ai/pricing](https://lambda.ai/pricing)

Source: official. **Confidence: high.** Self-serve on-demand; reserved capacity is "contact us" only. Prices per GPU-hr, before tax.

| GPU | $/GPU-hr | Notes |
|---|---|---|
| NVIDIA B200 SXM6 180GB | **$6.69** | |
| NVIDIA H100 SXM 80GB | **$3.99** | |
| NVIDIA A100 SXM 80GB | **$2.79** | |
| NVIDIA A100 SXM 40GB | **$1.99** | |
| NVIDIA Tesla V100 16GB | **$0.79** | |
| HGX B200 1-Click Cluster | **$9.86 / $9.36 / $8.87** | 16 / 64 / 256+ GPUs, 2 weeks–1 yr |

**Not listed / price not found:** A10 and GH200 no longer appear on Lambda's pricing page. No spot/preemptible tier exists.

## 5. RunPod — [runpod.io/pricing](https://www.runpod.io/pricing) (JS-blocked; figures via [gputracker.dev/provider/runpod](https://gputracker.dev/provider/runpod))

**Confidence: medium.** The official page served nav only. RunPod splits **Community Cloud** (cheaper, P2P hosts, interruptible) vs **Secure Cloud** (T3/T4 datacenters, higher price); gputracker does not label which tier each row is, so treat the low numbers as Community/Spot.

| GPU | Spot $/hr (from) | On-demand $/hr |
|---|---|---|
| RTX 3090 24GB | **$0.11** | ~$0.22 (see RTX 3080 Ti $0.18 for scale) |
| RTX 4090 24GB | **$0.20** | not verified on-demand |
| RTX A5000 24GB | $0.14 | — |
| A6000 / A40 48GB | A40 $0.20 | — |
| A100 80GB SXM4 | **$0.79–$0.95** | **$1.39–$1.49** |
| H100 80GB HBM3 | **$1.75** | not verified (H100 NVL from $1.40) |
| H200 | $2.29 | — |

Interruptible/Spot exists and saves ~50–80% but pods can be reclaimed without warning. Egress $0.10/GB.

## 6. Vast.ai — [vast.ai](https://vast.ai/) (marketplace; figures via [gputracker.dev/provider/vastai](https://gputracker.dev/provider/vastai))

**Confidence: medium–low — this is a P2P marketplace; prices vary per host and change hourly.**

| GPU | Typical interruptible/spot | Example on-demand |
|---|---|---|
| RTX 3090 24GB | **$0.02–$0.12/hr** (floor $0.021) | $0.1194 |
| RTX 4090 24GB | **$0.13–$0.35/hr** (floor $0.131) | ~$0.20–$0.35 |
| A100 40GB | from $0.08 | $0.0934 |
| H100 80GB | from $1.47 | $1.5550 |

Vast advertises free egress; **all storage is ephemeral** and hosts can reclaim "interruptible" instances without warning. No compliance certs or SLA.

## 7. CoreWeave — [coreweave.com/pricing](https://www.coreweave.com/pricing) (JS-blocked; figures via [gputracker.dev/provider/coreweave](https://gputracker.dev/provider/coreweave))

**Confidence: medium.** Listed as 8-GPU HGX nodes (US-East), on-demand; reserved/contracted rates are lower but not public.

| GPU | Node $/hr | $/GPU-hr |
|---|---|---|
| NVIDIA L40 (8×) | $10.00 | **$1.25** |
| NVIDIA L40S (8×) | $18.00 | **$2.25** |
| RTX PRO 6000 Blackwell (8×) | $20.00 | $2.50 |
| NVIDIA A100 (8× HGX) | $21.60 | **$2.70** |
| NVIDIA GH200 (1×) | $6.50 | $6.50 |
| NVIDIA HGX H100 (8×) | $49.24 | **$6.155** |
| NVIDIA HGX H200 (8×) | $50.44 | $6.305 |
| NVIDIA GB200 NVL72 | $42.00 | $10.50 |
| NVIDIA HGX B200 (8×) | $68.80 | $8.60 |

**Not listed / price not found:** RTX A4000 and A5000 are no longer on CoreWeave's public price sheet. No spot tier (0% spot share). Sales/waitlist process; egress $0.10/GB.

## 8. Paperspace (DigitalOcean) — [paperspace.com/pricing](https://www.paperspace.com/pricing)

Source: official page. **Confidence: high** for the fetched numbers; the page is legacy Paperspace CORE pricing and now carries a **"Paperspace is now part of DigitalOcean!"** banner — the DigitalOcean acquisition is live and branding is migrating.

| GPU | $/hr (hourly) | Notes |
|---|---|---|
| A4000 16GB | **$0.76** | also $488/mo |
| A5000 24GB | **$1.38** | also $891/mo |
| A6000 48GB | **$1.89** | also $1,219/mo |
| A100 80GB | **$1.15/hr (3-year commitment)** | on-demand not published |
| H100 | **$5.95/hr on-demand** ("special promo"); $2.24/hr = 3-yr commit | page renders the H100 card as $3.09/hr — inconsistent, flag |
| V100 16GB | **$2.30** | |
| RTX4000 / RTX5000 | $0.56 / $0.82 | |
| P4000 / P5000 / P6000 | $0.51 / $0.78 / $1.10 | |

**Flag:** the H100 and A100-80G on-demand rates are the weakest numbers here (promo/commitment caveats and a self-contradicting card). DigitalOcean's own GPU Droplet SKUs were not separately verified.

## 9. Modal — [modal.com/pricing](https://modal.com/pricing)

Source: official, fetched in full. **Confidence: high.** Billed **per second**; per-hour equivalents computed at ×3600.

| GPU | $/sec | $/hr |
|---|---|---|
| Nvidia T4 | $0.000164 | **$0.5904** |
| Nvidia L4 | $0.000222 | **$0.7992** |
| Nvidia A10 | $0.000306 | **$1.1016** |
| Nvidia A100 40GB | $0.000583 | **$2.0988** |
| Nvidia A100 80GB | $0.000694 | **$2.4984** |
| Nvidia L40S | $0.000542 | $1.9512 |
| Nvidia RTX PRO 6000 | $0.000842 | $3.0312 |
| Nvidia H100 SXM5 | $0.001097 | **$3.9492** |
| Nvidia H200 SXM | $0.001261 | $4.5396 |
| Nvidia B200 | $0.001736 | $6.2496 |
| Nvidia B300 | $0.001972 | $7.0992 |

CPU $0.0000131/core/s, memory $0.00000222/GiB/s, **Volumes $0.09/GiB/mo (first 1 TiB free)**. Free tier: Starter $0/mo with **$30/mo free compute**; Team $250/mo with $100/mo free compute. **Critical trap for hours-long renders: "Non-preemptible execution — 3× base prices."** Default Modal execution is preemptible; a guaranteed H100 therefore costs **$11.85/hr**, not $3.95. Region selection also costs 1.15–1.75× base.

## 10. Replicate — [replicate.com/pricing](https://replicate.com/pricing)

Source: official, fetched in full. **Confidence: high.** Billed per second. **Inference-oriented.**

| Hardware | $/sec | $/hr |
|---|---|---|
| Nvidia T4 16GB | $0.000225 | **$0.81** |
| Nvidia L40S 48GB | $0.000975 | **$3.51** |
| Nvidia A100 80GB | $0.001400 | **$5.04** |
| Nvidia H100 80GB | $0.001525 | **$5.49** |
| Nvidia H200 80GB | $0.001525 | $5.49 |
| 8× A100 80GB | $0.011200 | $40.32 |

**A40 is not listed — price not found** (Replicate's hardware list is now T4/L40S/A100/H100/H200). Multi-GPU (>2×) requires committed-spend contracts.

**Can it run a Blender render?** Not practically. Public models are request/response and billed per run. Custom *private* models run via Cog on dedicated hardware, but you **pay for setup time, idle time and active time**, there is no SSH/desktop, no persistent large scene storage, and no interactive control over a shell — you would have to package Blender as a Cog container and expose it as a prediction. For a multi-hour Cycles render this is the wrong abstraction; use a VM/pod provider instead. Effectively inference-only.

---

## Comparison: usable for an hours-long Blender Cycles render?

**Full VMs / pods — usable (persistent disk, SSH, arbitrary length):** AWS (g5.12xlarge is the canonical 4×A10G render node), Azure (NVadsA10_v5/NCasT4_v3), GCP (g2-standard), Lambda, RunPod Pods, Vast.ai, CoreWeave, Paperspace/DigitalOcean. All of these let you `apt install blender`, run `blender -b` with Cycles, and keep a filesystem between frames.

**Serverless — workable only with care:** **Modal** can run long batch functions and mount a Volume, so a distributed Blender tile render is feasible, but you must budget **3× for non-preemptible execution**, container/function timeouts, and no interactive debugging. **Inference-only / not suitable:** **Replicate**.

**Interruption risk (use checkpointing or restart-on-interruption):** AWS Spot (2-minute notice), GCP Spot/preemptible (30-second notice), Azure Spot, RunPod Spot (no warning), Vast.ai **interruptible** (host can reclaim with no warning). For an 8-hour render, prefer on-demand or reserved over spot unless your job checkpoints per frame.

## Egress / storage cost traps

- **AWS:** EBS gp3 ≈$0.08/GB-month and **keeps billing while the instance is stopped**; snapshots ≈$0.05/GB-month; S3 Standard ≈$0.023/GB-month; **S3/internet egress $0.09/GB** after the 100 GB/month free tier; NAT gateway $0.045/GB. A multi-TB EXR sequence pulled out of AWS is usually more expensive than the GPU time that made it. (Egress figure verified via gputracker; EBS/S3 rates not re-verified this session — medium.)
- **Azure:** egress ≈$0.087/GB; managed disks bill separately and persist across `stop` (you must **deallocate**). Azure's disk and egress line items are frequently larger than the T4/A100 hourly rate.
- **GCP:** egress ≈$0.08/GB (premium tier); Persistent Disk bills while the VM is stopped; **Local SSD is ephemeral** — render output on Local SSD dies with the instance; GPU-backed A3/A4 are excluded from SUD/flexible-CUD discounts.
- **Lambda:** persistent filesystem storage is billed per GB-month whether or not an instance is attached, plus egress on export. Worth confirming before parking TBs of frames. (Not verified this session.)
- **RunPod:** local disk is **ephemeral**; a Network Volume is required for persistence and bills continuously; **egress $0.10/GB**. Spot pods can vanish mid-render.
- **Vast.ai:** free egress, but **all storage is ephemeral — data is lost when the instance ends**. The dominant risk is losing a multi-hour render, not bandwidth.
- **Modal:** Volumes $0.09/GiB-month (first 1 TiB free) bill even at zero compute; preemptible-by-default means an interrupted long job is re-run.

**Cheapest plausible path for a long Cycles render:** single-GPU on-demand or 1-week-reserved A10G/L4/L40S/A100 on Lambda, RunPod Secure, or Paperspace CORE; use AWS g5.12xlarge only if the workflow is already EC2-native and the frames stay inside AWS. Avoid Replicate entirely, and avoid spot/interruptible tiers unless per-frame checkpointing is implemented.
