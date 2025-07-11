## Aureus Engine — 3-Material Modeling Logic (Reverse Engineering)

### 🔒 Canvas Edit Protocol

- Canvas edits will now follow a strict proposal-first workflow.
- All suggested logic, constraint, or structure updates must be explicitly approved before being applied.
- Suggested edits will be shown as:
  > **📝 Proposed Canvas Change** *(Not yet applied — awaiting approval)*
- Only upon user confirmation will the proposed change be committed.
- Exception: routine formatting or emergency error correction may be handled immediately when context clearly requires it.
- This safeguard does not interfere with dataset analysis or modeling continuity — it strictly governs the logic canvas.

### ✅ Analysis Plan for Tier-Deviation Coefficient Model (2- and 3-Material Recipes)

---

### PHASE 1: Dataset Ingestion (2- and 3-Material)

#### ⚠️ Terminology Protection

- The term **“template”** refers exclusively to the special `TEMPLATE` fragment used in certain 2-, 3-, 4-, and 5-material recipes.
- It designates the final material position (if present) with disproportionate influence on shaping logic.
- The word “template” must **not** be used to describe curve shapes, modeling patterns, deviation profiles, or output structures.
- Alternative terms such as “output profile,” “curve shape,” or “fingerprint” must be used in all non-fragment contexts.

**Input Requirements:**

- Each entry must contain:
  - A 2-tier or 3-tier recipe string (e.g., "PC" or "PCF")
  - An output distribution: six floats in canonical tier order `[P, C, F, X, E, Y]`, summing to 100.0

**Input Validation Rules:**

- Recipe string must include exactly 2 or 3 tiers from `{P, C, F, X, E, Y}`
- All six output values must be valid floats, two decimal places, and total between 99.99–100.01

**Important:** This analysis applies **only** to 2- or 3-material recipes that use **BASE-only** fragments (no TEMPLATE position). Other 3-material recipes **with TEMPLATE fragments** are **excluded** from this phase and must be handled separately.

---

### PHASE 2: Recipe Normalization

- Parse input recipe into a list of quality tiers `Q1`, `Q2`, `Q3`, etc.
- Identify the true **minimum tier** from the original input using the canonical tier index (not alphabetically or by order of appearance)
  - Example: In recipe `('C', 'P', 'X')`, quality `P` has the lowest canonical index (0), so it is the true minimum and assigned deviation = 0 — not `C`
- Map each quality tier to its canonical index:
  ```
  tier_map = { 'P': 0, 'C': 1, 'F': 2, 'X': 3, 'E': 4, 'Y': 5 }
  ```
- Determine the minimum tier index (`min_idx`)
- Compute deviation for each quality input: `deviation = tier_index - min_idx`

---

### PHASE 3: Contribution Weighting

- 🔒 **Structural Integrity Rule:** After projection, all tiers between the minimum and maximum tier **must** contain non-zero values. If any intermediate tier has a weight of 0.0, a small placeholder (e.g., `0.01`) will be injected prior to normalization to enforce validity.

- **Coefficient Range Constraint:** Tunable weights `x₁–x₅` are provisionally bounded (0.01–5.0). These bounds are empirical and subject to adjustment.

- **Deviation-to-Weight Mapping:**

  - Deviation 0 → weight = 1.00 (provisionally fixed)
  - Deviations 1–5 → weights = `x₁–x₅` (tunable)

- **Repeated Tier Handling:**

  - If repeated tier is the **minimum**, each instance contributes 1.00 independently
  - If repeated tier is **above the minimum**, each instance is weighted by its individual deviation

- **Deviation Attribution Rule:** Each fragment must be assigned a deviation relative to the true minimum and evaluated independently. BASE tier order is ignored, but per-fragment attribution is required.

- **Failsafe Enforcement:**

  - Predictions must include **non-zero weights for all intermediate tiers** (i.e., all canonical tier indices between the min and max tier must be represented)
  - After weight calculation but before final normalization, the model must forcibly insert a minimum placeholder value (e.g., 0.01) into any missing intermediate tier to ensure output validityFragment collapsing or omission is not allowed

---

### PHASE 4: Output Vector Generation (3-Material Only)

---

### PHASE 4A: Deviation Profile Isolation (2-Material Recipes)

#### ✅ Canonical Profile Alignment Rule

- All 2-material predictions must use a **direct lookup from canonical output profiles** based on the deviation signature `(0, X)`.
- These output profiles have been verified to produce 100% valid matches across all known 2-material combinations.
- No Gaussian shaping, fitted polynomial, or COM-derived distribution generation is permitted in 2-material logic.
- The curve must be aligned to the correct tier anchors (min → index 0) and reshaped only by **tier offset**, not shape logic.
- This method has full deterministic parity with the game system and is locked in as the official model for 2-material shaping.

