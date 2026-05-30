# 宠物救助与领养平台

一个前后端分离的宠物救助平台，覆盖走失宠物发布、线索提交、救助宠物领养、领养申请审核、回访提醒和运营统计等场景。

## 功能特性

- 用户认证：支持用户注册、登录、个人资料维护和 JWT 鉴权。
- 走失宠物：支持发布走失宠物、列表检索、详情查看、状态更新和删除。
- 寻宠线索：用户可针对走失宠物提交线索，管理员可审核线索状态。
- 领养管理：管理员维护待领养宠物，用户浏览宠物详情并提交领养申请。
- 申请审核：管理员审核领养申请，审核通过后自动更新宠物领养状态并拒绝同宠物的其他待处理申请。
- 回访提醒：领养申请通过后自动生成 7 天、30 天、90 天回访提醒。
- 数据统计：提供后台概览和月度统计，包含找回率、领养成功率、线索确认等指标。
- 文件上传：支持图片上传，并通过 `/uploads` 提供静态访问。

## 技术栈

### 前端

- Vue 3
- TypeScript
- Vite
- Vue Router
- Pinia
- Element Plus
- Axios
- Sass

### 后端

- FastAPI
- SQLAlchemy AsyncIO
- PostgreSQL
- Alembic
- Pydantic / pydantic-settings
- python-jose
- Argon2 密码哈希

### 部署

- Docker
- Docker Compose
- Nginx

## 目录结构

```text
.
├── backend/                 # FastAPI 后端服务
│   ├── alembic/             # 数据库迁移脚本
│   ├── app/
│   │   ├── crud/            # 数据访问层
│   │   ├── models/          # SQLAlchemy 模型
│   │   ├── routers/         # API 路由
│   │   ├── schemas/         # Pydantic 数据结构
│   │   ├── services/        # 业务服务
│   │   ├── config.py        # 配置项
│   │   ├── database.py      # 数据库连接
│   │   └── main.py          # FastAPI 入口
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                # Vue 前端应用
│   ├── src/
│   │   ├── api/             # API 请求封装
│   │   ├── components/      # 公共组件
│   │   ├── router/          # 路由配置
│   │   ├── stores/          # Pinia 状态管理
│   │   ├── styles/          # 全局样式
│   │   ├── types/           # TypeScript 类型
│   │   └── views/           # 页面视图
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
└── docker-compose.yml       # 本地容器编排
```

## 快速启动

### 使用 Docker Compose

确保已安装 Docker 和 Docker Compose。

```bash
docker compose up -d --build
```

容器启动后执行数据库迁移：

```bash
docker compose exec backend alembic upgrade head
```

访问地址：

- 前端页面：http://localhost
- 后端接口：http://localhost:8000
- API 文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/api/health

停止服务：

```bash
docker compose down
```

如需同时删除数据库和上传文件卷：

```bash
docker compose down -v
```

## 本地开发

### 1. 启动 PostgreSQL

可以复用 Docker Compose 中的数据库：

```bash
docker compose up -d db
```

默认数据库连接信息：

- Host：`localhost`
- Port：`5432`
- Database：`lost_pet_db`
- User：`postgres`
- Password：`postgres`

### 2. 启动后端

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Windows PowerShell 激活虚拟环境：

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端开发服务默认运行在：

```text
http://localhost:5173
```

Vite 已配置代理：

- `/api` -> `http://localhost:8000`
- `/uploads` -> `http://localhost:8000`

## 环境变量

