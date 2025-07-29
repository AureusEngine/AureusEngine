# Aureus Engine Functional Methodology

## Core Principle
Game distributions are **purely additive**:
- Each scaling step = previous distribution **+ delta** (per deviation signature)
- Normalize probabilities after each step.
- Template position is **fixed last**, bases are **unordered**.

---

## 1. Data Preparation

### Canonical Inputs
- **3-mat Non-Template dataset** (baseline probabilities)
- **3-mat Template dataset** (target probabilities, corrected)

### Normalization
- Convert recipe letters → deviations (`P=0 … Y=5`)
- **Min-zero normalize** deviations for calculation
- Keep **template as last position**; bases are unordered

---

## 2. Delta Computation
- Compute **deltas**:  
```
Δ = Template Canonical – Non-Template Canonical
```

- Match **template signature** (ordered) to **non-template signature** (unordered):
  - Sort bases
  - Combine with template deviation to form parametric triple:
    `(min base, max base, template)`

- Result = **51 unique deltas** (full coverage of template dataset).

---

## 3. Parametric Model
- Each delta is determined by `(min base, max base, template deviation)`:
  - No lookup by full recipe
  - Scales to unseen recipes automatically
- Baseline probabilities come from NT dataset:
  - Matched by unordered triple of normalized deviations

---

## 4. Prediction Function

### Algorithm
1. **Map input recipe to deviations**
   - e.g., `FXE → [2,3,4]`

2. **Record raw min and max deviations**
   - Used later for tier alignment

3. **Normalize by min deviation**
   - e.g., `[2,3,4] → [0,1,2]`

4. **Compute Non-Template baseline**
   - Match unordered triple to NT dataset
   - Get baseline probabilities (P–Y ladder)

5. **Apply parametric delta**
   - Lookup `(min base, max base, template)` triple
   - Add delta to baseline

6. **Remap bins back to real tiers**
   - Shift bins upward by raw `min deviation`
   - Output bins spanning **min → max** actual tiers
   - No forced spread to Y unless recipe uses Y

---

## 5. Validation
- Predictor tested against **all 51 canonical template recipes**:
  - 100% canonical match (probabilities + tier alignment)

---

## 6. Scaling to 4- and 5-Mat
- Same additive principle:
  - **3 Template → 4 Template** = Add fixed delta
  - **4 Template → 5 Template** = Add fixed delta
- Only requires delta extraction at each step (no full tables):
  - Triples/quads can be parametric (min, mid, max, template)
- Min→max remapping ensures correct tier alignment at any size

---

# Key Advantages
- **No giant lookup tables** needed after deltas derived
- **Canonical fidelity** at every step
- **Parametric rules generalize** to unseen combinations
- **Tier alignment preserved** for real recipes (no Q-shift errors)