#### ⚠️ Error-Proofing Constraints for Canonical Curve Analysis

1. **Averaging Restrictions**

   - Do **not** average output distributions for recipes sharing a deviation signature. If multiple recipes with the same deviation signature yield differing shapes after tier-zero alignment, this is not grounds for averaging — it is grounds for an immediate halt and dataset integrity check.
   - All recipes with a shared deviation signature are expected to yield **identical output shapes**, tier-shifted as necessary. If this does not hold, the canonical dataset must be verified.
   - Averaging must never mix curves whose actual tier ranges differ (e.g., `P→Y` vs `C→Y`) unless they have first been normalized to a shared alignment baseline.
   - Min–max tier anchors are used to track the curve's true tier location but do **not define separate deviation signatures** — they constrain alignment, not classification.
   - Structural similarity (e.g., curve shape) is not a valid criterion alone unless tier positions are explicitly aligned before comparison.
   - Structural similarity (e.g., curve shape) is not a valid criterion alone unless tier positions are explicitly aligned before comparison.

2. **Tier Anchor Preservation**

   - For all deviation signatures, the **minimum and maximum tier values** are considered tier anchors.
   - Both anchors must be tracked explicitly and preserved in all shape comparisons, alignment logic, and output evaluations.
   - Canonical curves must be stored or evaluated in context of their actual tier bounds (e.g., `P→Y` vs `C→Y`).

3. **Canonical Supremacy Rule**

   - If a verified canonical output curve exists for any recipe, it must be used directly without modification or substitution.
   - Do not attempt to recreate or approximate a canonical output from neighboring recipes.

4. **Shape Alignment Requirement**

   - Output curves must be **tier-zero aligned** (minimum tier normalized to index 0) before evaluating shape, center of mass, or skew behavior.

5. **No Deviation-Only Grouping**

   - Deviation signature `(0, X)` alone is insufficient for grouping curves unless their outputs have been normalized to a common tier baseline.
   - Tier anchors (e.g., `P→Y` vs `C→Y`) do **not define new deviation signatures**, but must be respected for proper output alignment and validation.

These safeguards must apply to **all deviation signatures** and **all material combinations**, not just examples like `(0, 4)` and `(0, 5)`. This ensures fully general, tier-anchored accuracy across the shaping kernel.

---

### 📦 Appendix: Canonical 2-Material Dataset (Embedded for Permanence)

#### ✅ Verified Deviation Profiles (Tier-Zero Aligned)

| Deviation Signature | Aligned Output Profile                      | Count | Center of Mass |
| ------------------- | ------------------------------------------- | ----- | -------------- |
| `(0, 0)`            | `[100.0, 0.0, 0.0, 0.0, 0.0, 0.0]`          | 5     | **0.00**       |
| `(0, 1)`            | `[60.0, 40.0, 0.0, 0.0, 0.0, 0.0]`          | 10    | **0.40**       |
| `(0, 2)`            | `[57.14, 14.29, 28.57, 0.0, 0.0, 0.0]`      | 8     | **0.71**       |
| `(0, 3)`            | `[50.0, 20.0, 10.0, 20.0, 0.0, 0.0]`        | 6     | **1.00**       |
| `(0, 4)`            | `[42.86, 21.43, 14.29, 7.14, 14.29, 0.0]`   | 4     | **1.29**       |
| `(0, 5)`            | `[36.84, 21.05, 15.79, 10.53, 5.26, 10.53]` | 2     | **1.58**       |

```json


#### 📊 Observed Behavioral Patterns from 2-Material Canonical Data

1. **Perfect Symmetry Confirmed**
   - Inputs such as ["P", "Y"] and ["Y", "P"] produce **identical output curves**
   - No reversal or reordering is necessary — game outputs are **invariant to input order** for 2-material recipes

2. **Deviation Signature Governs Distribution Shape**
   - All recipes with the same tier deviation (e.g., `(0, 2)`) produce **identical curve shapes**, differing only in tier placement (i.e., anchor-shifted along the output vector)
   - Output skew consistently favors the **lower tier** in all valid tier gaps

3. **Higher Deviations Increase Spread and Lower Center Mass**
   - As tier distance increases (e.g., from `(0, 1)` to `(0, 4)`), output distribution shifts more weight to edges and away from center
   - `(0, 4)` profiles show sharp skew toward the lower tier with balanced tails

4. **Flat Profiles Never Occur**
   - No canonical shape is uniform across tiers (other than exact match `(0, 0)`)
   - Even mirrored-tier inputs always resolve into **directionally-weighted** curves

5. **Repeatability and Determinism Confirmed**
   - No input pair showed unstable, random, or ambiguous shaping
   - Dataset demonstrates **deterministic 1-to-1 mapping** from tier pair → output curve

These patterns are now considered ground truth for informing and constraining 3-material logic in Phase 4.

```

