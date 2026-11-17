# REPLACEMENT ORACLE

## Problems first

No independent-oracle failures.

Verdict: **PASS**

## Method and limits
- Independently recomputed per-file SHA/bytes, UTF16 code-unit FNV, domain/raw links, save base64, exact query immutability, Single bits, full-field projection, ID/state preservation and asset-derived spatial constraints.
- UI EventSystem accepted raycast + down/up is separated from supplemental API probes. Source is reviewed read-only; raw logs are observations, not externally authenticated OS telemetry.
- Worn item body Attack=0 is distinct from container slot Contribution=6. Strength3 gives progressionBonus=15. Reserve and Overflow body attack do not imply active contribution.
- Natural save gates: independently validate timer advancement, fixed interval5, unchanged focus epoch, gate save base64/SHA, gate-after to operation-before exact bytes and both operation snapshots SavedAt matching the same natural boundary. Different saves are never ignored.
- Existing FLOAT-FINAL: Mono seven cases / 24 prefixes / ULP0; no new product execution or Python numerical R03 oracle.

## Six-mode evidence levels
|Mode|Checks|Failures|Levels|
|---|---:|---:|---|
|accessory|2347|0|{"independent raw": 2290, "source review": 3, "natural autosave raw": 27, "EventSystem/input raw": 12, "UI normal behavior": 1, "ADDITIONAL API only": 14}|
|arms|2404|0|{"independent raw": 2347, "source review": 3, "natural autosave raw": 27, "EventSystem/input raw": 12, "UI normal behavior": 1, "ADDITIONAL API only": 14}|
|board-insufficient|6960|0|{"independent raw": 6905, "source review": 3, "natural autosave raw": 28, "EventSystem/input raw": 13, "ADDITIONAL API only": 11}|
|global|5|0|{"independent raw": 4, "existing actual Mono": 1}|
|illegal-swap|2208|0|{"independent raw": 2152, "source review": 3, "natural autosave raw": 27, "EventSystem/input raw": 12, "ADDITIONAL API only": 14}|
|legal-swap|2229|0|{"independent raw": 2172, "source review": 3, "natural autosave raw": 27, "EventSystem/input raw": 12, "UI normal behavior": 1, "ADDITIONAL API only": 14}|
|main|2153|0|{"independent raw": 2100, "source review": 3, "natural autosave raw": 27, "EventSystem/input raw": 8, "UI normal behavior": 1, "ADDITIONAL API only": 14}|

## Exact UI requests and actual outcomes
Single bytes below are little-endian IEEE754 binary32 reconstructed only from serialized Mono values.
|Mode|Exact replaced ID → candidate ID|target / rotation / role|feasible|actual AP / projected AP bits|
|---|---|---|---|---|
|accessory|75599832a147497ea16e629d4584ab7f → 75d18747569c443aa4a46309c60fb6b2|{'x': 0, 'y': 2} / 0 / Board|True|73.5 / 00009342|
|arms|a2b056371dbf4741b0009b6b9a2f96ae → 62a6b145db4b4556abb0e10417226559|{'x': 0, 'y': 2} / 0 / Board|True|65.85 / 33b38342|
|main|2ae5e14970774010ae65e866344cf036 → a86966e1b3bf434381ed4264bb653e93|{'x': 9, 'y': 0} / 0 / Main|True|83 / 0000a642|
|board-insufficient|91594eaa6c2c46d8b74689f4210df0cb → 542a76963e124bcb89d229f3b815bae9|{'x': 0, 'y': 2} / 1 / Board|False|240 / N/A: rejected|
|legal-swap|342adc14e32241f5ae1ae2c70abe1048 → 8dbe60023159483286d115489a7fc272|{'x': 0, 'y': 2} / 0 / Board|True|69.5 / 00008b42|
|illegal-swap|d6a3a2056f3942f88f476526b69b7b0f → 4fc36177373f498f8bdf60a0ada6094d|{'x': 0, 'y': 2} / 0 / Board|False|54.65 / N/A: rejected|

## Independent geometric failure proofs
- board-insufficient / D-full-board: 48
- board-insufficient / D-target-in-bounds-other-collision: [(0, 2), (1, 2)] collision={'6afc2568705745eaad577af3dbe0931a'}
- legal-swap / E-legal-source-exchange-independent: [(11, 0)]
- illegal-swap / F-return-swap-out-of-bounds-independent: [(12, 0)]

## Final run identities
|Mode|runId|PID|buildId|
|---|---|---:|---|
|accessory|UX04B2R2FIX-A07-accessory|19728|ux04b2r2fix-ab3d5ba4-b70442f9-0c44b9c6|
|arms|UX04B2R2FIX-A07-arms|5132|ux04b2r2fix-ab3d5ba4-b70442f9-0c44b9c6|
|main|UX04B2R2FIX-A07-main|11412|ux04b2r2fix-ab3d5ba4-b70442f9-0c44b9c6|
|board-insufficient|UX04B2R2FIX-A07-board-insufficient|31532|ux04b2r2fix-ab3d5ba4-b70442f9-0c44b9c6|
|legal-swap|UX04B2R2FIX-A07-legal-swap|12660|ux04b2r2fix-ab3d5ba4-b70442f9-0c44b9c6|
|illegal-swap|UX04B2R2FIX-A07-illegal-swap|5880|ux04b2r2fix-ab3d5ba4-b70442f9-0c44b9c6|

Product SHA: ab3d5ba4f4a234598056915ab7b1dca4ad4be57f68298fc24d1b718d267a2df1

Driver SHA: 0c44b9c626cbe8d7fa27c83d6369a98c4cb112486e0859713ee57805e719fd45

## Immutable history
UI-A01 accessory verifier Worn expectation 0 failed; UI-A02 accessory/arms/main succeeded; D wheel120 could not reach old control and did not Evaluate. UI-A03 first three succeeded; D wheel8 still overshot (1296px/tick), no Evaluate, not product capacity failure. A04-PROBE quarterwheel D accepted (reported PID7972/exit0); a probe, not the unified final six. A05 first five reported PASS; F original FAIL must remain FAIL: all nine canonical and random unchanged but save bytes changed (revision1 to2 and new .bak) during natural 5-second unscaled autosave. Source CombatSaveSystem.LateUpdate independently confirms autonomous save; ApplyEquipment returns before mutation on projection failure. This timing explanation does not waive byte-level atomicity or promote A05 F to PASS. A06 was a natural-save-boundary F probe, not final acceptance. Historical A01/A02/A03/A04-PROBE/A05/A06-PROBE immutable, not final six.

Complete rows and digests: [JSON](<I:/unity/WanxiangGuitu/ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/EVIDENCE/REPLACEMENT_ORACLE.json>) / [CSV](<I:/unity/WanxiangGuitu/ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/EVIDENCE/REPLACEMENT_ORACLE.csv>).
