# Licensing research: Science Museum Group + Europeana
**Research date: 17 September 2026.** All checks performed live on that date. Monetisation context assumed: Instagram Reels, 9:16 vertical, AI voiceover, ad revenue + brand sponsorship ⇒ **commercial use** under CC and under SMG's own definition.

Legend: **[HIGH]** = read verbatim on a live page/endpoint today. **[MED]** = read from a live page but interpretation/one hop removed. **[LOW]** = inferred or third-party. **INFERENCE:** = my reasoning, not cited. **UNVERIFIED** = could not confirm.

---

## 0. Contradictions with prior expectations (recorded as required)

| I expected | Live sources show | Source |
|---|---|---|
| SMG released large sets of images under **CC0** | **False.** Images are `CC BY-NC-SA 4.0`, `CC BY-NC-ND 4.0` or `OGL v3.0`. **Zero** CC0 images found. Only *metadata* fields are CC0. | [HIGH] group CC policy + API licence fields + filter probe |
| SMG API supports `filter[image_licences]` (documented) | **Param is IGNORED** by the live API — counts identical with and without it, including for the value `CC0`. | [HIGH] live counts |
| Europeana accepts all 12 RightsStatements.org statements | **False.** Europeana accepts **6 of the 12**: NoC-NC, NoC-OKLR, InC, InC-EDU, InC-OW-EU, CNE. | [HIGH] KB "Accepted rights statements and URIs" v36, 2026-08-18 |
| `wskey` is the standard Europeana auth | **Deprecated since 2023.** Preferred is the `X-Api-Key` header. Access policy split into Personal vs Project keys on **28 May 2025**. | [HIGH] KB "Accessing the APIs" v20 |
| Europeana has a published numeric rate limit | **No numeric limit is published.** "Fair use policy" is qualitative; 429 is the only signal. | [HIGH] KB "Fair use policy & guidelines" v10 |
| Europeana 3D viewer built on **3D Hop** | **No evidence of 3D Hop anywhere.** Europeana embeds **Sketchfab** and **WEAVE** (weave-3dviewer.com) oEmbed URLs; EDM guidelines also show a **Eureka3D Viewer**. | [HIGH] 3D publishing guide |
| "Europeana **Sculpture** pilot" | **UNVERIFIED.** No such pilot found in the Europeana Knowledge Base, PRO index, or web search. Likely confusion with **"Twin it! 3D for Europe's culture"** and/or the **EUreka3D** project. | — |
| `lab.sciencemuseum.org.uk` is a live 3D blog | **Host is broken:** Cloudflare **Error 1000 — "DNS points to prohibited IP"**. Never fetched successfully. | [HIGH] fetch attempt 17 Sep 2026 |

---

# A. SCIENCE MUSEUM GROUP

## A1. Collection API — endpoints

**Licensing/usage page (must-read):** `https://www.sciencemuseumgroup.org.uk/our-work/our-collection/using-our-collection-api` (200 OK). **[HIGH]**
The URL `.../about-us/collection/using-our-collection-api/` **redirects here** — use the `/our-work/our-collection/` form.

**API docs:** `https://github.com/TheScienceMuseum/collectionsonline/wiki/Collections-Online-API` (200 OK, read via `https://raw.githubusercontent.com/wiki/TheScienceMuseum/collectionsonline/Collections-Online-API.md`). **[HIGH]**
**JS examples:** `https://github.com/TheScienceMuseum/collectionsonline-api/tree/master/examples`

Base URL: `https://collection.sciencemuseumgroup.org.uk`

| Endpoint | Verified |
|---|---|
| `GET /search?q=…` | [HIGH] returns `application/vnd.api+json` |
| `GET /search/objects?q=…` / `/search/people` / `/search/documents` | [HIGH] all returned JSON |
| `GET /objects/{id}/{slug?}` , `/people/{id}` , `/documents/{id}` | [HIGH] JSON **with correct headers** |
| `GET /api/objects/{id}/{slug?}` , `/api/documents/{id}`, `/api/people/{id}` | [HIGH] JSON **with correct headers** |
| `.json` suffix (e.g. `/objects/co26704.json`) | **Does NOT work** — the `.json` suffix returns the SPA HTML / 403. **[HIGH]** |

**Content negotiation is mandatory and fragile. [HIGH]**
- `curl -A "<browser UA>" -H "Accept: application/json" https://collection.sciencemuseumgroup.org.uk/api/objects/co26704/rocket-locomotive` → **200, `application/vnd.api+json`**
- Same path **without** the `Accept` header → **200 but `text/html`** (the SPA shell, ~442 KB) — you silently get HTML.
- Same path with a **non-browser UA + `Accept: application/json`** → **403 CloudFront "Request blocked"**.
- The wiki's own example (`curl -ig -H "Accept: application/json" -A "Your User Agent / 1.0"`) is what I could NOT get through reliably; a full Chrome UA string worked.
- **Send BOTH a browser-like `User-Agent` and `Accept: application/json`, and always verify `content-type` before parsing.** INFERENCE: the front end is a CloudFront-protected SPA and the JSON API is served only on that content-negotiation path.

### Exact query parameters (verbatim from the wiki + verified live)

Global: `q` (required), `random`, `page[number]` (zero-indexed), `page[size]` (default 50, **max 100**), `fields[TYPE]`, `date[from]`, `date[to]`, `places`.
Objects: `type`, `makers`, `people`, `organisations` (alias for `people`), `categories`, `museum` (`NRM|SMG|NMeM|MSI`), `on_display`, `location`.
People: `birth[place]`, `birth[date]`, `death[date]`, `occupation`.
Documents: `type`, `makers`, `people`, `organisations`, `archive`, `formats`, **`image_licences`**.
JSON:API form is also accepted: `filter[PARAM_NAME]` (e.g. `filter[categories]=…`).

**`filter[image_licences]` is documented but has NO EFFECT. [HIGH]** Measured 17 Sep 2026:

| Query | Count |
|---|---|
| `/search/objects?q=thames` | all=1401 (objects 1105, documents 163) |
| `/search/objects?q=thames&filter[image_licences]=CC BY-NC-SA` | **identical 1401** |
| `/search/objects?q=thames&filter[image_licences]=CC0` | **identical 1401** |
| `/search/objects?q=tunnel` | 2454 |
| `/search/objects?q=tunnel&filter[image_licences]=CC BY-NC-ND` | **identical 2454** |

`filter[makers]` **does** appear to filter (a non-matching value returned 0). So the failure is specific to `image_licences`. INFERENCE: it is a Documents-only facet and/or broken. **Never rely on it to prove a licence — read `multimedia[].legal.rights[].licence` per image.**

### Licence location in the JSON (note: docs are WRONG)

The datasets page documents the field as `source.legal.rights.usage`. **That path does not exist.** The live field is:

```
data.attributes.multimedia[N].legal.rights[N].licence        e.g. "CC BY-NC-SA 4.0"
data.attributes.multimedia[N].legal.rights[N].copyright      e.g. "© The Board of Trustees of the Science Museum"
data.attributes.multimedia[N].credit.value                   e.g. "Science Museum Group Collection"
data.attributes.multimedia[N]["@processed"].large.location
data.attributes.multimedia[N]["@processed"].zoom.location    (IIIF .ptif)
```
**[HIGH]** — verified on `co26704` (Rocket), `co27198`, `co8013336`, `aa110066849`.
Note `attributes.legal` at object level is a **different thing** — usually just `{"credit": "…"}` (donor credit), **not** a licence.

