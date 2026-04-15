# 部署到 GitHub Pages 说明

## 配置步骤

### 1. 修改 hugo.toml

将 `hugo.toml` 中的 `baseURL` 修改为您的 GitHub Pages 地址：

```toml
baseURL = 'https://your-username.github.io/investment-reports-site'
```

将 `your-username` 替换为您的 GitHub 用户名。

### 2. 推送到 GitHub

```bash
# 进入项目目录
cd investment-reports-site

# 初始化 Git 仓库（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: Hugo site with investment reports"

# 添加远程仓库（替换为您的仓库地址）
git remote add origin https://github.com/your-username/investment-reports-site.git

# 推送到 GitHub
git push -u origin main
```

### 3. 启用 GitHub Pages

1. 进入您的 GitHub 仓库页面
2. 点击 **Settings** → **Pages**
3. 在 "Source" 部分选择：
   - **Deploy from a branch** → 改为 **GitHub Actions**
4. 保存设置

### 4. 等待部署

- 推送到 GitHub 后，Actions 会自动运行
- 进入 **Actions** 标签页查看部署状态
- 部署完成后，网站将在 `https://your-username.github.io/investment-reports-site` 可用

## 自动部署

每次推送到 `main` 或 `master` 分支时，GitHub Actions 会自动：
1. 构建 Hugo 网站
2. 部署到 GitHub Pages

您也可以手动触发部署：
- 进入 **Actions** → **Deploy Hugo site to Pages** → **Run workflow**

## 自定义域名（可选）

如需使用自定义域名：

1. 在 `static/` 目录下创建 `CNAME` 文件，内容为您的域名
2. 在域名 DNS 设置中添加 CNAME 记录指向 `your-username.github.io`
3. 修改 `hugo.toml` 中的 `baseURL` 为您的自定义域名

## 故障排除

### 部署失败

1. 检查 **Actions** 日志查看错误信息
2. 确保主题子模块已正确添加：
   ```bash
   git submodule update --init --recursive
   ```

### 页面样式丢失

检查 `baseURL` 配置是否正确，确保与 GitHub Pages 地址匹配。

### 主题不显示

确保 PaperMod 主题已正确添加为子模块：
```bash
git submodule add https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
```
