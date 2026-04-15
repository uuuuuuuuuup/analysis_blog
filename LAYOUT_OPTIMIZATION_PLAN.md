# Hugo 博客布局优化 - 完整实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 通过重新设计首页、报告列表、导航和筛选系统，提升用户体验和信息架构，将线性列表布局转变为现代卡片网格系统。

**Architecture:** 
- 保持PaperMod主题兼容性，通过自定义layouts和CSS扩展实现
- 分阶段优化：第一阶段（首页+列表）、第二阶段（细节优化）、第三阶段（高级功能）
- 使用CSS Grid/Flexbox实现响应式卡片网格（1列移动端、2列平板、3列桌面）
- 添加投资等级颜色系统和数据可视化增强

**Tech Stack:** 
- Hugo + PaperMod 主题
- CSS3 (Grid/Flexbox/Variables)
- JavaScript (交互增强、筛选/排序逻辑)
- Markdown frontmatter（扩展元数据）

---

## 文件结构规划

### 新增文件
```
├── assets/
│   └── css/
│       ├── custom-cards.css              # 卡片网格系统
│       ├── investment-ratings.css        # 投资等级颜色和标签
│       ├── responsive-layout.css         # 响应式布局增强
│       └── enhanced-navigation.css       # 导航栏增强
├── assets/js/
│   ├── filters-sorting.js                # 筛选和排序功能
│   ├── card-interactions.js              # 卡片交互效果
│   └── sticky-nav.js                     # 粘性导航栏
├── layouts/
│   ├── reports/
│   │   ├── list.html                     # 报告列表页面（卡片布局）
│   │   ├── single.html                   # 单篇报告优化版本
│   │   └── _markup/
│   │       └── render-heading.html       # 标题渲染增强（侧边栏导航）
│   ├── _default/
│   │   ├── home.html                     # 首页新设计
│   │   └── list.html                     # 列表页优化
│   └── partials/
│       ├── report-card.html              # 报告卡片组件
│       ├── rating-badge.html             # 等级徽章组件
│       ├── filters-panel.html            # 筛选面板
│       ├── sticky-header.html            # 粘性导航增强
│       ├── stats-panel.html              # 统计面板（首页）
│       └── toc-sidebar.html              # 目录侧边栏（单篇报告）
└── data/
    └── report-metadata.json              # 报告元数据（板块、收益率等）
```

### 修改文件
```
├── hugo.toml                             # 配置扩展（参数、菜单）
├── content/
│   ├── reports/_index.md                 # 添加frontmatter元数据
│   └── reports/*/front_matter.md         # 每份报告添加元数据
└── themes/PaperMod/
    └── 无需修改（通过layouts覆盖实现）
```

---

## 三阶段优化计划

### 阶段 1：核心布局重构（首页 + 列表页 + 导航）
优先级最高，涵盖主要视觉改进和用户流程优化

### 阶段 2：交互增强（筛选/排序 + 侧边栏导航 + 卡片动效）
提升用户操作体验和内容发现效率

### 阶段 3：高级功能（数据可视化 + 性能优化 + 移动端适配）
完善细节，提升专业度和加载性能

---

## 详细任务分解

### 第一阶段：首页优化

#### Task 1: 创建首页新设计（Home Layout）

**Files:**
- Create: `layouts/_default/home.html`
- Create: `assets/css/custom-cards.css`
- Modify: `hugo.toml` (添加首页配置参数)

**目标：** 将首页从简单的profile模式升级为包含统计面板、分类卡片网格、最近报告的现代化首页

- [ ] **Step 1: 创建首页自定义layout文件**

创建文件 `layouts/_default/home.html`，这将覆盖PaperMod默认的首页layout：

```html
{{- define "main" }}
<section class="home-hero">
  <div class="hero-content">
    <h1>{{ .Site.Title }}</h1>
    <p class="hero-subtitle">{{ .Site.Params.description }}</p>
    <div class="hero-buttons">
      <a href="/reports/" class="btn btn-primary">📈 浏览所有报告</a>
      <a href="/summary/" class="btn btn-secondary">📊 查看汇总</a>
    </div>
  </div>
</section>

<!-- 统计面板 -->
<section class="stats-panel">
  <div class="stats-container">
    <div class="stat-card">
      <div class="stat-number">40</div>
      <div class="stat-label">优质股票</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">5</div>
      <div class="stat-label">分析因子</div>
    </div>
    <div class="stat-card">
      <div class="stat-number">2026</div>
      <div class="stat-label">更新年份</div>
    </div>
  </div>
</section>

<!-- 优先级分类 -->
<section class="priority-categories">
  <h2>📋 投资建议分类</h2>
  <div class="category-grid">
    <div class="category-card high-priority">
      <div class="priority-icon">✅</div>
      <h3>高优先级</h3>
      <p class="priority-count">15只</p>
      <p class="priority-desc">当前价低于目标价<br>具备安全边际</p>
      <a href="/reports/?rating=good" class="category-link">查看详情 →</a>
    </div>
    
    <div class="category-card medium-priority">
      <div class="priority-icon">⚠️</div>
      <h3>中优先级</h3>
      <p class="priority-count">18只</p>
      <p class="priority-desc">接近目标价<br>需要持续观察</p>
      <a href="/reports/?rating=warning" class="category-link">查看详情 →</a>
    </div>
    
    <div class="category-card low-priority">
      <div class="priority-icon">❌</div>
      <h3>低优先级</h3>
      <p class="priority-count">7只</p>
      <p class="priority-desc">观望或谨慎<br>暂不建议建仓</p>
      <a href="/reports/?rating=exclude" class="category-link">查看详情 →</a>
    </div>
  </div>
</section>

<!-- 最近更新 -->
<section class="recent-reports">
  <h2>🆕 最近更新</h2>
  <div class="reports-grid">
    {{- $recentPages := first 6 (sort .Site.RegularPages "Date" "desc") }}
    {{- range $recentPages }}
      {{- partial "report-card.html" . }}
    {{- end }}
  </div>
</section>

<!-- 底部导航 -->
<section class="home-footer-nav">
  <div class="nav-item">
    <h3>📚 学习资源</h3>
    <p>了解龟龟投资策略框架和分析方法</p>
    <a href="/about/">详细了解 →</a>
  </div>
</section>
{{- end }}
```

- [ ] **Step 2: 创建卡片和布局样式**

创建文件 `assets/css/custom-cards.css`：

