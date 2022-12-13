import os.path
from base64 import urlsafe_b64decode
from bs4 import BeautifulSoup


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


'''
Gmail API 사용하기
1. https://console.cloud.google.com/flows/enableapi?apiid=gmail.googleapis.com
   링크에서 Gmail API 사용 등록하기
2. https://console.cloud.google.com/apis/credentials
   링크에서 GCP 사용자 인증 정보에 접속하기
3. 사용자 인증 정보 만들기 - OAuth 클라이언트 ID 클릭
4. 애플리케이션 유형: 데스크톱 앱 선택 - 클라이언트 이름 짓기 - 만들기 클릭
5. OAuth 클라이언트 생성됨 팝업창에서 JSON 다운로드
'''

USER_ID = 'example@gmail.com'
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
SECRETS_JSON = 'client_secret_00000000000-ihaveapenihaveanapple0applepen00.apps.googleusercontent.com.json'

'''
변수 소개
USER_ID: Gmail API를 사용할 Gmail 계정: example@gmail.com
SCOPES: OAuth 클라이언트의 권한 범위, 사용 가능한 범위 리스트 -> https://developers.google.com/gmail/api/auth/scopes
SECRETS_JSON: GCP OAuth 클라이언트 계정에서 다운로드 받은 클라이언트 ID, Sectet Key 등이 담긴 .json 파일 경로
              ex) 'client_secret_00000000000-ihaveapenihaveanapple0applepen00.apps.googleusercontent.com.json'
'''
def main():
    # 저장된 엑세스 토큰 불러오기
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # 저장된 토큰이 없거나 엑세스 토큰 기간이 만료된 경우
    if not creds or not creds.valid:
        # 리프레시 토큰이 있는 경우 리프레시 토큰으로 엑세스 토큰 재발급
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        # 리프레시 토큰이 없거나 만료된 경우 클라이언트 ID와 Secret Key로 엑세스 토큰 재발급
        else:
            flow = InstalledAppFlow.from_client_secrets_file(SECRETS_JSON, SCOPES)
            creds = flow.run_local_server(port=0)

        # 발급한 엑세스 토큰 .json으로 저장
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        '''
        users().messages().list()의 파라메터 q
         : Gmail search box의 쿼리문, 링크에서 확인 -> https://support.google.com/mail/answer/7190?hl=en
        '''
        # 쿼리 조건에 맞는 메세지의 고유 id 값 리스트 얻기
        id_results: dict = service.users().messages().list(userId=USER_ID, q='newer_than:7d').execute()
        messages: list[dict[str, str]] = id_results.get('messages', [])

        if not messages:
            print('No labels found.')
            return

        id_list: list[str] = [message['id'] for message in messages]

        # 아이디 리스트에서 부터 메세지 추출하기
        message_results: list[dict] = [service.users().messages().get(userId=USER_ID, id=id, format='full').execute() for id in id_list]

        # Base64로 인코딩된 메세지 내용 디코딩하기
        # Content-type: "text/html; charset=utf-8"
        data_html_str: list[str] = [urlsafe_b64decode(m['payload']['body']['data']).decode('utf-8') for m in message_results]
        
        for data in data_html_str:
            print(BeautifulSoup(data))

    except HttpError as error:
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()
