# Engine qualification commit trace

- Engine commit: `5a6795b34535fdc311b519e8d452ea1c9f715bba`
- Engine issue: #3.
- Change: exact SDK/global.json and direct dependency pins, locked63-package qualification graph, bounded HTTPS/JWT/GraphQL/PostgreSQL/RabbitMQ smoke executable, retained failures/inventories, and immutable-action Linux/Windows CI workflow.
- Main-checkout local validation before commit: locked restore/Release build passed with0warnings/errors; owned-provider smoke14/14 on Windows26H2 (observational/unlisted host) and WSL Ubuntu22.04.5 (listed distribution); no provider checks skipped.
- Actual SDK archive SHA512, selected package assets/raw archive hashes/content-hash consistency, source hashes and same-host rebuild evidence are retained in Engine Tests/PlatformQualification/evidence.
- Platform/provider smoke is not Engine Core/composition/tenant/business/AI/E2E/HA/benchmark/production proof. Engine feature maturity remainsM0.
- Exact committed-source local results are in `exact-engine-win.json` and `exact-engine-linux.json`. Hosted CI for this revision was rejected before steps by reported account payments/spending limit; see `hosted-ci-blocker.json`. Local tests are not a hosted CI pass.
- GraphQL transitive ChilliCream.Nitro.App license differs from MIT; redistribution approval is pending under release work, and nothing was published.
