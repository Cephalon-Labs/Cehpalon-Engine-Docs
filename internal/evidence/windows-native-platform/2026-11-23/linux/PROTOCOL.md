# Linux WSL GA real-driver smoke

This run complements Engine issue #3. It executes the existing 14-case PlatformQualification harness at exact Engine c18757f7ef4df2c78c73e902aa39d05424e6bcff on Ubuntu 22.04.5 LTS under WSL. Seven build/runtime inputs come from a Git archive made after verifying the exact clean Engine checkout. The archive SHA-256 and frozen W0 manifest SHA-256 are embedded in run.py. New evidence does not modify the package lock or the existing harness.

Use the private Linux .NET GA 11.0.100 SDK and a local Linux/amd64 Docker default context. PostgreSQL 18.6 and bare RabbitMQ 4.4.0 use the immutable Linux/amd64 OCI manifest and config digests from the W0 manifest. The runner verifies inspect identity, container platform, real readiness, actual server and Erlang/OTP versions, the full 14/14 outcome, and teardown. It caches the required pulled images and creates unique containers and bridge owned by this attempt. Provider bindings are IPv4 loopback only, with expiring random fixture credentials in a private native WSL temporary directory. Build artifacts and the package cache are isolated there. Temporary files are removed during cleanup.

Run only after other work on this shared host has completed.

    wsl -d Ubuntu -- python3 /mnt/d/Cephalon/Cehpalon-Engine/.local/continuation-delivery-20261123/platform-linux/run.py --dotnet /mnt/d/Cephalon/.tools/dotnet11-ga/linux-x64/dotnet --out /mnt/d/Cephalon/Cehpalon-Engine/.local/continuation-delivery-20261123/platform-linux/attempt01

Each attempt retains sanitized command stdout/stderr and the bounded qualification results. On failure inspect the attempt directory, fix only the stated cause, and start a new attempt. No application E2E, Windows qualification, native-host performance, provider TLS, HA, restart or production maturity follows from this bounded WSL smoke.

