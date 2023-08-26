from cmath import log
from distutils.sysconfig import PREFIX
import discord
#from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, date
import asyncio
#load_dotenv()
import mysql.connector
import pytz

PREFIX = os.environ['PREFIX']
TOKEN = os.environ['TOKEN']

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
korea_timezone = pytz.timezone('Asia/Seoul')

LOWBOSS_INFO = {
    '울리케': {'젠주기': 180, '젠위치': '어스름깃털 언덕', '레벨': 32, '다음 젠 시간': '??:??'},
    '룬드레드': {'젠주기': 180, '젠위치': '황금 거리', '레벨': 32, '다음 젠 시간': '??:??'},
    '나딘': {'젠주기': 180, '젠위치': '소금바람 항구', '레벨': 32, '다음 젠 시간': '??:??'},
    '투르': {'젠주기': 180, '젠위치': '푸른 용의 숲', '레벨': 32, '다음 젠 시간': '??:??'},
    '나스로': {'젠주기': 180, '젠위치': '모래벌레 사육장', '레벨': 35, '다음 젠 시간': '??:??'},
    '보모': {'젠주기': 180, '젠위치': '간헐천 지대', '레벨': 35, '다음 젠 시간': '??:??'},
    '리안': {'젠주기': 180, '젠위치': '노예 시장', '레벨': 35, '다음 젠 시간': '??:??'},
    '캄투드': {'젠주기': 180, '젠위치': '가려진 숲', '레벨': 35, '다음 젠 시간': '??:??'},
    '로드리고': {'젠주기': 180, '젠위치': '운하거리 부둣가', '레벨': 38, '다음 젠 시간': '??:??'},
    '프랜신': {'젠주기': 180, '젠위치': '경계지 숲', '레벨': 38, '다음 젠 시간': '??:??'},
    '볼테르': {'젠주기': 180, '젠위치': '어둠 장벽', '레벨': 38, '다음 젠 시간': '??:??'},
    '루바란': {'젠주기': 180, '젠위치': '은빛태양 시가지', '레벨': 38, '다음 젠 시간': '??:??'},
    '라크다르': {'젠주기': 180, '젠위치': '모래폭풍 용병기지', '레벨': 41, '다음 젠 시간': '??:??'},
    '이올라': {'젠주기': 180, '젠위치': '동부 삼각주 하류', '레벨': 41, '다음 젠 시간': '??:??'},
    '기드온': {'젠주기': 180, '젠위치': '잿빛안개 폐허', '레벨': 41, '다음 젠 시간': '??:??'},
    '호쏜': {'젠주기': 180, '젠위치': '아민타 검문소', '레벨': 41, '다음 젠 시간': '??:??'},
    '분쇄자': {'젠주기': 180, '젠위치': '붉은 모래언덕', '레벨': 44, '다음 젠 시간': '??:??'},
    '다비드': {'젠주기': 180, '젠위치': '불타는 벌판', '레벨': 44, '다음 젠 시간': '??:??'},
    '암몬': {'젠주기': 180, '젠위치': '고통의 계곡', '레벨': 44, '다음 젠 시간': '??:??'},
    '아르노슈트': {'젠주기': 180, '젠위치': '고대유적지', '레벨': 44, '다음 젠 시간': '??:??'},
    '이드라칸': {'젠주기': 180, '젠위치': '아슬라니스 부족 옛터', '레벨': 47, '다음 젠 시간': '??:??'},
    '보드레': {'젠주기': 180, '젠위치': '보가트 뒷골목', '레벨': 47, '다음 젠 시간': '??:??'},
    '카를로스': {'젠주기': 180, '젠위치': '운하거리 시가지', '레벨': 47, '다음 젠 시간': '??:??'},
    '아무르': {'젠주기': 180, '젠위치': '돌염전 지대', '레벨': 47, '다음 젠 시간': '??:??'},
    '수호자': {'젠주기': 180, '젠위치': '메아리숲', '레벨': 47, '다음 젠 시간': '??:??'},
    '솔그리더': {'젠주기': 180, '젠위치': '몰락농가', '레벨': 47, '다음 젠 시간': '??:??'},
    '제니나': {'젠주기': 180, '젠위치': '파괴된 농장', '레벨': 47, '다음 젠 시간': '??:??'},
    '악몽': {'젠주기': 180, '젠위치': '망령의 장막', '레벨': 47, '다음 젠 시간': '??:??'},
    '부요부요': {'젠주기': 180, '젠위치': '축제 행사장', '레벨': 50, '다음 젠 시간': '??:??'},
    '아무르': {'젠주기': 180, '젠위치': '돌염전 지대', '레벨': 50, '다음 젠 시간': '??:??'},
    '칼비오레': {'젠주기': 180, '젠위치': '브레드 농장', '레벨': 50, '다음 젠 시간': '??:??'},
    '머라이어': {'젠주기': 180, '젠위치': '조개무덤', '레벨': 50, '다음 젠 시간': '??:??'},
    '게란타': {'젠주기': 180, '젠위치': '돌무덤 초소', '레벨': 50, '다음 젠 시간': '??:??'}
}

