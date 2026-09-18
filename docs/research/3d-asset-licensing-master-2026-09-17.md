# 3D Scans, Photogrammetry & Reference Imagery — Licensing Master Reference

**For:** a MONETISED Instagram Reels channel (vertical 9:16, AI voiceover, no on-camera presenter) on the history of engineering. Episode 1: Marc Brunel's tunnelling shield, Thames Tunnel (1825–1843). Solo operator, Blender + Python.

**Research date:** 17 September 2026. Every claim below was checked against a live source on that date. Licence terms change; re-verify before relying.

**Confidence convention.** `HIGH` = verbatim text fetched from the primary source this session. `MEDIUM` = fetched from an authoritative secondary source, or fetched but with an unresolved ambiguity. `LOW` = inferred or single weak source. `INFERENCE:` = my reasoning, not a citation. `UNVERIFIED` = could not confirm; asserted nowhere.

**This file is the entry point.** §1 is the table to act on; §3 and §4 are the merged form of the
four long-form source documents, which now live in
[`evidence/`](evidence/) — see [`evidence/README.md`](evidence/README.md) for what each one carries
that this summary cannot (chiefly: what could *not* be verified, and why).

- [`evidence/3d-asset-licensing-report-2026-09-17.md`](evidence/3d-asset-licensing-report-2026-09-17.md) — full Smithsonian / Scan the World / Sketchfab report.
- [`evidence/licensing-research-monetised-reels-2026-09-17.md`](evidence/licensing-research-monetised-reels-2026-09-17.md) — Internet Archive, Library of Congress, HABS/HAER.
- [`evidence/licensing-research-smg-europeana.md`](evidence/licensing-research-smg-europeana.md) — Science Museum Group, Europeana.
- [`evidence/cc-attribution-monetised-reels-advice.md`](evidence/cc-attribution-monetised-reels-advice.md) — full legal analysis (≈9,000 words, every authority cited).

*This is legal research, not legal advice.*

---

## 1. EXECUTIVE DECISION TABLE

Classified by **licence structure**, not by individual item. "Safe" assumes the item-level rights statement matches the source's default — always verify per item.

| Source | Default licence for images/3D | Verdict for a monetised channel |
|---|---|---|
| **Public domain works** (published ≤1930 US; PD-old-100; Crown copyright expired) | none — rights expired | **SAFE** |
| **Smithsonian Open Access** — CC0 subset | `CC0` | **SAFE** (best 3D/imagery source) |
| **Smithsonian** — "usage conditions apply" subset | bespoke | **PROHIBITED** (commercial expressly excluded) |
| **Rijksmuseum** PD images | CC0 / Public Domain Mark | **SAFE** (verify per item) |
| **Getty Open Content** | CC0 (verify) | **SAFE** (verify per item) |
| **Sketchfab** `cc0` | "CC0 Public Domain" | **SAFE** |
| **Sketchfab** `by` | "CC Attribution" | **SAFE WITH ATTRIBUTION** |
| **Sketchfab** `by-sa` | "CC Attribution-ShareAlike" | **REQUIRES A DECISION** (viral licence) |
| **Sketchfab** `by-nd` | "CC Attribution-NoDerivs" | **DO NOT USE** in a Blender-derived render |
| **Sketchfab** `by-nc` / `by-nc-sa` / `by-nc-nd` | "No commercial use" | **PROHIBITED** |
| **Sketchfab Store** `st` / `free-st` | Standard / Free Standard | **SAFE** (royalty-free, no credit) |
| **Sketchfab Store** `ed` | Editorial | **PROHIBITED** (no commercial/promotional) |
| **Science Museum Group / National Railway Museum** images | `CC BY-NC-SA 4.0`, `CC BY-NC-ND 4.0`, or `OGL v3.0` | **PROHIBITED** except the OGL v3.0 subset |
| **Science Museum Group** metadata (title/made/maker/details) | CC0 | **SAFE** |
| **Science Museum Group** descriptions/text | CC BY 4.0 | **SAFE WITH ATTRIBUTION** |
| **Science Museum Group** Sketchfab — 8 of 52 models | CC0 | **SAFE** (none Brunel-related) |
| **Science Museum Group** Sketchfab — 33 of 52 models | CC BY-NC | **PROHIBITED** |
| **Scan the World (MyMiniFactory)** | `CC BY-NC-SA 4.0` + MMF ToS | **PROHIBITED** (two independent blockers) |
| **Europeana** — API metadata | CC0 | **SAFE** |
| **Europeana** — items with `edm:rights` ∈ {PDM, CC0, CC BY, CC BY-SA} | per record | **SAFE / SAFE WITH ATTRIBUTION / SA decision** |
| **Europeana** — items with InC / InC-EDU / InC-OW-EU / CNE / NoC-NC / NoC-OKLR | rights statement only | **PROHIBITED** |
| **Internet Archive** — IA's own scans of pre-1930 books | PD | **SAFE** |
| **Internet Archive** — uploader/Community content | self-declared | **REQUIRES A DECISION → treat as unusable** |
| **Internet Archive** — lending library | in copyright | **PROHIBITED** |
| **Library of Congress** — PD items, HABS/HAER/HALS | PD | **SAFE** |
| **Library of Congress** — "Free to Use and Reuse" | not a licence | **REQUIRES A DECISION** |
| **Wikimedia Commons** — ALL files (NC is banned by policy) | per file; always commercially reusable | **SAFE** except CC BY-SA (viral) — see §3.10 |
| **Wikimedia Commons** CC BY-SA | per file | **REQUIRES A DECISION** |
| **British Library / Flickr Commons** | "No known copyright restrictions" | **REQUIRES A DECISION → treat as unusable** |
| **Historic England Archive / Britain from Above** | bespoke / non-commercial free tier | **REQUIRES A DECISION → licensed, not free** |
| **The National Archives** — OGL v3 catalogue metadata | OGL v3.0 | **SAFE WITH ATTRIBUTION** |
| **The National Archives** — digitised record images | free to view ≠ free to reuse | **PROHIBITED** without licence |
| **Network Rail** | bespoke | **UNVERIFIED / assume restricted** |
| **TU Delft / Charles Babbage Institute** | per item | **UNVERIFIED (CBI: not relevant)** |

**One-line rule for the channel:** use **CC0, public domain, CC BY, and Standard-licensed purchases**. Never use **NC**, **ND**, **Scan the World**, **SMG images**, or **Flickr Commons / IA uploader content**. Treat **SA** as a business decision.

---

## 2. EPISODE 1 — WHERE THE ACTUAL MATERIAL IS

The single most useful discovery: **the Thames Tunnel and Brunel material you need is overwhelmingly out of copyright, and the good open-licensed copies are in US institutions rather than UK ones.**

| Need | Best source | Licence | Why |
|---|---|---|---|
| **Sectional drawings of the tunnelling shield** | **Internet Archive `explicationdestr00unse`** (1837, Getty Research Institute) + 4 IA pamphlets | PD | **the single best Episode 1 asset found** |
| Period engravings / prints of the shield & tunnel | **Wikimedia Commons** (Penny Magazine 1832 woodcuts etc.) | PD | best *image* of the shield; every Commons file is commercially reusable |
| Marc Brunel portraits / biography material | **Commons** + **Smithsonian Open Access** | PD / CC0 | Northcote & Howlett portraits; `siris_sil_4317` |
| Tunnelling-shield geometry reference | **Build it in Blender** from the PD 2D drawings | your own work | **no Thames Tunnel 3D model exists in any source surveyed** |
| Industrial 3D scans (steam, boilers, machine tools) | **Sketchfab** `cc0` / `by`; **SMG Sketchfab** 8 CC0 models; **Europeana** 3D (~4,906 commercial-safe) | CC0 / CC BY | verified real industrial-heritage content exists |
| 19th-c engineering **construction photography** | **Getty Open Content** (Manchester Ship Canal 1894, Gotthardbahn c.1875–82) | CC0 | strongest openly licensed engineering-photo pool found |
| Museum-object reference photos | **SMG collection** — *research only* | CC BY-NC — do not publish | metadata CC0 reusable; images are not |
| Measured engineering drawings | **LoC HABS/HAER/HALS** (US federal PD); Commons Box Tunnel drawing | PD | covers bridges, dams, factories, railways, canals — American |

The strategic conclusion: **build Episode 1 on PD 2D visual material (engravings, patent drawings, watercolours) plus your own Blender modelling, and treat 3D museum scans of the physical machine as licensed material to be negotiated, not assumed.** The legal reason is in §4.4.

---

## 3. SOURCE-BY-SOURCE FINDINGS

### 3.1 Science Museum Group (sciencemuseumgroup.org.uk) — includes the National Railway Museum

**Licence structure — this is the critical finding.** SMG does *not* use CC0 for images. Per the SMG bulk-datasets page (dated 6 August 2025):

- **Metadata** (title, made, maker, details): **Creative Commons Zero (CC0)**. HIGH
- **Descriptions and all other text**: **Creative Commons Attribution 4.0**. HIGH
- **Images**: "Each image referenced within the dataset has it's own copyright." The page lists only **three** permitted image licences:
  - `CC BY-NC-SA 4.0`
  - `CC BY-NC-ND 4.0`
  - `Open Government Licence v3.0`
  
  Verbatim from the page: "Please check and only use image which fall under on of ther following three licence and attribute accordingly." HIGH
- "**Always check the licence** … Many records contain more than one image and while the first image may be made available under an open source licence that does not necessarily hold true for all other image on that record."

**Quantified.** The collection site's own filter for NC-licensed images — `https://collection.sciencemuseumgroup.org.uk/search/image_license` — returns **212,113 records** (205,203 objects, 6,910 documents). HIGH (API, 17 Sep 2026). The About page describes this filter as "records with images released under a **Non-Commercial** Creative Commons licence", and directs commercial users elsewhere: "If you would like to use our images commercially, please **contact the Science & Society Picture Library** (scienceandsociety.co.uk)." HIGH

→ **There is effectively no CC0 image pool at SMG.** The only commercially usable image licence in the set is **OGL v3.0** — which *does* permit commercial use with attribution. UNVERIFIED: how many images carry OGL v3.0 versus NC; the datasets page does not give a breakdown, and I did not enumerate it.

**Worked example — the flagship NC-wrapper case.** Object `co66652` "Thames Tunnel" has **20 images**: **18 carry `CC BY-NC-SA 4.0`** with copyright `© The Board of Trustees of the Science Museum`, and **2 carry no licence at all** with third-party copyright (`T Blood`, `J Fairburn`). HIGH (fetched `/api/objects/co66652/thames-tunnel`, 17 Sep 2026). This is exactly the "NC wrapper on a PD object" problem in §4.4 — and note the second trap: *some images in a CC-licensed record are unlicensed third-party works.*

**Held Thames Tunnel material (HIGH, API search, 1847 total results for "Thames Tunnel"):**

| ID | Title | Type |
|---|---|---|
| `co27198` | Thames Tunnel opening commemorative medal, 1843 | object |
| `ap24782` | Thames Tunnel Company | person/org |
| `co66652` | Thames Tunnel | object |
| `co8012665` | The Thames Tunnel | object |
| `co8013323` | Print: Thames Tunnel | object |
| `co8013322` | Print: Thames Tunnel Rotherhithe Entrance | object |
| `co8013321` | Print: Proposed entrance to the Thames Tunnel | object |
| `co65677` | Lithograph, "The Thames Tunnel" | object |
| `co66671` | 'The Thames Tunnel' peepshow, with original box | object |
| `co66194` | Advertisement of 1840 for the Thames Tunnel | object |
| `co524211` | Commemorative trowel used to lay the first stone of the Thames Tunnel | object |
| `aa110098623` | "Thames Tunnel. Copies of Treasury Minutes and Correspondence…" | document |
| `aa110098622` | "A plan shewing the progress of the Thames Tunnel" | document |
| `aa110067120` | Notebooks of G.H. Wollaston relating to Thames Tunnel from Rotherhithe to Wapping | document |
| `co8013314` | Print: The Thames Tunnel./ Published by R.H.Laurie | object |
| **`co58317`** | **Model of part of Marc Brunel's Thames Tunnel second shield — ★ NO IMAGE, NO 3D SCAN** | object |
| `co8234340` | model of tunnelling shield | object |
| `co8013336` | Print: Section through the Thames Tunnel and three diagrams of the interior (1981-1015/28) — 3 images: 2× CC BY-NC-SA + **1 with no licence, © "T Blood"** | object |
| `co58511` | Model, Greathead Shield, Blackwall Tunnel | object |
| `co58560` | Whitaker Tunnelling Machine | object |
| `co46742` / `co27093` | Bust of Marc Isambard Brunel / Portrait bust MIB | object |
| `co211045` / `co211006` | Portrait bust IKB | object |
| `aa110066849` | Collection of documents relating to Marc Isambard Brunel, mainly the Thames Tunnel (MS/0346) | document |
| `aa110066942` | Papers relating to M.I. Brunel and the construction of the Thames Tunnel | document |
| `aa110066756` | Engineering drawing: Plunging pump as used at the Thames Tunnel | document |
| `aa110098619` | Letter Brunel → M. D'avannes re working conditions, accidents, health of the workforce | document |
| `aa110098624` | Report from the Select Committee on the Thames Tunnel + Minutes of Evidence | document |
| `aa110134578` | Letter re steam engines mentioning another flood and how 'young Brunel… had a narrow escape' | document |
| `aa110133444` | Printed circular: Progress and state of the Tunnel under the Thames | document |

**Search counts, all live 17 Sep 2026 (HIGH):** `thames tunnel` → **1,847** (942 objects, 868 documents, 37 people) · `brunel` → **516** · `marc isambard brunel` → **2,412** · `tunnelling shield` → **391**.
**Key people records:** `cp37092` Marc Isambard Brunel · `cp520` Isambard Kingdom Brunel · `ap265` · `ap24334` · `cp32182` · `ap24964` Wollaston, George Hyde · `ap25463` Beamish, Richard.
**Sitemap of all records:** `https://s3-eu-west-1.amazonaws.com/smgco-sitemaps/sitemap.xml`

**Brunel holdings (HIGH):** 516 results for "Brunel" — **328 objects, 117 documents, 71 people**. Key person records: `ap24334` (Brunel, Marc Isambard), `cp37092` (Marc Isambard Brunel), `ap265` / `cp520` (Isambard Kingdom Brunel). Object `co226812` "Isambard Kingdom Brunel, 1848".

