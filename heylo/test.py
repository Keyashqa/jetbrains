#running tests on the data fetch tool using google sdk

import asyncio
from tool.adk_tool import grid_team_analysis_tool

async def test():
    result = await grid_team_analysis_tool(
        team_name="Team Liquid",
        title_id=6
    )
    print(result)

asyncio.run(test())
