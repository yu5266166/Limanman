# AstrBot Plugin Helper 2

这是一个专为 AstrBot 设计的辅助插件，旨在解决插件开发与调试过程中，因 Python `sys.modules` 模块缓存导致热重载（Reload）失效的问题。

## 功能特性

- **自动缓存清理**：在插件初始化阶段自动执行。每当本插件被加载或重载时，它会自动识别并清除指定插件（如 `zanwo`, `send_tool` 等）的 Python 内存缓存。
- **无感运行**：无需大语言模型或用户手动调用工具，实现后台静默清理。

## 安装方法

将本插件目录放入 AstrBot 的 `addons/plugins/` 文件夹下，重启 AstrBot 即可自动加载。