**API — exact mechanics.**
- Base/spec: JSON:API. Docs: `https://github.com/TheScienceMuseum/collectionsonline/wiki/Collections-Online-API` (HIGH — linked from SMG's own API page).
- Search: `https://collection.sciencemuseumgroup.org.uk/search?q={query}` — **requires `Accept: application/json`**.
- Object: `https://collection.sciencemuseumgroup.org.uk/api/{type}/{id}/{slug}` — e.g. `/api/objects/co26704/rocket-locomotive`. **The slug is required**; `/api/objects/{id}` alone returns the HTML shell. HIGH (tested).
- Response content type: `application/vnd.api+json`.
- **Per-image licence path:** `data.attributes.multimedia[].legal.rights[].licence` and `.copyright`; credit at `multimedia[].credit.value`. HIGH (extracted).
- **No API key.** HIGH.
- **RATE LIMIT — a hard, practical constraint.** After roughly 15–20 requests in a few minutes the API returns **HTTP 429 with body `Rate limited - please slow down`** (31 bytes, `text/plain`). HIGH (observed, then reproduced after a ~90 s cooldown). SMG states the cause on the datasets page: "in response to overly aggressive crawling we had to **heavily rate limit**." Any pipeline must throttle and back off; expect to use the bulk dumps instead.
- **Bulk downloads** (`https://coimages.sciencemuseumgroup.org.uk/datasets/index.html`, dated 6 Aug 2025). HIGH:
  - `smg_object_records_with_CC_images_09_04_2025.json.zip` — 150,355 records, 145 MB
  - `smg_object_records_all_09_04_2025.json.zip` — 525,595 records, 322.8 MB
  - `smg_document_records_with_CC_images_09_04_2025.json` — 7,017 records, 159.2 MB
  - `smg_document_records_all_09_04_2025.json` — 77,409 records, 560.8 MB
  - `smg_people_and_company_records_06_08_2025.json` — 23,684 records, 61.4 MB
  - CSV subsets and `smg_all_medium_thumbnail_images_09_04_2025.zip` (1.19 GB)
  - **Stated scope: "for academic or personal research use."** That is a contractual limit in tension with a monetised channel — even for the CC0 metadata. MEDIUM.
- **Prohibited harvesting (HIGH, verbatim):** "Images must not be harvested from our **IIIF and Zoom endpoints**, we will block access and may act again anyone doing so." And: "Pleas do not unnecessarily download the larger image sizes in bulk or you may be rate limited."

**SMG's OWN DEFINITION OF "COMMERCIAL" — decisive, and it condemns a monetised Reels channel (HIGH, verbatim from `https://group.sciencemuseum.org.uk/creative-commons/`).** SMG's site states that commercial use includes:
> *"use that promotes a product or service that is commercial"*, *"use by charities, including the trading arms of charities"*, and *"free-entry events … that promote a product of services"*.
and that **non**-commercial includes:
> *"use on personal social media accounts, **PROVIDED the individual is not promoting themselves commercially**"*.
> *"For all commercial usage, contact Science and Society Picture Library"* — `https://www.scienceandsociety.co.uk/`

**→ This is the rights-holder's own published test, and a monetised channel that promotes the creator's own work fails it outright.** It is also the clearest available illustration of the general NC analysis in §4.2.

**⚠️ TRAP — the documented `filter[image_licences]` parameter is SILENTLY IGNORED by the live API (HIGH, measured).** Counts are identical with and without it, including for the value `CC0`:
- `q=thames` → 1401; `+filter[image_licences]=CC BY-NC-SA` → 1401; `+filter[image_licences]=CC0` → **1401** (i.e. the CC0 filter returns the same 1401 records).
- `q=tunnel` → 2454; `+filter[image_licences]=CC BY-NC-ND` → 2454.
By contrast `filter[makers]` **does** filter correctly (a non-match returns 0). **Never use `image_licences` to prove a licence** — it silently returns everything. The website's own `/search/image_license` path is a different (display) route and does work as a UI filter, but the API parameter does not.

**Also note:** the API docs claim the licence path is `source.legal.rights.usage` — **that path does not exist.** The live path is `data.attributes.multimedia[N].legal.rights[N].licence` (plus `.copyright`), with `multimedia[N]["@processed"].large.location` / `.zoom.location` for the files. Object-level `attributes.legal` is usually just `{"credit": "<donor>"}` and is **not** a licence.

**SMG's 3D lives on Sketchfab, not in the collection API (HIGH).** Account: `https://sketchfab.com/sciencemuseum` (uid `0dca0f8b55514f1e84ddadf47cc299a8`); query it with `https://api.sketchfab.com/v3/models?user=sciencemuseum&count=24` (note: the `/v3/users/sciencemuseum/models` path 404s).
**Full catalogue as at 17 Sep 2026 — 52 unique models:**
- **33 × "CC Attribution-NonCommercial"** (downloadable) → **PROHIBITED**
- **8 × "CC0 Public Domain"** (downloadable) → **SAFE** ← *Amputation Saw; Figurehead – Science Museum; Chinese Junk Ship – Science Museum; Catalytic converter 1982–1983; Pill cutter Europe 1801–1900; Packet of Cigarettes; Pharmacy Leech Jar; Model of a human brain*
- 1 × CC BY-NC-SA (Enigma machine) → **PROHIBITED**
- 10 × no licence at all (not downloadable) → **PROHIBITED**

**★ THE DECISIVE NEGATIVE FOR EPISODE 1: no Brunel, Thames Tunnel or tunnelling-shield 3D model exists — not in SMG's 52 Sketchfab models, not anywhere in the sources surveyed.** The nearest engineering item is **"Stephenson's Rocket" (`09d73611eeda4aa7a4f3643766b340da`), and it is CC Attribution-NonCommercial.** Furthermore **`co58317` "Model of part of Marc Brunel's Thames Tunnel second shield" — the single most relevant object in the SMG collection — has ZERO images and no 3D scan.**
→ **You must build the tunnelling shield in Blender.** SMG's archive *descriptions* are CC0/CC BY and can be cited and linked; its *images* cannot be shown.

**Object pages embed Sketchfab only in server-rendered HTML, not in the JSON API (HIGH).** `co26704` (Rocket)'s HTML contains `sketchfab.com/3d-models/09d73611eeda4aa7a4f3643766b340da/embed`, while the same object's JSON API response contains **zero** `sketchfab` hits. Map object↔model by scraping HTML or via the Sketchfab API.

**Other SMG operational traps (HIGH):**
- **`robots.txt` forbids the documented API.** Verbatim: `Crawl-Delay: 1`, `Disallow: /api/`, `Disallow: /iiif/`, `Disallow: /iris/`, `Disallow: /barcode/`, **`Disallow: /*?*`** (every query-string URL). The operators' own robots rules contradict their API documentation. Treat robots as the stated wish: **use the bulk dumps for volume; make few, slow interactive calls.**
- **IIIF/Zoom harvesting is expressly prohibited** (see the datasets page) — yet technically open: `zoom.sciencemuseumgroup.org.uk/iiif/3/52%2F199%2F…ptif/info.json` returns IIIF v3 level 2 with `ACAO *`. **Open but contractually forbidden. Do not use.**
- **No OAI-PMH** (`/oai`, `/api/oai` → 404). **No S3 bucket for collection JSON** (only the sitemap bucket: `https://s3-eu-west-1.amazonaws.com/smgco-sitemaps/sitemap.xml`).
- **Content negotiation is fragile:** you need **both** a browser-like User-Agent **and** `Accept: application/json`. Without `Accept` you get HTTP 200 with the HTML SPA shell (~442 KB) — **silently wrong**. With a non-browser UA + Accept you get 403 from CloudFront. **Always verify `content-type`.**
- Useful params: `q`, `page[number]` (0-indexed), `page[size]` (default 50, **max 100**), `date[from]`/`date[to]`, `museum` (`NRM|SMG|NMeM|MSI`), `on_display`, `categories`, `makers`, `people`. JSON:API form `filter[PARAM]` also accepted.
- **`lab.sciencemuseum.org.uk` is DEAD** — Cloudflare Error 1000 "DNS points to prohibited IP". Its 3D blog posts cannot be fetched; the photogrammetry programme is described instead at `https://blog.sciencemuseum.org.uk/photogrammetry-taking-collection-digitisation-to-the-next-level/` (2 Oct 2018).
- SMG's Terms & Conditions page is **last updated 4 August 2020**, and its substantive clauses are JS-collapsed — **UNVERIFIED**.

**Bottom line for SMG:** the *metadata* is a superb, genuinely open research resource (CC0 + CC BY); the *images* are an NC source with a paid commercial route; the *3D* is 33/52 NC and contains nothing relevant. **Use SMG to find and identify objects and to cite archive descriptions; get the imagery from Commons, Smithsonian or Europeana.**

---

### 3.2 Smithsonian Open Access (si.edu/openaccess, api.si.edu, 3d.si.edu)

**Not all of Open Access is CC0 — this is the key correction.** SMG-style programme-level claims do not hold here either.

- **Programme:** "We have released these images and data into the public domain as Creative Commons Zero (CC0)…" But: "If an item is not designated as CC0, it is subject to **usage conditions**." HIGH (FAQ).
- **Metadata vs media — the decisive split, verbatim:** "Portions of metadata are made available for **all** digital images of public domain objects… including a URL to a corresponding image file. Objects in the Smithsonian's collection that may have copyright or other limitations have **portions of metadata with CC0, but no media file is provided** by the Smithsonian due to limitations." HIGH
- **Quantified live** (`/v1.0/stats`): `total_objects: 42,650,469`; `CC0_records: 17,431,244`; `CC0_records_with_CC0_media: 5,255,849`. → ~41% of records have CC0 metadata; **only ~5.26M** have CC0 media. HIGH. **CC0 metadata ≠ CC0 image.**
- **Commercial use, verbatim:** "**May I use Smithsonian Open Access content for commercial use?** Yes, you may use Smithsonian Open Access assets designated as CC0 for commercial purposes **without any attribution, permission, or fee paid** to the Smithsonian." And: "**You may not use any assets with usage conditions for commercial purposes.**" HIGH

**API mechanics.**
- **Key required: YES.** Register at **`https://api.data.gov/signup/`** (`api_key` query param). HIGH. `DEMO_KEY` works for testing.
- Base: `https://api.si.edu/openaccess/api/v1.0/`
- Endpoints: `GET /search?q={query}&api_key={key}` (supports `&fq=` and `&rows=`); `GET /content/{record-url}?api_key={key}`; `GET /stats?api_key={key}`. HIGH (all exercised).
- **Rate limits (MEDIUM, third-party):** `DEMO_KEY` ≈ 30 req/hour; registered key ≈ 1,000 req/hour — api.data.gov's standard default tier. Implement 429 backoff.
- **Bulk (HIGH):** `https://github.com/Smithsonian/OpenAccess` — JSON, "**Data is refreshed at a weekly rate**"; plus an AWS Public Dataset. Exact S3 bucket UNVERIFIED.

**3D (3d.si.edu).**
- Run by the Smithsonian Digitization Program Office; there is a **CC0-filtered view at `https://3d.si.edu/cc0`** — evidence that 3D is *not* uniformly CC0. HIGH
- Download formats: **glTF, glb, obj (150k and full-res), Voyager scenes**. HIGH
- Viewer stack is Smithsonian's own open-source **Voyager** (`https://smithsonian.github.io/dpo-voyager/`), not Sketchfab. HIGH
- **Subject mix is wrong for this channel.** The 3D programme unit reports ~4,200 objects, weighted to cultural/portrait/natural-history/aerospace (the featured example is a Buddha). **No evidence of 19th-century engineering/industrial 3D.** MEDIUM (INFERENCE). **Do not budget time for Smithsonian 3D on Episode 1.**

**What actually exists for Episode 1 (CC0, HIGH — API search):** `Brunel` 843 records · `Thames Tunnel` 40 records · `steam engine` 5,036 records.
Thames Tunnel records include period hand-coloured peepshows: `siris_sil_261561` (1844), `siris_sil_160362` (1840), `siris_sil_160365` (1836), `siris_sil_160364` (1837), `siris_sil_377827` (1838), `siris_sil_285653` (1828, French), `siris_sil_261531` (1851), `siris_sil_246327`, `siris_sil_261583` (1830), `siris_sil_368208` (1840s), and **`nmah_1144472` "broadside, Thames Tunnel"**. Brunel: `siris_sil_4317` "Marc Isambard Brunel", `siris_sil_246163` "The life of Isambard Kingdom Brunel" (1870), `siris_sil_255547` (Rolt 1957).
**TRAP (HIGH, verified):** a record can show `online_media_type: ["Images"]` with **no `media` array and no `media_usage`** — only `metadata_usage.access: "CC0"`. **Always fetch `/content/{url}` and confirm a `media` block with `media_usage` = CC0 before using an image.**

**Other restrictions (HIGH):** the Smithsonian **name and logo are not part of the release** — do not use "Smithsonian"/"SI"/any museum name in the channel name, handle, nickname or display name (a bio mention is fine). Trademarks and third-party rights are not cleared (CC0 §4(c) disclaims them).

---

### 3.3 Scan the World (MyMiniFactory)

**Licence: `CC BY-NC-SA 4.0`** — confirmed verbatim on live object pages (the `BY-NC-SA` label links to `creativecommons.org/licenses/by-nc-sa/4.0/`). HIGH. Not 3.0, not plain BY-SA.

**Two independent blockers, either fatal:**
1. **NC** — non-commercial only; see §4.2.
2. **MyMiniFactory's own Terms of Use, verbatim (HIGH):** "You may print or download portions of the materials from various areas of this website (**including through the use of our API**) **solely for your own non-commercial use**"; "You may not access any content on the website (including, without limitation, 3D print files) **for any other reason except your non-commercial, personal use**." This is a **contract with My Mini Factory Ltd** (51–53 Rivington Street, London, EC2A 3QB; Company No. 09562672; English law) that bites **independently of the CC grant**. MMF reserves the right to modify terms with retroactive effect: "the modified agreement shall apply to existing content uploaded to the website at the time of the modification." HIGH
   
ShareAlike also compounds: any derivative Reel would have to be released under CC BY-NC-SA 4.0.

**Scope — not an engineering source.** STW self-describes as "an archive of fully 3D printable **sculptures, artworks and landmarks**". Its engineering-adjacent holdings are museum *artefacts* (a damaged Stahlhelm from the Imperial War Museum, sundials, landmark architecture) — **no machinery, engines, locomotives, bridges-as-structures, tools, tunnelling equipment, Thames Tunnel or Brunel.** MEDIUM (INFERENCE; the negative could not be exhaustively enumerated because MMF's search is JS-rendered and bot-walled).
**Count conflict (HIGH):** the STW about page claims "25,000+ artefacts freed" while the MMF account profile shows ~12,446 objects. Treat ~12.4k as live.

**Mirror warning (HIGH):** STW's older **Wikimedia Commons** uploads carry plain **CC BY-SA 4.0** (e.g. `File:Scan_the_World_-_Juno_Ludovisi.stl`). So the same scan has *different* licences on different platforms. **The authoritative licence is the one on the page you actually download from.**

**No API or bulk route found.** UNVERIFIED that one exists.

**Verdict: DO NOT USE.**

---

### 3.4 Sketchfab — the most important commercial source

**Ownership: Epic Games sold Sketchfab (and ArtStation) to KitBash.** There is **no "Clara"** — that recollection is wrong.
- Announced **10–12 August 2026** by Epic Games, KitBash and ArtStation. HIGH (Kotaku, 12 Aug 2026; GamesBeat, 10 Aug 2026).
- Buyer: **KitBash** — the company behind **KitBash3D** and **Greyscalegorilla**, operating as **KitBash SF Operations LLC**. HIGH — Sketchfab's own footer now reads "© 2026, KitBash SF Operations LLC", and ToS §4.2.1(b) names "our affiliate, KitBash SF Operations LLC ('KitBash')".
- "**There are no changes to how creators access or use** ArtStation and Sketchfab." HIGH (ArtStation statement, quoted in Kotaku).
- Epic acquired both in **2021** (HIGH).

**Live document contradictions (HIGH — relevant to due diligence):**
- Sketchfab's **License Agreement §1.9 still says**: "'Sketchfab' means Sketchfab Inc. … **Sketchfab is a division of Epic Games, Inc. ('Epic')**." That is now false.
- The **Terms of Use are "Effective August 12, 2026"** — re-issued on the acquisition date — yet §13 still names "Sketchfab, Inc., a Delaware corporation" as the contracting entity. **The public documents are internally inconsistent as at 17 Sep 2026.**

**Retroactive-change risk — explicit, and the reason to keep a licence log (HIGH).**
- ToS §4.1: "You agree that your use of any User Content downloaded from the Services will always be subject to the **most-current version** of the License Agreement or Creative Commons license … any **new version** … as we may update from time to time."
- ToS §4.6: "We reserve the right to remove User Content from the Services and **terminate any licenses thereto**, in whole or in part, without prior notice, for any reason or for no reason at all."
- INFERENCE: for **CC** licences these clauses are arguably ineffective — CC grants are irrevocable, and the CC wiki states platform explanations "never form part of the CC license". But for **Sketchfab's own Store licences** §4.1 is a live retroactive hook. **Archive every download, and screenshot the licence + date.**
- Note carefully: ToS §3.3's prohibition on "commercial exploitation of the Services or **Sketchfab Content**" does **not** restrict commercial use of user-uploaded CC models — §3.1 defines "Sketchfab Content" to **exclude** User Content. HIGH

**The authoritative licence list** — `GET https://api.sketchfab.com/v3/licenses` returns exactly 10. HIGH:

| slug | label | uid | requirements (verbatim) |
|---|---|---|---|
| `by` | CC Attribution | `322a749bcfa841b29dff1e8a1bb74b0b` | "Author must be credited. **Commercial use is allowed.**" |
| `by-sa` | CC Attribution-ShareAlike | `b9ddc40b93e34cdca1fc152f39b9f375` | "Author must be credited. Modified versions must have the same license. Commercial use is allowed." |
| `by-nd` | CC Attribution-NoDerivs | `72360ff1740d419791934298b8b6d270` | "Author must be credited. Modified versions can not be distributed. Commercial use is allowed." |
| `by-nc` | CC Attribution-NonCommercial | `bbfe3f7dbcdd4122b966b85b9786a989` | "Author must be credited. **No commercial use.**" |
| `by-nc-sa` | CC Attribution-NonCommercial-ShareAlike | `2628dbe5140a4e9592126c8df566c0b7` | "Author must be credited. **No commercial use.** Modified versions must have the same license." |
| `by-nc-nd` | CC Attribution-NonCommercial-NoDerivs | `34b725081a6a4184957efaec2cb84ed3` | "Author must be credited. **No commercial use.** Modified versions can not be distributed." |
| `cc0` | CC0 Public Domain | `7c23a1ba438d4306920229c12afcb5f9` | "Credit is not mandatory. **Commercial use is allowed.**" |
| `free-st` | Free Standard | `72eb2b1960364637901eacce19283624` | commercial use permitted, basic restrictions |
| `st` | Standard | `783b685da9bf457d81e829fa283f3567` | commercial use permitted, basic restrictions |
| `ed` | Editorial | `5b54cf13b1a4422ca439696eb152070d` | "Use only in connection with events that are newsworthy or of public interest" |

**Filter mechanics — exact values (HIGH, tested 17 Sep 2026).** The API search param takes the **slug**, not the uid and not a `cc-`-prefixed name:
- ✅ `…/v3/search?type=models&downloadable=true&licenses=cc0&q=engine` → `CC0 Public Domain` results
- ✅ `licenses=by` → `CC Attribution`; `licenses=by-nc-sa` → `CC Attribution-NonCommercial-ShareAlike`
- ❌ `licenses=cc-by` → **HTTP 400**: `{"detail":{"licenses":["Select a valid choice. cc-by is not one of the available choices."]}}`
- ❌ a licence **uid** → HTTP 400
- Both `licenses=` (plural) and `license=` (singular) are accepted and behave identically. HIGH

Website: `features=downloadable` is confirmed from Sketchfab's own navigation markup. The website's `licenses=` param **appears** to take the licence **uid** (`…/search?features=downloadable&licenses=322a749bcfa841b29dff1e8a1bb74b0b`), whereas the API takes the slug — **MEDIUM; the website is a JS shell and could not be read as text. Verify in a browser, or just use the API.**

**Downloadable vs view-only.** `isDownloadable` is a real per-model field, independent of licence. **The only safe query is `downloadable=true&licenses={slug}`** — a CC-BY model that is not downloadable grants you no file. Requesting a non-downloadable model's file returns `400 Bad Request. Model is not downloadable.` HIGH

**Download API (HIGH).**
```
GET https://api.sketchfab.com/v3/models/{UID}/download
Authorization: Bearer {OAUTH_ACCESS_TOKEN}
```
- Returns time-limited signed URLs (`expires: 300`); glTF arrives as a ZIP (`scene.gltf`, `scene.bin`, `textures/`), plus USDZ. **Do not cache the URL.**
- **Authentication is required for CC0 and CC BY alike** — the licence governs what you may *do*, not whether you authenticate. Without auth: `401 {"detail":"Authentication credentials were not provided."}` HIGH (tested).
- **Simplest route for a solo creator:** the **API Token** header form — `Authorization: Token {API_TOKEN}`, token from `https://sketchfab.com/settings/password`. This avoids the OAuth dance entirely for a Python script. HIGH
- OAuth2 (if needed): authorize at `https://sketchfab.com/oauth2/authorize/`, exchange at `POST https://sketchfab.com/oauth2/token/`. **"Access tokens last 1 month."** App registration is **manual** ("contact us"). HIGH
- Data API: `https://api.sketchfab.com/v3/search`; machine-readable spec at **`https://docs.sketchfab.com/data-api/v3/swagger.json`**. Page size defaults to 24 and **is capped at 24** — use cursor pagination. HIGH
- **Rate limits: no numeric quota is published.** The spec names throttling and HTTP 429 only. `https://sketchfab.com/developers/guidelines` is bot-walled (HTTP 202). **Do not invent a number** — implement 429 backoff and contact Sketchfab if a hard figure is needed. UNVERIFIED
- **Attribution (Sketchfab's own wording, updated 5 Aug 2026, HIGH):** *"This work is based on Model 2 by Sketchfab licensed under CC BY 4.0."* And: "If the model author changes the license after you download it, that's ok, but **the license you received it under will always prevail**." CC0 and Standard need no credit.

**Store licences — commercial rights.**
- **Standard / Free Standard:** worldwide, all media, **commercial and non-commercial**, all types of derivative works; **royalty-free** — "Buyers do not need to provide credit or attribution." HIGH
- **Editorial:** "**You may not use them for any commercial or promotional use.**" Cannot suggest sponsorship/affiliation. HIGH → **unusable for this channel.**
- **There is no "Extended" tier.** The three paid/non-CC tiers are Free Standard, Standard, Editorial. HIGH
- Standard-licence restrictions that matter (HIGH §2.2): no stand-alone file distribution; no derivative whose primary value is the asset itself; no incorporation into a logo/name/trademark; **no promoting alcoholic beverages, tobacco, gambling, weapons or explosives** (relevant if an episode covers armaments engineering).
- **Social-media clause (§2.8, HIGH, verbatim):** "If the Licensed Material is used on **any social media platform** … any rights granted by this Agreement to Licensee shall **automatically be revoked** in the event that the third-party website seeks to exploit purported rights to the Licensed Material contrary to the terms of this Agreement, and … upon request, Licensee shall remove any Licensed Material."
- Useful clarification for this channel (HIGH): "Can I use my Sketchfab Store model in a YouTube video I'm making? **Yes, as long as the 3D model is not the only element of the video.**"
- Penalty for unauthorised use: "a fee **equal to up to 25 times** the amounts paid hereunder." HIGH
- Sketchfab **does not warrant the seller's rights** (§1.7, §5). Record the licence yourself.

**Verified real CC0 industrial content (HIGH) — this is the good news for the channel:**
- RG Ross & Sons Steam Hammer — `d80b52dc800e4c76b6b27749bbd8e782`
- VIC 32 Cochran boiler — `884ed11e38054aa48a3db1d9025c881d`, `fb84ddbabd554f7e9b5b2d34b9b47be5`
- QE2 turbine patterns — `8e135c1a917c476a98f011a48c4192c7`, `96d548dfc5d943a8a5cfcc07ebfd1618`
All `CC0 Public Domain`, all by `ScottishMaritimeMuseum`, tagged `industrial-heritage` / `photogrammetry` / `scanningthehorizon`.
Also available under `by` (CC BY, commercially usable with credit): "Brunel Museum Priming Pump" `e54d96c2906a446bb6d1c423bfe29768`, "Glaze Brook Brunel Viaduct" `87b71f9886fe4f01ad84b8e10f91dff0`, "Brunel Model" `6ea474657f944eafb30507e82410bb5f`.

**Also note (HIGH):** Sketchfab now has `is_ai=0` / `is_ai=1` filters (Human Created / AI Generated), and a **NoAI** tag whose terms (ToS §15) prohibit use as input to generative AI programmes.

**NC verdict for this channel: CC BY-NC / NC-SA / NC-ND are NOT usable.** Full reasoning in §4.2.

---

### 3.5 Europeana (europeana.eu)

**API — endpoint, key and the `reusability` facet all verified live (HIGH).**
- Base Search: `https://api.europeana.eu/record/v2/search.json` · Record: `https://api.europeana.eu/record/v2/{ID}.json` · Console: `https://api.europeana.eu/console/search`
- **Key required. Three forms, in order of preference (HIGH):**
  1. **`X-Api-Key: [WSKEY]` header — PREFERRED.**
  2. `?wskey=[WSKEY]` — **DEPRECATED since 2023** (I used it successfully with the demo key, but do not build on it).
  3. `Authorization: Bearer [JWT]` from `https://auth.europeana.eu/...` — restricted to selective customers.
- No key → HTTP 401 `{"success":false,"error":"Unauthorized","message":"Invalid API key provided!","code":"invalid_apikey"}`. Bogus key → `401_key_invalid`.
- **A public demo key `api2demo` works** (HTTP 200) — fine for testing, **not production** (its `requestNumber` is permanently pinned at 999). HIGH
- **Getting a real key (28 May 2025 policy, HIGH):** registration moved into the Europeana website account area — create account → "Manage API keys". **Personal key:** anyone, one active key per account, but **"rate limits for personal keys have been progressively reduced until April 2026."** **Project key:** "significantly higher usage limits", approval by support, 1–5 working days. → **For a production pipeline, apply for a Project key.** Support: api@europeana.eu
- **The `reusability` filter works, with exactly three values: `open`, `permission`, `restricted`** (all three returned data live). This is the most useful parameter for a commercial channel:
  - **`open`** → CC0, Public Domain Mark, CC BY, CC BY-SA
  - **`permission`** → NC licences and similar
  - **`restricted`** → In Copyright and undetermined
- **⚠️ CRITICAL TRAP (HIGH, verified live): an INVALID `reusability` value is SILENTLY IGNORED and returns EVERYTHING.** `reusability=bogus` → HTTP 200 with `totalResults` = the whole corpus (62,662,285). **A typo will hand you In-Copyright records with no warning.** Validate the value client-side and **re-check `edm:rights` on every record.**
- Also verified: `rows` is **capped at 100** (`rows=101` → 100 items, no error); `qf=RIGHTS:"<uri>"` works; `theme=industrial` is a valid theme facet (also `archaeology, art, fashion, manuscript, map, migration, music, nature, newspaper, photography, sport, ww1`).
- **Rights fields per record:** `aggregations[].edmRights.def[]` and `aggregations[].webResources[].webResourceEdmRights.def[]` (also `proxies[].dcRights`). Records ship ready-made **`textAttributionSnippet` / `htmlAttributionSnippet`** — use verbatim.
- **Rate limits: NO NUMBERS ARE PUBLISHED (HIGH).** The Fair Use policy is purely qualitative: *"Use of the API must be limited to a reasonable number of concurrent requests… failure to comply… may result in your access key be temporarily blocked or even revoked."* Documented codes: 200 / 401 / **429** ("reached its usage limit") / 500. **Do not state a daily figure.**
- **Bulk (HIGH):** FTP `ftp://download.europeana.eu/dataset/` — user `anonymous`, blank password, port 21; subdirs `XML` (RDF-XML) and `TTL` (Turtle); one ZIP per dataset with `.md5sum`; **regenerated weekly, Sunday evening**. `wget -m ftp://download.europeana.eu/dataset/XML`. OAI-PMH for incremental. Find a record's dataset via the `edm_datasetName` facet.
- **Europeana's own METADATA is CC0 (HIGH, verbatim):** *"All metadata from Europeana's APIs are provided as CC0, meaning you can reuse that metadata as you wish without any restrictions. Some of that metadata may link to content from Europeana's partners… These objects can be used in accordance with the Rights Statement mentioned in the object metadata, in the europeana:rights/edm:rights field. Always check these fields before using the objects!"*

**Worked example — `query="Thames Tunnel"` returns 24 records: 9 open / 4 permission / 11 restricted.** Rights URIs actually present: `publicdomain/mark/1.0/` (5), `rightsstatements.org/vocab/InC/1.0/` (4), `licenses/by-nc-nd/4.0/` (4), `licenses/by-nc-sa/4.0/` (3), `licenses/by/4.0/` (3), `rightsstatements.org/vocab/NoC-NC/1.0/` (1). HIGH
**The one commercially usable Thames Tunnel asset found in either source:** *"Der Themse-Tunnel / The Thames tunnel"* — **Public Domain Mark**, City Museum Berlin (Stiftung Stadtmuseum Berlin): `https://www.europeana.eu/item/736/item_6C4HHEPIENLL7RFGCYVBFM6JNY4USSDZ` (rights confirmed at both aggregation and webResource level; 1000px JPEG at sammlung-online.stadtmuseum.de; IIIF manifest at `iiif.europeana.eu/presentation/736/…`).
Other Thames Tunnel records and why they fail: "Thames Tunnel paper" (National Library of Scotland, **NoC-NC**), "The Thames tunnel" (Bodleian Libraries Oxford, **InC**), "Messingmedaille 1846" (Vienna Museum of Science and Technology, **CC BY-NC-ND**), "A perspective view of the Thames and the Thames Tunnel" and "Counter commemorating the Thames tunnel" (Royal Museums Greenwich, **CC BY-NC-SA**).
Contributors to the Thames Tunnel set: **Bodleian Libraries (Oxford), National Library of Scotland, Vienna Museum of Science and Technology, Royal Museums Greenwich, City Museum Berlin.**
**Note:** `q=brunel` in Europeana is polluted by the botanist Brunel (*Phyllanthus* spp.) and a Portuguese tailor — **effectively useless for this episode.**

**The rights vocabulary — Europeana accepts only 6 of the 12 RightsStatements.org statements.** This is an important correction. Per Europeana's own "Accepted rights statements and URIs" (v36, 18 Aug 2026), data providers may choose between **14** standardised statements: **6 Creative Commons licences + 2 CC public-domain tools + 6 of the 12 RightsStatements**. HIGH

*The 6 CC licences accepted:* CC BY · CC BY-SA · CC BY-ND · CC BY-NC · CC BY-NC-SA · CC BY-NC-ND (`creativecommons.org/licenses/{props}/{version}/{port}/`; 1.0–4.0 accepted, 4.0 recommended).
*The 2 CC public-domain tools:* **CC0** (`publicdomain/zero/1.0/` — waives all rights) and **PDM** (`publicdomain/mark/1.0/` — no longer protected worldwide).
*The 6 RightsStatements Europeana accepts:* **NoC-NC**, **NoC-OKLR**, **InC**, **InC-EDU**, **InC-OW-EU**, **CNE**.
**NOT accepted by Europeana: `InC-RUU`, `InC-NC`, `NoC-CR`, `NoC-US`, `UND`, `NKC`.** HIGH

*Europeana's PDM-vs-CC0 distinction (HIGH):* **PDM = no copyright exists (worldwide); CC0 = copyright exists (or may exist, including in the digitisation) and the rightsholder actively waives it.** Operationally both are unrestricted.

The full RightsStatements.org vocabulary is 12 statements (URIs verified live; HTTP 303 = resolvable) — but only the 6 above appear in Europeana:
- *In Copyright:* `InC`, `InC-OW-EU`, `InC-EDU`, `InC-NC`, `InC-RUU`
- *No Copyright:* `NoC-CR`, `NoC-NC`, `NoC-OKLR`, `NoC-US`
- *Other:* `CNE`, `UND`, `NKC`
All at `http://rightsstatements.org/vocab/{ID}/1.0/`.

**NKC 1.0 is a disclaimer, not a licence** (verbatim, HIGH): *"The organization that has made the Item available **reasonably believes** that the Item is not restricted by copyright or related rights, **but a conclusive determination could not be made**… It is **not a License, and should not be used to license your Work**." → **unusable for a monetised channel.**

**2026 governance change (HIGH).** On **1 April 2026**, **Digital Scholar** (Zotero, Omeka, Tropy) assumed stewardship of RightsStatements.org from an Interim Steering Committee. 16 languages; implemented by Europeana, DPLA and the Common European Data Space for Cultural Heritage. The vocabulary is unchanged.

**Live corpus scale — the commercial-safe pool is about half (HIGH, facet query `query=*:*`, total 62,662,285):**
| Rights | Count |
|---|---|
| InC | 11,656,827 |
| PDM | 10,920,833 |
| CC0 | 8,032,410 |
| CC BY 4.0 | 7,614,678 |
| CC BY-NC-ND 4.0 | 3,644,732 |
| NoC-OKLR | 3,336,449 |
| CC BY-SA 4.0 | 3,104,200 |
| CC BY-NC-SA 4.0 | 3,030,510 |
| NoC-NC | 2,789,586 |
| CC BY 3.0 | 1,763,694 |
| InC-EDU | 1,722,117 |
| CC BY-SA 3.0 | 1,553,900 |
| CC BY-NC 4.0 | 1,120,689 |
| CNE | 362,761 |
**→ Commercial-safe (PDM + CC0 + CC BY + CC BY-SA) ≈ 31.7M, ≈ 51% of the corpus.** HIGH

**EUROPEANA DOES NOT HOST 3D FILES — a correction to a common assumption.** Verbatim from Europeana's "Publishing guide for 3D content": *"Can Europeana host 3D files? — **No.** Some national aggregators have solutions if you are unable to host content yourself."* HIGH
- **There is no "Europeana 3D viewer" and no 3D Hop anywhere.** Europeana **embeds third-party viewers by oEmbed**. Supported URL patterns (verbatim): `sketchfab.com/3d-models/*`, `sketchfab.com/models/*`, `sketchfab.com/show/*`, `weave-3dviewer.com/asset/*`. EDM guidelines (v40, 8 May 2026) additionally show a "Eureka3D Viewer", and live records now use `https://3d.repox.io/api/oembed?url=…` — the supported set has grown.
- EDM: `edm:type='3D'`; `dc:type` from `data.europeana.eu/vocabulary/modelType/{3DMesh|3DPointCloud|BIM|parametricModel|3DGaussianSplatting}`. Formats seen: DAE, PLY, WRL, GLTF, OBJ, STL, NXS, DICOM, IFC, USDZ. *"For 3D records, 3D PDF files are not sufficient."*
- **Downloadability is the provider's choice, not Europeana's.** Europeana advises reusers *"need to be able to download the 3D files… shape files, textures, metadata and paradata."* So: **check `edm:rights`, then check the host** (Sketchfab `isDownloadable`, Zenodo, the aggregator).
- **Live 3D scale (HIGH): `qf=TYPE:"3D"` → 13,474 records; `+reusability=open` → 4,904.** 3D rights breakdown: CC BY 4.0 3,072 · CC BY-NC 4.0 2,465 · CC BY-NC-ND 4.0 2,004 · CC BY-NC-SA 4.0 1,149 · InC 1,116 · CC BY-NC-ND 3.0 979 · CC BY-SA 4.0 808 · InC-EDU 760 · **CC0 639** · **PDM 385** · NoC-NC 47 · CC BY-ND 4.0 42 · CNE 3 · InC-OW-EU 3 · NoC-OKLR 2 → **commercially safe 3D ≈ 4,906** (and it is overwhelmingly CC BY rather than CC0).
- Example open 3D records: `3D Model of the Vendel XIV Helmet` (Swedish History Museum, CC BY 4.0, Sketchfab oEmbed); `Valentino Castle (Turin)` (Polytechnic University of Turin via CARARE, CC BY 4.0, direct `.glb` on Zenodo); `/2048707/A_0_9_10739_3D` (Polytechnic University of Milan, **CC0**); `Pashley Sarcophagus` (Fitzwilliam, CC BY 4.0).
- **"Europeana Sculpture pilot" is UNVERIFIED — no evidence found** in the Europeana Knowledge Base, PRO, or web search. INFERENCE: likely a conflation with **"Twin it! 3D for Europe's culture"** (Parts I–II), **EUreka3D**, Share3D, CARARE or 3D-ICONS.

**The Europeana Publishing Framework — the tier that matters.** There are two parallel ladders: CONTENT tiers 1–4 and METADATA tiers A–C. Verbatim:
- **CONTENT 3** = *"as a distribution platform for **NON-COMMERCIAL** reuse… Your collections could be used in non-commercial websites, apps, and services."*
- **CONTENT 4** = *"as a free reuse platform… Your collections could be used in **commercial and non-commercial** websites, apps, services, and products."* **3D rights allowed at Tier 4: PDM, CC0, CC BY, CC BY-SA ONLY.** HIGH
→ For a downstream reuser the whole Framework reduces to: **`edm:rights` ∈ {PDM, CC0, CC BY, CC BY-SA}** for any commercial use. Metadata tier is orthogonal — the rights statement gates commerce.

**Engineering/industrial content — confirmed, live (HIGH).** With `reusability=open`:
| Query (`theme=industrial`) | Results | Example |
|---|---|---|
| `steam engine` | 190 | "Steam Engine Brewery" · PDM · European Heritage Awards Archive |
| `bridge` | 4,373 | "Brooklyn Bridge" · PDM · Deutsche Fotothek; "Eisenbahnbrücke / Railway bridge" · CC BY-SA 4.0 |
| `dock OR harbour` | 2,226 | "Harbour mill" · CC BY-SA 4.0 · Deutsche Fotothek |
| `colliery OR mine` | 5,477 | "Pemberton Main Colliery" · CC BY-SA 4.0 · Newcastle University |
| `railway OR locomotive` | 15,061 | "Järnväg / Railway" · PDM · Jamtli |
| `tunnel` | 278 | "Der Themse-Tunnel" · PDM · City Museum Berlin |
→ **Europeana is a genuine, substantial source of openly licensed industrial-engineering imagery** — far stronger for this channel than Rijksmuseum.

---

### 3.6 Internet Archive (archive.org)

**US public-domain cut-off at 17 Sep 2026 — CONFIRMED (HIGH).** Multiple authoritative sources agree:
- Internet Archive, verbatim: *"On January 1, 2026, **creative works from 1930 and sound recordings from 1925** entered the public domain in the United States."*
- Library of Congress, verbatim: *"**Works published or registered in the U.S. more than 95 years ago are now in the public domain.**"*
- BYU, verbatim: *"all works published in 1930 or earlier are in the public domain in the United States. On January 1, 2027, works published in 1931 will enter the public domain."*

→ **1930 or earlier = PD. 1931 → 1 Jan 2027. 1932 → 1 Jan 2028.** (95 years, 17 U.S.C. §304(b) arithmetic.)
**Two traps:** (i) pre-1964 works are PD **only if not renewed** — a work renewed in 1961 is protected to 1 Jan 2057; (ii) 1964–1977 works are generally protected for 95 years.
**Thames Tunnel material (1825–1843) is categorically PD and raises no renewal question.** HIGH

**Three different things, routinely confused (HIGH, legally the crux):**
1. **IA's own scans of public-domain books** — PD. Safe. IA states its scans of PD works carry no additional rights (this is the `publicdate`/PD-collection material).
2. **Uploader / Community content** (Community Texts, Community Uploads) — **the uploader self-declares the rights status and IA does not verify it.** A "Public Domain" label on an uploaded item is an assertion by an anonymous user, not a rights determination. Frequently wrong.
3. **Borrowable / lending-library books** (Controlled Digital Lending) — **in copyright.** You may borrow and read; you may **not** reuse, reproduce or include footage/stills in a monetised video. The 2023–2025 litigation over CDL makes this the most contested part of the IA corpus. **Do not touch lending items for production.**

**"No known copyright restrictions" ≠ public domain.** It is a statement of the uploader's *belief*. See the NKC 1.0 text in §3.5 — it is expressly not a licence.

**APIs (HIGH — all exercised live).**
- Search: `https://archive.org/advancedsearch.php?q={query}&fl[]=identifier&fl[]=title&fl[]=licenseurl&fl[]=collection&rows=50&page=1&output=json`
- Metadata: `https://archive.org/metadata/{identifier}` (gives `metadata.licenseurl`, `metadata.rights`, `metadata.possible-copyright-status`, `metadata.collection`, `metadata.uploader`)
- Files: `https://archive.org/download/{identifier}/{filename}`
- Scrape API (bulk): `https://archive.org/services/search/v1/scrape?q={query}&fields=identifier,title,licenseurl`
- Worked example: `q=Thames Tunnel` → **121 items**. The `licenseurl` field is present for only some items — e.g. a Community upload carried `http://creativecommons.org/publicdomain/mark/1.0/`, while IA-hosted scans of library books carried **no `licenseurl` at all**. HIGH
- **Practical filter for PD:** there is no single reliable "public domain only" switch. Check **`collection` membership** (PD/`texts` collections), the **`licenseurl`** field, and the **`rights`**/**`possible-copyright-status`** fields together. **A missing `licenseurl` is not evidence of public domain** — it usually just means IA has not tagged it. MEDIUM
- 3D: the Internet Archive hosts some 3D model collections (including Thingiverse mirrors). Downloads are per-item and licences vary wildly; many are mislabelled. **REQUIRES A DECISION → treat as unusable.**

**THE EPISODE-1 HERO ITEM — a 1837 volume containing sectional drawings of the shield (HIGH).**
`https://archive.org/metadata/explicationdestr00unse` — a **1837** French volume on the Thames Tunnel. `sponsor` / `contributor` = **Getty Research Institute**. The item description, verbatim: *"Describes the tunnel begun by Brunel in 1825 and completed in 1843, **with sectional drawings of the tunneling shield**."* **Public domain by date (1837).** Verify the Getty Research Collections record for an explicit CC0 download button.
**Plus four IA pamphlets, all `possible-copyright-status = NOT_IN_COPYRIGHT` and directly on topic (HIGH):**
| Identifier | Year | Note |
|---|---|---|
| `thamestunnelade00tunngoog` | 1825 | |
| `originprogressa00westgoog` | 1827 | |
| `sketchesworksfo00cruigoog` | 1829 | Cruikshank |
| `anexplanationwo00compgoog` | 1840 | Thames Tunnel Company |
Downloads verified HTTP 200 for both **`_jp2.zip`** (high-resolution page images) and PDF.

**⚠️ THE FAILURE MODE, IN THE WILD — the David Rumsey Thames Tunnel plate.** `dr_view-plate-1-construction-of-roads-thames-tunnel-12190612` is an on-topic **1851** Thames Tunnel engraving whose **scan** carries, verbatim: *"Creative Commons **CC BY-NC-SA 3.0** … **Please contact the David Rumsey Map Collection for commercial use**."* **The underlying print is public domain; the scan is expressly non-commercial.** This is precisely the three-tier distinction of §4.4, and it is a live, on-topic trap for this very episode. HIGH

**The working PD filter — and the one that does not work (HIGH).**
- ✅ **`possible-copyright-status:NOT_IN_COPYRIGHT`** — this returned exactly the four pamaphlets above.
- ❌ **`collection:pub_*` does NOT work** as a PD filter — a test surfaced only in-copyright lending items.
- A missing `licenseurl` is **not** evidence of public domain — it usually just means IA has not tagged it.

**Uploader content — IA's own schema confirms the risk (HIGH).** For uploader items, `rights`, `licenseurl` and `possible-copyright-status` are all **"defined by: uploader"** — **free text, and `required: No`.** So an absent rights field proves nothing, and a present one is an anonymous user's assertion. This is the documentary basis for treating IA uploader content as unusable.

**Controlled Digital Lending — do not touch (HIGH).** Items in the `internetarchivebooks`, `printdisabled` or `inlibrary` collections are lending-library copies. **Lending ≠ licensing.** Example: a 1970 Brunel biography (`isambardkingdomb0000rolt_d0g4`) is in copyright and borrow-only.

**Thingiverse 3D mirror (~2.6M items) — licence distribution (HIGH):** 1.32M CC BY · 604k BY-SA 3.0 · 299k BY-NC · 266k BY-NC-SA · **38k CC0** · **1,732 unlicensed**. Only **CC0 and CC BY** are usable for a monetised channel; NC bars the ad revenue, and SA sits badly against Instagram's terms. **No Thames Tunnel or Brunel 3D geometry exists there.** → **REQUIRES A DECISION → treat as unusable.**

**Operational rules (HIGH).**
- IA **requires** a descriptive `User-Agent` identifying the tool/version (and the model, if an AI agent). No numeric rate limit is documented; honour `429` / `Retry-After`, use ~4 concurrent connections with ~1 s delay, and cache responses.
- **Hard limit: `advancedsearch.php` returns sorted paged results only to the 10,000th result.** Use the cursor-based **Scrape API** for deeper paging.
- **Never hotlink** `ia######.us.archive-assets.org` file URLs — IA's documentation says **"DO NOT LINK"**. Download and re-host.

**Verdict:** IA is genuinely excellent for **pre-1930 books** and is the source of the single best Episode 1 asset (the 1837 shield-section volume). It is a **liability** for uploader content, lending items and mislabelled scans, and `licenseurl` is too sparsely populated to filter on.

---

### 3.7 Library of Congress (loc.gov)

*loc.gov was bot-blocked (HTTP 403) for direct fetch during this session; the findings below are MEDIUM unless noted and must be verified in a browser.*

**JSON API (MEDIUM — endpoint shapes are long-standing and stable).**
- `https://www.loc.gov/search/?q={query}&fo=json`
- `https://www.loc.gov/item/{id}/?fo=json`
- `https://www.loc.gov/collections/{slug}/?fo=json`
- Prints & Photographs: `https://www.loc.gov/pictures/`
- **No API key.** Rate limits: LoC asks that automated requests be limited and identifies bots; a `User-Agent` with contact details is expected. UNVERIFIED exact ceiling.

**HABS / HAER / HALS — the strongest asset class in this whole report, and confirmed public domain.**
- **NPS, verbatim (nps.gov, updated 12 August 2026, HIGH):** *"**Materials created for HABS, HAER, or HALS are in the public domain.**"* Over **46,000 sites** documented, with measured drawings plus large-format photographs.
- **LOC wording, verbatim (HIGH):** *"The original measured drawings and **most** of the photographs and data pages in HABS/HAER/HALS were created for the U.S. Government and are considered to be in the public domain."* → **the word "most" means per-item verification is still required for photographs and data pages.** Measured drawings are the safest.
- Confirmed HAER subject coverage includes **bridges, dams and blast furnaces** — e.g. Arlington Memorial Bridge (HAER DC-7), Rock Point Arch Bridge (HAER OR-29), U.S. Steel Duquesne Works (HAER PA-115-A).
- Browse: `https://www.loc.gov/pictures/collection/hh/`. High-resolution TIFFs downloadable.
- **Caveat: HAER documentation is overwhelmingly AMERICAN engineering** — excellent for later episodes (bridges, docks, railways, industrial buildings), not for Episode 1.

**⚠️ A reachability finding that matters operationally: `www.loc.gov` is hard-blocked (403 Cloudflare) — HTML *and* `?fo=json` — and `chroniclingamerica.loc.gov` likewise.** HIGH (observed from two independent sandboxes). **So the `fo=json` endpoint signatures are UNVERIFIED.**
**Working alternatives that ARE reachable (HIGH):**
- **`https://lccn.loc.gov/{lccn}/mods`** and **`/marcxml`** — expose the verbatim **`<accessCondition>`** rights string for an item. **This is the reliable programmatic route to LoC rights.** Example: the LoC Thames Tunnel lithograph `https://lccn.loc.gov/98507755/mods` → `"No known restrictions on publication."`
- **`tile.loc.gov`** serves full-resolution IIIF.
- Also reachable: `guides.loc.gov`, `data.labs.loc.gov`, `nps.gov`, `libraryofcongress.github.io`, `id.loc.gov`.

**"No known restrictions on publication" is NOT public domain — LoC says so expressly (HIGH, verbatim):** *"**These facts do not mean the image is in the public domain**, but do indicate that no evidence has been found to show that restrictions apply."* That is precisely the same posture as Flickr Commons' NKC and RightsStatements.org's NKC 1.0 — **a diligence statement, not a licence.**

**"Free to Use and Reuse" — the disclaimer is a THREE-WAY DISJUNCTION, and the third branch is the problem (HIGH, verbatim):** *"The Library believes that this content is **either in the public domain, has no known copyright, or has been cleared by the copyright owner for public use**."*
**The third branch is an unstated third-party grant** — LoC is telling you a rights-holder cleared it, without identifying the rights-holder or the scope. 2,610 items; dataset last updated 17 April 2024. **No engineering theme is among the named sets.**
**Also (HIGH):** LoC does not grant permission — *"We cannot sign permission forms."*

**Rights statements and what they mean.**
- *"No known restrictions on publication"* — see above. **Not PD. Not a licence.**
- *"Public Domain"* — safe.
- *"Rights status not evaluated"* / *"Publication may be restricted"* / no rights note — **unusable without your own evaluation.**
- Always read the item's `<accessCondition type="use and reproduction">` via the MODS route above.

**HABS / HAER / HALS — the strongest LoC finding for this channel.** The Historic American Buildings Survey, **Historic American Engineering Record**, and Historic American Landscapes Survey produce **measured drawings, large-format photographs and written histories**. These are **US federal government works and are in the public domain** (17 U.S.C. §105), and **HAER covers exactly this channel's subject matter**: bridges, dams, factories, railways, canals, harbours, industrial structures.
- Browse: `https://www.loc.gov/pictures/collection/hh/`
- High-resolution TIFFs are downloadable.
- **Caveat:** HAER documentation is predominantly 20th-century structures (the programme began in 1933; HAER in 1969). It will serve later episodes (bridges, docks, railways, steam-era industrial buildings) far better than a strictly 1825–1843 Thames Tunnel episode. MEDIUM

**Chronicling America** (`https://chroniclingamerica.loc.gov/`) — digitised US newspapers with an API; the underlying newspapers are PD (pre-1964, no renewal / pre-1930). Useful for period reporting but not for 3D.

**Other LoC holdings relevant here:** the **Institution of Civil Engineers** material is a UK body, not LoC — but LoC holds substantial 19th-century engineering photography and technical drawings in Prints & Photographs and the Geography & Map Division. **UNVERIFIED for specific Brunel/Thames Tunnel items** (403).

---

### 3.8 Rijksmuseum (rijksmuseum.nl / Rijksstudio)

**⚠️ MAJOR CORRECTION: the legacy keyed API is DEAD. `https://www.rijksmuseum.nl/api/en/collection?key=…` returns HTTP 410 Gone (permanently removed).** Any guidance you find about "get a Rijksmuseum API key, ~10,000 requests/day" is **stale** — that quota belonged to the retired API. HIGH

**The replacement is keyless Linked Art: `https://data.rijksmuseum.nl/search/collection`.** HIGH
- **There is NO `q` parameter.** `?q=windmill` → HTTP 400 `{"detail":"Unsupported query parameter: q"}`. Use instead: `description=`, `creator=`, `objectNumber=`, `imageAvailable=`, `creationDate=`, `pageToken=`.
- Scale: **840,004 objects; 735,982 with images; 64,555 19th-century with images.** HIGH
- IIIF `full/max` is permitted (verified HTTP 200). Full-resolution masters are downloadable.
- **OAI-PMH at `https://data.rijksmuseum.nl/oai`** — no key required. **A June 2026 OAI-PMH update introduced breaking changes for XML parsers** — expect to update your client. HIGH

**The CC0 question — resolved, and machine-verifiable.** Every object carries:
`subject_of → subject_to: { type: "Right", classified_as: [{ id: "https://creativecommons.org/publicdomain/zero/1.0/" }] }`
→ **CC0, not a bare Public Domain Mark.** Confirmed on 6/6 objects sampled, including directly relevant engineering items: **`NG-MC-28` (dredger model, c.1800)**, **`NG-MC-528` (1855 trunk steam engine)**, `SK-C-211`, `RP-P-1908-4837` (railway station). HIGH
*Note:* the museum's own prose describes the **metadata as CC0** and the **images as "in the Public Domain"** — but the machine-readable rights mark is CC0 on the object. Either way it is **commercially free**. The currently correct, machine-checkable statement is **CC0**.

**⚠️ TRAP: the IIIF manifest does NOT carry the licence.** `license`, `requiredStatement` and `rights` are all **null** on the manifest (e.g. `https://iiif.micr.io/RFwqO/manifest`). **Assert CC0 from `GET https://data.rijksmuseum.nl/{id}` — never from the manifest.** HIGH

**19th-century engineering content.** Dutch hydraulic, maritime and steam material: `polder` 96 · `stoommachine` 41 · `spoorweg` (railway) 103 · `brug` (bridge) 3,287. **Not** the Thames Tunnel. Leads worth running: `description=Brunel` (2 items), `description=Thames` (31 items) — **UNVERIFIED whether those hits are on-topic.**
**Verdict: a genuinely SAFE, machine-verifiable CC0 source, strong for Dutch civil-engineering episodes (polders, canals, dredging, steam) and low-yield for British tunnelling.**

---

### 3.9 Getty

**Getty Open Content Program — CC0, verified (HIGH).** From the Getty Open Content Program FAQs (retrieved via the Wayback Machine; getty.edu is Cloudflare-walled to direct automation), verbatim:
> *"Images in the Open Content Program are images of works in the public domain in the United States. The works depicted in the images are not protected by copyright, but **Getty may have a copyright interest in the digital image of the work. To the extent that Getty owns copyright in the digital images, we have chosen to make the images freely available under CC0.** However, some images may include people or objects for which a third party may claim rights (e.g., trademark, copyright, privacy, or publicity rights). **Getty does not guarantee that all of its Open Content images are free from rights claimed by third parties. As the user, it is your responsibility to do that research.**"*
> *"Getty places no restriction…"* [on uses and alterations — the sentence continues past the retrieved excerpt]

**Two things to take from this (HIGH):**
1. **The CC0 dedication is Getty's own choice, not a statement that no copyright could exist** — *"Getty may have a copyright interest in the digital image of the work."* That is precisely the "wrapper" posture discussed in §4.4, but resolved **in your favour**: Getty has waived it.
2. **Getty expressly does not clear third-party rights** (trademark, privacy, publicity, and third-party copyright), and puts that research on you. So an Open Content image can be CC0 *and* still carry an uncleared personality or trademark issue — relevant if a photograph includes identifiable people.

**Distinguish the two Getty postures:** Getty's own FAQ language here is **CC0**. The GRI's separate "Open Content" framing and other Getty material may be described as **"no known copyright restrictions"** — which, per §3.5, is a disclaimer and **not** a licence. **Check which one the specific item carries.**

**APIs and IIIF — verified working.**
- **Search API (works, keyless): `https://www.getty.edu/art/collection/api/search?q={query}&size=100`** — returns per-item **`manifest.license`**, so the licence is **machine-readable per item**. HIGH
- A 100-row railway pull returned **81 CC0**, 4 InC, 4 UND, 1 InC-RUU. → Getty is a genuinely CC0-dominant source.
- IIIF manifest `rights` = `"http://creativecommons.org/publicdomain/zero/1.0/"`. Full masters are downloadable (`full/max` = `full/full`; e.g. 14.2 MB, 13301×4158) on **`media.getty.edu`**.
- **⚠️ `iiif.getty.edu` is UNREACHABLE (HTTP 000). Use `media.getty.edu`.** HIGH
- Getty's object-level REST signature: **404 on all attempts — UNVERIFIED.** Use the search API plus `manifest.url`.
- Rate limits, bulk dump and API-key documentation: **UNVERIFIED**.

**Actual CC0 engineering items found (HIGH) — directly useful for this channel:**
- **Manchester Ship Canal construction, 1894**
- **Gotthardbahn bridge under construction, c.1875–82**
- [Bridge under construction], 1855–60
- New Bridge over the Potomac, 1864
- The Great Exhibition, 1852
→ **This is the strongest openly licensed pool of 19th-century *engineering construction* photography found in any source surveyed.**

**Obligations (HIGH):** credit **"Digital image courtesy of Getty's Open Content Program"**; no implied endorsement. **And a trap: Getty's catalogue TEXT is CC BY 4.0 while the IMAGES are CC0** — two different licences on the same page, easily missed.

**⚠️ Terms-of-use tension — FLAG FOR LEGAL REVIEW IF THE CHANNEL SCALES (HIGH).** Getty's **general Terms of Use state that commercial use is prohibited**, while the **Open Content clause expressly permits commercial use of OCP images**. The Open Content clause should carve OCP images out of the general prohibition — that is plainly its purpose — but the two statements sit on the same site and have not been reconciled in a document I could verify. **This is the one Getty point I would put in front of a lawyer before relying on Getty at scale.**

**19th-century engineering photography — confirmed strong.** Getty's holdings include 19th-century British photography and industrial/engineering subjects, and the GRI is the likely home for more. **Only Getty "Thames Tunnel" hit is IN COPYRIGHT** (a 1930s toy photograph, `10431B`) — so **Getty is not an Episode 1 source, but is excellent for later episodes (bridges, canals, railways, the Great Exhibition).**

**Verdict: a legitimate, machine-verifiable CC0 source with the best engineering-construction photography pool found; subject to an explicit third-party-rights caveat, a text-vs-image licence split, and a ToU tension worth a legal opinion before scaling.**

---

### 3.10 Wikimedia Commons — the single best source for this channel

**THE HEADLINE FINDING: non-commercial licences are not permitted on Commons at all.** `{{Cc-by-nc-4.0}}` **redirects to `Template:Noncommercial`**, which is a **speedy-delete / copyright-violation tag**: *"This file is ONLY published under a license that does not allow unrestricted commercial use… files must be published under at least one license which permits unrestricted commercial use. The file will be deleted without notice unless it is relicensed."* HIGH (template wikitext fetched).

→ **Therefore every file that survives on Commons is, by policy, commercially reusable.** Commons is the one major source where you do **not** have to run the NC analysis at all. The only remaining decision is **ShareAlike**. This is a structural advantage over SMG, Scan the World, Flickr Commons and Europeana.

**Per-file licensing.** Every file carries its own licence template; there is no site-wide licence. Site footer (verbatim): *"Files are available under licenses specified on their description page. All structured data from the file namespace is available under the Creative Commons CC0 License; all unstructured text is available under the Creative Commons Attribution-ShareAlike License."* HIGH

**The templates that matter here (exact displayed wording verified, HIGH):**

| Template | Effect | Commercial? |
|---|---|---|
| `{{PD-old-100}}` | "public domain in its country of origin and other countries… where the copyright term is the author's life plus 100 years or fewer." Directly applicable: **Brunel died 1849** | ✅ |
| `{{PD-old-70}}` / `{{PD-old}}` | life + 70 (EU standard) | ✅ |
| `{{PD-US-expired}}` (and its alias `{{PD-1923}}`, a redirect) | "for works published before **1 January 1931**" (as of 2026) | ✅ |
| `{{PD-scan}}` | "a mere mechanical scan or photocopy of a public domain original, or … so similar to such a scan or photocopy that no copyright protection can be expected to arise" | ✅ |
| `{{PD-Art}}` | faithful reproduction of a **2D** PD work — see below | ✅ (US) |
| `{{Cc-zero}}` / CC0 | "Creative Commons Zero, Public Domain Dedication"; attribution not required | ✅ |
| `{{Cc-by-4.0}}` | attribution required | ✅ |
| `{{Cc-by-sa-4.0}}` | derivatives must carry the same licence | ⚠️ viral |
| `{{Cc-by-nc-4.0}}` | **delete tag — not a valid Commons licence** | 🚫 |

**PD-Art — the nuance, and the 2D/3D line.** Commons policy (`Commons:When_to_use_the_PD-Art_tag`) states the WMF position: *"faithful reproductions of two-dimensional public domain works of art are public domain"* and, per WMF General Counsel, *"claims to the contrary represent an assault on the very concept of a public domain."* It cites *Bridgeman*. Critically:
- **PD-Art applies ONLY to 2D works. "2D is OK, 3D is not."** It does **not** cover photographs of sculptures, coins or other 3D objects — for those you need the *photograph itself* to be old enough for a PD-old tag. HIGH
- Commons grants a **"rare exception"** to its own rule that images must be free in the source country as well as the US. The template itself warns: *"In other jurisdictions, re-use of this content may be restricted."*

**Country-by-country reuse position (HIGH — from `Commons:Reuse_of_PD-Art_photographs`, fetched live):**
- **UK: OK.** *"a November 2023 Appeal Court judgement (THJ v Sheridan, 2023) clarified that, in the UK, no new copyright is created in making a photographic reproduction of a public domain artwork, and that this has been the case since 2009."* Also: *"there is also no issue regarding raw unenhanced scans or photocopies of PD illustrations in an old book. These are always OK, as purely mechanical copying has never been capable of creating a new copyright."*
- **Germany: OK "in most cases"** — s.68 UrhG: simple photographs of PD visual art are not protected.
- **Spain:** mere photographs get 25 years from 1 January following creation → OK before 2001, **not OK otherwise**.
- **Nordic countries: generally NOT OK** — a special simple-photograph neighbouring right, 50 years from creation.
- **Australia / Belgium / Canada / France / Turkey:** "Inconclusive".

**→ For a UK-based channel covering British engineering, the UK position is permissive and this is a major de-risking.** See §4.4.4.

**THE ACTUAL EPISODE 1 MATERIAL — Commons files verified live (HIGH).** This is the best available source of period Thames Tunnel imagery, and it is all PD:
- `File:Penny_Magazine_1832_341_Shield_used_in_the_Excavation_of_the_Thames_Tunnel.jpg` — **1832 woodcut of the shield, 1400×840**; `{{PD-scan|PD-old-100-expired}}`. **The single best historical image of the shield.**
- `File:Thames_tunnel_shield.png` — 787×542 diagram; `{{PD-Art|PD-anon-expired}}`
- `File:Penny_Magazine_1832_340_Longitudinal_Section_of_the_Tunnel.jpg` — 1750×370 section drawing
- `File:Penny_Magazine_1832_258_Thames_Tunnel.jpg` — 1659×1007
- `File:The_Thames_Tunnel_LCCN98507755.jpg` — LoC lithograph, **6736×5248** (also .tif), "No known restrictions on publication"
- `File:Thames_tunnel_construction_1830.jpg` — 400×421
- `File:Thames_Tunnel,_1827,_Museum_of_history_and_Technology.png` — 1369×1494, `{{cc-zero}}`
- `File:Illustrirte_Zeitung_(1843)_01_006_3_Sir_I_Brunel_wie_er_bei_der_Eröffnungsfeier_den_Tunnel_durchschritt.PNG` — 1843 opening ceremony
- `File:Sir_Marc_Isambard_Brunel_by_James_Northcote.jpg` — 2400×3025 portrait (Northcote d. 1831), PD
- `File:Robert_Howlett_(Isambard_Kingdom_Brunel_Standing_Before_the_Launching_Chains_of_the_Great_Eastern),_The_Metropolitan_Museum_of_Art.jpg` — 5616×7334 (Howlett d. 1858), PD
- `File:Medaille_met_portret_van_Marc_Isambard_Brunel,_RP-P-1910-4751.jpg` — Rijksmuseum, **CC0**
- `File:Network_Rail_Virtual_Archive_Box_Tunnel.jpg` — 1838 GWR Box Tunnel engineering drawing, `{{PD-scan|PD-old-100-1923}}` — a directly relevant **engineering drawing**
- Modern site photos (CC BY-SA 2.0/4.0 — attribution + SA): `File:Thames_Tunnel_walk.jpg` (5499×3666), `File:Thames_Tunnel_Shaft.jpg`, `File:Thames_Tunnel_ceiling.jpg` (5616×3744)
- Useful categories: `Category:Thames Tunnel`, `Category:Brunel tunnelling shield`, `Category:Tunnelling`

**API (HIGH, verified live).**
- Licence metadata: `https://commons.wikimedia.org/w/api.php?action=query&prop=imageinfo&iiprop=extmetadata|url|mime|size&titles=File:{name}&format=json&formatversion=2` → per-file `LicenseShortName`, `UsageTerms`, `License` (`pd`/`cc0`/`cc-by-sa-4.0`), `LicenseUrl`, `Artist`, `Credit`, `AttributionRequired`, `Copyrighted`.
- Search: `action=query&list=search&srsearch={q}&srnamespace=6` (namespace 6 = File).
- **Filter by licence:** `haswbstatement:P275={Qid}` — e.g. `Thames Tunnel haswbstatement:P275=Q20007257` (CC BY 4.0) returned **44 hits**. Category membership (`Category:CC-BY-4.0`, `Category:CC-Zero`, `Category:PD Old`) also works. HIGH
- **3D:** `filemime:application/sla` → **11,642 STL files** (note: `filetype:stl` returns 0 — invalid syntax, do not use). Commons supports **.stl only, untextured**. HIGH
- **No media dumps:** *"As of 2024, there are no publicly available dumps of media files for download since about 2013."* Only XML wiki-content dumps. Use the API, PetScan, or `commons-category-downloader`. HIGH
- **User-agent policy — mandatory.** Wikimedia *requires* an HTTP `User-Agent`; *"Do not use generic agents such as 'curl', 'lwp', 'Python-urllib'"*; use the form `CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org) generic-library/0.0`. Unlabelled scripts *"may be blocked without notice"* (HTTP 403). HIGH
- **No published numeric rate limit.** Use exponential backoff. UNVERIFIED (none stated).

**3D reality check:** no Thames Tunnel or Brunel 3D/STL model was found anywhere. INFERENCE (MEDIUM): Commons is not a source of Thames-Tunnel 3D geometry. **Model it in Blender from the PD 2D drawings** — which is also the cleanest licensing path, since PD drawings carry no NC/SA constraints.

**Verdict: Commons is the primary source for Episode 1.** Every surviving file is commercially reusable; the only decisions are (a) whether you accept ShareAlike for CC BY-SA files, and (b) the jurisdictional PD-Art caveat, which for a UK channel resolves in your favour.

---

### 3.11 British Library / Flickr Commons

**The British Library's Flickr account is LIVE in 2026** (HIGH, profile JSON fetched 17 Sep 2026): **1,073,907 photos**, 58,507 followers, recent uploads dated Dec 2025.

**But the licence label is not what people remember.** The live Flickr field on BL's own photostream reads **`license: 7` = "No known copyright restrictions"** — *not* the Public Domain Mark (which is licence 10). HIGH. The 2013 release announcement said: *"We have released over a million images onto Flickr Commons for anyone to use, remix and repurpose. These images were taken from the pages of 17th, 18th and 19th century books digitised by Microsoft who then generously gifted the scanned images to us, **allowing us to release them back into the Public Domain**."* (HIGH). The Public Domain Review describes it as "under the public domain mark". **FLAG: the original label is mixed/unresolved — but both are re-use-permissive.**

**"No known copyright restrictions" is not a licence and carries no warranty** (HIGH, Flickr Foundation, verbatim): *"When Flickr Commons members assert no known copyright restrictions, they are sharing the benefit of this research **without also providing an expressed or implied warranty**… **the responsibility is yours to make your own independent analysis of your right to do so.**"* See also the NKC 1.0 text at §3.5.

**The BL's own website terms draw a clear and useful line (HIGH, verbatim):**
- **PD-marked content:** *"Where content is marked as public domain, the Library believes it to be in the public domain in most territories… **You are free to use this material as you wish**, but it is your responsibility to ensure that your use… will not infringe on the rights of third parties."* → **commercial OK.**
- **CC-marked content:** *"**You may freely use such content for non-commercial purposes** as long as you acknowledge the British Library Board…"* → **non-commercial only.**
- **Reading-room content:** no commercial re-use without written authorisation.

→ **Practical rule: BL PD-marked images = usable; BL CC-marked images = not usable on a monetised channel.** Because the Flickr field is NKCR rather than an explicit PD mark, verify the underlying work is genuinely PD-old (pre-1900 book illustrations are safe) rather than relying on the label.

**Bulk access:** `https://github.com/BL-Labs/imagedirectory` (Flickr Commons manifests) plus the Flickr uploads themselves. HIGH

**2023 cyber-attack status (MEDIUM):** the BL's own cyber-attack page still describes digital collections as unavailable, but that text appears **stale (last updated March 2024)**; the live homepage served 17 Sep 2026 shows a working catalogue link and normal navigation → **partial restoration**. Whether all digitised content is fully back: UNVERIFIED.

**BL Images Online** (`imagesonline.bl.uk`) returned **HTTP 403** to automated fetch. INFERENCE (MEDIUM): a paid commercial licensing service.

**Flickr Commons generally → REQUIRES A DECISION → in practice DO NOT USE for a monetised channel.** The uploader's belief is not a rights determination, the rightsholder is unidentified, and there is no indemnity.

---

### 3.12 National Railway Museum (railwaymuseum.org.uk)

**The NRM is part of the Science Museum Group**, and its collection is published through the **same** SMG collection platform and API. HIGH — confirmed: the Rocket locomotive record `co26704` carries `category: {museum: "NRM", name: "Locomotives and Rolling Stock"}` in the SMG API.

**Consequence: the NRM image licence position is SMG's** — per-image `CC BY-NC-SA 4.0` / `CC BY-NC-ND 4.0` / `OGL v3.0`, with commercial use routed to the Science & Society Picture Library. HIGH. The exact per-image string is `"legal":{"rights":[{"licence":"CC BY-NC-SA 4.0","copyright":"© The Board of Trustees of the Science Museum"}]}`.

SMG's own About page, verbatim (HIGH): *"All our collection data and images, where possible, are made available under a Creative Commons licence."* / *"you can find records with images released under a **Non-Commercial** Creative Commons licence."* / *"**If you would like to use our images commercially, please contact the Science & Society Picture Library.**"* The `search/image_license` filter reports "Non-Commercial Use **177,227**" in its UI (vs the **212,113** API total I measured) — both confirm the NC predominance.

**Actual NRM / SMG items (HIGH):** `co26704` Rocket locomotive (1829); `co205749` "Evening Star"; `co205762` Electric locomotive No. 26020; `co429392` Locomotive worksplate. All under the same NC scheme.

**3D:** no downloadable 3D assets found in the API. Press coverage indicates 3D scanning work has been done (e.g. of Rocket), but downloadable models and their licences are **UNVERIFIED**.

→ **SMG/NRM is a research and identification source, not a publishable imagery source**, except for any OGL v3.0-licensed images (UNVERIFIED how many).

---

### 3.13 Historic England Archive & Britain from Above

**Historic England — restrictive, and effectively unavailable without a paid licence.** All HE hosts returned **HTTP 403 (Cloudflare)** to automated fetching, including archive.org mirrors. From the archived **Website Terms and Conditions** (snapshot 18 Dec 2025), verbatim (HIGH):
> *"All content, designs, text, graphics, software compilations and source codes on this website are the copyright of Historic England and/or its content providers. Reproduction of part or all of the contents of this website in any form is prohibited other than for individual use only… The permission to recopy by an individual does not allow for incorporation of material or any part of it in any work or publication… **Any other use of the website without prior written consent from Historic England is strictly forbidden.**"*
And for OS/APGB imagery: *"a non-exclusive, royalty free, revocable licence **solely to view** the Licensed Data for **non-commercial purposes**."*
- Archive image licensing and the price list are **UNVERIFIED** (403 on every route). Search indexing confirms an "Archive Services and Price List" with a permission/commercial section. INFERENCE (MEDIUM): **commercial use is a paid permission process.**
- **NHLE listing data** (`/listing/the-list/data-downloads/`) is commonly OGL — but **UNVERIFIED** (403). Do not assume.
- **Warning flag (LOW on detail):** a Wikimedia UK mailing-list thread is titled *"False copyright claims in Historic England's 'Aerial Photograph Explorer'"*, concerning aerial photos "whose copyright has expired". Relevant as a caution that HE asserts rights over very old material.
- **Aerial Photo Explorer / APEX:** HE states it holds **~6 million historic aerial photographs** covering England. Terms UNVERIFIED.

**Britain from Above — hypothesis CONFIRMED: no commercial use.** Live terms at `https://britainfromabove.org.uk/en/legalities`, verbatim (HIGH):
> *"The Britain from Above website is open for all people to use as it is provided. **That free use is limited to personal, individual and educational use.**"*
> *"**No permission is given for any commercial use, distribution or reproduction in these terms.** Please email archives@hes.scot for these purposes and separate licenses will be provided."*
> *"The images, information and data featured on this website are subject to Crown Copyright and other Intellectual Property Rights held by the applicable BfA Parties and Contributors…"*
Download page, verbatim (HIGH): *"You may: copy, print, display, and store for your personal use at home and you may copy to a blog or personal web page as long as the page is freely available with no [ads]… **No Commercial Use or Sale, No Sub-Licensing.**"*

**CORRECTION to a common assumption: Britain from Above is run by Historic Environment Scotland (HES)**, not Historic England — *"This is a Licence from HISTORIC ENVIRONMENT SCOTLAND"* — with Historic England and RCAHMW licensing their own materials. Licence T&C last updated **28 November 2024**. HIGH

Coverage begins **1919** (Aerofilms) → **irrelevant to 1825–1843**, but relevant to later railway/dock/bridge episodes, and **non-commercial only** in every case.

---

### 3.14 Network Rail & The National Archives (UK)

**Network Rail.** No open image archive found. Material is bespoke and permission-based. The Network Rail Media Centre (`networkrailmediacentre.co.uk`) exists with press images, some login-gated; its terms did not render to automated fetch — **UNVERIFIED**. INFERENCE (MEDIUM): **press-use only**, not a general commercial licence.
One directly relevant item has already escaped into the public domain: `File:Network_Rail_Virtual_Archive_Box_Tunnel.jpg` — the **1838 GWR Box Tunnel engineering drawing**, on Commons under `{{PD-scan|PD-old-100-1923}}`, sourced from `networkrail.co.uk/VirtualArchive/`. **PD, commercially usable.** HIGH. This suggests historical Network Rail Virtual Archive drawings may be PD *as works*, whatever Network Rail's website terms say — a useful route for later episodes.

**The National Archives — the three-way distinction is CONFIRMED.**
The **Discovery API** works and returns **catalogue metadata only, no images** (HIGH):
`https://discovery.nationalarchives.gov.uk/API/search/records?sps.searchQuery=Thames%20Tunnel&sps.resultsPageSize=2` → HTTP 200, JSON with `count` (**1,058 records** for "Thames Tunnel") and `records[]` carrying `reference`, `title`, `description`, `coveringDates`, `heldBy`, plus facets.

TNA's own copyright terms, verbatim (HIGH):
- **Catalogue metadata / website text:** *"The material featured on this website is subject to Crown copyright protection and licensed for use under the Open Government Licence unless otherwise indicated."* → **commercially reusable.**
- **Digitised record images — NOT free to reuse:** *"The permissions above **do not extend to: images downloaded from our Discovery service; images in our image library; any material on this website which is identified as being the copyright of a third party.**"* And: *"**Commercial re-use:** Images from the collections of The National Archives posted on **Flickr and Wikimedia are for non-commercial use only.** If you need to use images for a commercial purpose, please refer to the pages on image reproduction and the Image Library."*
- **Transcriptions of Crown-copyright record text:** *"Under the terms of the Open Government Licence written content from a Crown copyright public record may be published by **transcription**, without charge."* → **free commercially.**

**OGL v3.0 — the licence, and the exact attribution string (HIGH, verbatim):**
> *"The Licensor grants you a **worldwide, royalty-free, perpetual, non-exclusive licence** to use the Information…"*
> *"exploit the Information **commercially and non-commercially** for example, by combining it with other Information, or by including it in your own product or application."*
> *"If the Information Provider does not provide a specific attribution statement, you must use the following: **Contains public sector information licensed under the Open Government Licence v3.0.**"*
Plus a link to `https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/`. **Where the Information Provider has specified its own attribution statement, that one governs.**

**Crown copyright duration rules (50-year rule, and the 125-year rule for some unpublished records): UNVERIFIED** — TNA's dedicated guidance page could not be loaded. **Do not rely on it without checking.**

**Relevance to Episode 1:** TNA holds Thames Tunnel Company and Board of Trade railway/Thames Tunnel plans (`YHC/CL/PB/6/plan1840/121`, `plan1824/60` and 1,058 Thames Tunnel records) — **catalogue entries and transcribed text are usable; the document images are not.**

---

### 3.15 TU Delft & Charles Babbage Institute

**TU Delft / 4TU.ResearchData.** Terms of Use PDF fetched, verbatim (HIGH): *"**Unless specified otherwise, metadata may be freely reused under the CC0 waiver.**"* Depositors choose the dataset licence. The live licence filter exposes **CC0, CC BY 4.0, CC BY-SA 4.0, CC BY-NC 4.0, CC BY-NC-ND 4.0, CC BY-NC-SA 4.0, CC BY-ND 4.0, ODbL-1.0, and a Restrictive Licence**, plus software licences (MIT, Apache-2.0, GPL).
→ **Metadata is CC0; the dataset file licence varies per record and must be checked individually.** No TU Delft heritage/engineering 3D dataset was confirmed for this episode.
`https://sketchfab.com/tudelft` returned **HTTP 202 with 0 bytes** (anti-bot) — **UNVERIFIED** whether the account is active in 2026 or its model licences. Do not rely on it without a manual check.

**Charles Babbage Institute (University of Minnesota).** Bot-blocked (Cloudflare / HTTP 202). UNVERIFIED terms. INFERENCE (MEDIUM): CBI is a **computing/information-technology history** archive — 20th-century papers, oral histories and photographs, overwhelmingly **in copyright**. **It is not a source of 19th-century engineering imagery or 3D, and its relevance to this channel is NONE.** HIGH on the negative (its collecting scope is explicit).

---

## 4. LEGAL ANALYSIS

*Full authorities, quotations and pin cites are in [`evidence/cc-attribution-monetised-reels-advice.md`](evidence/cc-attribution-monetised-reels-advice.md). This section is the operative summary.*

### 4.1 The licence spectrum

| Licence | Commercial? | Derivatives? | Must do | Breach trigger |
|---|---|---|---|---|
| **Public domain** | ✅ | ✅ | nothing (credit is courtesy) | none |
| **CC0 1.0** | ✅ expressly | ✅ | nothing | none |
| **CC BY 4.0** | ✅ | ✅ | attribution, modification indicator, licence URI | failing any §3(a) limb |
| **CC BY-SA 4.0** | ✅ | ✅ but **viral** — the adaptation must be BY-SA | BY + license your Reel under BY-SA | publishing the adaptation under anything more restrictive |
| **CC BY-NC 4.0** | ❌ | ✅ non-commercially | attribution + keep it non-commercial | any use whose primary purpose is commercial |
| **CC BY-NC-SA 4.0** | ❌ | ✅ non-commercially + viral | both | both |
| **CC BY-ND 4.0** | ✅ | ❌ for publication | BY | **sharing** an adaptation |
| **CC BY-NC-ND 4.0** | ❌ | ❌ | — | **categorically unusable** |
| **Rights-managed** | per instrument | per instrument | per instrument | exceeding scope (e.g. "editorial use only" used in advertising) |

**The structural point that governs everything** (HIGH, verbatim): a CC licence grants only rights the licensor holds — "Licensed Rights means the rights granted to You … which are limited to all Copyright and Similar Rights that apply to Your use of the Licensed Material **and that the Licensor has authority to license**" (CC BY 4.0 §1). And: "If the licensor's permission is not necessary for any reason … then that use is **not regulated by the license**." So §4.4 is logically prior to §4.2: if there is no copyright in the scan, the NC wrapper has nothing to attach to.

**CC's own position (HIGH, verbatim):** "**NC licenses do not qualify as 'open licenses' under the Open Definition, and works licensed under an NC license are not considered Free Cultural Works.**" → Treat an NC/ND-only source as **rights-managed with a discount**, not as open content.

**Corrections made during research** (each changes the analysis):
- **NoAdditionalRestrictions is §2(a)(5)(B)** in all six 4.0 licences; BY-SA adds a parallel term at **§3(b)(3)** for Adapted Material. It is *not* §3(a).
- **CC BY-ND 4.0 has no defined term "Modified Material."** The ND restriction lives in **§2(a)(1)(B)** ("produce and reproduce, but not Share, Adapted Material") and the closing sentence of §3(a)(1): "You do not have permission under this Public License to Share Adapted Material."
- **Attribution is §3(a)**, not §2(a)(1) (which is the licence grant).

### 4.2 Does monetisation make a use "commercial"?

**Definition, verbatim (HIGH)** — CC BY-NC 4.0 §1(a):
> "**NonCommercial** means not primarily intended for or directed towards commercial advantage or monetary compensation."

Two drivers: **"primarily"** — "no activity is completely disconnected from commercial activity; it is only the **primary purpose of the reuse** that needs to be considered"; and **"intended for or directed towards"** — a *purpose* test, not an *accounting* test. **Receipt of money is not required.** That is why a demonetised channel *with intent* fails.

**CC's own guidance (HIGH, verbatim):**
> "**NonCommercial turns on the use, not the identity of the reuser.**"

> "**Reusers may make NonCommercial uses only, even when reusing NC material with other works.** … an NC essay may not be included as part of a collection in a commercially distributed book of essays, **even if it is only a small portion of the book**. … an NC song may be used as the basis for a video where the visual elements are under a different license such as the BY license. When the **music video is distributed as a whole, it may not be used commercially** because of the NC license of the song."

**That passage is the single most important one for this project: the commercial character of the CONTAINING WORK governs; NC taint is not diluted by smallness or by mixing with freely-licensed material.** A Reel is both an adaptation and a collection, so the restriction flows through the whole video.

> "**The NonCommercial term does not limit uses otherwise allowed by limitations and exceptions to copyright.**"

**Verdicts per revenue model** (assuming arguendo the asset is protected):

| Revenue model | Commercial? | Confidence |
|---|---|---|
| Instagram ad revenue / Reels bonus / creator fund | **YES** | HIGH |
| Brand sponsorship / paid partnership on a Reel | **YES** | HIGH |
| Affiliate links in bio | **YES** | HIGH-MEDIUM |
| Selling your own unrelated paid products (Patreon, courses) | **YES** | HIGH-MEDIUM |
| Currently demonetised but intends to monetise | **YES** | HIGH |
| Genuinely personal, no money sought, on a public account | **NO** (arguable) | MEDIUM-HIGH |

**The channel described in the brief fails every commercial branch.** It is monetised by ad revenue, sponsorship, brand deals and promotion of the creator's own paid work.

**CRITICAL — is a CC BY-NC asset safe if the video is demonetised or is a personal project?**
**No, in the circumstances described.** CC BY-NC 4.0 §6 (HIGH, verbatim):
> "**§6(a)** … if You fail to comply with this Public License, then Your rights under this Public License **terminate automatically**."
> "**§6(b)** Where Your right to use the Licensed Material has terminated under Section 6(a), it reinstates: **1. automatically as of the date the violation is cured, provided it is cured within 30 days of Your discovery of the violation**; or 2. upon express reinstatement by the Licensor."

Three consequences:
1. **No front-end grace.** Enrolling in a monetisation programme or signing a sponsorship converts every prior NC use into ongoing breach **at that moment**; the licence terminates automatically and continued hosting is unauthorised reproduction + communication to the public.
2. **A 30-day cure window** after discovery is the only mitigation — a reason to keep a rights register that lets you find and pull affected Reels within a month, **not** a reason to rely on NC.
3. **Pivoting later is the most common failure mode.** Monetising a back-catalogue of NC-containing Reels means unpublishing or re-rendering all of them.
**Rule: never build an NC asset into an evergreen episode.**

**A note on the "it's just a hobby" argument.** `MEDIUM-HIGH`: public availability ≠ commerciality, and CC confirms NC "turns on the use, not the identity of the reuser" — so a genuinely private-purpose public account seeking no money can rely on NC. But that branch does not describe this channel, and the **intent** limb means "I plan to monetise eventually" breaks it before the first payout.

**Not curable** by attribution, a disclaimer, or "not monetising that specific Reel."

**One genuine escape hatch:** an exception or limitation — fair use (US) / fair dealing (UK). CC expressly says NC "does not limit uses otherwise allowed by limitations and exceptions." For short critical/commentary history content a fair-use argument is *arguable*, but it is a **legal-risk position, not a licence position**, jurisdiction-specific, and outside a no-legal-review workflow. **Do not build a channel on it.**

**ShareAlike compounds it:** derivatives must be released under the same NC-SA licence — incompatible with monetisation.

**A correction to a common belief:** the alleged German LG Köln / LG Frankfurt "Klimt" NC disputes are **UNVERIFIED**; no case name, date or holding could be located. Do not cite them.

### 4.3 Attribution that actually satisfies CC BY — TASL in a 9:16 Reel

**Exact required elements — CC BY 4.0 §3(a)(1) (HIGH, verbatim):** if You Share the Licensed Material (including in modified form), You must:
> **a. retain the following if it is supplied by the Licensor with the Licensed Material:**
> i. identification of the creator(s) … in any reasonable manner requested by the Licensor (including by pseudonym if designated);
> ii. a copyright notice;
> iii. a notice that refers to this Public License;
> iv. a notice that refers to the disclaimer of warranties;
> v. a URI or hyperlink to the Licensed Material **to the extent reasonably practicable**;
> **b. indicate if You modified the Licensed Material and retain an indication of any previous modifications; and**
> **c. indicate the Licensed Material is licensed under this Public License, and include the text of, or the URI or hyperlink to, this Public License.**
> **2. You may satisfy the conditions in Section 3(a)(1) in any reasonable manner based on the medium, means, and context in which You Share the Licensed Material. For example, it may be reasonable to satisfy the conditions by providing a URI or hyperlink to a resource that includes the required information.**

Limb (a) is a duty to **retain what was supplied** — you must not invent a copyright notice or warranty disclaimer that was not given.

**TASL.** Title, Author, Source, Licence. From CC's *Recommended practices for attribution* (HIGH): **Title** is required for CC 3.0 and earlier but **optional in 4.0**; **Author** means the licensor/rightsholder (include the copyright notice if supplied); **Source** should be the **original** URL, not a shortener; **Licence** must name and link the licence. CC's own good example: *"[Creative Commons 10th Birthday Celebration San Francisco](…) by [Timothy Vollmer](…) is licensed under [CC BY 4.0](…)"*. CC's expressly **incorrect** example: *"Photo: Creative Commons"* — "Creative Commons is not the author!"

**Copy-pasteable strings.**

**(a) CC0 asset** (not legally required; recommended):
> "Marc Brunel's tunnelling shield, 1825–1843" — 3D scan by [Creator], [Institution], https://example.org/scan/123. Dedicated to the public domain under CC0 1.0 (https://creativecommons.org/publicdomain/zero/1.0/).

**(b) CC BY 4.0 photogrammetry scan:**
> "Marc Brunel's tunnelling shield (1825)" — 3D scan by [Creator], [Institution]. Source: https://example.org/scan/123. Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Adapted: re-meshed, retextured and re-lit in Blender; camera re-angled for vertical format.

**(c) CC BY-SA 4.0** — same, plus:
> **This Reel is licensed under CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0).**

**(d) PD work** (recommended credit line):
> "Marc Brunel's tunnelling shield, Thames Tunnel (1825–1843)." Public domain. Source: [Institution], https://example.org/item/456.

**The hard practical problem — and the answer.** §3(a)(2)'s "**in any reasonable manner based on the medium, means, and context**", expressly contemplating "providing a URI or hyperlink to a resource that includes the required information", is the provision that makes a 9:16 Reel workable. CC's own guidance for video: "**consider publishing a web page with attribution information**", and make Author/Source/Licence followable "if possible within the medium". But CC also warns that attributing **in metadata fields only** is "in most cases this is **not the only place**", and that many users never see it.

**Instagram constraints (verified status, 17 Sep 2026):**
- **Caption length:** historically 2,200 characters. **LOW** — the official Help Centre page returned empty; **caption length is not the binding constraint; discoverability and persistence are.**
- **Clickable links in captions:** historically Instagram did **not** linkify captions ("link in bio" was the workaround; the link sticker was a Stories feature). **MEDIUM-HIGH for the historical position.**
- **2026 state:** multiple secondary reports (Mar–Apr 2026) describe **testing/rolling out clickable caption links**, reportedly tied to a paid/verified tier. **LOW-MEDIUM** — no primary source, and a test is not a shipped feature. **Verify in-app on the day; do not design compliance around caption links.**
- Whether **comments / pinned comments** are linkified, and whether the **link sticker works on Reels**: **UNVERIFIED.**

**Recommended layered architecture — no single point of failure:**
1. **On-video overlay (2–3 s, end card or lower-third).** Minimum TASL: creator, licence, source domain. E.g. `Scan: [Creator] / [museum.org] — CC BY 4.0`. **This is the only layer that travels with the video** when it is screen-recorded, re-uploaded or embedded. INFERENCE — high practical value.
2. **Caption** — the full string, with the licence URI written out as **plain text** (`creativecommons.org/licenses/by/4.0`) so it survives non-linkification.
3. **Pinned first comment** — same full string.
4. **Bio link → a stable per-episode credits page on your own domain** (`/credits/ep1`) with complete TASL records, full licence URIs and the modification log. §3(a)(2) expressly contemplates this route.

**Is a bio-linked credits page sufficient? Probably yes under §3(a)(2), but it is the weakest layer and relying on it alone is a real risk.** (i) §3(a)(1)(A) requires *retaining* supplied info — a credits page omitting a supplied copyright notice or warranty disclaimer fails; (ii) the reasonableness test is medium-relative, and where a 2-second on-screen credit *is* possible, viewer-facing attribution two taps away is arguably unreasonable; (iii) the bio link is a single rotating slot — the Reel and the credits page **detach** when you change the bio, and permanently when the Reel is re-shared; (iv) CC expressly criticises metadata-only attribution. **MEDIUM-HIGH as to risk.** **Rule: never rely on the bio link alone.**

**What does NOT work:** metadata/EXIF only; alt text only; crediting "Creative Commons" or the hosting platform instead of the author; crediting a real name where a pseudonym was supplied. All four are CC-identified pitfalls. HIGH

**Modification indicators — §3(a)(1)(B).** Two duties: declare your modifications, **and preserve the licensor's pre-existing modification statement**. CC's examples: slight modification → *"'[Title]' by [Author], used under [CC BY 4.0] / **Cropped from original**"*; adaptation → *"**This work, '90fied', is adapted from** '[Title]' by [Author]…"*; for video, attribute **both in the description box and in the video recording itself**.
**Correct wording for a Blender render derived from a scan:**
> 3D render adapted from "[Scan Title]" by [Creator] ([Host], CC BY 4.0). Modifications: decimated and re-meshed; UVs re-unwrapped; albedo/normal maps re-baked; materials replaced with a Principled BSDF setup; camera re-positioned for 9:16; lighting and HDRI environment added; geometry of [X] reconstructed from period engravings where the scan was occluded.
For BY-SA add the licence line. For ND there is **no wording fix** — you may not publish the render at all.
**Practical rule: log modifications as you make them** — retrofitting from memory understates them.

**Watermarks / "all rights reserved" / NoAdditionalRestrictions — §2(a)(5)(B) (HIGH, verbatim):** "You may not offer or impose any additional or different terms or conditions on, or apply any Effective Technological Measures to, the Licensed Material **if doing so restricts exercise of the Licensed Rights** by any recipient." §3(b)(3) extends this to Adapted Material.

| Question | CC BY | CC BY-SA |
|---|---|---|
| Channel watermark? | **Ordinarily yes** if it is branding — the clause bites only where the term/measure *restricts* recipients' exercise. MEDIUM-HIGH | **Risky.** The whole Reel is Adapted Material offered under BY-SA; a watermark functioning as an ownership assertion or anti-copy measure risks §3(b)(3). Neutral brand mark defensible; "© All Rights Reserved" or an anti-download overlay is not. MEDIUM-HIGH |
| Claim the whole video as mine? | **No, not the whole.** You own your script, animation, voiceover, edit, compositing; you must not assert rights over the CC material or imply endorsement. Correct form: *"© 2026 [Channel]. Contains material by [Creator], used under CC BY 4.0."* HIGH | **No.** The video as distributed must be offered under BY-SA. HIGH |
| Moral rights? | Not licensed (§2(b)(1)); integrity rights may separately constrain derogatory treatment. HIGH | Same. |
| Trademarks? | Not licensed (§2(b)(2)). A museum name in a credit line is attribution, not endorsement. HIGH | Same. |

### 4.4 The "NC scan of a PD object" wrapper problem

Two questions must be separated: **(Q1) does copyright subsist in the scan?** **(Q2) if not, can the museum still bind you by contract?**

**4.4.1 United States — a faithful scan is very likely unprotectable.**
- ***Bridgeman Art Library, Ltd. v. Corel Corp.*, 36 F. Supp. 2d 191, 195 (S.D.N.Y. 1999)** (HIGH — quoted and adopted by the U.S. Copyright Office): "a photograph which is no more than a copy of a work of another as exact as science and technology permits lacks originality. That is not to say that such a feat is trivial, simply not original."
- **U.S. Copyright Office, Compendium (3d ed.) §313.4(A)** (HIGH, verbatim): "**A work that is a mere copy of another work of authorship is not copyrightable.**" Unregistrable examples include "An exact reproduction of the Mona Lisa that cannot be distinguished from the original — **A photocopy or scan of a photograph** — Photocopying, scanning, or digitizing a literary work."
  *Correction:* the brief attributed the derivative-work/PD rule to **§313.4(C)**; §313.4(C) is "Words and Short Phrases". The correct provisions are **§311.2** and **§313.4(A)**.
- **Compendium §311.2** (HIGH, verbatim): "**A registration for a derivative work only covers the new authorship that the author contributed** … a registration for a derivative work **does not cover … public domain material** that appears in the derivative work." *See* 17 U.S.C. §103(b). Threshold: "'the key inquiry is whether there is sufficient nontrivial expressive variation … to make it distinguishable from the [preexisting] work in some meaningful way' … 'Nor can the requirement of originality be satisfied simply by the demonstration of "physical skill" or "special training."'" (*Schrock v. Learning Curve Int'l*, 586 F.3d 513, 521 (7th Cir. 2009)).
- ***Meshwerks, Inc. v. Toyota Motor Sales U.S.A., Inc.*, 528 F.3d 1258 (10th Cir. 2008)** — directly on point for 3D models. HIGH for the facts and holding quoted; LOW for any finer doctrinal characterisation (full opinion text was unreachable; WorldLII/OpenJurist 403).
  *Facts:* Meshwerks measured Toyota vehicles with an articulated arm, then hand-sculpted the models. "**approximately 90 percent of the data points contained in each final model … were the result not of the first-step measurement process, but of the skill and effort its digital sculptors manually expended at the second step**"; "nearly **80 to 100 hours of effort per vehicle**"; wheels, headlights, handles and the emblem "had to be added at the second 'sculpting' stage".
  *Holding (verbatim):* "*While fully appreciating that digital media present new frontiers for copyrightable creative expression, in this particular case the uncontested facts reveal that **Meshwerks' models owe their designs and origins to Toyota and deliberately do not include anything original of their own; accordingly, we hold that Meshwerks' models are not protected by copyright and affirm.***"
  *What it did **not** hold:* it is not a technology-wide rule (framed as "this particular case"), and it concerned measurement-and-modelling rather than photogrammetric capture — though the reasoning transfers directly.
- **Application:** the *Meshwerks* facts are **more favourable to the institution** than a modern photogrammetry scan — Meshwerks *added* 90% of data points by hand and still lost. A capture-and-solve pipeline is, on the *Meshwerks*/Compendium framing, a mere copy of a useful article. INFERENCE: MEDIUM-HIGH for US law. The counter-argument — curatorial *selection and arrangement* of a scan collection — protects only the collection, not the individual scan. HIGH
- **US synthesis:** the shield itself is PD; US law does not protect useful articles in their utilitarian aspects; a faithful scan adds no protectable authorship. **US risk: LOW-MEDIUM legally.**

**4.4.2 Germany — the riskiest jurisdiction for this project.**
- **§72 UrhG** (HIGH, fetched verbatim): *Lichtbilder* — mere photographs, and products made similarly to photographs — get the **related right** of a *Lichtbildner*, expiring **"fünfzig Jahre nach dem Erscheinen des Lichtbildes"** (50 years from publication). Contrast *Lichtbildwerke* (photographic works) under §2(1) No.5 / §2(2), which get 70 years p.m.a.
- **BGH "Museumsfotos", 20 December 2018 – I ZR 104/17** (HIGH; JurPC Web-Dok. 26/2019). Plaintiff: Reiss-Engelhorn-Museum, Mannheim. *(Note: some secondary reports say 19 December; the JurPC record says **20.12.2018**.)*
  *Leitsätze (verbatim):*
  > "2. **Fotografien von (gemeinfreien) Gemälden oder anderen zweidimensionalen Werken unterfallen regelmäßig dem Lichtbildschutz nach § 72 UrhG.**"
  > "3. Fertigt der Besucher eines kommunalen Kunstmuseums unter Verstoß gegen das im privatrechtlichen Besichtigungsvertrag mittels Allgemeiner Geschäftsbedingungen wirksam vereinbarte Fotografierverbot Fotografien … an und macht er diese Fotografien im Internet öffentlich zugänglich, kann der Museumsträger als Schadensersatz die Unterlassung der öffentlichen Zugänglichmachung im Internet verlangen."
  *The crucial structure — the museum won on two different bases for two different asset sets:*
  - **The museum's own pre-existing photographs** (scanned by the defendant): infringement of the **§72 *Lichtbild* right** — injunction under §97(1), §72 UrhG. "Auch die handwerkliche Leistung ohne künstlerische Aussage kann in den Schutzbereich des § 72 UrhG fallen"; photographing a work requires "Entscheidungen des Fotografen über … **Standort, Entfernung, Blickwinkel, Belichtung und Ausschnitt**". The court **expressly refused** the academic argument for teleological reduction excluding photographs of PD works from §72. HIGH
  - **The defendant's own photographs of PD exhibits**: **no copyright claim at all** — the claim succeeded **only** on breach of the *Besichtigungsvertrag* (viewing contract, photography ban incorporated as AGB), grounded in **§280(1), §249(1) BGB**. The ban survived a §307 BGB fairness challenge. HIGH
  - **Limit 1 — 2D only.** The Leitsatz is confined to "**zweidimensionalen Werken**". HIGH
  - **Limit 2 — the "Urbild" requirement.** "Der Lichtbildschutz erfordert, dass das Lichtbild als solches **originär, das heißt als Urbild, geschaffen** worden ist." A photogrammetry capture of a physical object is an *Urbild*; a re-scan of someone else's photograph is not. HIGH
- **Application.** A photograph of a PD 2D work → **§72 Lichtbild, 50 years from publication**. A photogrammetry scan of a PD 3D engineering object → §72 **probably available** (the "Standort, Entfernung, Blickwinkel, Belichtung, Ausschnitt" reasoning applies a fortiori to camera positions, coverage and solver choices), but the Leitsatz is confined to 2D. INFERENCE: MEDIUM. **Germany's Article 14 transposition could not be verified — do not assert a section number.** UNVERIFIED.
- **German synthesis — MEDIUM-HIGH practical risk.** Unlike the US, German law gives the museum a **statutory related right requiring no originality**, and the BGH has already blessed it for museum photographs of PD works.
- **A safe harbour worth knowing:** §51 Satz 3 UrhG (quotation right, from 1 March 2018, UrhWissG, BGBl. 2017 I, S. 3346) permits using "eine Abbildung des zitierten Werkes zum Zwecke des Zitats" even where the image is itself protected. It failed in *Museumsfotos* because uploading to Wikimedia Commons was not for citation — but it is genuinely useful for a documentary video that **quotes** an image in commentary. HIGH

**4.4.3 Spain.** Real Decreto Legislativo 1/1996 (LPI) **Article 128** gives a **25-year right in "meras fotografías"** (mere photographs) — a related right of the German kind. MEDIUM — the BOE text was **not fetched**; verify article number and wording at boe.es. The "Carmen Calvo" / PD-painting controversy and any Tribunal Supremo ruling are **UNVERIFIED — do not assert a Supreme Court decision.** Article 14 transposition: **UNVERIFIED.** **Practical Spanish risk: MEDIUM, mitigated for 2D visual art by Article 14.**

**4.4.4 United Kingdom — no Article 14, a favourable 2023 Court of Appeal ruling, and one real trap.**
- **No UK equivalent of DSM Article 14.** The UK left the EU before the 7 June 2021 transposition deadline (Article 29), so Article 14 was never implemented. MEDIUM.
- **Originality — the *Infopaq* test now governs, and the old "skill and labour" test is displaced.** ***THJ v Sheridan* [2023] EWCA Civ 1354** (primary judgment fetched from the National Archives' Find Case Law service): the Court of Appeal held the trial judge applied the wrong test — *"the test he applied was that of 'skill and labour', which was the test applied by the English courts prior to Infopaq"* — and that the correct test is the *Infopaq* "author's own intellectual creation" standard (Case C-5/08, at [37]). HIGH that skill-and-labour is displaced.
  **FLAG:** the proposition that this specifically means faithful photographic reproductions of PD 2D art gain no UK copyright is stated flatly by Commons policy and by law-firm commentary, but an **explicit PD-art holding could not be located in the retrieved judgment text** — *THJ* concerned a photograph of a Red Bus/other subject, not a reproduction of a PD artwork. Treat the specific proposition as **well-supported but not fully primary-verified. MEDIUM.**
- **CDPA 1988 s.12(2)** (HIGH, verified): copyright in a literary, dramatic, musical or artistic work *"expires at the end of the period of 70 years from the end of the calendar year in which the author dies."* s.12(3) unknown authorship: 70 years from making/making available.
- **THE SPECIAL RULE FOR OLD PHOTOGRAPHS — a major de-risking.** **CDPA 1988 Schedule 1, para 12(2)(c)** (HIGH, verified): copyright in *"published photographs and photographs taken before 1st June 1957"* continues only until the date it would have expired under the **1956 Act — i.e. 50 years from creation**. So **essentially all pre-1957 photographs are out of copyright in the UK**, regardless of the 70-years-pma rule. Para 12(4)(c): unpublished photographs taken on/after 1 June 1957 got 50 years from commencement (1 August 1989).
  → For a British-engineering channel this is powerful: any 19th- or early-20th-century photograph is out of UK copyright on this rule alone.
- **Correction:** the brief asked about **CDPA s.99** — **s.99 is "Delivery up in criminal proceedings" and is unrelated.** The relevant provisions are s.1(1)(a) (originality), s.12 (duration) and Sch 1 para 12 (transitional).
- **THE TRAP — the publication right, SI 1996/2967 reg. 16** (HIGH, verbatim, current revised text):
  > "**16.—(1)** A person who after the expiry of copyright protection, publishes for the first time a **previously unpublished work** has … a property right ('publication right') **equivalent to copyright**. … **(6) Publication right expires at the end of the period of 25 years** from the end of the calendar year in which the work was first published. **(7)** … a 'work' means a literary, dramatic, musical or artistic work or a film."
  Publication includes *"making the work available by means of an electronic retrieval system"* and *"communicating the work to the public"*. Reg. 16(5): no publication right where Crown/Parliamentary copyright subsisted.
  
  **The right attaches to the previously unpublished WORK ITSELF — not to the photograph.** So if a UK/EEA institution is first to publish a previously unpublished Brunel drawing, notebook, letter or report, it obtains a **copyright-equivalent property right for 25 years**, surviving expiry of the underlying copyright, unaffected by Article 14 (never implemented in the UK), and undefeated by the work's PD status.
  **Practical rule: a PD-old-100 *published* work is safe; a PD-old-100 *previously unpublished* work first published by a museum in the last 25 years is NOT. Check publication history, not just death dates.** INFERENCE from reg. 16: HIGH. **Prefer published-period sources** (Penny Magazine 1832, Illustrated London News, LoC) over newly-surfaced archival material.
- **UK synthesis — practical risk: LOW-MEDIUM, and better than the brief assumed.** No Article 14, but (a) the *THJ v Sheridan* / *Infopaq* originality standard likely defeats a claim over a faithful photo of PD 2D art, and (b) Sch 1 para 12(2)(c) puts essentially all pre-1957 photographs out of copyright. **The residual risk is the 25-year publication right on previously unpublished archival material — not scan copyright.**

**4.4.5 France.** Protection depends on *originalité* — classically the "**empreinte de la personnalité de l'auteur**". **CPI Article L.112-2, 9°** protects "les œuvres photographiques" as *œuvres de l'esprit* only if original. 2026 decisions published on the Cour de cassation's own Judilibre database apply a **demanding** originality filter to photographs (e.g. reasoning that the choices observed did not distinguish the photograph from an ordinary snapshot). MEDIUM. France has **no general simple-photograph related right** of the German/Spanish kind. LOW-MEDIUM (INFERENCE from the absence of such a right in the CPI's related-rights title). **No Cour de cassation decision on photographs of PD works could be verified — asserted nowhere.** **Practical French risk: LOW-MEDIUM.**

**4.4.6 DSM Directive (EU) 2019/790, Article 14 — the provision that decides the EU question.**
**Verbatim (HIGH):**
> "**Article 14 — Works of visual art in the public domain**
> Member States shall provide that, when the term of protection of **a work of visual art** has expired, **any material resulting from an act of reproduction of that work is not subject to copyright or related rights, unless the material resulting from that act of reproduction is original in the sense that it is the author's own intellectual creation.**"

**Recital 53 (verbatim, via IPKat):** "In the field of visual arts, the circulation of **faithful reproductions of works in the public domain** contributes to the access to and promotion of culture… **the protection of such reproductions through copyright or related rights is inconsistent with the expiry of the copyright protection of works.** … **Certain reproductions of works of visual arts in the public domain should, therefore, not be protected by copyright or related rights.** All of that should not prevent cultural heritage institutions from **selling reproductions, such as postcards**."

**Scope and limits — four points:**
1. **"Related rights" is expressly covered.** This is what makes Article 14 bite on Germany's §72 *Lichtbild* right and Spain's *mera fotografía* right. MEDIUM-HIGH.
2. **It is confined to "works of visual art".** Article 14 is *not* a general "no rights in reproductions of PD works" rule. MEDIUM-HIGH.
3. **Does it cover a 3D scan of a physical engineering object? — no authority answers this, and it is the single most consequential open question.** The trigger is "a **work of visual art**". A 19th-century tunnelling shield is a **machine — a useful article**, generally not a work of visual art (its *drawings* could be; its *utilitarian aspects* would not be). Therefore:
   - For a scan of **the shield itself**, Article 14 **probably does not apply** — and a §72-style related right may survive. INFERENCE: MEDIUM.
   - For a scan of a **PD painting, engraving, lithograph or architectural drawing**, Article 14 **probably does apply**, defeating a new related right. INFERENCE: MEDIUM-HIGH.
   - "any **material** resulting from an act of reproduction" is broad enough to encompass a 3D model or point cloud, so the *medium* is not the obstacle — the **subject-matter gate** is. MEDIUM-HIGH on the medium point.
4. **Term Directive 2006/116/EC Article 6** confirms Member States "may provide for the protection of other photographs" — i.e. sub-original photographs by related right, exactly what §72 UrhG and Art. 128 LPI do. Article 14 then carves out the PD-visual-art case within its field. MEDIUM-HIGH.

**→ Practical translation for Episode 1: you are on much firmer ground using scans of 2D visual artworks (engravings, watercolours, patent drawings, period illustrations) than scans of the 3D machine itself.**

**4.4.7 The museum-contract argument.**
The verified German authority shows the contract route worked — but on facts that do **not** transfer to a public-website download: the contract was a *Besichtigungsvertrag* formed at the ticket desk, the ban was an AGB incorporated "durch hinreichend deutlich sichtbaren Aushang", and it survived §307 BGB review. **That is an on-site, contracting-in-person model, not browsewrap.** HIGH

Three contract models:
1. **Click-through / signed image-supply licence** (you request the file; the museum sends it; you accept terms). **Strongest** — genuine offer and acceptance; binds regardless of what copyright says. **If you ask a museum for a scan under a bespoke licence, you are bound by it.** HIGH
2. **Website terms accepted by conduct ("browsewrap").** **Weakest.** Turns on notice and assent (Germany: §305(2) BGB; the UK: incorporation-by-notice and consumer-unfairness rules). MEDIUM generally; LOW for any specific authority.
3. **A CC licence tag on a work with no copyright.** Grants nothing — "Licensed Rights" are limited to rights "that the Licensor has authority to license" (deed §1). A CC BY-NC tag on an unprotectable scan imposes no condition enforceable *qua* licence. MEDIUM-HIGH.

**The third-party-rights wildcard — the real reason for caution.** Even if the *museum's* claim fails, the scan may embody rights the museum had no authority to waive or license (the photographer's own §72/related right; a data provider's; donor conditions). CC0 §4(c) and every CC disclaimer expressly disclaim responsibility for clearing third-party rights. HIGH for the disclaimer; INFERENCE for its application. **This is exactly what the two unlicensed third-party images in SMG record `co66652` demonstrate.**

**Policy materials.** The *principle* is well evidenced by instruments verified directly (DSM Article 14 and Recital 53; the *Bridgeman*/Compendium position; WMF policy). The Europeana **Public Domain Charter** / **Public Domain Usage Guidelines**, **Communia** position papers, and the RightsStatements.org NKC rationale express the same principle, but **could not be fetched** (europeana.eu and pro.europeana.eu returned HTTP 403). **Their specific wording is UNVERIFIED and is not quoted here.**

**4.4.8 Synthesis — is the museum's CC BY-NC wrapper enforceable?**

| Jurisdiction | (a) Legal enforceability over a faithful scan | (b) Platform takedown risk | (c) Reputational risk | Overall |
|---|---|---|---|---|
| **US** | **Low.** No copyright in a faithful reproduction; no "Licensed Rights" to license. Contract claim only if you accepted terms. MEDIUM-HIGH | Medium — Meta acts on notices, not merits | Medium-high — museums police uploads actively | **LOW-MEDIUM legally; MEDIUM overall** |
| **EU (general)** | **Low-medium**, subject to the "visual art" gate. Art. 14 defeats copyright *and related rights* for PD **visual art**; probably not for a 3D machine. MEDIUM | Medium | Medium-high | **MEDIUM** |
| **Germany** | **Medium-high against you.** §72 UrhG gives a 50-year related right; *Museumsfotos* blesses it for PD works (framed for 2D). MEDIUM-HIGH on §72; LOW on Art. 14 | Medium | High | **MEDIUM-HIGH — worst jurisdiction** |
| **UK** | **Low-medium.** No Art. 14; *Infopaq* originality likely defeats a faithful-photo claim. **But reg. 16's 25-year publication right is a real trap for unpublished Brunel material.** MEDIUM-HIGH on the publication right | Medium | Medium | **MEDIUM** |
| **France** | **Low-medium.** Demanding *originalité*; no general simple-photograph related right. MEDIUM | Medium | Medium | **LOW-MEDIUM** |
| **Spain** | **Medium.** Art. 128 LPI (*mera fotografía*, 25 years) is a fallback related right; Art. 14 should defeat it for PD visual art. UNVERIFIED | Medium | Medium-high | **MEDIUM** |

**The three-layer distinction, plainly.**
- **(a) Legal enforceability** is what a court would hold after full argument. Weak in the US; weak-to-medium in the EU and UK; genuinely contested in Germany. Practical value: a well-drafted letter asserting *Bridgeman*/Article 14 usually ends a dispute — if you can afford to write it.
- **(b) Platform takedown risk is independent of (a).** Meta operates notice-and-takedown; a rights-manager claim or DMCA notice from a museum results in removal or monetisation-diversion **whether or not the claim is valid**. You may counter-notice, but that requires identifying yourself, consenting to jurisdiction, and takes weeks. HIGH for US notice-and-takedown generally; INFERENCE as to Meta's specific processes.
- **(c) Reputational risk compounds.** Museums are the natural sources of the *good* scans and curators talk. A public dispute over Episode 1 can cost the cooperation you need for Episodes 2–20. CC-licence breaches are, in practice, **published** breaches — the CC community and Wikimedia volunteers detect and document them. MEDIUM-HIGH (INFERENCE).
- **Repeated strikes risk account loss.** Accumulating strikes can lead to feature restrictions and ultimately account disablement. MEDIUM — standard platform practice; Instagram's current thresholds UNVERIFIED.

**Recommended posture: do not rely on the legal argument as your operating strategy. Operate as if the NC wrapper binds — i.e. do not use NC-licensed scans — and keep *Bridgeman*/Article 14 in reserve for (i) US-federal-PD material obtained from a source asserting rights it does not have, and (ii) negotiating a bespoke licence.**

### 4.5 Categorically safe, requires a decision, prohibited

**SAFE — no legal review needed**
- Public domain works (published ≤1930 US; PD-old-100; Crown copyright expired; UK pre-1957 photographs under CDPA Sch 1 para 12(2)(c)), **subject to the publication-right check for previously unpublished works**
- **CC0 1.0** (Smithsonian CC0 subset; Rijksmuseum PD images; Getty Open Content where CC0)
- **Sketchfab `cc0`** and **Sketchfab Store Standard/Free Standard**
- **ALL Wikimedia Commons files** — because **NC licences are banned by Commons policy**, every surviving file permits unrestricted commercial use. The *only* remaining Commons decision is whether to accept **CC BY-SA** (viral). This makes Commons the only major source that needs no NC analysis at all.
- Your own Blender modelling and renders

**SAFE WITH ATTRIBUTION**
- **CC BY 4.0** (Sketchfab `by`; Wikimedia CC-BY; Europeana CC-BY; SMG descriptions/text)
- **OGL v3.0** (the SMG image subset; TNA catalogue metadata)
- **The decision forced is not *whether* but *how you record it*:** build the TASL pipeline **before you download anything**. If you cannot reconstruct the creator, source URL, licence and modification record from your own files, you cannot satisfy CC BY — which converts a "safe with attribution" source into an unresolved risk.

**REQUIRES A DECISION**
- **CC BY-SA 4.0** — *Are you willing to license the Reel **and** the Blender-derived render under CC BY-SA 4.0 and give up exclusivity?* If yes, legally safe and commercially viable. If no — "all rights reserved" branding, sponsor exclusivity, paid bundling of the render — you must not use SA.
- **Library of Congress "Free to Use and Reuse"** — *Does this item have third-party rights the label does not clear?* Safe as *copyright* risk; not safe as *uncleared-rights* risk.
- **Historic England / Britain from Above / Getty (pre-verification)** — *What does this specific licence actually permit, and is there a commercial tier?* Treat as licensed content until proven otherwise.

**PROHIBITED for a monetised channel**
- **CC BY-NC / NC-SA / NC-ND** — no exceptions on the facts described. If you badly want a specific NC asset, **ask the institution for a commercial licence** — NC licensors may expressly grant separate commercial terms (CC wiki confirms NC is non-exclusive).
- **CC BY-ND** — for any Blender-derived render (§2(a)(1)(B) permits producing but not *sharing* Adapted Material). A straight unmodified turntable render is the only defensible use, and even that is arguable.
- **CC BY-NC-ND** — categorically.
- **Scan the World / MyMiniFactory** — NC licence *plus* an independent non-commercial ToS.
- **Science Museum Group / National Railway Museum images** — NC, except the OGL v3.0 subset.
- **Sketchfab Store `ed` (Editorial)** — no commercial or promotional use.
- **Smithsonian "usage conditions apply"** — commercial use expressly excluded.
- **Internet Archive lending-library items** — in copyright.
- **Rights-managed / "no known copyright restrictions"** (Flickr Commons, IA uploader content) — NKC is a disclaimer, not a licence.
- **The National Archives digitised record images** — free to view ≠ free to reuse.

**Four cross-cutting checks.** Make each once, in writing, and apply consistently:
1. **Is the item's rights statement the one you think it is?** Programme-level claims ("open access", "free to use") are not item-level licences. Screenshot the item page and its rights statement at download time.
2. **Is the work protected where your audience is, not just where the server is?** PD status is territorial; the US/EU/UK divergence is the whole of §4.4.
3. **Is the work *previously unpublished*?** If yes, run the UK/EEA publication-right check (25 years).
4. **What is the attribution and modification record?** Build the register before Episode 1 ships, not after Episode 10.

---

## 5. PRODUCTION PLAN FOR EPISODE 1

**Pre-cleared (no legal review needed) — in priority order:**

1. **Internet Archive — the Episode 1 hero material.**
   - **`explicationdestr00unse`** — the **1837** French volume on the Thames Tunnel, contributed by the **Getty Research Institute**, described as containing ***"sectional drawings of the tunneling shield."*** PD by date. **This is the best single Episode 1 asset found in any source.** Verify the Getty Research Collections record for an explicit CC0 download.
   - Four pamphlets, all `possible-copyright-status = NOT_IN_COPYRIGHT`: `thamestunnelade00tunngoog` (1825), `originprogressa00westgoog` (1827), `sketchesworksfo00cruigoog` (1829, Cruikshank), `anexplanationwo00compgoog` (1840, Thames Tunnel Company). Download `_jp2.zip` (high-res page images) or PDF.
   - **Filter with `possible-copyright-status:NOT_IN_COPYRIGHT`** — `collection:pub_*` does **not** work.

2. **Wikimedia Commons PD files — the primary Episode 1 imagery source.** Every surviving Commons file is commercially reusable (NC is banned by policy), and the period Thames Tunnel imagery is PD. Highest-value items:
   - **`File:Penny_Magazine_1832_341_Shield_used_in_the_Excavation_of_the_Thames_Tunnel.jpg`** — 1832 woodcut of the shield, 1400×840. **The best historical image of the shield.**
   - `File:Thames_tunnel_shield.png` — diagram, 787×542
   - `File:Penny_Magazine_1832_340_Longitudinal_Section_of_the_Tunnel.jpg` — 1750×370 section
   - `File:Penny_Magazine_1832_258_Thames_Tunnel.jpg` — 1659×1007
   - `File:The_Thames_Tunnel_LCCN98507755.jpg` — LoC lithograph, **6736×5248**
   - `File:Illustrirte_Zeitung_(1843)_01_006_3_Sir_I_Brunel_wie_er_bei_der_Eröffnungsfeier_den_Tunnel_durchschritt.PNG` — 1843 opening ceremony
   - `File:Sir_Marc_Isambard_Brunel_by_James_Northcote.jpg` — 2400×3025 portrait (d. 1831)
   - `File:Robert_Howlett_(Isambard_Kingdom_Brunel_Standing_Before_the_Launching_Chains_of_the_Great_Eastern),_The_Metropolitan_Museum_of_Art.jpg` — 5616×7334 (d. 1858)
   - `File:Network_Rail_Virtual_Archive_Box_Tunnel.jpg` — **1838 GWR Box Tunnel engineering drawing**, `{{PD-scan|PD-old-100-1923}}`
   - `File:Medaille_met_portret_van_Marc_Isambard_Brunel,_RP-P-1910-4751.jpg` — Rijksmuseum, **CC0**
   
   **Prefer published-period sources** (Penny Magazine, Illustrated London News, LoC) over newly-surfaced archival material, to stay clear of the UK 25-year publication right.

3. **Europeana** — `reusability=open`, including the one commercially usable Thames Tunnel image: **"Der Themse-Tunnel"**, Public Domain Mark, City Museum Berlin (`/736/item_6C4HHEPIENLL7RFGCYVBFM6JNY4USSDZ`). Remember the invalid-`reusability`-value trap.

4. **Smithsonian CC0** — Thames Tunnel records `nmah_1144472`, `siris_sil_261561`, `siris_sil_160362`, `siris_sil_160364`, `siris_sil_160365`, `siris_sil_377827`, `siris_sil_285653`, `siris_sil_261531`, `siris_sil_246327`, `siris_sil_261583`, `siris_sil_368208`; Brunel `siris_sil_4317`, `siris_sil_246163`, `siris_sil_255547`. **Fetch `/content/{url}` and confirm a `media` block with `media_usage` = CC0** — metadata CC0 alone is insufficient.

5. **Sketchfab** `cc0` / `by` via `https://api.sketchfab.com/v3/search?type=models&downloadable=true&licenses=cc0&q=…`, downloaded with an **API Token** (`Authorization: Token …`). Verified CC0 industrial content: RG Ross & Sons Steam Hammer `d80b52dc800e4c76b6b27749bbd8e782`; VIC 32 Cochran boiler `884ed11e38054aa48a3db1d9025c881d`, `fb84ddbabd554f7e9b5b2d34b9b47be5`; QE2 turbine patterns `8e135c1a917c476a98f011a48c4192c7`, `96d548dfc5d943a8a5cfcc07ebfd1618`. Also the **8 CC0 SMG models** (amputation saw, figurehead, Chinese junk, catalytic converter, pill cutter, cigarettes, leech jar, brain model). Log `license.label`, `user.username`, `uid`, download date.

6. **Build the tunnelling shield in Blender** from the PD 2D drawings (the 1837 sectional drawings, the Penny Magazine sections, the 1838 Box Tunnel drawing) — the cleanest licensing path, and **necessary**: no Thames Tunnel 3D model exists in any source surveyed (not in Sketchfab's SMG catalogue, not in the Thingiverse mirror, not anywhere).

7. **Getty Open Content CC0** for later episodes — Manchester Ship Canal 1894, Gotthardbahn bridge c.1875–82. Credit *"Digital image courtesy of Getty's Open Content Program"*. **Getty has no usable Thames Tunnel material** (its only hit is in copyright).

8. **Rijksmuseum** (`data.rijksmuseum.nl`, keyless Linked Art) — assert CC0 from the object record, not the IIIF manifest.

9. **LoC HABS/HAER/HALS** measured drawings (US federal PD) for later episodes; read rights via `https://lccn.loc.gov/{lccn}/mods`.

10. **TNA transcriptions** of Crown-copyright record text — free commercially under OGL, with the attribution string in §3.14.

**Prohibited for this episode:** SMG/NRM images and their NC Sketchfab models; Scan the World; Sketchfab `*-nc*` and `*-nd`; Sketchfab Store Editorial; Smithsonian "usage conditions apply"; Flickr Commons / BL CC-marked content; IA uploader content and lending items; **the David Rumsey Thames Tunnel plate (CC BY-NC-SA 3.0)**; Historic England / Britain from Above; TNA digitised record images; Getty's in-copyright items.

**Requirements to build before Episode 1 ships:**
- A **licence register** (asset → creator → source URL → licence → download date → modifications). Essential given Sketchfab ToS §4.1/§4.6 (retroactive change, licence termination) and the 30-day CC cure window.
- A **per-episode credits page** on your own domain, linked from bio — the §3(a)(2) backbone.
- A **2–3 s on-video TASL overlay** — the only layer that survives re-sharing.
- **Do not** put "Smithsonian"/"SI"/any museum name in the channel name, handle or nickname (a bio mention is fine).

---

## 6. VERIFICATION LEDGER

**Verified verbatim from primary sources (HIGH):** CC BY 4.0, CC BY-NC 4.0, CC BY-SA 4.0, CC BY-ND 4.0 and CC0 1.0 licence deeds; CC wiki *NonCommercial interpretation* and *Recommended practices for attribution*; Compendium 3d ed. §§311.2, 313.4(A)–(C); DSM Directive (EU) 2019/790 Article 14; §72 UrhG; CDPA 1988 s.12 and **Sch 1 para 12(2)(c)**; SI 1996/2967 reg. 16; *THJ v Sheridan* [2023] EWCA Civ 1354 (Find Case Law); RightsStatements.org NKC 1.0 and the 12 statement URIs; RightsStatements.org governance release (1 Apr 2026); WMF *Resolution:Licensing policy*; **Commons licensing policy, the 11 PD/CC templates, `Commons:When_to_use_the_PD-Art_tag`, `Commons:Reuse_of_PD-Art_photographs`, the user-agent policy, and ~20 Thames Tunnel/Brunel file pages**; BGH 20.12.2018 – I ZR 104/17 "Museumsfotos" (JurPC Web-Dok. 26/2019); *Meshwerks* 528 F.3d 1258 (facts and holding); **SMG's datasets page, API page, About page, Creative Commons policy page, robots.txt, and API responses (including the 429 body, the ignored `filter[image_licences]` param, and the `co66652` per-image licences)**; **SMG's 52-model Sketchfab catalogue via `api.sketchfab.com/v3/models?user=sciencemuseum`**; **Europeana's accepted-rights-statements page, 3D publishing guide, Publishing Framework tiers, Fair Use policy, and live API responses (`reusability` values and the invalid-value trap, `qf=RIGHTS`, the RIGHTS/TYPE facets, and the 24-record Thames Tunnel set with its `edm:rights` values)**; Sketchfab `GET /v3/licenses`, the search-param rejection of `cc-by`, the 401 download response, and the help-centre licence and Store pages; KitBash acquisition (Kotaku/GamesBeat/ArtStation); Smithsonian `/stats` and FAQ; **Getty Open Content FAQs (via Wayback)**; **LoC Free to Use and Reuse (via Wayback)**; **Rijksmuseum's CC0/PD statements (via the Commons batch-upload page)**; **BL Flickr profile JSON and BL site terms**; **Britain from Above live terms (Historic Environment Scotland)**; **TNA copyright terms, the Discovery API, and OGL v3.0**; **4TU.ResearchData terms**; **Internet Archive `advancedsearch`, `metadata` and `download` endpoints**.

**Verified at HIGH confidence through an authoritative conduit rather than the primary text:** *Bridgeman*, 36 F. Supp. 2d 191, 195 — quoted and adopted by the U.S. Copyright Office at Compendium §313.4(A); DSM Recital 53 and Term Directive Art. 6 — quoted verbatim by IPKat; DSM Recital 53 also confirmed via IPKat's reproduction of the OJ text.

**Blocked / unusable this session (403, 410 or empty):** `collection.sciencemuseumgroup.org.uk` via the fetch tool (works via curl with a browser UA + `Accept: application/json`); `si.edu`, `3d.si.edu`; `myminifactory.com` (Cloudflare); `pro.europeana.eu`, `europeana.eu`, `www.europeana.eu` (Cloudflare — Europeana documentation was read via the public Knowledge Base at `europeana.atlassian.net`); **`www.loc.gov` HTML *and* `?fo=json`, and `chroniclingamerica.loc.gov` (403 Cloudflare — worked around via `lccn.loc.gov/{lccn}/mods` and Wayback)**; `getty.edu` (Cloudflare — read via Wayback); **`iiif.getty.edu` (HTTP 000 — use `media.getty.edu`)**; `historicengland.org.uk` and all HE hosts (Cloudflare); `epicgames.com`; `imagesonline.bl.uk`; `sketchfab.com/developers/guidelines` (202); full *Meshwerks*/*Bridgeman* opinion text (WorldLII, OpenJurist, CourtListener, Casetext); Instagram Help Centre; **`lab.sciencemuseum.org.uk` (DEAD — Cloudflare Error 1000)**; **`rijksmuseum.nl/api/...` (HTTP 410 Gone — retired)**.

**UNVERIFIED — asserted nowhere in this document:** **the LoC `fo=json` endpoint signatures (`c=`, `sp=`, `dates=`) and the Chronicling America API (both unreachable)**; Europeana's numeric rate limit (none is published) and the API terms at `europeana.eu/rights/terms-of-use`; whether the "Europeana Sculpture pilot" exists (no evidence — likely a conflation with "Twin it! 3D for Europe's culture" or EUreka3D); **Rijksmuseum's rate limits (the 10,000/day figure belonged to the retired 410 API), its logo/marks terms, and whether its 2 `Brunel` / 31 `Thames` hits are on-topic**; **Getty's object-level REST signature (404 on all attempts), its rate limits, bulk dump and API-key documentation**; the resolution of **Getty's internal ToU tension** (general "commercial use prohibited" vs the Open Content clause permitting it); Getty's Museum-vs-GRI licence split; **Historic England's current commercial licence terms** (403); Network Rail's terms; **TNA's current Crown-copyright duration rules**; **Britain from Above's terms beyond the verified Nov 2024 version**; TU Delft's holdings and Sketchfab account; the German/Spanish/French statutory transposition of DSM Article 14; **whether *THJ v Sheridan* specifically establishes that faithful reproductions of PD 2D art gain no UK copyright** (the primary text confirms only the displaced *Infopaq* test); **Instagram's current Reels caption limit, whether it linkifies captions or comments in 2026, whether the link sticker works on Reels, and its copyright-strike thresholds**; SMG's OGL-vs-NC image split and its Terms & Conditions substantive clauses; Sketchfab's numeric rate limit; **the Internet Archive's platform-wide rights statement and any numeric rate limit**; Rijksmuseum's OAI-PMH June 2026 breaking-change details.

**The single most consequential open question.** Whether **DSM Article 14 reaches a photogrammetry scan of a 3D engineering object that is not a "work of visual art"**. On my reading it probably does not — so the EU, and Germany in particular, may give a museum a surviving §72-style related right in a scan of **the shield itself**, while a scan of a period **engraving** of the shield would be protected by Article 14. If that reading is right, the actionable strategy is exactly the one in §5: **build the episode on PD 2D visual material and your own Blender modelling, and treat 3D museum scans of the machine as licensed material to be negotiated, not assumed.**
