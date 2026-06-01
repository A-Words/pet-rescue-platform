# 宠物走失与领养救助平台数据库分析与设计

---

## 摘  要

随着城市宠物饲养数量的快速增长，宠物走失和流浪动物收容问题日益突出。传统的宠物寻找方式效率低下，信息传播范围有限，而领养救助流程也缺乏系统化的管理手段。为此，本文设计并实现了一个宠物走失与领养救助平台的数据库系统。

本系统主要完成了以下工作：第一步从需求概述和系统边界、业务需求分析、功能需求分析、数据需求分析和业务规则分析对系统进行了需求分析；第二步从概念结构设计、逻辑结构设计以及物理结构设计三个方面对系统进行了数据库设计，其中使用E-R图完成了概念结构设计，使用规范化理论对转换后的关系模式进行了规范化处理，使用PostgreSQL 16创建了名为lost_pet_db的数据库，并设计了7张数据表结构从而完成了物理结构的设计；第三步主要使用SQL语句创建数据库、创建数据表、创建索引、创建视图、创建存储过程以及创建触发器，并完成了表中数据的查询、插入、删除等操作。

设计这个系统解决了传统宠物救助方式信息不对称、流程不规范的弊端，能够实现走失宠物信息发布与线索上报、可领养宠物信息管理、领养申请与审核、领养后回访提醒以及运营数据统计等功能，为宠物救助站提供了完整的信息化管理方案。

**关键词：** PostgreSQL；数据库设计；宠物救助；领养管理

---

## ABSTRACT

With the rapid growth of urban pet ownership, the problems of lost pets and stray animal sheltering have become increasingly prominent. Traditional pet search methods are inefficient with limited information dissemination, while the adoption and rescue process lacks systematic management. To address these issues, this paper designs and implements a database system for a pet loss and adoption rescue platform.

The system mainly completed the following work: First, requirements analysis was conducted from the perspectives of system overview and boundary, business requirements, functional requirements, data requirements, and business rules. Second, database design was carried out from three aspects including conceptual structure design, logical structure design, and physical structure design, where E-R diagrams were used for conceptual design, normalization theory was applied to optimize the converted relational schemas, PostgreSQL 16 was used to create a database named lost_pet_db with 7 data tables to complete the physical structure design. Third, SQL statements were used to create the database, tables, indexes, views, stored procedures, and triggers, along with data query, insertion, and deletion operations.

This system solves the problems of information asymmetry and irregular processes in traditional pet rescue methods, and can realize functions such as lost pet information publishing and clue reporting, adoptable pet information management, adoption application and review, post-adoption visit reminders, and operational data statistics, providing a complete information management solution for pet rescue stations.

**Key words:** PostgreSQL; Database Design; Pet Rescue; Adoption Management

---

## 目  录

- 摘要
- ABSTRACT
- 第1章 需求分析
  - 1.1 需求概述和系统边界
    - 1.1.1 需求概述
    - 1.1.2 系统边界
  - 1.2 业务需求分析
  - 1.3 功能需求分析
  - 1.4 数据需求分析
  - 1.5 业务规则分析
- 第2章 概念结构设计
  - 2.1 确定实体集及属性
  - 2.2 确定联系集及属性
  - 2.3 绘制局部E-R图
  - 2.4 绘制全局E-R图
- 第3章 逻辑结构设计
  - 3.1 E-R模型转换为关系模型的转换方法
  - 3.2 设计初始关系模式
  - 3.3 关系模式优化
- 第4章 物理结构设计
- 第5章 数据库实施
  - 5.1 定义数据库对象
    - 5.1.1 定义数据库
    - 5.1.2 定义数据表
  - 5.2 数据操作
    - 5.2.1 插入数据
    - 5.2.2 修改数据
    - 5.2.3 删除数据
    - 5.2.4 查询数据
  - 5.3 创建视图
  - 5.4 创建存储过程
  - 5.5 创建触发器
- 第6章 数据库的安全性（选做）
  - 6.1 用户和权限管理
  - 6.2 数据库的备份与恢复
- 第7章 系统实现（选做）
  - 7.1 走失宠物发布功能
    - 7.1.1 界面
    - 7.1.2 数据操作核心代码
  - 7.2 领养申请功能
    - 7.2.1 界面
    - 7.2.2 数据操作核心代码
- 结论
- 参考文献
- 致谢

---

## 第1章 需求分析

### 1.1 需求概述和系统边界

#### 1.1.1 需求概述

随着我国城市化进程加快，宠物饲养家庭数量持续增长。据相关统计，我国城镇宠物犬猫数量已超过1亿只。与此同时，宠物走失事件频发，每年有大量宠物因各种原因走失，给宠物主人带来极大的精神痛苦。此外，流浪动物的数量也在不断增加，亟需有效的救助和领养机制。

传统的宠物寻找方式主要包括张贴寻宠启事、在社交媒体发布信息等，这些方式存在信息传播范围有限、信息真实性难以验证、匹配效率低下等问题。在领养方面，许多救助站缺乏系统化的管理工具，导致领养流程不规范、回访机制缺失、数据统计困难。

因此，开发一个集宠物走失信息发布、线索收集、可领养宠物管理、领养申请审核、领养后回访提醒及运营统计于一体的综合性数据库系统具有重要的现实意义。

本系统主要包括以下用户角色：

（1）普通用户：可以发布走失宠物信息、提交发现线索、浏览可领养宠物、提交领养申请、查看自己的申请记录等。

（2）管理员：可以管理可领养宠物信息、审核发现线索、审批领养申请、查看运营统计数据、管理回访提醒等。

#### 1.1.2 系统边界

宠物走失与领养救助平台的系统边界如图1.1所示。系统外部实体包括普通用户和管理员，系统内部处理走失宠物管理、线索管理、领养管理、审核管理和统计分析等核心业务。

图1.1 系统边界图

```
                    ┌─────────────────────────────┐
                    │       宠物走失与领养         │
    ┌──────┐        │         救助平台             │        ┌──────────┐
    │普通用户│──────▶│  走失宠物管理  线索管理     │◀───────│  管理员   │
    │      │──────▶│  领养管理      审核管理     │───────▶│          │
    │      │◀──────│  统计分析                   │        │          │
    └──────┘        └─────────────────────────────┘        └──────────┘
```

### 1.2 业务需求分析

宠物走失与领养救助平台的业务流程主要包括以下几个核心流程：

（1）走失宠物信息发布流程：用户登录系统后，填写宠物基本信息（种类、品种、颜色、性别等）、走失信息（走失日期、地点、联系方式等）并上传照片，提交后系统保存走失宠物记录，状态默认为"active"（寻找中）。

（2）发现线索上报流程：其他用户在浏览走失宠物详情时，如发现疑似宠物，可提交线索信息，包括发现地点、发现日期、描述信息和照片等。线索提交后状态为"pending"（待审核），管理员审核后可将其标记为"confirmed"（已确认）或"rejected"（已拒绝）。

（3）领养申请流程：用户浏览可领养宠物列表，选择心仪宠物后填写领养申请表，包括个人信息、住房情况、养宠经验等。系统通过数据库触发器自动检查：宠物是否仍可领养、用户是否已提交过申请。申请提交后状态为"pending"。

（4）领养审核流程：管理员查看所有待审核的领养申请，对申请进行审批。审批通过时，数据库触发器自动执行以下操作：将宠物状态更新为"已领养"、自动拒绝该宠物的其他待审核申请、自动生成30天后的回访提醒记录。

（5）回访管理流程：领养审批通过后系统自动生成回访提醒，管理员可在提醒到期后记录回访情况，标记为"已完成"或"逾期"。

宠物走失与领养救助平台的业务流程如图1.2所示。

图1.2 业务流程图

```
用户注册/登录
    │
    ├──▶ 发布走失宠物信息 ──▶ 系统保存（状态：寻找中）
    │                              │
    │                              ▼
    │                         其他用户提交线索
    │                              │
    │                              ▼
    │                         管理员审核线索
    │                         ├── 确认 ──▶ 标记宠物为"已找回"
    │                         └── 拒绝
    │
    ├──▶ 浏览可领养宠物 ──▶ 提交领养申请
    │                              │
    │                              ▼
    │                         管理员审批申请
    │                         ├── 通过 ──▶ 宠物标记"已领养"
    │                         │           ──▶ 拒绝其他申请
    │                         │           ──▶ 生成回访提醒
    │                         └── 拒绝
    │
    └──▶ 查看统计数据（管理员）
```

### 1.3 功能需求分析

根据上述的需求概述和业务需求分析，宠物走失与领养救助平台的功能模块结构如图1.3所示。

图1.3 功能模块结构图

```
宠物走失与领养救助平台
├── 用户管理
│   ├── 用户注册
│   ├── 用户登录
│   └── 个人信息管理
├── 走失宠物管理
│   ├── 发布走失信息
│   ├── 查询走失宠物
│   ├── 查看宠物详情
│   ├── 修改走失信息
│   └── 更新宠物状态
├── 线索管理
│   ├── 提交发现线索
│   ├── 查看线索列表
│   └── 管理员审核线索
├── 领养宠物管理
│   ├── 添加可领养宠物（管理员）
│   ├── 浏览可领养宠物
│   ├── 查看宠物详情
│   └── 修改宠物信息（管理员）
├── 领养申请管理
│   ├── 提交领养申请
│   ├── 查看申请记录
│   ├── 撤回申请
│   └── 管理员审批申请
├── 回访提醒管理
│   ├── 查看回访提醒列表
│   └── 记录回访结果
└── 统计分析
    ├── 月度统计报表
    └── 仪表盘概览
```

### 1.4 数据需求分析

对功能需求分析的结果进行抽象和提取，绘制数据流图。

宠物走失与领养救助平台的顶层数据流图如图1.4所示。

图1.4 顶层数据流图

```
    ┌──────┐                    ┌─────────────────────┐                    ┌──────────┐
    │普通用户│──走失信息/线索/申请──▶│  宠物走失与领养救助平台 │──审核结果/统计──▶│  管理员   │
    │      │◀──查询结果/状态────│                     │◀──审核操作──────│          │
    └──────┘                    └─────────────────────┘                    └──────────┘
```

宠物走失与领养救助平台的0层数据流图如图1.5所示。

图1.5 0层数据流图

