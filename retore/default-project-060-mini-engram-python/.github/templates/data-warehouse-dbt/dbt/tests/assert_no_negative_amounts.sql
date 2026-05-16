-- tests/assert_no_negative_amounts.sql
-- Custom singular data test: verify no negative amounts in the orders mart.
-- dbt will fail the test if this query returns any rows.

select
    order_id,
    amount
from {{ ref('stg_example') }}
where amount < 0
