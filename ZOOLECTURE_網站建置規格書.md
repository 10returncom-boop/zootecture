# ZooTecture 入梯毛孩 — 網站建置完整規格書

> 本文件可用於在新對話中重建相同或更加優化的功能網站。
> 建立日期：2026-08-27
> 網域名稱：zootecture.com（CNAME 已設定）

---

## 一、網站定位與品牌

| 項目 | 內容 |
|------|------|
| 網站名稱 | **ZooTecture 入梯毛孩** |
| 品牌主軸 | 入梯寵物專欄（ZooTecture）× PetLogic 毛行知識 |
| Meta Title | `ZooTecture 入梯毛孩｜入梯寵物專欄 × PetLogic 毛行知識` |
| Meta Description | ZooTecture 入梯毛孩｜入梯寵物專欄與PetLogic毛行知識平台，提供專業貓狗飼養知識、寵物行為矯正、居家寵物空間規劃與正向訓練教學，打造人寵共居的舒適共生環境。 |
| 主色調 | 深藍 `#2c3e50`（導覽列）、橘色 `#e67e22`（強調/連結hover）、淺灰 `#f7f9fa`（背景） |
| 語言 | 繁體中文（zh-TW） |

---

## 二、目錄結構與檔案清單

```
petblog/                          # 網站根目錄
├── index.html                    # 主站首頁（ZooTecture落地頁，無文章連結）
├── blog.html                     # 250篇文章總覽（卡片列表+分類篩選）
├── dog-diary.html                # 分類頁：狗狗日記（36篇）
├── cat-story.html                # 分類頁：貓咪物語（35篇）
├── pet-education.html            # 分類頁：寵物教育（35篇）
├── pet-health.html               # 分類頁：寵物健康（43篇）
├── home-design.html              # 分類頁：居家設計（6篇）
├── pet-daily.html                # 分類頁：萌寵日常（20篇，含異寵世界5篇）
├── pet-encyclopedia.html         # 分類頁：順寵圖鑑（各類伴侶寵物圖鑑）
├── breed-guide.html              # 分類頁：乖寵養成錄（品種與養成指南）
├── pet-art.html                  # 分類頁：寵物藝術（6篇）
├── positive-training.html        # 分類頁：正向訓練（寵物教育第二頁）
├── pet-space.html                # 分類頁：寵物空間規劃（50篇，最大分類）
├── outdoor-adventure.html        # 分類頁：戶外探險（7篇，含節日寵物7篇、成功案例）
├── CNAME                         # 網域設定：zootecture.com
├── add_article.py                # ⭐ 自動新增文章腳本（核心工具）
├── article_template.json         # 新增文章設定檔模板
├── articles_meta.json            # 250篇文章中繼資料（id/title/category/meta_desc/keywords/images/excerpt）
├── zootecture_petlogic_petswiki.mp4  # 首頁介紹影片（約20MB）
├── zootecture-main/              # 原始zootecture設計備份（含圖片）
│   ├── index.html
│   ├── col*.html (12個)
│   └── images/ (30張原始圖片)
├── posts/                        # 250篇完整文章
│   ├── post-001.html ~ post-250.html
│   └── （每篇約30-40KB，含完整SEO/AIO結構）
├── images/                       # 全部圖片（WebP格式）
│   ├── 284張 .webp（文章圖+分類封面+banner+logo）
│   └── 1張 favicon.png（保留PNG格式）
└── css/
    └── style.css                 # 部落格文章頁樣式
```

### 檔案大小統計

| 類別 | 數量 | 大小 |
|------|------|------|
| 根目錄HTML | 14個 | 約500KB |
| 文章頁HTML | 250篇 | 約8MB |
| 圖片 | 285張 | 28MB（284 WebP + 1 PNG） |
| 影片 | 1部 | 20MB |
| 腳本/資料 | 3個 | 約190KB |
| **總計** | **~553個檔案** | **~57MB** |

---

## 三、11大文章分類與對應分類頁