后端配置读取 `backend/.env`，未提供时使用 `backend/app/config.py` 中的默认值。

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/lost_pet_db
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
UPLOAD_DIR=uploads
CORS_ORIGINS=["http://localhost:5173"]
```

前端可通过 `.env` 配置接口地址：

```env
VITE_API_BASE_URL=/api
```

生产环境请务必替换 `SECRET_KEY`，并按实际域名调整 `CORS_ORIGINS`。

## 管理员账号

系统注册用户默认角色为 `user`。需要管理员权限时，可先通过前端或接口注册账号，再在数据库中将角色更新为 `admin`：

```sql
UPDATE users SET role = 'admin' WHERE username = 'your_admin_username';
```

管理员可访问后台路由：

```text
/admin
```

## 常用 API

### 认证

- `POST /api/auth/register`：注册用户
- `POST /api/auth/login`：登录并获取访问令牌
- `GET /api/auth/me`：获取当前用户
- `PUT /api/auth/me`：更新当前用户

### 走失宠物

- `GET /api/lost-pets`：分页查询走失宠物
- `POST /api/lost-pets`：发布走失宠物
- `GET /api/lost-pets/my`：查询我的走失宠物
- `GET /api/lost-pets/{pet_id}`：查询走失宠物详情
- `PUT /api/lost-pets/{pet_id}`：更新走失宠物
- `DELETE /api/lost-pets/{pet_id}`：删除走失宠物
- `PATCH /api/lost-pets/{pet_id}/status`：更新走失宠物状态

### 寻宠线索

- `POST /api/found-clues/lost-pets/{pet_id}/clues`：提交线索
- `GET /api/found-clues/lost-pets/{pet_id}/clues`：查询指定宠物线索
- `GET /api/found-clues/my`：查询我提交的线索
- `GET /api/found-clues/{clue_id}`：查询线索详情
- `PATCH /api/found-clues/{clue_id}/status`：审核线索

### 领养宠物

- `GET /api/adoptable-pets`：分页查询待领养宠物
- `POST /api/adoptable-pets`：新增待领养宠物
- `GET /api/adoptable-pets/{pet_id}`：查询待领养宠物详情
- `PUT /api/adoptable-pets/{pet_id}`：更新待领养宠物
- `DELETE /api/adoptable-pets/{pet_id}`：删除待领养宠物
- `PATCH /api/adoptable-pets/{pet_id}/status`：更新领养状态

### 领养申请

- `POST /api/adoption-applications`：提交领养申请
- `GET /api/adoption-applications/my`：查询我的领养申请
- `GET /api/adoption-applications/{app_id}`：查询申请详情
- `PATCH /api/adoption-applications/{app_id}/cancel`：取消待处理申请

### 管理后台

- `GET /api/admin/applications`：查询申请列表
- `POST /api/admin/applications/{app_id}/review`：审核领养申请
- `GET /api/admin/statistics`：查询月度统计
- `GET /api/admin/statistics/overview`：查询后台概览
- `GET /api/admin/visit-reminders`：查询回访提醒
- `PATCH /api/admin/visit-reminders/{reminder_id}`：更新回访提醒
- `GET /api/admin/clues`：查询线索列表

### 文件上传

- `POST /api/upload/image`：上传图片
- `GET /uploads/{filename}`：访问上传文件

## 数据库说明

初始迁移包含以下核心表：

- `users`：用户
- `lost_pets`：走失宠物
- `found_clues`：寻宠线索
- `adoptable_pets`：待领养宠物
- `adoption_applications`：领养申请
- `review_records`：审核记录
- `visit_reminders`：回访提醒

迁移还创建了：

- 视图 `v_adoptable_pets`：查询可领养宠物及待处理申请数量。
- 函数 `sp_monthly_statistics(year, month)`：统计月度找回、领养和线索数据。
- 触发器：自动更新时间戳、处理领养通过后的状态联动、阻止重复申请、生成回访提醒。

## 常用命令

### 前端

```bash
cd frontend
npm run dev
npm run build
npm run preview
```

### 后端

```bash
cd backend
uvicorn app.main:app --reload
alembic upgrade head
alembic downgrade -1
```

### Docker

```bash
docker compose up -d --build
docker compose logs -f backend
docker compose logs -f frontend
docker compose down
```

## 开发注意事项

- 受保护接口需要在请求头中携带 `Authorization: Bearer <token>`。
- 前端登录后会将 token 写入 `localStorage`，Axios 拦截器会自动附加认证头。
- 管理后台路由要求用户角色为 `admin`。
- 图片上传目录默认为 `uploads`，Docker 环境下映射到命名卷 `uploads`。
- 数据库迁移依赖 PostgreSQL，首次启动后必须执行 `alembic upgrade head`。