```
    ┌──────┐
    │普通用户│
    └──┬───┘
       │走失信息         ┌──────────────┐
       ├──────────────▶│ 1.0 走失宠物  │──▶ 走失宠物数据
       │               │   信息管理    │
       │线索信息         └──────────────┘
       ├──────────────▶│ 2.0 线索管理  │──▶ 线索数据
       │               └──────────────┘
       │领养申请         ┌──────────────┐
       ├──────────────▶│ 3.0 领养申请  │──▶ 申请数据
       │               │   管理        │
       │               └──────┬───────┘
       │                      │审批操作
       │                      ▼
       │               ┌──────────────┐
       │               │ 4.0 审核管理  │──▶ 审核记录
       │               └──────────────┘
       │
       │查询请求         ┌──────────────┐
       └──────────────▶│ 5.0 统计查询  │──▶ 统计结果
                       └──────────────┘

    ┌──────┐
    │ 管理员│
    └──┬───┘
       │审核操作 ───────▶ 4.0 审核管理
       │宠物管理 ───────▶ 1.0 走失宠物信息管理
       │统计查询 ───────▶ 5.0 统计查询
```

### 1.5 业务规则分析

宠物走失与领养救助平台的业务规则主要包括以下几个方面：

（1）用户信息管理规则

系统中的用户分为普通用户和管理员两种角色。每个用户拥有唯一的用户名和邮箱地址，用于系统登录和身份识别。用户密码采用Argon2算法进行哈希存储，确保密码安全。用户注册时系统自动分配"普通用户"角色，管理员角色由系统预设或由其他管理员分配。

（2）走失宠物信息管理规则

每条走失宠物信息必须关联一个发布用户，记录宠物的种类（猫/狗/鸟/其他）、品种、颜色、性别、年龄描述、走失日期、走失地点和联系方式等基本信息。宠物信息支持多张照片存储，使用PostgreSQL数组类型实现。宠物状态包括"寻找中"（active）、"已找回"（found）和"已关闭"（closed）三种。宠物信息可关联救助站，便于按救助站进行统计分析。

（3）发现线索管理规则

每条线索必须关联一条走失宠物信息和一个上报用户。线索包含发现地点、发现日期、描述信息和照片等。线索状态包括"待审核"（pending）、"已确认"（confirmed）和"已拒绝"（rejected）。只有宠物发布者或管理员可以查看和审核线索。当线索被确认时，可将关联的走失宠物状态更新为"已找回"。

（4）领养宠物信息管理规则

可领养宠物信息由管理员录入和管理，包含宠物基本信息、健康状况、疫苗接种状态、驱虫状态、绝育状态等。宠物领养状态包括"可领养"（available）、"已预留"（reserved）和"已领养"（adopted）。只有状态为"可领养"、已完成疫苗接种和驱虫的宠物才会在前台展示。

（5）领养申请管理规则

每个用户对同一宠物最多保留一条领养申请记录，避免同一用户重复占用审核资源。系统在插入申请前检查宠物是否仍为"可领养"状态，以及是否已存在同一用户对同一宠物的待审核或已通过申请。这些约束通过唯一约束和数据库触发器共同实现，确保数据一致性。领养申请被批准后，系统自动将该宠物状态更新为"已领养"，并自动拒绝该宠物的其他待审核申请。

（6）回访提醒管理规则

当领养申请被批准时，系统自动创建一条30天后的回访提醒记录。回访提醒状态包括"待处理"（pending）、"已完成"（completed）和"逾期"（overdue）。管理员可记录回访结果并更新提醒状态。

（7）统计分析规则

系统提供按月统计功能，统计指标包括：走失上报数量、成功找回数量、找回率、领养申请总数、审批通过数量、领养成功率、线索总数、已确认线索数等。统计结果支持按救助站进行筛选。

---

## 第2章 概念结构设计

### 2.1 确定实体集及属性

本系统一共包含7个实体，分别是用户（User）、走失宠物（LostPet）、发现线索（FoundClue）、可领养宠物（AdoptablePet）、领养申请（AdoptionApplication）、审核记录（ReviewRecord）和回访提醒（VisitReminder）。

各实体及其属性描述如下：

（1）用户实体（User）包含用户编号（user_id）、用户名（username）、邮箱（email）、密码哈希值（hashed_password）、手机号（phone）、头像地址（avatar_url）、角色（role）、是否激活（is_active）、创建时间（created_at）、更新时间（updated_at）等属性。用户实体属性图如图2.1所示。

图2.1 用户实体属性图

```
                    ┌─────────────────────┐
                    │       用户           │
                    │      (User)          │
                    ├─────────────────────┤
                    │ user_id (PK)        │
                    │ username (UNIQUE)    │
                    │ email (UNIQUE)       │
                    │ hashed_password      │
                    │ phone                │
                    │ avatar_url           │
                    │ role                 │
                    │ is_active            │
                    │ created_at           │
                    │ updated_at           │
                    └─────────────────────┘
```

（2）走失宠物实体（LostPet）包含宠物编号（lost_pet_id）、发布用户编号（user_id）、宠物名称（pet_name）、宠物种类（pet_type）、品种（breed）、颜色（color）、性别（gender）、年龄描述（age_description）、照片地址（photo_urls）、描述信息（description）、走失日期（lost_date）、走失地点（lost_location）、救助站（rescue_station）、纬度（latitude）、经度（longitude）、联系方式（contact_info）、悬赏金额（reward_amount）、状态（status）、创建时间（created_at）、更新时间（updated_at）等属性。走失宠物实体属性图如图2.2所示。

图2.2 走失宠物实体属性图

```
                    ┌─────────────────────┐
                    │     走失宠物         │
                    │    (LostPet)         │
                    ├─────────────────────┤
                    │ lost_pet_id (PK)    │
                    │ user_id (FK)        │
                    │ pet_name             │
                    │ pet_type             │
                    │ breed                │
                    │ color                │
                    │ gender               │
                    │ age_description      │
                    │ photo_urls[]         │
                    │ description          │
                    │ lost_date            │
                    │ lost_location        │
                    │ rescue_station       │
                    │ latitude             │
                    │ longitude            │
                    │ contact_info         │
                    │ reward_amount        │
                    │ status               │
                    │ created_at           │
                    │ updated_at           │
                    └─────────────────────┘
```

（3）发现线索实体（FoundClue）包含线索编号（found_clue_id）、关联走失宠物编号（lost_pet_id）、上报用户编号（reporter_id）、照片地址（photo_urls）、描述信息（description）、发现地点（found_location）、纬度（latitude）、经度（longitude）、发现日期（found_date）、联系方式（contact_info）、状态（status）、管理员备注（admin_notes）、审核人编号（reviewed_by）、审核时间（reviewed_at）、创建时间（created_at）等属性。发现线索实体属性图如图2.3所示。

图2.3 发现线索实体属性图

```
                    ┌─────────────────────┐
                    │     发现线索         │
                    │   (FoundClue)        │
                    ├─────────────────────┤
                    │ found_clue_id (PK)  │
                    │ lost_pet_id (FK)    │
                    │ reporter_id (FK)    │
                    │ photo_urls[]         │
                    │ description          │
                    │ found_location       │
                    │ latitude             │
                    │ longitude            │
                    │ found_date           │
                    │ contact_info         │
                    │ status               │
                    │ admin_notes          │
                    │ reviewed_by (FK)     │
                    │ reviewed_at          │
                    │ created_at           │
                    └─────────────────────┘
```

（4）可领养宠物实体（AdoptablePet）包含宠物编号（adoptable_pet_id）、宠物名称（pet_name）、宠物种类（pet_type）、品种（breed）、颜色（color）、性别（gender）、月龄（age_months）、照片地址（photo_urls）、描述信息（description）、健康状况（health_status）、是否已接种疫苗（is_vaccinated）、是否已驱虫（is_dewormed）、是否已绝育（is_sterilized）、领养状态（adoption_status）、救助站（rescue_station）、入站日期（intake_date）、创建时间（created_at）、更新时间（updated_at）等属性。可领养宠物实体属性图如图2.4所示。

图2.4 可领养宠物实体属性图

```
                    ┌─────────────────────┐
                    │    可领养宠物        │
                    │  (AdoptablePet)      │
                    ├─────────────────────┤
                    │ adoptable_pet_id(PK)│
                    │ pet_name             │
                    │ pet_type             │
                    │ breed                │
                    │ color                │
                    │ gender               │
                    │ age_months           │
                    │ photo_urls[]         │
                    │ description          │
                    │ health_status        │
                    │ is_vaccinated        │
                    │ is_dewormed          │
                    │ is_sterilized        │
                    │ adoption_status      │
                    │ rescue_station       │
                    │ intake_date          │
                    │ created_at           │
                    │ updated_at           │
                    └─────────────────────┘
```

（5）领养申请实体（AdoptionApplication）包含申请编号（application_id）、可领养宠物编号（adoptable_pet_id）、申请人编号（applicant_id）、申请人姓名（applicant_name）、申请人电话（applicant_phone）、申请人地址（applicant_address）、申请人身份证号（applicant_id_number）、住房类型（housing_type）、是否饲养其他宠物（has_other_pets）、领养原因（adoption_reason）、养宠经验描述（experience_description）、状态（status）、创建时间（created_at）、更新时间（updated_at）等属性。领养申请实体属性图如图2.5所示。

图2.5 领养申请实体属性图

```
                    ┌─────────────────────┐
                    │     领养申请         │
                    │(AdoptionApplication) │
                    ├─────────────────────┤
                    │ application_id (PK) │
                    │ adoptable_pet_id(FK)│
                    │ applicant_id (FK)   │
                    │ applicant_name       │
                    │ applicant_phone      │
                    │ applicant_address    │
                    │ applicant_id_number  │
                    │ housing_type         │
                    │ has_other_pets       │
                    │ adoption_reason      │
                    │ experience_description│
                    │ status               │
                    │ created_at           │
                    │ updated_at           │
                    └─────────────────────┘
```

（6）审核记录实体（ReviewRecord）包含记录编号（review_record_id）、申请编号（application_id）、审核人编号（reviewer_id）、审核决定（decision）、审核备注（review_notes）、审核时间（reviewed_at）等属性。

（7）回访提醒实体（VisitReminder）包含提醒编号（reminder_id）、申请编号（application_id）、领养人编号（adopter_id）、可领养宠物编号（adoptable_pet_id）、提醒日期（reminder_date）、回访日期（visit_date）、状态（status）、回访备注（visit_notes）、创建时间（created_at）等属性。

### 2.2 确定联系集及属性

系统中各实体之间的联系描述如下：

（1）用户与走失宠物之间：一对多联系（1:N）。一个用户可以发布多条走失宠物信息，每条走失宠物信息只属于一个用户。

（2）用户与发现线索之间：一对多联系（1:N）。一个用户可以提交多条发现线索，每条线索只属于一个上报用户。

