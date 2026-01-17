from tool.graphql_queries import GET_SERIES_STATE

#when we provide the series-id we get the per game stats and per player stats for that series.\
#Win/Loss, maps played, scores etc. is used to derive more detailed performance metrics like map control, shot fired etc
class SeriesStateFetcher:
    def __init__(self, gql):
        self.gql = gql

    async def fetch(self, series_id: str):
        data = await self.gql.execute(
            GET_SERIES_STATE, {"seriesId": series_id}
        )
        return data["seriesState"]
