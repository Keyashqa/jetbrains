from tool.graphql_queries import GET_TEAM_ROSTER

#for a given team id, it fetches the player_id and nickname of all players in that team
class PlayerRosterFetcher:
    def __init__(self, gql):
        self.gql = gql

    async def fetch(self, team_id: str):
        data = await self.gql.execute(
            GET_TEAM_ROSTER, {"teamId": team_id}
        )

        return [
            {
                "player_id": p["node"]["id"],
                "nickname": p["node"]["nickname"]
            }
            for p in data["players"]["edges"]
        ]
