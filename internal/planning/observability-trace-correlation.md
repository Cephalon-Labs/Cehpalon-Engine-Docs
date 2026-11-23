# Proposed dispatch trace and log correlation for #18

## First delivery

Allow a host to opt in to one completion record from a selected Core
dispatcher. The record contains a fixed event name, the existing bounded
dispatch outcome, elapsed duration and optional W3C trace and span IDs.
Capture the IDs once from the ambient Activity at dispatch entry. Capture
nullable typed IDs as values so the observer never retains an Activity or
operation context. The host owns the structured log sink. Continue to use
the existing duration histogram and its bounded outcome tag.
[W3C Trace Context](https://www.w3.org/TR/2021/REC-trace-context-1-20211123/)

For a protected HTTPS proof, observe the outer Core gateway shared by HTTP
and GraphQL. Use the ASP.NET server Activity that is already active on those
paths. Keep handler correlation under the existing operation-context
contract and let ASP.NET own incoming context parsing. Trace and span IDs
are diagnostic data and carry no caller or tenant authority. Keep them out of
metric dimensions. A future internal child span requires its own lifecycle
and observer-isolation design.
[ASP.NET Core request diagnostics at .NET 11.0.0](https://github.com/dotnet/aspnetcore/blob/v11.0.0/src/Hosting/Hosting/src/Internal/HostingApplicationDiagnostics.cs#L378-L426)

Use the field allowlist above. Exclude
custom correlation values, raw headers, trace state, baggage, tenant,
principal, resource, operation and module identifiers, request contents,
metadata and exception details. Export and retention settings belong to
the host's telemetry policy. Define the callback as a synchronous,
best-effort observation after Core handler cleanup. The timing interval ends
before the callback. The selected dispatcher may still sit inside an
enclosing admission permit. The callback must return without waiting on the
dispatch or its drain. Invoke it outside Engine locks, contain callback
exceptions, and suppress same-flow recursive notifications.

## Acceptance of the first delivery

- Confirm that opting out keeps the existing dispatcher contract and that a
  dispatcher with either no ambient Activity or a non-W3C Activity emits
  absent trace IDs.
- Cover success, expected failure, cancellation, execution fault and
  cleanup fault. Verify the record arrives after held cleanup finishes and
  that throwing or recursively dispatching observers preserve the caller's
  result, exception ordering and cleanup.
- Exercise actual protected HTTPS through HTTP and GraphQL. The opt-in
  outer gateway should emit one event for an owner request, one for an
  authenticated tenant denial and zero for an anonymous denial. The
  existing histogram observes both Core layers. Verify native trace
  correlation with overlapping requests and parallel GraphQL fields.
- Check absent or malformed trace headers against the native request
  Activity observed by the fixture. Verify the structured payload against
  private fixture sentinels and publish only the comparison outcomes.
- After functional proof, predeclare disabled and enabled component
  measurements, with and without ambient trace context. A separate
  supported-path exercise covers shutdown, recovery and exporter overhead.

The proposal scopes the next #18 implementation slice. Widening to
additional dispatch layers, worker or broker propagation, internal spans
or external exporters needs its own contract and evidence.
