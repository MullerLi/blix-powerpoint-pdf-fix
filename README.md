# Blix 卜力士 PowerPoint / PDF 相容修正版

[English README](README.en.md)

本專案提供 **Blix（卜力士）** 的 PowerPoint 相容 TrueType 修正版。Blix 是由
IBM Plex Sans TC 改名衍生而來的字型。

本修正版解決字型在 PowerPoint 中顯示正常，但輸出 PDF 後繁體中文字元全部變成
方框的問題，並改善字型內嵌、PDF 子集化與 Windows 字型快取相容性。

## 下載

修復後的 8 個 Blix 字重位於 [`fonts/Blix`](fonts/Blix)：

- Blix Thin
- Blix ExtraLight
- Blix Light
- Blix Regular
- Blix Text
- Blix Medium
- Blix SemiBold
- Blix Bold

## 修復內容

- 補齊原本為空的 Windows BMP Unicode 對照表：
  - `cmap` platform `3`、encoding `1`、format `4`
  - `cmap` platform `0`、encoding `3`、format `4`
- 保留完整的 format 12 Unicode 對照，包括非 BMP 字元。
- 確認 `OS/2.fsType = 0`，允許字型安裝及內嵌。
- 將 `Blix-Text` 的非標準字重 metadata 由 `450` 正規化為 `400`。
- 更新字型版本與 Unique ID，降低 Windows 重複使用舊字型快取的機率。
- 重新計算 TrueType checksum 並驗證所有字型表格。

## 驗證結果

修復後的字型已通過：

- Windows `T2Embed.dll` 完整字型內嵌
- Windows `T2Embed.dll` 子集字型內嵌
- PowerPoint 字型內嵌
- PowerPoint 輸出 PDF
- PDF 內嵌字型檢查
- PDF 繁體中文文字抽取

可使用附帶工具再次驗證：

```powershell
python -m pip install fonttools
python tools/validate_fonts.py fonts/Blix
```

## 安裝方式

1. 從 Windows 設定或控制台移除舊版 Blix。
2. 重新啟動 Windows，以清除 Office 與 Windows 的舊字型快取。
3. 安裝 [`fonts/Blix`](fonts/Blix) 內的全部字型。
4. PowerPoint 儲存簡報時，啟用「將字型內嵌於檔案」。

## IBM Plex Sans TC

本專案的修復工具也能套用於 IBM Plex Sans TC。IBM Plex 的 `Plex` 是 SIL OFL
指定的 Reserved Font Name，因此本專案不散布保留原名稱的修改版本。

請從 [IBM 官方 Plex repository](https://github.com/IBM/plex) 下載 IBM Plex Sans TC。

## 授權協議

本專案使用的正式協議是 **SIL Open Font License 1.1（SIL OFL 1.1）**。
IBM Plex 與 Blix 沒有名為「SLC」的官方字型授權；若你所指的 SLC 是 SIL，
對應文件如下：

- [Blix SIL OFL 1.1 協議](LICENSES/Blix-SIL-OFL-1.1.txt)
- [Blix 衍生修改聲明](LICENSES/Blix-MODIFICATION-NOTICE.md)
- [IBM Plex Sans TC SIL OFL 1.1 協議](LICENSES/IBM-Plex-Sans-TC-SIL-OFL-1.1.txt)
- [IBM 官方原始協議](OFL.txt)

IBM 原始協議將 **Plex** 指定為 Reserved Font Name。本衍生版本使用重新命名後的
**Blix / 卜力士**，且未新增其他 Reserved Font Name。

