## Aureus Engine — 3-Material Modeling Logic (Reverse Engineering)

### ✅ Analysis Plan for Tier-Deviation Coefficient Model (3-Material Recipes)

---

### PHASE 1: Dataset Ingestion

**Input Requirements:**

- Each entry must contain:
  - A 3-tier recipe string (e.g., "PCF")
  - An output distribution: six floats in canonical tier order `[P, C, F, X, E, Y]`, summing to 100.0

**Input Validation Rules:**

- Recipe string must include exactly 3 tiers from `{P, C, F, X, E, Y}`
- All six output values must be valid floats, two decimal places, and total between 99.99–100.01

**Important:** This analysis applies **only** to 3-material recipes that use **BASE-only** fragments (no TEMPLATE position). Other 3-material recipes **with TEMPLATE fragments** are **excluded** from this phase and must be handled separately.

---

### PHASE 2: Recipe Normalization

- Parse input recipe into a list of tier symbols

- Always identify the true **minimum tier** from the original input set using its canonical value

  - Do **not** assign deviation zero to the lowest alphabetical or first-listed input
  - Example: In recipe `('C', 'P', 'X')`, tier `P` has the lowest canonical index (0), so it is the true minimum and assigned deviation = 0 — not `C`

- Map each tier to its canonical index:

  ```
  tier_map = { 'P': 0, 'C': 1, 'F': 2, 'X': 3, 'E': 4, 'Y': 5 }
  ```

- Determine the minimum tier index (min\_idx)

- Compute deviation for each tier: `deviation = tier_index - min_idx`

---

### PHASE 3: Contribution Weighting

- **Coefficient Range Constraint:** The tunable weights `x₁–x₅` were originally bounded arbitrarily (0.01–5.0) to avoid nullifying tier influence. These ranges may require recalibration once shape projections are introduced, as they are not yet grounded in canonical tier influence ratios.

- **No Implicit Collapsing:** Repeated deviation values are allowed, but each instance must be attributed individually to its corresponding fragment. Deviation grouping must never suppress or combine inputs.

- **Deviation-to-Weight Mapping:**

  - Deviation 0 → weight = 1.00 (provisionally fixed based on observed outcomes in uniform-tier recipes)
  - Deviations 1–5 → weights = `x₁–x₅` (tunable)

- **Repeated Tier Handling:**

  - If the repeated tier is the **minimum**, **every instance** must contribute a full weight of 1.00. Do not collapse, merge, or suppress these entries.
  - If the repeated tier is **above the minimum**, each instance must be evaluated independently by its deviation.

- **Deviation Attribution Rule:**

  - While BASE material order is mathematically irrelevant, **each fragment must be tracked individually** when applying deviation logic.
  - Deviations must be computed per fragment and weights must be assigned **to the actual tier of that fragment**, not to a sorted or grouped bucket.
  - Failure to assign weights to the correct tier index will distort the curve and must be treated as an implementation error.

- **Failsafe Enforcement:** Any recipe where multiple fragments share the minimum tier must be flagged if it produces invalid output (e.g., missing intermediate tiers). These cases are priority candidates for kernel revision.

- Repeated Tier Handling:

  - If the repeated tier is the **minimum**, **every instance** must contribute a full weight of 1.00. Do not collapse, merge, or suppress these entries.
  - If the repeated tier is **above the minimum**, each instance must be evaluated independently by its deviation.

- **Failsafe Enforcement:** Any recipe where multiple fragments share the minimum tier must be flagged if it produces invalid output (e.g., missing intermediate tiers). These cases are priority candidates for kernel revision.

  - Deviation 0 → weight = 1.00 (fixed)
  - Deviation 1 → weight = x₁ (tunable)
  - Deviation 2 → weight = x₂ (tunable)
  - Deviation 3 → weight = x₃ (tunable)
  - Deviation 4 → weight = x₄ (tunable)
  - Deviation 5 → weight = x₅ (tunable)

- All fragments contribute. Duplicate tiers do **not** zero out influence.

- For each tier, sum the weights of all fragments contributing to that tier index.

---

### PHASE 4: Output Vector Generation

