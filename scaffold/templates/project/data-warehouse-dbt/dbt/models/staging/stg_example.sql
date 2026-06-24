-- models/staging/stg_example.sql
-- Staging model: select and rename columns from the raw source.
-- Materialised as a view. No business logic here.
-- Replace 'raw_schema.raw_orders' with your source table.

with source as (
    select * from {{ source('raw', 'orders') }}
),

renamed as (
    select
        id                                  as order_id,
        user_id,
        status,
        amount,
        created_at                          as ordered_at,
        updated_at

    from source
    -- Exclude soft-deleted records if the source uses a deleted_at flag
    where deleted_at is null
)

select * from renamed
