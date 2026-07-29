import pandas as pd
import numpy as np
import requests
from datetime import datetime
import os
import time

CSV_FILE = "flight_history.csv"
# app.py と同じ VIP_DB をここにコピーして定義します (長いため一部省略)
VIP_DB = {
    "862000": {"country": "日本", "type": "B777-300ER", "reg": "80-1111", "owner": "航空自衛隊"},
        "862001": {"country": "日本", "type": "B777-300ER", "reg": "80-1112", "owner": "航空自衛隊"},
        "adfdf8": {"country": "アメリカ", "type": "VC-25A (AF1)", "reg": "82-8000", "owner": "US Air Force"},
        "adfdf9": {"country": "アメリカ", "type": "VC-25A (AF1)", "reg": "92-9000", "owner": "US Air Force"},
        "ae0006": {"country": "アメリカ", "type": "C-32A (AF2)", "reg": "98-0001", "owner": "US Air Force"},
        "ae0022": {"country": "アメリカ", "type": "C-32A (AF2)", "reg": "99-0004", "owner": "US Air Force"},
        "43c6f5": {"country": "イギリス", "type": "A330 MRTT", "reg": "ZZ336", "owner": "Royal Air Force"},
        "3e110c": {"country": "ドイツ", "type": "A350-900", "reg": "10+01", "owner": "German Air Force"},
        "3e1271": {"country": "ドイツ", "type": "A350-900", "reg": "10+02", "owner": "German Air Force"},
        "3b77da": {"country": "フランス", "type": "A330-200", "reg": "F-RARF", "owner": "French Air Force"},
        "71BE43": {"country": "韓国", "type": "B747-8I", "reg": "21001", "owner": "Republic of Korea Air Force"},
        "c2b3ea": {"country": "カナダ", "type": "CC-150", "reg": "15001", "owner": "Royal Canadian Air Force"},
        "7cf9d6": {"country": "オーストラリア", "type": "B737-700", "reg": "A39-007", "owner": "Royal Australian Air Force"},
        "480c00": {"country": "オランダ", "type": "B737-700", "reg": "PH-GOV", "owner": "Netherlands Government"},
        "4b8277": {"country": "トルコ", "type": "B747-8I", "reg": "TC-TRK", "owner": "Turkish Government"},
        "800c01": {"country": "インド", "type": "B777-300ER", "reg": "K7066", "owner": "Indian Air Force"},
        "e400d3": {"country": "ブラジル", "type": "A319", "reg": "FAB2101", "owner": "Brazilian Air Force"},
        "3101b0": {"country": "イタリア", "type": "A319", "reg": "MM62243", "owner": "Italian Air Force"},
        "899015": {"country": "台湾", "type": "B737-800", "reg": "3701", "owner": "Republic of China Air Force"},
        "341050": {"country": "スペイン", "type": "A310", "reg": "T.22-1", "owner": "Spanish Air Force"},
        
        # 追加データ
        "010024": {"country": "エジプト", "type": "エアバス A340-211", "reg": "SU-GGG", "owner": "エジプト政府"},
        "010230": {"country": "エジプト", "type": "ボーイング747-8", "reg": "SU-EGY", "owner": "エジプト政府"},
        "07a200": {"country": "エスワティニ", "type": "マクドネル・ダグラス MD-87", "reg": "3DC-SWZ", "owner": "エスワティニ政府"},
        "07a201": {"country": "エスワティニ", "type": "エアバス A340-313", "reg": "3DC-SDF", "owner": "エスワティニ政府"},
        "09a01a": {"country": "ガンビア", "type": "Il-62M", "reg": "C5-RTG", "owner": "ガンビア政府"},
        "09a01e": {"country": "ガンビア", "type": "ボンバルディア チャレンジャー 601", "reg": "C5-AFT", "owner": "ガンビア政府"},
        "04c030": {"country": "ケニア", "type": "フォッカー 70", "reg": "KAF308", "owner": "ケニア政府"},
        "038084": {"country": "コートジボワール", "type": "ガルフストリーム IV", "reg": "TU-VAD", "owner": "コートジボワール政府"},
        "098014": {"country": "ジブチ", "type": "ダッソー ファルコン 7X", "reg": "J2-HPV", "owner": "ジブチ政府"},
        "08001f": {"country": "タンザニア", "type": "フォッカー 50", "reg": "5H-TGF", "owner": "タンザニア政府"},
        "08000f": {"country": "タンザニア", "type": "ガルフストリーム G550", "reg": "5H-ONE", "owner": "タンザニア政府"},
        "201001": {"country": "ナミビア", "type": "ダッソー ファルコン 900B", "reg": "V5-NAM", "owner": "ナミビア政府"},
        "20103f": {"country": "ナミビア", "type": "ダッソー ファルコン 7X", "reg": "V5-GON", "owner": "ナミビア政府"},
        "09c008": {"country": "ブルキナ・ファソ", "type": "ボーイング727-282", "reg": "XT-BFA", "owner": "ブルキナ・ファソ政府"},
        "030012": {"country": "ボツワナ", "type": "ボンバルディア グローバル・エクスプレス", "reg": "OK1", "owner": "ボツワナ政府"},
        "00aec9": {"country": "南アフリカ", "type": "ボーイング737-7ED BBJ", "reg": "ZS-RSA", "owner": "南アフリカ政府"},
        "018021": {"country": "リビア", "type": "エアバスA340-213", "reg": "5A-ONE", "owner": "リビア政府"},
        "05e0bb": {"country": "モーリタニア", "type": "ボーイング737-7BQ BBJ", "reg": "5T-ONE", "owner": "モーリタニア政府"},
        "0200cc": {"country": "モロッコ", "type": "ボーイング737-8KB BBJ", "reg": "CN-MVI", "owner": "モロッコ政府"},
        "02000f": {"country": "モロッコ", "type": "ボーイング747-428", "reg": "CN-RGA", "owner": "モロッコ政府"},
        "020130": {"country": "モロッコ", "type": "ボーイング747-8Z5 BBJ", "reg": "CN-MBH", "owner": "モロッコ政府"},
        "020125": {"country": "モロッコ", "type": "BAe Avro RJ100", "reg": "CN-MSM", "owner": "モロッコ政府"},
        "600be9": {"country": "アゼルバイジャン", "type": "ボーイング777-200LR", "reg": "4K-AI001", "owner": "アゼルバイジャン政府"},
        "600806": {"country": "アゼルバイジャン", "type": "ガルフストリーム G550", "reg": "4K-AI06", "owner": "アゼルバイジャン政府"},
        "600bc0": {"country": "アゼルバイジャン", "type": "エアバス A340-642 ACJ", "reg": "4K-AI08", "owner": "アゼルバイジャン政府"},
        "600858": {"country": "アゼルバイジャン", "type": "ガルフストリーム G650", "reg": "4K-AZ88", "owner": "アゼルバイジャン政府"},
        "600b78": {"country": "アゼルバイジャン", "type": "ガルフストリーム G450", "reg": "4K-AZ888", "owner": "アゼルバイジャン政府"},
        "600801": {"country": "アゼルバイジャン", "type": "エアバス A319-115 ACJ", "reg": "4K-8888", "owner": "アゼルバイジャン政府"},
        "60003c": {"country": "イラン", "type": "エアバス A321-231", "reg": "EP-IGD", "owner": "イラン政府"},
        "7324e1": {"country": "イラン", "type": "エアバス A340-313", "reg": "EP-IGA", "owner": "イラン政府"},
        "7324e5": {"country": "イラン", "type": "BAe Avro RJ85", "reg": "EP-IGE", "owner": "イラン政府"},
        "7324e6": {"country": "イラン", "type": "BAe Avro RJ85", "reg": "EP-IGF", "owner": "イラン政府"},
        "7324e3": {"country": "イラン", "type": "ダッソー ファルコン 900", "reg": "EP-IGC", "owner": "イラン政府"},
        "800585": {"country": "インド", "type": "ボーイング777-337(ER)", "reg": "K7066", "owner": "インド政府"},
        "800c3d": {"country": "インド", "type": "ボーイング777-337(ER)", "reg": "K7067", "owner": "インド政府"},
        "8a0002": {"country": "インドネシア", "type": "ボーイング 737-8U3 BBJ2", "reg": "A-001", "owner": "インドネシア政府"},
        "8a0452": {"country": "インドネシア", "type": "Boeing 777-3U3(ER)", "reg": "PK-GIG", "owner": "インドネシア政府"},
        "8a0855": {"country": "インドネシア", "type": "BAe Avro RJ85", "reg": "PK-PJJ", "owner": "インドネシア政府"},
        "507c4f": {"country": "ウズベキスタン", "type": "ボーイング787-8", "reg": "UK001", "owner": "ウズベキスタン政府"},
        "507c53": {"country": "ウズベキスタン", "type": "エアバスA320-200", "reg": "UK002", "owner": "ウズベキスタン政府"},
        "507c3c": {"country": "ウズベキスタン", "type": "エアバスA320-200", "reg": "UK32000", "owner": "ウズベキスタン政府"},
        "70c0ba": {"country": "オマーン", "type": "エアバス A319-133 ACJ", "reg": "A4O-AJ", "owner": "オマーン政府"},
        "70c057": {"country": "オマーン", "type": "エアバス A320-232", "reg": "A4O-AA", "owner": "オマーン政府"},
        "70c04d": {"country": "オマーン", "type": "ボーイング747-430", "reg": "A4O-OMN", "owner": "オマーン政府"},
        "70c0b7": {"country": "オマーン", "type": "ボーイング 747-8H0 BBJ", "reg": "A4O-HMS", "owner": "オマーン政府"},
        "683037": {"country": "カザフスタン", "type": "ボーイング757-2M6", "reg": "UP-B5701", "owner": "カザフスタン政府"},
        "683011": {"country": "カザフスタン", "type": "ボーイング767-2DX(ER)", "reg": "UN-B6701", "owner": "カザフスタン政府"},
        "6830a5": {"country": "カザフスタン", "type": "エアバス A320-214 ACJ", "reg": "UP-A2001", "owner": "カザフスタン政府"},
        "68322e": {"country": "カザフスタン", "type": "エアバス A321-211 ACJ", "reg": "UP-A2101", "owner": "カザフスタン政府"},
        "6830ed": {"country": "カザフスタン", "type": "エアバス A330-243", "reg": "UP-A3001", "owner": "カザフスタン政府"},
        "683087": {"country": "カザフスタン", "type": "CRJ-200ER", "reg": "UP-C8502", "owner": "カザフスタン政府"},
        "7806fd": {"country": "カンボジア", "type": "エアバス A320-214", "reg": "B-6738", "owner": "カンボジア政府"},
        "60100d": {"country": "キルギス", "type": "Tu-154M", "reg": "EX-00001", "owner": "キルギス政府"},
        "885332": {"country": "タイ王国", "type": "エアバス A319-115 (ACJ)", "reg": "HS-TYR", "owner": "タイ王国空軍"},
        "885334": {"country": "タイ王国", "type": "エアバス A320-214 ACJ", "reg": "HS-TYT", "owner": "タイ王国空軍"},
        "885336": {"country": "タイ王国", "type": "エアバス A340-541", "reg": "HS-TYV", "owner": "タイ王国政府"},
        "881b6d": {"country": "タイ王国", "type": "ATR 72-500", "reg": "60313", "owner": "タイ王国空軍"},
        "881c62": {"country": "タイ王国", "type": "ATR 72-500", "reg": "60314", "owner": "タイ王国政府"},
        "881b6e": {"country": "タイ王国", "type": "ATR 72-500", "reg": "60315", "owner": "タイ王国空軍"},
        "881b6f": {"country": "タイ王国", "type": "ATR 72-500", "reg": "60316", "owner": "タイ王国空軍"},
        "880db6": {"country": "タイ王国", "type": "ボーイング737-4Z6", "reg": "HS-CMV", "owner": "タイ王室"},
        "882248": {"country": "タイ王国", "type": "ボーイング737-448", "reg": "HS-HRH", "owner": "タイ王国政府"},
        "8821ab": {"country": "タイ王国", "type": "ボーイング737-8Z6", "reg": "HS-HMK", "owner": "タイ王室"},
        "8836d3": {"country": "タイ王国", "type": "ボーイング737-8Z6", "reg": "HS-MVS", "owner": "タイ王室"},
        "4b85cb": {"country": "トルコ", "type": "エアバス A319-133 ACJ", "reg": "TC-IST", "owner": "トルコ政府"},
        "4bd2b2": {"country": "トルコ", "type": "エアバス A330-243", "reg": "TC-TUR", "owner": "トルコ政府"},
        "4b8c2e": {"country": "トルコ", "type": "エアバス A330-243", "reg": "TC-TUR", "owner": "トルコ政府"},
        "4bd24b": {"country": "トルコ", "type": "ボーイング 747-8ZV BBJ", "reg": "TC-TRK", "owner": "トルコ政府"},
        "60185a": {"country": "トルクメニスタン", "type": "ボーイング737-7GL", "reg": "EZ-A007", "owner": "トルクメニスタン政府"},
        "601831": {"country": "トルクメニスタン", "type": "ボーイング737-72K BBJ", "reg": "EZ-A700", "owner": "トルクメニスタン政府"},
        "601861": {"country": "トルクメニスタン", "type": "ボーイング777-22K(LR)", "reg": "EZ-A700", "owner": "トルクメニスタン政府"},
        "60183e": {"country": "トルクメニスタン", "type": "Challenger 850", "reg": "EZ-B024", "owner": "トルクメニスタン政府"},
        "762af3": {"country": "パキスタン", "type": "ガルフストリーム IV SP", "reg": "J-755", "owner": "パキスタン政府"},
        "762bf4": {"country": "パキスタン", "type": "ガルフストリーム G450", "reg": "J-756", "owner": "パキスタン政府"},
        "7602f5": {"country": "パキスタン", "type": "エアバス A310-304", "reg": "J-757", "owner": "パキスタン政府"},
        "894014": {"country": "バーレーン", "type": "ボーイング747-4P8", "reg": "A9C-HMK", "owner": "バーレーン政府"},
        "894082": {"country": "バーレーン", "type": "ボーイング767-4FS(ER)", "reg": "A9C-HMH", "owner": "バーレーン政府"},
        "894016": {"country": "バーレーン", "type": "ボーイング767-4FS(ER)", "reg": "A9C-HWR", "owner": "バーレーン政府"},
        "8953c7": {"country": "ブルネイ", "type": "ボーイング767-27G(ER)", "reg": "V8-MHB", "owner": "ブルネイ政府"},
        "8953df": {"country": "ブルネイ", "type": "ボーイング747-8LQ BBJ", "reg": "V8-BKH", "owner": "ブルネイ政府"},
        "8953e3": {"country": "ブルネイ", "type": "ボーイング787-8 BBJ", "reg": "V8-BKH", "owner": "ブルネイ政府"},
        "750156": {"country": "マレーシア", "type": "エアバスA319-115 ACJ", "reg": "9M-NAA", "owner": "マレーシア政府"},
        "75026d": {"country": "マレーシア", "type": "エアバスA320-214 ACJ", "reg": "9M-NAB", "owner": "マレーシア政府"},
        "7500c5": {"country": "マレーシア", "type": "Global Express", "reg": "M48-02", "owner": "マレーシア政府"},
        "758001": {"country": "フィリピン", "type": "フォッカー F28", "reg": "RP-1250", "owner": "フィリピン政府"},
        "758674": {"country": "フィリピン", "type": "ガルフストリーム G280", "reg": "RP-1251", "owner": "フィリピン政府"},
        "899180": {"country": "台湾", "type": "フォッカー 50", "reg": "5001", "owner": "台湾政府"},
        "899181": {"country": "台湾", "type": "フォッカー 50", "reg": "5002", "owner": "台湾政府"},
        "899182": {"country": "台湾", "type": "フォッカー 50", "reg": "5003", "owner": "台湾政府"},
        "e200dd": {"country": "アルゼンチン", "type": "ボーイング757-200", "reg": "ARG-01", "owner": "アルゼンチン政府"},
        "e01645": {"country": "アルゼンチン", "type": "ボーイング737-500", "reg": "ARG-02", "owner": "アルゼンチン政府"},
        "e84035": {"country": "エクアドル", "type": "Legacy 600", "reg": "FAE-051", "owner": "エクアドル政府"},
        "e84834": {"country": "エクアドル", "type": "ダッソー ファルコン 7X", "reg": "FAE-052", "owner": "エクアドル政府"},
        "c2b355": {"country": "カナダ", "type": "エアバス CC-150 ポラリス", "reg": "15001", "owner": "カナダ政府"},
        "c2c363": {"country": "カナダ", "type": "エアバス CC-330 ハスキー", "reg": "330002", "owner": "カナダ政府"},
        "0ac3a8": {"country": "コロンビア", "type": "ボーイング 737-74V BBJ", "reg": "FAC0001", "owner": "コロンビア政府"},
        "0ac005": {"country": "コロンビア", "type": "フォッカー F28", "reg": "FAC0002", "owner": "コロンビア政府"},
        "e80642": {"country": "チリ", "type": "ボーイング737-58N", "reg": "921", "owner": "チリ政府"},
        "e80647": {"country": "チリ", "type": "ボーイング737-330(QC)", "reg": "922", "owner": "チリ政府"},
        "e80648": {"country": "チリ", "type": "ボーイング767-3Y0(ER)", "reg": "985", "owner": "チリ政府"},
        "e400d9": {"country": "ブラジル", "type": "エアバス VC-1A", "reg": "FAB2101", "owner": "ブラジル政府"},
        "e483ba": {"country": "ブラジル", "type": "エンブラエル VC-2", "reg": "FAB2590", "owner": "ブラジル政府"},
        "e483bb": {"country": "ブラジル", "type": "エンブラエル VC-2", "reg": "FAB2591", "owner": "ブラジル政府"},
        "e8c007": {"country": "ペルー", "type": "ボーイング737-500", "reg": "FAP356", "owner": "ペルー政府"},
        "e940fa": {"country": "ボリビア", "type": "ダッソー ファルコン 900EX", "reg": "FAB-001", "owner": "ボリビア政府"},
        "e940fb": {"country": "ボリビア", "type": "ダッソー ファルコン 50", "reg": "FAB-002", "owner": "ボリビア政府"},
        "0d01e0": {"country": "メキシコ", "type": "ボーイング737-2B7(A)", "reg": "3520", "owner": "メキシコ政府"},
        "0d003f": {"country": "メキシコ", "type": "ボーイング737-7ED BBJ", "reg": "3529", "owner": "メキシコ政府"},
        "0d0914": {"country": "メキシコ", "type": "ガルフストリーム G100", "reg": "3915", "owner": "メキシコ政府"},
        "0d088c": {"country": "メキシコ", "type": "ガルフストリーム G550", "reg": "3910", "owner": "メキシコ政府"},
        "0d0795": {"country": "メキシコ", "type": "ボーイング787-8", "reg": "XC-MEX", "owner": "メキシコ政府"},
        "4ca204": {"country": "アイルランド", "type": "リアジェット45", "reg": "258", "owner": "アイルランド政府"},
        "4b85c1": {"country": "アルバニア", "type": "エアバス A319-115 (ACJ)", "reg": "TC-ANA", "owner": "アルバニア政府"},
        "43c146": {"country": "イギリス", "type": "BAe 146", "reg": "ZE700", "owner": "イギリス政府"},
        "43c147": {"country": "イギリス", "type": "BAe 146", "reg": "ZE701", "owner": "イギリス政府"},
        "43c6f9": {"country": "イギリス", "type": "エアバス A330-200MRTT", "reg": "ZZ336", "owner": "イギリス政府"},
        "407a3f": {"country": "イギリス", "type": "エアバス A321neo", "reg": "G-GBNI", "owner": "イギリス政府"},
        "33fff9": {"country": "イタリア", "type": "エアバス A319-115 (ACJ)", "reg": "MM62174", "owner": "イタリア政府"},
        "33ffc1": {"country": "イタリア", "type": "エアバス A319-115 (ACJ)", "reg": "MM62209", "owner": "イタリア政府"},
        "30064a": {"country": "イタリア", "type": "エアバス A340-541", "reg": "I-TALY", "owner": "イタリア政府"},
        "50815f": {"country": "ウクライナ", "type": "エアバス A319-115 ACJ", "reg": "UR-ABA", "owner": "ウクライナ政府"},
        "4840ce": {"country": "オランダ", "type": "フォッカー 70", "reg": "PH-KBX", "owner": "オランダ政府"},
        "485920": {"country": "オランダ", "type": "ボーイング 737-700 BBJ", "reg": "PH-GOV", "owner": "オランダ政府"},
        "4c8092": {"country": "キプロス", "type": "Legacy 600", "reg": "CAF-001", "owner": "キプロス政府"},
        "4680d1": {"country": "クロアチア", "type": "Challenger 604", "reg": "9A-CRO", "owner": "クロアチア政府"},
        "4682a6": {"country": "ギリシャ", "type": "ガルフストリーム V", "reg": "678", "owner": "ギリシャ政府"},
        "468111": {"country": "ギリシャ", "type": "ダッソー ファルコン 7X", "reg": "273", "owner": "ギリシャ政府"},
        "354555": {"country": "スペイン", "type": "エアバス A310-304", "reg": "T.22-1", "owner": "スペイン政府"},
        "354556": {"country": "スペイン", "type": "エアバス A310-304", "reg": "T.22-2", "owner": "スペイン政府"},
        "341390": {"country": "スペイン", "type": "ダッソー ファルコン 900", "reg": "T.18-1", "owner": "スペイン政府"},
        "341391": {"country": "スペイン", "type": "ダッソー ファルコン 900", "reg": "T.18-2", "owner": "スペイン政府"},
        "3542c3": {"country": "スペイン", "type": "ダッソー ファルコン 900", "reg": "T.18-3", "owner": "スペイン政府"},
        "3542c4": {"country": "スペイン", "type": "ダッソー ファルコン 900", "reg": "T.18-4", "owner": "スペイン政府"},
        "3542c5": {"country": "スペイン", "type": "ダッソー ファルコン 900", "reg": "T.18-5", "owner": "スペイン政府"},
        "4a8199": {"country": "スウェーデン", "type": "TP 102 C", "reg": "102004", "owner": "スウェーデン政府"},
        "4a822a": {"country": "スウェーデン", "type": "TP 102 D", "reg": "102005", "owner": "スウェーデン政府"},
        "4b7f44": {"country": "スイス", "type": "Challenger 604", "reg": "T-751", "owner": "スイス政府"},
        "4b7f43": {"country": "スイス", "type": "Challenger 604", "reg": "T-752", "owner": "スイス政府"},
        "4b7fd4": {"country": "スイス", "type": "Citation Excel", "reg": "T-784", "owner": "スイス政府"},
        "4b7f4c": {"country": "スイス", "type": "ダッソー ファルコン 900", "reg": "T-785", "owner": "スイス政府"},
        "4b7f45": {"country": "スイス", "type": "ピラタス PC-24", "reg": "T-786", "owner": "スイス政府"},
        "505c06": {"country": "スロバキア", "type": "エアバス A319-115 ACJ", "reg": "OM-BYA", "owner": "スロバキア政府"},
        "505c09": {"country": "スロバキア", "type": "エアバス A319-115 ACJ", "reg": "OM-BYK", "owner": "スロバキア政府"},
        "505c07": {"country": "スロバキア", "type": "フォッカー 100", "reg": "OM-BYB", "owner": "スロバキア政府"},
        "505c08": {"country": "スロバキア", "type": "フォッカー 100", "reg": "OM-BYC", "owner": "スロバキア政府"},
        "506f24": {"country": "スロベニア", "type": "ダッソー ファルコン 2000EX", "reg": "L1-01", "owner": "スロベニア政府"},
        "4c4a21": {"country": "セルビア", "type": "Legacy", "reg": "YU-SRB", "owner": "セルビア政府"},
        "4c05a0": {"country": "セルビア", "type": "ダッソー ファルコン 50", "reg": "YU-BNA", "owner": "セルビア政府"},
        "498422": {"country": "チェコ", "type": "エアバス A319-115 ACJ", "reg": "2801", "owner": "チェコ政府"},
        "498421": {"country": "チェコ", "type": "エアバス A319-115 ACJ", "reg": "3085", "owner": "チェコ政府"},
        "498426": {"country": "チェコ", "type": "Challenger 600", "reg": "5105", "owner": "チェコ政府"},
        "45f424": {"country": "デンマーク", "type": "Challenger 604", "reg": "C-168", "owner": "デンマーク政府"},
        "45f426": {"country": "デンマーク", "type": "Challenger 604", "reg": "C-215", "owner": "デンマーク政府"},
        "477ff6": {"country": "ハンガリー", "type": "ダッソー ファルコン 7X", "reg": "606", "owner": "ハンガリー政府"},
        "477ff7": {"country": "ハンガリー", "type": "ダッソー ファルコン 7X", "reg": "074", "owner": "ハンガリー政府"},
        "477ff4": {"country": "ハンガリー", "type": "エアバスA319", "reg": "604", "owner": "ハンガリー政府"},
        "477ff5": {"country": "ハンガリー", "type": "エアバスA319", "reg": "605", "owner": "ハンガリー政府"},
        "451e92": {"country": "ブルガリア", "type": "エアバスA319", "reg": "LZ-AOB", "owner": "ブルガリア政府"},
        "51002b": {"country": "ベラルーシ", "type": "ボーイング737-8EV BBJ2", "reg": "EW-001PA", "owner": "ベラルーシ政府"},
        "51005e": {"country": "ベラルーシ", "type": "ボーイング767-32K(ER)", "reg": "EW-001PB", "owner": "ベラルーシ政府"},
        "510055": {"country": "ベラルーシ", "type": "Challenger 850", "reg": "EW-301PJ", "owner": "ベラルーシ政府"},
        "48d960": {"country": "ポーランド", "type": "ガルフストリーム G550", "reg": "0001", "owner": "ポーランド政府"},
        "48d961": {"country": "ポーランド", "type": "ガルフストリーム G550", "reg": "0002", "owner": "ポーランド政府"},
        "48d980": {"country": "ポーランド", "type": "ボーイング737-86X", "reg": "0110", "owner": "ポーランド政府"},
        "48d982": {"country": "ポーランド", "type": "ボーイング737-8TV BBJ2", "reg": "0111", "owner": "ポーランド政府"},
        "48d981": {"country": "ポーランド", "type": "ボーイング737-8TV BBJ2", "reg": "0112", "owner": "ポーランド政府"},
        "48ad06": {"country": "ポーランド", "type": "ERJ-175LR", "reg": "SP-LIG", "owner": "ポーランド政府"},
        "48ad07": {"country": "ポーランド", "type": "ERJ-175LR", "reg": "SP-LIH", "owner": "ポーランド政府"},
        "497c71": {"country": "ポルトガル", "type": "ダッソー ファルコン 50", "reg": "17401", "owner": "ポルトガル政府"},
        "497c72": {"country": "ポルトガル", "type": "ダッソー ファルコン 50", "reg": "17402", "owner": "ポルトガル政府"},
        "497c73": {"country": "ポルトガル", "type": "ダッソー ファルコン 50", "reg": "17403", "owner": "ポルトガル政府"},
        "4d403f": {"country": "モナコ", "type": "ダッソー ファルコン 8X", "reg": "3A-MGA", "owner": "モナコ政府"},
        "516001": {"country": "モンテネグロ", "type": "リアジェット45", "reg": "4O-MNE", "owner": "モンテネグロ政府"},
        "7cf85c": {"country": "オーストラリア", "type": "ボーイング 737-7DT BBJ", "reg": "A36-001", "owner": "オーストラリア政府"},
        "7cf85d": {"country": "オーストラリア", "type": "ボーイング 737-7DF BBJ", "reg": "A36-002", "owner": "オーストラリア政府"},
        "7cf9c9": {"country": "オーストラリア", "type": "エアバス KC-30A", "reg": "A39-007", "owner": "オーストラリア政府"},
        "7cfa93": {"country": "オーストラリア", "type": "ボーイング 737 MAX 8 BBJ", "reg": "A62-001", "owner": "オーストラリア政府"},
        "c87f00": {"country": "ニュージーランド", "type": "ボーイング757-2K2(C)", "reg": "NZ7571", "owner": "ニュージーランド政府"},
        "c87f01": {"country": "ニュージーランド", "type": "ボーイング757-2K2(C)", "reg": "NZ7572", "owner": "ニュージーランド政府"},
        "89804c": {"country": "パプアニューギニア", "type": "ダッソー ファルコン 900EX", "reg": "P2-ANW", "owner": "パプアニューギニア政府"}
}

