class EVMQuery:
    @staticmethod
    def get_blocks(table: str) -> str:
        query = f"""
        with base as (
            select number, row_number() over (order by number) rn from {table}
        )
        select 
            distinct(number) 
        from 
            base
        where not
            rn - number = 1
        """
        return query