- **Deviation Signature Shape Templates:**

  - Signature `(0, 0, 0)` → Canonical shape: `[100.0, 0.0, 0.0, 0.0, 0.0, 0.0]`
    - Deterministic result: when all input tiers are the same, the output must be 100% at that tier
    - This is not derived by averaging, but hardcoded due to in-game behavior
  - Signature `(0, 1, 2)` → Canonical shape: `[44.44, 33.33, 22.22, 0.0, 0.0, 0.0]`
    - Derived from canonical recipes such as `PCF`, `CFX`, `FXE`, and `XEY`
    - Output is strictly constrained to the tier indices between the input minimum and maximum (e.g., P–F for `PCF`)
    - This shape must be projected only within its valid tier band; nonzero values outside this range are invalid

- **Preventative Shaping Principle:** The kernel must be constructed in such a way that it is **impossible** for an invalid prediction to occur. This means:

  - Intermediate tiers between the minimum and maximum must be **guaranteed nonzero** by the shaping logic itself — not enforced after prediction.
  - Output shaping must occur within a normalized tier-relative domain, using deviation signatures to generate deterministic shapes.
  - These shapes must then be mapped to the bounded output tier range.
  - Any kernel implementation that assigns weights directly to absolute tier indices without shape logic introduces leakage and must be rejected.

- **Canonical Zero Rule:** A value of `0.0` in any output position always represents a **real, deterministic 0% chance** of that tier occurring — it is **not** a null, placeholder, or interpolation artifact.

  - All six tiers must always be explicitly represented
  - Any `0.0` in an output curve is meaningful and final

- **Failsafe Enforcement:**

  - Before normalization, explicitly check that all tier indices between `min(input_tier)` and `max(input_tier)` have nonzero contributions.
  - If any intermediate tier has a zero, the prediction is **invalid** and must be corrected or rejected.
  - If the minimum tier appears more than once in the input, ensure that each instance is counted independently.
  - This is a strict rule: no prediction may omit a tier within the bounding range.

- **Failsafe Enforcement:** Before normalization, explicitly check that all tier indices between the **lowest and highest canonical tier indices** of the input recipe have nonzero contributions.

  - If any intermediate tier has a zero, the prediction is **invalid** and must be corrected or rejected.
  - If the minimum tier appears more than once in the input, ensure that each instance is counted independently.
  - This is a strict rule: no prediction may omit a tier within the bounding range.
  - If any intermediate tier has a zero, the prediction is **invalid** and must be corrected or rejected.
  - This is a strict rule: no prediction may omit a tier within the bounding range.

- Initialize output vector: `[0, 0, 0, 0, 0, 0]`

- Assign total weights to each tier based on contribution

- Trim values to the **inclusive range** `[min(input_tier), max(input_tier)]`

- Normalize weights:

  ```
  total = sum(active_weights)
  normalized = [(w / total) * 100.0 for w in active_weights]
  rounded = [round(n, 2) for n in normalized]
  ```

---

**Important Determinism Note:**

- Although the game returns crafting results as **percentage-based distributions** of possible outcomes, these distributions are **deterministic**, not predictive. A given recipe will always yield the same outcome distribution. The modeling kernel must reflect this by producing the **exact same output curve** for any given normalized input recipe.

---

### Governing Rules Summary

| Rule                           | Requirement                                                                                                       |   |                    |                                           |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------- | - | ------------------ | ----------------------------------------- |
| ------------------------------ | -----------------------------------------------------------------------------                                     |   |                    |                                           |
| BASE Input Order               | ⚠️ Tier order is ignored during canonical comparison, but fragment-tier mapping must be preserved during modeling |   |                    |                                           |
| Output Curve Order             | ✅ Canonical — must be `[P, C, F, X, E, Y]`                                                                        |   |                    |                                           |
| Fragment Contribution          | ✅ Each fragment’s contribution is computed individually — even for repeated or identical tiers                    |   |                    |                                           |
| Identical-Tier Recipes         | ✅ Recipes where all materials share a tier yield 100% at that tier                                                |   | Output Tier Bounds | ✅ Must be within `[min, max]` input tiers |
| Intermediate Tier Inclusion    | ✅ Strict — all intermediate tiers between min and max must have nonzero values                                    |   |                    |                                           |
| Explicit Zero Representation   | ✅ `0.0` is a true 0% probability — not null, not interpolated                                                     |   |                    |                                           |
| Normalization                  | ✅ Total must sum to 100.0 (±0.01)                                                                                 |   |                    |                                           |
| Match Requirement              | ✅ Output curve must match canonical distribution to two decimal places, tier-aligned                              |   |                    |                                           |
| TEMPLATE Inclusion             | ❌ Excluded — this dataset does not include any TEMPLATE fragments                                                 |   |                    |                                           |
| Output Nature                  | ✅ Deterministic — not probabilistic or random                                                                     |   |                    |                                           |

