import asyncio
import csv
import os
from uuid import UUID
from datetime import datetime
from construct import Struct, Const, Int16ub, Int8sl, Array, Byte, ConstructError
from bleak import BleakScanner

# iBeaconのデータ構造を定義
ibeacon_format = Struct(
    "prefix" / Const(b"\x02\x15"),
    "uuid" / Array(16, Byte),
    "major" / Int16ub,
    "minor" / Int16ub,
    "tx_power" / Int8sl
)

# 対象のUUIDと対応するCSVファイル名を定義（ファイル名のみ、パスは後で付加）
TARGET_UUIDS = {
    UUID("E2C56DB5-DFFB-48D2-B060-D0F5A71096E1"): "ibeacon_log_96E1.csv", # C300 000D 537F
    UUID("E2C56DB5-DFFB-48D2-B060-D0F5A71096E0"): "ibeacon_log_96E0.csv"  # C300 000D 5382
}

# 検出されたデバイスの情報を保存する辞書
detected_devices = {uuid: [] for uuid in TARGET_UUIDS}

def detection_callback(device, advertisement_data):
    manufacturer_data = advertisement_data.manufacturer_data
    if 0x004C in manufacturer_data:
        data = manufacturer_data[0x004C]
        try:
            parsed = ibeacon_format.parse(data)
            uuid = UUID(bytes=bytes(parsed.uuid))
            if uuid not in TARGET_UUIDS:
                return
            major = parsed.major
            minor = parsed.minor
            tx_power = parsed.tx_power
            rssi = advertisement_data.rssi
            mac_address = device.address
            timestamp = datetime.now().isoformat()

            device_info = {
                "Timestamp": timestamp,
                "MAC Address": mac_address,
                "UUID": str(uuid),
                "Major": major,
                "Minor": minor,
                "TX Power": tx_power,
                "RSSI": rssi
            }

            detected_devices[uuid].append(device_info)
            print(f"検出: {device_info}")

        except ConstructError:
            pass

async def main():
    timestamp_dir = datetime.now().strftime("results/%Y%m%d_%H%M%S")
    os.makedirs(timestamp_dir, exist_ok=True)

    scanner = BleakScanner()
    scanner.register_detection_callback(detection_callback)
    await scanner.start()
    print("スキャンを開始します。10秒間スキャンを実行します。")
    await asyncio.sleep(10.0)
    await scanner.stop()
    print("スキャンを終了しました。")

    for uuid, devices in detected_devices.items():
        filename = os.path.join(timestamp_dir, TARGET_UUIDS[uuid])
        with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["Timestamp", "MAC Address", "UUID", "Major", "Minor", "TX Power", "RSSI"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for device in devices:
                writer.writerow(device)
        print(f"{filename} に検出結果を保存しました。")

asyncio.run(main())