BOSS_INFO = {
    '거대유충': {'젠주기': 180, '젠위치': '폭풍 황무지', '레벨': 53, '다음 젠 시간': '??:??'},
    '판': {'젠주기': 180, '젠위치': '독초정원', '레벨': 53, '다음 젠 시간': '??:??'},
    '단테': {'젠주기': 180, '젠위치': '검은 울음 협곡', '레벨': 53, '다음 젠 시간': '??:??'},
    '웬디': {'젠주기': 180, '젠위치': '솟아오른 곶', '레벨': 53, '다음 젠 시간': '??:??'},
    '노보모': {'젠주기': 180, '젠위치': '바리족 벌판', '레벨': 53, '다음 젠 시간': '??:??'},
    '피요크': {'젠주기': 180, '젠위치': '독초단지', '레벨': 53, '다음 젠 시간': '??:??'},
    '레쉬': {'젠주기': 180, '젠위치': '벌목지대', '레벨': 53, '다음 젠 시간': '??:??'},
    '이주드': {'젠주기': 180, '젠위치': '고통의 숲', '레벨': 56, '다음 젠 시간': '??:??'},
    '에일레스': {'젠주기': 180, '젠위치': '트렌체 바위숲', '레벨': 56, '다음 젠 시간': '??:??'},
    '포보모': {'젠주기': 180, '젠위치': '바리족 둥지', '레벨': 56, '다음 젠 시간': '??:??'},
    '루드라': {'젠주기': 180, '젠위치': '돌담 경작지', '레벨': 56, '다음 젠 시간': '??:??'},
    '라이진': {'젠주기': 180, '젠위치': '금빛바람평야', '레벨': 56, '다음 젠 시간': '??:??'},
    '엘라': {'젠주기': 300, '젠위치': '저주받은 들판', '레벨': 59, '다음 젠 시간': '??:??'},
    '율리우스': {'젠주기': 300, '젠위치': '돌무지숲', '레벨': 59, '다음 젠 시간': '??:??'},
    '길예르모': {'젠주기': 300, '젠위치': '광석 채굴장', '레벨': 59, '다음 젠 시간': '??:??'},
    '현자': {'젠주기': 300, '젠위치': '미치광이숲', '레벨': 59, '다음 젠 시간': '??:??'},
    '보르테가': {'젠주기': 300, '젠위치': '쓰레기 해안', '레벨': 59, '다음 젠 시간': '??:??'},
    '오색수호자': {'젠주기': 300, '젠위치': '오색 평원', '레벨': 59, '다음 젠 시간': '??:??'},
    '티아고': {'젠주기': 300, '젠위치': '학살 정원', '레벨': 59, '다음 젠 시간': '??:??'},
    '뒤트는자': {'젠주기': 300, '젠위치': '바투 숲', '레벨': 59, '다음 젠 시간': '??:??'},
    '바르테온': {'젠주기': 300, '젠위치': '투쟁의 연병장', '레벨': 62, '다음 젠 시간': '??:??'},
    '엘레칸': {'젠주기': 300, '젠위치': '갯벌 언덕', '레벨': 62, '다음 젠 시간': '??:??'},
    '숲의악몽': {'젠주기': 300, '젠위치': '저주받은 숲', '레벨': 62, '다음 젠 시간': '??:??'},
    '배회자': {'젠주기': 300, '젠위치': '생명의 탑', '레벨': 62, '다음 젠 시간': '??:??'},
    '도굴꾼': {'젠주기': 300, '젠위치': '어둠노을 장막', '레벨': 62, '다음 젠 시간': '??:??'},
    '건드루드': {'젠주기': 300, '젠위치': '포효하는 숲', '레벨': 62, '다음 젠 시간': '??:??'},
    '무라드': {'젠주기': 300, '젠위치': '옛 왕국의 폐허', '레벨': 65, '다음 젠 시간': '??:??'},
    '뜯먹자': {'젠주기': 300, '젠위치': '동부 삼각주 상류', '레벨': 65, '다음 젠 시간': '??:??'},
    '이드발': {'젠주기': 300, '젠위치': '체스성', '레벨': 65, '다음 젠 시간': '??:??'},
    '뼈돌문지기': {'젠주기': 300, '젠위치': '뼈와 돌의 평원', '레벨': 65, '다음 젠 시간': '??:??'}
}

