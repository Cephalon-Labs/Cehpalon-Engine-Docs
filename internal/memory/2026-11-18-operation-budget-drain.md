# Operation budget drain handoff

The 2026-11-18 continuation delivered Engine `cb9088cc9b02f3855107444e28bb1af592a13ad4`. Both admission budgets permanently close and let admitted work finish cleanup. Each drain waiter can cancel its wait independently. The generated host closes admissions before Kestrel stops. Tests include a held protected write during shutdown for both budget modes.

Windows and WSL passed 519 and 516 Engine checks, respectively. The real generated verifier passed 153 each. The fixed synchronous observation retained 56 B/op with mixed paired timing changes across hosts. See the [results](../planning/operation-budget-drain.md) and [protocol](../validation/operation-budget-drain.md).

#18 and #20 remain In Progress. #3 stays Blocked because hosted smoke still omits live PostgreSQL and RabbitMQ. No GitHub usage or billing skips occurred. The canonical benchmark gates remain as recorded.