（3）走失宠物与发现线索之间：一对多联系（1:N）。一条走失宠物信息可以有多条发现线索，每条线索只关联一条走失宠物信息。

（4）用户与领养申请之间：一对多联系（1:N）。一个用户可以提交多个领养申请，每个领养申请只属于一个申请人。

（5）可领养宠物与领养申请之间：一对多联系（1:N）。一个可领养宠物可以收到多个领养申请，每个领养申请只针对一个宠物。

（6）领养申请与审核记录之间：一对多联系（1:N）。一个领养申请可以有多条审核记录，每条审核记录只关联一个申请。

（7）领养申请与回访提醒之间：一对多联系（1:N）。一个领养申请可以有多条回访提醒，每条提醒只关联一个申请。

（8）用户与审核记录之间：一对多联系（1:N）。一个管理员用户可以创建多条审核记录，每条审核记录只关联一个审核人。

### 2.3 绘制局部E-R图

走失宠物管理模块的局部E-R图如图2.6所示。

图2.6 走失宠物管理模块局部E-R图

```
    ┌────────┐     发布      ┌────────────┐     关联      ┌────────────┐
    │  用户   │────────────▶│  走失宠物   │◀────────────│  发现线索   │
    │ (User)  │  1      N   │ (LostPet)   │  1      N   │(FoundClue) │
    └────────┘              └────────────┘              └─────┬──────┘
         │                                                    │
         │                 上报                                │
         └────────────────────────────────────────────────────┘
                              1          N
```

领养管理模块的局部E-R图如图2.7所示。

图2.7 领养管理模块局部E-R图

```
    ┌────────┐     提交申请    ┌────────────┐     针对     ┌────────────┐
    │  用户   │──────────────▶│  领养申请   │◀────────────│ 可领养宠物  │
    │ (User)  │  1        N   │(Application)│  N      1   │(Adoptable) │
    └────────┘                └──────┬─────┘              └────────────┘
                                     │
                         ┌───────────┼───────────┐
                         │ 1         │ N         │ 1
                         ▼           ▼           ▼
                  ┌────────────┐         ┌────────────┐
                  │ 审核记录   │         │ 回访提醒   │
                  │(ReviewRec) │         │(VisitRem)  │
                  └─────┬──────┘         └────────────┘
                        │
                        │ 审核人
                        ▼
                  ┌────────────┐
                  │   用户     │
                  │ (Admin)    │
                  └────────────┘
```

### 2.4 绘制全局E-R图

将上述局部E-R图进行整合，消除可能存在的命名冲突和属性冲突，得到全局E-R图如图2.8所示。

图2.8 全局E-R图

```
                              ┌────────────┐
                              │   用户      │
                              │  (User)     │
                              └──┬──┬──┬───┘
                 ┌───────────────┘  │  └───────────────┐
                 │ 发布 1:N        │ 上报 1:N          │ 审核 1:N
                 ▼                  ▼                   ▼
          ┌────────────┐    ┌────────────┐      ┌────────────┐
          │  走失宠物   │    │  发现线索   │      │  审核记录   │
          │ (LostPet)   │◀───│(FoundClue) │      │(ReviewRec) │
          └────────────┘ 1:N└────────────┘      └─────┬──────┘
                 ▲  关联 1:N                           │
                                                   N:1│关联
                                                      ▼
                               ┌────────────┐    ┌────────────┐
                               │ 可领养宠物  │    │  领养申请   │
                               │(Adoptable) │◀───│(Application)│
                               └────────────┘ 1:N└──────┬─────┘
                                                        │
                                                     1:N│关联
                                                        ▼
                                                 ┌────────────┐
                                                 │  回访提醒   │
                                                 │(VisitRem)  │
                                                 └────────────┘
```

---

## 第3章 逻辑结构设计

### 3.1 E-R模型转换为关系模型的转换方法

E-R模型向关系模型的转换遵循以下规则：

（1）实体的转换：每个实体转换为一个关系模式，实体的属性转换为关系的属性，实体的主键转换为关系的主键。

（2）联系的转换：
- 1:1联系：将联系并入任一端实体的关系模式中，在该关系中加入另一端实体的主键作为外键。
- 1:N联系：将联系并入N端实体的关系模式中，在N端关系中加入1端实体的主键作为外键。
- M:N联系：为联系创建一个新的关系模式，将两端实体的主键组合作为该关系的主键（或单独设置主键并将两端主键设为外键）。

（3）多值属性的转换：使用PostgreSQL数组类型存储多值属性（如照片地址列表）。

### 3.2 设计初始关系模式

根据E-R图到关系模型的转换规则，设计初始关系模式如下：

（1）用户（用户编号，用户名，邮箱，密码哈希值，手机号，头像地址，角色，是否激活，创建时间，更新时间）

（2）走失宠物（宠物编号，发布用户编号，宠物名称，宠物种类，品种，颜色，性别，年龄描述，照片地址，描述信息，走失日期，走失地点，救助站，纬度，经度，联系方式，悬赏金额，状态，创建时间，更新时间）

（3）发现线索（线索编号，关联宠物编号，上报用户编号，照片地址，描述信息，发现地点，纬度，经度，发现日期，联系方式，状态，管理员备注，审核人编号，审核时间，创建时间）

（4）可领养宠物（宠物编号，宠物名称，宠物种类，品种，颜色，性别，月龄，照片地址，描述信息，健康状况，是否已接种疫苗，是否已驱虫，是否已绝育，领养状态，救助站，入站日期，创建时间，更新时间）

（5）领养申请（申请编号，宠物编号，申请人编号，申请人姓名，申请人电话，申请人地址，申请人身份证号，住房类型，是否饲养其他宠物，领养原因，养宠经验描述，状态，创建时间，更新时间）

（6）审核记录（记录编号，申请编号，审核人编号，审核决定，审核备注，审核时间）

（7）回访提醒（提醒编号，申请编号，领养人编号，宠物编号，提醒日期，回访日期，状态，回访备注，创建时间）

### 3.3 关系模式优化

对初始关系模式进行规范化处理，检查各关系模式是否满足第三范式（3NF）。

（1）用户关系模式：所有非主属性完全依赖于主键用户编号，不存在传递依赖，满足3NF。

（2）走失宠物关系模式：所有非主属性完全依赖于主键宠物编号，发布用户编号为外键引用用户表，不存在传递依赖，满足3NF。

（3）发现线索关系模式：所有非主属性完全依赖于主键线索编号，关联宠物编号和上报用户编号为外键，不存在传递依赖，满足3NF。

（4）可领养宠物关系模式：所有非主属性完全依赖于主键宠物编号，不存在传递依赖，满足3NF。

（5）领养申请关系模式：所有非主属性完全依赖于主键申请编号，宠物编号和申请人编号为外键。设置（宠物编号，申请人编号）为唯一约束，确保同一用户对同一宠物最多保留一条申请记录；同时通过触发器检查宠物是否可领养以及是否存在待审核或已通过的重复申请，满足3NF。

（6）审核记录关系模式：所有非主属性完全依赖于主键记录编号，申请编号和审核人编号为外键，满足3NF。

（7）回访提醒关系模式：所有非主属性完全依赖于主键提醒编号，申请编号、领养人编号和宠物编号为外键，满足3NF。

经过规范化处理，所有关系模式均满足第三范式要求，不存在数据冗余和更新异常问题。

---

## 第4章 物理结构设计

本系统使用PostgreSQL 16作为数据库管理系统，创建了名为lost_pet_db的数据库。PostgreSQL是一款功能强大的开源对象关系数据库系统，支持丰富的数据类型（如数组、JSON等）、高级SQL特性（如窗口函数、CTE等）以及存储过程和触发器等数据库对象，非常适合本系统的数据存储需求。

在该数据库中计划创建7张数据表，每张表的表结构设计情况如下：

（1）用户表（users）的表结构如表4.1所示：

表4.1 users表结构

| 字段 | 数据类型 | PK | FK | 是否为空 | 其他约束 | 说明 |
|------|----------|----|----|----------|----------|------|
| user_id | UUID | 是 |  | 否 | 默认gen_random_uuid() | 用户编号 |
| username | VARCHAR(50) |  |  | 否 | UNIQUE | 用户名 |
| email | VARCHAR(100) |  |  | 否 | UNIQUE | 邮箱 |
| hashed_password | VARCHAR(255) |  |  | 否 |  | 密码哈希值 |
| phone | VARCHAR(20) |  |  | 是 |  | 手机号 |
| avatar_url | VARCHAR(500) |  |  | 是 |  | 头像地址 |
| role | VARCHAR(20) |  |  | 否 | 默认'user' | 角色 |
| is_active | BOOLEAN |  |  | 否 | 默认true | 是否激活 |
| created_at | TIMESTAMPTZ |  |  | 否 | 默认now() | 创建时间 |
| updated_at | TIMESTAMPTZ |  |  | 否 | 默认now() | 更新时间 |

（2）走失宠物表（lost_pets）的表结构如表4.2所示：

表4.2 lost_pets表结构

| 字段 | 数据类型 | PK | FK | 是否为空 | 其他约束 | 说明 |
|------|----------|----|----|----------|----------|------|
| lost_pet_id | UUID | 是 |  | 否 | 默认gen_random_uuid() | 宠物编号 |
| user_id | UUID |  | users.user_id | 否 |  | 发布用户编号 |
| pet_name | VARCHAR(50) |  |  | 否 |  | 宠物名称 |
| pet_type | VARCHAR(20) |  |  | 否 |  | 宠物种类 |
| breed | VARCHAR(50) |  |  | 是 |  | 品种 |
| color | VARCHAR(30) |  |  | 是 |  | 颜色 |
| gender | VARCHAR(10) |  |  | 是 |  | 性别 |
| age_description | VARCHAR(50) |  |  | 是 |  | 年龄描述 |
| photo_urls | VARCHAR[] |  |  | 是 |  | 照片地址（数组） |
| description | TEXT |  |  | 否 |  | 描述信息 |
| lost_date | DATE |  |  | 否 |  | 走失日期 |
| lost_location | VARCHAR(255) |  |  | 否 |  | 走失地点 |
| rescue_station | VARCHAR(100) |  |  | 是 |  | 救助站 |
| latitude | NUMERIC(10,7) |  |  | 是 |  | 纬度 |
| longitude | NUMERIC(10,7) |  |  | 是 |  | 经度 |
| contact_info | VARCHAR(100) |  |  | 否 |  | 联系方式 |
| reward_amount | NUMERIC(10,2) |  |  | 是 | 默认0 | 悬赏金额 |
| status | VARCHAR(20) |  |  | 否 | 默认'active' | 状态 |
| created_at | TIMESTAMPTZ |  |  | 否 | 默认now() | 创建时间 |
| updated_at | TIMESTAMPTZ |  |  | 否 | 默认now() | 更新时间 |

