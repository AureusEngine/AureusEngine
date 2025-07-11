## Aureus Engine — 3-Material Modeling Logic (Reverse Engineering)

---

### ✅ Canonical Modeling Rules for All BASE-Only Recipes

**ADV Handling Note:** ADV materials are known to be mathematically identical in shaping logic to BASE materials. To prevent modeling interference, ADV logic is excluded from all reverse-engineering calculations. The first-slot display of ADV fragments in ADV-eligible recipes will be handled entirely by the UI layer.

This workflow will be revisited in a separate logic pass for full ADV system handling.

These rules govern all shaping behavior and logic for 2-, 3-, 4-, and 5-material recipes using BASE-only fragments. They are foundational and apply before any runtime modeling or projection logic.

**Rule 1: Deviation Signature Uniqueness**

> A given deviation signature — defined as the list of deviations from the minimum tier (e.g., `(0, 1, 2)`) — maps deterministically to a single canonical output profile. This rule holds across all BASE-only recipes regardless of length.

**Rule 2: Base Material Order Irrelevance**

> The order of BASE fragments is irrelevant. Only the set of quality tiers and their deviations from the minimum tier determine the output shape. All BASE and ADV fragment positions are fully interchangeable.

**Rule 3: Deviation Must Be Computed from the True Minimum Tier**

> Deviation calculations must anchor to the true minimum quality tier present in the recipe. If multiple fragments share that minimum tier, each one contributes independently using the `(0)` weight vector. This logic ensures consistency in deviation signature construction and proper reuse of tier-zero-aligned vectors in all recipes.

**Rule 4: Canonical Tier Weight Vectors Must Be Tier-Zero Aligned**

> Each fragment’s contribution to the output shape must be projected using its canonical tier-weight vector, aligned to a zero-based tier index anchored at the minimum quality tier in the recipe. After projection, the resulting distribution curve is realigned to match the actual tier anchors of the recipe (min → max) before normalization. The curve must terminate at the maximum tier — not before — and all intermediate tiers between min and max must be represented with non-zero values.

**Rule 5: No Gaps Between Tier Anchors**

> All output distributions must include non-zero values for every tier between the minimum and maximum quality tiers present in the recipe. Any prediction that omits a tier between these anchors is invalid and must be rejected or corrected with enforced placeholder logic. This requirement ensures structural integrity and matches all known canonical output behavior.

**Rule 6: Mirrored Inputs Yield Identical Output**

> For any BASE-only recipe, if the same quality tiers are present — regardless of the order — the output curve must be identical. This rule applies to 2-, 3-, 4-, and 5-material combinations with BASE materials only. Even in recipes that include a `TEMPLATE` fragment, this rule remains valid as long as the TEMPLATE position is excluded from the tier comparison.

**Rule 7: Canonical Supremacy Rule**

> If a verified canonical output curve exists for any recipe, it must be used directly without modification or substitution. Do not attempt to recreate, estimate, or interpolate output from similar recipes when canonical data is available. Canonical data always takes precedence over model logic.

**Rule 8: Tier Anchor Preservation**

> For every recipe, the minimum and maximum quality tiers (tier anchors) must be explicitly preserved during all alignment, projection, and validation operations. Tier-zero alignment may be used during projection, but final outputs must honor the true tier anchors present in the original recipe.

**Rule 9: No Averaging Allowed for Shared Deviation Signatures**

> If multiple recipes share a deviation signature but produce differing output shapes after tier alignment, this indicates a dataset integrity issue — not an opportunity to average. No averaging or blending of curves is permitted across deviation groups. Deviations must yield consistent deterministic outputs.

**Rule 10: Failsafe Compliance Must Be Modeled, Not Patched**

> All valid output predictions must naturally include non-zero values for every tier between the minimum and maximum quality tiers. If any intermediate tier is predicted as 0.0, this indicates a failure in the shaping logic — not a situation to patch. No placeholder values (e.g., 0.01) may be inserted to circumvent failsafe enforcement. Model logic must be refined to produce structurally valid distributions without correction.

**Rule 11: Deviation Signature Canonicalization Rule**

> Deviation signatures must always be sorted in ascending order before use in modeling, lookup, or validation. This includes cases with repeated deviations (e.g., `(0, 0, 2)` or `(0, 1, 1)`). Sorting ensures that all recipes with identical quality tiers — regardless of order — produce a consistent, canonical deviation signature. This is essential for signature-keyed profile alignment, deterministic prediction, and avoiding false profile mismatches.

(Additional rules will appear here as they are verified)

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

#### ✅ Additive Tier-Weight Projection Rule

- 3-material recipes must project each fragment’s contribution to the output shape using the **canonical tier-weight vector** for its deviation from the recipe’s minimum tier.
- This model uses:
  - One fixed canonical vector for the minimum-tier fragment: `(0)` → `[1.0]`
  - Two additional vectors for the other fragments, based on their deviations `(1–5)`
