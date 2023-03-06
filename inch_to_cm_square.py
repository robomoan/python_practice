import sys

'''
모니터, 스마트폰 액정 넓이 단위 변환
입력: 대각선 길이 (inch), 화면 비율(가로 : 세로)
출력: 화면 넓이 (cm^2)

활용: 터미널에서
    inch_to_cm_square.py (대각선 길이 inch) (가로비) (세로비)
'''

def inch_to_cm_square(diag_inch , ratio=(1, 1)) -> float:
    try:
        diag_inch_float = float(diag_inch)
        ratio_width = float(ratio[0])
        ratio_height = float(ratio[1])
    except(ValueError):
        raise ValueError("int 자료형 또는 float 자료형을 입력하세요.")

    ratio_diagonal = (ratio_width ** 2 + ratio_height ** 2) ** (1/2)
    width_inch: float = diag_inch_float / ratio_diagonal * ratio_width
    height_inch: float = diag_inch_float / ratio_diagonal * ratio_height

    return width_inch * height_inch * (2.54 ** 2)


if __name__ == "__main__":
    try:
        result: float = inch_to_cm_square(diag_inch=sys.argv[1], ratio=(sys.argv[2], sys.argv[3]))
    except(IndexError):
        result: float = inch_to_cm_square(diag_inch=sys.argv[1])

    print(result)