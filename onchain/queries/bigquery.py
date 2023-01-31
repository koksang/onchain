class EVMQuery:
    @staticmethod
    def block(table: str) -> str:
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

    @staticmethod
    def transaction(blocks_table: str, transactions_table: str) -> str:
        # TODO: Transaction query
        raise NotImplementedError
        query = """

        """
        return query
