from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1.router import api_router
import app.models  # 确保所有模型加载

# 初始化创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc"
)

# 开启 Gzip 全局响应压缩 (大幅缩减公网传输体积，130KB JSON 压缩至 12KB，加速国内公网秒开)
app.add_middleware(GZipMiddleware, minimum_size=500)

# 允许跨域请求 (适配前端 Vue 开发及外嵌调用)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health")
def health_check():
    return {"status": "ok", "system": settings.PROJECT_NAME}

# 前端静态资源与多页面/SPA 兜底托管 (使 8000 端口与 5173 端口均可直接访问控制台与体检书)
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse

frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"))
if os.path.exists(frontend_dist):
    assets_dir = os.path.join(frontend_dist, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/console.html")
    def serve_console():
        return FileResponse(os.path.join(frontend_dist, "console.html"))

    @app.get("/console")
    def redirect_console():
        return RedirectResponse(url="/console.html")

    @app.get("/diagnostic")
    def redirect_diagnostic():
        return RedirectResponse(url="/console.html")

    @app.get("/")
    def serve_index():
        return FileResponse(os.path.join(frontend_dist, "index.html"))

    @app.get("/{full_path:path}")
    def serve_spa(full_path: str):
        # 排除 API 与文档路由
        if full_path.startswith("api/") or full_path == "health" or full_path.startswith("docs") or full_path.startswith("openapi.json"):
            return None
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        if "console" in full_path:
            return FileResponse(os.path.join(frontend_dist, "console.html"))
        return FileResponse(os.path.join(frontend_dist, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