---

### Uniform Shift Principle (For Reference Only — Not Used for Prediction)

**Definition:** If the same increase or decrease in quality tier is applied to every position in a recipe, the shape of the resulting distribution remains the same.

However, the output tier **range must shift accordingly**, meaning:

- The **distribution shape** (i.e., percentage pattern) is preserved
- The **output curve is shifted** up or down the tier axis
- The **final output** is still bounded by the new min and max input tiers

**Example 1: Upward Shift**

- Recipe `PCF` → tiers `[P=0, C=1, F=2]` → Output curve: `[44.44, 33.33, 22.22, 0.0, 0.0, 0.0]`
- Shifted to `CFX` → tiers `[C=1, F=2, X=3]` → Output becomes: `[0.0, 44.44, 33.33, 22.22, 0.0, 0.0]`

**Example 2: Downward Shift**

- Recipe `CFX` → `[C=1, F=2, X=3]` → Output: `[0.0, 44.44, 33.33, 22.22, 0.0, 0.0]`
- Shifted to `PCF` → `[P=0, C=1, F=2]` → Output becomes: `[44.44, 33.33, 22.22, 0.0, 0.0, 0.0]`

**Wraparound and Distortion Behavior:**

- Uniform Shift still holds when tier shifts move input values beyond `P` or `Y`
- Output curves in these cases retain the shape but are **truncated** at `P` (lower bound) or `Y` (upper bound)
- However, **deviation signature must remain unchanged** — if the pattern of tier spacing changes, the output shape may no longer follow the original curve

**Verified Examples:**

- ✅ `PCF → CFX → FXE → XEY` → constant deviation pattern `(0, +1, +2)` → shape preserved and shifted up
- ✅ `FEP → CXY` and `PFE → YCX` → shape preserved across downward wrapping
- ❌ `CCX → FFE → XXY → EEP` → deviation set changes mid-sequence → shape breaks

**Implication:**

- Validates that **tier-deviation** is the fundamental driver of curve shape
- Confirms that identical deviation signatures yield identical output shapes regardless of absolute tier values
- Modeling kernel should always use deviation signatures as the core unit of curve structure

**Enforcement:**

- This observed behavior may assist in identifying gaps in canonical data
- It **must not** be used as a source of truth for prediction or model training

---

### Model Validation Verdict

**Conclusion:** The Tier-Deviation Coefficient Model is strongly validated by canonical test data. In both BASE-only and TEMPLATE-inclusive recipes, output distributions depend only on tier deviation signatures, not on absolute tier values.

**Supporting Evidence:**

- Downward and upward "Uniform Shifts" across recipes like `PCF → CFX → FXE → XEY` confirm that identical tier-deviation signatures yield identical output curves (modulo truncation at bounds)
- Even across full wraps from `Y` to `P` or vice versa, the shape is preserved as long as **relative tier spacing remains unchanged**
- Cases where the deviation signature changes (e.g., due to repeated or tightly grouped tiers) consistently lead to **curve distortion**, supporting the idea that deviation—not absolute tier—is the governing feature. Additional canonical evidence from 5-material recipes (e.g. `YYYYP` = `PPPPY`) shows that even extreme reversals in tier arrangement yield identical outputs as long as the deviation signature is preserved. This validates that TEMPLATE contribution can be modeled with a fixed multiplier `T`, and does not require positional tier adjustments

**Implication for Kernel:**

- The kernel correctly emphasizes **deviation from minimum tier**
- No adjustments needed to the weighting architecture — the model remains mathematically sound
- Further tuning (via `x₁–x₅`, and `T` for TEMPLATE weight) should continue assuming this structure is valid and complete

**Caution:** While Uniform Shift behavior offers strong empirical validation, it must not be used to predict missing curves unless deviation patterns are preserved

---

### Optional Tuning Loop

- Run grid search or optimization on `x₁` through `x₅`
- Evaluate prediction accuracy against all canonical data
- Accept only if **all recipes produce exact matches**

---

### Desktop Usage Note

This modeling kernel is being prepared for use with the **Desktop reverse-engineering tool**, which will calculate the table of constants (`x₁–x₅`) explicitly from canonical test cases. This canvas applies **only** to the BASE-only 3-material dataset and excludes any recipes that involve TEMPLATE fragments.

