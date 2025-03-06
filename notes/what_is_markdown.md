# 什么是`.md`文件格式？

## 目录

- [什么是markdown？](#什么是`Markdown`?)
- [md的受众群体？](#md的受众群体？)
- [`Typora`是什么?](#`Typora`是什么?)
- [参考文献References](#参考文献References)









## 什么是`Markdown(md)`?

Markdown 是用来编写结构化文档的一种纯文本格式，它使我们在双手不离开键盘的情况下，可以对文本进行一定程度的格式排版。你可以在 [这篇文章](https://sspai.com/post/36610) 中快速入门 Markdown。











## md的受众群体？

程序员、、喜欢编写Markdown文档(下文简称MD)



















# *Typora*是什么?

Typora 是一款<u>支持实时预览的</u> **Markdown 文本编辑器**。

Typora 首先是一个 **Markdown 文本编辑器**，它支持且仅支持 **Markdown语法** 的文本编辑。



## *Markdown* 语法

由于目前还没有一个权威机构对 Markdown 的语法进行规范，各应用厂商制作时遵循的 Markdown 语法也是不尽相同的。其中比较受到认可的是 [GFM 标准](https://sspai.com/link?target=https%3A%2F%2Fgithub.github.com%2Fgfm%2F)，它是由著名代码托管网站 `GitHub` 所制定的。Typora 主要使用的也是 GFM 标准。

#### Typora 的扩展语法

Typora 支持一些非标准的 Markdown 扩展语法，例如 `==高亮==`、`~~删除线~~` 等，但这些语法在其他 Markdown 解析器中可能无法正确渲染。





#### GitHub 仅支持标准的 Markdown 语法

1. GitHub 仅支持标准的 Markdown 语法，例如加粗 (`**`)、斜体 (`*`)、代码块 (`代码`) 等。
2. GitHub 使用的是 CommonMark 标准的 Markdown，而 `==高亮==` 是 Typora 的扩展语法，不属于 CommonMark 标准。
3. 如果你希望文档在 GitHub 和 Typora 中都显示良好，建议使用标准的 Markdown 语法。



#### GitHub 的 README.md 如何实现目录

GitHub 的 Markdown 不支持 `[TOC]`，但你可以**手动编写目录**。例如：

```markdown
## 目录
- [简介](#简介)
- [安装](#安装)
- [使用](#使用)
- [贡献](#贡献)

## 简介
这里是简介内容。

## 安装
这里是安装说明。

## 使用
这里是使用方法。

## 贡献
这里是贡献指南。
```



## 学术文档 编辑器

除了基本的文本编辑体验极佳之外，Typora 还是一个非常优秀的学术文档编辑器。当然作为一个轻量级的、基于 Markdown 的编辑器，它不能与那些专业 LaTeX 编辑器相提并论，但它仍支持了许多可用于学术写作的功能。

### LaTeX

> LaTeX 是一种基于 TeX 的排版系统，由于它易于快速生成复杂表格和数学公式，非常适用于生成高印刷质量的科技和数学类文档。如果你常阅读数学、计算机等领域的学术论文，你一定对 LaTeX 不陌生。

Typora 原生支持 LaTeX 语法，你有两种方式输入 LaTeX 风格的数学公式：

1. **行内公式（inline）：**用 `$...$` 括起公式，公式会出现在行内。
2. **块间公式（display）：**用 `$$...$$` 括起公式（注意 `$$` 后需要换行），公式会默认显示在行中间。

具体的 LaTeX 语法在此不赘述了，你可以在 [这篇文章](https://sspai.com/link?target=https%3A%2F%2Fblog.csdn.net%2Fhappyday_d%2Farticle%2Fdetails%2F83715440) 中查看。















# 参考文献

1. [Typora 完全使用详解](https://sspai.com/post/54912/)——墙裂建议阅读原文
2. [Typora 完全使用详解](https://www.typora.net/1033.html)
3. [Markdown 完全入门（上）](https://sspai.com/post/36610)



























