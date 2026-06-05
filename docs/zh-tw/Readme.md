SPDX-License-Identifier: MIT
Copyright (c) 2026-${year} WEMI Contributors

This software is released under the MIT License.
https://opensource.org/licenses/MIT

<!-- SPDX-License-Identifier: MIT -->
<!-- Copyright (c) 2026 TaiXeflar -->

# WEMI 環境模組安裝器

歡迎來到 環境模組安裝器 的中文文檔說明!

環境模組安裝器是一個基於Python語言、命令列的輕量級環境模組(Environment Modules)安裝程式。

## 預先準備
 - [git][]分散式版本控制
 - 一個Python3虛擬環境(建議使用[Astral uv][], Python版本號`3.11`~`3.14`)
 - 電腦上必須要有[Everything][]服務
 - 電腦上必須要有[Everything-CLI][]程式
 - 電腦上必須要先行安裝[環境模組][]

## 使用方法

1. 使用git複製這個repo，並在repo內建立Python虛擬環境並啟動它。
   ```
    PS X:\ROG> git clone https://github.com/TaiXeflar/wemi.git --depth=1
    PS X:\ROG> cd wemi
    PS X:\ROG\wemi> uv venv .venv --python 3.14.2
   ```

2. 呼叫Python執行wemi.py，針對你/妳的電腦組態進行掃描，生成一個可用於生成、安裝的json快取組態檔案`cache.json`。
   ```
   # 確認組態
   (.venv) PS X:\ROG\wemi> python ./wemi configure

   # 建置 (必須要有cache.json)
   (.venv) PS X:\ROG\wemi> python ./wemi build

   # 安裝 (必須要有cache.json)
   (.venv) PS X:\ROG\wemi> python ./wemi install --prefix='X:\ROG\server\tools\module'
   ```

- 命令列允許使用flags。部分flags支援Unix/DOS/CMake風格(`--flags/-flags`, `/flags`,`-DFlags...`)。
   ```
   (.venv) PS X:\ROG\wemi> python ./wemi  --help, -help, /help, -?, /
   ```

## 注意事項
環境模組安裝器會調用Everything服務以及調用`winreg`模組，查詢電腦的登錄編輯資料資料庫(Registry)。

## 關於簡體中文文檔說明
很抱歉，目前環境模組安裝器專案在建立初期為一人計劃並由作者親自維護，短期/中期內個人排定可見的更新/維護歷程中無法提供簡體中文說明檔案。

相關的想法及建議可以在GitHub中提供給我! (請注意盡量不要在相同的請求下重複開啟Issue/Discuss/PR)

<!-- links -->

[Astral UV]:                            https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_2

[Everything]:                           https://www.voidtools.com/downloads/

[Everything-CLI]:                       https://github.com/voidtools/ES

[gsudo]:                                https://github.com/gerardog/gsudo

[環境模組]:                  https://github.com/envmodules/modules