def track_and_record():
    try:
        airports_df = pd.read_csv("https://davidmegginson.github.io/ourairports-data/airports.csv")
        airports_df = airports_df[airports_df['type'].isin(['large_airport', 'medium_airport'])]
    except:
        airports_df = pd.DataFrame()

    def get_nearest_airport(lat, lon):
        if airports_df.empty or pd.isna(lat) or pd.isna(lon): return "不明", "---", "----"
        lat1, lon1 = np.radians(lat), np.radians(lon)
        lat2, lon2 = np.radians(airports_df['latitude_deg']), np.radians(airports_df['longitude_deg'])
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
        distances = 6371 * c
        nearest = airports_df.loc[distances.idxmin()]
        return nearest['name'], nearest['iata_code'] if pd.notna(nearest['iata_code']) else "---", nearest['ident'] if pd.notna(nearest['ident']) else "----"

    current_time_obj = datetime.now()
    active_flights = {}
    
    # 【注意】 GitHub Actions環境は毎回リセットされるため、継続的な監視(while True)ではなく、
    # 実行されたその瞬間のスナップショットだけを取得し、履歴としてCSVに追記するシンプルな作りに変更します。
    try:
        url = "https://opensky-network.org/api/states/all"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            states = response.json().get("states", [])
            completed_flights = []
            
            for flight in states:
                if not flight: continue
                icao24 = str(flight[0]).lower()
                lon, lat = flight[5], flight[6]
                
                if icao24 in VIP_DB and lat and lon:
                    info = VIP_DB[icao24]
                    dep_name, dep_iata, dep_icao = get_nearest_airport(lat, lon) # 出発/到着を厳密に追えないため現在地の最寄りとする
                    
                    completed_flights.append({
                        "Hex": icao24, 
                        "レジ番号": info["reg"], 
                        "所属国": info["country"],
                        "記録時刻": current_time_obj.strftime('%Y-%m-%d %H:%M:%S'),
                        "現在地最寄り空港": f"{dep_name} ({dep_iata} / {dep_icao})",
                        "緯度": lat,
                        "経度": lon
                    })
            
            if completed_flights:
                df_new = pd.DataFrame(completed_flights)
                if not os.path.isfile(CSV_FILE):
                    df_new.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")
                else:
                    df_new.to_csv(CSV_FILE, mode='a', header=False, index=False, encoding="utf-8-sig")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    track_and_record()