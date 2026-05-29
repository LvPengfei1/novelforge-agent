# 技术栈：Web出海建站工具链

主角用于搭建出海网站、赚取美元收入的完整技术栈。本页作为小说中所有涉及建站、部署、变现等技术环节的事实基准，写作时应以本页为准，避免随意更换工具或流程。

## 前端开发栈

**核心三件套：Next.js + Tailwind CSS + TypeScript**

- **Next.js 15/16**（基于React 19）：服务端渲染（SSR），SEO天然友好，Google爬虫可直接抓取页面内容。配合Vercel AI SDK V5可实现AI驱动的动态功能。
- **Tailwind CSS 4**：原子化CSS框架，AI生成代码时产出质量高、风格统一，减少手工调整成本。
- **TypeScript**：静态类型检查，降低AI生成代码的运行时错误率。

选栈理由（小说中主角的思考逻辑）：
1. SEO友好——Next.js的SSR让Google能直接索引页面，工具站和内容站都受益。
2. 部署方便——Next.js与Vercel深度绑定，推送代码即上线，零运维。
3. AI生成代码质量高——ChatGPT/Claude对Next.js+Tailwind+TS的训练数据最充足，生成的代码可直接使用率高。

备选方案：WordPress（新手友好、插件丰富，但AI生成代码效率低）、No-Code工具（快速上线但可定制性差）。主角初期可能尝试过这些方案，最终转向Next.js。

## 部署与基础设施

**Vercel**：主力部署平台。免费额度足够个人站使用，与GitHub仓库联动，push即部署，自动HTTPS。Next.js的首选部署环境。

**Cloudflare**：承担多个角色——
- DNS解析：域名托管后自动管理DNS记录。
- CDN加速：全球节点分发静态资源。
- R2对象存储：免费10GB存储空间，绑定自定义子域名（如cdn.example.com），用于存放图片、视频等静态文件。设置自定义域名时系统自动配置DNS。
- 邮件转发：免费域名邮箱转发功能。
- Crawler Hints：开启后可帮助Bing等搜索引擎自动发现和收录页面。

**域名管理**：
- 注册查询：instantdomainsearch.com、query.domains 检查域名是否可注册。
- 黑历史查询：virustotal.com 检查域名是否曾被惩罚。
- 购买平台：Namecheap、Spaceship，购买时可搜索优惠码。
- 绑定流程：在域名注册商处将NameServer改为Cloudflare提供的地址，约10分钟生效。

**数据库**：Supabase（开源Firebase替代）或Neon（Serverless PostgreSQL）。

**邮箱**：Resend（事务邮件）、Zoho（免费企业邮箱）。

## 支付与变现

**Stripe**：海外订阅支付首选，支持信用卡和多种支付方式，按交易抽成。需要海外银行账户接收款项。

**Google AdSense**：广告变现，但2025年后ECPM下降70-90%，不能作为唯一收入来源。适合内容站和工具站的补充收入。

**Creem**：Stripe的替代方案，对个人开发者更友好，接入门槛低。主角早期可能先接Creem，后期升级Stripe。

**LemonSqueezy**：数字产品销售和SaaS订阅的替代支付平台，无需海外银行账户即可收款。

**收款账户**：香港银行卡是收款必需品。需亲自赴港办理，常见选择包括中银香港、汇丰等。小说中这一环节可以作为主角出海路上的一个关卡。

变现组合策略：订阅模式为主（40-60%）+ AdSense广告（30-50%）+ 联盟营销（10-20%）。

## 分析与监控

**Google Analytics（GA4）**：流量分析标配，追踪用户来源、行为、转化。

**Google Search Console（GSC）**：SEO必备工具。提交Sitemap、监控收录状态、查看搜索词排名和点击数据。网站上线后第一时间提交收录。

**Hotjar**：热力图和用户行为录制，了解用户在页面上的实际点击和浏览行为。

**Microsoft Clarity**：免费的热力图和会话录制工具，可替代Hotjar。

**Plausible**：注重隐私的分析工具，不使用Cookie，适合面向欧洲用户。

其他监控：pagespeed.web.dev（性能测试）、web.archive.org（网站历史查询）。

## AI编程工具链

**ChatGPT（GPT-4）**：内容生成首选，擅长写营销文案、SEO文章、产品描述。

**Claude**：代码生成和长文写作，对Next.js+TypeScript代码生成质量高，能理解复杂上下文。

**Cursor**：AI驱动的代码编辑器，内置代码补全和对话式编程，主角日常开发的主力工具。

**GitHub Copilot**：行级代码补全，在Cursor之外提供额外的编码辅助。

**v0.dev**：Vercel推出的AI UI生成工具，输入描述即可生成React组件，快速搭建页面原型。

典型用法：用v0.dev快速生成UI原型，用Cursor/Claude编写业务逻辑，用ChatGPT生成内容和文案。

## 典型建站流程

从零到上线的完整步骤，主角在小说中应多次执行此流程（速度逐渐加快体现成长）：

1. **关键词研究**：用Ahrefs/Google Trends找到有搜索量但竞争低的蓝海词。关注新词红利期（24小时黄金窗口）。核心公式：搜索量 > 1000，关键词难度（KD） < 20。
2. **需求确认**：确定网站类型（工具站/内容站/SaaS），明确核心功能和目标用户。
3. **域名购买**：通过Namecheap/Spaceship购买域名，绑定Cloudflare DNS。
4. **AI生成代码**：用v0.dev生成UI，Cursor+Claude编写逻辑，ChatGPT生成内容。人工审核调整核心功能。
5. **部署上线**：推送到GitHub，Vercel自动构建部署。配置Cloudflare R2存储、邮件转发。
6. **提交收录**：向Google Search Console提交Sitemap，同时提交Bing Webmaster。开启Cloudflare Crawler Hints。
7. **SEO优化**：配置TDK（标题、描述、关键词），添加Schema结构化数据，优化Core Web Vitals指标。
8. **变现接入**：根据网站类型接入Stripe/Creem（订阅）、AdSense（广告）或联盟链接。
9. **外链建设**：提交到导航站和目录站（如bestdirectories.org、directoryfame.com），提升域名权重。
10. **数据监控**：接入GA4和GSC，持续追踪流量和排名，根据数据迭代优化。

进阶操作：程序化SEO（pSEO）批量生成页面、Google One Tap丝滑登录接入、favicon多平台适配（通过favicon.io一键生成）。

## 写作注意事项

- 小说中涉及的具体技术细节（版本号、工具名称、操作步骤）以本页为准。
- 主角在不同阶段对技术栈的掌握深度不同：初期依赖AI生成、中期能人工审核调整、后期可独立架构。
- 遇到技术困难时，合理的解决路径是：问AI → 查文档 → 社区求助，不要凭空突破。
- 工具和平台的名称不要随意更换或混淆（如不要把Vercel写成Verdcel）。

## 交叉引用

- 人物：主角的技术成长弧见 `characters/protagonist.md`
- 主线：建站里程碑见 `plot/main-plot.md`
- 相关页面：`world/monetization.md`（变现策略详述）、`world/seo-strategy.md`（SEO策略详述）

## 变更记录

- 2026-05-28：初始创建，基于 raw/出海备份 系列资料整理。
