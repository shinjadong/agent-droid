from __future__ import annotations

import os
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Optional

import yaml

from droidrun.config_manager.path_resolver import PathResolver
from droidrun.config_manager.safe_execution import SafeExecutionConfig


# ---------- 설정 스키마 ----------
@dataclass
class LLMProfile:
    """LLM 프로필 설정."""

    provider: str = "GoogleGenAI"
    model: str = "models/gemini-2.0-flash-exp"
    temperature: float = 0.2
    base_url: Optional[str] = None
    api_base: Optional[str] = None
    kwargs: Dict[str, Any] = field(default_factory=dict)

    def to_load_llm_kwargs(self) -> Dict[str, Any]:
        """프로필을 load_llm 함수용 kwargs로 변환합니다."""
        result = {
            "model": self.model,
            "temperature": self.temperature,
        }
        # 선택적 URL 매개변수 추가
        if self.base_url:
            result["base_url"] = self.base_url
        if self.api_base:
            result["api_base"] = self.api_base
        # 추가 kwargs 병합
        result.update(self.kwargs)
        return result


@dataclass
class CodeActConfig:
    """CodeAct 에이전트 설정."""

    vision: bool = False
    system_prompt: str = "system.jinja2"
    user_prompt: str = "user.jinja2"
    safe_execution: bool = False


@dataclass
class ManagerConfig:
    """Manager 에이전트 설정."""

    vision: bool = False
    system_prompt: str = "system.jinja2"


@dataclass
class ExecutorConfig:
    """Executor 에이전트 설정."""

    vision: bool = False
    system_prompt: str = "system.jinja2"


@dataclass
class ScripterConfig:
    """Scripter 에이전트 설정."""

    enabled: bool = True
    max_steps: int = 10
    execution_timeout: float = 30.0
    system_prompt_path: str = "system.jinja2"
    safe_execution: bool = False


@dataclass
class AppCardConfig:
    """앱 카드 설정."""

    enabled: bool = True
    mode: str = "local"  # local | server | composite
    app_cards_dir: str = "config/app_cards"
    server_url: Optional[str] = None
    server_timeout: float = 2.0
    server_max_retries: int = 2


@dataclass
class AgentConfig:
    """에이전트 관련 설정."""

    max_steps: int = 15
    reasoning: bool = False
    after_sleep_action: float = 1.0
    wait_for_stable_ui: float = 0.3
    prompts_dir: str = "config/prompts"

    codeact: CodeActConfig = field(default_factory=CodeActConfig)
    manager: ManagerConfig = field(default_factory=ManagerConfig)
    executor: ExecutorConfig = field(default_factory=ExecutorConfig)
    scripter: ScripterConfig = field(default_factory=ScripterConfig)
    app_cards: AppCardConfig = field(default_factory=AppCardConfig)

    def get_codeact_system_prompt_path(self) -> str:
        """CodeAct 시스템 프롬프트의 절대 경로를 가져옵니다."""
        path = f"{self.prompts_dir}/codeact/{self.codeact.system_prompt}"
        return str(PathResolver.resolve(path, must_exist=True))

    def get_codeact_user_prompt_path(self) -> str:
        """CodeAct 사용자 프롬프트의 절대 경로를 가져옵니다."""
        path = f"{self.prompts_dir}/codeact/{self.codeact.user_prompt}"
        return str(PathResolver.resolve(path, must_exist=True))

    def get_manager_system_prompt_path(self) -> str:
        """Manager 시스템 프롬프트의 절대 경로를 가져옵니다."""
        path = f"{self.prompts_dir}/manager/{self.manager.system_prompt}"
        return str(PathResolver.resolve(path, must_exist=True))

    def get_executor_system_prompt_path(self) -> str:
        """Executor 시스템 프롬프트의 절대 경로를 가져옵니다."""
        path = f"{self.prompts_dir}/executor/{self.executor.system_prompt}"
        return str(PathResolver.resolve(path, must_exist=True))

    def get_scripter_system_prompt_path(self) -> str:
        """Scripter 시스템 프롬프트의 절대 경로를 가져옵니다."""
        path = f"{self.prompts_dir}/scripter/{self.scripter.system_prompt_path}"
        return str(PathResolver.resolve(path, must_exist=True))


@dataclass
class DeviceConfig:
    """기기 관련 설정."""

    serial: Optional[str] = None
    use_tcp: bool = False
    platform: str = "android"  # "android" or "ios"


