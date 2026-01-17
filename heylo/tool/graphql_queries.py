GET_TEAMS = """
query GetTeams {
  teams(first: 50) {
    edges {
      node {
        id
        name
      }
    }
  }
}
"""

GET_RECENT_SERIES = """
query GetRecentSeries($titleId: Int!) {
  allSeries(
    first: 10
    filter: { titleId: $titleId, types: ESPORTS }
    orderBy: StartTimeScheduled
    orderDirection: DESC
  ) {
    edges {
      node {
        id
        startTimeScheduled
        tournament { name }
        teams { baseInfo { name } }
      }
    }
  }
}
"""

GET_SERIES_STATE = """
query GetSeriesState($seriesId: ID!) {
  seriesState(id: $seriesId) {
    valid
    finished
    teams { name won }
    games {
      sequenceNumber
      teams {
        name
        players {
          name
          kills
          deaths
          money
          position { x y }
        }
      }
    }
  }
}
"""

GET_TEAM_STATS = """
query TeamStatsLast3Months($teamId: ID!) {
  teamStatistics(teamId: $teamId, filter: { timeWindow: LAST_3_MONTHS }) {
    series { count kills { avg } }
    game { wins { value percentage } }
    segment { type count }
  }
}
"""

GET_TEAM_ROSTER = """
query GetTeamRoster($teamId: ID!) {
  players(filter: { teamIdFilter: { id: $teamId } }) {
    edges {
      node {
        id
        nickname
      }
    }
  }
}
"""

GET_PLAYER_STATS = """
query PlayerStatsLast3Months($playerId: ID!) {
  playerStatistics(playerId: $playerId, filter: { timeWindow: LAST_3_MONTHS }) {
    series { count kills { avg } }
    game { wins { percentage } }
    segment { type deaths { avg } }
  }
}
"""