## A2. Licence situation — exact strings

**Source: `https://group.sciencemuseum.org.uk/creative-commons/` → redirects to `https://www.sciencemuseumgroup.org.uk/creative-commons/` (200 OK). [HIGH]**

Exact licence strings found live on the policy page:
- **`CC BY-NC-SA 4.0`** — "Where indicated, the Creative Commons Attribution-Noncommercial-ShareAlike (CC BY-NC-SA 4.0) licence applies to **images**, learning resources and other content."
- **`CC BY 3.0`** — applies to "'open access' content such as the **Science Museum Group Journal**."
- **`CC0`** — "applies to **datasets such as the collection metadata**."

SMG's own definition of **commercial** (verbatim, this is the clause that kills the channel):
> "Creative Commons defines commercial use as 'reproducing a work in any manner that is primarily intended for or directed toward commercial advantage or monetary compensation'. The Science Museum considers the following to be commercial (this list is not exhaustive): use in a product or service that is commercial, such as books and journals; **use that promotes a product or service that is commercial**; use by charities, including the trading arms of charities; free-entry events (including lectures) that promote a product of services."
> Non-commercial includes: "use on personal social media accounts, **provided the individual is not promoting themselves commercially**".
> "**For all commercial usage, contact Science and Society Picture Library**" → `https://www.scienceandsociety.co.uk/`

**API page licence split (verbatim): [HIGH]**
> "Data in the title, made, maker and details fields: **Creative Commons Zero**"
> "Descriptions and all other text content: **Creative Commons Attribution 4.0 licence**"
> "Imagery and photography: **the licensing and copyright varies per image** (please check the source.legal.rights.usage for each image)."

**Datasets page licence split (`https://coimages.sciencemuseumgroup.org.uk/datasets/index.html`, page dated 6 August 2025). [HIGH]**
> "Data in the title, made, maker and details fields are released under **Creative Commons Zero**."
> "Descriptions and all other text content are licensed under a **Creative Commons Attribution 4.0 licence**."
> Attribution text required: **"© The Board of Trustees of the Science Museum"** plus a link back to `https://collection.sciencemuseumgroup.org.uk`.
> "Please check and only use image which fall under on of ther following three licence": **`CC BY-NC-SA 4.0`**, **`CC BY-NC-ND 4.0`**, **`Open Government Licence v3.0`** (links given).
> "Many records contain more than one image and while the first image may be made available under an open source licence that does not necessarily hold true for all other image on that record. **Always check the licence for each individual image.**"

