-- models/marts/mart_example.sql
-- Mart model: aggregated, business-ready table for BI tools.
-- Materialised as a table for query performance.
-- Replace with real metric definitions.

with orders as (
    select * from {{ ref('stg_example') }}
),

order_summary as (
    select
        date_trunc('day', ordered_at)       as order_date,
        status,
        count(*)                            as order_count,
        sum(amount)                         as total_amount_cents,
        round(sum(amount) / 100.0, 2)       as total_amount,
        avg(amount)                         as avg_amount_cents,
        count(distinct user_id)             as distinct_users

    from orders
    group by 1, 2
)

select * from order_summary
