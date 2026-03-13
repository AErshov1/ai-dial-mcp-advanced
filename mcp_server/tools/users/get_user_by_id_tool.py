from typing import Any

from mcp_server.tools.users.base import BaseUserServiceTool


class GetUserByIdTool(BaseUserServiceTool):

    @property
    def name(self) -> str:
        return "get_user_by_id"

    @property
    def description(self) -> str:
        return "Get user by id. This tool retrieves user information based on the provided unique user id."

    @property
    def input_schema(self) -> dict[str, Any]:
        # Provide tool params Schema. This tool applies user `id` (number) as a parameter and it is required
        return {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "integer",
                    "description": "Unique identifier of the user to retrieve",
                    "minimum": 0
                }
            },
            "required": ["user_id"]
        }

    def execute(self, arguments: dict[str, Any]) -> str:
        # 1. Get int `user_id` from arguments
        # 2. Call user_client get_user and return its results
        # 3. Optional: You can wrap it with `try-except` and return error as string `f"Error while retrieving user by id: {str(e)}"`
        user_id = arguments.get("user_id")
        if user_id is None:
            raise ValueError("user_id is required")
