➡️[回到原文](src_analysis.md)

# 文件名消毒

### **一、为什么需要专门的消毒库？**

1. **跨平台差异**：Windows/Linux/macOS 的文件系统限制不同（如 Windows 禁止 `*`，macOS 允许冒号）
2. **保留名称过滤**：需处理 `CON`、`AUX` 等系统保留名称（仅Windows）
3. **Unicode 处理**：正确处理多语言字符和emoji
4. **长度限制**：自动处理文件名截断（如 Windows 255 字符限制）



### **二、推荐开源库及对比**

#### **手动消毒 vs 库函数对比**

| 功能               | 手动实现 | pathvalidate | python-slugify |
| :----------------- | :------- | :----------- | :------------- |
| 跨平台非法字符处理 | ❌        | ✅            | ✅              |
| 保留名称过滤       | ❌        | ✅            | ❌              |
| 长度自动截断       | 需实现   | ✅            | ✅              |
| Unicode → ASCII    | ❌        | ❌            | ✅              |
| 中文支持           | ✅        | ✅            | ✅ (需扩展)     |

------

- **优先使用 `pathvalidate`**：如果你需要严格遵守文件系统规范
- **选择 `python-slugify`**：如果需要生成SEO友好的短名称
- **手动消毒的适用场景**：仅当项目不允许添加新依赖时









## 参考文献

1. [开源库：pathvalidate](https://github.com/thombashi/pathvalidate)
2. [库官方文档：pathvalidate’s documentation](https://pathvalidate.readthedocs.io/en/latest/index.html)