@dataclass
class TelemetryConfig:
    """원격 측정 설정."""

    enabled: bool = True


@dataclass
class TracingConfig:
    """추적 설정."""

    enabled: bool = False
    provider: str = "phoenix"  # "phoenix" or "langfuse"
    langfuse_secret_key: str = ""  # 비어 있지 않으면 LANGFUSE_SECRET_KEY 환경 변수로 설정
    langfuse_public_key: str = ""  # 비어 있지 않으면 LANGFUSE_PUBLIC_KEY 환경 변수로 설정
    langfuse_host: str = ""  # 비어 있지 않으면 LANGFUSE_HOST 환경 변수로 설정
    langfuse_user_id: str = "anonymous"
    langfuse_session_id: str = (
        ""  # 비어 있음 = UUID 자동 생성; 실행 간 유지하려면 사용자 정의 값 설정
    )


@dataclass
class LoggingConfig:
    """로깅 설정."""

    debug: bool = False
    save_trajectory: str = "none"
    trajectory_path: str = "trajectories"
    rich_text: bool = False


@dataclass
class ToolsConfig:
    """도구 설정."""

    allow_drag: bool = False


@dataclass
class CredentialsConfig:
    """자격 증명 설정."""

    enabled: bool = False
    file_path: str = "credentials.yaml"


