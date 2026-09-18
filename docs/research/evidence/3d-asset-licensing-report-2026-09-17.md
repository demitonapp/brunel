# 3D / Imagery Licensing Report — Monetised Instagram Reels (Engineering History)

**Research date:** 17 September 2026 · **Researcher:** licensing-research agent
**Subject:** Marc Brunel's Thames Tunnel tunnelling shield (1825–1843), vertical 9:16 AI-voiceover Reels, ad revenue + brand sponsorships, Blender + Python, solo creator.
**Method:** live page fetches only. Confidence markers: **HIGH** (fetched verbatim) / **MEDIUM** (fetched, ambiguous or third-party) / **LOW** (weak/unconfirmed). Inference labelled `INFERENCE:`. Unconfirmed labelled `UNVERIFIED`.

**Access note:** `si.edu`, `3d.si.edu` and `3d-api.si.edu` sit behind a bot-verification wall (HTTP 403 "Smithsonian request verification"). `myminifactory.com` sits behind Cloudflare (HTTP 403 "Just a moment..."). Those pages were reached via `web.archive.org`, `r.jina.ai` text extraction, or the underlying API, as noted per item.

---

## EXECUTIVE VERDICT

| Source | Licence actually found | Usable on a monetised Reels channel? |
|---|---|---|
| **Smithsonian CC0** (metadata **and** media) | `CC0` | **YES — clean.** No attribution required, commercial use expressly permitted. |
| **Smithsonian "usage conditions apply"** | "Usage conditions apply" | **NO.** Commercial use expressly prohibited. |
| **Smithsonian 3D (Voyager)** | CC0 subset exists (`3d.si.edu/cc0`) | **YES for the CC0 subset**, but the 3D corpus is ~0.01% engineering; effectively **no Brunel-era engineering 3D**. |
| **Scan the World (MyMiniFactory)** | **CC BY-NC-SA 4.0** | **NO.** NC element + MMF's own blanket non-commercial ToS. |
| **Sketchfab CC0** | `cc0` / "CC0 Public Domain" | **YES** (download API needs a Sketchfab login). |
| **Sketchfab CC BY** | `by` / "CC Attribution" | **YES**, with credit. |
| **Sketchfab CC BY-SA** | `by-sa` | **YES**, with credit + share-alike on derivatives. |
| **Sketchfab BY-NC / BY-NC-SA / BY-NC-ND** | `by-nc`, `by-nc-sa`, `by-nc-nd` | **NO** for a monetised channel. |
| **Sketchfab BY-ND / BY-NC-ND** | `by-nd` | **Risky** — Reel rendering/editing likely creates a derivative. |
| **Sketchfab Store: Standard** | `st` / `free-st` | **YES** commercially, subject to licence restrictions. |
| **Sketchfab Store: Editorial** | `ed` | **NO** — no commercial, promotional or sponsored use. |

**Bottom line for Episode 1:** build the shield geometry yourself in Blender; use Smithsonian **CC0** Thames Tunnel engravings/broadsides for period reference and on-screen imagery; use Sketchfab **CC0 / CC-BY** (filtered `features=downloadable&licenses=cc0`) for any third-party 3D. **Do not use Scan the World** and **do not use any NC/ND licence** on a monetised channel.

---

# A. SMITHSONIAN OPEN ACCESS

## A1. Is ALL of Open Access CC0? — **NO. There is a mix.**

**HIGH — fetched** `https://r.jina.ai/https://www.si.edu/openaccess/faq` (live page text; direct fetch is 403)

The FAQ states the program is CC0:

> "We have released these images and data into the public domain as Creative Commons Zero (CC0), meaning you can use, transform, and share our open access assets without asking permission from the Smithsonian."

But it also defines a **non-CC0** class:

> "**What is not included in Smithsonian Open Access?** … some items are not part of this program and their use is restricted."
> "If an item is not designated as CC0, it is subject to usage conditions."

Exact licence strings found in the API response body (not prose): `"access": "CC0"` under `content.descriptiveNonRepeating.metadata_usage`.

**HIGH — the decisive media/metadata split**, from `https://web.archive.org/web/20250902123933/https://www.si.edu/openaccess/devtools`:

> "You can access open access metadata and register for an API key via the Smithsonian's public API hosted on api.data.gov."
> "**Portions of metadata are made available for all digital images of public domain objects whose underlying work is in the public domain, including a URL to a corresponding image file. Objects in the Smithsonian's collection that may have copyright or other limitations have portions of metadata with CC0, but no media file is provided by the Smithsonian due to limitations.**"

**HIGH — quantified by the live API** `https://api.si.edu/openaccess/api/v1.0/stats?api_key=DEMO_KEY`:

```json
"total_objects": 42650469,
"metrics": {
  "CC0_records": 17431244,
  "CC0_records_with_CC0_media": 5255849,
  "CC0_media_percentage": 30,
  "CC0_media": 4785570
}
```

**Reading:** ~41% of records carry CC0 metadata; only ~5.26M of those have CC0 media, and ~4.79M CC0 media assets total. **CC0 metadata ≠ CC0 image.** Never assume a search hit is CC0 — check `metadata_usage` *and* pull the record's `media` block before using an image.

