# ai malware detection

##주어진 목표 : pe 파일이 주어졌을 때, 주어진 파일이 악성파일인지 정상파일인지 판별하는 *이진분류기 모델* 만드는 것이 목표

---

## pe파일이란 
+ Portable Excutable 파일
+ 윈도우 상에서 실행 가능한 프로그램
+ ex) exe dll sys 등등

## 문 제 
1. 주어진 파일에서 어떤 특징이 악성의 근거가 되는지 모름
2. 분류기를 어떻게 만드는 가
 + 파일의 특징을 최대한 추출한 후, 이 특징들을 머신러닝으로 학습시켜 주어진 파일이 악성이 되는 조건을 찾자
  + PEMIER, EMBER, PESTUDIO에서 다양한 feature(특징)들을 추출하여 accuracy 높이기

## 진행 순서
1. 주요 라이브러리  import
2. EMBER, PESTUDIO에서 적절한 특징 추출 함수 작성
3. 학습데이터 구성 (20000개) | 검증데이터 구성 (10000개)
 + PESTUDIO 특징 추가시 x의 차원이 1차원으로 낮아지는 문제 발생 -> 추가하지 않음
 # 근데 지금 100개만 해보니까 차원 그대로로 나온다....?? 코드 바꿔서 push 해둠 마지막으로 테스트 해보고 안되면 그냥 없애고 없애는 이유 고민해보자 코드 추가는 해뒀는데 pestudio 값은 추가 안되는데 폰 pestudio로 하자 뒤에 문제 생기면 그때 없애고 
4. 학습, 검증 (최적 모델 추출)
 - 주의 사항
  - x의 개수와 y의 개수가 일치해야함
  - x의 피처개수와 모델의 피처 개수가 일치해야함
  - 이는 RFE모델 학습중 알아낸 사실임
5. 최적 모델 중 몇가지만 앙상블 하여 향상된 결과 확인
6. RFE 알고리즘을 사용하여 유효 특징 추출한 모델 생성
7. CSV 출력
 - 'file', 'predict'
 - '파일명1', '0 or 1'
 - '파일명2', '0 or 1'
 - ......
 




## 우리의 할 일
1. EMBER, PESTUDIO 파일을 분석하여 핵심적인 header내용 추출
 + 우리가 이해할 수 있는 선에서 확실히 오류로 판별될 가능성이 있는 feature 골라잡기
2. 추출한 내용을 수치적으로 표현방법 찾기
 + 최대한의 데이터 활용 + 해시함수 적용
3. 8개의 모델중 최적의 모델 선택
 + "rf", "lgb", "dt", "svm", "lr", "knn", "adaboost", "mlp"
 + 학습데이터 활용 시 무지성 반복문으로 골라내기

## 추가한 라이브러리들
 >from tqdm import tqdm # 반복문에서의 진행정도 살피기
 >from sklearn.feature_extraction import FeatureHasher # 숫자로 이루어져 있지 않은 데이터 가공을 위한 hash

## EMBER에서 추출한 특징들
+ self.get_header_info()
 - header의 size가 지나치게 많거나
 - version이 잘 못 되는 등의 상황은 의심스러움
+ self.get_exports_info()
 - 악성코드의 경우 export를 많이 할것으로 예상됨
 - *feature 해시로 추출*
+ self.get_imports_info()
 - import하는 라이브러리와 imports들의 내용이 의심스러움
 - *feature 해시로 추출*

## PESTUDIO에서 추출한 특징들
+ self.get_libraries_info()
 - 라이브러리의 블랙리스트 비율을 체크
+ self.get_imports_info()
 - imports의 브랙리스트 비율 체크
+ self.get_exports_info()
 - export의 크기 추출 (길다면 의심감)
+ self.get_certificate()
 - 인증서의 유무 체크

 # 시간많고 멘탈 괜찮으면 특징추출 싹 긁어다가 추가해놓고 RFE돌려서 모델 뽑는게 좋아보이는데 너무 힘들다 난 여기까지인가보다