ABOSS_INFO = {
    '선지자': {'젠주기': 360, '젠위치': '선지자의 성소', '레벨': 50, '다음 젠 시간': '??:??'},
    '야수': {'젠주기': 360, '젠위치': '용암호수', '레벨': 50, '다음 젠 시간': '??:??'},
    '체스킹퀸': {'젠주기': 360, '젠위치': '왕과 여왕의 성', '레벨': 50, '다음 젠 시간': '??:??'},
    '이즈굴드': {'젠주기': 360, '젠위치': '용의 둥지', '레벨': 50, '다음 젠 시간': '??:??'},
    '토룡': {'젠주기': 360, '젠위치': '토룡의 둥지', '레벨': 56, '다음 젠 시간': '??:??'},
    '어미': {'젠주기': 360, '젠위치': '어미 서식지', '레벨': 56, '다음 젠 시간': '??:??'},
    '궤': {'젠주기': 360, '젠위치': '버려진 광장', '레벨': 56, '다음 젠 시간': '??:??'},
    '어머니': {'젠주기': 360, '젠위치': '지룡의 쉼터', '레벨': 56, '다음 젠 시간': '??:??'},
    '인면벌레': {'젠주기': 720, '젠위치': '몰락자의 거처', '레벨': 62, '다음 젠 시간': '??:??'},
    '해적왕': {'젠주기': 720, '젠위치': '해적왕의 거처', '레벨': 62, '다음 젠 시간': '??:??'},
    '덩굴거인': {'젠주기': 720, '젠위치': '괴수 경기장', '레벨': 62, '다음 젠 시간': '??:??'},
    '나뭇돌골렘': {'젠주기': 720, '젠위치': '바위터', '레벨': 62, '다음 젠 시간': '??:??'},
    '주시대': {'젠주기': 720, '젠위치': '금빛 염전', '레벨': 65, '다음 젠 시간': '??:??'},
    '절멸자': {'젠주기': 720, '젠위치': '적모래 분지', '레벨': 65, '다음 젠 시간': '??:??'},
    '테스투도': {'젠주기': 720, '젠위치': '바다의 해안가', '레벨': 65, '다음 젠 시간': '??:??'},
    '칼부숨이': {'젠주기': 720, '젠위치': '칼부숨이 수용소', '레벨': 65, '다음 젠 시간': '??:??'}
}

CROSSBOSS_INFO = {
    '무크로': {'젠주기': 540, '젠위치': '4번 망령의 황무지', '레벨': 65, '다음 젠 시간': '??:??'},
    '루벤스': {'젠주기': 540, '젠위치': '1번 스러진 날개숲', '레벨': 65, '다음 젠 시간': '??:??'},
    '이시도르': {'젠주기': 660, '젠위치': '2번 축축한 숲', '레벨': 68, '다음 젠 시간': '??:??'},
    '야수조달자': {'젠주기': 660, '젠위치': '3번 흐느끼는 황야', '레벨': 68, '다음 젠 시간': '??:??'},
    '으뜸자1번': {'젠주기': 360, '젠위치': '1번', '레벨': 68, '다음 젠 시간': '??:??'},
    '으뜸자2번': {'젠주기': 360, '젠위치': '2번', '레벨': 68, '다음 젠 시간': '??:??'},
    '으뜸자3번': {'젠주기': 360, '젠위치': '3번', '레벨': 68, '다음 젠 시간': '??:??'},
    '으뜸자4번': {'젠주기': 360, '젠위치': '4번', '레벨': 68, '다음 젠 시간': '??:??'},
    '으뜸자5번': {'젠주기': 360, '젠위치': '5번', '레벨': 68, '다음 젠 시간': '??:??'}
}


