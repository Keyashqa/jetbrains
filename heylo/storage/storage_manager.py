class StorageManager:
    def __init__(self, redis_cache, postgres_store):
        self.redis = redis_cache
        self.postgres = postgres_store

    def store_team(self, team):
        self.redis.set_team(team.team_id, team.dict())
        self.postgres.upsert_team(team)
