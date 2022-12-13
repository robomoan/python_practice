import os.path
import sys
import pandas as pd

'''
밀크런 발주 리스트 발주번호 컬럼에 복수로 적혀있는 발주번호들을 행 분리하는 모듈
xlsx 또는 csv 파일을 입력으로 넣어야 함.
xlsx 파일의 경우 맨 앞 시트에 raw table이 있어야 함.
output: {raw file name}_expand.csv

pyinstaller로 실행파일 생성
pyinstaller -w -F milkrun_transformer.py
'''

# 파일 드래그 앤 드롭으로 받기
file_path = sys.argv[1]
file_path.replace('\\', '/')
file_name: str = file_path.split('/')[-1].split('.')[0]
file_dir: str = '/'.join(file_path.split('/')[:-1])

if file_path.split('/')[-1].split('.')[1] == 'xlsx':
    raw_df = pd.read_excel(
        file_path, sheet_name=0,
        dtype= {'발주번호': 'string'},
        engine='openpyxl'
)
elif file_path.split('/')[-1].split('.')[1] == 'csv':
    raw_df = pd.read_csv(
        file_path,
        dtype= {'발주번호': 'string'},
)
else:
    raise Exception('파일 확장자가 맞지 않습니다. xlsx 또는 csv 파일을 입력해주세요.')

output_df = pd.concat([raw_df.drop('발주번호', axis=1), raw_df['발주번호'].str.split(pat=' / ', expand=True)], axis=1)
output_df.rename(
    columns={
        0: '발주번호1',
        1: '발주번호2',
        2: '발주번호3',
        3: '발주번호4',
        4: '발주번호5',
        5: '발주번호6',
    },
    inplace=True
)

output_df = pd.wide_to_long(output_df, stubnames='발주번호', i=raw_df.drop('발주번호', axis=1).columns.to_list(), j = '발주번호구분')
output_df.dropna(axis=0, inplace=True)

output_file_name: str = file_name + '_expand.csv'
output_file_path: str = os.path.join(file_dir, output_file_name)
output_df.to_csv(output_file_path, encoding='utf-8-sig', index=True)
sys.exit()
