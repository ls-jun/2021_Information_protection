# 프로젝트2: AI 악성코드 탐지

<br/>

## 조원 소개

```
20171664 소프트웨어학부 이범석
github: https://github.com/LeeBumSeok
```

```
20171667 소프트웨어학부 이승준
github: https://github.com/ls-jun
```

```
20182210 정보보안암호수학과 김승현
github: https://github.com/seunghy6n
```

```
20182229 정보보안암호수학과 신기현
github: https://github.com/shinkihyeon
```

---

<br/>

## 프로젝트 소개

<br/>

**pe 파일이 주어졌을 때, 주어진 파일이 악성파일인지 정상파일인지 판별하는 '이진분류기 모델'을 만든다.**

- **pe파일**
  - Portable Excutable 파일
  - 윈도우 상에서 실행 가능한 프로그램
  - ex) exe dll sys 등등

`EMBER`, `PEMINER`, `PESTUDIO` 각각 20000개의 학습 데이터, 10000개의 검증 데이터, 10000개의 테스트 데이터로 구성되어 있다.

<br/>

### 실행 방법

- `ai_malware_detect.ipynb` 파일을 순서대로 실행한다.

  - `file_path` 변수를 로컬 경로에 맞게 수정한다.
  - `ModuleNotFoundError` 경고가 나오면 다음 명령어를 이용해 패키지를 설치한다.

    ```
    pip install <Package name>
    ```

### 실행 환경

```
python 3.7.6 (default, Jan  8 2020, 20:23:39) [MSC v.1916 64 bit (AMD64)]
python 3.8.9 (default, Aug  3 2021, 19:21:54) [Clang 13.0.0 (clang-1300.0.29.3)]
```

위 두 환경에서는 정상적으로 작동하는 것으로 확인하였다.

---

<br/>

## 진행 순서

<br/>

1. 주요 라이브러리 import

   - 추가한 라이브러리들

   - `tqdm`
     
     - 반복문 진행정도를 보여주는 라이브러리
   - `FeatureHasher`

     - 숫자로 이루어져 있지 않은 데이터 가공을 위한 라이브러리

   - 추가한 라이브러리에 대한 코드는 다음과 같다.

     ```python
     #tqdm
     from tqdm import tqdm
      
     #FeatureHasher
     from sklearn.feature_extraction import FeatureHasher
     ```

2. `EMBER`, `PESTUDIO` 파일에서 적절한 특징 추출 함수 작성

   - 파일의 특징을 최대한 추출한 후, 이 특징들을 머신러닝으로 학습시켜 주어진 파일이 악성이 되는 조건 검출
   - `PEMIER`, `EMBER`, `PESTUDIO`에서 다양한 feature(특징)들을 추출하여 정확도 높이기
   - EMBER에서 추출한 특징들

     ```python
     self.get_header_info()
       # header의 size가 지나치게 많거나 version이 잘 못 되는 등의 상황은 의심스러움

     self.get_exports_info()
       # 악성코드의 경우 export를 많이 할것으로 예상됨
       # _feature 해시로 추출_

     self.get_imports_info()
       # import하는 라이브러리와 imports들의 내용이 의심스러움
       # _feature 해시로 추출_
     ```

   - PESTUDIO에서 추출한 특징들

     ```python
     self.get_libraries_info()
       # 라이브러리의 블랙리스트 비율을 체크
      
     self.get_imports_info()
       # imports의 블랙리스트 비율 체크
      
     self.get_exports_info()
       # export의 크기 추출
      
      self.get_certificate()
        # 인증서의 유무 체크
     ```

   


3. 학습, 검증 (최적 모델 추출)

   - 8개의 모델 각각 학습과 검증을 거친 후 정확도를 측정

     - 학습 결과

       | 모델 | 정확도 |
       | ---- | ------ |
       | **Random Forest**   | **0.9469** |
       | Decision Tree       | 0.9126     |
       | **Light GBM**       | **0.953**  |
       | SVC                 | 0.8299     |
       | Logistic Regression | 0.8411     |
       | KNeighbors          | 0.9027     |
       | AdaBoost            | 0.8946     |
       | MLP                 | 0.84       |

   - 주의 사항

     - x의 개수와 y의 개수가 일치해야 함
     - x의 피처개수와 모델의 feature 개수가 일치해야 함



4. 최적 모델 중 두 가지만 앙상블 하여 향상된 결과 확인

   - 8개의 모델중 최적의 모델 선택
     - 정확도가 가장 높았던 `Random Forest`, `Light GBM` 두 개의 모델을 선택하여 앙상블
     - 학습 결과
       - 0.9546의 정확도 검출
       - 기존 튜토리얼 코드의 정확도 0.9433, 0.9501에서 유의미한 향상폭 검출

   

5. RFE 알고리즘을 사용하여 유효 특징 추출한 모델 생성

   - 특징 추출 후 추출한 특징으로 학습 후 정확도 측정

   - 학습 결과

     - 특징 추출 전 특징의 개수  :  1986

     - 특징 추출 후 특징의 개수  :  993

     - 정확도: 0.5919

       > 정확도가 낮아진 이유
       >
       > - 프로젝트 진행 초기에는 모델의 문제로 판단해서 Light GBM 모델을 활용하여 진행해 보았지만 결과는 비슷했음
       >
       > - feature의 문제로 판단 후 원인 파악
       >   1. 수많은 실제 특징 중 추가한 feature의 개수가 적어서 추출 후에 너무 적은 특징으로 학습함
       >   2. 이미 효과적인 특징만을 추출한 상태에서 재추출함으로써 좋은 특징이 줄어듦
       >      - 훨씬 더 많은 특징을 추가한 데이터에 대해서 적용시에 더 좋은 성능을 보일 것으로 추측

   

6. CSV 출력

   - 파일명, 정상/비정상 순으로 출력됨
   - 정상: 0, 악성 1으로 검출

   - csv 파일에 대한 예시는 다음과 같다.
     ```csv
     file,predict
     file_name_1, 0
     file_name_2, 1
     ......
     ```