```css
/* ===== 首页英雄部分 ===== */
.home-hero {
  background: linear-gradient(135deg, var(--theme) 0%, var(--primary) 100%);
  color: white;
  padding: 60px 20px;
  text-align: center;
  margin-bottom: 40px;
  border-radius: 8px;
}

.hero-content h1 {
  font-size: clamp(28px, 5vw, 48px);
  margin-bottom: 16px;
  font-weight: 700;
}

.hero-subtitle {
  font-size: clamp(16px, 2.5vw, 20px);
  margin-bottom: 32px;
  opacity: 0.95;
  line-height: 1.5;
}

.hero-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  padding: 12px 24px;
  border-radius: 6px;
  font-size: 16px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  cursor: pointer;
  border: none;
  display: inline-block;
}

.btn-primary {
  background: white;
  color: var(--theme);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid white;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

/* ===== 统计面板 ===== */
.stats-panel {
  margin: 60px 0;
}

.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  background: var(--entry);
  border: 1px solid var(--border);
  padding: 24px;
  border-radius: 8px;
  text-align: center;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  border-color: var(--theme);
}

.stat-number {
  font-size: 36px;
  font-weight: 700;
  color: var(--theme);
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: var(--secondary);
  font-weight: 500;
}

/* ===== 优先级分类 ===== */
.priority-categories {
  margin: 60px 0;
}

.priority-categories h2 {
  font-size: 28px;
  margin-bottom: 32px;
  text-align: center;
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.category-card {
  padding: 32px;
  border-radius: 12px;
  text-align: center;
  transition: all 0.3s ease;
  border: 2px solid;
  cursor: pointer;
}

.category-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

.high-priority {
  background: rgba(34, 197, 94, 0.05);
  border-color: rgba(34, 197, 94, 0.3);
}

.high-priority:hover {
  border-color: #22c55e;
  background: rgba(34, 197, 94, 0.1);
}

.medium-priority {
  background: rgba(245, 158, 11, 0.05);
  border-color: rgba(245, 158, 11, 0.3);
}

.medium-priority:hover {
  border-color: #f59e0b;
  background: rgba(245, 158, 11, 0.1);
}

.low-priority {
  background: rgba(239, 68, 68, 0.05);
  border-color: rgba(239, 68, 68, 0.3);
}

.low-priority:hover {
  border-color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
}

.priority-icon {
  font-size: 40px;
  margin-bottom: 16px;
}

.category-card h3 {
  font-size: 20px;
  margin-bottom: 12px;
  font-weight: 600;
}

.priority-count {
  font-size: 28px;
  font-weight: 700;
  color: var(--theme);
  margin-bottom: 8px;
}

.priority-desc {
  font-size: 14px;
  color: var(--secondary);
  line-height: 1.6;
  margin-bottom: 16px;
}

.category-link {
  display: inline-block;
  color: var(--theme);
  text-decoration: none;
  font-weight: 600;
  transition: all 0.2s ease;
}

.category-link:hover {
  transform: translateX(4px);
}

/* ===== 报告网格 ===== */
.reports-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  margin: 32px 0;
}

@media (max-width: 768px) {
  .reports-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 16px;
  }
}

@media (max-width: 480px) {
  .reports-grid {
    grid-template-columns: 1fr;
  }
}

/* ===== 首页底部导航 ===== */
.home-footer-nav {
  margin: 60px 0;
  padding: 40px;
  background: var(--entry);
  border-radius: 12px;
  border-left: 4px solid var(--theme);
}

.nav-item h3 {
  font-size: 20px;
  margin-bottom: 12px;
}

.nav-item p {
  color: var(--secondary);
  margin-bottom: 16px;
}

.nav-item a {
  color: var(--theme);
  text-decoration: none;
  font-weight: 600;
  transition: all 0.2s ease;
}

.nav-item a:hover {
  transform: translateX(4px);
}

/* ===== 响应式调整 ===== */
@media (max-width: 768px) {
  .home-hero {
    padding: 40px 16px;
  }

  .hero-buttons {
    flex-direction: column;
  }

  .btn {
    width: 100%;
  }

  .category-grid {
    grid-template-columns: 1fr;
  }

  .stats-container {
    grid-template-columns: repeat(3, 1fr);
  }

  @media (max-width: 480px) {
    .stats-container {
      grid-template-columns: 1fr;
    }

    .hero-subtitle {
      font-size: 14px;
    }
  }
}
```

- [ ] **Step 3: 更新Hugo配置，启用首页**

编辑 `hugo.toml`，在 `[params]` 部分禁用profile模式或添加首页特定配置：

```toml
# 更新 profileMode，使其在首页显示英雄内容后使用网格布局
[params]
  # ... 其他配置 ...
  
  # 禁用默认的profile模式，使用自定义首页
  [params.profileMode]
    enabled = false
  
  # 首页自定义参数
  [params.homeParams]
    showStatsPanel = true
    showPrioritiesGrid = true
    showRecentReports = true
    recentReportsCount = 6
```

- [ ] **Step 4: 验证首页渲染**

在浏览器中访问首页，验证：
- ✓ 英雄部分显示正确
- ✓ 统计面板的三个卡片正确布局
- ✓ 优先级分类卡片显示正确颜色
- ✓ 最近更新的报告网格显示
- ✓ 响应式布局在移动端正确显示

- [ ] **Step 5: 提交第一部分**

```bash
git add layouts/_default/home.html assets/css/custom-cards.css hugo.toml
git commit -m "feat: 完全重设计首页，添加英雄部分、统计面板和优先级分类卡片网格"
```

---

#### Task 2: 创建报告卡片组件

**Files:**
- Create: `layouts/partials/report-card.html`
- Create: `layouts/partials/rating-badge.html`
- Create: `assets/css/investment-ratings.css`

**目标：** 设计可复用的报告卡片组件，包含等级徽章、关键指标、悬停效果

- [ ] **Step 1: 创建评级徽章组件**

创建文件 `layouts/partials/rating-badge.html`：

```html
{{- $rating := .Params.rating | default "exclude" }}
{{- $ratingMap := dict "good" "✅ 推荐" "warning" "⚠️ 观望" "exclude" "❌ 回避" }}
{{- $ratingClass := dict "good" "rating-good" "warning" "rating-warning" "exclude" "rating-exclude" }}

<span class="rating-badge {{ index $ratingClass $rating }}" data-rating="{{ $rating }}">
  {{ index $ratingMap $rating }}
</span>
```

- [ ] **Step 2: 创建报告卡片组件**

创建文件 `layouts/partials/report-card.html`：

```html
{{- $code := .Params.code | default (path.BaseName .Dir) }}
{{- $name := .Params.name | .Title }}
{{- $rating := .Params.rating | default "exclude" }}
{{- $summary := .Summary | default .Description }}

<article class="report-card" data-code="{{ $code }}" data-rating="{{ $rating }}">
  <div class="card-header">
    <div class="card-title-section">
      <h3 class="card-title">
        <a href="{{ .Permalink }}">{{ $name }}</a>
      </h3>
      <p class="card-code">{{ $code }}</p>
    </div>
    {{- partial "rating-badge.html" . }}
  </div>

  {{- if .Params.sector }}
  <div class="card-sector">
    <span class="sector-tag">{{ .Params.sector }}</span>
  </div>
  {{- end }}

  <div class="card-summary">
    {{ $summary | plainify | truncate 120 }}
  </div>

  {{- if .Params.targetPrice }}
  <div class="card-metrics">
    <div class="metric">
      <span class="metric-label">目标价</span>
      <span class="metric-value">¥{{ .Params.targetPrice }}</span>
    </div>
    {{- if .Params.expectedReturn }}
    <div class="metric">
      <span class="metric-label">预期收益</span>
      <span class="metric-value {{ if gt (.Params.expectedReturn | float) 0 }}positive{{ else }}negative{{ end }}">
        {{ .Params.expectedReturn }}%
      </span>
    </div>
    {{- end }}
  </div>
  {{- end }}

  <div class="card-footer">
    <span class="card-date">{{ .Date.Format "2006-01-02" }}</span>
    <a href="{{ .Permalink }}" class="card-link">查看报告 →</a>
  </div>
</article>
```

- [ ] **Step 3: 创建投资等级样式**

创建文件 `assets/css/investment-ratings.css`：

