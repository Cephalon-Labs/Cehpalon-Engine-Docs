# Retained conformance01 negative outcome

Windows01 completed all4,000 corpus executions (including400 cancellation cases) and120 repeated host lifecycles, but one case failed. Linux01 completed the same matrix with zero failures. These complete results remain retained.

Windows baseline-http case409:

- Actual client abort tick:1962827142176.
- Handler entry tick:1962827145558, **0.3382ms after abort** at the recorded10MHz clock.
- Server acknowledgement: 0.5528ms after abort.
- No-mutation flag: True; owned handler completed: True.

The acknowledgement and cleanup outcomes do not satisfy the missing handler-entered-before-abort condition. Windows01 therefore does not pass the declared in-flight cancellation criterion. The exact source remains unchanged.

Root reports simultaneous two-host conformance and metadata/staging work. Interference is possible, but is not proven as the cause. Root predeclared a complete sequential Windows02 thenLinux02 repeat with unchanged criteria and no concurrent builds/audits/hash work. Neither01host may be discarded, and no single-case favorable replacement is allowed. A staging identity pass does not promote conformance, platform or #3 status.

This audit issued no build, test, request or timing. Its activity stops before the sequential repeat begins.