（3）发现线索表（found_clues）的表结构如表4.3所示：

表4.3 found_clues表结构

| 字段 | 数据类型 | PK | FK | 是否为空 | 其他约束 | 说明 |
|------|----------|----|----|----------|----------|------|
| found_clue_id | UUID | 是 |  | 否 | 默认gen_random_uuid() | 线索编号 |
| lost_pet_id | UUID |  | lost_pets.lost_pet_id | 否 |  | 关联宠物编号 |
| reporter_id | UUID |  | users.user_id | 否 |  | 上报用户编号 |
| photo_urls | VARCHAR[] |  |  | 是 |  | 照片地址（数组） |
| description | TEXT |  |  | 否 |  | 描述信息 |
| found_location | VARCHAR(255) |  |  | 否 |  | 发现地点 |
| latitude | NUMERIC(10,7) |  |  | 是 |  | 纬度 |
| longitude | NUMERIC(10,7) |  |  | 是 |  | 经度 |
| found_date | DATE |  |  | 否 |  | 发现日期 |
| contact_info | VARCHAR(100) |  |  | 否 |  | 联系方式 |
| status | VARCHAR(20) |  |  | 否 | 默认'pending' | 状态 |
| admin_notes | TEXT |  |  | 是 |  | 管理员备注 |
| reviewed_by | UUID |  | users.user_id | 是 |  | 审核人编号 |
| reviewed_at | TIMESTAMPTZ |  |  | 是 |  | 审核时间 |
| created_at | TIMESTAMPTZ |  |  | 否 | 默认now() | 创建时间 |

（4）可领养宠物表（adoptable_pets）的表结构如表4.4所示：

表4.4 adoptable_pets表结构

| 字段 | 数据类型 | PK | FK | 是否为空 | 其他约束 | 说明 |
|------|----------|----|----|----------|----------|------|
| adoptable_pet_id | UUID | 是 |  | 否 | 默认gen_random_uuid() | 宠物编号 |
| pet_name | VARCHAR(50) |  |  | 否 |  | 宠物名称 |
| pet_type | VARCHAR(20) |  |  | 否 |  | 宠物种类 |
| breed | VARCHAR(50) |  |  | 是 |  | 品种 |
| color | VARCHAR(30) |  |  | 是 |  | 颜色 |
| gender | VARCHAR(10) |  |  | 是 |  | 性别 |
| age_months | INTEGER |  |  | 是 |  | 月龄 |
| photo_urls | VARCHAR[] |  |  | 是 |  | 照片地址（数组） |
| description | TEXT |  |  | 是 |  | 描述信息 |
| health_status | VARCHAR(20) |  |  | 否 | 默认'healthy' | 健康状况 |
| is_vaccinated | BOOLEAN |  |  | 否 | 默认false | 是否已接种疫苗 |
| is_dewormed | BOOLEAN |  |  | 否 | 默认false | 是否已驱虫 |
| is_sterilized | BOOLEAN |  |  | 否 | 默认false | 是否已绝育 |
| adoption_status | VARCHAR(20) |  |  | 否 | 默认'available' | 领养状态 |
| rescue_station | VARCHAR(100) |  |  | 是 |  | 救助站 |
| intake_date | DATE |  |  | 否 |  | 入站日期 |
| created_at | TIMESTAMPTZ |  |  | 否 | 默认now() | 创建时间 |
| updated_at | TIMESTAMPTZ |  |  | 否 | 默认now() | 更新时间 |

（5）领养申请表（adoption_applications）的表结构如表4.5所示：

表4.5 adoption_applications表结构

| 字段 | 数据类型 | PK | FK | 是否为空 | 其他约束 | 说明 |
|------|----------|----|----|----------|----------|------|
| application_id | UUID | 是 |  | 否 | 默认gen_random_uuid() | 申请编号 |
| adoptable_pet_id | UUID |  | adoptable_pets.adoptable_pet_id | 否 |  | 可领养宠物编号 |
| applicant_id | UUID |  | users.user_id | 否 |  | 申请人编号 |
| applicant_name | VARCHAR(50) |  |  | 否 |  | 申请人姓名 |
| applicant_phone | VARCHAR(20) |  |  | 否 |  | 申请人电话 |
| applicant_address | VARCHAR(255) |  |  | 否 |  | 申请人地址 |
| applicant_id_number | VARCHAR(20) |  |  | 否 |  | 身份证号 |
| housing_type | VARCHAR(20) |  |  | 是 |  | 住房类型 |
| has_other_pets | BOOLEAN |  |  | 是 | 默认false | 是否有其他宠物 |
| adoption_reason | TEXT |  |  | 否 |  | 领养原因 |
| experience_description | TEXT |  |  | 是 |  | 养宠经验 |
| status | VARCHAR(20) |  |  | 否 | 默认'pending' | 状态 |
| created_at | TIMESTAMPTZ |  |  | 否 | 默认now() | 创建时间 |
| updated_at | TIMESTAMPTZ |  |  | 否 | 默认now() | 更新时间 |

（6）审核记录表（review_records）的表结构如表4.6所示：

表4.6 review_records表结构

| 字段 | 数据类型 | PK | FK | 是否为空 | 其他约束 | 说明 |
|------|----------|----|----|----------|----------|------|
| review_record_id | UUID | 是 |  | 否 | 默认gen_random_uuid() | 记录编号 |
| application_id | UUID |  | adoption_applications.application_id | 否 |  | 申请编号 |
| reviewer_id | UUID |  | users.user_id | 否 |  | 审核人编号 |
| decision | VARCHAR(20) |  |  | 否 |  | 审核决定 |
| review_notes | TEXT |  |  | 是 |  | 审核备注 |
| reviewed_at | TIMESTAMPTZ |  |  | 否 | 默认now() | 审核时间 |

（7）回访提醒表（visit_reminders）的表结构如表4.7所示：

表4.7 visit_reminders表结构

| 字段 | 数据类型 | PK | FK | 是否为空 | 其他约束 | 说明 |
|------|----------|----|----|----------|----------|------|
| reminder_id | UUID | 是 |  | 否 | 默认gen_random_uuid() | 提醒编号 |
| application_id | UUID |  | adoption_applications.application_id | 否 |  | 申请编号 |
| adopter_id | UUID |  | users.user_id | 否 |  | 领养人编号 |
| adoptable_pet_id | UUID |  | adoptable_pets.adoptable_pet_id | 否 |  | 可领养宠物编号 |
| reminder_date | DATE |  |  | 否 |  | 提醒日期 |
| visit_date | DATE |  |  | 是 |  | 回访日期 |
| status | VARCHAR(20) |  |  | 否 | 默认'pending' | 状态 |
| visit_notes | TEXT |  |  | 是 |  | 回访备注 |
| created_at | TIMESTAMPTZ |  |  | 否 | 默认now() | 创建时间 |

索引设计策略：为提高查询性能，在以下字段上创建了索引：

- lost_pets表：user_id、status、lost_date、rescue_station
- found_clues表：lost_pet_id、reporter_id
- adoptable_pets表：pet_type、adoption_status、rescue_station
- adoption_applications表：adoptable_pet_id、applicant_id、status
- visit_reminders表：reminder_date、status

---

## 第5章 数据库实施

### 5.1 定义数据库对象

#### 5.1.1 定义数据库

在PostgreSQL中创建名为lost_pet_db的数据库，创建代码如下：

```sql
CREATE DATABASE lost_pet_db
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;
```

#### 5.1.2 定义数据表

结合物理结构设计章节中表结构的设计情况，在名为lost_pet_db的数据库中使用SQL语句创建了7张数据表。

（1）用户表（users）的创建代码如下：

```sql
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    avatar_url VARCHAR(500),
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

（2）走失宠物表（lost_pets）的创建代码如下：

```sql
CREATE TABLE lost_pets (
    lost_pet_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id),
    pet_name VARCHAR(50) NOT NULL,
    pet_type VARCHAR(20) NOT NULL,
    breed VARCHAR(50),
    color VARCHAR(30),
    gender VARCHAR(10),
    age_description VARCHAR(50),
    photo_urls VARCHAR[],
    description TEXT NOT NULL,
    lost_date DATE NOT NULL,
    lost_location VARCHAR(255) NOT NULL,
    rescue_station VARCHAR(100),
    latitude NUMERIC(10, 7),
    longitude NUMERIC(10, 7),
    contact_info VARCHAR(100) NOT NULL,
    reward_amount NUMERIC(10, 2) DEFAULT 0,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

（3）发现线索表（found_clues）的创建代码如下：

