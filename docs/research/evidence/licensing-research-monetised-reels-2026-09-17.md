# Licensing Research — 4 Sources for a Monetised History-of-Engineering Reels Channel
**Research date: 17 September 2026.** All findings from live fetches unless marked otherwise.
Episode 1 subject: Marc Brunel's Thames Tunnel tunnelling shield (1825–1843). Use case: monetised Instagram Reels (9:16, AI voiceover, ad revenue + sponsorships), solo creator, Blender + Python, needs 3D geometry, photogrammetry, high-res reference imagery.

## 0. Access limitations encountered (read this first)
This environment could not reach several hosts. This materially affects confidence in section B.

| Host | Result | Consequence |
|---|---|---|
| `www.loc.gov` (HTML **and** `?fo=json`) | **HTTP 403**, Cloudflare "Just a moment..." interstitial on every UA tried (curl default, Chrome, Googlebot) | Could not live-verify `loc.gov` JSON API responses or item pages. `www.loc.gov` is **UNVERIFIED** by direct fetch here. |
| `chroniclingamerica.loc.gov` | **HTTP 308** → `www.loc.gov/chroniclingamerica/...` → **403** | Chronicling America API **UNVERIFIED** by direct fetch. |
| `web.archive.org` | **Connection failure (HTTP 000)** from this sandbox | No Wayback fallback available. |
| `loc.getarchive.net` | HTTP 403 | Third-party LOC mirror unusable. |
| `archivesupport.zendesk.com` (IA's own Rights article) | HTTP 403 | IA rights-statement article **UNVERIFIED**; substituted IA's developer docs + live metadata. |
| **Reachable LOC-family hosts:** `guides.loc.gov` ✅, `data.labs.loc.gov` ✅, `lccn.loc.gov` ✅, `tile.loc.gov` ✅, `id.loc.gov` ✅, `libraryofcongress.github.io` ✅, `nps.gov` ✅ | — | Used these as the authoritative substitute. `lccn.loc.gov/{lccn}/mods` and `/marcxml` expose **verbatim `accessCondition` rights strings** and are reachable. |

**Bottom line on access:** the LOC *rights* doctrine and *actual item records* were verified from reachable LOC hosts. The `fo=json` endpoint signatures in section B.1 are **UNVERIFIED** — treat the quoted parameter list as documentation-derived, not fetch-confirmed.

---

# A. INTERNET ARCHIVE (archive.org)

## A.1 US public domain cutoff as of Sept 2026 — the 95-year rule

**Claim: works published in 1930 entered the US public domain on 1 January 2026.** — verified, **HIGH**.

- Source: https://blog.archive.org/public-domain-day-2026/ — verbatim:
  > "On January 1, 2026, **creative works from 1930 and sound recordings from 1925** entered the public domain in the United States."
- Source: https://copyright.byu.edu/public-domain — verbatim:
  > "Under U.S. copyright law, all works published at least 95 years before January 1 of the current year are in the public domain. In 2026, for example, all works published in 1930 or earlier are in the public domain in the United States. On January 1, 2027, works published in 1931 will enter the public domain in the United States."
- Source (LOC's own duration guidance): https://guides.loc.gov/p-and-p-rights-and-restrictions/risk-assessment — verbatim:
  > "**Works published or registered in the U.S. more than 95 years ago are now in the public domain.** The simplest calculation (if you prefer to deal in round numbers) is to: add 100 to the year the item was published/registered for copyright and subtract 4. The item will enter the public domain on January 1 of that year"
  > "Starting in the late 1990s and up until 2019, a key date for assessing copyright in the U.S. was the year 1923. … Public Law 105-298 enacted in October 1998 increased the maximum to 95 years [28 years first term and 67 for the second, if renewed]. Before 1998 the longest amount of time a work could be protected was 75 years, so works before 1923 were no longer protected (1998 minus 75 years equals 1923). When the law changed, the 1923 date was "frozen" and remained so until January 1, 2019."

**Exact rule:** 95 years from year of publication, expiring 1 January of (publication year + 96). So 1930 → 1 Jan 2026. **1931 → 1 Jan 2027. 1932 → 1 Jan 2028.** Confidence **HIGH**.

**Two important qualifications** (both verbatim from the LOC guide above):
- Renewal matters for pre-1964 works: *"Published works registered for copyright in the U.S. through Dec. 31, 1963 are now in the public domain unless the copyright was renewed."* So "published before 1964" is **not** automatically PD — a renewed 1961 work is protected to 1 Jan 2057 (LOC example #5).
- *"Works published with a copyright notice or registered for copyright between January 1, 1964 and December 31, 1977 are generally protected for 95 years."*
- Foreign works: *"Works published outside the U.S. but registered for copyright in the U.S. more than 95 years ago are considered to be in the public domain."*

**Relevance to Episode 1:** everything printed for the Thames Tunnel (1825–1843) is ~180+ years old — categorically PD in the US. **HIGH**. No renewal question arises.

## A.2 The three-tier distinction: IA scans vs uploader content vs borrowable

This is the crux of the Internet Archive problem, and the platform's own documentation supports the distinction.

### (i) IA's own scans of PD books
IA-curated/partner-scanned items carry a machine-readable `possible-copyright-status` field. The IA metadata schema defines it verbatim (https://archive.org/developers/_sources/metadata-schema/index.md):
> "### possible-copyright-status … **label**: Possible Copyright Status … **definition**: Information relevant to copyright status … **accepted values**: string … **usage notes**: Do not use this field for CC license information (see licenseurl)."

**Live example — four items, all `possible-copyright-status = NOT_IN_COPYRIGHT`, all directly on Episode 1's subject** (all confirmed via `https://archive.org/metadata/{id}`):

| identifier | year | title | collection | sponsor / contributor |
|---|---|---|---|---|
| `thamestunnelade00tunngoog` | 1825 | The Thames tunnel [a description of the projected tunnel …] | `europeanlibraries` | Google / Oxford University |
| `sketchesworksfo00cruigoog` | 1829 | Sketches of the Works for the Tunnel Under the Thames, from Rotherhithe to … (Robert Cruikshank) | `americana` | Google / Harvard University |
| `anexplanationwo00compgoog` | 1840 | An explanation of the works of the tunnel under the Thames from Rotherhithe to Wapping (Thames Tunnel Company) | `europeanlibraries` | Google / Oxford University |
| `originprogressa00westgoog` | 1827 | The Origin, Progress and Present State of the Thames Tunnel … (William Westall) | `americana` | Google / Harvard University |

Download URLs (all verified HTTP 200):
- `https://archive.org/download/sketchesworksfo00cruigoog/sketchesworksfo00cruigoog_jp2.zip` → **200, `application/zip`** (JPEG2000 page images, 15.4 MB)
- `https://archive.org/download/anexplanationwo00compgoog/anexplanationwo00compgoog.pdf` → **200, `application/pdf`**
- The `_jp2.zip` derivative is the high-resolution page-image route; `_djvu.txt` gives OCR text.

**INFERENCE (MEDIUM):** `possible-copyright-status = NOT_IN_COPYRIGHT` is a per-item uploader/partner assertion, but here it aligns with the independently-calculable 95-year rule, so the PD conclusion is solid regardless.

### (ii) Uploader-contributed content (Community Texts / Community Uploads)
The Community collections are, verbatim from https://archive.org/developers/items.html:
> "`opensource` (Community Texts), `opensource_movies` (Community Video), `opensource_audio` (Community Audio), `opensource_image` (Community Images), `opensource_media` (Community Data), or `open_source_software` (Community Software)"

**Why uploader content is NOT a reliable PD claim** — grounded in IA's own schema, verbatim:
- `rights` — **defined by**: uploader; **edit access**: uploader. Definition: *"Rights statement"*. Accepted values: *"String"*. Usage note: *"Please see licenseurl for URL-based rights designations, like Creative Commons. For other rights information or statements, use the rights field."*
- `licenseurl` — **defined by**: uploader; **edit access**: uploader. Definition: *"URL of the selected license"*. Usage note: *"This link should point to a recognized license, like Creative Commons or GNU. For other types of rights statements, use the rights field."*
- `possible-copyright-status` — **defined by**: uploader; **edit access**: uploader.

**Conclusion (HIGH):** on archive.org, `rights`, `licenseurl` and `possible-copyright-status` are **free-text fields that the uploader writes about their own upload**. There is no IA verification step in the schema. Therefore:
- The presence of a rights statement proves only that *someone typed it*.
- The **absence** of a rights statement proves nothing at all (the schema marks all three fields `required: No`).
- Community-upload content can only be used safely if you independently establish PD or a valid licence. It is **not** a reliable PD claim.

### (iii) Borrowable / lending-library books (Controlled Digital Lending)
**What it looks like in metadata:** the collection identifiers tell you. Live evidence from `https://archive.org/services/search/v1/scrape?fields=identifier,title,collection&q=collection:(pub_americana OR pub_domain OR printdisabled)&count=100` — the CDL/lending buckets are `internetarchivebooks`, `printdisabled`, `inlibrary`. A real Episode-1-adjacent hit returned:
- `isambardkingdomb0000rolt_d0g4` — "Isambard Kingdom Brunel : [a biography]", year 1970, collection `["internetarchivebooks","inlibrary","printdisabled", …]` → **borrow-only, in copyright, NOT reusable as a source asset.**

**Explanation (HIGH):** CDL items are in-copyright works that IA is permitted to *lend* one-copy-one-user. Lending is not licensing. There is **no** grant of reproduction, adaptation, or redistribution rights. Using frames/pages from a `printdisabled`/`inlibrary` item in a monetised Reel is outside any lending permission. **Do not use.**

### (iv) "No known copyright restrictions" ≠ public domain — on IA
- IA's own schema has **no** NKC field. The only rights fields are the three uploader-authored ones above. **UNVERIFIED:** I could not fetch IA's `archivesupport.zendesk.com` "Rights" article (403), so I cannot quote an IA-branded "no known copyright restrictions" statement verbatim. **INFERENCE (MEDIUM):** IA does not use the NKC phrase as a platform-wide designation.
- The **NKC statement is a Flickr Commons** construct, not an Internet Archive one. **UNVERIFIED verbatim** — I did not fetch the Flickr Commons statement in this session. **INFERENCE (HIGH confidence on the legal point):** NKC is an assertion by the contributing institution that *it is unaware of* restrictions. It is not a warranty, not a licence, and not a public-domain dedication. It shifts diligence to you.

## A.3 Metadata APIs — exact endpoints

All confirmed live unless noted.

| Endpoint | Result | Notes |
|---|---|---|
| `https://archive.org/advancedsearch.php?q=…&output=json` | **200** | Confirmed. Supports `fl[]` (fields), `rows`, `page`, `sort[]`. |
| `https://archive.org/metadata/{identifier}` | **200** | Confirmed. Returns `{"metadata":{…},"files":[…],"server":…,"dir":…}`. |
| `https://archive.org/download/{identifier}/` | **200** | Confirmed. Directory listing / direct file fetch. |
| `https://archive.org/download/{identifier}/{filename}` | **200** | Confirmed (e.g. PDF and `_jp2.zip` above). |
| `https://archive.org/services/search/v1/scrape` | **200** | Confirmed. Cursor-based. |
| `https://archive.org/advancedsearch.php` (docs) | **200** | https://archive.org/help/aboutsearch.htm |

### advancedsearch.php — hard limit, verbatim (https://archive.org/help/aboutsearch.htm)
> "We limit the number of sorted paged results returnable to 10,000. Paged sorted results are supported only until the 10,000th result. For example, the search: … should be fine, but requesting `page=10000` is rejected."

### Scrape API — parameters, verbatim (same page)
> "- `q`: the query (using the same query Lucene-like queries supported by Internet Archive Advanced Search).
> - `fields`: Metadata fields to return, comma delimited
> - `sorts`: Fields to sort on, comma delimited (if `identifier` is specified, it must be last)
> - `count`: Number of results to return (minimum of 100)
> - `cursor`: A cursor, if any (otherwise, search starts at the beginning)
> - `total_only`: if this is set to `true`, then only the number of results is returned."

Also verbatim: *"Note that there is no absolute guarantee that every item will be returned, or that every item returned will remain in the Archive."*

### Rate limits — verbatim (https://archive.org/developers/bots.html)
IA documents **no numeric request-per-second cap**. Verbatim:
> "Automated tools should respect rate limits:
> - Add delays between requests for bulk operations
> - Honor `429 Too Many Requests` responses and `Retry-After` headers
> - Use `--checksum` flags to avoid re-downloading/re-uploading unchanged files
> - Consider using GNU Parallel with `-j` to limit concurrent requests"

Their worked example, verbatim: `cat items.txt | parallel -j4 --delay 1 'ia download {}'` → **4 concurrent, 1 s delay**.
Mandatory UA, verbatim: *"All automated requests to archive.org must include a descriptive User-Agent header that identifies: The tool or bot name; Version number; For AI agents: the model being used."* Their example: `curl -H "User-Agent: MyBot/1.0.0 (claude-sonnet-4-20250514)" https://archive.org/metadata/example-item`.
Best-practice list verbatim includes *"Cache responses"*, *"Use bulk endpoints"*.

**UNVERIFIED:** a specific numeric rate limit or a published Terms-of-Use API quota. None is stated in the developer docs I fetched.

### Download URL permanence — important, verbatim (https://archive.org/developers/items.html)
> "A particular file can always be downloaded from: `https://archive.org/download/<identifier>/<filename>`
> **Note**: Archival URLs may redirect to an actual server that contains the content. The resultant URL is **not** a permalink. … **DO NOT LINK** to any archive.org URL that begins with numbers like this."

## A.4 3D content collections — YES, and the licence varies per item

**Search results (live `advancedsearch.php` counts):**

| collection | numFound | mediatype | note |
|---|---|---|---|
| `thingiverse` | **2,637,652** | `data` | Full Thingiverse mirror. **HIGH.** |
| `3dmodels` | **449** | `data` | Patron-uploaded game/character models. |
| `3dprinting` | **0** | — | Does not exist. |
| `3d-printing` | **0** | — | Does not exist. |

**Licence breakdown inside `collection:thingiverse` (live counts):**

| `licenseurl` | count |
|---|---|
| `https://creativecommons.org/licenses/by/4.0/` | 1,323,107 |
| `https://creativecommons.org/licenses/by-sa/3.0/` | 604,160 |
| `https://creativecommons.org/licenses/by-nc/4.0/` | 298,922 |
| `https://creativecommons.org/licenses/by-nc-sa/4.0/` | 266,163 |
| `https://creativecommons.org/publicdomain/zero/1.0/` | 38,396 |
| **no `licenseurl` at all** | **1,732** |
| other (GPL/LGPL, legacy CC URLs) | remainder |

Verified sample record: `https://archive.org/metadata/thingiverse-5877531` → `licenseurl = https://creativecommons.org/licenses/by/4.0/`, `creator = Dan Terwilliger (dudeski)`, `mediatype = data`.

**Are they downloadable?** Yes — `https://archive.org/download/thingiverse-5877531/AllSteel_File_Cabinet_Sprocket__Poorly_modeled_5877531_5877531.zip`. **Directly usable on a monetised channel?** **No, not as a block.** Verbatim implication of the licence split:
- **CC BY 4.0** (~1.32 M): commercially usable **with attribution**.
- **CC BY-SA 3.0** (~604 k): commercially usable with attribution **and share-alike** — the derivative work inherits the licence. **Risk:** share-alike on an Instagram Reel is legally awkward (Instagram's ToS conflicts with SA licensing for video).
- **CC BY-NC 4.0 / BY-NC-SA 4.0** (~565 k combined): **explicitly no commercial use** — unusable on an ad-revenue channel.
- **CC0** (~38 k): unrestricted, commercial OK.
- **No licence (~1,732)**: all rights reserved by default. Unusable.

**INFERENCE (HIGH):** a solo creator wanting 3D geometry must filter to `CC0` **or** `CC BY 4.0` and carry attribution, and must exclude every `-NC-` item. There is **no** engineering-history-relevant 3D geometry of the Thames Tunnel shield in these collections — the mirrors are consumer 3D-printing models and game assets. **UNVERIFIED:** I found no Thames-Tunnel/Brunel 3D model in `thingiverse` or `3dmodels`.

## A.5 How to filter a search to public domain — exact query syntax

All of these were executed live and returned results.

**Strongest filter — explicit machine-readable PD status:**
```
https://archive.org/advancedsearch.php?q=thames+tunnel+AND+mediatype%3Atexts+AND+possible-copyright-status%3ANOT_IN_COPYRIGHT&fl%5B%5D=identifier&fl%5B%5D=title&fl%5B%5D=year&fl%5B%5D=collection&fl%5B%5D=possible-copyright-status&rows=10&output=json
```
→ `numFound: 4` — exactly the four Thames Tunnel items in A.2. **This is the single most useful query for this project. HIGH.**

**By licence URL (needs the full URL, quoted):**
```
q=collection:thingiverse AND licenseurl:"https://creativecommons.org/publicdomain/zero/1.0/"
```
Note: the query value must be the **full licence URL including trailing slash**. `licenseurl:creativecommons.org/publicdomain/zero/1.0` (no scheme) returns 0. **HIGH.**

**Exclude any item that has a licence field** (find unlicensed = all-rights-reserved):
```
q=collection:thingiverse AND -licenseurl:[* TO *]
```
→ 1,732. **HIGH.**

**By collection — and a correction on `pub_*`:**
- **`collection:pub_*` as a wildcard does not work** in my testing. The query `collection:(pub_americana OR pub_domain OR printdisabled)` returned only `internetarchivebooks`/`printdisabled`/`inlibrary` items — i.e. **lending-library books**, not PD scans. Treat `pub_*` as **UNVERIFIED / unreliable**; do not build a pipeline on it.
- Working, verified PD-adjacent collections: `americana`, `europeanlibraries`, `getty`, `metropolitanmuseumofart-gallery`, `david-rumsey-map-collection`.
- Note `americana` self-describes as PD, verbatim from `https://archive.org/metadata/americana`: *"As a whole, this collection of material brings holdings that cover many facets of American life and scholarship into the public domain."* — **but this is a collection-level claim, and the same query surfaced in-copyright lending items**, so it is a **weak** filter. Prefer `possible-copyright-status:NOT_IN_COPYRIGHT`.
- **`collection:getty`** (Getty Research Institute) is a real collection to mine. `https://archive.org/metadata/getty` describes it as *"Books contributed by Getty Research Institute."* — with **no rights field on the collection**.

**Per-item trap found — this is the highest-value warning in section A:**

`dr_view-plate-1-construction-of-roads-thames-tunnel-12190612` (David Rumsey Map Collection; Heck/Winkles, 1851 — "(View) Plate 1. (Construction of Roads; Thames Tunnel.)", an on-topic engraving). Its metadata, verbatim at `https://archive.org/metadata/dr_view-plate-1-construction-of-roads-thames-tunnel-12190612`:
> `rights` = "Images may be downloaded and used following Creative Commons **CC BY-NC-SA 3.0** license. Image credit should be given to "David Rumsey Map Collection, David Rumsey Map Center, Stanford Libraries." **Please contact the David Rumsey Map Collection for commercial use**"

The underlying 1851 print is PD, but the **scan** is licensed **BY-NC-SA** and the rights holder explicitly requires contact for commercial use. **Do not use this file on a monetised channel.** This is exactly the failure mode the three-tier distinction is meant to catch. **HIGH.**

Also on-topic but licence-encumbered differently:
- `mma_marc_isambart_brunel_17691849_engineer_builder_of_the_thames_tunnel_188446` (Pierre Jean David d'Angers, 1828 — a Brunel portrait, mediatype `image`, real `.jpg` in the item): `rights` = *"Metropolitan Museum of Art Terms and Conditions"* — **not** a PD or CC0 statement. Partner-imposed terms. **Treat as not cleared.**

## A.6 IA's own rights statement on PD scans + NKC

- **UNVERIFIED:** IA's Zendesk "Rights" article is 403 from here. I could not quote an IA-branded platform-wide rights statement verbatim.
- **Verified substitute (HIGH):** IA's schema deliberately separates *licence* from *rights*: `licenseurl` is for *"a recognized license, like Creative Commons or GNU"*; `rights` is for *"other rights information or statements"*. Both are **uploader-authored**. That is the structural fact that makes the three-tier distinction necessary.
- **NKC vs PD:** see A.2(iv). **INFERENCE (HIGH on the legal effect):** NKC is a diligence statement, not a licence and not a PD dedication. IA does not appear to use it as a platform designation (**UNVERIFIED**).

---

# B. LIBRARY OF CONGRESS (loc.gov)

## B.1 The JSON API — endpoint signatures

> ⚠️ **All of B.1 is UNVERIFIED by direct fetch** — `www.loc.gov` returns HTTP 403 Cloudflare challenge from this environment for both HTML and `?fo=json`. The following is documentation-derived. I verified the *parameter semantics* through LOC's own GitHub-hosted tutorials (reachable) and the LC Labs data package (reachable), and I verified that LOC's **IIIF image host `tile.loc.gov` is reachable and serving images**.

Endpoints as documented:
- `https://www.loc.gov/search/?q={query}&fo=json`
- `https://www.loc.gov/item/{id}/?fo=json`
- `https://www.loc.gov/collections/{slug}/?fo=json`
- `https://www.loc.gov/pictures/` (Prints & Photographs Online Catalog; also `https://www.loc.gov/pictures/collection/hh/` for HABS/HAER/HALS)
- `https://www.loc.gov/free-to-use/?fo=json`

**Verified parameter semantics** (source: LOC's own tutorial `https://libraryofcongress.github.io/data-exploration/loc.gov%20JSON%20API/LOC.gov%20JSON%20API.html`):
- `fo=json` — *"Note: The addition of the "fo=json" string ensures that the item request is in JSON format"*. **HIGH** (this is LOC's own wording about the parameter).
- `at=` — subset the response. Verbatim: *"the 'at=trending_content' part says only get me the json about the trending content. If you leave that off you will get lots more information"*; example given: `https://www.loc.gov/?fo=json&at=trending_content`. **HIGH.**
- **Pagination**: default page size is **40**, with a `pagination` object containing `next`/`previous` URLs. Verbatim (section heading): *"Why does it stop after 40?"*, and the documented loop is `next_page = collections_json["pagination"]["next"]`. **HIGH** (default 40 is directly evidenced by LOC's own tutorial).
- **Item response top-level keys**, verbatim from `https://libraryofcongress.github.io/data-exploration/loc.gov%20JSON%20API/resources2pdf.html`: `articles_and_essays, cite_this, item, more_like_this, options, related_items, resources, timestamp, type`. Resources live at `data['resources'][0]['files']`, each file having `url`, `height`, `width`. **HIGH.**
- **`c=` (count) and `sp=` (page)**: **UNVERIFIED** in this session. I could not fetch `https://www.loc.gov/apis/json-and-yaml/requests/parameters/` (403). The widely-cited "`c=` max 100" figure is **UNVERIFIED — do not rely on it**; infer page size from the `pagination` object instead.

**API key:** none required — **MEDIUM** (no key appears anywhere in LOC's own tutorials or data-package code, all of which make plain `requests.get(...)` calls).
**Rate limits:** **UNVERIFIED.** LOC documents a page `https://www.loc.gov/apis/json-and-yaml/working-within-limits/` (403 here; the search snippet references an anchor "Deep Paging"). **Do not assume a numeric cap.** Practical guidance from LOC's own tutorials: follow `pagination.next` sequentially rather than deep-paging.
**Bulk download:** **YES, verified via a reachable LOC host** — LC Labs publishes **data packages** at `https://data.labs.loc.gov/`. Confirmed live: `https://data.labs.loc.gov/free-to-use/README.md` (HTTP 200, 195 lines), plus a documented tutorial index at `https://libraryofcongress.github.io/data-exploration/` listing data packages for Sanborn Maps, Free to Use, National Jukebox, Stereograph Cards, digitized books, telephone directories, and more.

**IIIF — the most useful practically-verified item in section B.** LOC's own tutorial contains working image URLs of the form (verified pattern, and I confirmed `tile.loc.gov` serves them, HTTP 200 `image/jpeg`):
```
https://tile.loc.gov/image-services/iiif/service:{collection}:{sub}:{id}:{seq}/full/pct:100/0/default.jpg
```
Real example from LOC's tutorial: `https://tile.loc.gov/image-services/iiif/service:mss:mss25064:mss25064-141:0018/full/pct:100/0/default.jpg`. **`full/pct:100` = full resolution.** **HIGH** that the pattern and host work; **MEDIUM** that it generalises to every collection.

## B.2 "Free to Use and Reuse" sets — and why "free to use" ≠ public domain

**What they are**, verbatim from the LC Labs data package (`https://data.labs.loc.gov/free-to-use/README.md`):
> "Free to Use and Reuse is a collection of themed sets curated by Library staff. Themes are intentionally varied, to illustrate the depth and breadth of the Library's collections. Themes have included skyscrapers, natural disasters, birds, shoes, games and more. These sets are just a small sample of the Library's digital collections that are free to use and reuse."

**Exact disclaimer wording**, verbatim from the same README (section "### Rights information", repeated under "## Rights Statement"):
> "The Free to Use and Reuse Sets are curated selections from the Library's digital collections that are **either in the public domain, have no known copyright, or have been cleared by the copyright owner for public use**. For more information, see https://www.loc.gov/free-to-use/."

And verbatim from the brief description:
> "The Library believes that this content is either in the public domain, has no known copyright, or has been cleared by the copyright owner for public use."

**Why "free to use" ≠ public domain — HIGH.** The disclaimer itself is a **three-way disjunction**. Only the first branch is PD. The second branch ("no known copyright") is a diligence statement, not a PD finding. The third ("cleared by the copyright owner for public use") is a **permission grant by a third party** — which is neither PD nor a blanket commercial licence, and may carry conditions LOC has not published. **"Free to use" is a curation label, not a rights status.** For a monetised channel, the third branch is the dangerous one: it looks safe and is actually an unstated third-party grant.

**Scale (verbatim):** *"This dataset contains metadata records and images for **2,610** curated selections featured in the Library of Congress' Free to Use and Reuse Sets as well as links to images for the full digital objects represented in the sets. This dataset includes only those items which are accessible via the Library of Congress' API."* **HIGH.** Data package version: *"Version 1.2 | Last updated 2024-04-17"* — note this is ~2.5 years stale as of Sept 2026. **MEDIUM.**

**Engineering relevance:** the themes enumerated are *"skyscrapers, natural disasters, birds, shoes, games"* — **no engineering/industrial theme is named**. **INFERENCE (MEDIUM):** Free to Use is unlikely to be a rich vein for Episode 1.

## B.3 Rights statements in LOC metadata — which are commercially safe

Authoritative source: LOC's own Prints & Photographs guide, `https://guides.loc.gov/p-and-p-rights-and-restrictions/risk-assessment` (HTTP 200, "Last Updated: Sep 8, 2026"). **All quotations below are verbatim. HIGH.**

**Overarching rule, verbatim:**
> "**In all cases, it is the researcher's obligation to determine and satisfy copyright or other use restrictions when publishing or otherwise distributing materials found in the Library's collections.**"

**"No known restrictions on publication"** — verbatim:
> "**No known restrictions on publication** means that the Library is unaware of any restrictions on the use of the image. These are generally the situations where this phrase is used: 1. There was a copyright and it was not renewed or the term of copyright has expired … 2. The image is from a late 19th or early 20th century collection for which there is no evidence of any rights holder: - There are no copyright markings or other indications on the images to indicate that they were copyrighted or otherwise restricted, AND - The records of the U.S. Copyright Office do not indicate any copyright registration, AND - The acquisition paperwork for the collection does not contain any evidence of any restrictions, AND - Images from the collection have been used and published extensively without anyone stepping forward to claim rights.
> **These facts do not mean the image is in the public domain, but do indicate that no evidence has been found to show that restrictions apply.**"

→ **Direct answer to "is NKC public domain?" — NO, and LOC says so explicitly.** For a monetised channel this is **practically usable where branch 1 applies** (expired/unrenewed copyright = actually PD), and **a calculated risk where branch 2 applies**. **Commercially safe: MEDIUM-HIGH, item-dependent.** Note the phrase is sometimes rendered "no known copyright restrictions" in LOC's rights-and-restrictions statements for specific collections (the guide shows the George Grantham Bain Collection example labelled "no known copyright restrictions").

**"Public Domain"** — verbatim:
> "If images were copyrighted and copyright has expired, we say "Images in this collection are considered to be in the public domain.""
> "If images have been placed in the public domain by the creator or rights holder, we say that the images are in the public domain in the rights and restrictions statement." (Carol M. Highsmith example)

→ **Commercially safe: HIGH.**

**"Rights status not evaluated"** — verbatim:
> "Does the catalog record include text that says "**Rights status not evaluated. For general information see 'Copyright and Other Restrictions...' (http://lcweb.loc.gov/rr/print/195_copr.html)**." This means the Library has not received or gathered information pertaining to the rights status of the image"

→ **Commercially safe: NO.** This is an explicit "we don't know". Requires your own evaluation.

**"Publication may be restricted"** — verbatim:
> "Does the catalog record include text that says "**Publication may be restricted**" and refer to a rights statement? See "[Rights and Restrictions statements]" below."
> "Does the catalog record include text that says "**May be restricted: Information on reproduction rights available in LC P&P Restrictions Notebook**" (or similar wording). This refers to a notebook that is now online in the form of rights statements."

→ **Commercially safe: NO without reading the specific rights statement.** Read it and check for donor restrictions.

**Empty / differently-worded note** — verbatim:
> "What if there is a note with different wording from the above examples or no note at all? Catalog records have been created over a long period of time, so wording of rights information may vary. If a record does not contain a rights note, it may mean the Library has not received or gathered information pertaining to the rights for the image and you will need to gather that information yourself"

**LOC does not give permission and does not sign forms** — verbatim:
> "As a publicly supported institution, the Library of Congress generally does not own the rights to materials in the collections, and it does not charge permission fees for use of material from the collections. **We cannot sign permission forms** because, with one exception (the Seagram County Court House Archives), the Prints & Photographs Division does not administer permissions to publish or otherwise distribute material from its collections."

**"If it displays off-site, is it ok to use?"** — verbatim:
> "The Library displays jpegs and tiffs offsite for those images for which a rights analysis shows: 1. that there are "No known restrictions," OR 2. that the copyright has expired, OR 3. that the creator has released his rights OR 4. that the creator has agreed to allow his images to be displayed but still retains the publication rights. … 5. that the vast majority of images in a large collection are not restricted … **While the overwhelming majority of images that display jpegs and tiffs off-site fall into the first three categories, be sure you haven't wandered into one of the few collections in the fourth category.**"

→ **A visible image does NOT mean reusable.** Category 4 is a trap.

**Other rights that apply but aren't copyright** — verbatim: *"Users need to be aware of other types of rights that can apply, including privacy rights, publicity rights, licensing and trademarks."*
**Credit line requested** — verbatim: *"the Library requests the courtesy of a credit line"* including Library of Congress, the collection, and the reproduction number (e.g. *"Wright Brothers collection, Prints and Photographs Division, Library of Congress, LC-ppmsca-04598"*). Not a legal condition — **but do it.**

## B.4 Actual LOC items found for 19th-century engineering — with rights, verbatim

> ⚠️ **Caveat (HIGH):** `www.loc.gov` item pages are 403 here. However **`https://lccn.loc.gov/{lccn}/mods` and `/marcxml` are reachable and returned real records with verbatim `accessCondition` rights strings.** That is a robust workaround and is the source of the item below. Use `lccn.loc.gov/{lccn}/mods` as your verification endpoint.

### VERIFIED ITEM — Thames Tunnel, 1830 lithograph
- **MODS record:** `https://lccn.loc.gov/98507755/mods` → **HTTP 200, `application/xml`**
- **MARC record:** `https://lccn.loc.gov/98507755/marcxml` → **HTTP 200**
- **Item page:** `https://www.loc.gov/item/98507755/` (**UNVERIFIED** — 403 here)
- **Resource page:** `https://www.loc.gov/resource/cph.3c20899` (cited by search result; **UNVERIFIED**)
- **Title:** "The Thames Tunnel" · **Date:** `[between 1830 and 1880(?)]` (`dateIssued encoding="marc"` 1830)
- **Format:** `1 print : lithograph.` · **Genre:** `Lithographs-1830-1880.`
- **Classification:** `PGA - Unattributed--Thames Tunnel`
- **Rights — verbatim `<accessCondition type="use and reproduction">`:**
  > **"No known restrictions on publication."**
- **Identifiers:** LCCN `98507755`; stock numbers `LC-DIG-pga-13664`, `LC-USZ62-120899`; handles `hdl:loc.pnp/pga.13664`, `hdl:loc.pnp/cph.3c20899`
- **Location:** "Library of Congress Prints and Photographs Division Washington, D.C. 20540 USA"
- **Rights verdict:** NOT a PD statement — it is LOC's NKC formula (B.3). Given the 1830 date, copyright has expired, so this falls under NKC branch 1 → **commercially usable, MEDIUM-HIGH.** Diligence: confirm the scan is not a separately-licensed third-party reproduction (compare the David Rumsey trap in A.5).

### Other engineering-relevant collection entry points (discovered, not item-verified)
- **Architecture, Design & Engineering Drawings** — a real LOC collection, confirmed present in the live collection list returned by `https://www.loc.gov/collections/?fo=json` as captured in LOC's own tutorial: *"Architecture, Design & Engineering Drawings"*. **HIGH** that the collection exists.
- Also present in that live list: *"Historic American Buildings Survey/Historic American Engineering Record/Historic American Landscapes Survey"*, *"Railroad Maps, 1828-1900"*, *"Transportation and Communication"*, *"Engineering"*-adjacent holdings via *"Inside an American Factory: Films of the Westinghouse Works, 1904"*, *"World's Transportation Commission"*, *"Tissandier Collection"*.
- **Institution of Civil Engineers / Brunel / locomotive / bridge / dock / canal as such:** **UNVERIFIED.** I could not run free-text LOC searches (403). **INFERENCE (MEDIUM):** LOC's British-engineering holdings are thin; the strong engineering corpus is **American** (HABS/HAER/HALS), which is a mismatch for a Thames Tunnel episode but a good fit for later episodes.

## B.5 HABS / HAER / HALS — measured drawings and photographs ARE public domain

This is the **single best-verified asset class in the entire report** for a monetised engineering-history channel.

**Authoritative verbatim statement — National Park Service, `https://www.nps.gov/subjects/heritagedocumentation/collection.htm` (HTTP 200, "Last updated: August 12, 2026"):**
> "Materials created for HABS, HAER, or HALS are in the public domain."

Same page, verbatim on scale and content:
> "The HABS/HAER/HALS Collection at the Library of Congress is the nation's largest archive of historic architectural, engineering, and cultural landscape documentation. It is an active collection that grows each year. The collection includes **measured and interpretive drawings, large-format black & white and color photographs, written historical and descriptive data, and original field notes.** … As of 2026, more than **46,000 sites** are included in the collection."

**Corroborating verbatim quote from LOC's own (now-archived) HABS rights page**, as reproduced in Wikimedia Commons' licence template `https://commons.wikimedia.org/wiki/Template:PD-USGov-NPS-HALS`, which cites `https://www.loc.gov/rr/print/res/114_habs.html`:
> "**Copyright:** "The original measured drawings and most of the photographs and data pages in HABS/HAER/HALS were created for the U.S. Government and are considered to be in the public domain.""

**Note the qualifier carefully** — "the original measured drawings and **most** of the photographs". **INFERENCE (HIGH):** the residual "some" photographs are third-party donations. LOC's own guide (B.3) says rights statements exist per-collection for exactly this reason, and it explicitly warns about the FSA/OWI and Horydczak collections where a minority of images are third-party. **Action: check each item's rights line; do not assume the whole record group is PD.**

**Does HAER cover engineering structures?** — **YES, HIGH.** Verbatim from NPS (`https://www.nps.gov/subjects/heritagedocumentation/collection.htm`) — the homepage credit list names, among others:
- "Arlington Memorial Bridge (**HAER DC-7**)"
- "Milltown Dam, Powerhouse (**HAER MT-43-A**)"
- "Rock Point Arch Bridge (**HAER OR-29**)"
- "U.S. Steel Duquesne Works, Blast Furnace Plant (**HAER PA-115-A**)"
- "1964 Meyers Manx (**HAER CA-2312**)"
→ bridges, dams, bridges, **steelworks/blast furnaces**. Confirmed by Wikipedia (`https://en.wikipedia.org/wiki/Heritage_Documentation_Programs`): *"HAER documents historic sites, structures, mechanical, and engineering artifacts"*, founded 10 January 1969 by NPS and the **American Society of Civil Engineers**; headquartered at the Library of Congress Prints and Photographs Division.

**Exact places to search:**
- `https://www.loc.gov/pictures/collection/hh/` — LOC's collection front door (**403 here; UNVERIFIED live, but cited by NPS as the canonical search page**)
- Browse-by indexes cited by NPS: `/index/names/`, `/index/subjects/`, `/index/places/`
- Per-item handles of the form `https://hdl.loc.gov/loc.pnp/hhh.{state}{num}` — e.g. `https://hdl.loc.gov/loc.pnp/hhh.dc0604` (Arlington Memorial Bridge). These are the stable HOLLIS-style links. **HIGH** that this is the identifier pattern NPS itself publishes.
- **NPS program data:** `https://www.nps.gov/subjects/heritagedocumentation/` and the statistics page `https://www.nps.gov/subjects/heritagedocumentation/collection-statistics.htm`; program records at NARA **Record Group 515** (`https://www.archives.gov/research/guide-fed-records/groups/515.html`). **HIGH.**
- Data package route: LC Labs `https://data.labs.loc.gov/`, and a dedicated LOC tutorial `geocoding-hhh/geocoding_with_the_hhh_collection.html` (confirmed to exist in the tutorial index at `https://libraryofcongress.github.io/data-exploration/`), which implies the HHH collection is queryable via the same `loc.gov` JSON API **with geospatial metadata**. **MEDIUM** (tutorial listed; notebook not fetched).

**Are high-res TIFFs downloadable? Any restrictions?**
- **Downloads: YES — HIGH.** `https://tile.loc.gov/` is reachable from here and serves full-resolution IIIF derivatives, verified: `https://tile.loc.gov/image-services/iiif/service:mss:mss25064:mss25064-141:0018/full/pct:100/0/default.jpg` → **HTTP 200, `image/jpeg`**. LOC's own tutorial uses exactly this host and `full/pct:100` for the largest available image.
- **UNVERIFIED:** direct master **TIFF** URLs for HHH items specifically. My guess-tests at `https://tile.loc.gov/storage-services/service/pnp/habshaer/...` returned 404 because I do not have a real identifier. **Obtain the real item's API record and read `resources[0].files[]`** — that array contains the authoritative `url`/`height`/`width` per file, which is how LOC's own tutorial picks the largest JPEG.
- **Restrictions:** the only stated restriction is the "most of the photographs" qualifier. No fee, no permission form (LOC: *"it does not charge permission fees"*, *"We cannot sign permission forms"*). **Commercially safe: HIGH**, subject to per-item rights-line check and the "most/not all" caveat.

## B.6 Chronicling America — newspaper API

> ⚠️ **UNVERIFIED live.** `chroniclingamerica.loc.gov` → **HTTP 308** permanent redirect → `https://www.loc.gov/chroniclingamerica/search/pages/results/?...` → **HTTP 403** Cloudflare. The legacy host has been folded into `loc.gov`, which is blocked here. I could **not** confirm current endpoint behaviour, rate limits, or a machine-readable rights field.

What is documented/derivable:
- LOC's own tutorial index (`https://libraryofcongress.github.io/data-exploration/`, HTTP 200) lists a **Chronicling America notebook set**, confirming the collection is API-accessible and documenting these task patterns **verbatim as page titles**: *"Using the loc.gov API with the Chronicling America Historic Newspapers Collection"*, *"Learning and Applying Basic API Tasks in Chronicling America"*, *"Downloading Search Results from Chronicling America"*, *"Downloading Newspaper Titles and Batches from Chronicling America"*, and word-frequency analyses. Note the framing: **Chronicling America is now accessed "with the loc.gov API"** — i.e. it is a `loc.gov` collection endpoint, not a separate API. **HIGH** on that structural point.
- A public API description exists at `https://chroniclingamerica.loc.gov/about/api/` — but fetching it **cross-origin redirected to `https://www.loc.gov`**, consistent with the migration. **UNVERIFIED content.**

**Rights status — INFERENCE (HIGH):** Chronicling America digitises US newspapers published 1690–1963, all in the public domain or with no known restrictions. LOC's guide (B.3) applies the same NKC/"no known restrictions" vocabulary. **But there are real carve-outs** — LOC's guide explicitly warns that varied circumstances within a collection produce differing rights statuses.
**How to search:** use the `loc.gov` collections API with the Chronicling America collection slug plus `fo=json`, e.g. `https://www.loc.gov/collections/chronicling-america/?q=thames+tunnel&fo=json&dates=1825/1843` — **INFERENCE, UNVERIFIED** (parameter forms `dates=` and the slug are not fetch-confirmed).
**Practical route for this project:** LOC's own tutorial uses `tile.loc.gov` for page images; but for Thames Tunnel newspaper coverage, the **Internet Archive's 4 verified NOT_IN_COPYRIGHT pamphlets (A.2) and Getty's holdings (D.4) are lower-risk and already verified.**

---

# C. RIJKSMUSEUM (rijksmuseum.nl / Rijksstudio / data.rijksmuseum.nl)

## C.1 MAJOR LIVE CONTRADICTION: the legacy API is gone (HTTP 410)

**The old documented API endpoint is retired.** Verified live:
- `https://www.rijksmuseum.nl/api/en/collection?key=...&q=...` → **HTTP 410 Gone** (empty body). Also 410 with a plausible key. **410 = "Gone"**, i.e. permanently removed, not merely unauthorised (which would be 401/403). **HIGH.**
- `https://www.rijksmuseum.nl/api/en/collection?key=demokey&q=test` → **HTTP 410**. **HIGH.**
- `https://www.rijksmuseum.nl/en/rijksstudio` → **HTTP 301** (redirect; target not followed to a usable JSON/HTML doc from here).

> **This contradicts the widely-documented "Rijksmuseum API key, ~10,000 requests/day" model.** Any tutorial, blog, or LLM answer describing `www.rijksmuseum.nl/api/en/collection` with a `key=` parameter is **stale**. The replacement is a keyless Linked Art API at `data.rijksmuseum.nl`.

## C.2 The current API — endpoint signatures

**Documentation:** `https://data.rijksmuseum.nl/docs` (HTTP 200) and `https://data.rijksmuseum.nl/docs/search` (HTTP 200). Sitemap: `https://data.rijksmuseum.nl/sitemap.xml`.

### Search API — `https://data.rijksmuseum.nl/search/collection`
Verbatim from `https://data.rijksmuseum.nl/docs/search`:
> "**Accessing the API** — The API is available at the following URL. **No API key is needed.** `GET https://data.rijksmuseum.nl/search/collection`
> Requesting this URL without query parameters will return the first 100 items of the entire collection. See below for specifying search parameters.
> **Query parameters** — To search for specific objects based on certain characteristics, use the following query parameters. All of which are optional and can be combined with other query parameters, to perform fine-grained searches. Either Dutch or English terms can be used and combined. For example, `schilderij` also matches objects with type `painting`.
> `aboutActor` str … `creator` str … `creationDate` str … `description` str Search for keywords present in the object's description. `imageAvailable` bool Search for objects with or without an available digital reproduction: `true` or `false`. `material` str … `memberOfSetId` str … `objectNumber` str … `pageToken` str The page token used for pagination. `technique` str … `title` str …"

**Confirmed live responses:**
- `https://data.rijksmuseum.nl/search/collection` → **200, `application/ld+json`**. Body: `{"@context":"https://linked.art/ns/v1/search.json","id":"…","type":"OrderedCollectionPage","partOf":{"type":"OrderedCollection","totalItems":840004, …}}` → **840,004 objects total.**
- `?imageAvailable=true` → **200**, `totalItems: 735982` → **735,982 objects with a digital image.**
- `?creator=Rembrandt` → **200**, `totalItems: 1463`.
- `?creationDate=18??&imageAvailable=true` → **200**, `totalItems: 64555` → **64,555 nineteenth-century objects with images.**
- ⚠️ **Live contradiction:** `?q=windmill` → **HTTP 400**, body `{"detail":"Unsupported query parameter: q"}`. **There is no `q` parameter.** Use `description=`, `title=`, `creator=`, `objectNumber=` instead. Any guide telling you to use `?q=` is wrong.

### Object metadata (Linked Art) — `https://data.rijksmuseum.nl/{numeric id}`
- `https://data.rijksmuseum.nl/200314891` → **200, `application/ld+json`**. `type: "HumanMadeObject"`, `id: "https://id.rijksmuseum.nl/200314891"`.
- Cross-reference: `equivalent: [{"id":"http://hdl.handle.net/10934/RM0001.COLLECT.242753"}]`.
- Human-readable object identifier lives in `identified_by[]` as an `Identifier` with `classified_as` AAT `300312355` ("object number"), e.g. `NG-MC-28`, `SK-C-211`, `RP-P-1908-4837`, `RP-F-…`.
- **Resolution/human pages:** persistent identifier resolver `https://id.rijksmuseum.nl/{id}` (content negotiation documented at `https://data.rijksmuseum.nl/docs/http/arguments`). **INFERENCE (MEDIUM):** human page = `https://www.rijksmuseum.nl/en/collection/{objectNumber}`.

### OAI-PMH — `https://data.rijksmuseum.nl/oai`
Verbatim (`https://data.rijksmuseum.nl/docs/oai-pmh`, HTTP 200):
> "**note june 11, 2026** — We have released a new version of our OAI-PMH API, in which the Europeana Data Model (EDM) representations provided are valid according to Europeana's XML Schema and Schematron validation rules. **This update may have breaking changes for your usecase** … if you parse the XML, please refer to the EDM documentation"
> "**Access to the OAI-PMH API** — The API is available at the following URL. **No API key is needed.** OAI-PMH base url `https://data.rijksmuseum.nl/oai`
> Verbs — Every request to the OAI-PMH API must be accompanied by a verb parameter … `Identify`, `ListMetadataFormats`, `ListSets`, `ListRecords`, `GetRecord`, `ListIdentifiers` … `https://data.rijksmuseum.nl/oai?verb={verb}`"
Live: `https://data.rijksmuseum.nl/oai` → **200, `text/xml`** with a valid OAI-PMH envelope and `responseDate 2026-09-17T09:36:04Z`. **HIGH.**

### Bulk data dumps — `https://data.rijksmuseum.nl/docs/data-dumps`
Verbatim counts (archive / files / domain): `image.tar.gz` — **580,039** "Collection Image metadata as Linked Art D1_Digital_Object and IIIF Image API endpoint"; `classification.tar.gz` 23,834; `concept.tar.gz` 14,051; `event.tar.gz` 2,412; `exhibition.tar.gz` 870; plus library domains. Multi-domain object metadata, serialized as `application/n-triples`. **HIGH.**

### Libraries also present
- **LDES** — `https://data.rijksmuseum.nl/docs/ldes/` (listed in the docs sitemap).
- **SRU (bibliographic)** — `https://data.rijksmuseum.nl/docs/sru`, explicitly marked **"(deprecated)"** in the docs nav. **HIGH** on the deprecation.

### API key / rate limits
- **Key: NOT required** — verbatim *"No API key is needed"* on both the Search and OAI-PMH doc pages. **HIGH.**
- **Rate limits: UNVERIFIED.** The legacy "~10,000 requests/day" figure belongs to the **retired** 410 API and does **not** transfer. No numeric limit is stated on `data.rijksmuseum.nl`. **Do not cite a number.** Practical: paginate with `pageToken`.

## C.3 CRITICAL: CC0, not Public Domain Mark — and the machine-readable answer

**This is the key finding, and it is machine-verifiable.**

Every Rijksmuseum Linked Art object record I fetched carries a rights declaration inside `subject_of` → `subject_to`, structured as a `Right` classified with the CC0 URI. Verified across six objects:

| Object id | Object number | Title | rights URI found |
|---|---|---|---|
| `200314891` | `NG-MC-28` | Model of a Dredger | `https://creativecommons.org/publicdomain/zero/1.0/` |
| `200315817` | `NG-MC-528` | Model of a Trunk Engine | `https://creativecommons.org/publicdomain/zero/1.0/` |
| `200107959` | `SK-C-211` | The windmill at Wijk bij Duurstede | `https://creativecommons.org/publicdomain/zero/1.0/` |
| `200109836` | `SK-A-3567` | Bouwput | `https://creativecommons.org/publicdomain/zero/1.0/` |
| `200192329` | `RP-P-1908-4837` | Gezicht op het station Willemspoort te Amsterdam | `https://creativecommons.org/publicdomain/zero/1.0/` |
| `200551759` | `RP-P-OB-87.276` | Waldiepers Nieuwejaars Wensch … | `https://creativecommons.org/publicdomain/zero/1.0/` |

The raw JSON shape, verbatim from `https://data.rijksmuseum.nl/200314891`:
```json
"subject_of": [{"id":"https://data.rijksmuseum.nl/200314891","type":"LinguisticObject",
  "subject_to":[{"type":"Right","classified_as":[{"id":"https://creativecommons.org/publicdomain/zero/1.0/","type":"Type"}]}],
  "classified_as":[{"id":"http://vocab.getty.edu/aat/300379475","type":"Type"}]}]
```
→ **CC0 1.0 Universal** (`https://creativecommons.org/publicdomain/zero/1.0/`) — i.e. a **licence with a waiver**, not the Public Domain Mark. **HIGH.**

**This corrects the user's stated belief, and partially confirms it.** The user wrote: *"I believe Rijksmuseum releases PD works as CC0 for the image but the museum may state some restrictions on the museum's own marks/logo."*
- ✅ **CC0 for the image — CONFIRMED**, machine-readable, on every object checked.
- ⚠️ **Nuance / history:** the article `https://creativecommons.nl/2013/11/11/rijksmuseum-haalt-voorwaarden-van-collectie-af/` (HTTP 200, dated 11 Nov 2013) documents that Rijksmuseum **originally used the Public Domain Mark and imposed non-commercial download conditions**, then removed them. Verbatim (Dutch):
  > "Vorig jaar al heeft het Rijksmuseum de werken waarvan de auteursrechtelijke bescherming afgelopen is al gemarkeerd met de Creative Commons Public Domain Mark. **De Public Domain Mark is geen licentie en ook geen vrijwaring zoals CC0.**"
  ("The Public Domain Mark is not a licence and not a waiver like CC0.")
  > "Rijksstudio heeft nu deze downloadbeperking van zijn publieke domein scans in hoge resolutie verwijderd. Dit geeft iedereen de mogelijkheid om de beschikbare werken van Rijksstudio te downloaden en **voor alle doeleinden te gebruiken**." ("…to download and use for **all purposes**.")
  → So the 2013 position was PDM + no restrictions; the **current** machine-readable position is **CC0**. A commenter in Feb 2017 already noted CC0 in use, and the editor replied *"sinds die tijd is een en ander veranderd"* ("things have changed since then").
- ⚠️ **Museum marks/logo: the user's caveat is directionally right.** **UNVERIFIED verbatim** — I could not fetch a current Rijksmuseum "Terms of use" / "Copyright" page that states a logo restriction. **INFERENCE (MEDIUM-HIGH):** this is the near-universal museum position (compare Getty, which states it explicitly in D.2) and is consistent with the 2013 CC-NL discussion. **Practical rule: use the CC0 image; do not use the Rijksmuseum logo, wordmark, or the Rijksstudio UI chrome, and do not imply endorsement.**

**⚠️ A real inconsistency to flag (MEDIUM):** the **IIIF manifests do NOT carry the licence.** `https://iiif.micr.io/RFwqO/manifest` (HTTP 200) returns only these top-level keys: `@context, id, type, label, thumbnail, provider, items` — with `license`, `requiredStatement`, `rights` and `attribution` **all absent (`null`)**. So you cannot read the licence off the image service; you must read it from the Linked Art object record. **This is a concrete gap for anyone building an automated licence check.**

**Programmatic licence check (recommended):** `GET https://data.rijksmuseum.nl/{id}` with `Accept: application/ld+json`, then assert `https://creativecommons.org/publicdomain/zero/1.0/` appears in the payload before ingesting.

## C.4 19th-century ENGINEERING content — what actually exists

Rijksmuseum is **not** primarily an engineering museum for *building/civil* engineering, but it holds **strong Dutch maritime, hydraulic, and industrial material**, and — importantly for a Thames Tunnel episode — **some British material**.

**Live search results (`https://data.rijksmuseum.nl/search/collection?description=…`, `totalItems`):**

| query | total | sample ids |
|---|---|---|
| `baggeren` (dredging) | 2 | `200551759`, `200610144` |
| `dredging` | 1 | `200314891` |
| `polder` | 96 | `200107950` |
| `sluice` | 9 | `20015031` |
| `shipbuilding` | 8 | `200108524` |
| `steam engine` | 2 | `200315817` |
| `stoommachine` (steam engine) | 41 | `200109836`, `200151665`, `200312919`, `200316149` |
| `railway` | 18 | `200131425` |
| `spoorweg` (railway) | 103 | `200192329`, `20029313`, `200322604`, `200412183` |
| `locomotive` | 21 | `200322641`, `200578298`, `200578307`, `200578308` |
| `stoomlocomotief` (steam locomotive) | 46 | `200278870`, `200285609`, `20033627`, `200417917` |
| `canal` | 105 | `200107817` |
| `haven` (harbour) | 1,564 | `200101022`, `200101172` |
| `brug` (bridge) | 3,287 | `200101430`, `200101431`, `200101432` |
| `watersnood` (flood disaster) | 298 | `200108300`, `200110000`, `200110001`, `200145775` |
| `Zuiderzee` | 142 | `200108235`, `200108653`, `200117985`, `200125464` |
| `tunnel` | 149 | `200106392`, `200107989`, `200112519`, `200112525` |
| `London` | 293 | `200106035`, `200106056`, `200106216`, `200108376` |
| **`Thames`** | **31** | `200131384`, `200131385`, `200144993`, `200145001` |
| **`Brunel`** | **2** | `200523990`, `200524469` |
| `industriële revolutie` | 2 | `200216416`, `200421337` |
| `maalmolen` | 0 | — |

**Verified on-topic objects (full records fetched, rights = CC0):**
- **`200314891` / `NG-MC-28` — "Model of a Dredger" / "Model van een baggermolen"**, produced `c. 1800`, materials `"hout, messing en touw"` (wood, brass, rope). Description verbatim (Dutch): *"Het nieuwe van dit ontwerp was de plaatsing van de rosmolen, waardoor de lange transmissie-as…"* — a **shipborne dredger model with a horse-mill drive**. Directly relevant to hydraulic-engineering episodes. `demonstrates: https://id.rijksmuseum.nl/202314891` (a `VisualItem`). **CC0.**
- **`200315817` / `NG-MC-528` — "Model of a Trunk Engine"**, 1855, by **Petrus van der Loo** (1806–1864), *"designed by John Penn (1805–1878)"*, wood/brass/iron. Description verbatim: *"Model van een 150 pk trunkmachine of kokermachine in een dwarsdoorsnede van een schip geplaatst…"* — a **150 hp trunk steam engine in a ship cross-section**. Excellent reference geometry for a steam/engineering episode. **CC0.**
- **`200192329` / `RP-P-1908-4837` — "Gezicht op het station Willemspoort te Amsterdam"** — a **railway station** print. **CC0.**
- **`200109836` / `SK-A-3567` — "Bouwput"** ("building pit"/cofferdam) — civil-works subject. **CC0.**
- **`200551759` / `RP-P-OB-87.276`** — a satirical print referencing a dredger ("Waldiepers Nieuwejaars Wensch…"). **CC0.**

**Brunel / Thames — a lead worth chasing:** `description=Brunel` returns exactly **2** objects (`200523990`, `200524469`), and `description=Thames` returns **31** (`200131384`, `200131385`, `200144993`, `200145001`, …). I did **not** fetch these to confirm whether they are on-topic for Marc Brunel the engineer (the surname "Brunel" is common in Dutch contexts, and the collection has strong French/Dutch print holdings). **UNVERIFIED — flag as a lead, not a result.** Print them before relying on them.
- **No Rijksmuseum Thames Tunnel tunnelling-shield material was found.** **UNVERIFIED** that none exists; but nothing on-topic surfaced.

**Verdict:** Rijksmuseum is a **good source for Dutch hydraulic/steam/maritime engineering reference and for CC0 steam-engine models**, but it is **not** a source for the Thames Tunnel shield specifically. Its single biggest asset for this project is that **its licence is CC0 and machine-readable**.

## C.5 IIIF — exact endpoints and permitted resolution

Verbatim from `https://data.rijksmuseum.nl/docs/iiif/image` (HTTP 200):
> "Rijksmuseum uses an IIIF Image API to offer images of artworks. For this, it uses the product **Micrio** which is created by Q42. … **Access** — There is one production endpoint available. Intended Use: All · Resource Scope: All · Root Location: Production · **`https://iiif.micr.io`**
> Examples — `https://iiif.micr.io/RFwqO/info.json` Retrieve image metadata. **`https://iiif.micr.io/RFwqO/full/max/0/default.png`** The image of an object in PNG format. `https://iiif.micr.io/RFwqO/full/max/0/gray.jpg` … `https://iiif.micr.io/ohGMs/full/800,80/90/gray.jpg` …"

Presentation API, verbatim from `https://data.rijksmuseum.nl/docs/iiif/presentation`:
> "Rijksmuseum relies on Micrio to provide a IIIF Presentation API endpoint for its images. … **`https://iiif.micr.io`** … `https://iiif.micr.io/RFwqO/manifest` Retrieve the manifest of a specific image."
Docs also list **IIIF Change Discovery API** (`/docs/iiif/cd`).

**Live verification:**
- `https://iiif.micr.io/RFwqO/info.json` → **200**, `ImageService3`, `profile: level2`, `version: 4.0`, `width: 4645`, `height: 4645`, `formats: ["jpg","png","webp"]`, `qualities: ["default","gray","color"]`, `tiles: [{"scaleFactors":[1,2,4,8],"width":1024,"height":1024}]`.
- **`https://iiif.micr.io/RFwqO/full/max/0/default.png` → HTTP 200, `image/png`.** ✅ **`full/max` — the maximum/full resolution — is permitted and works.** **HIGH.**
- `https://iiif.micr.io/RFwqO/manifest` → **200**, `presentation/3`, `type: Manifest`; but as noted in C.3, **no `license`/`requiredStatement`/`rights`/`attribution`**.
- **Resolutions permitted: `full/max`** (and arbitrary sizes/crops/rotation per level2, e.g. `full/800,80/90/gray.jpg`). **No resolution cap observed.** **HIGH** for the example object; **MEDIUM** that all objects expose `full/max`.
- **Does the manifest indicate the licence? NO.** **HIGH** (verified `null` on the fetched manifest). You must read CC0 from the Linked Art object record (C.3).

---

# D. GETTY

## D.1 Open Content Program — CC0, with an explicit third-party-rights caveat

**Program page:** `https://www.getty.edu/projects/open-content-program/` (HTTP 200). Verbatim:
> "The Open Content Program makes high-resolution images of public domain artwork from the Getty collections freely available, without restrictions, to advance the research, teaching, and practice of art and art history."
> "**Rights Information** — Digital images of Getty-owned artworks in the public domain marked with the CC0-public domain icon are available for download under CC0. Such images are not protected by copyright and **may be used without restriction or fees for commercial and noncommercial purposes.** See the Open Content FAQ for details."
> "…**[number] images of art and archival material from the Getty Research Institute's collections, including prints, maps, photographs, and study images** documenting the history of European art."
Note: the page's own image count was not cleanly extractable from the fetched HTML — **UNVERIFIED count.** (Press coverage in the search results referenced "more than 88,000"; not adopted.)

**FAQ:** `https://www.getty.edu/projects/open-content-program/faqs/` (HTTP 200). **All verbatim:**

*The exact licence statement, and the CC0 / third-party split:*
> "**What is the copyright status of Getty Open Content images?** Images in the Open Content Program are images of works in the public domain in the United States. The works depicted in the images are not protected by copyright, but Getty may have a copyright interest in the digital image of the work. **To the extent that Getty owns copyright in the digital images, we have chosen to make the images freely available under CC0.** However, some images may include people or objects for which a third party may claim rights (e.g., trademark, copyright, privacy, or publicity rights). **Getty does not guarantee that all of its Open Content images are free from rights claimed by third parties. As the user, it is your responsibility to do that research.**"

> "**What uses and alterations (e.g., cropping, overprinting) of the Open Content images are allowed?** Getty places no restrictions on the use, modification, or reuse of Open Content images. The only requirement is that you **not suggest or imply endorsement by the Getty.**"

> "**How should I credit images from the Open Content Program?** Please include the following credit line after the artwork caption: **Digital image courtesy of Getty's Open Content Program.** Please do not suggest or imply endorsement by Getty."

> "**My editor or publisher requires written permission to use an Open Content image. Whom do I contact?** The J. Paul Getty Trust does not issue individual permission letters… Instead, Getty is pleased to grant this general permission to reproduce any image from its Open Content image repository **to the extent the Getty has rights to do so.** The image may include people or objects for which a third party may claim rights; **Getty is not giving permission to exploit any such third party rights. As the user or publisher, you must ascertain whether any such rights exist, pay any royalties or fees claimed by any third party, and obtain all other permission that may be required.**"

> "**How can I confirm an image is part of the Open Content Program?** … look for the CC0-public domain icon or either of these sentences on the image record page: **"This image is available for free download and may be used for any purpose under Getty's Open Content Program."** or, **"Digital image courtesy of Getty's Open Content Program."**"

> "**What happened to Getty Search Gateway?** The Getty Search Gateway was a discovery tool … We **sunset the Getty Search Gateway** because it was built on older technology… Its role has been taken up by newer, more robust platforms, including the Art Collection and Research Collections sites."

**CC0 vs "no known copyright restrictions" — the precise answer (HIGH):**
- Getty's Open Content is **CC0 1.0** (`http://creativecommons.org/publicdomain/zero/1.0/`), verbatim as above and machine-readably in every manifest I fetched (D.3).
- **Getty does also use rightsstatements.org vocabulary** for the *non*-open material — verbatim from the Terms of Use: *"Every effort has been made to accurately determine the rights status of works and their images. **The Museum utilizes standardized rights statements developed by RightsStatements.org** to communicate the copyright [status]…"*
- **Live confirmation that non-open Getty items carry `InC` / `UND`, not NKC:** from the Getty search API (D.2), a sample of 90 railway-related objects with manifests gave:
  `http://creativecommons.org/publicdomain/zero/1.0/` × **81**; `https://rightsstatements.org/vocab/UND/1.0/` × 4; `https://rightsstatements.org/vocab/InC/1.0/` × 4; `https://rightsstatements.org/vocab/InC-RUU/1.0/` × 1.
  → So the Getty split is **CC0 vs RightsStatements.org `InC`/`InC-RUU`/`UND`**. **I did not observe Getty using the "no known copyright restrictions" phrase as a licence label.** **UNVERIFIED** whether Getty ever uses an NKC-style string. **INFERENCE (HIGH):** Getty's model is cleaner than the user expected — CC0 for open, rightsstatements.org URIs for everything else.
- **Third-party rights caveat (the user's key risk):** even for CC0 images, Getty disclaims warranty as to **trademark, copyright, privacy, publicity** — verbatim as quoted above. On a monetised channel this matters if a photographed artwork depicts a person or a trademarked object. **INFERENCE (HIGH):** for 19th-century engineering photographs, third-party rights risk is low (long-dead subjects, expired copyrights), but **privacy/publicity risk is non-zero for identifiable persons** — e.g. a portrait of a living person is not in this corpus, so risk is low.

**Where to browse:** `https://www.getty.edu/art/collection/` (Getty Museum) and `https://www.getty.edu/research/collections/` (Getty Research Institute). Both HTTP 200. `https://www.getty.edu/research/open-content/` → **HTTP 404 (live contradiction: the old Open Content URL is dead)**; the working page is `https://www.getty.edu/projects/open-content-program/`. **HIGH.**

## D.2 The Getty Museum collection API — REST + SPARQL both live

**API portal:** `https://data.getty.edu/` → **HTTP 200**, titled "Getty API Documentation". Verbatim from that page:
> "As part of Getty's Open Access program, we're pleased to provide public access to much of our collection data via APIs. These APIs are the same ones that we use behind-the-scenes for our website, Getty Guide, and other key applications."
> "**Getty Museum Collection** — A **REST API and SPARQL API** for data about the artwork held at the Getty Museum. Includes data about artwork, people, groups, exhibitions, and gallery locations. Last updated: 04/10/2025. Documentation"
Also listed: **Getty Provenance Index** (REST + SPARQL), **ID Manager** (`/tools/id_manager/docs/`).

**SPARQL endpoint — `https://data.getty.edu/museum/collection/sparql` — CONFIRMED LIVE. HIGH.**
- `GET https://data.getty.edu/museum/collection/sparql` (no query) → **HTTP 400**, body verbatim: `{"errors":[{"status":400,"title":"Bad Request","detail":"No query parameter included"}]}` → proves the endpoint exists and expects `query=`.
- With `?query=SELECT ?s WHERE { ?s ?p ?o } LIMIT 3` + `Accept: application/sparql-results+json` → **HTTP 200**, `application/sparql-results+json`, returning bindings. **HIGH.**
- ⚠️ **Performance:** aggregate `GROUP BY`/`COUNT` queries **timed out** (>60 s) from here. **INFERENCE (HIGH):** restrict SPARQL to narrow, indexed lookups; do not run analytics against it.

**REST/Linked-Art resource endpoint — `https://data.getty.edu/museum/collection/{type}/{id}` — CONFIRMED for `group`, NOT for `object`.**
- `GET https://data.getty.edu/museum/collection/group/ee294bfc-bbe5-42b4-95b2-04872b802bfe` → **HTTP 200, `application/ld+json`**. Verbatim body head:
  `{"@context":"https://static.getty.edu/contexts/linked.art/ns/v1.1.0/linked-art.json","id":"https://data.getty.edu/museum/collection/group/ee294bfc-…","type":"Group","_label":"Drawings (Curatorial Department)","classified_as":…}`
- ⚠️ **`object` sub-type returned 404 for every ID I tried** — `107T5V`, `109J9`, `4d1b6b7c`, `107T5V.json`, trailing slash, case variants — all `{"errors":[{"status":404,"title":"Record Not Found","detail":"Unable to obtain matching record from database"}]}`. **INFERENCE (MEDIUM):** the object path either requires a **UUID** (as `group` does) or a different segment name; Accessibility-number-style IDs like `107T5V` are **Id Manager slugs**, not API IDs. **The practical consequence: use the Id Manager slug for the website URL and the UUID/manifest for API/image access.** **UNVERIFIED** — I could not resolve the exact object-REST signature.
- **`https://data.getty.edu/museum/collection/docs/` → HTTP 404** (`Record Not Found`, i.e. the JSON error handler, not a static 404). The docs link on the portal points here but it does **not** resolve from this environment. **Live contradiction / UNVERIFIED.**

**The working, undocumented search API — `https://www.getty.edu/art/collection/api/search` — CONFIRMED LIVE. HIGH.**
- `GET https://www.getty.edu/art/collection/api/search?q=railway` → **HTTP 200, `application/json`**, 43 KB.
- Top-level keys verbatim: `["query","from","end","size","facets","total","data","one_year_range_min","one_year_range_max","range_min","range_max","took"]`
- `total` (railway) = **358**; `total` ("suspension bridge") = 189; `engineer` = 249; `canal` = 476; `locomotive` = 125; `"thames tunnel"` = **1**.
- `size=100` is honoured (returned 100 rows against `total: 358`) → **pagination via `from`/`size`**.
- Each row in `data[]` carries: `id` (a UUID URI, e.g. `object/86c918fb-…`), `primary_name`, `object_number`, `accession_number`, `date_created`, `producers[]`, `culture[]`, `slug_with_path` (e.g. `/object/10431B`), `id_manager_slug` (e.g. `10431B`), `associated_program`, and — **only when the item has an image** — a **`manifest`** object.
- **The `manifest` object is the licence oracle**, verbatim shape:
  ```json
  "manifest": {"url":"https://media.getty.edu/iiif/manifest/3/31492498-fc0a-4e29-b7e7-8924a64ec9c4",
               "license":"https://rightsstatements.org/vocab/InC/1.0/",
               "sizeRestricted":true,
               "thumb":"https://media.getty.edu/iiif/image/{uuid}/full/!300,300/0/default.jpg",
               "thumbUuid":"…","numItems":1,"altText":"Main View"}
  ```
  → **`manifest.license` gives the rights URI per item.** For the open items it is `http://creativecommons.org/publicdomain/zero/1.0/`; for restricted items `https://rightsstatements.org/vocab/InC/1.0/` etc. **This is the cleanest per-item licence signal across all four sources. HIGH.**
- ⚠️ **Facet filtering is undocumented and `open_content=1` returns HTTP 500.** Tried and **failed**: `open_content=1` → **500**; `f[open_content]=1`, `openContent=1`, `f.open_content=1` → **200 but `total: 0`** (silently returns nothing rather than erroring). **INFERENCE (HIGH): filter client-side on `manifest.license`.** Do not trust a zero result from these params.
- The human search page `https://www.getty.edu/art/collection/search?q=…` is an **empty SPA shell (9,098 bytes, no embedded JSON)** — **do not scrape it; use the JSON API.** **HIGH.**

**API key requirement:** **none observed** for `data.getty.edu` REST/SPARQL or for `www.getty.edu/art/collection/api/search`. **MEDIUM** (no key was needed for any call; no key is documented on the portal page I fetched).
**Rate limits:** **UNVERIFIED.** No limit stated on the portal or docs pages I could reach.
**Bulk download:** **UNVERIFIED** for Getty. I did not find a Getty data dump. (A `github.com/thegetty` collection-data repo was hypothesised in the brief; **UNVERIFIED.**)

## D.3 Getty IIIF — exact patterns, resolution, and licence in the manifest

**Two IIIF hosts, both confirmed:**
- **Manifests:** `https://media.getty.edu/iiif/manifest/{n}/{uuid}` — e.g. `https://media.getty.edu/iiif/manifest/8f4cd093-7e6e-4a4b-96c5-a77ffee7c3b7` → **HTTP 200, `application/json`**.
- **Images:** `https://media.getty.edu/iiif/image/{uuid}/{region}/{size}/{rotation}/{quality}.{format}` — e.g. `.../full/!300,300/0/default.jpg` (thumbnail), `.../full/max/0/default.jpg`, `.../full/full/0/default.jpg`.
- ⚠️ **`https://iiif.getty.edu/` returned HTTP 000 (unreachable)** from this environment for both root and `/collection/{id}/manifest.json`. **Live contradiction: the `iiif.getty.edu` hostname pattern does not work here; the working host is `media.getty.edu`.** **HIGH** on the media host; the `iiif.getty.edu` failure may be environment-specific — but **do not build on it.**

**Resolution: full maximum is permitted. HIGH.**
- `https://media.getty.edu/iiif/image/4828d2ce-e49e-444f-9561-a4f99d5159a9/info.json` → **200**, IIIF Image API **v3**, `width: 13301`, `height: 4158`, with an explicit `sizes[]` array (`207×64`, `415×…`, …).
- **`https://media.getty.edu/iiif/image/4828d2ce-e49e-444f-9561-a4f99d5159a9/full/max/0/default.jpg` → HTTP 200, `image/jpeg`, 14,210,238 bytes (~14 MB).** And `full/full/0/default.jpg` returns the **identical 14,210,238-byte** payload. → **`max` and `full` are equivalent here: the full 13,301-px master is downloadable.** ✅ **HIGH.** (Server banner: `iipsrv/1.3`, ICC profile embedded.)

**Does the IIIF manifest indicate the licence? — YES. HIGH.** Verbatim from `https://media.getty.edu/iiif/manifest/8f4cd093-7e6e-4a4b-96c5-a77ffee7c3b7`:
- `rights` = **`"http://creativecommons.org/publicdomain/zero/1.0/"`** ← a non-HTTPS CC0 URI.
- `requiredStatement` = `{"label":{"en":["attribution"]},"value":{"en":["<p>Images provided here are believed to be in the public domain and are available under <a href=\"https://creativecommons.org/publicdomain/zero/1.0/\">CC0</a> through Getty's <a href=\"http://www.getty.edu/about/opencontent.html\">Open Content Program</a>. Texts provided here are &copy; J. Paul Getty Trust, licensed under <a href=\"https://creativecommons.org/licenses/by/4.0/legalcode\">CC BY 4.0</a>. Terms of use for the Getty logo can be found <a href=\"http://www.getty.edu/legal/copyright.html#logo\">here</a>"]}}`
- Other keys present: `@context, homepage, id, items, label, metadata, partOf, provider, requiredStatement, rights, seeAlso, structures, thumbnail, type`. `license` and `attribution` are **absent** (`null`) — Getty uses **`rights` + `requiredStatement`**, not `license`. **HIGH — this is the exact field-name trap.**
- `provider` = `[{"id":"https://www.getty.edu/about/","label":{"en":["J. Paul Getty Trust"]}, …}]`.
- `homepage` = `[{"id":"https://www.getty.edu/art/collection/object/105X94","type":"Text"}]`.

**⚠️ The manifest's `requiredStatement` text is a three-way licence statement, not a single one — read it carefully:**
1. **Images → CC0** (`https://creativecommons.org/publicdomain/zero/1.0/`).
2. **Texts → © J. Paul Getty Trust, CC BY 4.0.**
3. **Getty logo → separate terms** (`…/legal/copyright.html#logo`).
So if you reproduce Getty's *catalogue text* (not just the image) in your Reel description, you need **CC BY 4.0 attribution** to the Trust. **HIGH.** This is a real, easily-missed obligation.

## D.4 Getty 19th-century engineering / industrial / railway photography — YES, and it is CC0

**Verbatim licence line as displayed/injected on an item page** — `https://www.getty.edu/art/collection/object/105X94` and `/108KWG` and `/107B2A`, each **HTTP 200**. The embedded JSON-LD carries, verbatim:
> `"license": "http://creativecommons.org/publicdomain/zero/1.0/"`
> `"creditText": ["Images provided here are believed to be in the public domain and are available under CC0 through Getty's Open Content Program. Texts provided here are © J. Paul Getty Trust, licensed under CC BY 4.0. Terms of use for the Getty logo can be found here."]`

**Actual on-topic items found via `https://www.getty.edu/art/collection/api/search` (all with `manifest.license = http://creativecommons.org/publicdomain/zero/1.0/` unless noted):**

| Id slug | Title | Date | Accession | Rights |
|---|---|---|---|---|
| **`107B2A`** | **[Bridge under construction]** — hand-coloured albumen silver print | 1855–1860 | `84.XC.979.10066` | **CC0** |
| **`108KWG`** | **Gotthardbahn: Kerstellenbachbrücke (Im Bau)** — albumen silver print; description verbatim: *"View of a bridge under construction over a rocky stream. The stream is lined on both sides with stone embankments and houses."* | about 1875–1882 | `84.XO.392.26` | **CC0** |
| `108KWF` | Gotthardbahn: Kerstellenbachbrücke (Im Bau) | about 1875–1882 | — | **CC0** |
| **`104HMC`** | **The Manchester Ship Canal. A Pictorial Record of its Construction** | **1894** | — | **CC0** |
| `104HMD` | The Manchester Ship Canal… (variant) | 1894 | — | **CC0** |
| `104JAC` | New Bridge over Potomac River. On the Washington, Alexandria… | July 1864 | — | **CC0** |
| `1076P6` / `1076P8` | Jericho Mills from North Bank of North Anna, Va., with Canvas… | May 23, 1864 | — | **CC0** |
| `107RXS` | Wire Rope across the Fall | 1868–1869 | — | **CC0** |
| `104H5N` | Australia. A.C.D. 1887. (cover title) [Views and architect…] | 1887 | — | **CC0** |
| `106RNR` | **Exhibition of the Works of Industry of all Nations, 185[1]** (the Great Exhibition) | 1852 | — | **CC0** |

Sample aggregate evidence: a 100-row `q=photograph railway` pull returned **90 rows with a manifest**, of which **81 were CC0**, 4 `UND/1.0`, 4 `InC/1.0`, 1 `InC-RUU/1.0`. A `q=bridge construction` pull returned **50 rows with manifests, 45 CC0.** **HIGH.**

**Item URL formats (all confirmed HTTP 200):**
- Human page: `https://www.getty.edu/art/collection/object/{id_manager_slug}` — e.g. `https://www.getty.edu/art/collection/object/108KWG`, `.../107B2A`, `.../104HMC`, `.../106RNR`, `.../104H5N`.
- Manifest: from `manifest.url` in the search API, e.g. `https://media.getty.edu/iiif/manifest/3/31492498-fc0a-4e29-b7e7-8924a64ec9c4`.
- Image: `https://media.getty.edu/iiif/image/{thumbUuid}/full/max/0/default.jpg`.

**Thames Tunnel / Brunel specifically — a NEGATIVE result worth stating plainly:**
- `q="thames tunnel"` on the Getty Museum API returns **exactly 1** object: `object/ed77c57e-a4f6-4ac7-bf11-a5dc110047cc`, slug **`10431B`**, *'Old Toys: "Tunnel under the Thames"'*, by **Werner Franz Rohde** (German, 1906–1990), **date 1930–1939**, accession `84.XM.175.5`, medium gelatin silver print.
  - **`manifest.license` = `https://rightsstatements.org/vocab/InC/1.0/`** and **`sizeRestricted: true`** → **IN COPYRIGHT. NOT Open Content.** It is also a photograph of *toys* from the 1930s, not the tunnel itself. **Commercially unusable. HIGH.**
- **No Getty Museum item depicting Marc Brunel, the tunnelling shield, or the Thames Tunnel works was found.** **MEDIUM-HIGH** (the API search is the museum's own index). Contrast with the Getty ***Research Institute***, which **does** hold an 1837 Thames Tunnel work — see the Internet Archive cross-reference below.
- **Cross-source lead (HIGH):** `https://archive.org/metadata/explicationdestr00unse` — *"Explication des travaux entrepris pour la construction de la tonnelle ou passage sous la Tamise entre Rotherhithe et Wapping…"*, **1837**, `sponsor = Getty Research Institute`, `contributor = Getty Research Institute`, collection `["getty","americana"]`, description verbatim: *"Describes the tunnel begun by Brunel in 1825 and completed in 1843, **with sectional drawings of the tunneling shield**"*, *"Plate facing leaf 21 has an overlay"*. → **This is the single most on-topic item found in the entire research, and it contains tunnelling-shield sectional drawings.** Its archive.org item has **no `licenseurl` and no `rights` field**, and it is an **IA scan of a Getty Research Institute book**. **INFERENCE (HIGH):** the underlying 1837 work is unambiguously PD (pre-1930 by 189 years); the only open question is whether Getty asserts a scan-level right — and Getty's own OCP position (D.1) is that it releases PD-work images under **CC0**, while the manifest `requiredStatement` says images are *"believed to be in the public domain."* **Recommended: download from archive.org (`https://archive.org/download/explicationdestr00unse/explicationdestr00unse.pdf`) and/or verify the corresponding record in Getty's own Research Collections at `https://www.getty.edu/research/collections/` for a CC0 download button. MEDIUM.**

**Other on-topic-once-you-look items (CC0):** the **Manchester Ship Canal 1894 construction album** and the **Gotthardbahn bridge-construction** plates are excellent B-roll/reference for later engineering episodes (docks, canals, railways, bridges) even though not Thames-Tunnel-specific. The **1851 Great Exhibition** album is directly useful for engineering-history context.

## D.5 The "In Copyright" vs "Open Content" split and how it is marked

**Two independent machine-readable markers, and they agree:**
1. **On the collection-record page (JSON-LD / `creditText`)**, verbatim:
   > `"creditText": ["Images provided here are believed to be in the public domain and are available under CC0 through Getty's Open Content Program. Texts provided here are © J. Paul Getty Trust, licensed under CC BY 4.0. Terms of use for the Getty logo can be found here."]`
   for open items; **absent** for in-copyright items.
2. **In the search API's `manifest.license` / the IIIF manifest's `rights`**, verbatim:
   - **Open:** `http://creativecommons.org/publicdomain/zero/1.0/` (+ `rightsstatements.org` never used for open)
   - **In copyright:** `https://rightsstatements.org/vocab/InC/1.0/`, `https://rightsstatements.org/vocab/InC-RUU/1.0/` (In Copyright – Rights-holder Unlocatable or Unidentifiable)
   - **Undetermined:** `https://rightsstatements.org/vocab/UND/1.0/`
3. **Getty Terms of Use** (`https://www.getty.edu/legal/copyright.html` → **redirects to `https://www.getty.edu/legal/terms-of-use/`**, HTTP 200). Verbatim:
   > "**Open Content Program** — Many high-resolution digital images to which Getty holds the rights, or which depict works in the public domain, are available for free download under CC0 through Getty's Open Content Program. **No permission from Getty is required. You may use these images for any purpose** under the following terms: You may not use the images in any way that suggests or implies that Getty endorses, approves of, or participated in your project, or in any way that might create confusion about the source of your project."
   > "All text in the collection records is licensed under a **Creative Commons Attribution 4.0. International (CC-BY) License**, unless otherwise noted. **Images and other media are not covered by the CC-BY license.** Digital images of Getty-owned artworks in the public domain are available for free download under CC0 through Getty's Open Content Program… **The Museum utilizes standardized rights statements developed by RightsStatements.org** to communicate the copy[right status]…"
   > "**Trademarks** — The names, titles, building images, trademarks, service marks, and logos that appear on Getty websites are registered and unregistered marks of Getty, including but not limited to "Getty," "J. Paul Getty Trust," "J. Paul Getty Museum," and the exterior and interior building images of the Getty Center and Getty Villa (collectively, the "Getty Trademarks"). **Getty Trademarks may not be used in any way that suggests an actual or implied endorsement** of any program, product, or service of a non-Getty entity."

**⚠️ IMPORTANT LIVE CONTRADICTION INSIDE GETTY'S OWN TERMS — flag this to the operator.** The same Terms of Use page contains a **general** clause that flatly forbids commercial use of Site Content, and an **Open Content Program** clause that expressly permits it. Verbatim, general clause:
> "Getty authorizes you to view, download, and print the Site Content subject to the following conditions: … (2) Unless otherwise restricted, you may only do so for **your own personal and noncommercial use**, or for fair use as defined in the United States copyright laws; (3) **Using Site Content for commercial purposes is prohibited**; (4) Using Site Content for personal websites is **subject to review and approval by Getty provided your site takes no advertising and has no commercial sponsors**…"

**Resolution (INFERENCE, HIGH confidence):** the general clause is scoped by its own opening words — *"Other than the open content images identified on the website for unrestricted downloading and the portions of the website expressly made available under a Creative Commons license (both described below), all of the text, images, marks, logomarks, and other content of the Getty websites ("Site Content") are proprietary to Getty…"*. Open Content images are therefore carved **out** of "Site Content", and the OCP clause governs them: **CC0, commercial use permitted, no permission required.** But note that this is a **reading**, and the two clauses do sit on the same page in tension. **This is the one Getty point I would put in front of a lawyer if the channel ever gets large.** Confidence that CC0 governs OCP images: **HIGH**. Confidence that a hostile reading could not be constructed: **MEDIUM.**

---

# E. BOTTOM LINE — what is usable on a monetised Instagram Reels channel without legal review

Ordered by safety. "No legal review" means: the licence is unambiguous, machine-readable, and permits commercial use.

## ✅ TIER 1 — Safe. Use freely, with the stated credit.
1. **HABS / HAER / HALS (Library of Congress).** NPS verbatim: *"Materials created for HABS, HAER, or HALS are in the public domain."* Measured drawings, large-format photos, data pages for >46,000 sites. Full-resolution images are served from reachable `tile.loc.gov` IIIF (`full/pct:100`).
   - **Action:** check the per-item rights line; LOC's own wording is *"the original measured drawings and **most** of the photographs… are considered to be in the public domain"* — verify each item. Credit LOC. **Best asset class in this report.**
   - **Caveat:** overwhelmingly **American** engineering — good for later episodes, not for Thames Tunnel.
2. **Getty Open Content (CC0).** `rights`/`license` = `http://creativecommons.org/publicdomain/zero/1.0/`, machine-readable per item via `manifest.license`. Getty verbatim: *"may be used without restriction or fees for commercial and noncommercial purposes."* Full 13,301-px masters downloadable via `media.getty.edu/iiif/image/{uuid}/full/max/0/default.jpg`.
   - **Obligations:** credit *"Digital image courtesy of Getty's Open Content Program"*; **do not imply Getty endorsement**; if you reproduce Getty **catalogue text**, that text is **CC BY 4.0** and needs attribution.
   - **Caveat:** Getty disclaims warranty for third-party **trademark/copyright/privacy/publicity** rights. Low risk for 19th-c engineering photography; non-zero if a person is identifiable.
   - **Filter rule:** ingest only where `manifest.license == "http://creativecommons.org/publicdomain/zero/1.0/"`; exclude `InC/1.0`, `InC-RUU/1.0`, `UND/1.0`.
3. **Rijksmuseum (CC0), via the new API.** Machine-readable CC0 (`https://creativecommons.org/publicdomain/zero/1.0/`) in the Linked Art `subject_of → subject_to → Right`. `full/max` IIIF downloads permitted. No API key.
   - **Obligations:** do not use the Rijksmuseum logo/wordmark; do not imply endorsement. Credit the museum as courtesy.
   - **Caveat:** the **IIIF manifest does NOT carry the licence** — you must read it from `https://data.rijksmuseum.nl/{id}`. Build that check in.
   - **Caveat:** 19th-c engineering content is Dutch hydraulic/maritime/steam (verified CC0: `NG-MC-28` dredger model c.1800; `NG-MC-528` 1855 trunk steam engine), **not** the Thames Tunnel.
4. **The four Internet Archive Thames Tunnel pamphlets** (`thamestunnelade00tunngoog` 1825, `originprogressa00westgoog` 1827, `sketchesworksfo00cruigoog` 1829, `anexplanationwo00compgoog` 1840). All `possible-copyright-status = NOT_IN_COPYRIGHT` **and** independently PD by the 95-year rule (published 1825–1840). **Directly on Episode 1.** `_jp2.zip` and PDFs verified downloadable.
   - **Obligations:** IA requests a descriptive User-Agent and rate courtesy (4 concurrent / 1 s delay); do **not** hotlink `ia######.us.archive.org` URLs — use `archive.org/download/...`.
   - **Caveat:** scan-level rights are asserted by the contributing partner (Google/Oxford/Harvard). Google-scanned `*goog` items carry the usual Google-scan provenance; **INFERENCE (MEDIUM)** that no separate scan-level restriction is being asserted, but this is the one Tier-1 item with residual diligence.
5. **The ex-GRI 1837 Thames Tunnel volume with tunnelling-shield sectional drawings** (`explicationdestr00unse`). PD by date (1837); Getty Research Institute is the contributor and Getty's OCP position is CC0 for PD-work images.
   - **Action:** this **is** your Episode 1 hero imagery. Verify the matching record in `https://www.getty.edu/research/collections/` for an explicit CC0 download button before publishing, and **note the caveat below**.

## ⚠️ TIER 2 — Usable with a per-item check, not blanket.
6. **LOC "No known restrictions on publication" items.** LOC verbatim: *"These facts do not mean the image is in the public domain, but do indicate that no evidence has been found to show that restrictions apply."*
   - **Verified example:** LOC Thames Tunnel lithograph (1830), `https://lccn.loc.gov/98507755/mods`, `accessCondition` = *"No known restrictions on publication."* Given the 1830 date this falls under the expired-copyright branch → **treat as commercially usable, MEDIUM-HIGH.**
   - **Check:** confirm the underlying work is pre-1930 (or had unrenewed copyright), and that the file you take is not a separately-licensed third-party reproduction.
   - **Rule of thumb:** `No known restrictions` + pre-1930 + no donor restriction + LOC's own scan → usable. Anything else → read the collection's rights statement.
7. **LOC "Free to Use and Reuse" sets.** Usable, but **only after reading the per-item rights line**, because the disclaimer is a three-way disjunction — one branch is *"cleared by the copyright owner for public use"*, which may carry unpublished conditions. Dataset is 2,610 items, last updated **2024-04-17**. No engineering theme is named.
8. **LOC "Public Domain" statement items.** LOC verbatim: *"If images were copyrighted and copyright has expired, we say 'Images in this collection are considered to be in the public domain.'"* **Commercially safe: HIGH** — this is stronger than NKC and can be used with the same credit courtesy.

## ❌ TIER 3 — Do NOT use on a monetised channel.
9. **Any IA `internetarchivebooks` / `printdisabled` / `inlibrary` item.** Controlled Digital Lending = lend-only, no reproduction rights. (e.g. the 1970 Brunel biography `isambardkingdomb0000rolt_d0g4`.)
10. **The David Rumsey Thames Tunnel plate** `dr_view-plate-1-construction-of-roads-thames-tunnel-12190612`. Rights verbatim: *"Creative Commons **CC BY-NC-SA 3.0** … **Please contact the David Rumsey Map Collection for commercial use**." Explicitly non-commercial, despite the 1851 underlying work being PD. **This is the exact trap to avoid.**
11. **IA "Community Texts"/`opensource*` uploader content** used on the strength of its own rights field. `rights`/`licenseurl`/`possible-copyright-status` are **uploader-authored free text** per IA's schema. Never a reliable PD claim.
12. **The Metropolitan Museum of Art item mirrored on IA** (`mma_marc_isambart_brunel_…`, a Brunel portrait). Its `rights` field is *"Metropolitan Museum of Art Terms and Conditions"* — partner terms, not PD/CC0.
13. **Any Getty item with `manifest.license` of `InC/1.0`, `InC-RUU/1.0`, or `UND/1.0`.** Includes the only Getty "Thames Tunnel" hit (`10431B`, 1930s, In Copyright, size-restricted).
14. **LOC items marked "Rights status not evaluated", "Publication may be restricted", "May be restricted…", or with no/differently-worded rights note.** LOC verbatim: *"the Library has not received or gathered information pertaining to the rights status of the image."* Requires your own evaluation — outside "no legal review".
15. **Thingiverse 3D models under `BY-NC`/`BY-NC-SA`** (~565 k items) and **unlicensed models** (1,732). Non-commercial only / all rights reserved.
16. **Getty's general "Site Content"** (site design, Getty building photography, marks, logos, non-collection text). Verbatim: *"Using Site Content for commercial purposes is prohibited."* Open Content images are carved out; nothing else is.

## 🔧 Cross-cutting operational rules
- **Verify licences programmatically before ingest, not by eye.**
  - Getty: assert `manifest.license == "http://creativecommons.org/publicdomain/zero/1.0/"`.
  - Rijksmuseum: assert `https://creativecommons.org/publicdomain/zero/1.0/` appears in `GET https://data.rijksmuseum.nl/{id}` with `Accept: application/ld+json` (**not** in the manifest — it isn't there).
  - Internet Archive: assert `possible-copyright-status == "NOT_IN_COPYRIGHT"` **and** independently compute `year <= 1930`. Do **not** rely on `collection:pub_*`.
  - LOC: fetch `https://lccn.loc.gov/{lccn}/mods` and read `<accessCondition type="use and reproduction">` verbatim.
- **Never hotlink** IA `ia######.us.archive.org` URLs (IA's own docs: *"DO NOT LINK"*) or brief-serving hosts.
- **UA + rate courtesy on archive.org:** descriptive User-Agent incl. tool/version (and model, if an AI agent); 4 concurrent max, 1 s delay; honour 429/`Retry-After`.
- **Cache aggressively.** IA's own best-practice list says *"Cache responses."* Re-fetching across a Blender/Python pipeline will trip limits.
- **Keep a per-asset rights manifest** (URL fetched, verbatim licence string, date, HTTP status). This is your defence if a claim arrives, and it is cheap to generate from the APIs above.
- **Attribution minimum across all Tier 1:** source institution + collection + item/reproduction number (LOC's requested form), *"Digital image courtesy of Getty's Open Content Program"* for Getty, and no implied endorsement of any institution.
- **Instagram-specific:** CC BY-SA and CC BY-NC assets are effectively unusable here — NC bars the ad revenue, and SA's share-alike obligation sits badly against Instagram's ToS. **Restrict to CC0 / PD / CC BY** (CC BY only where attribution can be carried in-frame or in the caption).

## Gaps I could not close (do not guess these)
- **`www.loc.gov` JSON API signatures** (`c=`/`sp=`/`dates=`, item-response shape) — **UNVERIFIED** (Cloudflare 403). Use the `pagination.next` loop LOC documents, and `lccn.loc.gov/{lccn}/mods` for item rights.
- **`chroniclingamerica.loc.gov` API** — **UNVERIFIED** (308 → 403). It has been folded into `loc.gov`.
- **Rijksmuseum rate limits** — **UNVERIFIED.** The "~10,000/day" figure was for the **retired** API that now returns **410 Gone**. Do not cite a number.
- **Rijksmuseum's own logo/marks terms** — **UNVERIFIED verbatim** (no reachable terms page). Treated as INFERENCE.
- **Getty object-level REST signature** (`/museum/collection/object/{id}`) — **UNVERIFIED** (404 on all attempts); use the search API + `manifest.url`.
- **`iiif.getty.edu`** — **unreachable (HTTP 000)**; use `media.getty.edu`.
- **Getty rate limits / bulk dump / API key documentation** — **UNVERIFIED.**
- **IA platform-wide rights statement and numeric rate limit** — **UNVERIFIED** (Zendesk 403; developer docs state no number).
- **Whether Rijksmuseum's 2 `description=Brunel` and 31 `description=Thames` objects are on-topic** — **UNVERIFIED; print them before use.**
