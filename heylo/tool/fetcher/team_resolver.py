from tool.graphql_queries import GET_TEAMS

#grid api does not have direct team lookup by name, so we fetch all teams and filter using name to find id. 
#additionally this acts as a validation step to ensure the team exists.

class TeamResolver:
    def __init__(self, gql):
        self.gql = gql

    async def resolve(self, team_name: str) -> dict:
        data = await self.gql.execute(GET_TEAMS)

        for edge in data["teams"]["edges"]:
            node = edge["node"]
            if node["name"].lower() == team_name.lower():
                return {
                    "team_id": node["id"],
                    "name": node["name"]
                }

        raise ValueError(f"Team '{team_name}' not found")
