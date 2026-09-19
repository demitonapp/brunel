# Evidence — the long-form receipts

**Do not start here.** Start at
[`../3d-asset-licensing-master-2026-09-17.md`](../3d-asset-licensing-master-2026-09-17.md). Its §3
(source-by-source findings, 15 sources) and §4 (legal analysis) are the merged, decision-ready form
of everything in this directory, and §1 is the table you actually act on.

These four files are what §3 and §4 were compressed *from*: the verbatim licence strings, the exact
API signatures, the per-item record IDs, and — the part a summary cannot carry — the record of what
could **not** be verified and why.

| File | Covers | Why it survives the summary |
|---|---|---|
| [`3d-asset-licensing-report-2026-09-17.md`](3d-asset-licensing-report-2026-09-17.md) | Smithsonian Open Access, Scan the World / MyMiniFactory, Sketchfab | Exact licence-filter values, the Sketchfab ownership correction, and which hosts sat behind a bot wall |
| [`licensing-research-monetised-reels-2026-09-17.md`](licensing-research-monetised-reels-2026-09-17.md) | Internet Archive, Library of Congress, HABS/HAER, Chronicling America | Records `loc.gov` as **UNVERIFIED by direct fetch** (Cloudflare 403 on every UA tried). The summary states conclusions; only this file states that they were not live-checked |
| [`licensing-research-smg-europeana.md`](licensing-research-smg-europeana.md) | Science Museum Group, Europeana | Live API licence fields showing **zero CC0 images** at SMG, against the expectation that there were many. Contradictions are recorded here, not in the summary |
| [`cc-attribution-monetised-reels-advice.md`](cc-attribution-monetised-reels-advice.md) | CC mechanics: commercial use, TASL attribution, the NC-scan-of-a-PD-object wrapper problem | The full reasoning and every authority cited. §4 of the master is its conclusion, not its argument |

All four were fetched live on **17 September 2026**. Licence terms change; the master's §6
verification ledger is the thing to re-run, not these.

---

## The gap this directory currently has

Nothing in the repo links to any of these files, and nothing links to the master either. Meanwhile
`spec/ep01/legal/licences.json` carries one asset — `lic_placeholder_brunel_museum`, licence `unknown` — which
**blocks `licencegate`**, and therefore blocks `deliver --publish` for every episode.

2,847 lines of licence research and a register with a placeholder in it is the same failure the
harness keeps finding in its own code: the evidence exists, and it is wired to nothing. The fix is
to populate `spec/ep01/legal/licences.json` from the master's §1 decision table, not to do more research.
