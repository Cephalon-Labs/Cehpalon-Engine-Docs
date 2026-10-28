# Independent raw benchmark audit

Status: audit-findings. All188 gzip files were streamed;8,596,800 offered observations and6,672,000 frozen manifest rows were checked. No raw record was filtered or changed.

Startup absolute1s budgets fail for both transports. All idle pair numeric budgets pass. Main latency/allocation pairs pass, but GraphQL Engine p95 CV=0.12368092068471122 exceeds10%; the performance series remains invalid. The environment remains nonqualifying, so no full benchmark acceptance is claimed.

See audit.json for exact independently recomputed results, findings and proof limits; phase-recomputation.json and manifest-recomputation.json retain per-file hashes and results.
