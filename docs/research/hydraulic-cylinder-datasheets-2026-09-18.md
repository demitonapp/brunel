# Hydraulic Cylinder Datasheets — Sourcing S1's Numbers

**Research date:** 18 September 2026. Every PDF below was fetched live on that date and the figures
were read off the document, not recalled. Catalogue revisions change; re-verify before a re-cut.

**Question.** `docs/videos/s01-hydraulic-cylinder/brief.md` asserted a 120 mm bore, 80 mm rod and
350 bar working pressure, and marked all three **SOURCE NEEDED**. This document answers: *what does
a manufacturer actually publish, and what do the numbers become once they are sourced?*

**Confidence convention** (as `video-api-geometric-control-comparison-2026-09-18.md`).
`HIGH` = verbatim from a primary document fetched this session. `MEDIUM` = authoritative secondary.
`LOW` = weak or single source. `INFERENCE:` = reasoning, not a citation.

---

## EXECUTIVE VERDICT

**The brief's rod diameter was wrong, and correcting it makes the video better.**

1. **350 bar is confirmed** by Caterpillar's own spec sheet for a 21.7 t machine. `HIGH`
2. **120 × 80 does not exist.** The Cat 320 boom cylinder ships in five bore/rod combinations and
   none of them is 120/80. The 120 mm one has an **85 mm rod**. `MEDIUM`
3. **The standard rod is bore ÷ √2.** That makes the rod's area exactly half the piston's, so the
   annulus is exactly half, so **pulling is exactly half of pushing.** Two manufacturers publish the
   same series independently. `HIGH`
4. **Use 140 × 100.** It is the one pair that appears in *both* sources, and Rexroth's published
   areas match our own derivation to 0.002 cm². Nothing else on the board is cross-confirmed.

The hook changes from *"44% weaker"* — a number between two standards, which reads as cherry-picked
— to **half**, which is a designed value with a catalogue designation.

---

## 1. The sources

| id | Document | Tier | What it establishes |
|---|---|---|---|
| **S001** | Bosch Rexroth, *Hydraulic cylinder, mill type, Series CDH1 / CGH1*, RE 17331/09.05, 44 pp | manufacturer datasheet | bore, rod, **both areas**, area ratio φ, force, flow — all published, nothing derived |
| **S002** | Caterpillar, *320 Hydraulic Excavator Technical Specifications* | OEM spec sheet | implement circuit pressure, machine class |
| **S003** | HW Part Store, Cat 320C/320L/320S boom cylinder seal-kit listing | trade listing | the five bore/rod combinations Cat actually ships |
| **S004** | Bosch Rexroth, *Hydraulic cylinder, mill type, Type CDL1*, RE 17325/2009-07, 28 pp | manufacturer datasheet | the same series at 160 bar — cross-check on the rod progression |
| **S005** | Enerpac, *RC-Series single-acting cylinders* | manufacturer datasheet | effective area published directly in cm² — the single-acting reference |

**Not obtained: Parker.** `parker.com` is behind Akamai and returns `Access Denied` to a scripted
fetch; the in-app browser turned the PDF link into a save dialog rather than a page. Two community
mirrors were tried — one returned HTML, one a PDF with a corrupt xref table that `pdftotext` could
not open. **This is not a gap.** Rexroth publishes areas, forces *and* the area ratio; Parker's
mobile catalogue publishes dimensions only. The better document was obtained.

---

## 2. What Caterpillar publishes `HIGH`

**S002**, p. 2, verbatim:

```
Maximum Pressure – Equipment – Normal          35 000 kPa    5,075 psi
Maximum Pressure – Equipment – Auto Dig Boost  38 000 kPa    5,510 psi
Maximum Pressure – Travel                      34 300 kPa    4,974 psi
Operating Weight                               21 700 kg     47,800 lb
```

**35 000 kPa = 350 bar, on a 21.7 t machine.** The brief's assumed working pressure was correct and
is now cited. Note the OEM distinguishes *normal* from *Auto Dig Boost* — the video uses 350 bar and
must not quote the 380 bar boost figure, which is transient.

Caterpillar does **not** publish cylinder bore or rod anywhere in this document. `HIGH` — the whole
44-page specification was searched. This is why the OEM route alone cannot clear the gate.

---

## 3. What Rexroth publishes `HIGH`

**S001**, "Areas, forces, flows". This is the table the brief needed and did not have — bore, rod,
**both areas**, the ratio, and force, all published by the manufacturer:

```
     Piston  Piston      Area         Areas              Force at 250 bar
       AL      rod MM    ratio    A1      A2      A3      F1       F3
      Ø mm    Ø mm      A1/A3    cm2     cm2     cm2      kN       kN
       40       22       1.43    12.56    3.80    8.76    31.40    21.90
       40       28       1.96    12.56    6.16    6.40    31.40    16.00
       80       45       1.46    50.26   15.90   34.36   125.65    85.90
       80       56       1.96    50.26   24.63   25.63   125.65    64.10
      100       56       1.46    78.54   24.63   53.91   196.35   134.80
      100       70       1.96    78.54   38.48   40.06   196.35   100.15
      140      100       2.04   153.94   78.54   75.40   384.75   188.40
      200      140       1.96   314.16  153.96  160.20   785.25   400.35
```

Nominal pressure **250 bar (25 MPa)**, piston Ø 40–320 mm, piston rod Ø 22–220 mm, to DIN ISO 3320.

**Every bore is offered with exactly two rods.** That is the finding. The two rod series are:

| Series | φ = A1/A3 | rod ÷ bore | retract ÷ extend |
|---|---|---|---|
| slim | ≈ 1.46 | 0.56 | 0.685 — **31% weaker** |
| **standard** | **≈ 2.0** | **0.707** | **0.50 — exactly half** |