async def bosstime_alert(boss_info):
    for boss_name, boss_data in boss_info.items():
        next_time = boss_data['다음 젠 시간']
        if next_time == '??:??':
            continue

        next_time = datetime.strptime(next_time, '%H:%M').time()
        now = datetime.now(korea_timezone).time()

        #if next_time < now:
        #    next_time += timedelta(days=1)

        time_left = int ((datetime.combine(date.today(), next_time) - datetime.combine(date.today(), now)).total_seconds() // 60)
        if time_left == 4:
            channel = client.get_channel(1114409826714406963)  # 메시지를 보낼 채널의 ID를 입력하세요.
            await channel.send(f'영지보스 {boss_name}의 다음 젠이 {time_left + 1}분 남았습니다.')  # 원하는 메시지를 입력하세요.



@client.event
async def on_ready():
    #데이터 베이스 연결
    db_host = os.environ.get('DB_HOST')
    db_user = os.environ.get('DB_USER_NAME')
    db_password = os.environ.get('DB_PASSWORD')
    db_name = os.environ.get('DB_NAME')
    
    boss_db = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = boss_db.cursor()

    #DB 에 테이블이 없을 경우, 테이블 생성
    cursor.execute('''CREATE TABLE IF NOT EXISTS BOSS_INFO (
                        name VARCHAR(255) PRIMARY KEY,
                        location VARCHAR(255),
                        level INT,
                        next_spawn VARCHAR(255)
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS LOWBOSS_INFO (
                        name VARCHAR(255) PRIMARY KEY,
                        location VARCHAR(255),
                        level INT,
                        next_spawn VARCHAR(255)
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS ABOSS_INFO (
                        name VARCHAR(255) PRIMARY KEY,
                        location VARCHAR(255),
                        level INT,
                        next_spawn VARCHAR(255)
                    )''')

    await update_boss_data()
    await update_aboss_data()
    await update_lowboss_data()
    await client.change_presence(status=discord.Status.online, activity=discord.Game("보스 타임 체크"))
    print('봇이 온라인으로 전환되었습니다.')
    while not client.is_closed():
        asyncio.create_task((bosstime_alert(ABOSS_INFO)))
        await asyncio.sleep(60)


async def update_boss_data():
    # DB에 저장되어 있던 데이터를 딕셔너리로 이동
    boss_db = mysql.connector.connect(
        host='us-cdbr-east-06.cleardb.net',
        user='bf61fea885d392',
        password='ff8f9bad',
        database='heroku_b11c445fa59b270',
    )
    cursor = boss_db.cursor()

    #BOSS_INFO 테이블 조회 쿼리 실행
    query = "SELECT * FROM BOSS_INFO"
    cursor.execute(query)

    #조회된 데이터를 파이썬의 BOSS_INFO 에 딕셔너리에 저장
    global BOSS_INFO
    for row in cursor:
        boss_name = row[0]
        boss_info = {
            '젠주기': BOSS_INFO.get(boss_name, {}).get('젠주기'),  # 기존 젠주기 값 유지
            '젠위치': row[1],
            '레벨': row[2],
            '다음 젠 시간': row[3]
        }
        BOSS_INFO[boss_name] = boss_info

    cursor.close()
    boss_db.close()

async def update_aboss_data():
    # DB에 저장되어 있던 데이터를 딕셔너리로 이동
    boss_db = mysql.connector.connect(
        host='us-cdbr-east-06.cleardb.net',
        user='bf61fea885d392',
        password='ff8f9bad',
        database='heroku_b11c445fa59b270',
    )
    cursor = boss_db.cursor()

    # ABOSS_INFO 테이블 조회 쿼리 실행
    query = "SELECT * FROM ABOSS_INFO"
    cursor.execute(query)

    # 조회된 데이터를 파이썬의 ABOSS_INFO 에 딕셔너리에 저장
    global ABOSS_INFO
    for row in cursor:
        boss_name = row[0]
        boss_info = {
            '젠주기': ABOSS_INFO.get(boss_name, {}).get('젠주기'),  # 기존 젠주기 값 유지
            '젠위치': row[1],
            '레벨': row[2],
            '다음 젠 시간': row[3]
        }
        ABOSS_INFO[boss_name] = boss_info

    cursor.close()
    boss_db.close()


async def update_lowboss_data():
    # DB에 저장되어 있던 데이터를 딕셔너리로 이동
    boss_db = mysql.connector.connect(
        host='us-cdbr-east-06.cleardb.net',
        user='bf61fea885d392',
        password='ff8f9bad',
        database='heroku_b11c445fa59b270',
    )
    cursor = boss_db.cursor()

    # LOWBOSS_INFO 테이블 조회 쿼리 실행
    query = "SELECT * FROM LOWBOSS_INFO"
    cursor.execute(query)

    # 조회된 데이터를 파이썬의 BOSS_INFO 에 딕셔너리에 저장
    global LOWBOSS_INFO
    for row in cursor:
        boss_name = row[0]
        boss_info = {
            '젠주기': LOWBOSS_INFO.get(boss_name, {}).get('젠주기'),  # 기존 젠주기 값 유지
            '젠위치': row[1],
            '레벨': row[2],
            '다음 젠 시간': row[3]
        }
        LOWBOSS_INFO[boss_name] = boss_info

    cursor.close()
    boss_db.close()


async def update_crossboss_data():
    # DB에 저장되어 있던 데이터를 딕셔너리로 이동
    boss_db = mysql.connector.connect(
        host='us-cdbr-east-06.cleardb.net',
        user='bf61fea885d392',
        password='ff8f9bad',
        database='heroku_b11c445fa59b270',
    )
    cursor = boss_db.cursor()

    # LOWBOSS_INFO 테이블 조회 쿼리 실행
    query = "SELECT * FROM CROSSBOSS_INFO"
    cursor.execute(query)

    # 조회된 데이터를 파이썬의 CROSSBOSS_INFO 에 딕셔너리에 저장
    global CROSSBOSS_INFO
    for row in cursor:
        boss_name = row[0]
        boss_info = {
            '젠주기': CROSSBOSS_INFO.get(boss_name, {}).get('젠주기'),  # 기존 젠주기 값 유지
            '젠위치': row[1],
            '레벨': row[2],
            '다음 젠 시간': row[3]
        }
        LOWBOSS_INFO[boss_name] = boss_info

    cursor.close()
    boss_db.close()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

# 이 뒤에서 메시지로 쓸 리스트를 미리 배열로 정의
    boss_reply = []
    aboss_reply = []
    lowboss_reply = []
    crossboss_reply = []
    boss_db = mysql.connector.connect(
        host='us-cdbr-east-06.cleardb.net',
        user='bf61fea885d392',
        password='ff8f9bad',
        database='heroku_b11c445fa59b270',
    )

# 실제 명령어 부분
        
    if message.content.startswith('!컷'):
        target = message.content.split()[1]  # 입력된 메시지에서 2번째 단어 추출
        now = datetime.utcnow() + timedelta(hours=9)  # KST (UTC+9)
        args = message.content.split()  # 보스 이름과 시간 정보 추출
        boss_name = args[1]

        if boss_name in BOSS_INFO:
            for name, info in BOSS_INFO.items():
                if name == target:
                    next_spawn = now + timedelta(minutes=info["젠주기"])
                    BOSS_INFO[name]["다음 젠 시간"] = next_spawn.strftime('%H:%M')
                    boss_reply.append(f"{next_spawn.hour}:{next_spawn.minute}, {name}, , {info['젠위치']}, {info['레벨']}")
                else:
                    boss_reply.append(f"{info['다음 젠 시간']} , {name},  {info['젠위치']}, {info['레벨']}")
            boss_reply = sorted(boss_reply, key=lambda x: x.split(',')[0])
            await message.reply('\n'.join(boss_reply))
            #메시지 보낸걸, DB에 저장하자
            cursor = boss_db.cursor()
            for name, info in BOSS_INFO.items():
                next_spawn = info['다음 젠 시간']
                location = info['젠위치']
                level = info['레벨']

                query = "UPDATE BOSS_INFO SET next_spawn = %s, location = %s, level = %s WHERE name = %s"
                values = (next_spawn, location, level, name)
                cursor.execute(query, values)

            boss_db.commit()

            cursor.close()
            boss_db.close()
        else:
            await message.reply('존재하지 않는 보스 이름입니다.')
            return

    elif message.content.startswith('!젠타임'):

        args = message.content.split()  # 보스 이름과 시간 정보 추출
        if len(args) != 3:
            await message.reply('잘못된 명령어입니다. 사용법: !젠타임 보스이름 시간(HH:MM)')
            return
        boss_name = args[1]
        time_str = args[2]

        # BOSS_INFO 갱신
        if boss_name not in BOSS_INFO:
            await message.reply('존재하지 않는 보스 이름입니다.')
            return
        try:
            time_obj = datetime.strptime(time_str, '%H:%M')
        except ValueError:
            await message.reply('잘못된 시간 형식입니다. 사용법: HH:MM')
            return
        BOSS_INFO[boss_name]['다음 젠 시간'] = time_str
        # 갱신된 BOSS_INFO 출력
        for name, info in BOSS_INFO.items():
            boss_reply.append(f"{info['다음 젠 시간']}, {name}, {info['젠위치']}, {info['레벨']}")
        boss_reply = sorted(boss_reply, key=lambda x: x.split(',')[0])
        await message.reply('\n'.join(boss_reply))
        # 메시지 보낸걸, DB에 저장하자
        cursor = boss_db.cursor()
        for name, info in BOSS_INFO.items():
            next_spawn = info['다음 젠 시간']
            location = info['젠위치']
            level = info['레벨']

            query = "UPDATE BOSS_INFO SET next_spawn = %s, location = %s, level = %s WHERE name = %s"
            values = (next_spawn, location, level, name)
            cursor.execute(query, values)

        boss_db.commit()

        cursor.close()
        boss_db.close()

    elif message.content.startswith('!초기화'):

        args = message.content.split()  # 보스 이름과 시간 정보 추출
        if len(args) != 2:
            await message.reply('잘못된 명령어입니다. 사용법: !초기화 보스이름')
            return
        boss_name = args[1]

        if boss_name not in BOSS_INFO:
            await message.reply('존재하지 않는 보스 이름입니다.')
            return
        BOSS_INFO[boss_name]['다음 젠 시간'] = '??:??'

        # 갱신된 BOSS_INFO 출력
        for name, info in BOSS_INFO.items():
            boss_reply.append(f"{info['다음 젠 시간']}, {name}, {info['젠위치']}, {info['레벨']}")
        boss_reply = sorted(boss_reply, key=lambda x: x.split(',')[0])
        await message.reply('\n'.join(boss_reply))
        # 메시지 보낸걸, DB에 저장하자
        cursor = boss_db.cursor()
        for name, info in BOSS_INFO.items():
            next_spawn = info['다음 젠 시간']
            location = info['젠위치']
            level = info['레벨']

            query = "UPDATE BOSS_INFO SET next_spawn = %s, location = %s, level = %s WHERE name = %s"
            values = (next_spawn, location, level, name)
            cursor.execute(query, values)

        boss_db.commit()

        cursor.close()
        boss_db.close()

    elif message.content == '!전체초기화':
        for name, info in BOSS_INFO.items():
            BOSS_INFO[name]['다음 젠 시간'] = '??:??'
            boss_reply.append(f"{info['다음 젠 시간']}, {name}, {info['젠위치']}, {info['레벨']}")
        boss_reply = sorted(boss_reply, key=lambda x: x.split(',')[0])
        await message.reply('\n'.join(boss_reply))
        # 메시지 보낸걸, DB에 저장하자
        cursor = boss_db.cursor()
        for name, info in BOSS_INFO.items():
            next_spawn = info['다음 젠 시간']
            location = info['젠위치']
            level = info['레벨']

            query = "UPDATE BOSS_INFO SET next_spawn = %s, location = %s, level = %s WHERE name = %s"
            values = (next_spawn, location, level, name)
            cursor.execute(query, values)

        boss_db.commit()

        cursor.close()
        boss_db.close()

    # 여기부턴 영지 보스

    if message.content.startswith('!영지컷'):
        target = message.content.split()[1]  # 입력된 메시지에서 2번째 단어 추출
        now = datetime.utcnow() + timedelta(hours=9)  # KST (UTC+9)
        args = message.content.split()
        boss_name = args[1]

        if boss_name in ABOSS_INFO:
            for name, info in ABOSS_INFO.items():
                if name == target:
                    next_spawn = now + timedelta(minutes=info["젠주기"])
                    ABOSS_INFO[name]["다음 젠 시간"] = next_spawn.strftime('%H:%M')
                    aboss_reply.append(f"{next_spawn.hour}:{next_spawn.minute}, {name}, {info['젠위치']}, {info['레벨']}")
                else:
                    aboss_reply.append(f"{info['다음 젠 시간']} , {name},  {info['젠위치']}, {info['레벨']}")
            aboss_reply = sorted(aboss_reply, key=lambda x: x.split(',')[0])
            await message.reply('\n'.join(aboss_reply))
            # 메시지 보낸걸, DB에 저장하자
            cursor = boss_db.cursor()
            for name, info in ABOSS_INFO.items():
                next_spawn = info['다음 젠 시간']
                location = info['젠위치']
                level = info['레벨']

                query = "UPDATE ABOSS_INFO SET next_spawn = %s, location = %s, level = %s WHERE name = %s"
                values = (next_spawn, location, level, name)
                cursor.execute(query, values)

            boss_db.commit()

            cursor.close()
            boss_db.close()
        else:
            await message.reply('존재하지 않는 보스 이름입니다.')
            return

    elif message.content.startswith('!영지젠타임'):

        args = message.content.split()  # 보스 이름과 시간 정보 추출
        if len(args) != 3:
            await message.reply('잘못된 명령어입니다. 사용법: !젠타임 보스이름 시간(HH:MM)')
            return
        boss_name = args[1]
        time_str = args[2]

        # BOSS_INFO 갱신
        if boss_name not in ABOSS_INFO:
            await message.reply('존재하지 않는 보스 이름입니다.')
            return
        try:
            time_obj = datetime.strptime(time_str, '%H:%M')
        except ValueError:
            await message.reply('잘못된 시간 형식입니다. 사용법: HH:MM')
            return
        ABOSS_INFO[boss_name]['다음 젠 시간'] = time_str
        # 갱신된 BOSS_INFO 출력
        for name, info in ABOSS_INFO.items():
            aboss_reply.append(f"{info['다음 젠 시간']}, {name}, {info['젠위치']}, {info['레벨']}")
        aboss_reply = sorted(aboss_reply, key=lambda x: x.split(',')[0])
        await message.reply('\n'.join(aboss_reply))
        # 메시지 보낸걸, DB에 저장하자
        cursor = boss_db.cursor()
        for name, info in ABOSS_INFO.items():
            next_spawn = info['다음 젠 시간']
            location = info['젠위치']
            level = info['레벨']

            query = "UPDATE ABOSS_INFO SET next_spawn = %s, location = %s, level = %s WHERE name = %s"
            values = (next_spawn, location, level, name)
            cursor.execute(query, values)

        boss_db.commit()

        cursor.close()
        boss_db.close()

    elif message.content.startswith('!영지초기화'):

        args = message.content.split()  # 보스 이름과 시간 정보 추출
        if len(args) != 2:
            await message.reply('잘못된 명령어입니다. 사용법: !초기화 보스이름')
            return
        boss_name = args[1]

        if boss_name not in ABOSS_INFO:
            await message.reply('존재하지 않는 보스 이름입니다.')
            return
        ABOSS_INFO[boss_name]['다음 젠 시간'] = '??:??'

        # 갱신된 BOSS_INFO 출력
        for name, info in ABOSS_INFO.items():
            aboss_reply.append(f"{info['다음 젠 시간']}, {name}, {info['젠위치']}, {info['레벨']}")
        aboss_reply = sorted(aboss_reply, key=lambda x: x.split(',')[0])
        await message.reply('\n'.join(aboss_reply))
        # 메시지 보낸걸, DB에 저장하자
        cursor = boss_db.cursor()
        for name, info in ABOSS_INFO.items():
            next_spawn = info['다음 젠 시간']
            location = info['젠위치']
            level = info['레벨']

            query = "UPDATE ABOSS_INFO SET next_spawn = %s, location = %s, level = %s WHERE name = %s"
            values = (next_spawn, location, level, name)
            cursor.execute(query, values)

        boss_db.commit()

        cursor.close()
        boss_db.close()

    elif message.content == '!영지전체초기화':
        for name, info in ABOSS_INFO.items():
            ABOSS_INFO[name]['다음 젠 시간'] = '??:??'
            aboss_reply.append(f"{info['다음 젠 시간']}, {name}, {info['젠위치']}, {info['레벨']}")
        await message.reply('\n'.join(aboss_reply))
        # 메시지 보낸걸, DB에 저장하자
        cursor = boss_db.cursor()
        for name, info in ABOSS_INFO.items():
            next_spawn = info['다음 젠 시간']
            location = info['젠위치']
            level = info['레벨']

            query = "UPDATE ABOSS_INFO SET next_spawn = %s, location = %s, level = %s WHERE name = %s"
            values = (next_spawn, location, level, name)
            cursor.execute(query, values)

        boss_db.commit()

        cursor.close()
        boss_db.close()


    # 여기부턴 크렐보스

    if message.content.startswith('!크렐컷'):
        target = message.content.split()[1]  # 입력된 메시지에서 2번째 단어 추출
        now = datetime.utcnow() + timedelta(hours=9)  # KST (UTC+9)
        args = message.content.split()
        boss_name = args[1]

        if boss_name in CROSSBOSS_INFO:
            for name, info in CROSSBOSS_INFO.items():
                if name == target:
                    next_spawn = now + timedelta(minutes=info["젠주기"])
                    CROSSBOSS_INFO[name]["다음 젠 시간"] = next_spawn.strftime('%H:%M')
                    crossboss_reply.append(f"{next_spawn.hour}:{next_spawn.minute}, {name}, , {info['젠위치']}, {info['레벨']}")
                else:
                    crossboss_reply.append(f"{info['다음 젠 시간']} , {name},  {info['젠위치']}, {info['레벨']}")
            crossboss_reply = sorted(crossboss_reply, key=lambda x: x.split(',')[0])
            await message.reply('\n'.join(crossboss_reply))
            # 메시지 보낸걸, DB에 저장하자
            cursor = boss_db.cursor()
            for name, info in CROSSBOSS_INFO.items():
                next_spawn = info['다음 젠 시간']
                location = info['젠위치']
                level = info['레벨']

                query = "UPDATE CROSSBOSS_INFO SET next_spawn = %s, location = %s, level = %s WHERE name = %s"
                values = (next_spawn, location, level, name)
                cursor.execute(query, values)

            boss_db.commit()

            cursor.close()
            boss_db.close()
        else:
            await message.reply('존재하지 않는 b보스 이름입니다.')
            return

    elif message.content.startswith('!크렐젠타임'):

        args = message.content.split()  # 보스 이름과 시간 정보 추출
        if len(args) != 3:
            await message.reply('잘못된 명령어입니다. 사용법: !크렐젠타임 보스이름 시간(HH:MM)')
            return
        boss_name = args[1]
        time_str = args[2]

        # BOSS_INFO 갱신
        if boss_name not in CROSSBOSS_INFO:
            await message.reply('존재하지 않는 보스 이름입니다.')
            return
        try:
            time_obj = datetime.strptime(time_str, '%H:%M')
        except ValueError:
            await message.reply('잘못된 시간 형식입니다. 사용법: HH:MM')
            return
        CROSSBOSS_INFO[boss_name]['다음 젠 시간'] = time_str

        # 갱신된 BOSS_INFO 출력
        for name, info in CROSSBOSS_INFO.items():
            crossboss_reply.append(f"{info['다음 젠 시간']}, {name}, {info['젠위치']}, {info['레벨']}")
        crossboss_reply = sorted(crossboss_reply, key=lambda x: x.split(',')[0])
        await message.reply('\n'.join(crossboss_reply))
        # 메시지 보낸걸, DB에 저장하자
        cursor = boss_db.cursor()
        for name, info in CROSSBOSS_INFO.items():
            next_spawn = info['다음 젠 시간']
            location = info['젠위치']
            level = info['레벨']

            query = "UPDATE CROSSBOSS_INFO SET next_spawn = %s, location = %s, level = %s WHERE name = %s"
            values = (next_spawn, location, level, name)
            cursor.execute(query, values)

        boss_db.commit()

        cursor.close()
        boss_db.close()

    elif message.content.startswith('!크렐초기화'):

        args = message.content.split()  # 보스 이름과 시간 정보 추출
        if len(args) != 2:
            await message.reply('잘못된 명령어입니다. 사용법: !초기화 보스이름')
            return
        boss_name = args[1]

        if boss_name not in CROSSBOSS_INFO:
            await message.reply('존재하지 않는 보스 이름입니다.')
            return
        CROSSBOSS_INFO[boss_name]['다음 젠 시간'] = '??:??'

        # 갱신된 BOSS_INFO 출력
        for name, info in CROSSBOSS_INFO.items():
            crossboss_reply.append(f"{info['다음 젠 시간']}, {name}, {info['젠위치']}, {info['레벨']}")
        crossboss_reply = sorted(crossboss_reply, key=lambda x: x.split(',')[0])
        await message.reply('\n'.join(crossboss_reply))
        # 메시지 보낸걸, DB에 저장하자
        cursor = boss_db.cursor()
        for name, info in CROSSBOSS_INFO.items():
            next_spawn = info['다음 젠 시간']
            location = info['젠위치']
            level = info['레벨']

            query = "UPDATE CROSSBOSS_INFO SET next_spawn = %s, location = %s, level = %s WHERE name = %s"
            values = (next_spawn, location, level, name)
            cursor.execute(query, values)

        boss_db.commit()

        cursor.close()
        boss_db.close()

    elif message.content == '!크렐전체초기화':
        for name, info in CROSSBOSS_INFO.items():
            CROSSBOSS_INFO[name]['다음 젠 시간'] = '??:??'
            crossboss_reply.append(f"{info['다음 젠 시간']}, {name}, {info['젠위치']}, {info['레벨']}")
        await message.reply('\n'.join(crossboss_reply))
        # 메시지 보낸걸, DB에 저장하자
        cursor = boss_db.cursor()
        for name, info in CROSSBOSS_INFO.items():
            next_spawn = info['다음 젠 시간']
            location = info['젠위치']
            level = info['레벨']

            query = "UPDATE CROSSBOSS_INFO SET next_spawn = %s, location = %s, level = %s WHERE name = %s"
            values = (next_spawn, location, level, name)
            cursor.execute(query, values)

        boss_db.commit()

        cursor.close()
        boss_db.close()


try:
    client.run(TOKEN)
except discord.errors.LoginFailure as e:
    print("Improper token has been passed.")
