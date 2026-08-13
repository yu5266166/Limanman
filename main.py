from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.message_components import Plain
from astrbot.core.platform.platform import MessageSesion
from astrbot.core.platform.message_type import MessageType
from astrbot.api.event import MessageChain

@register("send_tool", "Limanman", "支持通讯录和多机器人选择的代发插件", "1.4.1", "https://github.com/Limanman/astrbot_plugin_send_tool")
class SendMessageTool(Star):
    def __init__(self, context: Context, config: dict = None):
        super().__init__(context)
        self.config = config or {}

    @filter.llm_tool(name="send_private_message")
    async def send_private_message(
        self, 
        event: AstrMessageEvent, 
        target_user: str, 
        message_content: str, 
        platform_name: str = ""
    ):
        '''给指定名称或ID的用户发送私聊消息，支持指定发消息的平台/机器人。仅管理员可用。

        Args:
            target_user(string): 接收者的名称/别名（如“张三”、“群哥”）或直接账号ID（如“123456789”）
            message_content(string): 要发送的具体文本消息内容
            platform_name(string): 可选。指定用哪个后台平台/机器人发送（如：qq, telegram, aiocqhttp, lark）。不指定则自动匹配通讯录绑定的平台或当前对话平台。
        '''
        if not event.is_admin():
            return "权限拒绝：只有管理员才可调用机器人发送消息。"

        user_mappings = self.config.get("user_mappings", [])
        
        target_id = None
        mapped_platform = None
        display_name = target_user

        # 解析 list 格式配置 ["张三:123456789", "李四:987654321|telegram"]
        if isinstance(user_mappings, list):
            for item in user_mappings:
                item_str = str(item).strip().replace("：", ":")
                if ":" in item_str:
                    name, val_str = item_str.split(":", 1)
                    name = name.strip()
                    val_str = val_str.strip()
                    
                    if name.lower() == target_user.strip().lower():
                        if "|" in val_str:
                            target_id, mapped_platform = val_str.split("|", 1)
                            target_id = target_id.strip()
                            mapped_platform = mapped_platform.strip()
                        else:
                            target_id = val_str
                        display_name = f"{name} ({target_id})"
                        break

        # 若通讯录中没有匹配到别名，将输入值直接作为原始 ID
        if not target_id:
            target_id = target_user.strip()

        # 确定发送平台
        final_platform = None
        if platform_name and platform_name.strip():
            p_input = platform_name.strip().lower()
            if "qq" in p_input:
                final_platform = "aiocqhttp"
            elif "tg" in p_input or "telegram" in p_input:
                final_platform = "telegram"
            elif "feishu" in p_input or "lark" in p_input:
                final_platform = "lark"
            elif "wx" in p_input or "wechat" in p_input:
                final_platform = "wechat"
            else:
                final_platform = platform_name.strip()
        elif mapped_platform:
            final_platform = mapped_platform
        else:
            final_platform = event.get_platform_name()

        # 执行发送
        try:
            # 构造 MessageSesion 并调用 send_message
            session = MessageSesion(
                platform_name=final_platform,
                message_type=MessageType.FRIEND_MESSAGE,
                session_id=target_id
            )
            message_chain = MessageChain(chain=[Plain(message_content)])
            await self.context.send_message(
                session=session,
                message_chain=message_chain
            )
            return f"成功：已通过机器人平台 [{final_platform}] 向用户 [{display_name}] 发送消息：\"{message_content}\""
        except Exception as e:
            return f"发送失败 (平台: {final_platform}, 目标: {display_name})，错误原因：{str(e)}"