```css
/* ===== 评级徽章 ===== */
.rating-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}

.rating-good {
  background: rgba(34, 197, 94, 0.15);
  color: #16a34a;
  border: 1px solid rgba(34, 197, 94, 0.3);
}

.rating-warning {
  background: rgba(245, 158, 11, 0.15);
  color: #d97706;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.rating-exclude {
  background: rgba(239, 68, 68, 0.15);
  color: #dc2626;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

/* ===== 报告卡片 ===== */
.report-card {
  display: flex;
  flex-direction: column;
  background: var(--entry);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 20px;
  transition: all 0.3s ease;
  height: 100%;
}

.report-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  border-color: var(--theme);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 12px;
}

.card-title-section {
  flex: 1;
  min-width: 0;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 4px 0;
  line-height: 1.4;
}

.card-title a {
  color: var(--entry-text);
  text-decoration: none;
  transition: color 0.2s ease;
}

.card-title a:hover {
  color: var(--theme);
}

.card-code {
  font-size: 12px;
  color: var(--secondary);
  margin: 0;
  font-weight: 500;
  font-family: monospace;
}

.card-sector {
  margin-bottom: 12px;
}

.sector-tag {
  display: inline-block;
  background: var(--primary);
  color: var(--theme);
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.card-summary {
  font-size: 14px;
  color: var(--secondary);
  line-height: 1.6;
  margin-bottom: 12px;
  flex-grow: 1;
}

/* ===== 卡片指标 ===== */
.card-metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 12px;
  margin-bottom: 12px;
  padding: 12px;
  background: var(--primary);
  border-radius: 6px;
}

.metric {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.metric-label {
  font-size: 12px;
  color: var(--secondary);
  margin-bottom: 4px;
}

.metric-value {
  font-size: 16px;
  font-weight: 600;
  color: var(--entry-text);
}

.metric-value.positive {
  color: #22c55e;
}

.metric-value.negative {
  color: #ef4444;
}

/* ===== 卡片页脚 ===== */
.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid var(--border);
  font-size: 12px;
}

.card-date {
  color: var(--secondary);
}

.card-link {
  color: var(--theme);
  text-decoration: none;
  font-weight: 600;
  transition: all 0.2s ease;
}

.card-link:hover {
  transform: translateX(2px);
}

/* ===== 卡片网格 ===== */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

@media (max-width: 768px) {
  .cards-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 16px;
  }
}

@media (max-width: 480px) {
  .cards-grid {
    grid-template-columns: 1fr;
  }

  .report-card {
    padding: 16px;
  }

  .card-metrics {
    grid-template-columns: 1fr 1fr;
  }

  .card-header {
    flex-direction: column;
  }

  .card-footer {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
```

- [ ] **Step 4: 测试卡片组件**

在首页或任何列表页面验证卡片显示：
- ✓ 卡片标题和代码显示正确
- ✓ 评级徽章显示对应颜色
- ✓ 悬停时卡片向上移动，阴影增强
- ✓ 在不同屏幕尺寸下网格布局正确

- [ ] **Step 5: 提交第二部分**

```bash
git add layouts/partials/report-card.html layouts/partials/rating-badge.html assets/css/investment-ratings.css
git commit -m "feat: 创建投资评级系统和可复用的报告卡片组件"
```

---

#### Task 3: 优化报告列表页面（卡片网格布局）

**Files:**
- Create: `layouts/reports/list.html`
- Create: `assets/css/responsive-layout.css`
- Modify: `content/reports/_index.md` (添加frontmatter元数据)

**目标：** 将报告列表从线性改为卡片网格布局，添加筛选/排序UI框架

- [ ] **Step 1: 创建报告列表页面**

创建文件 `layouts/reports/list.html`：

```html
{{- define "main" }}

<header class="page-header">
  <h1>{{ .Title }}</h1>
  {{- if .Description }}
  <p class="page-description">{{ .Description }}</p>
  {{- end }}
</header>

<!-- 筛选和排序工具栏 -->
<div class="list-controls">
  <div class="controls-inner">
    <div class="search-box">
      <input type="text" id="searchInput" placeholder="搜索股票代码或名称..." class="search-input">
      <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="11" cy="11" r="8"></circle>
        <path d="m21 21-4.35-4.35"></path>
      </svg>
    </div>

    <div class="filter-sort-controls">
      <div class="control-group">
        <label for="ratingFilter">投资等级：</label>
        <select id="ratingFilter" class="filter-select">
          <option value="">全部</option>
          <option value="good">✅ 推荐</option>
          <option value="warning">⚠️ 观望</option>
          <option value="exclude">❌ 回避</option>
        </select>
      </div>

      <div class="control-group">
        <label for="sectorFilter">板块：</label>
        <select id="sectorFilter" class="filter-select">
          <option value="">全部板块</option>
          <option value="consumer">消费</option>
          <option value="tech">科技</option>
          <option value="pharma">医药</option>
          <option value="finance">金融</option>
          <option value="infrastructure">基础设施</option>
        </select>
      </div>

      <div class="control-group">
        <label for="sortBy">排序：</label>
        <select id="sortBy" class="filter-select">
          <option value="date-desc">最新更新</option>
          <option value="date-asc">最早更新</option>
          <option value="name">按名称</option>
          <option value="code">按代码</option>
        </select>
      </div>
    </div>
  </div>
</div>

<!-- 结果统计 -->
<div class="results-info">
  <span id="resultCount" class="result-count">显示 {{ len .Pages }} 份报告</span>
  <button id="resetFilters" class="btn-reset" style="display:none;">重置筛选</button>
</div>

<!-- 报告卡片网格 -->
<div class="cards-grid" id="reportsGrid">
  {{- range .Pages }}
    {{- partial "report-card.html" . }}
  {{- end }}
</div>

<!-- 空状态 -->
<div id="emptyState" class="empty-state" style="display:none;">
  <div class="empty-icon">📭</div>
  <h3>未找到匹配的报告</h3>
  <p>尝试调整筛选条件或搜索词</p>
  <button id="clearAllFilters" class="btn btn-primary">清除所有筛选</button>
</div>

<!-- 分页 -->
{{- if gt .Paginator.TotalPages 1 }}
<nav class="pagination" style="margin-top: 40px;">
  {{- if .Paginator.HasPrev }}
  <a href="{{ .Paginator.Prev.URL }}" class="pagination-link prev">← 上一页</a>
  {{- end }}

  <div class="pagination-info">
    第 {{ .Paginator.PageNumber }} / {{ .Paginator.TotalPages }} 页
  </div>

  {{- if .Paginator.HasNext }}
  <a href="{{ .Paginator.Next.URL }}" class="pagination-link next">下一页 →</a>
  {{- end }}
</nav>
{{- end }}

<script>
// 占位符：筛选和排序逻辑将在 Task 4 中实现
console.log('报告列表页面已加载');
</script>

{{- end }}
```

- [ ] **Step 2: 创建响应式布局样式**

创建文件 `assets/css/responsive-layout.css`：

```css
/* ===== 页面头部 ===== */
.page-header {
  margin-bottom: 32px;
}

.page-header h1 {
  font-size: 32px;
  margin-bottom: 8px;
}

.page-description {
  font-size: 16px;
  color: var(--secondary);
  margin: 0;
}

/* ===== 列表控制栏 ===== */
.list-controls {
  background: var(--entry);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 24px;
  sticky: top;
  top: var(--header-height);
  z-index: 50;
}

.controls-inner {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* ===== 搜索框 ===== */
.search-box {
  position: relative;
  display: flex;
  align-items: center;
}

.search-input {
  width: 100%;
  padding: 10px 16px 10px 40px;
  border: 1px solid var(--border);
  border-radius: 6px;
  font-size: 14px;
  background: var(--primary);
  color: var(--entry-text);
  transition: all 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: var(--theme);
  box-shadow: 0 0 0 3px rgba(var(--theme-rgb), 0.1);
}

.search-icon {
  position: absolute;
  left: 12px;
  color: var(--secondary);
  pointer-events: none;
}

/* ===== 筛选和排序 ===== */
.filter-sort-controls {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}

.control-group {
  display: flex;
  flex-direction: column;
}

.control-group label {
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 6px;
  color: var(--secondary);
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid var(--border);
  border-radius: 6px;
  background: var(--primary);
  color: var(--entry-text);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.filter-select:hover,
.filter-select:focus {
  border-color: var(--theme);
  outline: none;
}

/* ===== 结果信息 ===== */
.results-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 12px 0;
  border-bottom: 1px solid var(--border);
}

.result-count {
  font-size: 14px;
  color: var(--secondary);
  font-weight: 500;
}

.btn-reset {
  padding: 6px 12px;
  border: none;
  background: var(--primary);
  color: var(--theme);
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-reset:hover {
  background: var(--entry);
  border: 1px solid var(--theme);
}

/* ===== 空状态 ===== */
.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty-state h3 {
  font-size: 20px;
  margin-bottom: 8px;
}

.empty-state p {
  color: var(--secondary);
  margin-bottom: 24px;
}

/* ===== 分页 ===== */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
  margin: 40px 0;
  flex-wrap: wrap;
}

.pagination-link {
  padding: 10px 16px;
  background: var(--entry);
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--theme);
  text-decoration: none;
  font-weight: 600;
  transition: all 0.2s ease;
}

.pagination-link:hover {
  background: var(--theme);
  color: white;
  transform: translateY(-2px);
}

.pagination-info {
  font-size: 14px;
  color: var(--secondary);
  font-weight: 500;
}

/* ===== 响应式调整 ===== */
@media (max-width: 768px) {
  .list-controls {
    padding: 16px;
  }

  .filter-sort-controls {
    grid-template-columns: repeat(2, 1fr);
  }

  .control-group label {
    font-size: 11px;
  }

  .filter-select {
    font-size: 13px;
    padding: 7px 10px;
  }
}

@media (max-width: 480px) {
  .filter-sort-controls {
    grid-template-columns: 1fr;
  }

  .results-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .page-header h1 {
    font-size: 24px;
  }
}
```

