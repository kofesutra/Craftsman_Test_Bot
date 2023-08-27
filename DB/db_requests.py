class Request:
    def __init__(self, connector):
        self.connector = connector

    async def get_all(self, value):
        query = f'SELECT * FROM {value}'
        result = await self.connector.execute(query)
        return await result.fetchall()

    async def get_selected(self, table, condition_name, condition):
        query = f'SELECT * FROM {table} WHERE {condition_name} = {condition}'
        result = await self.connector.execute(query)
        return await result.fetchall()

    async def get_max_selected(self, table, condition_name, condition):
        query = f'SELECT * FROM {table} WHERE {condition_name} = {condition} AND id = (SELECT MAX (id) FROM {table})'
        result = await self.connector.execute(query)
        return await result.fetchall()

    async def get_one(self, request, table, condition_name, condition):
        query = f'SELECT {request} FROM {table} WHERE {condition_name} = {condition}'
        result = await self.connector.execute(query)
        return await result.fetchone()

    async def add_line(self, table, columns, values):
        query = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        await self.connector.execute(query)
        return True

    async def update_line(self, table, values, condition_name, condition):
        query = f"UPDATE {table} SET {values} WHERE {condition_name} = {condition}"
        await self.connector.execute(query)
        return True

    async def delete_from_db(self, table, condition_name, condition):
        query = f"DELETE FROM {table} WHERE {condition_name} = {condition}"
        await self.connector.execute(query)
        return