| 分類名稱 | 文章數 | 對應分類頁 | 說明 |
|----------|--------|------------|------|
| 寵物空間規劃 | 50篇 | pet-space.html | 居家空間設計、收納、寵物友善裝修（最大分類） |
| 寵物健康 | 43篇 | pet-health.html | 疾病預防、醫療護理、營養 |
| 狗狗日記 | 36篇 | dog-diary.html | 狗狗訓練、健康、品種介紹 |
| 寵物教育 | 35篇 | pet-education.html / positive-training.html | 訓練方法、行為矯正 |
| 貓咪物語 | 35篇 | cat-story.html | 貓咪護理、行為、品種 |
| 萌寵日常 | 20篇 | pet-daily.html | 可愛療癒日常故事 |
| 戶外探險 | 7篇 | outdoor-adventure.html | 帶寵物旅行、露營 |
| 節日寵物 | 7篇 | outdoor-adventure.html | 節日慶祝與安全須知 |
| 居家設計 | 6篇 | home-design.html | 寵物友善居家佈置 |
| 寵物藝術 | 6篇 | pet-art.html | 寵物肖像、攝影、創作 |
| 異寵世界 | 5篇 | pet-daily.html | 爬蟲、小型哺乳動物 |

**額外分類頁（zootecture原設計，非11大部落格分類）：**
| 頁面 | 說明 |
|------|------|
| pet-encyclopedia.html | 順寵圖鑑：各類伴侶寵物完整圖鑑 |
| breed-guide.html | 乖寵養成錄：品種介紹與養成指南 |

---

## 四、每篇文章的SEO/AIO完整結構

每篇 `post-XXX.html` 必須包含以下元素：

### 4.1 Head 區段
```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="150-160字元的搜尋摘要">
<meta name="keywords" content="關鍵字1, 關鍵字2, 關鍵字3（5-10個）">
<meta name="robots" content="index, follow, max-snippet:-1">
<link rel="canonical" href="https://zootecture.com/posts/post-XXX.html">
<meta property="og:title" content="文章標題 | ZooTecture 入梯毛孩">
<meta property="og:description" content="meta description">
<meta property="og:type" content="article">
<meta property="og:image" content="../images/封面圖.webp">
<title>文章標題 | ZooTecture 入梯毛孩</title>
<link rel="icon" type="image/png" href="../images/favicon.png">
<link rel="stylesheet" href="../css/style.css">
```

### 4.2 結構化資料（JSON-LD）
- **FAQPage schema**：4組Q&A，搶佔Google AIO摘要
- **Article schema**：文章標題、圖片、作者、發布日期、修改日期

### 4.3 頁面結構
```
<nav> 導覽列（首頁/文章總覽/分類頁連結）
<main>
  <article>
    ├── AIO快速回答框（綠色框，直接回答核心問題）
    ├── h1 文章標題
    ├── 文章資訊列（分類+日期）
    ├── 文章內文（h2/h3階層，關鍵名詞用<strong>粗體）
    ├── 圖片畫廊（每張圖含alt text + 圖說）
    ├── FAQ常見問題區（4組Q&A）
    ├── 重點整理區（條列重點）
    ├── 延伸閱讀（3-5篇相關文章內部連結）
    └── 文章導覽（上一篇/文章列表/下一篇）
  </article>
</main>
<footer> 頁尾（版權+導覽連結）
```

### 4.4 圖片規範
- 格式：**WebP**（quality=82, method=6）
- 最大寬度：1600px（超過自動縮放）
- 每張圖片必須有 `alt` 屬性（描述性文字）
- favicon 保留 PNG 格式

---

## 五、首頁（index.html）規格

### 5.1 導覽列
- Logo：`ZooTecture 動物空間 PetLogic 毛孩行為`
- 導覽按鈕：`📚 文章總覽`（→blog.html）、`🏗️ 入梯寵物專欄`（→#zootecture）、`🧠 PetLogic`（→#petlogic）、`📍 入梯城`

### 5.2 頁面區塊（由上到下）
1. **關於入梯ZooTecture** — 標題+自動播放影片（muted loop）+品牌說明
2. **12分類卡片網格** — 用CSS `background-image: url(./images/xx.webp)` 顯示分類封面，點擊進入對應col頁面
3. **🏗️ 入梯寵物專欄 ZooTecture** — 空間規劃主題介紹+4個快捷入口（空間規劃/拆家剋星/成功案例/全部文章）
4. **🧠 PetLogic 毛行知識** — 行為科普主題介紹+5個快捷入口（好好學/正向訓練/省錢/狗狗百科/貓咪圖鑑）

### 5.3 重要：首頁不放置文章連結
- 首頁是品牌落地頁，**不直接列出文章標題或文章卡片**
- 文章入口統一通過 `blog.html`（文章總覽）進入
- 分類頁（col*.html）可顯示該分類的精選文章卡片

---

## 六、文章總覽頁（blog.html）規格