- [ ] **Step 3: 更新报告列表前缀**

编辑 `content/reports/_index.md`，添加frontmatter元数据示例：

```markdown
---
title: "个股分析报告"
linkTitle: "个股分析"
weight: 30
type: docs
description: "浏览所有基于龟龟投资策略的A股深度分析报告。每份报告包含五因子分析框架，提供明确的投资建议。"
---

# 个股分析报告

本页面包含所有40只A股的详细分析报告...
```

- [ ] **Step 4: 验证报告列表页面**

访问 `/reports/` 页面，验证：
- ✓ 筛选和排序UI显示正确
- ✓ 报告卡片以网格形式显示
- ✓ 页面头部显示标题和描述
- ✓ 响应式布局在移动端正确显示
- ✓ 搜索框可以输入（虽然还无法筛选）

- [ ] **Step 5: 提交第三部分**

```bash
git add layouts/reports/list.html assets/css/responsive-layout.css content/reports/_index.md
git commit -m "feat: 将报告列表改为卡片网格布局，添加筛选/排序UI框架"
```

---

#### Task 4: 优化导航栏（粘性导航 + 响应式）

**Files:**
- Modify: `themes/PaperMod/layouts/partials/header.html` (通过覆盖)
- Create: `assets/css/enhanced-navigation.css`
- Create: `assets/js/sticky-nav.js`

**目标：** 改进导航栏，添加粘性效果和移动端优化

- [ ] **Step 1: 创建导航栏样式**

创建文件 `assets/css/enhanced-navigation.css`：

```css
/* ===== 导航栏增强 ===== */
.header {
  position: sticky;
  top: 0;
  z-index: 999;
  background: var(--entry);
  border-bottom: 1px solid var(--border);
  transition: all 0.3s ease;
}

.header.scrolled {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px var(--gap);
  max-width: calc(var(--main-width) + var(--gap) * 2);
  margin: 0 auto;
  gap: 16px;
}

/* ===== Logo部分 ===== */
.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  font-size: 18px;
}

.logo a {
  color: var(--entry-text);
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: color 0.2s ease;
}

.logo a:hover {
  color: var(--theme);
}

.logo img {
  height: 30px;
  width: auto;
}

/* ===== Logo开关 ===== */
.logo-switches {
  display: flex;
  gap: 8px;
  align-items: center;
}

.theme-toggle,
.lang-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: var(--primary);
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  color: var(--entry-text);
}

.theme-toggle:hover,
.lang-toggle:hover {
  background: var(--border);
  transform: scale(1.05);
}

.theme-toggle svg,
.lang-toggle svg {
  width: 18px;
  height: 18px;
  transition: opacity 0.2s ease;
}

.theme-toggle .sun {
  display: none;
}

.theme-toggle.dark .sun {
  display: block;
}

.theme-toggle.dark .moon {
  display: none;
}

/* ===== 主菜单 ===== */
.menu {
  display: flex;
  gap: 2px;
  align-items: center;
  flex-wrap: wrap;
  justify-content: flex-end;
  flex: 1;
}

.menu-item {
  position: relative;
  display: inline-flex;
}

.menu-item > a {
  display: inline-block;
  padding: 8px 16px;
  color: var(--entry-text);
  text-decoration: none;
  border-radius: 6px;
  transition: all 0.2s ease;
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
}

.menu-item > a:hover {
  background: var(--primary);
  color: var(--theme);
}

.menu-item.active > a {
  color: var(--theme);
  background: var(--primary);
}

/* ===== 移动菜单 ===== */
.mobile-menu-toggle {
  display: none;
  width: 36px;
  height: 36px;
  background: var(--primary);
  border: none;
  border-radius: 6px;
  cursor: pointer;
  color: var(--entry-text);
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 4px;
  transition: all 0.2s ease;
}

.mobile-menu-toggle:hover {
  background: var(--border);
}

.mobile-menu-toggle span {
  width: 18px;
  height: 2px;
  background: currentColor;
  transition: all 0.3s ease;
  display: block;
}

.mobile-menu-toggle.active span:nth-child(1) {
  transform: rotate(45deg) translate(8px, 8px);
}

.mobile-menu-toggle.active span:nth-child(2) {
  opacity: 0;
}

.mobile-menu-toggle.active span:nth-child(3) {
  transform: rotate(-45deg) translate(8px, -8px);
}

/* ===== 返回顶部按钮 ===== */
.scroll-to-top {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 40px;
  height: 40px;
  background: var(--theme);
  color: white;
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
  z-index: 99;
}

.scroll-to-top.visible {
  opacity: 1;
  visibility: visible;
}

.scroll-to-top:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.scroll-to-top svg {
  width: 20px;
  height: 20px;
}

/* ===== 响应式调整 ===== */
@media (max-width: 768px) {
  .header-nav {
    padding: 12px var(--gap);
    flex-wrap: wrap;
    gap: 8px;
  }

  .menu {
    position: absolute;
    top: 60px;
    right: 0;
    left: 0;
    background: var(--entry);
    border-bottom: 1px solid var(--border);
    flex-direction: column;
    width: 100%;
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.3s ease;
    gap: 0;
    padding: 0;
    order: 3;
  }

  .menu.active {
    max-height: 400px;
    padding: 12px 0;
  }

  .menu-item > a {
    display: block;
    width: 100%;
    padding: 10px var(--gap);
    border-radius: 0;
    margin: 0;
  }

  .mobile-menu-toggle {
    display: flex;
    order: 2;
  }

  .logo {
    order: 1;
    flex: 1;
    min-width: 0;
  }

  .logo-switches {
    order: 3;
  }

  .scroll-to-top {
    bottom: 16px;
    right: 16px;
    width: 36px;
    height: 36px;
  }
}

@media (max-width: 480px) {
  .header-nav {
    padding: 10px 12px;
  }

  .logo {
    font-size: 16px;
  }

  .logo a {
    gap: 6px;
  }

  .logo img {
    height: 24px;
  }

  .menu-item > a {
    font-size: 13px;
    padding: 8px var(--gap);
  }

  .logo-switches {
    gap: 6px;
  }

  .theme-toggle,
  .lang-toggle {
    width: 32px;
    height: 32px;
  }
}
```

- [ ] **Step 2: 创建粘性导航交互脚本**

创建文件 `assets/js/sticky-nav.js`：

```javascript
// 粘性导航增强功能
(function() {
  // 初始化粘性导航
  const header = document.querySelector('.header');
  const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
  const menu = document.querySelector('.menu');
  const menuItems = document.querySelectorAll('.menu-item > a');

  if (!header) return;

  // 监听滚动事件
  let lastScrollTop = 0;
  window.addEventListener('scroll', () => {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    if (scrollTop > 50) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
    
    lastScrollTop = scrollTop;
  });

  // 移动菜单切换
  if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', () => {
      mobileMenuToggle.classList.toggle('active');
      menu.classList.toggle('active');
    });

    // 菜单项点击时关闭菜单
    menuItems.forEach(item => {
      item.addEventListener('click', () => {
        mobileMenuToggle.classList.remove('active');
        menu.classList.remove('active');
      });
    });

    // 点击菜单外部关闭菜单
    document.addEventListener('click', (e) => {
      if (!header.contains(e.target)) {
        mobileMenuToggle.classList.remove('active');
        menu.classList.remove('active');
      }
    });
  }

  // 返回顶部按钮
  const scrollToTopBtn = document.querySelector('.scroll-to-top');
  if (scrollToTopBtn) {
    window.addEventListener('scroll', () => {
      if (window.pageYOffset > 300) {
        scrollToTopBtn.classList.add('visible');
      } else {
        scrollToTopBtn.classList.remove('visible');
      }
    });

    scrollToTopBtn.addEventListener('click', () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }
})();
```