**Live per-image evidence (this is the decisive point): [HIGH]**
- `co27198` (Thames Tunnel opening medal, 1843) — 2 images, both `licence: "CC BY-NC-SA 4.0"`, `copyright: "© The Board of Trustees of the Science Museum"`.
- `aa110066849` (Brunel/Thames Tunnel document collection, MS/0346) — 1 image, `CC BY-NC-SA 4.0`.
- `co8013336` (Print: Section through the Thames Tunnel) — 3 images: 2× `CC BY-NC-SA 4.0`, and **one with `licence` absent and `copyright: "T Blood"`** (third-party, no CC licence). **This single record disproves any blanket "SMG images are reusable" assumption.**
- `co58317` (Model of part of Marc Brunel's Thames Tunnel second shield) — **0 images.**

**Is there a separate "Open Access" subset? → NO for objects/images. [HIGH]**
The CC policy uses "open access" only to describe the **Science Museum Group Journal** under `CC BY 3.0`. The `/about` page's only licence-filter link is `http://collection.sciencemuseumgroup.org.uk/search/image_license`, which surfaces **"records with images released under a Non-Commercial Creative Commons licence"** — i.e. the "open" set is the **NC** set. Verified live: the SMG Journal is CC BY (commercial-allowed) — `https://journal.sciencemuseum.ac.uk/about/`: "made available using the **Creative Commons Attribution (CC BY) licence**… allows for the use, copying, reproduction and adaptation of articles, free of charge"; **but** "All images provided by the Science Museum Group/Science & Society Picture Library (SSPL) are provided under the **CC BY NC licence** for the benefit of the Journal". **[HIGH]**
**INFERENCE:** the SMG Journal is the only SMG "Open Access" content: text is CC BY 3.0 (commercially usable with citation), its SSPL images are CC BY-NC (not usable).

**Terms and conditions:** `https://www.sciencemuseumgroup.org.uk/terms-and-conditions/` (200 OK via web_fetch; **405 via plain curl/Varnish**). Last updated **4 August 2020**. The substantive clauses ("Prohibited use", "Intellectual property", "Using content from science museum group websites") are **JS-collapsed and were not retrievable** — **UNVERIFIED**. The page delegates: "Please also see our Creative Commons and Privacy and Cookies policies."

## A3. 3D scans / 3D models

**Yes — via Sketchfab, embedded into collection object pages. There is no SMG-hosted 3D viewer or downloadable 3D repository.**

- **Sketchfab account:** `https://sketchfab.com/sciencemuseum` ("Science Museum Group"). API: `https://api.sketchfab.com/v3/models?user=sciencemuseum&count=24`; user record `https://api.sketchfab.com/v3/users/...` — username `sciencemuseum`, **uid `0dca0f8b55514f1e84ddadf47cc299a8`** (the `/v3/users/sciencemuseum/models` path 404s; use `?user=sciencemuseum`). **[HIGH]**
- **Full catalogue enumerated 17 Sep 2026: 52 unique downloadable-or-not models.** Licence breakdown **[HIGH]**:
  - **33 × `CC Attribution-NonCommercial`** (`http://creativecommons.org/licenses/by-nc/4.0/`), `isDownloadable: true`
  - **8 × `CC0 Public Domain`**, `isDownloadable: true`
  - **1 × `CC Attribution-NonCommercial-ShareAlike`** (Enigma machine, 1934)
  - **10 × no licence at all**, `isDownloadable: false`
- **The 8 CC0 (commercially usable) models:** `Amputation Saw`, `Figurehead - Science Museum`, `Chinese Junk Ship - Science Museum`, `Catalytic converter, 1982-1983`, `Pill cutter, Europe, 1801-1900`, `Packet of Cigarettes`, `Pharmacy Leech Jar`, `Model of a human brain`.
- **No Brunel / Thames Tunnel / tunnelling-shield 3D model exists on the SMG Sketchfab account.** Nearest engineering item is **`Stephenson's Rocket`** — but it is **`CC Attribution-NonCommercial`** (§A6).
- **Collection pages embed Sketchfab.** Verified in the raw HTML of `https://collection.sciencemuseumgroup.org.uk/objects/co26704/rocket-locomotive`: the string `sketchfab.com/3d-models/09d73611eeda4aa7a4f3643766b340da/embed` is present. **The Sketchfab reference is NOT in the JSON API** (grep for `sketchfab` over the full API response for `co26704` = **0 hits**). **[HIGH]** → INFERENCE: 3D presence is server-rendered HTML only; you must scrape the HTML page to map object ↔ Sketchfab model, or use the Sketchfab API by name.
- **Historical/contextual (HIGH from live sources):** SMG's photogrammetry programme is described at `https://blog.sciencemuseum.org.uk/photogrammetry-taking-collection-digitisation-to-the-next-level/` (2 Oct 2018, Kira Zumkley) — "creating digital 3D models of our objects and our digital team is working on making them accessible via sketchfab and our collections online website". The linked deep-dive `https://lab.sciencemuseum.org.uk/scanning-stephensons-rocket-40916fdb4d20` is on the **dead host** (Cloudflare Error 1000). **UNVERIFIED** content.
- **`lab.sciencemuseum.org.uk` status: BROKEN. [HIGH]** Both `https://lab.sciencemuseum.org.uk/3d-object-scans-as-a-museum-learning-resource-part-1-9e1e51b67581` and `https://lab.sciencemuseum.org.uk/all?topic=3d-scanning` resolve to a Cloudflare **Error 1000 (DNS points to prohibited IP)** page. Do not cite that blog.

## A4. Thames Tunnel / Brunel material — actual IDs (all [HIGH], live API 17 Sep 2026)

Search counts: `q=thames tunnel` → **1847** (942 objects, 868 documents, 37 people). `q=brunel` → **516**. `q=marc isambard brunel` → **2412**. `q=tunnelling shield` → **391**. `q=tunnel shield` → **1940**.

**Key objects:**
| ID | Title | URL |
|---|---|---|
| `co58317` | **Model of part of Marc Brunel's Thames Tunnel second shield** | `https://collection.sciencemuseumgroup.org.uk/objects/co58317/model-of-part-of-marc-brunels-thames-tunnel-second-shield` |
| `co8234340` | model of tunnelling shield | `https://collection.sciencemuseumgroup.org.uk/objects/co8234340/model-of-tunnelling-shield` |
| `co27198` | Thames Tunnel opening commemorative medal, 1843 (acc. 1924-453) | `…/objects/co27198/thames-tunnel-opening-commemorative-medal-1843` |
| `co66652` | Thames Tunnel | `…/objects/co66652/thames-tunnel` |
| `co8012665` | The Thames Tunnel | `…/objects/co8012665/the-thames-tunnel` |
| `co8013323` | Print: Thames Tunnel | `…/objects/co8013323/print-thames-tunnel` |
| `co8013336` | **Print: Section through the Thames Tunnel and three diagrams of the interior** (acc. 1981-1015/28) | `…/objects/co8013336/print-section-through-the-thames-tunnel-and-three-diagrams-of-the-interior` |
| `co65677` | Lithograph, "The Thames Tunnel" | `…/objects/co65677/lithograph-the-thames-tunnel` |
| `co8013322` | Print: Thames Tunnel Rotherhithe Entrance | `…/objects/co8013322/print-thames-tunnel-rotherhithe-entrance` |
| `co8013321` | Print: Proposed entrance to the Thames Tunnel | `…/objects/co8013321/print-proposed-entrance-to-the-thames-tunnel` |
| `co524211` | Commemorative trowel used to lay the first stone of the Thames Tunnel | `…/objects/co524211/…` |
| `co66671` | 'The Thames Tunnel' peepshow, with original box | `…/objects/co66671/…` |
| `co66194` | Advertisement of 1840 for the Thames Tunnel | `…/objects/co66194/…` |
| `co8013330`, `co8013329` | Broadsheet: The Thames Tunnel (Teape & Son) | `…/objects/co8013330/…` |
| `co65117` | Rotherhithe tunnel | `…/objects/co65117/rotherhithe-tunnel` |
| `co58511` | Model, Greathead Shield, Blackwall Tunnel | `…/objects/co58511/…` |
| `co58560` | Whitaker Tunnelling Machine | `…/objects/co58560/whitaker-tunnelling-machine` |
| `co46742` | Bust of Marc Isambard Brunel, Engineer (1769-1849) | `…/objects/co46742/…` |
| `co27093` | Portrait bust of Marc Isambard Brunel | `…/objects/co27093/…` |
| `co211045`, `co211006` | Portrait bust of Isambard Kingdom Brunel | `…/objects/co211045/…` |
| `co27813` | Letter, Isambard Kingdom Brunel to G.H. Wollaston, 13 Feb 1834 | `…/objects/co27813/…` |
| `co74842` | Copy letter, Isambard Kingdom Brunel to ?, 22 Mar 1839 | `…/objects/co74842/…` |

**Key documents (archive):**
| ID | Title |
|---|---|
| `aa110066849` | **Collection of documents relating to the work of Marc Isambard Brunel, mainly concerning the Thames Tunnel** (MS/0346) — `https://collection.sciencemuseumgroup.org.uk/documents/aa110066849/collection-of-documents-relating-to-the-work-of-marc-isambard-brunel-mainly-concerning-the-thames-tunnel` |
| `aa110066942` | Papers relating to M.I.Brunel and the construction of the Thames Tunnel from Rotherhithe to Wapping |
| `aa110098622` | "A plan shewing the progress of the Thames Tunnel" |
| `aa110066756` | Engineering drawing: Plunging pump as used at the Thames Tunnel |
| `aa110067120` | Notebooks of G.H. Wollaston relating to Thames Tunnel from Rotherhithe to Wapping |
| `aa110098619` | Letter from Brunel to Monsieur D'avannes re working conditions, accident and health records of the workforce at the Thames Tunnel |
| `aa110098623` | "Thames Tunnel. Copies of Treasury Minutes and Correspondence…" |
| `aa110098624` | "Report from the Select Committee on the Thames Tunnel; with the Minutes of Evidence" |
| `aa110134582` | Printed report of the Directors of the Thames Tunnel Company |
| `aa110066847` | Advertisement by the Thames Tunnel Company, 'Open to the public every day…' |
| `aa110133444` | Printed circular: Progress and state of the Tunnel under the Thames / Thames Archway Company |
| `aa110134578` | Letter re steam engines, mentions another flood at the Thames Tunnel and how 'young Brunel … had a narrow escape' |
| `aa110066227` | Letter from Marc Isambard Brunel to James Walker |
| `aa110158408` | Material from other institutions |

**People records:** `cp37092` (Marc Isambard Brunel), `cp520` (Isambard Kingdom Brunel), `ap265` (Brunel, Isambard Kingdom), `ap24334` (Brunel, Marc Isambard), `cp32182` (Isambard Brunel), `cp28671` (Brunel University), `ap24964` (Wollaston, George Hyde), `ap25463` (Beamish, Richard).
Sitemap of all records: `https://s3-eu-west-1.amazonaws.com/smgco-sitemaps/sitemap.xml` (200 OK).

**Bottom line for the shield model (`co58317`): there is NO image and NO 3D model of the Thames Tunnel shield online. The user must model it from the documents/prints (all NC images) or from public-domain sources elsewhere.**

## A5. Bulk download routes

1. **Static JSON/CSV exports + one image zip** — `https://coimages.sciencemuseumgroup.org.uk/datasets/index.html` **[HIGH]**, "for **academic or personal research use** with attribution". Verified live `HTTP 200` headers:
   - `smg_object_records_with_CC_images_09_04_2025.json.zip` — 150,355 records, 145 MB
   - `smg_object_records_all_09_04_2025.json.zip` — 525,595 records, **322,807,536 bytes** (verified `content-type: application/zip`, `last-modified: 2025-04-28`)
   - `smg_document_records_with_CC_images_09_04_2025.json` — 7,017 records, 159.2 MB
   - `smg_document_records_all_09_04_2025.json` — 77,409 records, 560.8 MB
   - `smg_people_and_company_records_06_08_2025.json` — 23,684 records, 61.4 MB
   - CSVs: `smg_object_records_with_CC_images_09_04_2025.csv` (48.9 MB), `smg_object_records_all_09_04_2025.csv` (135.8 MB)
   - `smg_all_medium_thumbnail_images_09_04_2025.zip` — 1.19 GB, all `medium_thumbnail` images
   - Base for images: `https://coimages.sciencemuseumgroup.org.uk` + path from `multimedia[].@processed.*.location` (served from AmazonS3 via CloudFront — verified `server: AmazonS3`, `x-amz-server-side-encryption: AES256`).
2. **GitHub repo of collection data/code:** `https://github.com/TheScienceMuseum/collectionsonline` (+ `collectionsonline-api` examples). **[HIGH]**
3. **No S3 bucket for collection JSON.** The only S3 URL found is the **sitemap** bucket `s3-eu-west-1.amazonaws.com/smgco-sitemaps/`. **[HIGH]**
4. **No OAI-PMH endpoint.** `https://collection.sciencemuseumgroup.org.uk/oai` and `/api/oai` → **404**. **[HIGH]**

⚠️ The datasets page states the images in the bulk zip are the **same NC/OGL images** as online ("Each image referenced within the dataset has it's own copyright", example shows `"licence": "CC BY-NC-SA 4.0"`), and the whole page is scoped **"for academic or personal research use"**. INFERENCE: bulk download is **not** a route to commercially usable imagery.

## A6. API key, rate limits, robots.txt, harvesting restrictions

- **API key: NOT required.** The API is open ("Our API is open to all"). **[HIGH]**
- **Rate limiting is real and enforced. [HIGH]** A burst of ~10 requests produced `HTTP 429` with body exactly: **`Rate limited - please slow down`**. The datasets page confirms the cause: "in response to overly aggressive crawling we had to **heavily rate limit**" the API. No numeric limit is published. The usage page says: "We would also ask that requests to our API are **rate limited** and that you contact us at [email] before setting up any **significant daily exports or harvesting**".
- **`robots.txt` — `https://collection.sciencemuseumgroup.org.uk/robots.txt` (200 OK), verbatim: [HIGH]**
```
sitemap: https://s3-eu-west-1.amazonaws.com/smgco-sitemaps/sitemap.xml
User-agent: *
Crawl-Delay: 1
Disallow: /api/
Disallow: /iiif/
Disallow: /iris/
Disallow: /barcode/
Disallow: /*?*
User-agent: AhrefsBot
Disallow: /
```
  **This explicitly disallows `/api/` AND every URL containing `?` — i.e. the entire search API and all object JSON endpoints are Disallowed to crawlers, while the site's own docs tell you to use them.** Reconcile by treating the robots rules as the operator's stated wish: use the **bulk datasets** for volume, and keep interactive API calls few, slow, and with a truthful UA.
- **IIIF / Zoom harvesting is expressly forbidden. [HIGH]** Datasets page: "**Images must not be harvested from our IIIF and Zoom endpoints, we will block access and may act again anyone doing so.**" Nevertheless the endpoints are live and open: `https://zoom.sciencemuseumgroup.org.uk/iiif/3/52%2F199%2FMedal_to_commemorate_the_opening_of_the_Thames_Tunnel__1843.ptif/info.json` returns IIIF Image API **v3, profile level2, 3505×2481**, `extraQualities: [bitonal, color, gray]`, tiled 512; `…/full/max/0/default.jpg` returns 200. `access-control-allow-origin: *`, served by **Cantaloupe/6.0** behind Kong+CloudFront. **Technically open, contractually prohibited.** Do not use.
- **API format stability:** "we can not guarantee that it will remain unchanged over time and reserve the right to modify it without prior notice." **[HIGH]**

---

# B. EUROPEANA

⚠️ **Access note:** `pro.europeana.eu`, `www.europeana.eu` and `europeana.eu` are behind Cloudflare and returned `HTTP 403 "Just a moment…"` to every automated request (web_fetch and curl, multiple UAs). **All Europeana documentation below was therefore read from the Europeana Knowledge Base at `europeana.atlassian.net`, which is public and fetchable**, via `https://europeana.atlassian.net/wiki/rest/api/content/{pageId}?expand=body.storage`. The **API itself** (`api.europeana.eu`) is fully reachable. `rightsstatements.org` is reachable.

## B1. Rights statement vocabulary — what Europeana actually accepts

**Source: "Accepted rights statements and URIs", `https://europeana.atlassian.net/wiki/spaces/EF/pages/1503756289/Accepted+rights+statements+and+URIs` — version 36, last updated 2026-08-18. [HIGH]**

> "Data providers may choose between **14 standardised rights statements**, which fall into three groups: **Six Creative Commons licences**, **Two Creative Commons tools**, **Six out of the twelve Rights Statements by the Rights Statements Consortium**."

**Group 1 — 6 Creative Commons licences** (URI pattern `http://creativecommons.org/licenses/{licence-properties}/{version}/{port}/`; versions 1.0–4.0 accepted, **4.0 recommended)**:

| Licence | URI (4.0) | Commercial? |
|---|---|---|
| CC BY | `http://creativecommons.org/licenses/by/4.0/` | **YES** |
| CC BY-SA | `http://creativecommons.org/licenses/by-sa/4.0/` | **YES** (derivatives must be SA) |
| CC BY-ND | `http://creativecommons.org/licenses/by-nd/4.0/` | **YES, but no alterations** |
| CC BY-NC | `http://creativecommons.org/licenses/by-nc/4.0/` | NO |
| CC BY-NC-SA | `http://creativecommons.org/licenses/by-nc-sa/4.0/` | NO |
| CC BY-NC-ND | `http://creativecommons.org/licenses/by-nc-nd/4.0/` | NO |

Europeana's own verbatim one-liners: CC BY "lets others distribute, remix, tweak, and build upon the licensed work, **even commercially**"; CC BY-SA "…**even for commercial purposes**… and licence their adaptations of the work under the same terms"; CC BY-ND "lets others redistribute the work and make **commercial** and non-commercial use of it **as long as no alteration is made**"; CC BY-NC / CC BY-NC-SA — non-commercial only; CC BY-NC-ND — "the most restrictive… users cannot change the work in any way or use it commercially".

**Group 2 — 2 Creative Commons public domain tools** (pattern `http://creativecommons.org/publicdomain/{tool}/1.0/`):

| Tool | URI | Notes |
|---|---|---|
| **CC0** | `http://creativecommons.org/publicdomain/zero/1.0/` | "used to **waive all the rights** in a digital object… all possible existing rights in the content and the digital object are waived, and they can be used by anyone **without any restrictions**" |
| **Public Domain Mark (PDM)** | `http://creativecommons.org/publicdomain/mark/1.0/` | "applied to content that is **no longer protected by copyright, worldwide**… can be used by anyone without any restrictions" |

**Public Domain vs CC0 — the distinction Europeana draws. [HIGH]** PDM = the work was *never/ no longer* in copyright; CC0 = copyright *exists* (or may exist, including in the digitisation) and the rightsholder **actively waives** it. Operationally both are unrestricted for reuse. Europeana's 3D guidance adds: "the **CC0** should be used for 3D material in which copyright exists and for which the rightsholder has agreed to waive the rights", while "If **no copyright exists** in the underlying object, one of the 'public domain options' should be used. That is: the Creative Commons **Public Domain Mark**, or the Rights Statement with the 'no copyright' indication".

**Group 3 — 6 of the 12 RightsStatements.org statements** (pattern `http://rightsstatements.org/vocab/{id}/1.0/`), with Europeana's stated meaning **[HIGH]**:
| Statement | URI | Commercial? |
|---|---|---|
| No Copyright – Non-Commercial Use Only | `http://rightsstatements.org/vocab/NoC-NC/1.0/` | **NO** — public-domain work digitised under a public-private partnership whose contract limits commercial use for a period |
| No Copyright – Other Known Legal Restrictions | `http://rightsstatements.org/vocab/NoC-OKLR/1.0/` | **NO** — public domain but subject to known **legal** restrictions other than copyright |
| In Copyright | `http://rightsstatements.org/vocab/InC/1.0/` | **NO** — "any re-use is subject to additional permission from the rightsholder(s)" |
| In Copyright – Educational Use Permitted | `http://rightsstatements.org/vocab/InC-EDU/1.0/` | **NO** — educational use only |
| In Copyright – EU Orphan Work | `http://rightsstatements.org/vocab/InC-OW-EU/1.0/` | **NO** |
| Copyright Not Evaluated | `http://rightsstatements.org/vocab/CNE/1.0/` | **NO** — status unknown; Europeana "discouraged" its use |
*(The other 6 exist at rightsstatements.org — InC-RUU, InC-NC, NoC-CR, NoC-US, UND, NKC — but **Europeana does not accept them**.)*

**RightsStatements.org itself:** `https://rightsstatements.org/en/` (200 OK) — "provides **12 standardized rights statements**". Full vocabulary list confirmed from the live sitemap: `InC`, `InC-OW-EU`, `InC-RUU`, `InC-NC`, `InC-EDU`, `NoC-US`, `NoC-OKLR`, `NoC-CR`, `NoC-NC`, `UND`, `CNE`, `NKC`. **[HIGH]** (Note: as of the live page, stewardship has moved to **Digital Scholar**; announcements dated 2026-04.)

**Live confirmation of what is actually in the corpus** — `https://api.europeana.eu/record/v2/search.json?wskey=api2demo&query=*:*&rows=0&facet=RIGHTS&profile=facets` (62,662,285 records) **[HIGH]**, top values:
`InC` 11,656,827 · `PDM` 10,920,833 · `CC0` 8,032,410 · `CC BY 4.0` 7,614,678 · `CC BY-NC-ND 4.0` 3,644,732 · `NoC-OKLR` 3,336,449 · `CC BY-SA 4.0` 3,104,200 · `CC BY-NC-SA 4.0` 3,030,510 · `NoC-NC` 2,789,586 · `CC BY 3.0` 1,763,694 · `InC-EDU` 1,722,117 · `CC BY-SA 3.0` 1,553,900 · `CC BY-NC 4.0` 1,120,689 · `CNE` 362,761 · `InC-OW-EU` 1,146.
**Commercial-safe share (PDM + CC0 + CC BY + CC BY-SA) ≈ 31.7 M of 62.7 M ≈ 51%.**

## B2. Europeana API — exact signature

**Base endpoints (verified live):**
- Search: `https://api.europeana.eu/record/v2/search.json` **[HIGH]**
- Record: `https://api.europeana.eu/record/v2/{EUROPEANA_ID}.json` — e.g. `https://api.europeana.eu/record/v2/736/item_6C4HHEPIENLL7RFGCYVBFM6JNY4USSDZ.json` **[HIGH]**
- OpenSearch RSS: `https://api.europeana.eu/record/opensearch.rss?searchTerms=TERMS&count=COUNT&startIndex=START` **[HIGH]**
- Console/Swagger: `https://api.europeana.eu/console/search`
- Also available: Entity API, IIIF API, Newspapers API, Annotation API, SPARQL, Thumbnail API, Recommendation API, User Set API.

**Source: "Search API Documentation", `https://europeana.atlassian.net/wiki/spaces/EF/pages/2385739812` — v30, 2026-02-11. [HIGH]**

**API key: REQUIRED, with three forms.**
1. **`X-Api-Key: [WSKEY]` header — the preferred method.** [HIGH]
2. **`?wskey=[WSKEY]` query parameter — "deprecated"** ("This was the preferred—and only—option until 2023, but it is now deprecated. We will provide a grace period… because public keys included in URLs can be easily exposed"). [HIGH]
3. **`Authorization: Bearer [JWT]`** via the Auth Service — "restricted to a selective number of API customers". Token endpoint `https://auth.europeana.eu/auth/realms/europeana/protocol/openid-connect/token`; OIDC config `https://auth.europeana.eu/auth/realms/europeana/.well-known/openid-configuration`. [HIGH]

**Verified behaviour 17 Sep 2026 [HIGH]:**
| Request | Result |
|---|---|
| No key | `HTTP 401` → `{"success":false,"error":"Unauthorized","message":"Invalid API key provided!","code":"invalid_apikey"}` |
| Bogus key | `HTTP 401` → `{"apikey":"bogus123","success":false,"error":"API key is invalid","message":"Please register for an API key","code":"401_key_invalid"}` |
| `wskey=api2demo` | `HTTP 200`, `success:true`, **`requestNumber: 999` on every call** |
⚠️ **`api2demo` is a public demo key and works today, but `requestNumber` is pinned at 999 — do not build a production pipeline on it. Get a real key.**

**How to get a key (28 May 2025 policy) — `https://europeana.atlassian.net/wiki/spaces/EF/pages/2462351393/Accessing+the+APIs` v20. [HIGH]**
- Registration moved into the Europeana website account area: create an account → top-right menu → **"Manage API keys"**. (Account page: `https://www.europeana.eu/en/create-and-use-a-europeana-account`; the historical landing page `https://pro.europeana.eu/get-api` is Cloudflare-blocked from here.)
- **Personal API key** — anyone; **one active key per account**; "usage limits are generous enough to support most testing and discovery use cases"; "The rate limits for personal keys have been **progressively reduced until April 2026** to give customers with service-level requirements sufficient time to transition to project keys". **[HIGH]**
- **Project API key** — for services/operational needs; multiple keys allowed; "**significantly higher usage limits**"; approval by the customer support team, target **1–5 working days**; research projects (e.g. PhD) can get a limited-validity project key. **[HIGH]**
- Support: `api@europeana.eu`.

**Rate limits — no published numbers. [HIGH]** Source: "Fair use policy & guidelines", `https://europeana.atlassian.net/wiki/spaces/EF/pages/2704146433`, v10 (2024-09-05):
> "Use of the API must be limited to a **reasonable number of concurrent requests**… Europeana **may specify a limit per type of request and/or accross all Europeana APIs**… In the event that you receive an **error response resulting from reaching the limit**… you must reduce the number of concurrent requests… The failture to comply with this policy may result in your **access key be temporarily blocked or even revoked**."
Documented HTTP codes: **200** OK, **401** auth failed, **429** "the application has reached its usage limit", **500** server error. **There is no published requests/day or requests/sec figure.** INFERENCE: budget from the 429, and for volume use the bulk routes below (which Europeana explicitly recommends for "a large amount of items").

**Query parameters (verbatim from the Search API doc) [HIGH]:**
`query` (required) · `qf` (Query Refinement, repeatable) · **`reusability`** = `open` | `restricted` | `permission` · `media` (bool) · `thumbnail` (bool) · `landingpage` (bool) · `colourpalette` · **`theme`** = `archaeology, art, fashion, industrial, manuscript, map, migration, music, nature, newspaper, photography, sport, ww1` · `sort` = `score, timestamp_created, timestamp_update, europeana_id, COMPLETENESS, is_fulltext, has_thumbnails, has_media`, `random`, `random_SEED` (+`asc`/`desc`) · `profile` (`rich`, `facets`, `params`, `standard`) · **`rows` (max 100, default 12)** · `start` (1-based) · `cursor` (deep paging; `cursor=*` to begin) · `callback` (JSONP).
Facets: `facet=FIELD&profile=facets`, with `f.FIELD.facet.limit` / `f.FIELD.facet.offset`.

**Parameters verified live 17 Sep 2026 [HIGH]** (`api.europeana.eu`, `wskey=api2demo`):
| Probe | Result |
|---|---|
| `query=*:*&reusability=open` | 33,382,295 |
| `query=*:*&reusability=permission` | 12,020,734 |
| `query=*:*&reusability=restricted` | 17,259,256 |
| `query=*:*&reusability=bogus` | **HTTP 200, `totalResults: 62,662,285` — the invalid value is SILENTLY IGNORED, returning everything.** ⚠️ Validate your enum client-side. |
| `qf=RIGHTS:"http://creativecommons.org/publicdomain/zero/1.0/"` | 8,032,410 — works |
| `facet=RIGHTS&query=*:*&rows=0&profile=facets` | works, returns the table in §B1 |
| `rows=101` | `itemsCount: 100`, **no error** — the cap is silently applied |

**Rights fields in a record [HIGH]:** `object.aggregations[].edmRights.def[]` and per-asset `object.aggregations[].webResources[].webResourceEdmRights.def[]`; also `proxies[].dcRights`. Every record also ships ready-made `textAttributionSnippet` / `htmlAttributionSnippet` strings — use these verbatim for on-screen attribution.

**Metadata licence — CRITICAL. [HIGH]** "API FAQ", `https://europeana.atlassian.net/wiki/spaces/EF/pages/2360508417` v12:
> "**All metadata from Europeana's APIs are provided as CC0**, meaning you can reuse that metadata as you wish without any restrictions. Some of that metadata may link to content from Europeana's partners, like the content linked in the `edm:IsShownBy` and `edm:Object` fields. **These objects can be used in accordance with the Rights Statement mentioned in the object metadata, in the `europeana:rights`/`edm:rights` field. Always check these fields before using the objects**."
API terms of use = **points 8–18** of `https://www.europeana.eu/rights/terms-of-use` — **UNVERIFIED** (Cloudflare-blocked from this environment).

## B3. Europeana 3D — what it is, viewers, downloadability

**Source: "Publishing guide for 3D content", `https://europeana.atlassian.net/wiki/spaces/EF/pages/2365227031/Publishing+guide+for+3D+content` (full text retrieved). [HIGH]**

- **Europeana does NOT host 3D files. Verbatim: "Can Europeana host 3D files? — No. Some national aggregators have solutions if you are unable to host content yourself." [HIGH]**
- **Viewers — no "Europeana 3D viewer" product exists. Europeana embeds third-party viewers via oEmbed. Verbatim:** `edm:isShownBy` should be "a link to a webpage where the 3D object can be displayed and which can be mapped to an oEmbed URL. Europeana currently supports links to **Sketchfab** or the **WEAVE viewer** when they are provided as one of the following URL patterns:
  `https://sketchfab.com/3d-models/*` · `https://sketchfab.com/models/*` · `https://sketchfab.com/show/*` · `https://weave-3dviewer.com/asset/*`
  … If you have your own viewer, you can request your oEmbed-compliant viewer to be added to the internal registry… Please send a message to the **3D service desk**."
  The **EDM guidelines v40 (2026-05-08)** additionally show an **"Eureka3D Viewer"** in its Step-1 example, and live records now use **`https://3d.repox.io/api/oembed?url=…`** — so the supported set has grown beyond the two named. **3D Hop appears NOWHERE. [HIGH]**
- **EDM mapping:** `edm:type = '3D'`; direct link to an STL/GLB in `edm:isShownBy` is allowed but "**Europeana website does not yet support the display of 3D objects when `edm:isShownBy` is a direct link to a 3D file**"; `edm:hasView` for alternates; `dcterms:isFormatOf` links model↔view; `edm:intendedUsage` (mandatory for Tier 2); `schema:digitalSourceType` (`digitalCapture` / `dataDrivenMedia` / `digitalCreation`); `dc:type` from the controlled model vocabulary (`3DMesh`, `3DPointCloud`, `BIM`, `parametricModel`, `3DGaussianSplatting` at `http://data.europeana.eu/vocabulary/modelType/…`) with `edm:vertexCount` / `edm:polygonCount` / `edm:pointCount` / `edm:gaussianCount`. Formats seen in the wild: DAE, PLY, WRL, GLTF, OBJ, STL, NXS(NXZ), DICOM, IFC, USDZ. **"For 3D records, 3D PDF files are not sufficient and should not be submitted to Europeana."**
- **Is 3D downloadable/reusable?** Europeana's own advice: "Prioritise using **CC0, PDM**, or any of the rights statements or licences that permit reuse". Users needing to reuse "need to be able to **download the 3D files**… shape files, textures, metadata and paradata". Whether a download exists is determined by the *provider*, not Europeana — check `edm:rights` on the record and then the host (Sketchfab `isDownloadable`, Zenodo, the aggregator). **[HIGH on guidance; MED on any given record]**

**"Europeana Sculpture" pilot — UNVERIFIED.** No such pilot exists in the Europeana Knowledge Base (confluence search for `sculpture` returned only EDM definition PDFs and unrelated user-research pages), in Europeana PRO, or in web search. The real, documented 3D programmes are: **"Twin it! 3D for Europe's culture"** (a Europeana campaign/exhibition, Parts I–II — `https://pro.europeana.eu/page/twin-it-3d-for-europe-s-culture`, blocked here but indexed; story page `https://www.europeana.eu/en/stories/twin-it-3d-for-europes-culture`), **EUreka3D**, **Share3D**, **CARARE**, and the older **3D-ICONS**. INFERENCE: "Europeana Sculpture" is a conflation.

**Live 3D scale and rights (17 Sep 2026) [HIGH]:**
- `qf=TYPE:"3D"` → **13,474** records (of 62.66 M; TYPE facet: IMAGE 36,308,825 · TEXT 24,706,206 · SOUND 1,244,629 · VIDEO 389,151 · 3D 13,474).
- `qf=TYPE:"3D"&reusability=open` → **4,904** records.
- 3D RIGHTS facet: `CC BY 4.0` 3072 · `CC BY-NC 4.0` 2465 · `CC BY-NC-ND 4.0` 2004 · `CC BY-NC-SA 4.0` 1149 · `InC` 1116 · `CC BY-NC-ND 3.0` 979 · `CC BY-SA 4.0` 808 · `InC-EDU` 760 · **`CC0` 639** · **`PDM` 385** · `NoC-NC` 47 · `CC BY-ND 4.0` 42 · `CNE` 3 · `InC-OW-EU` 3 · `NoC-OKLR` 2. → **commercial-safe 3D ≈ 4,906 records (CC BY + BY-SA + CC0 + PDM).**
- Indicative open 3D records: `/1538/shm_media_9e68a753_…` "3D Model of the Vendel XIV Helmet" (Swedish History Museum, `CC BY 4.0`, Sketchfab oEmbed) · `/1599/share3d_0dd00181_…` "Valentino Castle (Turin) – Noble residential floor" (Polytechnic University of Turin via CARARE, `CC BY 4.0`, **direct `.glb` on Zenodo** via `3d.repox.io` oEmbed) · `/2048707/A_0_9_10739_3D` (Polytechnic University of Milan, **`CC0`**) · `/181/share3d_1152` "Pashley Sarcophagus" (Fitzwilliam Museum, `CC BY 4.0`).

## B4. Engineering / industrial / transport content — example records

`theme=industrial` + `reusability=open` works. Verified live counts and records **[HIGH]**:

| Query | totalResults | Example record (title · rights · dataProvider · URL) |
|---|---|---|
| `query=steam engine&reusability=open&theme=industrial` | 190 | "Steam Engine Brewery" · **PDM** · European Heritage Awards Archive · `/945/EUROPEANHERITAGEAWARDSXARCHIVEXEUX0X614858` |
| `query=bridge&reusability=open&theme=industrial` | 4,373 | "Brooklyn Bridge" · **PDM** · Deutsche Fotothek · `/440/item_PNQQGMRM4VYDTDJGTFXBSHGIPL73OK4X` |
| `query=dock OR harbour&reusability=open&theme=industrial` | 2,226 | "Harbour mill" · **CC BY-SA 4.0** · Deutsche Fotothek · `/463/item_UWW2APU4BU5TI2QXZHTE56FFW76UAOWU` |
| `query=colliery OR mine&reusability=open&theme=industrial` | 5,477 | "Etched print … Pemberton Main Colliery (Monkwearmouth Colliery)" · **CC BY-SA 4.0** · Newcastle University · `/590/providedCHO_gb186_thp_TH_1_41` |
| `query=railway/locomotive&reusability=open&theme=industrial` | 15,061 | "Järnväg / Railway" · **PDM** · Jamtli · `/76/jlm_item_128115` |
| `query=tunnel&reusability=open&theme=industrial` | 278 | "Der Themse-Tunnel / The Thames tunnel" · **PDM** · City Museum Berlin · `/736/item_6C4HHEPIENLL7RFGCYVBFM6JNY4USSDZ` |

**Thames Tunnel records in Europeana — full `q="thames tunnel"` result set (24 records) [HIGH]:**
| Title | Rights | Data provider | URL |
|---|---|---|---|
| **Der Themse-Tunnel / The Thames tunnel** | **PDM** (`http://creativecommons.org/publicdomain/mark/1.0/`) | City Museum Berlin (Stiftung Stadtmuseum Berlin) | `https://www.europeana.eu/item/736/item_6C4HHEPIENLL7RFGCYVBFM6JNY4USSDZ` |
| Thames Tunnel paper | **NoC-NC** | National Library of Scotland | `/91/_Resource_186897243` |
| The Thames tunnel | **InC** | Bodleian Libraries, Oxford | `/9200143/BibliographicResource_2000069499559` |
| Messingmedaille, 1846, Thames Tunnel | **CC BY-NC-ND 4.0** | Vienna Museum of Science and Technology | `/1457/https___id_kulturpool_at_b0cb6dfd_ed29_41a6_89e3_5f2afcf95014_cho` |
| A perspective view of the Thames and the Thames Tunnel, History of the Thames Tunnel | **CC BY-NC-SA 4.0** | Royal Museums Greenwich | `/2022362/_Royal_Museums_Greenwich__http___collections_rmg_co_uk_collections_objects_6563` |
| Counter commemorating the Thames tunnel and Trafalgar Square Memorial | **CC BY-NC-SA 4.0** | Royal Museums Greenwich | `/2022362/_Royal_Museums_Greenwich__…_objects_38933` |
→ **Only the City Museum Berlin image is commercially usable.** Note: `q=brunel` in Europeana is dominated by the botanist **Brunel** (Phyllanthus spp.) and a Portuguese tailor — **no Brunel-the-engineer material surfaced**. The `brunel` search is effectively useless for this episode.

## B5. Europeana Publishing Framework — tiers A–D and commercial reuse

**Content tiers** — source: "Content & Metadata Tiers" `…/pages/2059829253`, "ContentTier 1: 3D type" `…/pages/2059796518` (v32, 2025-11-14), "ContentTier 2-4: 3D type" `…/pages/3270115340` (v4, 2026-03-17). **[HIGH]**

The Framework has **two parallel ladders**: **Content tiers 1–4** (quality of the digital object) and **Metadata tiers A–C** (richness of the record).

| Content tier | Meaning | 3D requirements | Rights required |
|---|---|---|---|
| **1** | Europeana as a **search engine** — audience views the object on your site | working `edm:isShownAt` with a 3D viewer or link; thumbnail (`edm:object`); **no** other media resources | **any** accepted rights statement |
| **2** | Europeana as a **showcase** | Tier 1 + oEmbed-compliant viewer link + `edm:intendedUsage` | **any** accepted rights statement |
| **3** | Europeana as a **distribution platform for NON-COMMERCIAL reuse** — "Your collections could be used in **non-commercial** websites, apps, and services." | Tier 2 + direct link to a **supported model file** + `dc:type` (+ technical metadata) | **CC BY-NC, CC BY-ND, CC BY-NC-ND, CC BY-NC-SA, NoC-OKLR, NoC-NC, InC-EDU** |
| **4** | Europeana as a **free reuse platform** — "Your collections could be used in **commercial and non-commercial** websites, apps, services, and products." | Tier 3 | **PDM, CC0, CC BY, CC BY-SA** only |

Metadata **tier A** = "find the specific object I'm looking for"; **B** = "browse and explore"; **C** = "search and browse in a more precise way, by named authors, specific subjects or topics" — C adds reuse in education/research/creative-industries partnerships. Metadata tier A–C is orthogonal to the right to reuse; the **rights statement is what gates commerce**.

**Commercial-reuse rule, stated plainly:** for 3D, **Tier 4 (PDM / CC0 / CC BY / CC BY-SA) is the only tier that permits commercial reuse.** Tiers 1–2 permit no reuse at all (they are display-only); Tier 3 is explicitly non-commercial. The Framework is a *publishing* framework for data partners — for a downstream reuser it reduces to: **read `edm:rights` and check it is PDM / CC0 / CC BY / CC BY-SA.**

## B6. Bulk routes (if the channel ever needs scale)

Source: "Dataset download and OAI-PMH service", `https://europeana.atlassian.net/wiki/spaces/EF/pages/2324463617` v9. **[HIGH]**
- **FTP:** `ftp://download.europeana.eu/dataset/` — user `anonymous`, blank password, port 21. Subdirectories `XML` (RDF-XML) and `TTL` (Turtle). One ZIP per dataset, named by dataset id (e.g. `2021672.zip`), each with an `.md5sum`. **Regenerated weekly, Sunday evening.** `wget -m ftp://download.europeana.eu/dataset/XML`
- **OAI-PMH** for incremental harvesting.
- To find a record's dataset, facet the Search API on **`edm_datasetName`**.

---

# C. BOTTOM LINE — usable on a monetised Instagram channel WITHOUT legal review

## A. Science Museum Group

**✅ USABLE, no legal review needed**
1. **Collection metadata** — `title`, `made`, `maker`, `details` = **CC0**; `description` and all other text = **CC BY 4.0**. Both permit commercial use. Attribute: **`© The Board of Trustees of the Science Museum`** + link `https://collection.sciencemuseumgroup.org.uk`. Source: API usage page + datasets page. **[HIGH]**
2. **Factual research from the collection** — object IDs, dates, maker names, accession numbers, the existence and titles of the Brunel/Thames Tunnel archive (`aa110066849`, `aa110066849`, `co58317`, etc.). This is CC0/CC BY metadata. **[HIGH]**
3. **The 8 CC0 Sketchfab models** (see §A3 for the list) — `CC0 Public Domain`, downloadable. Commercially usable, no attribution required. **[HIGH]**
4. **The SMG Journal text** (`journal.sciencemuseum.ac.uk`) under **CC BY 3.0** — commercially usable with citation. **Not** its images (those are CC BY-NC). **[HIGH]**
5. **Deep-linking / "link out"** — pointing viewers to `collection.sciencemuseumgroup.org.uk` object pages. No licence needed; this is also what SMG wants ("referrals to your website"). **[HIGH]**

**❌ NOT USABLE without a licence (or a legal review)**
1. **All SMG collection images.** They are `CC BY-NC-SA 4.0`, `CC BY-NC-ND 4.0`, or unlicensed third-party (e.g. `co8013336`'s `copyright: "T Blood"`). **A monetised Reels channel is squarely "commercial" under SMG's own bullet list** ("use that promotes a product or service that is commercial"; "use on personal social media accounts, **provided the individual is not promoting themselves commercially**"). Ad revenue + sponsorships + self-promotion = commercial. **Route for a licence: Science & Society Picture Library, `https://www.scienceandsociety.co.uk/`.** **[HIGH]**
2. **The bulk datasets and the 1.19 GB image zip** — expressly "for **academic or personal research** use" and the images are NC anyway. Use them for *research*, not for episode assets. **[HIGH]**
3. **IIIF / Zoom endpoints** — expressly prohibited: "Images must not be harvested from our IIIF and Zoom endpoints, we will block access and may act again anyone doing so." **[HIGH]**
4. **`Stephenson's Rocket`** Sketchfab model — `CC Attribution-NonCommercial`. Tempting for episode content on Brunel; **not** usable. Same for the other 33 CC BY-NC models. **[HIGH]**
5. **`lab.sciencemuseum.org.uk`** — host is broken (Cloudflare Error 1000); nothing to use, and its 3D content is NC. **[HIGH]**

**⚠️ Named risk:** `co58317` — *the* Thames Tunnel shield model — has **no image and no 3D scan**. Every usable-looking Thames Tunnel image in the SMG collection is NC. For Episode 1's hero asset the creator must **model the shield in Blender from the archive documents** (the document *titles and descriptions* are CC0/CC BY — you may describe them and link to them; you may not show the images without a licence).

**Actionable, no-review path for SMG:** API/bulk = metadata only → script and citations. Blender geometry = built by the creator. Imagery = licensed from SSPL, or substituted from a commercial-safe source (see Europeana below).

## B. Europeana

**✅ USABLE, no legal review needed**
1. **All Europeana API metadata = CC0.** "you can reuse that metadata as you wish without any restrictions." Titles, descriptions, dates, provider names, Europeana IDs, and the ready-made attribution snippets. **[HIGH]**
2. **Records with `edm:rights` ∈ {`PDM`, `CC0`, `CC BY`, `CC BY-SA`}`** — full commercial reuse of the linked object, subject to the licence's attribution/share-alike terms. Filter with `reusability=open` **and** `qf=RIGHTS:"<uri>"`. ≈ **31.7 M records**, and ≈ **4,906** of the 13,474 3D records. **[HIGH]**
3. **The Thames Tunnel PDM image** — `https://www.europeana.eu/item/736/item_6C4HHEPIENLL7RFGCVBFM6JNY4USSDZ` (City Museum Berlin, "Der Themse-Tunnel", PDM, 1000px via `sammlung-online.stadtmuseum.de`). **The single clear commercial-safe Thames Tunnel asset found in either source.** **[HIGH]**
4. **Engineering/industrial imagery** filtered as above — bridges, docks, collieries, railways, steam engines; large PDM/CC BY pools (see §B4 table). **[HIGH]**
5. **Commercial-safe 3D** (4,906 open 3D records) — download the file from the host (Zenodo `.glb`, Sketchfab download, aggregator) under the stated PDM/CC0/CC BY/CC BY-SA licence. e.g. Valentino Castle / Turin 1911 pavilions `.glb` point clouds on Zenodo via CARARE. **[HIGH]**
6. **Europeana metadata for script research and for on-screen attribution strings** — use `textAttributionSnippet` verbatim. **[HIGH]**

**❌ NOT USABLE without a licence or legal review**
1. **`InC`, `InC-EDU`, `InC-OW-EU`, `CNE`** — all rights reserved / unknown / education-only. **No commercial use.** (3,336,449 `NoC-OKLR` records are also off-limits for a different reason: other legal restrictions, not copyright.) **[HIGH]**
2. **`NoC-NC` and `NoC-OKLR`** — explicitly non-commercial / legal restriction attached. **[HIGH]**
3. **Every `-NC-` and `-NC-ND` / `-ND` Creative Commons licence.** CC BY-ND permits commercial use **but forbids alterations** — **INFERENCE:** compositing a CC BY-ND still into a 9:16 video with crops, pans, overlays or colour grading is very likely an adaptation and therefore outside the licence; treat CC BY-ND (261,722 IMAGE records corpus-wide, 42 in 3D) as **not usable** for video without review. Plain video *display* of an unmodified, uncropped CC BY-ND image is defensible but is not worth the risk on a monetised channel.
4. **Europeana as a *source* of files** — Europeana does not host 3D (or most media). A rights statement on the Europeana record does not guarantee the file is still online or downloadable; you must check the host. **[HIGH]**
5. **`www.europeana.eu` / `pro.europeana.eu` page content** (editorial/story text, images) — **not** covered by the "API metadata = CC0" statement, and those hosts could not be fetched here to read their terms. **UNVERIFIED** — do not reuse Europeana's own editorial pages or their images.

**⚠️ Operational cautions (not legal, but blocking)**
- `reusability` silently ignores invalid values and returns **everything** — a typo will give you InC records. Validate client-side and re-check `edm:rights` per record.
- `api2demo` works but `requestNumber` is frozen at 999 — get a real key (Personal keys now have reduced limits and **Project keys** are the path for anything sustained; approval 1–5 working days).
- No published rate limit; 429 is the signal; the Fair Use policy explicitly warns of key suspension. For volume use the **FTP dataset dump** (`ftp://download.europeana.eu/dataset/`, weekly on Sunday) or **OAI-PMH**.
- `www.europeana.eu` and `pro.europeana.eu` are Cloudflare-walled to automation — plan to read them manually in a browser.
- SMG robots.txt disallows `/api/` and `/*?*`; the SMG API 429s quickly; the API contract is explicitly unfixed. Prefer the bulk JSON dumps for SMG.

## One-line verdict
**SMG gives you legally clean *research metadata* and almost nothing else for a monetised video** — all its imagery and its one relevant 3D model are NonCommercial, and the Episode-1 hero object (the shield, `co58317`) has no image or scan at all. **Europeana gives you a genuinely commercial-safe pool**: CC0 metadata plus ~31.7 M PDM/CC0/CC BY/CC BY-SA objects (~4,906 with 3D geometry), including exactly one public-domain Thames Tunnel image — filter hard on `edm:rights`, build the shield geometry yourself in Blender, and put your licence/attribution line in the episode description.
