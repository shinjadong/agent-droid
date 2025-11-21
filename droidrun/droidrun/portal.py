"""
Portal APK 관리 및 기기 통신 유틸리티.

이 모듈은 Android 기기에서 DroidRun Portal 앱을 다운로드, 설치 및 관리합니다.
또한 접근성 서비스 상태를 확인하고 기기 통신 모드(TCP 및 콘텐츠 제공자)를 관리하는
유틸리티를 제공합니다.
"""

import asyncio
import contextlib
import os
import tempfile

import requests
from rich.console import Console

from droidrun.tools import AdbTools
from async_adbutils import AdbDevice, adb

REPO = "droidrun/droidrun-portal"
ASSET_NAME = "droidrun-portal"
GITHUB_API_HOSTS = ["https://api.github.com", "https://ungh.cc"]

PORTAL_PACKAGE_NAME = "com.droidrun.portal"
A11Y_SERVICE_NAME = (
    f"{PORTAL_PACKAGE_NAME}/com.droidrun.portal.DroidrunAccessibilityService"
)


def get_latest_release_assets(debug: bool = False):
    """
    GitHub에서 최신 Portal APK 릴리스 자산을 가져옵니다.

    Args:
        debug: 디버그 로깅 활성화

    Returns:
        최신 GitHub 릴리스의 자산 딕셔너리 목록

    Raises:
        requests.HTTPError: GitHub API 요청이 실패하는 경우
    """
    for host in GITHUB_API_HOSTS:
        url = f"{host}/repos/{REPO}/releases/latest"
        response = requests.get(url)
        if response.status_code == 200:
            if debug:
                print(f"Using GitHub release on {host}")
            break

    response.raise_for_status()
    latest_release = response.json()

    if "release" in latest_release:
        assets = latest_release["release"]["assets"]
    else:
        assets = latest_release.get("assets", [])

    return assets


@contextlib.contextmanager
def download_portal_apk(debug: bool = False):
    """
    GitHub 릴리스에서 최신 Portal APK를 다운로드합니다.

    이 컨텍스트 매니저는 APK를 임시 파일에 다운로드하고 파일 경로를 반환합니다.
    컨텍스트가 종료되면 파일이 자동으로 삭제됩니다.

    Args:
        debug: 디버그 로깅 활성화

    Yields:
        str: 다운로드된 APK 파일 경로

    Raises:
        Exception: 릴리스에서 Portal APK 자산을 찾을 수 없는 경우
        requests.HTTPError: 다운로드가 실패하는 경우
    """
    console = Console()
    assets = get_latest_release_assets(debug)

    asset_version = None
    asset_url = None
    for asset in assets:
        if (
            "browser_download_url" in asset
            and "name" in asset
            and asset["name"].startswith(ASSET_NAME)
        ):
            asset_url = asset["browser_download_url"]
            asset_version = asset["name"].split("-")[-1]
            asset_version = asset_version.removesuffix(".apk")
            break
        elif "downloadUrl" in asset and os.path.basename(
            asset["downloadUrl"]
        ).startswith(ASSET_NAME):
            asset_url = asset["downloadUrl"]
            asset_version: str = asset.get("name", os.path.basename(asset_url)).split(
                "-"
            )[-1]
            asset_version = asset_version.removesuffix(".apk")
            break
        else:
            if debug:
                print(asset)

    if not asset_url:
        raise Exception(f"Asset named '{ASSET_NAME}' not found in the latest release.")

    console.print(f"Found Portal APK [bold]{asset_version}[/bold]")
    if debug:
        console.print(f"Asset URL: {asset_url}")

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".apk")
    try:
        r = requests.get(asset_url, stream=True)
        r.raise_for_status()
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                tmp.write(chunk)
        tmp.close()
        yield tmp.name
    finally:
        if os.path.exists(tmp.name):
            os.unlink(tmp.name)


async def enable_portal_accessibility(
    device: AdbDevice, service_name: str = A11Y_SERVICE_NAME
):
    """
    기기에서 Portal 접근성 서비스를 활성화합니다.

    Args:
        device: ADB 기기 연결
        service_name: 전체 접근성 서비스 이름 (기본값: Portal 서비스)

    Note:
        보안 제한으로 인해 일부 기기에서 실패할 수 있습니다.
        수동 활성화가 필요할 수 있습니다.
    """
    await device.shell(
        f"settings put secure enabled_accessibility_services {service_name}"
    )
    await device.shell("settings put secure accessibility_enabled 1")