- [ ] **Step 3: 在head中加载新的样式和脚本**

编辑 `hugo.toml`，添加新的CSS和JS资源配置（如果需要）。或者在 `layouts/partials/extend_head.html` 中添加（如果存在）。

如果该文件不存在，创建 `layouts/partials/extend_head.html`：

```html
{{- /* 加载自定义样式 */ -}}
{{ $style := resources.Get "css/enhanced-navigation.css" | resources.Minify | resources.Fingerprint }}
<link rel="stylesheet" href="{{ $style.RelPermalink }}">

{{- /* 加载自定义脚本 */ -}}
{{ $script := resources.Get "js/sticky-nav.js" | resources.Minify | resources.Fingerprint }}
<script defer src="{{ $script.RelPermalink }}"></script>
```

- [ ] **Step 4: 在header模板中添加返回顶部按钮**

创建或修改 `layouts/partials/extend_footer.html`：

```html
<!-- 返回顶部按钮 -->
<button class="scroll-to-top" aria-label="返回顶部">
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <polyline points="18 15 12 9 6 15"></polyline>
  </svg>
</button>
```

- [ ] **Step 5: 验证导航栏功能**

测试以下功能：
- ✓ 滚动时导航栏添加阴影效果
- ✓ 移动端菜单按钮可以切换菜单显示/隐藏
- ✓ 菜单项悬停显示背景色
- ✓ 返回顶部按钮在滚动300px后出现
- ✓ 点击返回顶部按钮平滑滚动到页面顶部

- [ ] **Step 6: 提交第四部分**

```bash
git add assets/css/enhanced-navigation.css assets/js/sticky-nav.js layouts/partials/extend_head.html layouts/partials/extend_footer.html
git commit -m "feat: 增强导航栏，添加粘性效果、移动菜单和返回顶部按钮"
```

---

### 第二阶段：交互增强（筛选/排序 + 数据增强）

#### Task 5: 实现报告筛选和排序功能

**Files:**
- Create: `assets/js/filters-sorting.js`
- Modify: `content/reports/*/front_matter.md` (添加metadata)
- Create: `data/report-metadata.json` (可选备用数据源)

**目标：** 实现客户端筛选和排序功能，无需后端

- [ ] **Step 1: 为报告文件添加frontmatter元数据**

编辑各报告的 `content/reports/{code}/_index.md` 文件，添加如下元数据示例：

对于 `content/reports/000333/_index.md`：

```markdown
---
title: "美的集团"
code: "000333"
name: "美的集团"
rating: "good"
sector: "consumer"
date: 2026-04-15
targetPrice: 35.5
expectedReturn: 15.2
summary: "美的集团作为全球领先的消费电器制造商..."
---
```

- [ ] **Step 2: 创建筛选和排序JavaScript**

创建文件 `assets/js/filters-sorting.js`：

```javascript
(function() {
  // 获取DOM元素
  const searchInput = document.getElementById('searchInput');
  const ratingFilter = document.getElementById('ratingFilter');
  const sectorFilter = document.getElementById('sectorFilter');
  const sortBy = document.getElementById('sortBy');
  const reportsGrid = document.getElementById('reportsGrid');
  const resultCount = document.getElementById('resultCount');
  const emptyState = document.getElementById('emptyState');
  const resetButton = document.getElementById('resetFilters');
  const clearAllButton = document.getElementById('clearAllFilters');

  if (!reportsGrid) return; // 仅在报告列表页面执行

  // 获取所有报告卡片
  function getCards() {
    return Array.from(document.querySelectorAll('.report-card'));
  }

  // 获取当前筛选条件
  function getFilters() {
    return {
      search: searchInput?.value.toLowerCase() || '',
      rating: ratingFilter?.value || '',
      sector: sectorFilter?.value || '',
      sortBy: sortBy?.value || 'date-desc'
    };
  }

  // 卡片匹配筛选条件
  function matchesFilters(card, filters) {
    const code = card.getAttribute('data-code') || '';
    const rating = card.getAttribute('data-rating') || '';
    const title = card.querySelector('.card-title a')?.textContent || '';
    const sector = card.querySelector('.sector-tag')?.textContent || '';

    // 搜索匹配（代码或名称）
    if (filters.search) {
      const searchMatch = code.includes(filters.search) || 
                         title.toLowerCase().includes(filters.search);
      if (!searchMatch) return false;
    }

    // 等级筛选
    if (filters.rating && rating !== filters.rating) {
      return false;
    }

    // 板块筛选
    if (filters.sector && !sector.includes(filters.sector)) {
      return false;
    }

    return true;
  }

  // 比较函数用于排序
  function compareCards(a, b, sortType) {
    switch (sortType) {
      case 'date-desc':
        return new Date(b.querySelector('.card-date')?.textContent || 0) - 
               new Date(a.querySelector('.card-date')?.textContent || 0);
      case 'date-asc':
        return new Date(a.querySelector('.card-date')?.textContent || 0) - 
               new Date(b.querySelector('.card-date')?.textContent || 0);
      case 'name':
        return a.querySelector('.card-title a')?.textContent.localeCompare(
          b.querySelector('.card-title a')?.textContent || ''
        );
      case 'code':
        return (a.getAttribute('data-code') || '').localeCompare(
          b.getAttribute('data-code') || ''
        );
      default:
        return 0;
    }
  }

  // 应用筛选和排序
  function applyFilters() {
    const filters = getFilters();
    let cards = getCards();

    // 筛选
    const filtered = cards.filter(card => matchesFilters(card, filters));

    // 排序
    filtered.sort((a, b) => compareCards(a, b, filters.sortBy));

    // 显示/隐藏卡片
    cards.forEach(card => {
      card.style.display = filtered.includes(card) ? 'flex' : 'none';
    });

    // 更新结果计数
    const visibleCount = filtered.length;
    if (resultCount) {
      resultCount.textContent = `显示 ${visibleCount} / ${cards.length} 份报告`;
    }

    // 显示/隐藏空状态
    if (emptyState) {
      emptyState.style.display = visibleCount === 0 ? 'flex' : 'none';
    }

    // 显示/隐藏重置按钮
    const hasActiveFilters = filters.search || filters.rating || filters.sector;
    if (resetButton) {
      resetButton.style.display = hasActiveFilters ? 'inline-block' : 'none';
    }
  }

  // 重置所有筛选
  function resetFilters() {
    if (searchInput) searchInput.value = '';
    if (ratingFilter) ratingFilter.value = '';
    if (sectorFilter) sectorFilter.value = '';
    if (sortBy) sortBy.value = 'date-desc';
    applyFilters();
  }

  // 事件监听
  if (searchInput) {
    searchInput.addEventListener('input', applyFilters);
    searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        searchInput.value = '';
        applyFilters();
      }
    });
  }

  if (ratingFilter) ratingFilter.addEventListener('change', applyFilters);
  if (sectorFilter) sectorFilter.addEventListener('change', applyFilters);
  if (sortBy) sortBy.addEventListener('change', applyFilters);
  if (resetButton) resetButton.addEventListener('click', resetFilters);
  if (clearAllButton) clearAllButton.addEventListener('click', resetFilters);

  // 初始化
  applyFilters();

  // 保存筛选状态到localStorage
  function saveFilterState() {
    const filters = getFilters();
    localStorage.setItem('reportFilters', JSON.stringify(filters));
  }

  function loadFilterState() {
    const saved = localStorage.getItem('reportFilters');
    if (saved) {
      const filters = JSON.parse(saved);
      if (searchInput) searchInput.value = filters.search || '';
      if (ratingFilter) ratingFilter.value = filters.rating || '';
      if (sectorFilter) sectorFilter.value = filters.sector || '';
      if (sortBy) sortBy.value = filters.sortBy || 'date-desc';
      applyFilters();
    }
  }

  // 加载保存的筛选状态
  loadFilterState();

  // 筛选变化时保存状态
  [searchInput, ratingFilter, sectorFilter, sortBy].forEach(el => {
    if (el) el.addEventListener('change', saveFilterState);
    if (el) el.addEventListener('input', saveFilterState);
  });
})();
```

