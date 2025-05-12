import platform
import sys
import asyncio

def print_environment_info():
    print("===== システム情報 =====")
    print(f"OS: {platform.system()} {platform.release()} ({platform.version()})")
    print(f"マシン: {platform.machine()}")
    print(f"プロセッサ: {platform.processor()}")
    print(f"Python バージョン: {platform.python_version()} ({platform.python_implementation()})")

    try:
        import importlib.metadata
        bleak_version = importlib.metadata.version("bleak")
        print(f"Bleak バージョン: {bleak_version}")
    except Exception as e:
        print(f"Bleak のバージョン取得に失敗しました: {e}")

    print("=======================")

async def get_ble_adapter_info():
    print("===== Bluetooth アダプタ確認 =====")
    try:
        from bleak import BleakScanner

        devices = await BleakScanner.discover(timeout=5.0)
        if devices:
            print(f"Bluetooth アダプタは正常に動作しています。{len(devices)} 台のデバイスを検出しました。")
            for device in devices[:3]:
                print(f"- {device.name} ({device.address}), RSSI={device.rssi}")
        else:
            print("Bluetooth アダプタは検出されましたが、近くにデバイスが見つかりませんでした。")
    except Exception as e:
        print(f"Bluetooth スキャン中にエラーが発生しました: {e}")
    print("=======================")

if __name__ == "__main__":
    print_environment_info()
    asyncio.run(get_ble_adapter_info())
