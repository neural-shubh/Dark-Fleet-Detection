# Real-Time Monitoring Roadmap

> Status: planning doc, tracks issue #1. The issue itself flags this as "a significant scope extension... worth phasing rather than one big PR" — this doc lays out that phasing.

## Current state
The pipeline (CNN on SAR imagery + LSTM/RNN fusion) runs entirely on pre-recorded, static datasets in a notebook. No live ingestion, no streaming inference.

## Phased plan

### Phase 1 — Live AIS-only anomaly scoring
- Integrate a streaming AIS source (AISHub, MarineTraffic API, Spire, or exactAIS — pick one based on free-tier availability and coverage of the Indian Ocean region).
- Replace the static AIS dataset feeding the LSTM/RNN branches with a polling or webhook-based feed.
- Maintain a rolling sliding-window per-vessel track (fixed-length buffer) so anomaly scores update incrementally instead of needing the full historical sequence recomputed each time.
- Output: anomaly scores updating on a polling interval (e.g. every few minutes), no SAR involved yet.

### Phase 2 — SAR re-tasking integration
- True continuous SAR video isn't realistic — the honest framing is "periodic re-tasking," not real-time video.
- Explore Sentinel-1 notifications via Copernicus, or commercial re-tasking (Capella Space, ICEYE) for on-demand imagery over flagged regions from Phase 1.
- CNN branch runs on new SAR passes as they arrive, not continuously.

### Phase 3 — Streaming inference architecture
- Move from notebook batch runs to a lightweight pipeline: a queue (Kafka or Redis Streams) feeding a scheduled or event-triggered inference worker.
- This is what actually makes Phase 1/2 operational rather than a manual notebook re-run.

### Phase 4 — Alerting layer
- Dashboard or webhook/email alerts on threshold-crossing anomaly scores.
- Similar in spirit to the fraud monitoring dashboard already built for the credit-card-fraud project — same Flask + polling pattern could be reused.

## Honesty note for the README
Once any phase ships, the README should be explicit that "real-time" here means minutes-to-hours latency (driven by satellite revisit time and AIS polling interval), not sub-second. This keeps the documentation consistent with how the rest of this project already reports limitations honestly.

## Suggested order to actually build
Phase 1 → Phase 3 (needed to make Phase 1 more than a manual script) → Phase 4 → Phase 2 (SAR re-tasking is the most infra-heavy and lowest-frequency signal, so it's the best candidate to defer).

## Explicitly out of scope for this doc
No code in this commit — this is a planning artifact. Phase 1 implementation needs an actual AIS API key/account, which isn't something to provision from here.
