import os
from dotenv import load_dotenv

load_dotenv()


def _env_float(key: str, default: float) -> float:
    """解析浮点环境变量，非法值静默回落默认值（配置写错绝不拖垮服务启动）。"""
    try:
        return float(os.getenv(key, default))
    except (TypeError, ValueError):
        return default


def _env_int(key: str, default: int) -> int:
    """解析整型环境变量，非法值静默回落默认值。"""
    try:
        return int(os.getenv(key, default))
    except (TypeError, ValueError):
        return default


def _env_bool(key: str, default: bool) -> bool:
    """解析布尔环境变量，接受 1/true/yes/on 与 0/false/no/off。"""
    raw = os.getenv(key)
    if raw is None or not raw.strip():
        return default
    return raw.strip().lower() not in ("0", "false", "no", "off")


class Settings:
    PROJECT_NAME: str = "GEO-Matrix AI 搜索引擎优化与巡检系统"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("GEO_SECRET_KEY", "geo-super-secret-key-change-in-production-2026")
    
    # 数据库配置 (默认使用轻量 SQLite，支持无缝切换到 PostgreSQL)
    _DEFAULT_DB = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "geo_system.db")
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        f"sqlite:///{_DEFAULT_DB}"
    )
    
    # 大模型 API 密钥配置 (可选配置，未配置时自动启用高质量异构爬虫分析引擎)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DOUBAO_API_KEY: str = os.getenv("DOUBAO_API_KEY", "")
    DOUBAO_MODEL_NAME: str = os.getenv("DOUBAO_MODEL_NAME", "doubao-seed-2-0-lite-260215")
    DASHSCOPE_API_KEY: str = os.getenv("DASHSCOPE_API_KEY", os.getenv("QWEN_API_KEY", ""))
    QWEN_API_KEY: str = os.getenv("QWEN_API_KEY", os.getenv("DASHSCOPE_API_KEY", ""))
    BAIDU_API_KEY: str = os.getenv("BAIDU_API_KEY", "")
    BAIDU_ACCESS_KEY_ID: str = os.getenv("BAIDU_ACCESS_KEY_ID", "")
    BAIDU_ACCESS_KEY_SECRET: str = os.getenv("BAIDU_ACCESS_KEY_SECRET", "")
    MOONSHOT_API_KEY: str = os.getenv("MOONSHOT_API_KEY", "")
    ALIYUN_ACCESS_KEY_ID: str = os.getenv("ALIYUN_ACCESS_KEY_ID", "")
    ALIYUN_ACCESS_KEY_SECRET: str = os.getenv("ALIYUN_ACCESS_KEY_SECRET", "")
    VOLC_ACCESS_KEY: str = os.getenv("VOLC_ACCESS_KEY", os.getenv("VOLCENGINE_ACCESS_KEY_ID", ""))
    VOLC_SECRET_KEY: str = os.getenv("VOLC_SECRET_KEY", os.getenv("VOLCENGINE_ACCESS_KEY_SECRET", ""))
    HUNYUAN_API_KEY: str = os.getenv("HUNYUAN_API_KEY", "")

    # 高德开放平台 Web服务 REST API Key (用于 POI 智能联想补全、权威事实反填与防呆消歧)
    AMAP_KEY: str = os.getenv("AMAP_KEY", "")

    # 下游 03 内容分发系统 (Content Hub & Dispatcher) 跨仓工单推送对接
    DISTRIBUTION_API_URL: str = os.getenv("DISTRIBUTION_API_URL", "http://127.0.0.1:8003")
    DISTRIBUTION_ENABLED: bool = _env_bool("DISTRIBUTION_ENABLED", True)
    DISTRIBUTION_AUTO_DISPATCH: bool = _env_bool("DISTRIBUTION_AUTO_DISPATCH", True)
    DISTRIBUTION_TIMEOUT_S: float = _env_float("DISTRIBUTION_TIMEOUT_S", 5.0)
    DISTRIBUTION_MAX_RETRIES: int = _env_int("DISTRIBUTION_MAX_RETRIES", 3)

    # 上游 02 品牌知识库（事实真理底座）跨仓事实回流对接（M7.1）
    KNOWLEDGE_API_URL: str = os.getenv("KNOWLEDGE_API_URL", "http://127.0.0.1:8002")
    KNOWLEDGE_SYNC_ENABLED: bool = _env_bool("KNOWLEDGE_SYNC_ENABLED", True)
    KNOWLEDGE_SYNC_AUTO: bool = _env_bool("KNOWLEDGE_SYNC_AUTO", True)
    KNOWLEDGE_SYNC_TIMEOUT_S: float = _env_float("KNOWLEDGE_SYNC_TIMEOUT_S", 5.0)
    KNOWLEDGE_SYNC_MAX_RETRIES: int = _env_int("KNOWLEDGE_SYNC_MAX_RETRIES", 3)

    # 跨仓内部服务预共享令牌 (AGENTS.md 五.4)：本地未配置时默认信任放行
    INTERNAL_SERVICE_SECRET: str = os.getenv("INTERNAL_SERVICE_SECRET", "")

settings = Settings()