- 250篇文章卡片網格（響應式：自動適應欄數）
- 分類篩選器：11個分類按鈕，點擊即時過濾卡片
- 每張卡片含：封面圖、分類標籤、標題、摘要
- 點擊卡片進入 `posts/post-XXX.html`
- 導覽列含「🏠 ZooTecture首頁」連結

---

## 七、分類頁規格（12個獨立分類頁）

每個分類頁結構：
1. 延續zootecture設計風格（深藍導覽+橘色強調）
2. 分類主題介紹（標題+說明+封面圖）
3. **精選文章區塊**：12篇該分類文章卡片（點擊進入文章頁）
4. 「查看全部250篇文章」按鈕（→blog.html）
5. 圖片使用CSS background-image（`./images/xx.webp`）

---

## 八、自動新增文章腳本（add_article.py）

### 8.1 位置
`petblog/add_article.py`

### 8.2 使用方式
```bash
# 方式A：指令列參數
python add_article.py --title "文章標題" --category "寵物空間規劃" --content-file article.txt --images img1.jpg img2.jpg

# 方式B：JSON設定檔（推薦）
python add_article.py --config article_template.json
```

### 8.3 支援的11個分類
`狗狗日記`、`貓咪物語`、`寵物教育`、`寵物健康`、`居家設計`、`萌寵日常`、`異寵世界`、`寵物空間規劃`、`戶外探險`、`節日寵物`、`寵物藝術`

### 8.4 腳本自動完成7件事
1. **產生文章頁**：`post-XXX.html`，含完整SEO/AIO結構（h1/h2/h3、meta、keywords、FAQ schema、AIO回答框、圖片畫廊、粗體名詞）
2. **自動找相關文章**：從同類別挑選3-5篇舊文章，自動加入「延伸閱讀」內部連結
3. **更新文章總覽**：`blog.html` 自動插入新文章卡片到最前面
4. **更新分類頁**：對應的 `col*.html` 自動加入新文章
5. **更新中繼資料**：`articles_meta.json` 自動新增紀錄
6. **更新Sitemap**：`sitemap.xml` 自動新增URL
7. **圖片自動轉WebP**：自動將新圖片轉換為WebP格式並複製到images/

### 8.5 article_template.json 格式
```json
{
  "title": "文章標題",
  "category": "寵物空間規劃",
  "content": "<h2>第一個小標題</h2><p>文章內容...</p>",
  "images": ["圖片1.jpg", "圖片2.jpg"],
  "meta_desc": "150-160字元的meta description",
  "keywords": ["關鍵字1", "關鍵字2", "寵物空間規劃"],
  "excerpt": "文章摘要（約80字，用於卡片顯示）",
  "faqs": [
    {"q": "問題1？", "a": "答案1"},
    {"q": "問題2？", "a": "答案2"},
    {"q": "問題3？", "a": "答案3"},
    {"q": "問題4？", "a": "答案4"}
  ],
  "aio_answer": "AIO快速回答框的內容"
}
```

---

## 九、圖片處理管線

### 9.1 格式規範
- **全部圖片使用WebP格式**（quality=82, method=6）
- favicon.png 保留PNG（瀏覽器需求）
- 最大寬度1600px（超過自動縮放，用Lanczos演算法）

### 9.2 圖片來源
- 文章圖片：從 `D:\_豆包圖庫SEO命名` 選取，使用後移動到 `used_clip/`
- 分類封面圖：zootecture原始設計的30張圖片（01-dog.webp ~ 12-case.webp, banner.webp, logo.webp等）

### 9.3 圖片引用方式（兩種）
- **文章頁**：`<img src="../images/檔名.webp" alt="描述文字">`
- **zootecture頁面（首頁+分類頁）**：CSS `background-image: url(./images/檔名.webp)` 或 inline `style="background-image: url(./images/檔名.webp)"`

### 9.4 常見坑（重要！）
- 偵測「未使用圖片」時，必須同時掃描 `<img src>`、CSS `url()`、inline style `url()`、`<video poster>` 四種格式
- zootecture設計主要用CSS background-image，只掃`<img src>`會誤刪
- 圖片路徑可能有 `./images/`、`../images/`、`images/` 三種前綴

---

## 十、GitHub Pages 部署規範

### 10.1 部署策略
- **單一Repo完整上架**（方案A，SEO最優）
- 全部250篇文章+14個根目錄頁面+圖片+影片一次部署
- 不使用分段覆蓋部署（會產生404，損害SEO權重）

### 10.2 頻寬注意
- GitHub Pages建議單月頻寬不超過100GB
- 圖片已壓縮為WebP（28MB），頻寬壓力小
- 影片20MB建議移至外部CDN（如YouTube嵌入），避免消耗GitHub頻寬
- 大型附件/PDF一律移至外部CDN

