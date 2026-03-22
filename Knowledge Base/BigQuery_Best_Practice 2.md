### BigQuery SQL Best Practices

#### Working with Dates and Timestamps

When filtering data based on a time interval, especially when dealing with months or years, it's important to use the correct functions to avoid errors.

**Incorrect Usage:**

BigQuery's `TIMESTAMP_SUB` function does **not** support `MONTH` or `YEAR` as date parts when the first argument is a `TIMESTAMP`. The following will result in an error:

```sql
-- This will fail
SELECT * FROM my_table
WHERE my_timestamp_column >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 12 MONTH);
```

**Correct Usage:**

To filter for a period of months or years, you should cast the timestamp column to a `DATE` and use `DATE_SUB` with `CURRENT_DATE()`.

```sql
-- This is the correct way
SELECT * FROM my_table
WHERE DATE(my_timestamp_column) >= DATE_SUB(CURRENT_DATE(), INTERVAL 12 MONTH);
```

This approach correctly handles the date subtraction and comparison.

#### Avoid "Aggregations of Aggregations"

BigQuery does not allow aggregate functions to be nested inside other aggregate functions. A common pitfall is placing `COUNT(...)`, `SUM(...)`, etc., inside `ARRAY_AGG(...)` or inside the `ORDER BY` of an aggregate.

Incorrect (will raise: "Aggregations of aggregations are not allowed"):

```sql
-- BAD: nested aggregates inside ARRAY_AGG
SELECT
  ARRAY_AGG(STRUCT(
    year,
    COUNT(DISTINCT pme_reference_no) AS case_volume,
    SUM(act_los_day_cnt) AS total_los_cnt,
    SAFE_DIVIDE(SUM(act_los_day_cnt), COUNT(DISTINCT pme_reference_no)) AS avg_los
  ) ORDER BY year)
FROM base
GROUP BY year;
```

Correct pattern: pre-aggregate in a subquery (or CTE), then build the array from plain columns.

```sql
-- GOOD: compute aggregates first, then aggregate rows into an array
SELECT
  ARRAY_AGG(t ORDER BY t.year) AS by_year
FROM (
  SELECT
    year,
    COUNT(DISTINCT pme_reference_no) AS case_volume,
    SUM(act_los_day_cnt) AS total_los_cnt,
    SAFE_DIVIDE(SUM(act_los_day_cnt), COUNT(DISTINCT pme_reference_no)) AS avg_los
  FROM base
  GROUP BY year
) AS t;
```

Key takeaway: never pass aggregate expressions as arguments to another aggregate. Always move inner aggregates into a prior SELECT/CTE.

#### Deterministic ARRAY_AGG Ordering

Arrays are unordered unless you specify `ORDER BY` inside `ARRAY_AGG`. Do not rely on subquery ordering to carry through.

```sql
-- Preferred: order inside ARRAY_AGG
SELECT ARRAY_AGG(t ORDER BY t.year, t.case_volume DESC)
FROM (
  SELECT year, COUNT(*) AS case_volume FROM base GROUP BY year
) AS t;
```

If you need only the top K elements, pair `ORDER BY` with `LIMIT` in a subquery or apply window functions (see below) and then `ARRAY_AGG`.

#### CTE Scope and Referencing (fixing "Unrecognized name: ctx")

- A CTE's columns are only visible within subsequent CTEs or the outer query when it participates in the `FROM` clause (directly or via a cross join).
- For single-row parameter CTEs (e.g., `ctx`), reference their fields by listing the CTE alongside tables in `FROM`:

```sql
WITH ctx AS (
  SELECT DATE('2024-01-01') AS start_date, DATE('2025-10-20') AS end_date,
         ['ME'] AS lob_whitelist, ['SNF'] AS stay_type_whitelist, ['PA'] AS state_whitelist
), base AS (
  SELECT EXTRACT(YEAR FROM decision_eff_dt) AS year,
         prncpl_icd9_dxgrp_dscrptn, prim_fac_prvdr_nm, pme_reference_no, act_los_day_cnt
  FROM `project.dataset.2mn_metrics`, ctx
  WHERE pending_auth_ind = 0
    AND LOWER(admission_type_desc) IN ('elective', 'emergency/urgent')
    AND decision_eff_dt BETWEEN ctx.start_date AND ctx.end_date
    AND business_ln_cd IN UNNEST(ctx.lob_whitelist)
    AND stay_srv_type_desc IN UNNEST(ctx.stay_type_whitelist)
    AND provider_state_postal_cd IN UNNEST(ctx.state_whitelist)
)
SELECT AS STRUCT (
  SELECT AS STRUCT start_date, end_date, lob_whitelist, stay_type_whitelist, state_whitelist,
                   (SELECT COUNT(*) FROM base) AS base_rows
  FROM ctx
) AS context;
```