- The three vectors are **summed tier-wise** in tier-zero alignment, then:
  - Realigned to actual tier anchors
  - Normalized to 100.0
  - Enforced to contain no zero-weight gaps between min and max tiers (failsafe)
- This logic builds directly on Phase 4A’s verified 2-material kernel, enabling deterministic generalization to 3-material predictions

---

### PHASE 4A: Deviation Profile Isolation (2-Material Recipes)

#### 📌 Generalized Deviation Signature Rule (Applies to All BASE-Only Recipes)

#### ✅ Universal Base Material Interchangeability Rule

#### ✅ Deviation Signature Anchoring Rule (Universal)

- All deviation signatures must be calculated **relative to the true minimum quality tier** in the recipe.
- The minimum-tier fragment is always assigned deviation = `0`.
- This anchoring enables correct tier-zero alignment for applying canonical tier-weight profiles.
- If multiple fragments share the minimum tier, \*\*each one is independently assigned deviation = \*\*\`\`, and contributes equally using the `(0)` canonical weight vector `[1.0]`.
- This rule holds across all BASE-only recipes regardless of material count.
- The order of BASE fragments in any recipe is **irrelevant** to the crafting outcome.
- All BASE and ADV fragment positions are **fully interchangeable** — only their tier and deviation from the minimum matter.
- This rule applies across all recipe sizes: 2-, 3-, 4-, or 5-material combinations.
- The only fragment type with positional importance is the `TEMPLATE`, which always occupies the final position and has distinct shaping influence.
- Output shaping must be invariant under reordering of BASE materials — canonical data confirms this behavior universally.
- A given **deviation signature** — defined as the ordered list of deviations from the minimum tier (e.g., `(0, 1, 2)`) — maps **deterministically** to a single output shape.
- This applies regardless of how many materials are involved (2, 3, 4, or 5), as long as all inputs are BASE fragments.
- Output profiles must:
  - Be tier-zero aligned (min tier = index 0)
  - Preserve all intermediate tiers between min and max
  - Reflect the canonical shape associated with the deviation signature
- This generalization expands the 2-material rule `(0, X)` to cover all BASE-only recipes.
- 🔧 **Note:** This rule will be extended in future phases to account for recipes that include a `TEMPLATE` fragment, which introduces asymmetric shaping behavior not governed by simple deviation.

#### 📌 Scalability Constraint (4- and 5-Material Recipes)

- Canonical profile alignment is feasible for 2-material and most 3-material recipes because the number of unique deviation signatures is tractable.
- However, 4- and 5-material recipes produce a **combinatorially large number** of deviation signatures and tier anchor combinations.
- It is therefore **not required nor scalable** to provide canonical output data for every possible deviation signature at higher material counts.

#### ✅ Strategic Resolution:

- A **coefficient-based shaping model** will be derived from validated 2- and 3-material canonical behavior.
- This shaping logic will interpolate tier weight contributions from deviation values (`x₁–x₅`) to generate deterministic curves.
- Where canonical outputs exist, they will override the model. Otherwise, the model will predict based on validated constraints.
- `TEMPLATE` influence will be handled as a distinct shaping factor (multiplicative or additive), not as a deviation.

---

#### ✅ Canonical Profile Alignment Rule

##### 🎯 Finalized Tier-Weight Vectors

- Each canonical 2-material deviation signature `(0, X)` has a normalized vector that defines the **relative tier weights** across the valid output range.
- These vectors are tier-zero aligned and encode the **exact shaping influence** without need for approximation.

| Deviation Signature | Normalized Weight Vector                           |
| ------------------- | -------------------------------------------------- |
| `(0, 0)`            | `[1.0]`                                            |
| `(0, 1)`            | `[0.6, 0.4]`                                       |
| `(0, 2)`            | `[0.5714, 0.1429, 0.2857]`                         |
| `(0, 3)`            | `[0.5, 0.2, 0.1, 0.2]`                             |
| `(0, 4)`            | `[0.4286, 0.2143, 0.1429, 0.0714, 0.1429]`         |
| `(0, 5)`            | `[0.3684, 0.2105, 0.1579, 0.1053, 0.0526, 0.1053]` |

- These vectors must be used for all 2-material output predictions.

- Output curves are generated by aligning the appropriate vector to the minimum tier anchor of the recipe.

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

#### 🔄 Canonical Output Profiles by Deviation Signature (Repopulation Workflow Pending)

> ⚠️ The prior entries in this section were found to contain conflicts, invalid tier-zero alignment, and violations of modeling rules. They have been purged to prevent modeling errors and will be repopulated through verified canonical analysis only.

✅ A future step will analyze the 3-material canonical dataset and regenerate this table using:

- Rule-validated deviation signatures
- Tier-zero aligned vectors
- Verified min–max anchor constraints

This ensures 100% deterministic parity with all 3-material shaping behavior.



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

```