### 10.3 自訂網域
- CNAME檔案內容：`zootecture.com`
- DNS設定：A記錄指向GitHub Pages IP，CNAME指向 username.github.io

### 10.4 新增文章後的部署
- 執行 `add_article.py` 產生新檔案
- `git add . && git commit -m "新增文章：標題" && git push`
- 到Google Search Console提交新URL，加速收錄

---

## 十一、SEO優化清單（全站適用）

| 優化項 | 實作方式 |
|--------|----------|
| 標題階層 | 每篇h1×1、h2×3-5、h3×5-15 |
| Meta Description | 每篇150-160字元，含主要關鍵字 |
| Keywords | 每篇5-10個相關關鍵字 |
| 圖片Alt | 每張圖片皆有描述性alt文字 |
| FAQ Schema | 每篇4組Q&A的JSON-LD，搶佔AIO摘要 |
| Article Schema | 文章結構化資料（標題/圖片/作者/日期） |
| 內部連結 | 每篇3-5篇延伸閱讀，傳遞權重 |
| 粗體名詞 | 關鍵名詞與術語用`<strong>`標註 |
| AIO回答框 | 每篇開頭綠色框直接回答核心問題 |
| Canonical | 每篇設定規範網址 |
| Open Graph | 社群分享標籤（title/description/image/type） |
| Sitemap | sitemap.xml自動更新，提交至Search Console |
| robots meta | `index, follow, max-snippet:-1`最大化摘要 |
| 響應式設計 | 手機/平板/桌面皆適用 |
| 圖片最佳化 | WebP格式+延遲載入（loading="lazy"） |

---

## 十二、未來優化建議

### 12.1 功能優化
- [ ] 加入站內搜尋功能（用JavaScript索引250篇文章標題+摘要）
- [ ] 加入相關文章推薦演算法（根據關鍵字相似度）
- [ ] 加入文章閱讀進度條
- [ ] 加入深色模式切換
- [ ] 加入多語言支援（繁中/簡中/英文）

### 12.2 SEO優化
- [ ] 建立HTML sitemap頁面（視覺化網站地圖）
- [ ] 加入Breadcrumb麵包屑導覽
- [ ] 優化Core Web Vitals（LCP/CLS/INP）
- [ ] 加入結構化麵包屑Schema
- [ ] 建立分類頁的專屬meta description

### 12.3 內容優化
- [ ] 每週新增1-2篇文章（保持更新頻率，提高爬蟲造訪）
- [ ] 在熱門舊文章的延伸閱讀加入新文章連結（加速新文章收錄）
- [ ] 建立「系列文章」連結（如「寵物空間規劃10講」）
- [ ] 加入作者資訊與作者頁面（E-E-A-T優化）

### 12.4 技術優化
- [ ] 影片移至YouTube嵌入（節省GitHub頻寬）
- [ ] 圖片移至Cloudflare CDN（進一步降低頻寬+加速）
- [ ] 加入Service Worker離線快取
- [ ] 自動化部署（GitHub Actions自動build+deploy）

---

## 十三、快速重建指令（給新對話的AI）

如果要在新對話中重建此網站，請按以下順序執行：

1. **建立目錄結構**：`posts/`、`images/`、`css/`
2. **準備圖片**：將文章圖片放入`images/`，全部轉換為WebP（quality=82）
3. **撰寫文章產生器**：用Python產生250篇`post-XXX.html`，每篇含第四節的完整SEO/AIO結構
4. **建立首頁**：`index.html`，依第五節規格（zootecture風格，無文章連結，含影片+12分類卡片+2個專欄區塊）
5. **建立文章總覽**：`blog.html`，250篇卡片+11分類篩選器
6. **建立12個分類頁**：`dog-diary.html`、`cat-story.html`、`pet-education.html`、`pet-health.html`、`home-design.html`、`pet-daily.html`、`pet-encyclopedia.html`、`breed-guide.html`、`pet-art.html`、`positive-training.html`、`pet-space.html`、`outdoor-adventure.html`，每頁含12篇精選文章
7. **撰寫add_article.py**：依第八節規格，自動化新增文章
8. **建立CNAME**：內容為`zootecture.com`
9. **建立sitemap.xml**：列出全部URL
10. **驗證**：檢查所有圖片引用存在、所有內部連結有效、SEO元素完整

---

*文件版本：v1.0 | 最後更新：2026-08-27*
