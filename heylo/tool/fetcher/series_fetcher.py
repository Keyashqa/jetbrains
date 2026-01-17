from tool.graphql_queries import GET_RECENT_SERIES

# Fetch recent series for a given team name and title ID
#we collect the series-id to check recent performence of a team in a title.
class SeriesFetcher:
    def __init__(self, gql):
        self.gql = gql

    async def fetch_for_team(self, team_name: str, title_id: int):
        data = await self.gql.execute(
            GET_RECENT_SERIES, {"titleId": title_id}
        )

        series = []
        for edge in data["allSeries"]["edges"]:
            node = edge["node"]
            team_names = [t["baseInfo"]["name"] for t in node["teams"]]

            if team_name in team_names:
                series.append({
                    "series_id": node["id"],
                    "start_time": node["startTimeScheduled"],
                    "tournament": node["tournament"]["name"],
                    "teams": team_names
                })

        return series
