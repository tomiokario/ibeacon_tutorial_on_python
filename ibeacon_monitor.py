import asyncio
import signal
from uuid import UUID
from datetime import datetime
from construct import Struct, Const, Int16ub, Int8sl, Array, Byte, ConstructError
from bleak import BleakScanner

# RSSIの閾値
RSSI_THRESHOLD = -200

# iBeaconのデータ構造を定義
ibeacon_format = Struct(
    "prefix" / Const(b"\x02\x15"),
    "uuid" / Array(16, Byte),
    "major" / Int16ub,
    "minor" / Int16ub,
    "tx_power" / Int8sl
)

# 対象UUIDと識別名の対応
TARGET_UUIDS = {
    # UUID: 裏面記載のMACアドレス
    UUID("E2C56DB5-DFFB-48D2-B060-D0F5A71096E1"): "C300 000D 537F",
    UUID("E2C56DB5-DFFB-48D2-B060-D0F5A71096E0"): "C300 000D 5382",
    UUID("E2C56DB5-DFFB-48D2-B060-D0F5A71096E2"): "C300 000D 5409"
}

# コールバック関数
def detection_callback(device, advertisement_data):
    manufacturer_data = advertisement_data.manufacturer_data
    if 0x004C in manufacturer_data:
        data = manufacturer_data[0x004C]
        try:
            parsed = ibeacon_format.parse(data)
            uuid = UUID(bytes=bytes(parsed.uuid))
            rssi = advertisement_data.rssi

            if uuid in TARGET_UUIDS and rssi >= RSSI_THRESHOLD:
                beacon_name = TARGET_UUIDS[uuid]
                timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                print(f"タイムスタンプ：{timestamp}")
                print(f"UUID：{uuid}")
                print(f"ビーコン名：{beacon_name}")
                print(f"RSSI：{rssi}")
                print("---------------------------------")

        except ConstructError:
            pass

# メイン関数
async def main():
    stop_event = asyncio.Event()

    def handle_shutdown():
        stop_event.set()

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, handle_shutdown)

    scanner = BleakScanner(detection_callback=detection_callback)
    await scanner.start()
    print("スキャンを開始しました。Ctrl+C で停止します。")

    await stop_event.wait()

    await scanner.stop()
    print("\nスキャンを停止しました。")

# エントリーポイント
if __name__ == "__main__":
    asyncio.run(main())