@dataclass
class DroidrunConfig:
    """완전한 DroidRun 설정 스키마."""

    agent: AgentConfig = field(default_factory=AgentConfig)
    llm_profiles: Dict[str, LLMProfile] = field(default_factory=dict)
    device: DeviceConfig = field(default_factory=DeviceConfig)
    telemetry: TelemetryConfig = field(default_factory=TelemetryConfig)
    tracing: TracingConfig = field(default_factory=TracingConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    tools: ToolsConfig = field(default_factory=ToolsConfig)
    credentials: CredentialsConfig = field(default_factory=CredentialsConfig)
    safe_execution: SafeExecutionConfig = field(default_factory=SafeExecutionConfig)

    def __post_init__(self):
        """기본 프로필이 존재하는지 확인합니다."""
        if not self.llm_profiles:
            self.llm_profiles = self._default_profiles()

    @staticmethod
    def _default_profiles() -> Dict[str, LLMProfile]:
        """기본 에이전트별 LLM 프로필을 가져옵니다."""
        return {
            "manager": LLMProfile(
                provider="GoogleGenAI",
                model="models/gemini-2.5-pro",
                temperature=0.2,
                kwargs={},
            ),
            "executor": LLMProfile(
                provider="GoogleGenAI",
                model="models/gemini-2.5-pro",
                temperature=0.1,
                kwargs={},
            ),
            "codeact": LLMProfile(
                provider="GoogleGenAI",
                model="models/gemini-2.5-pro",
                temperature=0.2,
                kwargs={},
            ),
            "text_manipulator": LLMProfile(
                provider="GoogleGenAI",
                model="models/gemini-2.5-pro",
                temperature=0.3,
                kwargs={},
            ),
            "app_opener": LLMProfile(
                provider="GoogleGenAI",
                model="models/gemini-2.5-pro",
                temperature=0.0,
                kwargs={},
            ),
            "scripter": LLMProfile(
                provider="GoogleGenAI",
                model="models/gemini-2.5-flash",
                temperature=0.1,
                kwargs={},
            ),
            "structured_output": LLMProfile(
                provider="GoogleGenAI",
                model="models/gemini-2.5-flash",
                temperature=0.0,
                kwargs={},
            ),
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        result = asdict(self)
        # Convert LLMProfile objects to dicts
        result["llm_profiles"] = {
            name: asdict(profile) for name, profile in self.llm_profiles.items()
        }
        # safe_execution is already converted by asdict
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DroidrunConfig":
        """Create config from dictionary."""
        # Parse LLM profiles
        llm_profiles = {}
        for name, profile_data in data.get("llm_profiles", {}).items():
            llm_profiles[name] = LLMProfile(**profile_data)

        # Parse agent config with sub-configs
        agent_data = data.get("agent", {})

        codeact_data = agent_data.get("codeact", {})
        codeact_config = (
            CodeActConfig(**codeact_data) if codeact_data else CodeActConfig()
        )

        manager_data = agent_data.get("manager", {})
        manager_config = (
            ManagerConfig(**manager_data) if manager_data else ManagerConfig()
        )

        executor_data = agent_data.get("executor", {})
        executor_config = (
            ExecutorConfig(**executor_data) if executor_data else ExecutorConfig()
        )

        script_data = agent_data.get("scripter", {})
        scripter_config = (
            ScripterConfig(**script_data) if script_data else ScripterConfig()
        )

        app_cards_data = agent_data.get("app_cards", {})
        app_cards_config = (
            AppCardConfig(**app_cards_data) if app_cards_data else AppCardConfig()
        )

        agent_config = AgentConfig(
            max_steps=agent_data.get("max_steps", 15),
            reasoning=agent_data.get("reasoning", False),
            after_sleep_action=agent_data.get("after_sleep_action", 1.0),
            wait_for_stable_ui=agent_data.get("wait_for_stable_ui", 0.3),
            prompts_dir=agent_data.get("prompts_dir", "config/prompts"),
            codeact=codeact_config,
            manager=manager_config,
            executor=executor_config,
            scripter=scripter_config,
            app_cards=app_cards_config,
        )

        # Parse safe_execution config
        safe_exec_data = data.get("safe_execution", {})
        safe_execution_config = (
            SafeExecutionConfig(**safe_exec_data)
            if safe_exec_data
            else SafeExecutionConfig()
        )

        return cls(
            agent=agent_config,
            llm_profiles=llm_profiles,
            device=DeviceConfig(**data.get("device", {})),
            telemetry=TelemetryConfig(**data.get("telemetry", {})),
            tracing=TracingConfig(**data.get("tracing", {})),
            logging=LoggingConfig(**data.get("logging", {})),
            tools=ToolsConfig(**data.get("tools", {})),
            credentials=CredentialsConfig(**data.get("credentials", {})),
            safe_execution=safe_execution_config,
        )

    @classmethod
    def from_yaml(
        cls,
        path: str,
        use_path_resolver: bool = True,
        create_if_missing: bool = False,
    ) -> "DroidrunConfig":
        """
        Create config from YAML file.

        Args:
            path: Path to YAML config file (relative or absolute).
                 If use_path_resolver=True (default), PathResolver will check:
                 - Absolute paths: used as-is
                 - Relative paths: checks working dir first, then package dir
            use_path_resolver: If True (default), resolve path using PathResolver.
                              If False, use path as-is.
            create_if_missing: If True, create config file from defaults if not found.
                              If False (default), raise FileNotFoundError.

        Returns:
            DroidrunConfig instance

        Raises:
            FileNotFoundError: If the YAML file doesn't exist and create_if_missing=False

        Example:
            >>> config = DroidrunConfig.from_yaml("config.yaml")
            >>> config = DroidrunConfig.from_yaml("/absolute/path/config.yaml")
            >>> config = DroidrunConfig.from_yaml("config.yaml", create_if_missing=True)
        """
        import logging

        logger = logging.getLogger("droidrun")

        # Resolve path if enabled
        if use_path_resolver:
            try:
                resolved_path = PathResolver.resolve(path, must_exist=True)
                final_path = str(resolved_path)
            except FileNotFoundError:
                if create_if_missing:
                    # File doesn't exist, create it from defaults
                    resolved_path = PathResolver.resolve(path, create_if_missing=True)
                    final_path = str(resolved_path)

                    # Ensure parent directory exists
                    os.makedirs(os.path.dirname(final_path) or ".", exist_ok=True)

                    # Create default config
                    default_config = cls()
                    with open(final_path, "w", encoding="utf-8") as f:
                        yaml.dump(
                            default_config.to_dict(),
                            f,
                            sort_keys=False,
                            default_flow_style=False,
                        )
                    logger.info(f"Created default config at: {final_path}")
                    return default_config
                else:
                    raise
        else:
            final_path = path
            if not os.path.exists(final_path):
                if create_if_missing:
                    # Create default config
                    os.makedirs(os.path.dirname(final_path) or ".", exist_ok=True)
                    default_config = cls()
                    with open(final_path, "w", encoding="utf-8") as f:
                        yaml.dump(
                            default_config.to_dict(),
                            f,
                            sort_keys=False,
                            default_flow_style=False,
                        )
                    logger.info(f"Created default config at: {final_path}")
                    return default_config
                else:
                    raise FileNotFoundError(f"Config file not found: {final_path}")

        with open(final_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if data:
                try:
                    return cls.from_dict(data)
                except Exception as e:
                    logger.warning(
                        f"Failed to parse config from {final_path}, using defaults: {e}"
                    )
                    return cls()
            else:
                logger.warning(f"Empty config file at {final_path}, using defaults")
                return cls()