- This phase applies only to 2-material BASE-only recipes.

- Output distributions will be grouped by **deviation signature** only after tier-zero alignment confirms structural identity. If shapes diverge after alignment, the group must be flagged for canonical verification — no averaging or shape inference is permitted.

- Each 2-material recipe has only two fragments, so possible deviation signatures are:

  - `(0, 0)`  → Uniform-tier inputs (e.g. "CC") → Always 100% of that tier
  - `(0, 1)`  → One-tier difference (e.g. "CF")
  - `(0, 2)`  → Two-tier difference (e.g. "CX")
  - `(0, 3)`  → Three-tier difference (e.g. "CE")
  - `(0, 4)`  → Four-tier difference (e.g. "CY")
  - `(0, 5)`  → Five-tier difference (e.g. "PY")

- Each deviation profile will be evaluated for:

  - Output shape stability across mirrored inputs
  - Output skew relative to minimum and maximum tier
  - Scaling characteristics (if any)

- Once deviation profile behavior is confirmed and deterministic, extracted constants or patterns will be used to inform more complex 3-material modeling.

- **Canonical Output Profiles by Deviation Signature:**

  - `(0, 0, 0)` → `[100.0, 0.0, 0.0, 0.0, 0.0, 0.0]`  // "PPP"
  - `(0, 0, 1)` → `[71.43, 28.57, 0.0, 0.0, 0.0, 0.0]`  // "PPC"
  - `(0, 0, 2)` → `[66.67, 11.11, 22.22, 0.0, 0.0, 0.0]`  // "PPC"
  - `(0, 0, 3)` → `[58.33, 16.67, 8.33, 16.67, 0.0, 0.0]`  // "PPX"
  - `(0, 0, 4)` → `[50.0, 18.75, 12.5, 6.25, 12.5, 0.0]`  // "PPF"
  - `(0, 0, 5)` → `[42.86, 19.05, 14.29, 9.52, 4.76, 9.52]`  // "PPY"
  - `(0, 1, 1)` → `[42.86, 57.14, 0.0, 0.0, 0.0, 0.0]`  // "CCP"
  - `(0, 1, 2)` → `[44.44, 33.33, 22.22, 0.0, 0.0, 0.0]`  // "PCF"
  - `(0, 1, 3)` → `[41.67, 33.33, 8.33, 16.67, 0.0, 0.0]`  // "CEF"
  - `(0, 1, 4)` → `[0.0, 37.5, 31.25, 12.5, 18.75, 0.0]`  // "CEX""
  - `(0, 0, 5)` → `[42.86, 19.05, 14.29, 9.52, 4.76, 9.52]`  // "PPY""
  - `(0, 2, 2)` → `[44.44, 11.11, 44.44, 0.0, 0.0, 0.0]`  // "PFF"
  - `(0, 2, 3)` → `[41.67, 16.67, 25.0, 16.67, 0.0, 0.0]`  // "PFX"
  - `(0, 2, 4)` → `[37.5, 18.75, 25.0, 6.25, 12.5, 0.0]`  // "PFE"
  - `(0, 1, 4)` → `[0.0, 33.33, 19.05, 23.81, 9.52, 14.29]`  // "CFY""
  - `(0, 1, 1)` → `[0.0, 41.67, 58.33, 0.0, 0.0, 0.0]`  // "FXX""
  - `(0, 1, 2)` → `[0.0, 37.5, 18.75, 43.75, 0.0, 0.0]`  // "FXE""
  - `(0, 1, 3)` → `[0.0, 33.33, 19.05, 14.29, 19.05, 14.29]`  // "FXY""
  - `(0, 4, 4)` → `[37.5, 18.75, 12.5, 6.25, 25.0, 0.0]`  // "EEP"
  - `(0, 4, 5)` → `[33.33, 19.05, 14.29, 9.52, 14.29, 9.52]`  // "EYP"
  - `(0, 5, 5)` → `[33.33, 19.05, 14.29, 9.52, 4.76, 19.05]`  // "YYP"