- [ ] **Step 3: 在报告列表页面加载筛选脚本**

修改 `layouts/reports/list.html`，在底部添加：

```html
{{ $script := resources.Get "js/filters-sorting.js" | resources.Minify | resources.Fingerprint }}
<script defer src="{{ $script.RelPermalink }}"></script>
```

- [ ] **Step 4: 测试筛选和排序功能**

在报告列表页面测试：
- ✓ 搜索框能够按代码或名称筛选
- ✓ 投资等级下拉框能够筛选
- ✓ 板块下拉框能够筛选
- ✓ 排序下拉框能够改变报告顺序
- ✓ 多个筛选条件叠加有效
- ✓ 结果计数更新正确
- ✓ 无匹配结果时显示空状态
- ✓ 重置按钮能够清除所有筛选

- [ ] **Step 5: 提交第五部分**

```bash
git add assets/js/filters-sorting.js layouts/reports/list.html content/reports
git commit -m "feat: 实现报告列表的客户端筛选和排序功能"
```

---

#### Task 6: 优化单篇报告页面（侧边栏导航）

**Files:**
- Create: `layouts/reports/single.html`
- Create: `layouts/partials/toc-sidebar.html`
- Create: `assets/css/post-layout-enhanced.css`

**目标：** 添加侧边栏目录导航，改进单篇报告的阅读体验

- [ ] **Step 1: 创建单篇报告layout**

创建文件 `layouts/reports/single.html`：

```html
{{- define "main" }}

<article class="post-single">
  <header class="post-header">
    <h1 class="post-title">{{ .Title }}</h1>
    {{- if .Params.code }}
    <p class="post-code">股票代码：<span>{{ .Params.code }}</span></p>
    {{- end }}
    
    <div class="post-meta">
      {{- if .Params.rating }}
      {{- partial "rating-badge.html" . }}
      {{- end }}
      
      <span class="post-date">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
          <line x1="16" y1="2" x2="16" y2="6"></line>
          <line x1="8" y1="2" x2="8" y2="6"></line>
          <line x1="3" y1="10" x2="21" y2="10"></line>
        </svg>
        {{ .Date.Format "2006年01月02日" }}
      </span>
      
      {{- if .ReadingTime }}
      <span class="reading-time">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"></circle>
          <polyline points="12 6 12 12 16 14"></polyline>
        </svg>
        {{ .ReadingTime }} 分钟阅读
      </span>
      {{- end }}
    </div>

    {{- if .Params.summary }}
    <div class="post-summary">{{ .Params.summary }}</div>
    {{- end }}
  </header>

  <div class="post-content-wrapper">
    {{- partial "toc-sidebar.html" . }}
    
    <div class="post-content">
      <div class="post-body md-content">
        {{- .Content }}
      </div>

      <div class="post-footer">
        {{- if .Params.targetPrice }}
        <div class="target-price-card">
          <h4>💰 投资目标</h4>
          <div class="price-details">
            {{- if .Params.targetPrice }}
            <div class="price-item">
              <span class="price-label">目标买入价</span>
              <span class="price-value">¥{{ .Params.targetPrice }}</span>
            </div>
            {{- end }}
            {{- if .Params.expectedReturn }}
            <div class="price-item">
              <span class="price-label">预期年化回报</span>
              <span class="price-value {{ if gt (.Params.expectedReturn | float) 0 }}positive{{ else }}negative{{ end }}">
                {{ .Params.expectedReturn }}%
              </span>
            </div>
            {{- end }}
          </div>
        </div>
        {{- end }}

        <div class="post-tags">
          {{- if .Params.tags }}
          {{- range .Params.tags }}
          <a href="/tags/{{ . }}" class="tag-link">#{{ . }}</a>
          {{- end }}
          {{- end }}
        </div>
      </div>

      {{- if .Params.relatedReports }}
      <div class="related-reports">
        <h3>📚 相关报告</h3>
        <div class="related-grid">
          {{- range .Params.relatedReports }}
          <a href="{{ . }}" class="related-card">查看报告</a>
          {{- end }}
        </div>
      </div>
      {{- end }}
    </div>
  </div>

  {{- if .NextInSection }}
  <nav class="post-nav">
    {{- with .PrevInSection }}
    <a href="{{ .Permalink }}" class="post-nav-prev">
      <span class="nav-label">← 上一篇</span>
      <span class="nav-title">{{ .Title }}</span>
    </a>
    {{- end }}
    {{- with .NextInSection }}
    <a href="{{ .Permalink }}" class="post-nav-next">
      <span class="nav-label">下一篇 →</span>
      <span class="nav-title">{{ .Title }}</span>
    </a>
    {{- end }}
  </nav>
  {{- end }}
</article>

{{- end }}
```

- [ ] **Step 2: 创建目录侧边栏组件**

创建文件 `layouts/partials/toc-sidebar.html`：

```html
{{- if .Params.showtoc | default (site.Params.showtoc) }}
<aside class="toc-sidebar">
  <div class="toc-wrapper">
    <div class="toc-header">
      <h3>📑 目录</h3>
      <button class="toc-toggle" aria-label="切换目录显示">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="8" y1="6" x2="21" y2="6"></line>
          <line x1="8" y1="12" x2="21" y2="12"></line>
          <line x1="8" y1="18" x2="21" y2="18"></line>
          <line x1="3" y1="6" x2="3.01" y2="6"></line>
          <line x1="3" y1="12" x2="3.01" y2="12"></line>
          <line x1="3" y1="18" x2="3.01" y2="18"></line>
        </svg>
      </button>
    </div>
    {{ .TableOfContents }}
  </div>
</aside>
{{- end }}
```

- [ ] **Step 3: 创建单篇报告样式**

创建文件 `assets/css/post-layout-enhanced.css`：