**Notable unit:** `OCIO_DPO3D` (the 3D digitisation program) reports `total_objects: 4200`, `CC0_records: 112`, `CC0_records_with_CC0_media: 3510`. (Media count exceeds record count — the 3D program's counting differs; treat as `UNVERIFIED`.)

**HIGH — commercial answer**, verbatim from the FAQ:

> "**May I use Smithsonian Open Access content for commercial use?** Yes, you may use Smithsonian Open Access assets designated as CC0 for commercial purposes without any attribution, permission, or fee paid to the Smithsonian."
> "**How can I use content NOT designated as CC0?** Assets marked with "usage conditions apply" may be used for personal, educational, and other non-commercial uses consistent with fair use … **You may not use any assets with usage conditions for commercial purposes.**"

**HIGH — social-media / bot-account guidance**, directly relevant to this channel:

> "**Can I create a bot or social media account to share Smithsonian images and information?** Yes! But please note our names are not part of the release! … avoid using our names (the Smithsonian, SI, or any museum name) in the account's name, address, display name, handle, nickname, or other field. … you may mention the Smithsonian in the bio section."

**HIGH — advertising nuance** (the FAQ's one concession toward ad-supported reuse of restricted content):

> "**Is it an unauthorized use of Content with usage conditions if the host of my website or blog adds advertising to my website or blog?** If that is the only commercial aspect of your website or blog, you may post the Content with usage conditions on that site consistent with these Terms of Use."

`INFERENCE:` This concession is framed for a blog where incidental display advertising is the *only* commercial aspect. A brand-sponsored Reel, or a channel whose stated purpose is promoting the creator's paid work, is **not** "the only commercial aspect", so this carve-out should not be relied on.

**HIGH — trademarks excluded:**

> "**Does this mean I can use the Smithsonian logo or trademark?** No, the Smithsonian logo and other trademarks are not included in the open access program."

### Contradition flagged (live pages disagree with each other)
The FAQ is **stale**: it still reads "2.8 million at February 2020 launch" and "committed to releasing over 3 million items throughout 2020 alone". The OA homepage (archived 2026-09-09) says **"more than 5.1 million 2D and 3D digital items"**, and the stats API reports **17.43M CC0 records / 4.79M CC0 media**. Use the API numbers, not the FAQ's. **HIGH** (all three fetched).

## A2. API — key, base URL, endpoints, rate limits, bulk

**Does it need a key?** Yes. `api_key` query parameter. **HIGH** — verified: `https://api.si.edu/openaccess/api/v1.0/search?q=steam%20engine&api_key=DEMO_KEY` returns HTTP 200 with `"status": 200, "responseCode": 1`.

**How to get one (HIGH):** register at **`https://api.data.gov/signup/`** — confirmed by the FAQ ("hosted on api.data.gov") and the devtools page ("register for an API key via the Smithsonian's public API hosted on api.data.gov"). There is no separate si.edu signup.

**Base URL (HIGH):** `https://api.si.edu/openaccess/api/v1.0/`

**Endpoints actually exercised (HIGH):**

| Method | Path | Result |
|---|---|---|
| `GET` | `/search?q={query}&api_key={key}` | 200. Also supports `&fq={field}:{value}` and `&rows={n}`. |
| `GET` | `/content/{url}?api_key={key}` | 200. `{url}` is the record's `url` field, e.g. `edanmdm:siris_sil_4317`. |
| `GET` | `/stats?api_key={key}` | 200. Returns monthly per-unit CC0 counts. |
| `GET` | `/terms?api_key={key}` | **404** — not an endpoint. |

Working examples:
- `https://api.si.edu/openaccess/api/v1.0/search?q=Thames%20Tunnel&api_key=DEMO_KEY` → `"rowCount": 40`
- `https://api.si.edu/openaccess/api/v1.0/content/edanmdm:siris_sil_4317?api_key=DEMO_KEY` → full record
- `https://api.si.edu/openaccess/api/v1.0/stats?api_key=DEMO_KEY` → stats table

`UNVERIFIED:` the full parameter list (the official Swagger/apidocs at `https://edan.si.edu/openaccess/apidocs/` and `https://edan.si.edu/openaccess/docs/` render via JavaScript and returned only "Loading…"). Also `UNVERIFIED:` whether `fq=online_media_type:"3D"` filters correctly — a test returned book records, so that facet appears not to do what its name suggests.

**Rate limits (MEDIUM — third-party source, not Smithsonian):** `https://apis.io/rate-limits/smithsonian/smithsonian-rate-limits/` states limits are "managed through api.data.gov … All limits reset on a rolling hourly basis", and `https://data.clawrxiv.org/sources/smithsonian-open-access` states:

> "DEMO_KEY: 30 req/hour. Registered key: 1000 req/hour."

`INFERENCE:` 1,000/hour is api.data.gov's standard default tier. Treat as MEDIUM; the Smithsonian docs page could not be read. Plan for a registered key and client-side backoff on HTTP 429.

**Bulk / data dump (HIGH):**
- **GitHub:** `https://github.com/Smithsonian/OpenAccess` — "Smithsonian Open Access Data Repository". Devtools page: *"Users can access the Smithsonian's collection data made by Smithsonian staff since 1846 via a GitHub repository … the data formatted in .JSON. Please note that the Smithsonian does not support pull requests. Data is refreshed at a weekly rate."*
- **AWS:** homepage states *"Data hosting provided by AWS Public Dataset Program"*. An AWS Public Dataset bucket exists but the exact bucket name was **not** directly fetched → `UNVERIFIED`.
- **Figshare:** `https://smithsonian.figshare.com/?searchMode=1&licenses=2` ("Discover open research datasets").
- **Wikimedia / Internet Archive / Wikidata / DPLA / GBIF**, and DarwinCore bulk via `https://collections.nmnh.si.edu/ipt` — listed verbatim in the FAQ.

## A3. 3D — what is on 3d.si.edu, downloadability, licence, API

**HIGH** — `https://web.archive.org/web/20230521062440/https://3d.si.edu/`: site is "Smithsonian 3D Digitization", run by the Digitization Program Office. It explicitly routes CC0 3D to a filtered view:

> "Smithsonian Open Access invites you to download, transform, and share millions of the Smithsonian's online items, for any purpose, for free, without further permission from the Smithsonian. **Search all Open Access 3D models: 3d.si.edu/cc0**"

And the OA homepage links the same: *"3D Voyager — View, interact, and download Smithsonian 3D content"* → `https://3d.si.edu/cc0`.

**Download formats (HIGH)** — FAQ verbatim:

> "**3D Images** — glTF, glb, obj (150k and full res versions), Voyager scenes (viewable models online)"

**Licence of 3D (HIGH by inference from the CC0 filter):** the existence of `3d.si.edu/cc0` as a distinct filtered view is direct evidence that **3D is NOT uniformly CC0** — there is a non-CC0 remainder. `INFERENCE:` 3D models surfaced under `/cc0` are CC0; those outside it are not. Verify per model.

**Is there a 3D API? (MEDIUM)** There is a host, not a documented public API:
- `https://3d-api.si.edu/` returns HTTP 200 with body `3d-api.si.edu` (a live host, no docs index).
- Media assets are served from it, e.g. an OA homepage thumbnail resolved to `https://3d-api.si.edu/content/document/3d_package:d8c62be8-4ebc-11ea-b77f-2e728ce88125/scene-image-thumb.jpg`.
- `https://3d-api.si.edu/content/search?q=tunnel` → **HTTP 404**.
- `UNVERIFIED:` there is no publicly documented "Smithsonian 3D API" with a search endpoint. **Practical route: query the EDAN Open Access API and filter for `type: 3d_package`.** `UNVERIFIED:` my attempt at `fq=type:"3d_package"` did not filter as intended.

**Serving stack (HIGH):** Smithsonian's own **Voyager** viewer, open-sourced at `https://smithsonian.github.io/dpo-voyager/` and `https://smithsonian.github.io/dpo-cook/`. **Not** Sketchfab-hosted for the canonical copies (Sketchfab is listed on the OA homepage only as a "remix" partner).

**Subject mix — is it natural history / aerospace?** `INFERENCE (MEDIUM):` the OA homepage's own "Featured Platforms" thumbnail and highlighted 3D example is *"Buddha draped in robes portraying the Realms of Desire"*, and the homepage topic links are `Sports`, `Portraits`, `Clothing and dress`, `Outer space`. Combined with the `OCIO_DPO3D` stats (4,200 objects total), the 3D corpus is **small and dominated by cultural/portrait/natural-history/aerospace subjects**. There is **no evidence of 19th-century engineering or industrial 3D content**. `UNVERIFIED:` an exact subject breakdown — the 3D catalogue could not be enumerated because the site and its API search are behind bot protection / undocumented.

## A4. Subject search — what actually exists for Brunel / Thames Tunnel / tunnelling

All rows below were fetched live from `https://api.si.edu/openaccess/api/v1.0/search?q=…&api_key=DEMO_KEY`. Every returned record carried `"metadata_usage": { "access": "CC0" }`. **Confidence HIGH** for existence, IDs and metadata licence; **`UNVERIFIED`** for whether each has a downloadable image (`media_usage`), because none of these returns included a `media` block in the search payload.

**Row counts (HIGH):** `Brunel` → 843 · `Thames Tunnel` → 40 · `steam engine` → 5,036.

**Marc Brunel / Brunel family**

| Record ID | Title | Unit |
|---|---|---|
| `siris_sil_4317` | **Marc Isambard Brunel** (Clements, Paul, 1970) | SIL |
| `siris_sil_246163` | The life of Isambard Kingdom Brunel, civil engineer (1870) | SIL |
| `siris_sil_255547` | Isambard Kingdom Brunel, a biography (Rolt, 1957) | SIL |

**Thames Tunnel (the Episode 1 subject) — all SIL/NMAH, all metadata CC0**

| Record ID | Title |
|---|---|
| `nmah_1144472` | **broadside, Thames Tunnel** (NMAH, ID 1986.0610.03) |
| `siris_sil_261561` | A Perspective view of the Thames and the Thames Tunnel; History of the Thames Tunnel (1844) |
| `siris_sil_160362` | An explanation of the works of the tunnel under the Thames from Rotherhithe to Wapping (1840) |
| `siris_sil_160365` | … same title (1836) |
| `siris_sil_160364` | … same title (1837) |
| `siris_sil_377827` | An Explanation of the works … (1838, Burndy Library) |
| `siris_sil_285653` | Esquisses des travaux du passage … sous la Tamise … (1828, French) |
| `siris_sil_261531` | A brief account of the Thames Tunnel (1851) |
| `siris_sil_246327` | A memoir of the Thames tunnel (Law, Henry) |
| `siris_sil_261583` | A Perspective view of the Thames Tunnel (1830) |
| `siris_sil_368208` | Le Tunnel = Der Tunnel = Tunnel views (1840s) |

Note several are **telescopic peepshow** items — period hand-coloured plates of exactly the tunnelling works. These are the single richest CC0 seam for this episode. **Verify each record's `media_usage` before reuse** (see A1).

**Tunnelling / civil engineering generally (metadata CC0)**

| Record ID | Title |
|---|---|
| `siris_sil_157993` | Hudson River Vehicular Tunnel contract no. 4: specifications (1920) |
| `siris_sil_221673` | SHEEN TUNNELER, BORES AND LINES A TUNNEL (Tunnel & Mine Machinery Co, c.1927) |
| `siris_sil_338690` | Innovation and the rise of the tunnelling industry (West, 1988) |
| `siris_sil_51548` | Tunnels (Sandström, 1963) |
| `siris_sil_428458` | Notes on the report of the Economic Advisory Council Channel Tunnel Committee (1930) |

**Industrial/steam (metadata CC0, from the `steam engine` query):** `nmah_843855` (Framed Demonstration Model, Oscillating Marine Steam Engine) · `nmah_336302` (toy, accessory, steam engine) · `nmah_336329` (toy, engine, steam) · `nmah_842310`, `nmah_842312` (drawings, steam engine) · `nmah_1433105` (photograph, steam engine) · `nmah_1347189` (Stromberg Carlson CRT) · plus Smithsonian Libraries trade catalogues `siris_sil_298697`, `siris_sil_246275`, `siris_sil_245924`.

**Verified example of the metadata/media gap (HIGH):** `https://api.si.edu/openaccess/api/v1.0/content/edanmdm:nmah_336302?api_key=DEMO_KEY` returned `indexedStructured.online_media_type: ["Images"]` **but no `media` array and no `media_usage`** — only `metadata_usage.access: "CC0"`. This is exactly the trap described in A1. **Do not treat "has an image" as "image is CC0".**

## A5. Open Access vs the general si.edu collections site

- **Smithsonian Open Access** = the CC0/released subset, surfaced at `si.edu/openaccess`, `si.edu/search?edan_fq[0]=media_usage:CC0`, `3d.si.edu/cc0`, and the API/GitHub. Filter parameter confirmed verbatim from the OA homepage's "Just browsing" link: **`https://www.si.edu/search/images?edan_fq%5B0%5D=media_usage%3ACC0`** → i.e. `edan_fq[]=media_usage:CC0`. **HIGH.**
- **General collections** (`https://www.si.edu/object/{slug}:{id}`) includes all-rights-reserved and "usage conditions apply" objects. **HIGH** — the FAQ: *"If an item is not designated as CC0, it is subject to usage conditions"*, and non-CC0 commercial use requires written permission from `rightsmanager@si.edu`.
- The API stats prove the general collection is far larger than the OA release (42.65M total objects vs 17.43M CC0 records). **HIGH.**

---

# B. SCAN THE WORLD (MyMiniFactory)

## B1. Licence — **CC BY-NC-SA 4.0** (exact, verbatim)

**HIGH — fetched** `https://r.jina.ai/https://www.myminifactory.com/object/3d-print-4215` ("Nelson Mandela in Pretoria, South Africa" by Scan The World). The page's licence block reads, verbatim:

```
License
[BY-NC-SA](https://www.myminifactory.com/object-licensing)
  "Credit the designer when sharing this object."
  "If you remix, transform, or build upon the object, you must distribute
   your contributions under the same license as the original."
  "You may not use the object for commercial purposes"
  "You can remix this object and share your remix"
  → https://creativecommons.org/licenses/by-nc-sa/4.0/
```

So: the label is **`BY-NC-SA`** and the linked deed is **`creativecommons.org/licenses/by-nc-sa/4.0/`** → **CC BY-NC-SA 4.0**. Not 3.0. Not plain BY-SA. **HIGH.**

**Confirmed on a second, independent object** — `https://r.jina.ai/https://www.myminifactory.com/object/3d-print-damaged-german-stahlhelm-helmet-at-the-imperial-war-museum-london-6645`: identical `BY-NC-SA` block, identical `by-nc-sa/4.0` link, identical alt text including *"You may not use the object for commercial purposes"*. **HIGH.**

**Licence is NOT uniform across Scan the World's footprint.** The same initiative's uploads to Wikimedia Commons carry **CC BY-SA 4.0** (no NC):

**HIGH — fetched** `https://commons.wikimedia.org/wiki/File:Scan_the_World_-_Juno_Ludovisi.stl` (uploaded by `Jonathanbeck`, STW's co-founder, 2018):

> "This file is licensed under the Creative Commons Attribution-Share Alike 4.0 International license."
> Categories include `CC-BY-SA-4.0`, `STL files from Scan the World`.

`INFERENCE:` the Commons-era uploads (2017–2018) were BY-SA; the MyMiniFactory-hosted catalogue is now BY-NC-SA 4.0. **Do not rely on an STW model being BY-SA because a Commons mirror says so** — the authoritative licence is the one on the MyMiniFactory object page at download time.

**Licence IS uniform within the current MMF catalogue**, by policy: MyMiniFactory's licensing page presents free objects' licences as designer-selected per object, and every STW object sampled carried `BY-NC-SA 4.0`. `UNVERIFIED:` whether any individual STW object deviates — sample was n=2.

## B2. Scope — sculpture/art, or engineering?

**STW self-description (HIGH):** `https://r.jina.ai/https://www.myminifactory.com/scantheworld/about/`

> "**Scan the World** is the world's largest ecosystem of free to download, 3D printable objects of cultural significance. Every object originates from 3D scan data…"
> "112,000,000+ views · **25,000+ artefacts freed**"
> Pillars: CULTURAL HERITAGE · ACCESSIBILITY · EDUCATION · PRESERVATION
> Team: **Jonathan Beck (Co-Founder)**, Elisa D'Antona (Project Manager)

Per-object blurb (identical boilerplate on every STW object, **HIGH**):

> "Scan the World is a non-profit initiative introduced by MyMiniFactory, through which we are creating a digital archive of fully 3D printable **sculptures, artworks and landmarks** from across the globe for the public to access for free."

Wikimedia Commons' category description (**HIGH**): *"archive the world's sculptures, statues, artworks and any other objects of cultural significance using 3D scanning technologies to produce content suitable for 3D printing."*

**Catalogue size conflict (flagged):** the STW about page claims **"25,000+ artefacts freed"**, while the MMF profile page for the same account states **"12,446 objects"** / 12,539 followers, and localized profile pages read *"All Objects (12437)"*. **HIGH** (both fetched). Treat ~12.4k as the live MMF catalogue count.

**Does ANY engineering content exist?** Yes — but as *museum artefacts*, not engineering documentation.

| Object | URL | Why it counts |
|---|---|---|
| Damaged German Stahlhelm Helmet (Imperial War Museum, London) | `https://www.myminifactory.com/object/3d-print-damaged-german-stahlhelm-helmet-at-the-imperial-war-museum-london-6645` | Militaria/metalwork; licence BY-NC-SA 4.0; 8,541 views / 664 downloads |
| Sundial in Tower Hill, London | `https://www.myminifactory.com/object/3d-print-sundial-in-tower-hill-london-5648` | Instrument / landmark |
| David Harber Sundial, Putney, London | via `https://stlfinder.com/model/david-harber-sundial-in-putney-london-Oc8fbI88/2650480` | Instrument / landmark |
| Archaeological finds (category) | Wikimedia Commons `STL files of archaeological finds` | Period artefacts |

**Assessment (`INFERENCE`, MEDIUM):** STW content is overwhelmingly sculpture, statuary, portraits, funerary/monumental art and museum artefacts, organised by geography (`Scan the World > Europe > United Kingdom`). There is **militaria, horology/sundials, and landmark architecture**, which is *adjacent* to engineering heritage — but there is **no evidence of machinery, engines, bridges-as-structures, locomotives, tools, tunnelling equipment, or the Thames Tunnel / Brunel**. `UNVERIFIED:` a negative can't be proven without full-catalogue enumeration, and MyMiniFactory's search page is JS-rendered so `?query=steam+engine` returned no results to a text fetch. **For Episode 1, Scan the World is not a source of the tunnelling shield.**

## B3. Access gating and MMF's own overlay restrictions

**Gating:** object pages served anonymously show a **download affordance** and a `Login` link in the header. `MEDIUM / INFERENCE:` MyMiniFactory has historically required a free account to download; the fetched anonymous page showed the Download control, so I could not confirm whether login is enforced at click time. **`UNVERIFIED` — do not assume anonymous download.**

**MMF ToS adds restrictions WELL BEYOND the CC licence. This is the decisive finding.**
**HIGH — fetched** `https://r.jina.ai/https://www.myminifactory.com/pages/terms-and-conditions`, verbatim:

> "You may print or download portions of the materials from various areas of this website (**including through the use of our API**) **solely for your own non-commercial use** - unless there is a prior arrangement or agreement with My Mini Factory Ltd or the owner of the design regarding the commercial use of said items"

> "This website or any portion of this website may not be reproduced, redistributed, duplicated, adapted, copied, sold, resold, transmitted or otherwise exploited **for any commercial purpose** without the express written consent of myminifactory.com or its relevant licensors."

> "You may not access any content on the website (including, without limitation, 3D print files) **for any other reason except your non-commercial, personal use** solely as intended through the web interface."

> "You may not modify, copy, reproduce, republish, upload, post, transmit, or distribute any portion of the website contents without the prior express written consent of Myminifactory.com or the original content uploader or uploaders."

**Retroactive-change clause (HIGH, verbatim):**

> "MyMiniFactory reserves the right to change the terms, conditions, and notices at any time, and such modifications shall be effective immediately upon posting of such changes. … Your continued access of this website shall be deemed your conclusive acceptance of the modified agreement, and **the modified agreement shall apply to existing content uploaded to the website at the time of the modification**."

**Governance (HIGH):** "Myminifactory.com is owned by **My Mini Factory Ltd**, Registered Office: 51-53 Rivington Street, London, EC2A 3QB, United Kingdom, Company Registration Number: 09562672". Governing law: **England**; disputes → binding arbitration in England. Footer confirms: "Copyright, MyMiniFactory, 2026 / 51-53 Rivington Street, London".

**MMF Object Licensing page (HIGH — fetched** `https://r.jina.ai/https://www.myminifactory.com/pages/object-licensing`**)** — paid objects are far more restrictive than free ones:

> "**Standard Digital File Store License** … Digital files sold on MyMiniFactory through the digital file store have a **strict non-commercial, personal use only license**. You shall not share, sub-license, sell, rent, host, transfer, or distribute in any way the digital or 3D printed versions of this object, nor any other derivative work of this object… The objects may not be used in any way whatsoever in which you charge money, collect fees, or receive any form of remuneration."
> "**Official Content License** — ® & © All Rights Reserved … strict non-commercial, non-distribution license … may not be used for marketing, collecting money, fees, donations reimbursement or any remuneration purposes"

For **free** objects the page defers to per-object designer choice: *"Please check the license the designer has selected for their design on the object page."*

**Relevance to this brief:** the creator's stated model is "Blender + Python" using scanned geometry as a **reference/base for rendered Reels**. Even setting the CC NC element aside, **adapting, rendering and publishing MMF-hosted content on a monetised channel is squarely prohibited by MMF's own ToS** ("adapted", "for any commercial purpose", "except your non-commercial, personal use"). Note also CC's own guidance (see C4) that *"Explanations of NC do not modify the CC license"* — but here the platform ToS operates as a **separate contract** between the user and My Mini Factory Ltd, so it binds independently of the CC grant. **HIGH.**

## B4. API / bulk access

**`UNVERIFIED` — no Scan the World API or bulk route found.** No STW API, no dataset mirror, no GitHub repository for the catalogue was located. The only access paths are the MyMiniFactory web catalogue and MMF's search. MMF's ToS references "our API", but it is a **platform** API for store/creator operations, and the ToS simultaneously restricts API downloads to non-commercial personal use (quoted above). Effectively: **web catalogue only, and not for commercial use.**

## B5. Section B verdict

**Do not use Scan the World.** Two independent blockers:
1. **CC BY-NC-SA 4.0** — the NonCommercial element forbids the monetised use case (see C4 for the analysis, which applies identically).
2. **MyMiniFactory's own ToS** separately restricts all downloads and API access to non-commercial personal use and prohibits adaptation and commercial exploitation.

Secondary risk: **ShareAlike (SA)** would require any derivative Reel to be released under CC BY-NC-SA 4.0, which is incompatible with a monetised Instagram channel.

---

# C. SKETCHFAB

## C0. Corporate ownership — Epic **SOLD** Sketchfab to **KitBash**. Your "Clara" recollection is wrong.

**Your memory, corrected:** there is no "Clara". The buyer is **KitBash** (the company behind **KitBash3D** and **Greyscalegorilla**), operating the platforms through **KitBash SF Operations LLC**.

**HIGH — primary/company-adjacent sources:**
- **Sketchfab's own footer on every page fetched (live):** `© 2026, KitBash SF Operations LLC. All rights reserved.` — e.g. `https://sketchfab.com/terms`, `https://sketchfab.com/developers/data-api/v3`, `https://sketchfab.com/developers/download-api/downloading-models`.
- **Sketchfab's own DMCA agent block** in the Terms of Use: `KitBash SF Operations LLC, ATTN: DMCA AGENT, 8605 Santa Monica Blvd PMB 90726, West Hollywood, California 90069-4109, United States, dmca@sketchfab.com`
- **Sketchfab ToS §4.2.1(b) (verbatim):** *"Sketchfab and our affiliate, **KitBash SF Operations LLC ("KitBash")**, use User Content to improve … our internal safety tools ("Safety Tools") … and … our search and recommendation tools."*
- **GamesBeat, 10 August 2026** — `https://gamesbeat.com/kitbash-acquires-artstation-and-sketchfab-art-platforms-from-epic-games/`: *"Epic Games has sold ArtStation and Sketchfab to KitBash … There are no changes to how creators access or use ArtStation and Sketchfab."* Quotes **Banks Boutté, co-CEO of KitBash**, and **Bill Clifford, SVP of the Unreal Ecosystem at Epic Games**.
- Announcement URLs cited by GamesBeat: `https://sketchfab.com/blogs/community/kitbash-acquires-sketchfab-and-artstation` · `https://kitbash3d.com/pages/kitbash-acquires-sketchfab-and-artstation-kitbash3d` · `https://magazine.artstation.com/2026/08/kitbash-acquires-artstation-and-sketchfab/`.
- **`https://www.epicgames.com/site/news/kitbash-acquires-artstation-and-sketchfab`** exists but returns **HTTP 403** to automated fetch — `UNVERIFIED` as to its exact text (it is the primary press release; verify manually).

`MEDIUM:` `https://sketchfab.com/blogs/community/kitbash-acquires-sketchfab-and-artstation` returned HTTP 202 (bot challenge) on both direct and proxy fetch — cite GamesBeat + the footer instead.

**Timeline (HIGH):** Epic Games acquired Sketchfab in **2021**; Epic sold Sketchfab **and** ArtStation to KitBash, **announced ~10–12 August 2026** (third-party coverage dates 10 Aug 2026; DigitalProduction 12 Aug 2026; ixbt 15 Aug 2026).

### Post-acquisition licence / policy changes — **there IS a live contradiction**
**Terms of Use effective August 12, 2026** — i.e. the ToS was **re-issued on the acquisition date**.
But the separate **License Agreement** at `https://sketchfab.com/licenses` still states, **§1.9, verbatim**:

> "**"Sketchfab" means Sketchfab Inc., its parents, affiliates, subsidiaries, co-venturers and licensed affiliates. Sketchfab is a division of Epic Games, Inc. ("Epic").**"

**This is stale and now false** — Sketchfab is no longer an Epic division. Under the Terms of Use, *"Sketchfab, Inc., a Delaware corporation"* remains the contracting entity named in §13, while the footer and ToS §4.2.1(b) point to KitBash SF Operations LLC. **HIGH** — all fetched live. This matters: if you ever need to know **who** your licence counterparty is, the public documents are internally inconsistent as of 17 Sep 2026.

### Retroactive-change risk — **YES, and it is explicit**
**HIGH — ToS §4.1, verbatim:**

> "You agree that your use of any User Content downloaded from the Services will always be subject to the **most-current version of the License Agreement or Creative Commons license**, as applicable … accordingly, you agree that your continued use of any such User Content constitutes your acceptance of the terms of any **new version** of the License Agreement or Creative Commons license, applicable to such User Content, **as we may update from time to time**."

**HIGH — ToS §4.6, verbatim:**

> "We reserve the right to remove User Content from the Services and **terminate any licenses thereto**, in whole or in part, without prior notice, for any reason or for no reason at all."

`INFERENCE:` For **Creative Commons** licences this clause is arguably ineffective — a CC grant, once made, is irrevocable, and CC's own guidance says platform explanations *"never form part of the CC license"*. **But for Sketchfab's own Store licences (Standard/Editorial/Free Standard), §4.1 is a live retroactive-change and termination hook.** Practical consequence: **archive your downloads and screenshot the licence + upload date at time of download**; do not rely on a model remaining under the same terms.

Also note **ToS §3.3 (verbatim):** *"Any commercial exploitation of the Services or Sketchfab Content without express prior written permission from us or the applicable rights holder is strictly prohibited."* Read carefully — *"Sketchfab Content"* is defined in §3.1 to **exclude** User Content, so this does **not** restrict commercial use of user-uploaded CC models; it restricts the platform's own content (UI, branding, data). **HIGH** (definitions fetched).

## C1. Licence filter mechanics — the exact accepted values

**The API's authoritative licence list, fetched live (HIGH)** — `https://api.sketchfab.com/v3/licenses` returns exactly **10** licences:

| `slug` | `label` | `uid` | `requirements` (verbatim) | `url` |
|---|---|---|---|---|
| `by` | CC Attribution | `322a749bcfa841b29dff1e8a1bb74b0b` | "Author must be credited. Commercial use is allowed." | creativecommons.org/licenses/by/4.0/ |
| `by-sa` | CC Attribution-ShareAlike | `b9ddc40b93e34cdca1fc152f39b9f375` | "Author must be credited. Modified versions must have the same license. Commercial use is allowed." | …/by-sa/4.0/ |
| `by-nd` | CC Attribution-NoDerivs | `72360ff1740d419791934298b8b6d270` | "Author must be credited. Modified versions can not be distributed. Commercial use is allowed." | …/by-nd/4.0/ |
| `by-nc` | CC Attribution-NonCommercial | `bbfe3f7dbcdd4122b966b85b9786a989` | "Author must be credited. **No commercial use.**" | …/by-nc/4.0/ |
| `by-nc-sa` | CC Attribution-NonCommercial-ShareAlike | `2628dbe5140a4e9592126c8df566c0b7` | "Author must be credited. **No commercial use.** Modified versions must have the same license." | …/by-nc-sa/4.0/ |
| `by-nc-nd` | CC Attribution-NonCommercial-NoDerivs | `34b725081a6a4184957efaec2cb84ed3` | "Author must be credited. **No commercial use.** Modified versions can not be distributed." | …/by-nc-nd/4.0/ |
| `cc0` | CC0 Public Domain | `7c23a1ba438d4306920229c12afcb5f9` | "Credit is not mandatory. **Commercial use is allowed.**" | creativecommons.org/publicdomain/zero/1.0/ |
| `free-st` | Free Standard | `72eb2b1960364637901eacce19283624` | "Under basic restrictions, use worldwide, on all types of media, commercially or not, and in all types of derivative works" | sketchfab.com/licenses |
| `st` | Standard | `783b685da9bf457d81e829fa283f3567` | (same as above) | sketchfab.com/licenses |
| `ed` | Editorial | `5b54cf13b1a4422ca439696eb152070d` | "Use only in connection with events that are newsworthy or of public interest" | sketchfab.com/licenses |

**The search endpoint takes SLUGS, not UIDs and not `cc-*` prefixed names. Verified by live request (HIGH):**

| Request | Result |
|---|---|
| `https://api.sketchfab.com/v3/search?type=models&downloadable=true&licenses=cc0&q=steam%20engine` | **200** — 6 CC0 results, e.g. RG Ross & Sons Steam Hammer (`d80b52dc800e4c76b6b27749bbd8e782`), Boiler from the puffer "VIC 32" (`884ed11e38054aa48a3db1d9025c881d`), QE2 Starboard High Pressure Turbine Pattern (`8e135c1a917c476a98f011a48c4192c7`), all under `ScottishMaritimeMuseum` |
| `…&licenses=by-nc-sa&q=steam%20engine` | **200** — Bodie California Sawmill (`e3ab52b07207448cbedccb28c5e9fa10`), `license.label: "CC Attribution-NonCommercial-ShareAlike"` |
| `…&licenses=by&q=tunnel` | **200** — 24 results (Futatsugoya Tunnel, Leake Street Graffiti Tunnel, etc.) |
| `…&licenses=cc-by&q=tunnel` | **400** — `"cc-by is not one of the available choices."` |
| `…&licenses=322a749bcfa841b29dff1e8a1bb74b0b&q=…` | **400** — `"…is not one of the available choices."` (a **UID** is rejected) |
| `…&licenses=7c23a1ba438d4306920229c12afcb5f9&q=…` | **400** — rejected (the **CC0 UID** is rejected) |
| `…&licenses=invalid-slug` | **400** — `"Select a valid choice. invalid-slug is not one of the available choices."` |

**Answer to your enumeration question:** `cc0`, `by`, `by-sa`, `by-nd`, `by-nc`, `by-nc-sa`, `by-nc-nd` (plus store licences `free-st`, `st`, `ed`). **Not** `cc-by`, **not** `cc-by-sa`, **not** `cc-by-nc-sa`, **not** UIDs.

**Website URL parameters:**
- **`features=downloadable` — HIGH, verified from Sketchfab's own navigation markup.** The site's "Downloadable" nav link is `https://sketchfab.com/3d-models?date=week&features=downloadable&sort_by=-likeCount`, and the same value appears in your own URL. This is the canonical downloadable filter.
- **`licenses={slug}` on the website — MEDIUM.** `https://sketchfab.com/search?features=downloadable&licenses=…` returns HTTP 200 but the page is a JavaScript shell; a text fetch returns only the cookie banner, so the UI's own value set could not be observed. The API definitively uses these slugs, and Sketchfab's April 2021 announcement `https://sketchfab.com/blogs/community/refine-downloadable-model-searches-with-new-license-filters/` documents the licence *categories* offered as search filters. `INFERENCE:` the website `licenses=` parameter accepts the same slug strings as the API. **Verify in a real browser before relying on it; prefer the API** (`/v3/search?type=models&downloadable=true&licenses=cc0`), which is unambiguous and machine-checkable.
- Also useful, from the same nav markup: `is_ai=0` / `is_ai=1` (Human Created / AI Generated) — a **NoAI / AI-generated** filter now exists. **HIGH.**

## C2. Downloadable vs view-only

- **`isDownloadable: true`** is a real field on every model object returned by the search API. **HIGH** (present on every result fetched).
- **Filter:** `downloadable=true` on `/v3/search`. **HIGH** (verified 200 with only `isDownloadable: true` results).
- **Every CC licence on Sketchfab is a *licence to use*, not a promise a file exists.** A licensor may publish a model under CC BY and **not** enable downloads. `INFERENCE (HIGH-quality):` because the API filters `downloadable` and `license` as **independent** dimensions, the only safe query is `downloadable=true&licenses={slug}` — exactly what the task asks. A CC-BY model that is not downloadable grants you no file.
- **Header text on the licence blog post (verbatim):** "CC BY-NC – Non-Commercial — **You cannot use the downloaded model commercially.**" and "CC0 – Public Domain — You may distribute, remix, adapt, and build upon the downloaded model in any medium or format, with no conditions." **HIGH.**
- **Do some models forbid download even under a CC licence?** Yes — `isDownloadable` is a per-model setting independent of licence. `INFERENCE:` and the Download API returns **`400 Bad Request. Model is not downloadable.`** for such models — that error description is in the official spec (below).

## C3. Download API, OAuth2, Data API, rate limits

**Download API — exact endpoint (HIGH)** from `https://sketchfab.com/developers/download-api/downloading-models`:

```
GET https://api.sketchfab.com/v3/models/{UID}/download
Authorization: Bearer {INSERT_USER_OAUTH_ACCESS_TOKEN}
```

Verbatim curl from the docs:

```bash
curl 'https://api.sketchfab.com/v3/models/{UID}/download' \
  -H 'authorization: Bearer {INSERT_USER_OAUTH_ACCESS_TOKEN}'
```

Response (docs' own example):

```json
{
  "gltf": { "url": "https://sketchfab-prod-media.s3.amazonaws.com/archives/…/gltf/…",
            "size": 45388265, "expires": 300 },
  "usdz": { "url": "https://sketchfab-prod-media.s3.amazonaws.com/archives/…/usdz/…",
            "size": 6394777, "expires": 300 }
}
```

Docs verbatim on the flow:
> "Downloading a model requires the user to be authenticated with a Sketchfab account."
> "To prevent abuse, models cannot be downloaded directly. Your app must request a download first."
> "Once you've obtained a link to download an archive, you can download it by making a HTTP GET request. No authentication is required. The link already contains a token that has a short expiration date. Also, for that reason, **you should not cache** the URL."
> glTF download is a **ZIP** (`scene.gltf`, `scene.bin`, `textures/`); USDZ is supplied directly.

**Is a token needed for CC0 vs CC-BY downloads? — YES, a token is needed for BOTH.**
**HIGH:** the endpoint's `security` is `[{ "Token": [] }]` in the official spec, and the docs state unconditionally that "Downloading a model requires the user to be authenticated with a Sketchfab account." The licence is irrelevant to *authentication*; it governs *what you may then do* with the file.
**HIGH — ToS §4.2.4 verbatim:**
> "Users accessing and downloading User Content through the download API operated by Sketchfab **shall be authenticated** and it is expressly agreed that: (i) the use of the download API is governed by these Terms and each User's plan; and (ii) **the authenticated User accessing and downloading the User Content shall be responsible for complying with the terms of the license governing said User Content.**"

**Legal point (`INFERENCE`, HIGH-quality):** the licence obligation sits on **you, the downloading user**, not on Sketchfab. Sketchfab is not warranting anything about a model's licence — see the Store License Agreement §5: *"Sketchfab makes no representations or warranties regarding Licensor's right or authority to grant any rights in or to any Licensed Material."* You must record the licence yourself.

**OAuth2 (HIGH)** — `https://r.jina.ai/https://sketchfab.com/developers/oauth`:
- Authorize (code flow): `https://sketchfab.com/oauth2/authorize/?response_type=code&client_id=[CLIENT_ID]&redirect_uri=[REDIRECT_URI]`
- Authorize (implicit): `https://sketchfab.com/oauth2/authorize/?state=123456789&response_type=token&client_id=[CLIENT_ID]`
- Token exchange: **`POST https://sketchfab.com/oauth2/token/`**, `Content-Type: application/x-www-form-urlencoded`, body `grant_type=authorization_code&code=…&client_id=…&client_secret=…&redirect_uri=…`
- Password grant: `POST https://sketchfab.com/oauth2/token/` with `grant_type=password&username=…&password=…` and header `Authorization: Basic base64(client_id:client_secret)`
- Authenticated call header: `Authorization: Bearer [ACCESS_TOKEN]`
- Token lifetime: **"Access tokens last 1 month."** Refresh via `grant_type=refresh_token` (not available in the Implicit flow).
- **App registration is manual:** "To register your app, simply **contact us** with the following information: Application name, Grant type, Redirect URI, Username." → you get a Client ID + Client Secret. **HIGH.** `INFERENCE:` plan for a manual approval step; you cannot self-serve OAuth credentials.
- **Alternative that avoids OAuth entirely:** from the Data API page — *"Some endpoints are public, while others require authentication with OAuth or your **API Token**."* Header form (from the official spec description): **`Authorization: Token {INSERT_API_TOKEN_HERE}`**. API tokens are obtained at `https://sketchfab.com/settings/password`. **HIGH** — and this is almost certainly the simplest path for a solo creator scripting downloads in Python.

**Data API (HIGH)** — `https://sketchfab.com/developers/data-api/v3` and the machine-readable spec at **`https://docs.sketchfab.com/data-api/v3/swagger.json`** (the Swagger UI at `https://docs.sketchfab.com/data-api/v3/index.html` is JS-only). Spec header verbatim:
> "Some endpoints require users to be authenticated. Users can log in with OAuth2 (preferred), or an API Token. … for OAuth2: `Authorization: Bearer {…}` … for API Token: `Authorization: Token {…}`"
> **Pagination:** "By default, pages contain 24 items. You can use the `count` parameter to change the number of items per page. **This parameter is capped to 24: it will be ignored if a higher value is passed.**" → pagination is cursor-based (`cursors.next` / `next` full URL).
> **"Limits and quotas" — verbatim:** "Calls to the API can be throttled to limit abuse. When your application is being throttled, it will receive a `429 Too Many Requests` response. This means that you must wait before making more requests."

**Search/model-list parameters confirmed present in the spec (HIGH):** `downloadable` (boolean, "Retrieves downloadable models"), `licenses`, `q`, `type=models`, `tags`, `categories`, `user`, `staffpicked`, `animated`, `has_sound`, `restricted`, `published_since`, `created_since`, `max_face_count`, `max_vertex_count`, `sort_by`, plus archive-shape filters (`archives_flavours`, max size / face count / vertex count / texture count / texture resolution). Note: the `licenses` enum values were **not** listed in the spec body — they were established empirically (C1).

**Rate limits — exact numbers: `UNVERIFIED`.** The spec names throttling and HTTP 429 but publishes **no numeric quota** (no per-hour/per-day figure anywhere in the spec, the Data API page, or the Download API page). `https://sketchfab.com/developers/guidelines` returned HTTP 202 (bot challenge) on repeated attempts and could not be read. **Do not invent a number** — implement 429 backoff and, if you need a hard figure, contact `help.sketchfab.com`.

**`/v3/models/{uid}/download` responses (HIGH, from the spec):** `200` Success → `ModelDownload` · `400` "Bad Request. **Model is not downloadable.**" · `401` "Unauthorized. User token is not valid or missing." · `403` Permission Denied · `404` "Not Found. Model does not exist." · `429` "Too many requests."

## C4. CRITICAL LEGAL QUESTION — Are CC BY-NC models usable on a monetised Instagram channel?

### The definition, verbatim

**HIGH** — `https://wiki.creativecommons.org/wiki/NonCommercial_interpretation` (CC's own steward page on NC):
> "In each of these licenses, NonCommercial is expressly defined as follows: **"NonCommercial means not primarily intended for or directed towards commercial advantage or monetary compensation."**"
> "The definition is **intent-based** and intentionally flexible… The inclusion of "primarily" in the definition recognizes that no activity is completely disconnected from commercial activity; **it is only the primary purpose of the reuse that needs to be considered.**"

Sketchfab's own restatement (HIGH, `/v3/licenses`): `by-nc` → requirements field: **"Author must be credited. No commercial use."**

### CC's own guidance that decides this case

**HIGH**, same page, verbatim:
> "**NonCommercial turns on the use, not the identity of the reuser.** The definition of NonCommercial depends on the primary purpose for which the work is used, not on the category or class of reuser."
> "**Reusers may make NonCommercial uses only, even when reusing NC material with other works.** The NC licenses limit reusers to NonCommercial uses of the work only, which includes when the work is used in a collection or when it is adapted. … For an example of an adaptation, **an NC song may be used as the basis for a video where the visual elements are under a different license such as the BY license. When the music video is distributed as a whole, it may not be used commercially because of the NC license of the song.**"
> "**Explanations of NC do not modify the CC license.** Some licensors or website providers state expectations or interpretations about what NC means. Those explanations never form part of the CC license …"
> "**The NonCommercial term does not limit uses otherwise allowed by limitations and exceptions to copyright.** … a person may commercially use an NC-licensed work for purposes of criticism in jurisdictions where this is fair use or otherwise covered by an exception to copyright."
> "NC licenses do not qualify as "open licenses" under the Open Definition, and works licensed under an NC license are not considered Free Cultural Works."

The song/video example is **directly on point**: an NC-licensed 3D model rendered into a Reel whose other elements are CC BY / CC0 / your own work → the composite Reel carries the NC restriction on the whole.

### Applying it to each monetisation channel in the brief

| Monetisation | Commercial? | Why |
|---|---|---|
| **Reels ad revenue / Reels bonus / in-stream ads** | **YES** | Direct monetary compensation; the Reel is *"directed towards … monetary compensation."* |
| **Brand sponsorship / paid partnership** | **YES** | Compensation from a third party for the post. Sketchfab's Editorial licence names this explicitly: *"any advertorial or any other use for which monetary or nonmonetary compensation is provided by a third-party advertiser or sponsor."* |
| **Brand deals / product placement** | **YES** | Same. |
| **Affiliate links** | **YES** | Commission = monetary compensation, and it makes the content a promotional vehicle. |
| **A channel that "merely exists to promote the creator's own paid work"** | **YES** | *"commercial advantage"* — the CC definition covers advantage, not only cash. This is the classic NC failure mode. |
| Ad revenue is the *only* commercial aspect and is incidental to an otherwise non-promotional account | **Grey — do not rely on it.** | The Smithsonian FAQ's blog/advertising carve-out (A1) is a Smithsonian-specific concession for *"usage conditions"*, **not** a CC NC rule. CC's own page offers no equivalent. |

### VERDICT — clear and unhedged

**CC BY-NC, CC BY-NC-SA and CC BY-NC-ND models are NOT usable on this channel.**

The brief describes a channel with ad revenue, sponsorships, brand deals, affiliate links, and a purpose of promoting the creator's own paid work. That is *"primarily intended for or directed towards commercial advantage or monetary compensation"* on every reading, including CC's own flexible, intent-based one. Because the NC restriction flows through **adaptations and collections**, and a Reel is both an adaptation (rendered/animated/composited) and a collection (model + imagery + AI voiceover), **the entire Reel inherits the NC restriction**, and the monetisation is a breach of the licence.

**Corollaries:**
- **CC BY-ND / CC BY-NC-ND (NoDerivatives)** are also a problem for this workflow even though BY-ND permits commercial use. `INFERENCE (MEDIUM-HIGH):` rendering a model into a 9:16 Reel involves adaptation (re-lighting, re-camera, compositing, possibly re-topology in Blender). ND requires you to *"not distribute modified versions"*; a materially altered render likely qualifies as a derivative. **A straight, unmodified turntable render of a BY-ND model is the only defensible BY-ND use, and even that is arguable.**
- **The NonCommercial element is not curable by attribution, by a disclaimer, or by "not monetising that specific Reel".** A single sponsored Reel taints the channel's use of that asset; and per CC, *"the primary purpose of the reuse"* is assessed at the level of the use, not per-post accounting tricks.
- **The genuine escape hatch** is an **exception or limitation** — fair use (US) / fair dealing (UK/AU). CC states NC *"does not limit uses otherwise allowed by limitations and exceptions to copyright."* For a short critical/commentary Reel about the history of engineering, a fair-use argument is *arguable* but is a **legal-risk position, not a licence position**, it is jurisdiction-specific, and it is outside the scope of a "no legal review" workflow. `INFERENCE:` do not build a channel on it.
- **ShareAlike (SA)** compounds it: any derivative must itself be released under the same NC-SA licence, which is incompatible with a monetised channel.

**Practical rule for this channel: download only `cc0`, `by`, and (with watchfulness) `by-sa`. Never `*-nc*`. Avoid `*-nd`.**

## C5. Store / paid models — do you get commercial rights?

**YES — "Standard" is a commercial licence; "Editorial" is not.**

**HIGH** — `https://r.jina.ai/https://sketchfab.com/licenses` (License Agreement, "Simple Version"), verbatim:

> "**What is the difference between the editorial and standard license?** Certain 3D assets are available under only an "editorial" license, which has certain restrictions. In particular, those assets **(a) cannot be used for any commercial or promotional use; (b) cannot be used to suggest sponsorship, affiliation, or association with any person, brand, or company; and (c) can be used in only works that comment on or criticize the subject matter of the assets or newsworthy or public interest events associated with them** (e.g., news articles, critical reviews, documentaries, etc.). You may edit an asset only if its editorial quality is not altered."
> "A **standard license** does not have all of the restrictions that apply to an editorial license, but there are some restrictions detailed below. **In both cases, others can do the same, as none of the licenses on the Sketchfab Website are exclusive.**"

**Tier list — there are THREE store/standard tiers, plus the four CC families (HIGH, `/v3/licenses`):** `free-st` "Free Standard", `st` "Standard", `ed` "Editorial". (There is **no** "Extended" tier — your recollection of "Editorial / Standard / Extended" is wrong; the third tier is **Free Standard**, not Extended.)

**Standard licence restrictions that matter to you (HIGH, verbatim §2.2):**
- "(b) **sell, license, distribute or otherwise make available the Licensed Material as a stand-alone file** … or in a way that allows third parties to use, download, extract or access the Licensed Material as a stand-alone file"
- "(c) distribute the Licensee Work if (i) it is so similar to the original Licensed Material … that the Licensee Work cannot qualify as an original work of authorship or (ii) **the primary value of the Licensed Work lies with the Licensed Material itself**"
- "(g) incorporate the Licensed Material into a logo, corporate name, trademark…"
- "(f) directly or indirectly **promote alcoholic beverages, tobacco, gambling, weapons or explosives**" ← relevant if you ever cover armaments engineering
- §2.6: if used in connection with an unflattering/controversial subject, add a statement that it is *"for illustrative purposes only"*

**Social-media clause — important for Instagram (HIGH, verbatim §2.8):**
> "If the Licensed Material is used on **any social media platform** or other third-party website, (i) **any rights granted by this Agreement to Licensee shall automatically be revoked in the event that the third-party website seeks to exploit purported rights to the Licensed Material contrary to the terms of this Agreement**, and (ii) in such event, upon request, Licensee shall remove any Licensed Material from such platform or website."

**Credit (HIGH, §3.2, verbatim):** *"If Licensed Material is used in an audio/visual production in either an editorial context or a non-editorial context but where credits are accorded to other providers of licensed material, credit shall be accorded, where technically feasible, in equal size and comparable placement to such credit(s), substantially in the following form: "[Video/Imagery] supplied by [Licensor]"."*

**Penalty for misuse (HIGH, §10, verbatim):** *"you agree to pay to Sketchfab a fee **equal to up to 25 times the amounts paid hereunder** for the unauthorized use of the Licensed Material."*

**Gate-of-rights (HIGH, §1.7, verbatim):** *"You acknowledge and agree that you are licensing the Licensed Material from **Licensor, not from Sketchfab**, and that Sketchfab has no obligation to support or maintain the Licensed Material."* Combined with §5's blanket warranty disclaimer, **Sketchfab does not stand behind a seller's rights** — you bear the risk that the uploader had no right to sell you the model.

**Summary:** buying a **Standard** model does grant broad **commercial** rights (royalty-free, worldwide, all media, derivative works) subject to the no-standalone-file, no-primary-value, no-trademark and no-vice promotion restrictions and the social-media revocation hook. **Editorial** is unusable for a monetised, sponsored channel. **Crediting is contractually required where credits are given to others.**

---

# CONSOLIDATED RECOMMENDATIONS FOR EPISODE 1

**Pre-cleared (no legal review needed):**
1. **Smithsonian CC0** — Thames Tunnel records (`nmah_1144472`, `siris_sil_261561`, `siris_sil_160362/160364/160365/377827`, `siris_sil_285653`, `siris_sil_261531`, `siris_sil_246327`, `siris_sil_261583`, `siris_sil_368208`) and Brunel records (`siris_sil_4317`, `siris_sil_246163`, `siris_sil_255547`). **Action: pull each via `/content/{url}`, confirm the `media` block and `media_usage` is `CC0`, and only then use.** Metadata CC0 alone is not enough.
2. **Smithsonian 3D** — only models surfaced under `https://3d.si.edu/cc0`. `INFERENCE:` expect essentially **no** Brunel/engineering 3D; do not budget time for it.
3. **Sketchfab `cc0` and `by` (and `by-sa` with care)** via `https://api.sketchfab.com/v3/search?type=models&downloadable=true&licenses=cc0&q=…`, downloaded through `GET /v3/models/{uid}/download` with an **API Token** (`Authorization: Token …`) from `https://sketchfab.com/settings/password`. Log the `license.label`, `user.username`, model `uid` and download date per asset. Real CC0 engineering-adjacent material **does exist** — verified examples: RG Ross & Sons Steam Hammer `d80b52dc800e4c76b6b27749bbd8e782`, VIC 32 Cochran boiler `884ed11e38054aa48a3db1d9025c881d` and `fb84ddbabd554f7e9b5b2d34b9b47be5`, QE2 turbine pattern `8e135c1a917c476a98f011a48c4192c7` and `96d548dfc5d943a8a5cfcc07ebfd1618` (all `CC0 Public Domain`, all under `ScottishMaritimeMuseum`, tagged `industrial-heritage`, `photogrammetry`, `scanningthehorizon`).
4. **Build the tunnelling shield in Blender from the CC0 period engravings** — this is both the safest and the strongest route, and it sidesteps every NC/ND problem entirely.

**Prohibited:**
- Anything **`by-nc`, `by-nc-sa`, `by-nc-nd`** on Sketchfab, and **all of Scan the World** (CC BY-NC-SA 4.0 **plus** MMF's blanket non-commercial ToS).
- Anything Smithsonian marked **"usage conditions apply"** / "no known copyright restriction".
- Anything in the **Sketchfab Store "Editorial"** tier.

**Housekeeping:**
- Do **not** put "Smithsonian", "SI", or any museum name in the channel name/handle/nickname — explicitly required by the FAQ even for CC0 content. A bio mention is permitted.
- Keep a licence evidence log (asset URL, licence string, uploader, fetch date, screenshot). This is essential given Sketchfab ToS §4.1 (retroactive change), §4.6 (licence termination) and §5 (no warranty of licensor rights).
- Consider the **NoAI** tag: Sketchfab ToS §5/§15 lets uploaders mark content `NoAI`, and using NoAI Content as an **input to a Generative AI Program** is prohibited. Your **AI voiceover** does not consume the model, but if you ever feed a downloaded model into a generative 3D/AI pipeline, check the tag. **HIGH.**

**Item to verify manually (could not be automated):**
- `https://www.epicgames.com/site/news/kitbash-acquires-artstation-and-sketchfab` — HTTP 403 to fetch; open in a browser to capture the exact primary press-release wording and date.
- `https://sketchfab.com/developers/guidelines` — HTTP 202 to fetch; may contain the numeric API rate limits that the Swagger spec does not publish.
- The live Smithsonian API docs (`https://edan.si.edu/openaccess/apidocs/`) render via JS — open in a browser to confirm the full parameter and field list.
