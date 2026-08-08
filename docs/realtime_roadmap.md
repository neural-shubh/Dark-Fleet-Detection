# Real-Time Monitoring — Phased Roadmap

Tracking issue: #1. Per the issue's own note, this is "a significant scope
extension... worth phasing rather than one big PR." This doc sequences that
phasing; no pipeline code is changed here.

## Phase 1 — Live AIS-only anomaly scoring (smallest useful slice)
- Swap the static AIS dataset for a streaming source (AISHub / MarineTraffic
  API / Spire / exactAIS) for the RNN positional-anomaly branch only
- Maintain a sliding-window per-vessel track buffer so the LSTM/RNN can score
  incrementally instead of needing the full historical sequence
- CNN (SAR) branch stays on the existing static/periodic pipeline for now —
  don't couple SAR latency into the first live pass
- Output: anomaly score updates on a schedule (e.g. every N minutes as new
  AIS pings arrive), not truly per-frame

## Phase 2 — SAR re-tasking integration
- Near-real-time SAR access via Sentinel-1 Copernicus notifications (free
  tier) or commercial (Capella, ICEYE) if budget allows
- Honest framing per the issue: this is periodic re-tasking, not continuous
  video — revisit times are hours, not seconds
- Fuse new SAR passes into the existing CNN branch's score when a vessel's
  AIS-based anomaly score crosses a threshold (targeted re-tasking > blanket
  polling, cheaper and more realistic)

## Phase 3 — Streaming infra + alerting
- Move from notebook batch runs to a lightweight worker: Kafka/Redis queue
  + scheduled or event-triggered inference, matching the pattern already
  used in the credit-card-fraud monitoring dashboard
- Alerting layer: webhook/email on threshold-crossing anomaly scores
- Add explicit latency documentation to the README — "real-time" here means
  minutes-to-hours end-to-end (satellite revisit time is the bottleneck),
  not sub-second

## Sequencing rationale
Phase 1 alone makes the system meaningfully more useful (continuous AIS
monitoring vs. static batch) without touching the harder SAR-latency
problem. Phases 2-3 only pay off once Phase 1's live AIS path is proven
out — no point building alerting infra around a still-static SAR branch.
