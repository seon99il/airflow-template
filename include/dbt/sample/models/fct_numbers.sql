select id, id * id as squared from {{ ref('stg_numbers') }}