```sql
CREATE TABLE found_clues (
    found_clue_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lost_pet_id UUID NOT NULL REFERENCES lost_pets(lost_pet_id),
    reporter_id UUID NOT NULL REFERENCES users(user_id),
    photo_urls VARCHAR[],
    description TEXT NOT NULL,
    found_location VARCHAR(255) NOT NULL,
    latitude NUMERIC(10, 7),
    longitude NUMERIC(10, 7),
    found_date DATE NOT NULL,
    contact_info VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    admin_notes TEXT,
    reviewed_by UUID REFERENCES users(user_id),
    reviewed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

（4）可领养宠物表（adoptable_pets）的创建代码如下：

```sql
CREATE TABLE adoptable_pets (
    adoptable_pet_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pet_name VARCHAR(50) NOT NULL,
    pet_type VARCHAR(20) NOT NULL,
    breed VARCHAR(50),
    color VARCHAR(30),
    gender VARCHAR(10),
    age_months INTEGER,
    photo_urls VARCHAR[],
    description TEXT,
    health_status VARCHAR(20) NOT NULL DEFAULT 'healthy',
    is_vaccinated BOOLEAN NOT NULL DEFAULT false,
    is_dewormed BOOLEAN NOT NULL DEFAULT false,
    is_sterilized BOOLEAN NOT NULL DEFAULT false,
    adoption_status VARCHAR(20) NOT NULL DEFAULT 'available',
    rescue_station VARCHAR(100),
    intake_date DATE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

（5）领养申请表（adoption_applications）的创建代码如下：

```sql
CREATE TABLE adoption_applications (
    application_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    adoptable_pet_id UUID NOT NULL REFERENCES adoptable_pets(adoptable_pet_id),
    applicant_id UUID NOT NULL REFERENCES users(user_id),
    applicant_name VARCHAR(50) NOT NULL,
    applicant_phone VARCHAR(20) NOT NULL,
    applicant_address VARCHAR(255) NOT NULL,
    applicant_id_number VARCHAR(20) NOT NULL,
    housing_type VARCHAR(20),
    has_other_pets BOOLEAN DEFAULT false,
    adoption_reason TEXT NOT NULL,
    experience_description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (adoptable_pet_id, applicant_id)
);
```

（6）审核记录表（review_records）的创建代码如下：

```sql
CREATE TABLE review_records (
    review_record_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    application_id UUID NOT NULL REFERENCES adoption_applications(application_id),
    reviewer_id UUID NOT NULL REFERENCES users(user_id),
    decision VARCHAR(20) NOT NULL,
    review_notes TEXT,
    reviewed_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

（7）回访提醒表（visit_reminders）的创建代码如下：

```sql
CREATE TABLE visit_reminders (
    reminder_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    application_id UUID NOT NULL REFERENCES adoption_applications(application_id),
    adopter_id UUID NOT NULL REFERENCES users(user_id),
    adoptable_pet_id UUID NOT NULL REFERENCES adoptable_pets(adoptable_pet_id),
    reminder_date DATE NOT NULL,
    visit_date DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    visit_notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

除数据表以外，结合物理结构设计中的索引策略，创建以下索引以提高常用筛选、关联和统计查询的执行效率：

```sql
CREATE INDEX idx_lost_pets_user_id ON lost_pets(user_id);
CREATE INDEX idx_lost_pets_status ON lost_pets(status);
CREATE INDEX idx_lost_pets_lost_date ON lost_pets(lost_date);
CREATE INDEX idx_lost_pets_rescue_station ON lost_pets(rescue_station);

CREATE INDEX idx_found_clues_lost_pet_id ON found_clues(lost_pet_id);
CREATE INDEX idx_found_clues_reporter_id ON found_clues(reporter_id);

CREATE INDEX idx_adoptable_pets_type ON adoptable_pets(pet_type);
CREATE INDEX idx_adoptable_pets_status ON adoptable_pets(adoption_status);
CREATE INDEX idx_adoptable_pets_rescue_station ON adoptable_pets(rescue_station);

CREATE INDEX idx_adoption_applications_adoptable_pet_id ON adoption_applications(adoptable_pet_id);
CREATE INDEX idx_adoption_applications_applicant_id ON adoption_applications(applicant_id);
CREATE INDEX idx_adoption_applications_status ON adoption_applications(status);

CREATE INDEX idx_visit_reminders_reminder_date ON visit_reminders(reminder_date);
CREATE INDEX idx_visit_reminders_status ON visit_reminders(status);
```

### 5.2 数据操作

#### 5.2.1 插入数据

为用户、走失宠物、发现线索、可领养宠物、领养申请等主要业务表插入初始测试数据，用于后续查询、更新、删除和触发器验证。

（1）用户表数据插入：

```sql
INSERT INTO users (username, email, hashed_password, phone, role) VALUES
('admin', 'admin@example.com', '$argon2id$v=19$m=65536,t=3,p=4$hash...', '13800000001', 'admin'),
('zhangsan', 'zhangsan@example.com', '$argon2id$v=19$m=65536,t=3,p=4$hash...', '13800000002', 'user'),
('lisi', 'lisi@example.com', '$argon2id$v=19$m=65536,t=3,p=4$hash...', '13800000003', 'user'),
('wangwu', 'wangwu@example.com', '$argon2id$v=19$m=65536,t=3,p=4$hash...', '13800000004', 'user'),
('zhaoliu', 'zhaoliu@example.com', '$argon2id$v=19$m=65536,t=3,p=4$hash...', '13800000005', 'user'),
('sunqi', 'sunqi@example.com', '$argon2id$v=19$m=65536,t=3,p=4$hash...', '13800000006', 'user'),
('zhouba', 'zhouba@example.com', '$argon2id$v=19$m=65536,t=3,p=4$hash...', '13800000007', 'user'),
('wujiu', 'wujiu@example.com', '$argon2id$v=19$m=65536,t=3,p=4$hash...', '13800000008', 'user');
```

（2）走失宠物表数据插入：

```sql
INSERT INTO lost_pets (user_id, pet_name, pet_type, breed, color, gender, age_description, description, lost_date, lost_location, contact_info, status) VALUES
((SELECT user_id FROM users WHERE username='zhangsan'), '豆豆', 'dog', '金毛寻回犬', '金色', 'male', '3岁', '性格温顺，走失时佩戴蓝色项圈', '2026-05-01', '广州市天河区体育中心附近', '13800000002', 'active'),
((SELECT user_id FROM users WHERE username='lisi'), '咪咪', 'cat', '英国短毛猫', '灰色', 'female', '2岁', '比较怕生，左耳有缺口', '2026-05-05', '深圳市南山区科技园', '13800000003', 'active'),
((SELECT user_id FROM users WHERE username='wangwu'), '小白', 'dog', '萨摩耶', '白色', 'male', '1岁', '非常活泼，右前腿有白色标记', '2026-05-10', '佛山市禅城区祖庙', '13800000004', 'found'),
((SELECT user_id FROM users WHERE username='zhangsan'), '花花', 'cat', '中华田园猫', '黑白花', 'female', '4岁', '已绝育，佩戴红色铃铛', '2026-05-12', '广州市越秀区北京路', '13800000002', 'active'),
((SELECT user_id FROM users WHERE username='zhaoliu'), '旺财', 'dog', '拉布拉多', '黑色', 'male', '5岁', '会握手，走失时穿橙色衣服', '2026-05-15', '东莞市东城区万达广场', '13800000005', 'active'),
((SELECT user_id FROM users WHERE username='sunqi'), '小黄', 'bird', '虎皮鹦鹉', '黄绿色', 'unknown', '1岁', '会说"你好"，脚上有编号环', '2026-05-18', '珠海市香洲区情侣路', '13800000006', 'active'),
((SELECT user_id FROM users WHERE username='lisi'), '球球', 'dog', '柯基', '黄白色', 'female', '2岁', '短腿，尾巴很短', '2026-05-20', '广州市番禺区大学城', '13800000003', 'closed'),
((SELECT user_id FROM users WHERE username='wangwu'), '大橘', 'cat', '中华田园猫', '橘色', 'male', '6岁', '体型较大，非常亲人', '2026-05-22', '深圳市福田区莲花山公园', '13800000004', 'active');
```

（3）发现线索表数据插入：

```sql
INSERT INTO found_clues (lost_pet_id, reporter_id, description, found_location, found_date, contact_info, status) VALUES
((SELECT lost_pet_id FROM lost_pets WHERE pet_name='豆豆'), (SELECT user_id FROM users WHERE username='lisi'), '在天河公园看到一只金色大狗，与描述相似', '广州市天河区天河公园东门', '2026-05-03', '13800000003', 'confirmed'),
((SELECT lost_pet_id FROM lost_pets WHERE pet_name='豆豆'), (SELECT user_id FROM users WHERE username='wangwu'), '体育西路地铁站附近看到类似狗狗', '广州市天河区体育西路', '2026-05-04', '13800000004', 'rejected'),
((SELECT lost_pet_id FROM lost_pets WHERE pet_name='咪咪'), (SELECT user_id FROM users WHERE username='zhangsan'), '科技园B栋楼下有一只灰色猫', '深圳市南山区科技园B栋', '2026-05-07', '13800000002', 'pending'),
((SELECT lost_pet_id FROM lost_pets WHERE pet_name='小白'), (SELECT user_id FROM users WHERE username='zhaoliu'), '在祖庙附近的宠物店看到一只白色萨摩耶', '佛山市禅城区祖庙路宠物店', '2026-05-11', '13800000005', 'confirmed'),
((SELECT lost_pet_id FROM lost_pets WHERE pet_name='花花'), (SELECT user_id FROM users WHERE username='sunqi'), '北京路步行街有一只黑白花猫在觅食', '广州市越秀区北京路步行街', '2026-05-14', '13800000006', 'pending'),
((SELECT lost_pet_id FROM lost_pets WHERE pet_name='旺财'), (SELECT user_id FROM users WHERE username='zhouba'), '万达广场停车场看到一只黑色拉布拉多', '东莞市东城区万达广场B2停车场', '2026-05-16', '13800000007', 'pending'),
((SELECT lost_pet_id FROM lost_pets WHERE pet_name='小黄'), (SELECT user_id FROM users WHERE username='wujiu'), '情侣路海边有一只黄绿色鹦鹉在树上', '珠海市香洲区情侣路海边', '2026-05-19', '13800000008', 'confirmed'),
((SELECT lost_pet_id FROM lost_pets WHERE pet_name='大橘'), (SELECT user_id FROM users WHERE username='zhangsan'), '莲花山公园草坪上有一只大橘猫', '深圳市福田区莲花山公园草坪', '2026-05-23', '13800000002', 'pending');
```

（4）可领养宠物表数据插入：

```sql
INSERT INTO adoptable_pets (pet_name, pet_type, breed, color, gender, age_months, description, health_status, is_vaccinated, is_dewormed, is_sterilized, rescue_station, intake_date) VALUES
('团团', 'cat', '布偶猫', '白色', 'female', 18, '性格温顺，喜欢撒娇', 'healthy', true, true, true, '广州市小动物救助中心', '2026-01-15'),
('圆圆', 'dog', '比熊', '白色', 'male', 24, '活泼好动，已训练基本指令', 'healthy', true, true, false, '广州市小动物救助中心', '2026-02-01'),
('小花', 'cat', '中华田园猫', '三花', 'female', 12, '亲人，适合家庭饲养', 'healthy', true, true, true, '深圳市流浪动物救助站', '2026-02-20'),
('大黄', 'dog', '中华田园犬', '黄色', 'male', 36, '忠诚护主，需要有经验的主人', 'treating', true, true, false, '深圳市流浪动物救助站', '2026-03-01'),
('雪球', 'cat', '波斯猫', '白色', 'female', 24, '安静优雅，适合公寓饲养', 'healthy', true, true, true, '佛山市宠物之家', '2026-03-10'),
('黑豆', 'dog', '拉布拉多', '黑色', 'male', 30, '温顺友善，适合有孩子的家庭', 'healthy', true, true, true, '佛山市宠物之家', '2026-03-15'),
('奶茶', 'cat', '英国短毛猫', '乳白色', 'female', 15, '独立性强，不需要太多陪伴', 'healthy', true, true, false, '广州市小动物救助中心', '2026-04-01'),
('旺仔', 'dog', '泰迪', '棕色', 'male', 20, '聪明伶俐，学会了很多小把戏', 'chronic', true, true, true, '深圳市流浪动物救助站', '2026-04-10');
```

（5）领养申请表数据插入：

```sql
INSERT INTO adoption_applications (adoptable_pet_id, applicant_id, applicant_name, applicant_phone, applicant_address, applicant_id_number, housing_type, has_other_pets, adoption_reason, experience_description, status) VALUES
((SELECT adoptable_pet_id FROM adoptable_pets WHERE pet_name='团团'), (SELECT user_id FROM users WHERE username='zhangsan'), '张三', '13800000002', '广州市天河区XX路XX号', '440100199001011234', 'apartment', false, '非常喜欢布偶猫，家里环境适合养猫', '之前养过一只英短，有3年养猫经验', 'pending'),
((SELECT adoptable_pet_id FROM adoptable_pets WHERE pet_name='团团'), (SELECT user_id FROM users WHERE username='lisi'), '李四', '13800000003', '广州市番禺区XX路XX号', '440100199002022345', 'house', true, '想给家里的猫咪找个伴', '有5年养猫经验，家中目前有一只橘猫', 'pending'),
((SELECT adoptable_pet_id FROM adoptable_pets WHERE pet_name='圆圆'), (SELECT user_id FROM users WHERE username='wangwu'), '王五', '13800000004', '佛山市禅城区XX路XX号', '440100199003033456', 'house', false, '一直想养一只比熊，家里有院子', '之前养过金毛，熟悉犬类护理', 'pending'),
((SELECT adoptable_pet_id FROM adoptable_pets WHERE pet_name='小花'), (SELECT user_id FROM users WHERE username='zhaoliu'), '赵六', '13800000005', '东莞市XX区XX路XX号', '440100199004044567', 'apartment', false, '喜欢中华田园猫，想给流浪猫一个家', '无养宠经验，但已学习相关知识', 'pending'),
((SELECT adoptable_pet_id FROM adoptable_pets WHERE pet_name='小花'), (SELECT user_id FROM users WHERE username='sunqi'), '孙七', '13800000006', '珠海市XX区XX路XX号', '440100199005055678', 'apartment', true, '想给家里增加一个新成员', '养过两只猫，有丰富经验', 'rejected'),
((SELECT adoptable_pet_id FROM adoptable_pets WHERE pet_name='雪球'), (SELECT user_id FROM users WHERE username='zhouba'), '周八', '13800000007', '广州市XX区XX路XX号', '440100199006066789', 'apartment', false, '一直很喜欢波斯猫', '有2年养猫经验', 'pending'),
((SELECT adoptable_pet_id FROM adoptable_pets WHERE pet_name='黑豆'), (SELECT user_id FROM users WHERE username='wujiu'), '吴九', '13800000008', '深圳市XX区XX路XX号', '440100199007077890', 'house', false, '家里空间大，适合养大型犬', '有8年养犬经验', 'pending'),
((SELECT adoptable_pet_id FROM adoptable_pets WHERE pet_name='奶茶'), (SELECT user_id FROM users WHERE username='zhangsan'), '张三', '13800000002', '广州市天河区XX路XX号', '440100199001011234', 'apartment', false, '英短很适合公寓饲养', '之前养过英短，有经验', 'pending');
```

#### 5.2.2 修改数据

（1）将走失宠物"豆豆"的状态更新为"已找回"：

```sql
UPDATE lost_pets SET status = 'found' WHERE pet_name = '豆豆';
```

（2）将可领养宠物"团团"的领养状态更新为"已预留"：

```sql
UPDATE adoptable_pets SET adoption_status = 'reserved' WHERE pet_name = '团团';
```

（3）更新用户的手机号：

```sql
UPDATE users SET phone = '13900000002' WHERE username = 'zhangsan';
```

#### 5.2.3 删除数据

（1）删除一条被拒绝的发现线索：

```sql
DELETE FROM found_clues
WHERE found_clue_id = (
    SELECT found_clue_id FROM found_clues WHERE status = 'rejected' LIMIT 1
);
```

（2）删除一条已关闭的走失宠物信息：

```sql
DELETE FROM lost_pets WHERE pet_name = '球球' AND status = 'closed';
```

#### 5.2.4 查询数据

（1）单表查询：查询所有状态为"寻找中"的走失宠物信息

```sql
SELECT pet_name, pet_type, breed, lost_date, lost_location, contact_info
FROM lost_pets
WHERE status = 'active'
ORDER BY created_at DESC;
```

查询结果：

| pet_name | pet_type | breed | lost_date | lost_location | contact_info |
|----------|----------|-------|-----------|---------------|--------------|
| 大橘 | cat | 中华田园猫 | 2026-05-22 | 深圳市福田区莲花山公园 | 13800000004 |
| 小黄 | bird | 虎皮鹦鹉 | 2026-05-18 | 珠海市香洲区情侣路 | 13800000006 |
| 旺财 | dog | 拉布拉多 | 2026-05-15 | 东莞市东城区万达广场 | 13800000005 |
| 花花 | cat | 中华田园猫 | 2026-05-12 | 广州市越秀区北京路 | 13800000002 |
| 咪咪 | cat | 英国短毛猫 | 2026-05-05 | 深圳市南山区科技园 | 13800000003 |

（2）多表查询：查询每条走失宠物信息及其线索数量

```sql
SELECT lp.pet_name, lp.pet_type, lp.lost_location, lp.status,
       COUNT(fc.found_clue_id) AS clue_count
FROM lost_pets lp
LEFT JOIN found_clues fc ON lp.lost_pet_id = fc.lost_pet_id
GROUP BY lp.lost_pet_id, lp.pet_name, lp.pet_type, lp.lost_location, lp.status
ORDER BY clue_count DESC;
```

查询结果：

| pet_name | pet_type | lost_location | status | clue_count |
|----------|----------|---------------|--------|------------|
| 豆豆 | dog | 广州市天河区体育中心附近 | found | 1 |
| 咪咪 | cat | 深圳市南山区科技园 | active | 1 |
| 小白 | dog | 佛山市禅城区祖庙 | found | 1 |
| 花花 | cat | 广州市越秀区北京路 | active | 1 |
| 旺财 | dog | 东莞市东城区万达广场 | active | 1 |
| 小黄 | bird | 珠海市香洲区情侣路 | active | 1 |
| 大橘 | cat | 深圳市福田区莲花山公园 | active | 1 |

（3）嵌套查询：查询有"待审核"领养申请的可领养宠物信息

```sql
SELECT pet_name, pet_type, breed, health_status, rescue_station
FROM adoptable_pets
WHERE adoptable_pet_id IN (
    SELECT adoptable_pet_id FROM adoption_applications WHERE status = 'pending'
)
ORDER BY pet_name;
```

查询结果：

| pet_name | pet_type | breed | health_status | rescue_station |
|----------|----------|-------|---------------|----------------|
| 团团 | cat | 布偶猫 | healthy | 广州市小动物救助中心 |
| 圆圆 | dog | 比熊 | healthy | 广州市小动物救助中心 |
| 小花 | cat | 中华田园猫 | healthy | 深圳市流浪动物救助站 |
| 奶茶 | cat | 英国短毛猫 | healthy | 广州市小动物救助中心 |
| 黑豆 | dog | 拉布拉多 | healthy | 佛山市宠物之家 |
| 雪球 | cat | 波斯猫 | healthy | 佛山市宠物之家 |

（4）带聚合函数的查询：按宠物种类统计走失宠物数量

```sql
SELECT pet_type, COUNT(*) AS total_count,
       COUNT(*) FILTER (WHERE status = 'found') AS found_count,
       ROUND(COUNT(*) FILTER (WHERE status = 'found') * 100.0 / COUNT(*), 2) AS recovery_rate
FROM lost_pets
GROUP BY pet_type
ORDER BY total_count DESC;
```

查询结果：

| pet_type | total_count | found_count | recovery_rate |
|----------|-------------|-------------|---------------|
| dog | 3 | 2 | 66.67 |
| cat | 3 | 0 | 0.00 |
| bird | 1 | 0 | 0.00 |

### 5.3 创建视图

创建视图v_adoptable_pets，查询当前所有待领养宠物（已驱虫/已疫苗）的详细信息及所在救助站：

```sql
CREATE OR REPLACE VIEW v_adoptable_pets AS
SELECT
    ap.adoptable_pet_id, ap.pet_name, ap.pet_type, ap.breed, ap.color, ap.gender,
    ap.age_months, ap.photo_urls, ap.description, ap.health_status,
    ap.is_vaccinated, ap.is_dewormed, ap.is_sterilized,
    ap.rescue_station, ap.intake_date,
    COALESCE(app_count.application_count, 0) AS application_count
FROM adoptable_pets ap
LEFT JOIN (
    SELECT adoptable_pet_id, COUNT(*) AS application_count
    FROM adoption_applications
    WHERE status = 'pending'
    GROUP BY adoptable_pet_id
) app_count ON ap.adoptable_pet_id = app_count.adoptable_pet_id
WHERE ap.adoption_status = 'available'
  AND ap.is_vaccinated = true
  AND ap.is_dewormed = true;
```

该视图的作用：
- 只展示领养状态为"可领养"、已完成疫苗接种和驱虫的宠物，确保展示的宠物满足基本领养条件。
- 通过LEFT JOIN关联统计每个宠物的待审核申请数量，便于用户了解竞争情况。
- 前端领养宠物列表页面直接查询该视图，简化了应用层的查询逻辑。

查询视图示例：

```sql
SELECT pet_name, pet_type, breed, health_status, rescue_station, application_count
FROM v_adoptable_pets
ORDER BY application_count DESC;
```

### 5.4 创建存储过程

创建存储过程sp_monthly_statistics，统计某救助站本月的走失上报数量、成功匹配找回数量及宠物领养成功率：

```sql
CREATE OR REPLACE FUNCTION sp_monthly_statistics(
    p_rescue_station VARCHAR,
    p_year INTEGER DEFAULT EXTRACT(YEAR FROM CURRENT_DATE)::INTEGER,
    p_month INTEGER DEFAULT EXTRACT(MONTH FROM CURRENT_DATE)::INTEGER
)
RETURNS TABLE (
    total_lost_reports BIGINT,
    successful_recoveries BIGINT,
    recovery_rate NUMERIC(5,2),
    total_adoption_applications BIGINT,
    approved_adoptions BIGINT,
    adoption_success_rate NUMERIC(5,2),
    total_found_clues BIGINT,
    confirmed_clues BIGINT
) AS $$
DECLARE
    v_month_start DATE;
    v_next_month_start DATE;
BEGIN
    v_month_start := make_date(p_year, p_month, 1);
    v_next_month_start := (v_month_start + INTERVAL '1 month')::DATE;

    RETURN QUERY
    SELECT
        (SELECT COUNT(*) FROM lost_pets
         WHERE created_at >= v_month_start
           AND created_at < v_next_month_start
           AND (p_rescue_station IS NULL OR rescue_station = p_rescue_station)) AS total_lost_reports,
        (SELECT COUNT(*) FROM lost_pets
         WHERE created_at >= v_month_start
           AND created_at < v_next_month_start
           AND (p_rescue_station IS NULL OR rescue_station = p_rescue_station)
           AND status = 'found') AS successful_recoveries,
        CASE
            WHEN (SELECT COUNT(*) FROM lost_pets
                  WHERE created_at >= v_month_start
                    AND created_at < v_next_month_start
                    AND (p_rescue_station IS NULL OR rescue_station = p_rescue_station)) = 0 THEN 0
            ELSE ROUND(
                (SELECT COUNT(*)::NUMERIC FROM lost_pets
                 WHERE created_at >= v_month_start
                   AND created_at < v_next_month_start
                   AND (p_rescue_station IS NULL OR rescue_station = p_rescue_station)
                   AND status = 'found') /
                (SELECT COUNT(*)::NUMERIC FROM lost_pets
                 WHERE created_at >= v_month_start
                   AND created_at < v_next_month_start
                   AND (p_rescue_station IS NULL OR rescue_station = p_rescue_station)) * 100, 2)
        END AS recovery_rate,
        (SELECT COUNT(*) FROM adoption_applications aa
         JOIN adoptable_pets ap ON ap.adoptable_pet_id = aa.adoptable_pet_id
         WHERE aa.created_at >= v_month_start
           AND aa.created_at < v_next_month_start
           AND (p_rescue_station IS NULL OR ap.rescue_station = p_rescue_station)) AS total_adoption_applications,
        (SELECT COUNT(*) FROM adoption_applications aa
         JOIN adoptable_pets ap ON ap.adoptable_pet_id = aa.adoptable_pet_id
         WHERE aa.created_at >= v_month_start
           AND aa.created_at < v_next_month_start
           AND (p_rescue_station IS NULL OR ap.rescue_station = p_rescue_station)
           AND aa.status = 'approved') AS approved_adoptions,
        CASE
            WHEN (SELECT COUNT(*) FROM adoption_applications aa
                  JOIN adoptable_pets ap ON ap.adoptable_pet_id = aa.adoptable_pet_id
                  WHERE aa.created_at >= v_month_start
                    AND aa.created_at < v_next_month_start
                    AND (p_rescue_station IS NULL OR ap.rescue_station = p_rescue_station)) = 0 THEN 0
            ELSE ROUND(
                (SELECT COUNT(*)::NUMERIC FROM adoption_applications aa
                 JOIN adoptable_pets ap ON ap.adoptable_pet_id = aa.adoptable_pet_id
                 WHERE aa.created_at >= v_month_start
                   AND aa.created_at < v_next_month_start
                   AND (p_rescue_station IS NULL OR ap.rescue_station = p_rescue_station)
                   AND aa.status = 'approved') /
                (SELECT COUNT(*)::NUMERIC FROM adoption_applications aa
                 JOIN adoptable_pets ap ON ap.adoptable_pet_id = aa.adoptable_pet_id
                 WHERE aa.created_at >= v_month_start
                   AND aa.created_at < v_next_month_start
                   AND (p_rescue_station IS NULL OR ap.rescue_station = p_rescue_station)) * 100, 2)
        END AS adoption_success_rate,
        (SELECT COUNT(*) FROM found_clues fc
         JOIN lost_pets lp ON lp.lost_pet_id = fc.lost_pet_id
         WHERE fc.created_at >= v_month_start
           AND fc.created_at < v_next_month_start
           AND (p_rescue_station IS NULL OR lp.rescue_station = p_rescue_station)) AS total_found_clues,
        (SELECT COUNT(*) FROM found_clues fc
         JOIN lost_pets lp ON lp.lost_pet_id = fc.lost_pet_id
         WHERE fc.created_at >= v_month_start
           AND fc.created_at < v_next_month_start
           AND (p_rescue_station IS NULL OR lp.rescue_station = p_rescue_station)
           AND fc.status = 'confirmed') AS confirmed_clues;
END;
$$ LANGUAGE plpgsql;
```

调用存储过程示例：

```sql
-- 查询2026年5月的全局统计数据
SELECT * FROM sp_monthly_statistics(NULL, 2026, 5);

-- 查询广州市小动物救助中心2026年5月的统计数据
SELECT * FROM sp_monthly_statistics('广州市小动物救助中心', 2026, 5);
```

### 5.5 创建触发器

本系统共创建了4个触发器函数和7个触发器。

（1）自动更新时间戳触发器

当用户表、走失宠物表、可领养宠物表或领养申请表的记录被更新时，自动将updated_at字段设置为当前时间。

```sql
CREATE OR REPLACE FUNCTION fn_update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION fn_update_timestamp();

CREATE TRIGGER trg_lost_pets_updated_at
BEFORE UPDATE ON lost_pets
FOR EACH ROW EXECUTE FUNCTION fn_update_timestamp();

CREATE TRIGGER trg_adoptable_pets_updated_at
BEFORE UPDATE ON adoptable_pets
FOR EACH ROW EXECUTE FUNCTION fn_update_timestamp();

CREATE TRIGGER trg_adoption_applications_updated_at
BEFORE UPDATE ON adoption_applications
FOR EACH ROW EXECUTE FUNCTION fn_update_timestamp();
```

（2）领养申请审批通过后自动处理触发器

当领养申请状态被更新为"approved"时，自动将对应宠物的领养状态更新为"已领养"，并自动拒绝该宠物的其他待审核申请。

```sql
CREATE OR REPLACE FUNCTION fn_on_adoption_approved()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'approved' AND (OLD.status IS NULL OR OLD.status != 'approved') THEN
        UPDATE adoptable_pets SET adoption_status = 'adopted', updated_at = now()
        WHERE adoptable_pet_id = NEW.adoptable_pet_id;
        UPDATE adoption_applications SET status = 'rejected', updated_at = now()
        WHERE adoptable_pet_id = NEW.adoptable_pet_id
          AND application_id != NEW.application_id
          AND status = 'pending';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_adoption_approved
AFTER UPDATE OF status ON adoption_applications
FOR EACH ROW EXECUTE FUNCTION fn_on_adoption_approved();
```

（3）领养申请重复检查触发器

在插入新的领养申请前，检查宠物是否仍可领养、用户是否已提交过申请，确保数据完整性。

```sql
CREATE OR REPLACE FUNCTION fn_check_duplicate_application()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM adoptable_pets
        WHERE adoptable_pet_id = NEW.adoptable_pet_id
          AND adoption_status = 'available'
    ) THEN
        RAISE EXCEPTION 'Pet is not available for adoption'
            USING ERRCODE = 'check_violation';
    END IF;

    IF EXISTS (
        SELECT 1 FROM adoption_applications
        WHERE adoptable_pet_id = NEW.adoptable_pet_id
          AND applicant_id = NEW.applicant_id
          AND status IN ('pending', 'approved')
    ) THEN
        RAISE EXCEPTION 'Duplicate application: user has already applied for this pet'
            USING ERRCODE = 'unique_violation';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_duplicate_application
BEFORE INSERT ON adoption_applications
FOR EACH ROW EXECUTE FUNCTION fn_check_duplicate_application();
```

（4）领养通过后自动生成回访提醒触发器

当领养申请被批准时，自动创建一条30天后的回访提醒记录。

```sql
CREATE OR REPLACE FUNCTION fn_generate_visit_reminders()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'approved' AND (OLD.status IS NULL OR OLD.status != 'approved') THEN
        INSERT INTO visit_reminders (application_id, adopter_id, adoptable_pet_id, reminder_date, status)
        VALUES (NEW.application_id, NEW.applicant_id, NEW.adoptable_pet_id, CURRENT_DATE + INTERVAL '30 days', 'pending');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_generate_visit_reminders
AFTER UPDATE OF status ON adoption_applications
FOR EACH ROW EXECUTE FUNCTION fn_generate_visit_reminders();
```

触发器验证示例：审批通过"圆圆"的领养申请后，观察触发器效果

```sql
-- 审批通过王五对圆圆的领养申请
UPDATE adoption_applications
SET status = 'approved'
WHERE adoptable_pet_id = (SELECT adoptable_pet_id FROM adoptable_pets WHERE pet_name = '圆圆')
  AND applicant_id = (SELECT user_id FROM users WHERE username = 'wangwu');

-- 验证宠物状态已更新为已领养
SELECT pet_name, adoption_status FROM adoptable_pets WHERE pet_name = '圆圆';
-- 结果：圆圆 | adopted

-- 验证自动生成了回访提醒
SELECT * FROM visit_reminders
WHERE adoptable_pet_id = (SELECT adoptable_pet_id FROM adoptable_pets WHERE pet_name = '圆圆');
-- 结果：自动生成了一条reminder_date为30天后的提醒记录
```

---

## 第6章 数据库的安全性（选做）

### 6.1 用户和权限管理

本系统在应用层面实现了基于角色的访问控制（RBAC）机制：

（1）用户角色划分：系统定义了两种角色——普通用户（user）和管理员（admin）。角色信息存储在users表的role字段中。

（2）认证机制：系统采用JWT（JSON Web Token）实现用户认证。用户登录时，服务端验证用户名和密码后生成JWT令牌，令牌中包含用户ID和角色信息。密码使用Argon2算法进行哈希存储，Argon2是目前公认最安全的密码哈希算法之一，能有效抵抗暴力破解和彩虹表攻击。

（3）授权机制：系统在API层面实现了细粒度的权限控制：
- 公开接口：走失宠物列表、宠物详情等无需认证即可访问。
- 用户接口：发布走失信息、提交线索、提交领养申请等需要用户登录。
- 管理员接口：宠物管理、线索审核、申请审批、统计查询等仅管理员可访问。

（4）数据隔离：普通用户只能查看和修改自己的数据，管理员可以查看和管理所有数据。例如，用户只能查看自己发布的走失宠物的线索详情，而管理员可以查看所有线索。

### 6.2 数据库的备份与恢复

本系统使用Docker Compose部署PostgreSQL数据库，数据存储在命名卷pgdata中。数据库备份与恢复方案如下：

（1）备份策略：使用pg_dump工具进行定期全量备份，备份命令如下：

```bash
docker exec <db_container> pg_dump -U postgres lost_pet_db > backup_$(date +%Y%m%d).sql
```

（2）恢复策略：使用psql工具进行数据恢复：

```bash
docker exec -i <db_container> psql -U postgres lost_pet_db < backup_20260530.sql
```

（3）Docker卷备份：定期备份Docker命名卷以确保数据安全：

```bash
docker run --rm -v pgdata:/data -v $(pwd):/backup alpine tar czf /backup/pgdata_backup.tar.gz /data
```

---

## 第7章 系统实现（选做）

### 7.1 走失宠物发布功能

#### 7.1.1 界面

走失宠物发布页面（LostPetPublish.vue）提供了一个完整的表单界面，用户可以填写宠物基本信息和走失信息。页面使用Element Plus组件库构建，包含以下主要区域：

- 基本信息区域：宠物名称（输入框）、宠物种类（下拉选择：猫/狗/鸟/其他）、品种（输入框）、颜色（输入框）、性别（单选：公/母/未知）、年龄描述（输入框）
- 走失信息区域：走失日期（日期选择器）、走失地点（输入框）、救助站（输入框）、联系方式（输入框）、悬赏金额（数字输入框）
- 描述信息区域：详细描述（多行文本框）
- 照片上传区域：支持多张照片上传，使用自定义ImageUploader组件，单张照片限制5MB

表单提交前会进行前端验证，确保必填字段不为空、联系方式格式正确等。

#### 7.1.2 数据操作核心代码

前端API调用代码（frontend/src/api/lostPets.ts）：

```typescript
import api from './index'
import type { LostPet, PaginatedResponse } from '@/types/models'

export const lostPetsApi = {
  list(params: Record<string, any>) {
    return api.get<PaginatedResponse<LostPet>>('/lost-pets', { params })
  },
  getDetail(lostPetId: string) {
    return api.get<LostPet>(`/lost-pets/${lostPetId}`)
  },
  create(data: Partial<LostPet>) {
    return api.post<LostPet>('/lost-pets', data)
  },
  update(lostPetId: string, data: Partial<LostPet>) {
    return api.put<LostPet>(`/lost-pets/${lostPetId}`, data)
  },
  delete(lostPetId: string) {
    return api.delete(`/lost-pets/${lostPetId}`)
  },
  updateStatus(lostPetId: string, status: string) {
    return api.patch(`/lost-pets/${lostPetId}/status`, { status })
  },
  getMy() {
    return api.get<LostPet[]>('/lost-pets/my')
  }
}
```

其中Axios实例统一配置了`baseURL`为`/api`，因此各业务API文件中只保留资源路径。

后端路由处理代码（backend/app/routers/lost_pets.py）：

```python
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud_lost_pet import crud_lost_pet
from app.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.lost_pet import LostPetCreate, LostPetResponse, LostPetUpdate

router = APIRouter()

@router.post("", response_model=LostPetResponse, status_code=status.HTTP_201_CREATED)
async def create_lost_pet(
    obj_in: LostPetCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    pet = await crud_lost_pet.create(db, obj_in=obj_in, user_id=current_user.user_id)
    return pet

@router.get("", response_model=dict)
async def list_lost_pets(
    db: Annotated[AsyncSession, Depends(get_db)],
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=50),
    pet_type: str | None = None,
    status: str | None = None,
    keyword: str | None = None,
):
    skip = (page - 1) * page_size
    items, total = await crud_lost_pet.get_multi(
        db, skip=skip, limit=page_size, pet_type=pet_type, status=status, keyword=keyword
    )
    return {
        "items": [LostPetResponse.model_validate(p) for p in items],
        "total": total,
        "page": page,
        "page_size": page_size,
    }
```

### 7.2 领养申请功能

#### 7.2.1 界面

领养申请页面（AdoptionApplicationForm.vue）在用户选择心仪宠物后展示，包含以下信息填写区域：

- 个人信息区域：申请人姓名（输入框）、联系电话（输入框）、居住地址（输入框）、身份证号（输入框）
- 住房信息区域：住房类型（下拉选择：自有住房/租房/其他）、是否饲养其他宠物（开关）
- 申请理由区域：领养原因（多行文本框）、养宠经验描述（多行文本框）

页面会在提交前检查用户是否已登录，未登录用户会被重定向到登录页面。表单提交后，后端通过数据库触发器自动检查是否存在重复申请，确保数据完整性。

#### 7.2.2 数据操作核心代码

前端提交领养申请的代码：

```typescript
import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { AdoptionApplication } from '@/types/models'
import { adoptionApplicationsApi } from '@/api/adoptionApplications'

export const useAdoptionApplicationsStore = defineStore('adoptionApplications', () => {
  const applications = ref<AdoptionApplication[]>([])
  const loading = ref(false)

  async function fetchMyApplications() {
    loading.value = true
    try {
      const res = await adoptionApplicationsApi.getMy()
      applications.value = res.data
    } finally {
      loading.value = false
    }
  }

  async function submitApplication(data: Partial<AdoptionApplication>) {
    const res = await adoptionApplicationsApi.create(data)
    return res.data
  }

  async function cancelApplication(applicationId: string) {
    await adoptionApplicationsApi.cancel(applicationId)
    const app = applications.value.find((a) => a.application_id === applicationId)
    if (app) app.status = 'cancelled'
  }

  return { applications, loading, fetchMyApplications, submitApplication, cancelApplication }
})
```

后端领养申请创建的CRUD操作（backend/app/crud/crud_adoption_application.py）：

```python
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.adoption_application import AdoptionApplication
from app.schemas.adoption_application import AdoptionApplicationCreate

class CRUDAdoptionApplication:
    async def create(
        self,
        db: AsyncSession,
        *,
        obj_in: AdoptionApplicationCreate,
        applicant_id: UUID,
    ) -> AdoptionApplication:
        db_obj = AdoptionApplication(**obj_in.model_dump(), applicant_id=applicant_id)
        db.add(db_obj)
        await db.flush()
        application_id = db_obj.application_id
        await db.commit()
        created = await self.get(db, application_id=application_id)
        if created is None:
            raise RuntimeError("Created adoption application not found")
        return created
```

---

## 结  论

通过本次数据库系统课程设计，完成了宠物走失与领养救助平台数据库系统的完整设计与实现。主要完成了以下工作：

（1）需求分析阶段：通过调研宠物救助领域的实际需求，明确了系统的两类用户角色（普通用户和管理员），梳理了走失宠物发布、线索上报、领养申请、审核管理、回访提醒和统计分析等核心业务流程，绘制了系统边界图、业务流程图、功能模块结构图和数据流图。

（2）概念结构设计阶段：识别了用户、走失宠物、发现线索、可领养宠物、领养申请、审核记录和回访提醒7个实体，分析了各实体之间的联系，绘制了局部E-R图和全局E-R图。

（3）逻辑结构设计阶段：将E-R图转换为7个关系模式，使用规范化理论验证所有关系模式均满足第三范式要求。

（4）物理结构设计阶段：选择PostgreSQL 16作为数据库管理系统，设计了7张数据表的物理结构，创建了14个索引以优化查询性能。

（5）数据库实施阶段：编写了完整的建表SQL语句，创建了1个视图（v_adoptable_pets）用于简化可领养宠物查询，创建了1个存储过程（sp_monthly_statistics）用于月度统计，创建了4个触发器函数和7个触发器用于实现自动时间戳更新、领养审批级联处理、申请重复检查和回访提醒自动生成等业务逻辑。

（6）系统实现阶段：使用FastAPI框架实现了后端RESTful API，使用Vue 3 + TypeScript + Element Plus实现了前端界面，使用Docker Compose实现了容器化部署。

在设计过程中遇到的问题及解决方案：
- 业务逻辑放在数据库层还是应用层的问题：最终选择将核心业务约束（如领养申请重复检查、审批级联操作）通过数据库触发器实现，确保数据一致性不受应用层代码影响。
- 多值属性存储问题：使用PostgreSQL的数组类型存储照片地址列表，避免了额外的关联表设计。
- 统计查询性能问题：通过创建存储过程将复杂的统计计算放在数据库层执行，减少了网络传输开销。

不足与改进方向：
- 目前系统缺少数据备份的自动化脚本，后续可添加定时备份任务。
- 地理位置信息仅支持简单的经纬度存储，未使用PostGIS进行空间查询优化。
- 系统缺少全文搜索功能，后续可引入PostgreSQL的全文检索能力提升搜索体验。
- 可考虑添加消息通知功能，在领养申请状态变更时通过邮件或短信通知用户。

---

## 参考文献

[1] 胡致杰,胡羽沫,李代平.《数据库系统原理及应用课程设计与实验指导》(第2版).清华大学出版社,2023.

[2] 胡致杰,梁玉英等.《数据库系统及应用》.北京工业大学出版社,2023.

[3] 王珊,萨师煊.《数据库系统概论》(第5版).高等教育出版社,2014.

[4] PostgreSQL Global Development Group. PostgreSQL 16 Documentation[EB/OL]. https://www.postgresql.org/docs/16/, 2023.

[5] FastAPI Documentation[EB/OL]. https://fastapi.tiangolo.com/, 2024.

[6] Vue.js 3 Documentation[EB/OL]. https://vuejs.org/guide/introduction.html, 2024.

[7] Ramalingam G, Vaswani A. Database-driven Web Application Development[J]. IEEE Software, 2020, 37(3): 45-52.

[8] 张海藩,牟永敏.《软件工程导论》(第6版).清华大学出版社,2013.

[9] Connolly T, Begg C. Database Systems: A Practical Approach to Design, Implementation, and Management (6th Edition). Pearson, 2014.

[10] Elmasri R, Navathe S. Fundamentals of Database Systems (7th Edition). Pearson, 2015.

[11] 刘增杰,张少林.PostgreSQL数据库从入门到精通[M].中国铁道出版社,2022.

[12] Docker Documentation[EB/OL]. https://docs.docker.com/, 2024.

---

## 致  谢

在本次数据库系统课程设计过程中，感谢指导教师的悉心指导和耐心解答，帮助我理清了数据库设计的思路和方法。感谢小组成员的协作与配合，在需求分析、概念设计和系统实现等环节中共同讨论、互相帮助。感谢广东理工学院提供的学习环境和实验资源，使我能够顺利完成本次课程设计。同时，感谢开源社区提供的PostgreSQL、FastAPI、Vue.js等优秀的开发工具和框架，为系统的设计与实现提供了强大的技术支持。
