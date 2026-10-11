---
paths:
  - "**/migrations/**"
  - "**/schema/**"
  - "**/models/**"
  - "**/db/**"
  - "**/*.{sql,prisma}"
---

# Data and database design

Treat data changes as contract changes.

Before changing schema or persistence behavior, understand:
- existing constraints;
- indexes;
- nullability;
- relationships;
- transaction boundaries;
- generated types or clients;
- migration ordering;
- production compatibility.

Prefer additive and backwards-compatible migrations when practical.

Do not manually alter generated database artifacts when a source schema or generator exists.

Treat destructive migrations and bulk data operations as high-risk.

Consider concurrency, locking, partial deployment, rollback, and data integrity when relevant.

Do not use production data as a casual debugging surface.