```css
/* ===== 文章容器 ===== */
.post-single {
  width: 100%;
}

/* ===== 文章头部 ===== */
.post-header {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--border);
}

.post-title {
  font-size: 40px;
  line-height: 1.2;
  margin-bottom: 8px;
  font-weight: 700;
}

.post-code {
  font-size: 14px;
  color: var(--secondary);
  margin: 0 0 12px 0;
  font-family: monospace;
  font-weight: 500;
}

.post-code span {
  color: var(--theme);
  font-weight: 600;
}

.post-meta {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  align-items: center;
  font-size: 14px;
  color: var(--secondary);
  margin-bottom: 12px;
}

.post-meta svg {
  width: 14px;
  height: 14px;
  vertical-align: middle;
  margin-right: 4px;
}

.post-date,
.reading-time {
  display: flex;
  align-items: center;
  gap: 4px;
}

.post-summary {
  font-size: 16px;
  line-height: 1.6;
  color: var(--entry-text);
  background: var(--primary);
  padding: 16px;
  border-left: 4px solid var(--theme);
  border-radius: 4px;
  margin-top: 12px;
}

/* ===== 内容布局 ===== */
.post-content-wrapper {
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: 32px;
  align-items: start;
  margin-bottom: 40px;
}

/* ===== 目录侧边栏 ===== */
.toc-sidebar {
  position: sticky;
  top: calc(var(--header-height) + 20px);
  max-height: calc(100vh - var(--header-height) - 40px);
  overflow-y: auto;
  z-index: 10;
}

.toc-wrapper {
  background: var(--entry);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 16px;
}

.toc-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border);
}

.toc-header h3 {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
}

.toc-toggle {
  display: none;
  background: var(--primary);
  border: none;
  width: 28px;
  height: 28px;
  border-radius: 4px;
  cursor: pointer;
  color: var(--entry-text);
}

.toc-toggle:hover {
  background: var(--border);
}

.toc-wrapper ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.toc-wrapper li {
  margin: 4px 0;
}

.toc-wrapper a {
  display: block;
  padding: 4px 8px;
  color: var(--secondary);
  text-decoration: none;
  font-size: 13px;
  border-radius: 4px;
  transition: all 0.2s ease;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.toc-wrapper a:hover {
  background: var(--primary);
  color: var(--theme);
  padding-left: 12px;
}

.toc-wrapper ul ul a {
  padding-left: 16px;
}

.toc-wrapper ul ul ul a {
  padding-left: 24px;
}

/* ===== 文章内容 ===== */
.post-content {
  min-width: 0;
}

.post-body {
  margin-bottom: 32px;
  line-height: 1.8;
}

.post-body h2,
.post-body h3,
.post-body h4 {
  margin-top: 32px;
  margin-bottom: 16px;
}

.post-body h2 {
  font-size: 28px;
  border-bottom: 2px solid var(--border);
  padding-bottom: 8px;
}

.post-body h3 {
  font-size: 22px;
}

.post-body h4 {
  font-size: 18px;
}

.post-body table {
  width: 100%;
  border-collapse: collapse;
  margin: 16px 0;
}

.post-body table th,
.post-body table td {
  padding: 12px;
  text-align: left;
  border: 1px solid var(--border);
}

.post-body table th {
  background: var(--primary);
  font-weight: 600;
}

.post-body table tr:nth-child(even) {
  background: var(--primary);
}

/* ===== 文章页脚 ===== */
.post-footer {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid var(--border);
}

.target-price-card {
  background: var(--primary);
  border-left: 4px solid var(--theme);
  padding: 16px;
  border-radius: 6px;
  margin-bottom: 16px;
}

.target-price-card h4 {
  margin: 0 0 12px 0;
  font-size: 14px;
}

.price-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 12px;
}

.price-item {
  display: flex;
  flex-direction: column;
}

.price-label {
  font-size: 12px;
  color: var(--secondary);
  margin-bottom: 4px;
}

.price-value {
  font-size: 18px;
  font-weight: 700;
  color: var(--theme);
}

.price-value.negative {
  color: #ef4444;
}

.post-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.tag-link {
  display: inline-block;
  padding: 6px 12px;
  background: var(--primary);
  color: var(--theme);
  border-radius: 20px;
  text-decoration: none;
  font-size: 12px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.tag-link:hover {
  background: var(--theme);
  color: white;
}

/* ===== 相关报告 ===== */
.related-reports {
  margin-top: 40px;
  padding-top: 24px;
  border-top: 1px solid var(--border);
}

.related-reports h3 {
  margin-bottom: 16px;
}

.related-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
}

.related-card {
  padding: 12px;
  background: var(--primary);
  border: 1px solid var(--border);
  border-radius: 6px;
  text-decoration: none;
  color: var(--theme);
  font-weight: 500;
  text-align: center;
  transition: all 0.2s ease;
}

.related-card:hover {
  background: var(--theme);
  color: white;
  transform: translateY(-2px);
}

/* ===== 文章导航 ===== */
.post-nav {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-top: 40px;
  padding: 24px;
  background: var(--entry);
  border: 1px solid var(--border);
  border-radius: 8px;
}

.post-nav a {
  display: flex;
  flex-direction: column;
  text-decoration: none;
  color: var(--entry-text);
  transition: all 0.2s ease;
  padding: 12px;
  border-radius: 4px;
}

.post-nav a:hover {
  background: var(--primary);
  color: var(--theme);
}

.nav-label {
  font-size: 12px;
  color: var(--secondary);
  margin-bottom: 4px;
}

.nav-title {
  font-weight: 600;
  font-size: 14px;
}

.post-nav-next {
  text-align: right;
}

/* ===== 响应式调整 ===== */
@media (max-width: 1024px) {
  .post-content-wrapper {
    grid-template-columns: 1fr;
    gap: 24px;
  }

  .toc-sidebar {
    position: static;
    max-height: none;
    order: -1;
  }
}

@media (max-width: 768px) {
  .post-title {
    font-size: 32px;
  }

  .post-meta {
    font-size: 12px;
    gap: 12px;
  }

  .post-body h2 {
    font-size: 24px;
  }

  .post-body h3 {
    font-size: 20px;
  }

  .toc-toggle {
    display: block;
  }

  .toc-wrapper {
    max-height: 0;
    overflow: hidden;
    padding: 0;
    border: none;
    transition: max-height 0.3s ease;
  }

  .toc-wrapper.expanded {
    max-height: 400px;
    border: 1px solid var(--border);
    padding: 16px;
  }

  .post-nav {
    grid-template-columns: 1fr;
  }

  .post-nav-next {
    text-align: left;
  }
}

@media (max-width: 480px) {
  .post-title {
    font-size: 24px;
  }

  .post-meta {
    flex-direction: column;
    align-items: flex-start;
  }

  .post-header {
    margin-bottom: 16px;
    padding-bottom: 16px;
  }

  .price-details {
    grid-template-columns: 1fr;
  }

  .related-grid {
    grid-template-columns: 1fr;
  }

  .post-body table {
    font-size: 12px;
  }

  .post-body table th,
  .post-body table td {
    padding: 8px;
  }
}
```

- [ ] **Step 4: 添加目录交互脚本**

在 `assets/js/sticky-nav.js` 中添加目录切换功能（或创建新文件 `assets/js/toc-interactions.js`）：

```javascript
(function() {
  const tocToggle = document.querySelector('.toc-toggle');
  const tocWrapper = document.querySelector('.toc-wrapper');

  if (!tocToggle || !tocWrapper) return;

  // 切换目录显示
  tocToggle.addEventListener('click', () => {
    tocWrapper.classList.toggle('expanded');
    tocToggle.classList.toggle('active');
  });

  // 点击目录链接时关闭目录（在移动设备上）
  if (window.innerWidth < 768) {
    const tocLinks = tocWrapper.querySelectorAll('a');
    tocLinks.forEach(link => {
      link.addEventListener('click', () => {
        tocWrapper.classList.remove('expanded');
        tocToggle.classList.remove('active');
      });
    });
  }
})();
```

- [ ] **Step 5: 测试单篇报告页面**

访问任何报告页面，验证：
- ✓ 页面标题和元信息显示正确
- ✓ 投资等级徽章显示
- ✓ 目标价卡片显示正确
- ✓ 侧边栏目录粘性定位工作正常
- ✓ 在移动端目录可以切换显示/隐藏
- ✓ 文章导航显示上一篇/下一篇

- [ ] **Step 6: 提交第六部分**

```bash
git add layouts/reports/single.html layouts/partials/toc-sidebar.html assets/css/post-layout-enhanced.css
git commit -m "feat: 优化单篇报告页面，添加侧边栏目录导航和目标价展示"
```

---

### 第三阶段：高级功能和性能优化

#### Task 7: 添加数据可视化和关键指标（可选）

**Files:**
- Create: `layouts/partials/metrics-chart.html`
- Create: `assets/js/chart-utils.js`
- Modify: `layouts/reports/single.html` (集成图表)

**目标：** 添加关键财务指标的可视化展示

> **注**：这一任务可选。如果报告中包含结构化数据（如JSON frontmatter），可以添加图表。

- [ ] **Step 1: 添加数据属性到报告**

编辑报告frontmatter，添加结构化数据：

```yaml
---
metrics:
  roic: 18.5
  roe: 16.2
  debt_ratio: 0.35
  growth_rate: 12.5
factorScores:
  factor1a: 9
  factor1b: 8
  factor2: 7
  factor3: 8
  factor4: 9
---
```

