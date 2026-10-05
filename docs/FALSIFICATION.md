# Falsification

> A residual is only a residual until known explanations are excluded.

Reject a **specific, versioned GV formulation** when its frozen prediction fails.
A flexible name covering any unexplained observation is not a falsifiable theory.
No universal physical GV claim is currently supported or sufficiently specified
to earn confirmation.

## Required Rejection Rules

| Failure | Decision for the tested claim |
| --- | --- |
| Statistic ties or loses to simpler baselines at the frozen endpoint/matched FPR | NOT SUPPORTIVE for an incremental-performance claim. |
| Signal disappears under a valid sham, shielding, or isolation control | Reject the claimed independent channel if the contrast follows a known pathway. |
| Timing follows clock identity, cable delay or software scheduling | Known clock/timing explanation; do not call it GV. |
| Signal tracks EM, vibration, sound or thermal manipulation | Known EM/environmental explanation; reject that event's GV attribution. |
| Effect fails the prespecified replication/effect-size tolerance with adequate sensitivity | NOT SUPPORTIVE for reproducibility under those conditions. |
| Result reverses across reasonable prespecified analyst/model choices | Reject robustness claim; exploratory sensitivity is not confirmation. |
| Performance collapses on independent held-out data | Reject out-of-sample discrimination claim. |
| Leakage, confounding, selection or sampling explains apparent performance | Attribution fails; invalidate affected analysis and preserve the original record. |
| Effect appears only after outcome-guided weighting, thresholds or exclusions | Not confirmatory; label exploratory and test on new independent data. |
| Apparatus/solver validity, calibration, sensitivity or data integrity fails | INVALID / INCONCLUSIVE, not a valid positive or performance rejection. |

Failure to detect within a stated bandwidth/sensitivity rejects only the predicted
effect in that regime. It does not establish absence at all scales. Conversely,
invoking inaccessible scales after failure cannot rescue the original prediction.
Report FPR **and** detection power; report missed alarms, null trials, and uncertainty.

## Freeze Before Testing

Assign an ID/version; freeze observable mapping, $K$, $G$, event time/window,
sample size, calibration/test split, endpoint, baseline set, multiplicity treatment,
stopping/exclusion rules, and support/rejection thresholds. Archive code commit,
manifest and data hashes. Retain all trials, including failed apparatus runs.
Use the [alternative-explanation matrix](ALTERNATIVE_EXPLANATIONS.md).

Separate validity failures from hypothesis failures. F2 is invalid; F0/F1/F1b/F2b
do not support their advantage claims. F1's confound remains visible rather than
being used to erase its original NOT SUPPORTIVE verdict.

## No Moving Goalposts

Different formulations can fail independently. A revised formulation must:

1. Keep the failed ID/result, protocol and original analysis in the ledger.
2. Describe why revision is justified and what changed before a new dataset.
3. Use a new ID/version and independent data; label exploratory work explicitly.
4. State how the new prediction differs measurably from both its failed predecessor
   and ordinary explanations, with a fixed failure condition.
5. Report the cumulative record rather than presenting only the surviving version.

The launch does not revise historical weights or promote a failed formulation
because a broader metaphor remains possible. Repeated reformulation without new
discriminating predictions is a reason to stop or narrow the program, not a success.
Further work must earn resources on predictive value, not the promise that GV can
always be renamed. Attempts to disprove GV are welcome.

## Limits on Escalation

An unexplained propagation candidate is not causal identification. A GV candidate
is not a novel-mechanism conclusion. New physics is not a theological conclusion.
Independent replication and discriminating causal evidence are necessary before
escalation under the [claims ladder](CLAIMS.md).