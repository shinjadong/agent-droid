import logging
import sys
from abc import ABC, abstractmethod
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Tuple

# 이 모듈에 대한 로거 가져오기
logger = logging.getLogger(__name__)


class Tools(ABC):
    """
    모든 도구의 추상 기본 클래스.
    이 클래스는 모든 도구가 구현할 공통 인터페이스를 제공합니다.
    """

    @staticmethod
    def ui_action(func):
        """
        UI를 수정하는 작업에 대한 스크린샷과 UI 상태를 캡처하는 데코레이터.
        """

        @wraps(func)
        async def wrapper(*args, **kwargs):
            self = args[0]
            result = await func(*args, **kwargs)

            # save_trajectories 속성이 존재하고 "action"으로 설정되어 있는지 확인
            if (
                hasattr(self, "save_trajectories")
                and self.save_trajectories == "action"
            ):
                frame = sys._getframe(1)
                caller_globals = frame.f_globals

                step_screenshots = caller_globals.get("step_screenshots")
                step_ui_states = caller_globals.get("step_ui_states")

                if step_screenshots is not None:
                    step_screenshots.append((await self.take_screenshot())[1])
                if step_ui_states is not None:
                    step_ui_states.append(await self.get_state())
            return result

        return wrapper

    @abstractmethod
    async def get_state(self) -> Dict[str, Any]:
        """
        도구의 현재 상태를 가져옵니다.
        """
        pass

    @abstractmethod
    async def get_date(self) -> str:
        """
        기기의 현재 날짜를 가져옵니다.
        """
        pass

    @abstractmethod
    async def tap_by_index(self, index: int) -> str:
        """
        주어진 인덱스의 요소를 탭합니다.
        """
        pass

    # @abstractmethod
    # async def tap_by_coordinates(self, x: int, y: int) -> bool:
    #    pass

    @abstractmethod
    async def swipe(
        self, start_x: int, start_y: int, end_x: int, end_y: int, duration_ms: int = 300
    ) -> bool:
        """
        주어진 시작 좌표에서 끝 좌표로 스와이프합니다.
        """
        pass

    @abstractmethod
    async def drag(
        self,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
        duration_ms: int = 3000,
    ) -> bool:
        """
        주어진 시작 좌표에서 끝 좌표로 드래그합니다.
        """
        pass

    @abstractmethod
    async def input_text(self, text: str, index: int = -1, clear: bool = False) -> str:
        """
        포커스된 입력 필드에 주어진 텍스트를 입력합니다.
        """
        pass

    @abstractmethod
    async def back(self) -> str:
        """
        뒤로 가기 버튼을 누릅니다.
        """
        pass

    @abstractmethod
    async def press_key(self, keycode: int) -> str:
        """
        주어진 키코드를 입력합니다.
        """
        pass

    @abstractmethod
    async def start_app(self, package: str, activity: str = "") -> str:
        """
        주어진 앱을 시작합니다.
        """
        pass

    @abstractmethod
    async def take_screenshot(self) -> Tuple[str, bytes]:
        """
        기기의 스크린샷을 캡처합니다.
        """
        pass

    @abstractmethod
    async def list_packages(self, include_system_apps: bool = False) -> List[str]:
        """
        기기의 모든 패키지를 나열합니다.
        """
        pass

    @abstractmethod
    async def get_apps(self, include_system_apps: bool = True) -> List[Dict[str, Any]]:
        """
        기기의 모든 앱을 나열합니다.
        """
        pass

    @abstractmethod
    def remember(self, information: str) -> str:
        """
        주어진 정보를 기억합니다. 이는 도구의 메모리에 정보를 저장하는 데 사용됩니다.
        """
        pass

    @abstractmethod
    async def get_memory(self) -> List[str]:
        """
        도구의 메모리를 가져옵니다.
        """
        pass

    @abstractmethod
    async def complete(self, success: bool, reason: str = "") -> None:
        """
        도구를 완료합니다. 이는 도구가 작업을 완료했음을 나타내는 데 사용됩니다.
        """
        pass

    @abstractmethod
    def _extract_element_coordinates_by_index(self, index: int) -> Tuple[int, int]:
        """
        주어진 인덱스의 요소 좌표를 추출합니다.
        """
        pass


def describe_tools(
    tools: Tools, exclude_tools: Optional[List[str]] = None
) -> Dict[str, Callable[..., Any]]:
    """
    주어진 Tools 인스턴스에 사용 가능한 도구들을 설명합니다.

    Args:
        tools: 설명할 Tools 인스턴스.
        exclude_tools: 설명에서 제외할 도구 이름 목록.

    Returns:
        도구 이름을 설명에 매핑하는 딕셔너리.
    """
    exclude_tools = exclude_tools or []

    description = {
        # UI 상호작용
        "swipe": tools.swipe,
        "input_text": tools.input_text,
        "press_key": tools.press_key,
        "tap_by_index": tools.tap_by_index,
        "drag": tools.drag,
        # 앱 관리
        "start_app": tools.start_app,
        "list_packages": tools.list_packages,
        # 상태 관리
        "remember": tools.remember,
        "complete": tools.complete,
    }

    # 제외된 도구 제거
    for tool_name in exclude_tools:
        description.pop(tool_name, None)

    return description
