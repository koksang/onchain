with blocks as (

    select number
    from
        {{ source("polygon", "blocks") }}
    order by
        number desc
    limit
        2

),

min_max as (

    select

        min(number) as min_number,
        least(min(number) + 1000000, max(number)) as max_number
        -- limit to 1m new blocks every run

    from
        blocks
)

select number
from
    min_max,
    unnest(generate_array(min_number + 1, max_number)) as number
