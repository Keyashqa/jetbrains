"""
Google ADK Tool wrapper for GRID data fetcher
"""

from typing import Dict, Any
from clients.grqphql_client import GraphQLClient
from storage.redis_cache import RedisCache
from tool.fetcher.team_resolver import TeamResolver
from tool.fetcher.series_fetcher import SeriesFetcher
from tool.fetcher.series_state_fetcher import SeriesStateFetcher
from tool.fetcher.team_stats_fetcher import TeamStatsFetcher
from tool.fetcher.player_roster_fetcher import PlayerRosterFetcher
from tool.fetcher.player_stats_fetcher import PlayerStatsFetcher
from tool.data_fetch_tool import GridDataFetcher
from config import Config

# ---------- Dependency initialization (singleton-style) ----------

_gql_client = GraphQLClient(
    Config.GRID_GRAPHQL_URL,
    Config.GRID_API_KEY
)

_redis_cache = RedisCache(Config.REDIS_URL)

_team_resolver = TeamResolver(_gql_client)
_series_fetcher = SeriesFetcher(_gql_client)
_series_state_fetcher = SeriesStateFetcher(_gql_client)
_team_stats_fetcher = TeamStatsFetcher(_gql_client)
_player_roster_fetcher = PlayerRosterFetcher(_gql_client)
_player_stats_fetcher = PlayerStatsFetcher(_gql_client)

_grid_fetcher = GridDataFetcher(
    gql=_gql_client,
    cache=_redis_cache,
    team_resolver=_team_resolver,
    series_fetcher=_series_fetcher,
    series_state_fetcher=_series_state_fetcher,
    team_stats_fetcher=_team_stats_fetcher,
    roster_fetcher=_player_roster_fetcher,
    player_stats_fetcher=_player_stats_fetcher,
)

# ---------- ADK Tool Handler ----------

async def grid_team_analysis_tool(
    team_name: str,
    title_id: int
) -> Dict[str, Any]:
    """
    Google ADK tool handler.
    This is what the agent actually calls.
    """
    return await _grid_fetcher.run(
        team_name=team_name,
        title_id=title_id
    )

# ---------- Tool Metadata ----------

GRID_TEAM_ANALYSIS_SCHEMA = {
    "name": "grid_team_analysis",
    "description": (
        "Fetches esports team intelligence from GRID including "
        "recent matches, live/historical series state, team statistics, "
        "and player-level tendencies."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "team_name": {
                "type": "string",
                "description": "Exact team name as used by GRID (case-insensitive)"
            },
            "title_id": {
                "type": "integer",
                "description": "Game title ID (6 = VALORANT, 3 = LoL, etc.)"
            }
        },
        "required": ["team_name", "title_id"]
    }
}