Notes:
- If you reference `ctx.field` outside of `FROM`, ensure `ctx` is in scope (e.g., via a subselect `FROM ctx`).
- Avoid scalar subqueries to fetch lists; prefer `IN UNNEST(ctx.list)` as shown.

#### Top-N Per Group via Window Functions (after pre-aggregation)

Always pre-aggregate to the desired grain before ranking. Then use window functions for top-N per group.

```sql
WITH agg AS (
  SELECT
    year,
    prncpl_icd9_dxgrp_dscrptn AS diagnosis_group,
    COUNT(DISTINCT pme_reference_no) AS case_volume,
    SUM(act_los_day_cnt) AS total_los_cnt,
    SAFE_DIVIDE(SUM(act_los_day_cnt), COUNT(DISTINCT pme_reference_no)) AS avg_los
  FROM base
  GROUP BY year, diagnosis_group
), ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY year ORDER BY case_volume DESC) AS rn
  FROM agg
)
SELECT ARRAY_AGG(STRUCT(year, diagnosis_group, case_volume, total_los_cnt, avg_los)
                 ORDER BY year, case_volume DESC)
FROM ranked
WHERE rn <= 10;
```

#### Context/CTE Pattern for Parameters and Whitelists

Use a single-row `ctx` CTE for dates and filter whitelists, and reference it via a cross join. This avoids repeated scalar subqueries and improves clarity.

```sql
WITH ctx AS (
  SELECT
    DATE('2024-01-01') AS start_date,
    DATE('2025-10-20') AS end_date,
    ['ME'] AS lob_whitelist,
    ['SNF'] AS stay_type_whitelist,
    ['PA'] AS state_whitelist
), base AS (
  SELECT
    EXTRACT(YEAR FROM decision_eff_dt) AS year,
    prncpl_icd9_dxgrp_dscrptn,
    pme_reference_no,
    act_los_day_cnt
  FROM `your_project.your_dataset.2mn_metrics`, ctx
  WHERE
    pending_auth_ind = 0
    AND LOWER(admission_type_desc) IN ('elective', 'emergency/urgent')
    AND decision_eff_dt BETWEEN ctx.start_date AND ctx.end_date
    AND business_ln_cd IN UNNEST(ctx.lob_whitelist)
    AND stay_srv_type_desc IN UNNEST(ctx.stay_type_whitelist)
    AND provider_state_postal_cd IN UNNEST(ctx.state_whitelist)
)
SELECT ...
```

Notes:
- `ctx` is a single-row CTE; listing it in the `FROM` clause behaves like a cross join to make its fields directly addressable.
- Prefer `IN UNNEST(ctx.list)` to repeated `(SELECT list FROM ctx)` scalar subqueries.

#### Null-Safe Math and Division

- Use `SAFE_DIVIDE(numerator, denominator)` to avoid division-by-zero errors; it returns `NULL` when the denominator is 0.
- When appropriate, coalesce to zero or another default: `COALESCE(SAFE_DIVIDE(...), 0) AS ratio`.
- For integer inputs where fractional precision matters, cast to a floating type explicitly before division.

#### Working with Date and Timestamp Ranges

- For month/year deltas, prefer `DATE_SUB(CURRENT_DATE(), INTERVAL N MONTH|YEAR)` and compare against `DATE(column)`.
- For timestamp ranges, consider half-open intervals to avoid off-by-one issues:

```sql
-- Half-open interval for timestamps
WHERE ts >= TIMESTAMP('2025-01-01')
  AND ts <  TIMESTAMP('2025-02-01')
```

- Extracting calendar parts: use `EXTRACT(YEAR FROM DATE(ts))`, `DATE_TRUNC(DATE(ts), MONTH)` when grouping by periods.

#### Packaging Results with STRUCT and Arrays

