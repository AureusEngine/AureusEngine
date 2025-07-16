
# Shaping Behavior Observations (Canonical Audit Log)

1. Template Warp Alignment
   - Template deviation dt appears to bias shaping outputs toward Q_anchor + dt.
   - This is not structurally enforced but is observed in warp-skewed recipes.

2. Template Boundary Collapse
   - When dt = 0, the template is interchangeable and collapses into base logic.
   - Observed equivalence between FFF + F and FFF.

3. Deviation Range Effects
   - Greater base spread in signature (e.g., (0, 4, 5)) correlates with more polarized output, concentrating mass at low and high bins.

4. Template Isolation Skew
   - In recipes where base deviations are uniform and dt > 0, the curve skews sharply toward the template’s tier.

5. Deviation Shift vs Q_Shift
   - Recipes with the same Q_shift but different deviation signatures yield different distributions.
   - Reinforces that deviation shape, not shift magnitude, determines the curve.

6. Tier Shift Invariance
   - Uniform recipes tier-shift cleanly, maintaining curve shape across configurations (e.g., FFF → X, Y, etc.).

7. Low-Deviation Pull
   - In mixed-tier recipes, base materials with d = 0 exert dominant shaping influence, biasing curves toward Q_anchor.

8. Mirror Signature Discrepancy (I)
   - Mirror sigs (e.g., (0,1,2) vs (0,2,1)) may not yield the same curves.
   - May suggest kernel base position weighting — warrants evaluation.

9. Mirror Signature Discrepancy (II)
   - Microstructure of curves (not skew) may diverge in mirrored sigs.
   - Asymmetry appears in peak smoothness, bin shaping, and secondaries.

10. Overmatch Template Instability
    - Templates with dt ≥ 3 above all bases can destabilize curve shape.
    - May indicate warp threshold or overdominant template behavior.

11. Tier Wrapping Asymmetry
    - Shifting across tier extremes (e.g., P to Y) breaks curve continuity in some sigs.
    - Wrapping behavior is asymmetric and should not be assumed safe.
