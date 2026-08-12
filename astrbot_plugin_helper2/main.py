import logging
import sys
from astrbot.api.event import filter
from astrbot.api.star import Context, Star, register

logger = logging.getLogger(__name__)

@register(
    "astrbot_plugin_helper2",
    "Limanman",
    "辅助清理缓存插件2",
    "1.0.0",
    "https://github.com/yu5266166/Yu-and-Limanman/tree/main/astrbot_plugin_helper2",
)
class HelperPlugin2(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        # 在初始化时，清理 sys.modules 里的特定插件缓存
        removed = []
        for key in list(sys.modules.keys()):
            if any(x in key for x in ['zanwo', 'send_tool', 'astrbot_plugin_zanwo', 'astrbot_plugin_send_tool']):
                sys.modules.pop(key, None)
                removed.append(key)
        logger.info(f"HelperPlugin2: Cleaned sys.modules: {removed}")
