import httpx

class GraphQLClient:
    def __init__(self, url: str, api_key: str):
        self.url = url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    async def execute(self, query: str, variables: dict | None = None) -> dict:
        payload = {
            "query": query,
            "variables": variables or {},
        }

        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.post(
                self.url,
                json=payload,
                headers=self.headers,
            )
            resp.raise_for_status()
            data = resp.json()

            if "errors" in data:
                raise RuntimeError(f"GraphQL Error: {data['errors']}")

            return data["data"]
