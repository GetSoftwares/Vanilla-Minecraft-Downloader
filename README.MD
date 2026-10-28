# ![Vanilla Minecraft Downloader LOGO](./_images/LOGO.png) **Vanilla Minecraft Downloader**

一个纯粹的原版 Minecraft Java 版下载器。

## **（必看）我为什么要写这个下载器？**

在 2026 年 10 月 21 日下午，MC 圈爆发了一件惊天动地的事件：传闻一娃子在某私服充钱，据传一个月 2700 元人民币，然后家长把服务器和启动器都举报了个遍，导致 PCL2 作者不得不关停中国大陆地区的原版 MC 下载功能。

这次事件影响非常广泛，国内很多知名主播都在用 PCL2 来作为自己的 Minecraft Java 版启动器，而且它默认是会自动更新的，一更新到 2.99.0 就会禁用下载功能，导致再也无法下载任意版本的 Minecraft 了。

我作为程序员，经常和 Python 打交道，我的项目里也大量用 Python 来写代码，因此对于这个项目而言使用 Python 完全不在话下。而且对于 Minecraft Java 版的[版本列表](https://zh.minecraft.wiki/w/Version_manifest.json)和[客户端清单](https://zh.minecraft.wiki/w/%E5%AE%A2%E6%88%B7%E7%AB%AF%E6%B8%85%E5%8D%95%E6%96%87%E4%BB%B6%E6%A0%BC%E5%BC%8F)的结构都是已经知道的，这使得我可以轻松地用 Python 去写一个原版 MC 的下载器来替代启动器的原版 MC 下载功能。

简单来说，Vanilla Minecraft Downloader（以下简称“VMD 下载器”）就是 PCL2 下载功能被禁的产物，用来接替 PCL2（和其他可能的启动器，如 HMCL）的原版 MC 下载功能。

**2026-10-25 更新**：PCL2 正式移除了中国大陆地区的相关下载功能，这更坚定了我要编写下载器的决心。详见：[2.99.0.1 更新已发布](https://www.bilibili.com/opus/1262817983873417220)

## **功能**

* 原版 MC 下载
* 多 Minecraft 文件夹管理
* 下载自动重试
* 可跳过愚人节版本
* 从其他启动器导入文件夹

## **支持的平台**

Windows 7+（Windows 7 使用 [PythonVista](https://github.com/adang1345/PythonVista) 来运行 Python）。

当前不支持 macOS 和 Linux 平台。

## **下载**

前往项目的 [release](https://github.com/GetSoftwares/Vanilla-Minecraft-Downloader/releases) 界面。根据页面提示选择下载 Win7 版本或 Win8+ 版本。

## **使用帮助**

解压下载的压缩包，然后查看 docs 下的文档。

你也可以看[这里](./docs/)的文档。

## **局限性**

* VMD 下载器当前只支持 Windows 平台，因此对于 Linux、macOS 和手机操作系统用户来说需要寻找其他替代方案。
* VMD 下载器仅仅只是 Minecraft 启动器中原版 MC 下载功能的替代，并无其他用处。因此，对于整合包玩家来说，需要寻找其他替代方案。
* 对于早于正式版 1.6.1 / 快照 13w16a 之前的版本可能不会很好的支持，因为他们并未使用新的客户端清单文件（虽然 Mojang 后来提供了这些文件）。

## **许可**

[MIT](./LICENSE)