- Use `SELECT AS STRUCT` to bundle context metadata.
- Build arrays of records only from already-aggregated rows (no aggregates inside `ARRAY_AGG` arguments).

```sql
SELECT AS STRUCT
  (
    SELECT AS STRUCT ctx.start_date, ctx.end_date, ctx.lob_whitelist
  ) AS context,
  (
    SELECT ARRAY_AGG(t ORDER BY t.year) FROM (
      SELECT year, COUNT(*) AS case_volume FROM base GROUP BY year
    ) AS t
  ) AS by_year;
```

#### QUALIFY for Window Function Filtering

- Use `QUALIFY` to filter by window function results without wrapping another subquery.

```sql
SELECT *
FROM (
  SELECT account_id,
         event_date,
         ROW_NUMBER() OVER (PARTITION BY account_id ORDER BY event_date DESC) AS rn
  FROM `project.dataset.events`
)
QUALIFY rn = 1; -- top-1 per account
```

#### Partitioning and Clustering Aware Filters

- Always filter on partition columns using simple predicates for partition pruning (e.g., `event_date BETWEEN DATE '2025-01-01' AND DATE '2025-01-31'`).
- When clustered, filter and order by clustering keys to reduce scanned bytes.
- Avoid applying functions to the partition column in the predicate (prefer `event_date BETWEEN ...` over `DATE(event_ts) BETWEEN ...`).

#### Arrays and UNNEST Patterns

- Use `IN UNNEST(array_expression)` for membership checks.
- When joining with repeated fields, `CROSS JOIN UNNEST(repeated_field) AS element` is explicit and avoids accidental cartesian blowups.
- For optional arrays, use `LEFT JOIN UNNEST(...)` to retain parent rows with empty arrays.

```sql
SELECT user_id
FROM `project.dataset.users`
WHERE 'PA' IN UNNEST(state_whitelist);
```

#### Parameterization and Safety

- Prefer query parameters via client libraries rather than string interpolation.
- Validate and normalize input lists and dates before constructing `UNNEST` arrays.
- Use `SAFE_CAST` and `SAFE.` functions (`SAFE_DIVIDE`, `SAFE_OFFSET`, `SAFE_ORDINAL`) to avoid runtime errors where appropriate.

```sql
SELECT SAFE_CAST(json_field AS INT64) AS id
FROM `project.dataset.raw`;
```

#### Approximate Aggregations for Large Data

- Use `APPROX_COUNT_DISTINCT(expr)` when exact distinct counts are not required, for significant performance gains.

```sql
SELECT APPROX_COUNT_DISTINCT(user_id) AS approx_users
FROM `project.dataset.events`
WHERE event_date BETWEEN DATE '2025-01-01' AND DATE '2025-01-31';
```

#### Join Typing and Null Semantics

- Ensure join key types match to avoid implicit casts that disable partition/clustering pruning.
- Consider null-handling explicitly (`COALESCE`, `IS [NOT] NULL`) and understand that `NULL` keys do not match in `JOIN` equality.
- Use `USING(key)` for succinctness when both sides share the same column name.

#### Avoid SELECT * in Production Queries

- Enumerate required columns to reduce scanned bytes and avoid schema-drift issues.
- Prefer `SELECT AS STRUCT`/named fields for API payloads to ensure stable output schemas.

#### Quick Pitfalls Checklist

- Do not nest aggregates (e.g., `COUNT(...)` inside `ARRAY_AGG(...)`).
- Always specify `ORDER BY` inside `ARRAY_AGG` if you need deterministic order.
- Pre-aggregate to the target grain before ranking or further aggregation.
- Prefer a `ctx` CTE with cross join over repeated scalar subqueries.
- Use `SAFE_DIVIDE` (and `COALESCE` if needed) for ratios.
- Cast timestamps to `DATE` for month/year arithmetic with `DATE_SUB`/`DATE_ADD`.
- Use `QUALIFY` to filter windowed rows without extra subqueries.
- Filter by partition columns with simple predicates; leverage clustering in filters/orders.
- Use `IN UNNEST(array)` for membership; `LEFT JOIN UNNEST` to preserve outer rows.
- Parameterize inputs; prefer `SAFE_CAST`/`SAFE_*` helpers.
- Prefer `APPROX_COUNT_DISTINCT` when exactness is not required.
- Avoid `SELECT *`; list needed columns for stability and cost.
