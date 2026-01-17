import psycopg2
from normalization.normalized_data import NormalizedTeam

class PostgresStore:
    def __init__(self, dsn: str):
        self.conn = psycopg2.connect(dsn)

    def upsert_team(self, team: NormalizedTeam):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO teams
                (team_id, name, color_primary, color_secondary, logo_url, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (team_id)
                DO UPDATE SET
                    name = EXCLUDED.name,
                    color_primary = EXCLUDED.color_primary,
                    color_secondary = EXCLUDED.color_secondary,
                    logo_url = EXCLUDED.logo_url,
                    updated_at = EXCLUDED.updated_at
                """,
                (
                    team.team_id,
                    team.name,
                    team.color_primary,
                    team.color_secondary,
                    team.logo_url,
                    team.updated_at,
                ),
            )

            cur.execute(
                "DELETE FROM team_external_links WHERE team_id = %s",
                (team.team_id,),
            )

            for link in team.external_links:
                cur.execute(
                    """
                    INSERT INTO team_external_links
                    (team_id, provider, external_id)
                    VALUES (%s, %s, %s)
                    """,
                    (team.team_id, link.provider, link.external_id),
                )

        self.conn.commit()