async def check_portal_accessibility(
    device: AdbDevice, service_name: str = A11Y_SERVICE_NAME, debug: bool = False
) -> bool:
    """
    Portal 접근성 서비스가 활성화되어 있는지 확인합니다.

    Args:
        device: ADB 기기 연결
        service_name: 확인할 전체 접근성 서비스 이름
        debug: 디버그 로깅 활성화

    Returns:
        접근성 서비스가 활성화된 경우 True, 그렇지 않으면 False
    """
    a11y_services = await device.shell(
        "settings get secure enabled_accessibility_services"
    )
    if service_name not in a11y_services:
        if debug:
            print(a11y_services)
        return False

    a11y_enabled = await device.shell("settings get secure accessibility_enabled")
    if a11y_enabled != "1":
        if debug:
            print(a11y_enabled)
        return False

    return True


async def ping_portal(device: AdbDevice, debug: bool = False):
    """
    Droidrun Portal이 설치되어 있고 접근 가능한지 확인합니다.
    """
    try:
        packages = await device.list_packages()
    except Exception as e:
        raise Exception("Failed to list packages") from e

    if PORTAL_PACKAGE_NAME not in packages:
        if debug:
            print(packages)
        raise Exception("Portal is not installed on the device")

    if not await check_portal_accessibility(device, debug=debug):
        await device.shell("am start -a android.settings.ACCESSIBILITY_SETTINGS")
        raise Exception(
            "Droidrun Portal is not enabled as an accessibility service on the device"
        )


async def ping_portal_content(device: AdbDevice, debug: bool = False):
    """
    콘텐츠 제공자를 통해 Portal 접근성을 테스트합니다.

    Args:
        device: ADB 기기 연결
        debug: 디버그 로깅 활성화

    Raises:
        Exception: 콘텐츠 제공자를 통해 Portal에 도달할 수 없는 경우
    """
    try:
        state = await device.shell(
            "content query --uri content://com.droidrun.portal/state"
        )
        if "Row: 0 result=" not in state:
            raise Exception("Failed to get state from Droidrun Portal")
    except Exception as e:
        raise Exception("Droidrun Portal is not reachable") from e


async def ping_portal_tcp(device: AdbDevice, debug: bool = False):
    """
    TCP 모드를 통해 Portal 접근성을 테스트합니다.

    Args:
        device: ADB 기기 연결
        debug: 디버그 로깅 활성화

    Raises:
        Exception: TCP를 통해 Portal에 도달할 수 없거나 포트 포워딩이 실패하는 경우
    """
    try:
        tools = AdbTools(serial=device.serial, use_tcp=True)
        await tools.connect()
    except Exception as e:
        raise Exception("Failed to setup TCP forwarding") from e


async def set_overlay_offset(device: AdbDevice, offset: int):
    """
    /overlay_offset portal 콘텐츠 제공자 엔드포인트를 사용하여 오버레이 오프셋을 설정합니다.
    """
    try:
        cmd = f'content insert --uri "content://com.droidrun.portal/overlay_offset" --bind offset:i:{offset}'
        await device.shell(cmd)
    except Exception as e:
        raise Exception("Error setting overlay offset") from e


async def toggle_overlay(device: AdbDevice, visible: bool):
    """오버레이 표시 여부를 전환합니다.

    Args:
        device: 오버레이를 전환할 기기
        visible: 오버레이를 표시할지 여부

    throws:
        Exception: 오버레이 전환이 실패하는 경우
    """
    try:
        await device.shell(
            f"am broadcast -a com.droidrun.portal.TOGGLE_OVERLAY --ez overlay_visible {'true' if visible else 'false'}"
        )
    except Exception as e:
        raise Exception("Failed to toggle overlay") from e


async def setup_keyboard(device: AdbDevice):
    """
    DroidRun 키보드를 기본 입력 방법으로 설정합니다.
    저장/복원 없이 DroidRun 키보드로 전환하는 간단한 설정입니다.

    throws:
        Exception: 키보드 설정이 실패하는 경우
    """
    try:
        await device.shell("ime enable com.droidrun.portal/.DroidrunKeyboardIME")
        await device.shell("ime set com.droidrun.portal/.DroidrunKeyboardIME")
    except Exception as e:
        raise Exception("Error setting up keyboard") from e


async def disable_keyboard(
    device: AdbDevice, target_ime: str = "com.droidrun.portal/.DroidrunKeyboardIME"
):
    """
    특정 IME(키보드)를 비활성화하고 선택적으로 다른 키보드로 전환합니다.
    기본적으로 DroidRun 키보드를 비활성화합니다.

    Args:
        target_ime: 비활성화할 IME 패키지/액티비티 (기본값: DroidRun 키보드)

    Returns:
        bool: 성공적으로 비활성화된 경우 True, 그렇지 않으면 False
    """
    try:
        await device.shell(f"ime disable {target_ime}")
        return True
    except Exception as e:
        raise Exception("Error disabling keyboard") from e


async def test():
    device = await adb.device()
    await ping_portal(device, debug=False)


if __name__ == "__main__":
    asyncio.run(test())
