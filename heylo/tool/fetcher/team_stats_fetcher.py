from tool.graphql_queries import GET_TEAM_STATS

#this gives the average performance stats of a team across all titles they have played in.
class TeamStatsFetcher:
    def __init__(self, gql):
        self.gql = gql

    async def fetch(self, team_id: str):
        data = await self.gql.execute(
            GET_TEAM_STATS, {"teamId": team_id}
        )
        return data["teamStatistics"]
