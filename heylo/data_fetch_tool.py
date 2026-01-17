from datetime import datetime

class GridDataFetcher:
    def __init__(
        self,
        gql,
        cache, #key value redis cache
        team_resolver, #get the team id from team name
        series_fetcher, #get the recent series played by the team
        series_state_fetcher, #get detailed analysis of the series and perfromance of the team
        team_stats_fetcher, #get the average team stats across all titles
        roster_fetcher, #get the player ids from the team id
        player_stats_fetcher, #get the individual player details from player id
    ):
        self.gql = gql
        self.cache = cache
        self.team_resolver = team_resolver
        self.series_fetcher = series_fetcher
        self.series_state_fetcher = series_state_fetcher
        self.team_stats_fetcher = team_stats_fetcher
        self.roster_fetcher = roster_fetcher
        self.player_stats_fetcher = player_stats_fetcher

    async def run(self, team_name: str, title_id: int):
        cache_key = f"grid:team_analysis:{team_name}:{title_id}"
        #check if data is present in cache
        cached = self.cache.get(cache_key) #return null if not present
        if cached:
            return cached

        #start pipeline to fetch data
        #get team id from team name
        team = await self.team_resolver.resolve(team_name)

        #get recent series for the team in the given title
        series = await self.series_fetcher.fetch_for_team(
            team["name"], title_id
        )

        #get detailed series state for each series
        series_states = []
        for s in series:
            series_states.append(
                await self.series_state_fetcher.fetch(s["series_id"])
            )

        #get overall team stats for all titles
        team_stats = await self.team_stats_fetcher.fetch(team["team_id"])

        #get player id from team id
        roster = await self.roster_fetcher.fetch(team["team_id"])

        #get player stats for each player in the roster
        players = []
        for p in roster:
            stats = await self.player_stats_fetcher.fetch(p["player_id"])
            players.append({
                "player": p,
                "statistics": stats
            })

        #aggregate all the data into a agent friendly format - json simple dict
        output = {
            "team": team,
            "recent_series": series,
            "series_states": series_states,
            "team_statistics": team_stats,
            "players": players,
            "metadata": {
                "source": "grid",
                "generated_at": datetime.now().isoformat()
            }
        }

        #store in cache for future use
        self.cache.set(cache_key, output)

        #return the aggregated output
        return output