- [ ] **Step 2: 创建指标可视化组件**

创建文件 `layouts/partials/metrics-chart.html`：

```html
{{- if .Params.metrics }}
<div class="metrics-dashboard">
  <h3>📈 关键指标</h3>
  
  <div class="metrics-grid">
    {{- with .Params.metrics.roic }}
    <div class="metric-box">
      <div class="metric-bar" style="width: {{ min . 30 | div 30 | mul 100 }}%"></div>
      <div class="metric-info">
        <span class="metric-name">ROIC</span>
        <span class="metric-num">{{ . }}%</span>
      </div>
    </div>
    {{- end }}

    {{- with .Params.metrics.roe }}
    <div class="metric-box">
      <div class="metric-bar" style="width: {{ min . 30 | div 30 | mul 100 }}%"></div>
      <div class="metric-info">
        <span class="metric-name">ROE</span>
        <span class="metric-num">{{ . }}%</span>
      </div>
    </div>
    {{- end }}

    {{- with .Params.metrics.debt_ratio }}
    <div class="metric-box">
      <div class="metric-bar" style="width: {{ . | div 1 | mul 100 }}%"></div>
      <div class="metric-info">
        <span class="metric-name">负债率</span>
        <span class="metric-num">{{ . }}</span>
      </div>
    </div>
    {{- end }}

    {{- with .Params.metrics.growth_rate }}
    <div class="metric-box">
      <div class="metric-bar" style="width: {{ min . 30 | div 30 | mul 100 }}%"></div>
      <div class="metric-info">
        <span class="metric-name">增长率</span>
        <span class="metric-num">{{ . }}%</span>
      </div>
    </div>
    {{- end }}
  </div>
</div>
{{- end }}
```

- [ ] **Step 3: 提交第七部分**

```bash
git add layouts/partials/metrics-chart.html
git commit -m "feat: 添加关键财务指标可视化展示"
```

---

#### Task 8: CSS/JS 资源加载优化

**Files:**
- Modify: `hugo.toml` (资源缩小和指纹识别配置)
- Modify: `layouts/partials/extend_head.html` (资源优化)

**目标：** 优化CSS和JavaScript加载，提升性能

- [ ] **Step 1: 配置Hugo资源处理**

编辑 `hugo.toml`，添加以下配置：

```toml
[outputs]
  home = ["HTML", "JSON"]
  section = ["HTML"]
  taxonomy = ["HTML"]
  term = ["HTML"]

[mediaTypes."application/json"]
  suffix = "json"

[outputFormats.JSON]
  mediaType = "application/json"
  isPlainText = true

[minify]
  disableHTML = false
  disableCSS = false
  disableJS = false
  disableJSON = false
```

- [ ] **Step 2: 更新extend_head.html以优化加载**

编辑 `layouts/partials/extend_head.html`：

```html
{{- /* 预加载关键资源 */ -}}
<link rel="preload" as="style" href="{{ resources.Get "css/custom-cards.css" | resources.Minify | resources.Fingerprint | .RelPermalink }}">
<link rel="preload" as="style" href="{{ resources.Get "css/investment-ratings.css" | resources.Minify | resources.Fingerprint | .RelPermalink }}">

{{- /* 加载关键样式 */ -}}
{{ $style1 := resources.Get "css/custom-cards.css" | resources.Minify | resources.Fingerprint }}
<link rel="stylesheet" href="{{ $style1.RelPermalink }}" integrity="{{ $style1.Data.Integrity }}">

{{ $style2 := resources.Get "css/investment-ratings.css" | resources.Minify | resources.Fingerprint }}
<link rel="stylesheet" href="{{ $style2.RelPermalink }}" integrity="{{ $style2.Data.Integrity }}">

{{ $style3 := resources.Get "css/responsive-layout.css" | resources.Minify | resources.Fingerprint }}
<link rel="stylesheet" href="{{ $style3.RelPermalink }}" integrity="{{ $style3.Data.Integrity }}">

{{ $style4 := resources.Get "css/post-layout-enhanced.css" | resources.Minify | resources.Fingerprint }}
<link rel="stylesheet" href="{{ $style4.RelPermalink }}" integrity="{{ $style4.Data.Integrity }}">

{{ $style5 := resources.Get "css/enhanced-navigation.css" | resources.Minify | resources.Fingerprint }}
<link rel="stylesheet" href="{{ $style5.RelPermalink }}" integrity="{{ $style5.Data.Integrity }}">

{{- /* 延迟加载脚本 */ -}}
{{ $script1 := resources.Get "js/sticky-nav.js" | resources.Minify | resources.Fingerprint }}
<script defer src="{{ $script1.RelPermalink }}" integrity="{{ $script1.Data.Integrity }}"></script>

{{ $script2 := resources.Get "js/filters-sorting.js" | resources.Minify | resources.Fingerprint }}
<script defer src="{{ $script2.RelPermalink }}" integrity="{{ $script2.Data.Integrity }}"></script>
```

- [ ] **Step 3: 提交第八部分**

```bash
git add hugo.toml layouts/partials/extend_head.html
git commit -m "perf: 优化CSS/JS资源加载，启用缩小和指纹识别"
```

---

#### Task 9: 最后的整合和测试

**Files:**
- Verify: 所有布局和样式文件

**目标：** 综合测试所有优化，确保没有破坏

- [ ] **Step 1: 本地构建和测试**

```bash
# 清空public目录
rm -rf public/

# 构建站点
hugo

# 启动本地服务器
hugo server -D

# 访问 http://localhost:1313 进行测试
```

- [ ] **Step 2: 检查所有页面**

- ✓ 首页（/）：英雄部分、统计面板、优先级分类、最近报告显示正确
- ✓ 报告列表（/reports/）：卡片网格、筛选/排序工作正常
- ✓ 单篇报告：布局正确、侧边栏导航、元信息显示
- ✓ 导航栏：粘性效果、移动菜单、返回顶部按钮
- ✓ 响应式：移动端（480px）、平板（768px）、桌面（1920px）

- [ ] **Step 3: 性能检查**

```bash
# 检查生成的文件大小
du -sh public/

# 检查CSS/JS文件是否已压缩
find public/assets -name "*.css" -o -name "*.js" | xargs wc -l
```

- [ ] **Step 4: 提交最终版本**

```bash
git add .
git commit -m "test: 完成全面的布局优化，验证所有功能正常工作"
```

---

## 总结

| 阶段 | 任务 | 优先级 | 状态 |
|-----|------|--------|------|
| 1 | 首页重设计 | 🔴 高 | - [ ] |
| 1 | 卡片组件 | 🔴 高 | - [ ] |
| 1 | 报告列表优化 | 🔴 高 | - [ ] |
| 1 | 导航栏增强 | 🟠 中 | - [ ] |
| 2 | 筛选/排序 | 🟠 中 | - [ ] |
| 2 | 单篇报告优化 | 🟠 中 | - [ ] |
| 3 | 数据可视化 | 🟡 低 | - [ ] |
| 3 | 性能优化 | 🟡 低 | - [ ] |
| 3 | 集成测试 | 🔴 高 | - [ ] |

---

## 关键成果

✅ **首页**：从简单profile改为现代化英雄部分 + 统计面板 + 优先级分类网格 + 最近报告
✅ **列表页**：从线性改为响应式卡片网格 + 客户端筛选排序
✅ **单篇报告**：添加侧边栏目录 + 目标价展示 + 相关报告推荐
✅ **导航**：粘性效果 + 移动菜单 + 返回顶部
✅ **响应式**：完整的移动端适配（480px/768px/1920px）
✅ **性能**：CSS/JS压缩、资源指纹识别

---

**下一步行动**: 用户选择执行方式
- **选项A**: 子代理驱动执行（使用superpowers:subagent-driven-development）
- **选项B**: 内联执行（使用superpowers:executing-plans）
