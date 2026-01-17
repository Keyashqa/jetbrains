from tool.graphql_queries import GET_PLAYER_STATS

#for each player and their player_id, this fetches the overall performance like role, win contribution etc
class PlayerStatsFetcher:
    def __init__(self, gql):
        self.gql = gql

    async def fetch(self, player_id: str):
        data = await self.gql.execute(
            GET_PLAYER_STATS, {"playerId": player_id}
        )
        return data["playerStatistics"]
