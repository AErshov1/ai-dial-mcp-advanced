from typing import Any

from mcp_server.tools.users.base import BaseUserServiceTool


class SearchUsersTool(BaseUserServiceTool):

    @property
    def name(self) -> str:
        return "search_user"

    @property
    def description(self) -> str:
        return "Tool for searching users. It accepts user information as parameters and returns the list of users matching the search criteria. All parameters are optional, and you can provide any combination of them to filter the search results."

    @property
    def input_schema(self) -> dict[str, Any]:
        # Provide tool params Schema:
        # - name: str
        # - surname: str
        # - email: str
        # - gender: str
        # None of them are required (see UserClient.search_users method)
        return {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "User name for searching",
                },
                "surname": {
                    "type": "string",
                    "description": "User surname for searching",
                },
                "email": {
                    "type": "string",
                    "description": "User email for searching",
                },
                "gender": {
                    "type": "string",
                    "description": "User gender for searching",
                }
            },
            "required": []
        }

    def execute(self, arguments: dict[str, Any]) -> str:
        # 1. Call user_client search_users (with `**arguments`) and return its results
        # 2. Optional: You can wrap it with `try-except` and return error as string `f"Error while searching users: {str(e)}"`
        print(f"Executing {self.name} with arguments: {arguments}")
        return self._user_client.search_users(**arguments)
