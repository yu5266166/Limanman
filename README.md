# AstrBot Plugin Helper

这是一个专为 AstrBot 设计的辅助插件，旨在解决插件开发与调试过程中，因 Python `sys.modules` 模块缓存导致热重载（Reload）失效的问题。

## 功能特性

- **主动缓存清理**：提供 `helper_clean_cache` 声明工具（Tool），允许大语言模型或系统在需要时主动触发指定插件的缓存清理。
- **精准释放**：针对性地清理特定的插件模块缓存（如 `zanwo`, `send_tool` 等），避免影响系统其他核心组件的正常运行。

## 安装方法

将本插件目录放入 AstrBot 的 `addons/plugins/` 文件夹下，重启 AstrBot 即可自动加载。

## 使用说明

当您修改了相关插件的代码并希望立即生效时，可以通过触发 `helper_clean_cache` 工具来清除旧的模块缓存，随后进行重载即可。
