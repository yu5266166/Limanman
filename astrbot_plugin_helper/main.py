import logging
import sys
from astrbot.api.event import filter
from astrbot.api.star import Context, Star, register
from astrbot.api.event.filter import PermissionType

logger = logging.getLogger(__name__)

@register(
    "astrbot_plugin_helper",
    "Limanman",
    "辅助清理缓存插件",
    "1.0.0",
    "https://github.com/Limanman/astrbot_plugin_helper",
)
class HelperPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.llm_tool(name="helper_clean_cache")
    async def helper_clean_cache(self, event) -> str:
        """辅助清理 sys.modules 里的特定插件缓存，以便重载。"""
        removed = []
        for key in list(sys.modules.keys()):
            if any(x in key for x in ['zanwo', 'send_tool', 'astrbot_plugin_zanwo', 'astrbot_plugin_send_tool']):
                sys.modules.pop(key, None)
                removed.append(key)
        return f"Successfully cleared main process sys.modules cache: {removed}"