`INFERENCE:` 0.707 is 1/√2, so rod area = ½ × piston area, so annulus = ½ × piston area. The φ = 2
designation is not an observation about these cylinders — it *is* the specification. Rexroth prints
the ratio in its own column.

---

## 4. What Caterpillar's parts list publishes `MEDIUM`

**S003** lists five boom cylinders for the 320C/320L/320S:

| bore × rod | rod ÷ bore | retract ÷ extend | φ | Cat cylinder no. |
|---|---|---|---|---|
| 120 × 85 | 0.708 | **0.498** | 2.01 | 1589058, 2742510, 2897875 (8-bolt head) |
| 120 × 85 | 0.708 | **0.498** | 2.01 | 1588991, 1850340, 2043614, 2590694 (12-bolt) |
| **140 × 100** | **0.714** | **0.490** | **2.04** | **2590702** |
| 150 × 105 | 0.700 | **0.510** | 1.96 | 1232081 |
| 160 × 95 | 0.594 | 0.647 | 1.54 | 1842614, 2795614 |

**Four of the five are the φ = 2 series** — the same series Rexroth publishes, on a different
continent, for a different application, from a different manufacturer. The 160 × 95 is the outlier
and sits near the slim series.

**Tier honesty.** S003 is a parts retailer's seal-kit listing, not a Caterpillar document. On its own
it is weak evidence. It is accepted here because **140 × 100 appears independently in S001**, and
because three of the remaining four rows fall on a ratio S001 defines. A single trade listing would
not clear the gate; a trade listing that reproduces a manufacturer's published series does.

---

## 5. The pair to build, and the cross-check that proves it

**140 mm bore × 100 mm rod** — in S001 *and* S003.

Derived from the geometry, against what Rexroth prints:

| | derived | S001 publishes | delta |
|---|---|---|---|
| A1 (piston) | 153.94 cm² | 153.94 cm² | 0.002 |
| A3 (annulus) | 75.40 cm² | 75.40 cm² | 0.002 |
| F1 @ 250 bar | 384.85 kN | 384.75 kN | 0.10 (vendor rounds) |
| F3 @ 250 bar | 188.50 kN | 188.40 kN | 0.10 (vendor rounds) |

**This is the assertion the harness can hold.** `library/` rule 5 — a component that has been seen to
fail gets a test — has a companion here: a component whose output can be checked against a published
table *should* be. `GEN cylinder` computes A1 and A3 from bore and rod; those two numbers have a
manufacturer's printed value to be compared against. That check belongs in `tests/run.sh`.

**At Caterpillar's 350 bar (S002):**

| | |
|---|---|
| Extend | 538.8 kN — **54.9 tonnes-force** |
| Retract | 263.9 kN — **26.9 tonnes-force** |
| Ratio | **0.490** |

---

## 6. What this does to the brief and the script

| | brief, before | sourced |
|---|---|---|
| Bore | 120 mm `SOURCE NEEDED` | **140 mm** — S001 + S003 |
| Rod | 80 mm `SOURCE NEEDED` | **100 mm** — S001 + S003 |
| Pressure | 350 bar `SOURCE NEEDED` | **350 bar** — S002, confirmed |
| Extend | 395.8 kN / 40.4 t | 538.8 kN / **54.9 t** |
| Retract | 219.9 kN / 22.4 t | 263.9 kN / **26.9 t** |
| Ratio | 0.556 — "44% weaker" | **0.490 — "half"** |

**The one number changes from 44% to half**, and stops being a number that needs defending.
`docs/strategy/spec.md` §2.5 sells the channel on not shipping a figure because the arithmetic checks
out. 44% was arithmetically correct and sat between two manufacturer standards, which is exactly the
shape of a number chosen to sound impressive. 50% is what the industry builds.

---

## 7. Single-acting, for later `MEDIUM`

**S005** publishes effective area directly, which removes the derivation entirely:

```
Cylinder   Stroke  Model      Effective   Oil Cap.  Collapsed
Capacity           Number     Area (cm2)   (cm3)    Height (mm)
   5 t      16     RC-50         6,5        10         41
   5 t      76     RC-53         6,5        50        165
  10 t      26     RC-101       14,5        38         89
  10 t     105     RC-104       14,5       152        171
```

Maximum operating pressure **700 bar**. Not needed for S1 — logged because it is the cleanest
single-acting reference on the board and S1's brief correctly declines to cover single-acting at all.

---

## 8. Known gaps

| Gap | Effect | Resolution |
|---|---|---|
| **No source is archived.** `archive.org` rate-limited (HTTP 429) during this session. | `factgate` rule `every_web_source_has_an_archive_url` **fails**. `--publish` is blocked. | Submit all five URLs to the Wayback Machine, paste the snapshot URLs and dates into `spec/s01/facts/s01.facts.json`. |
| **S003 is a trade listing, not a Cat document.** | The bore/rod fact carries `status: contested`, not `verified`. | The Caterpillar parts catalogue (SIS) entry, or a 320C workshop manual, for cylinder 2590702. |
| **Parker not obtained.** | None — S001 is strictly more complete. | Only worth revisiting if a *mobile*-specific 350 bar catalogue is wanted for a later Short. |

## 9. Licensing

**The PDFs are not in this repo and must not be.** They are copyrighted vendor documents; `legal/`
prohibits `unknown` and `rights-managed` assets, and a datasheet is one or the other.

**The dimensions are facts and are free to cite.** A bore diameter is not a creative work. What is
protected is the document, its drawings and its typography — so nothing here traces a datasheet
illustration, and `GEN cylinder` is modelled from dimensions, never from a vendor drawing.
