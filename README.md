# 프로젝트1: 웹공격탐지

### 조원 소개

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

<br/>

### 프로젝트 소개

**csic 2010 데이터를 활용하여 http 로그에서 정상 / 비정상 데이터를 구분하는 학습 알고리즘을 제작한다.**

총 61,065건의 로그는 36,000 건의 정상 데이터와 25,065건의 비정상 데이터로 구성되어 있다.

비정상 데이터는

1. static attacks: 정상적이지 않은 경로로 들어오는 공격
2. dynamic attacks: request argument에 대한 공격
3. Unintentional illegal requrests: 공격의도는 없지만 비정상적인 로그

세 종류로 구분되어 있다.

<br/>

### 실행 방법

- `real_code.ipynb` 파일을 순서대로 실행한다.

  - `ModuleNotFoundError` 경고가 나오면 다음 명령어를 이용해 패키지를 설치한다.

    ```
    pip install <Package name>
    ```

---

<br/>

### 실행 환경

```
python 3.7.12 (default, Sep 10 2021, 00:21:48) [GCC 7.5.0]
python 3.9.7 (tags/v3.9.7:1016ef3, Aug 30 2021, 20:19:38) [MSC v.1929 64 bit (AMD64)]
```

위 두 환경에서는 정상적으로 작동하는 것으로 확인하였다.

---

<br/>

### 프로젝트 진행 순서 명세

1. 회의를 통해 정상 데이터와 비정상 데이터의 차이를 도출하였다.

   직접 분석을 통해 얻은 바로 데이터 상에선 url, Host, Cookie, Content-Length 만의 차이가 발견되었고 이 중 유의미한 차이로는

   - url 및 body부분에서 쓰레기값들이 발견되거나 idA pwdA등 비정상적 내용이 포함되있는 경우,
   - url의 host와 로그상의 Host의 값이 다른경우

   위 두가지의 차이가 있었다.

2. 도출한 결과를 바탕으로 훈련할 데이터에서 가져올 내용을 수정하였다.

   - 튜토리얼 코드

   - `url + host` 파싱

   - `url` 파싱

3. 최적의 데이터들을 여러 알고리즘 학습 모델을 통하여 실행하였다.

   - `logistic regression`
   - `decesion Tree`
   - `Linear SVM`
   - `random Forest`

---

<br/>

### 실행 결과

아래에서 설명하는 용어들의 정의는 다음과 같다.

- Accuracy: 올바르게 예측된 데이터의 수를 전체 데이터의 수로 나눈 값

- F1 score: precision recall의 조화평균

- precision: model이 true로 예측한 데이터 중 실제로 true인 데이터의 수

- recall: 실제로 true인 데이터를 모델이 true로 인식한 데이터의 수

<br/>

1. 파싱 내용 수정

   1. 튜토리얼 코드로 실행한 결과

      다음은 튜토리얼 코드 중 파싱 함수의 내용이다.

      ```python
      def parsing(path):
          with open(path,'r',encoding='utf-8') as f:
              train=[]
              para=""
              while True:
                  l = f.readline()
                  print(l)

                  if not l:
                      break

                  if l != "\n":
                      para +=l
                  else:
                      if para!='':
                          if para[:4]=='POST':
                              para+=f.readline()
                          train.append(para)
                          para=""
          return train
      ```

      전체 내용을 가져 오고, Method가 POST인 경우 예외적으로 body까지 가져온다.

      위의 데이터를 `random Forest` 알고리즘을 통해 실행한 결과는 다음과 같다.

      - Accuracy: 0.44769806409630714
      - F1 score: 0.5914069081718618

      Accuracy가 약 44%, F1 score가 59%로 낮게 측정되었다. 따라서 개선이 필요하다고 판단했다.

   <br/>

   2. `url + host` 파싱

      url과 host 부분에 차이가 있다고 판단했다.

      파싱 함수를 다음과 같이 변경하여 실행해 보았다.

      ```python
      def parsing(path):
          with open(path, "r", encoding="utf-8") as f:
              train = []
              head = ["POST", "PUT"]
              l = f.readlines()
              for i in range(len(l)):
                  line = l[i].split()
                  if len(line) != 0:
                      if l[i].startswith("Host: "):
                          train.append(l[i])
                      if line[0] == "GET":
                          train.append(line[0] + line[1])
                      elif line[0] in head:
                          j = 1
                          while True:
                              j += 1
                              if l[i + j].startswith("Content-Length: "):
                                  break
                          train.append(line[0] + line[1] + "?" + l[i + j + 2])

          return train
      ```

      1. readlines()로 전체파일을 받아온다.

      2. 이후 startswith() 함수를 활용하여 Host로 시작하는 부분을 추가한다.
      3. 데이터셋에서 post put은 일관적으로 content-length 부분의 두줄 뒤에 body가 나오기에 index를 활용하여
         body부분을 함께 추가해 주었다.

      위의 데이터를 `random Forest` 알고리즘을 통해 실행한 결과는 다음과 같다.

      - Accuracy: 0.7802751166789487
      - F1 score: 0.6509722312544709

      Accuracy와 F1 score가 78%, 65%로 비약적 상승하였다.

      하지만 여전히 낮은 수치라고 판단하여 다른 방법을 사용하게 되었다.

   <br/>

   3. `url` 파싱

      HOST로 인한 비정상 로그는 수가 적어서 정상 데이터와 비정상 데이터에 같은 내용의 단어가 많이 들어가서 정확도가 떨어질 것으로 예상했다.

      때문에 url만을 parsing 해서 실험해보았다.

      ```python
      def parsing(path):
          with open(path, "r", encoding="utf-8") as f:
              train = []
              head = ["POST", "PUT"]
              l = f.readlines()
              for i in range(len(l)):
                  line = l[i].split()
                  if len(line) != 0:
                      if line[0] == "GET":
                          train.append(line[0] + line[1])
                      elif line[0] in head:
                          j = 1
                          while True:
                              j += 1
                              if l[i + j].startswith("Content-Length:"):
                                  break
                          train.append(line[0] + line[1] + "?" + l[i + j + 2])

          return train
      ```

      데이터셋에서 post put은 일관적으로 content-length 부분의 두줄 뒤에 body가 나오기에 index를 활용하여
      body부분을 함께 추가해 주었다.

      위의 데이터를 `random Forest` 알고리즘을 통해 실행한 결과는 다음과 같다.

      - Accuracy: 0.964873495455662
      - F1 score: 0.9582968795567222

      Accuracy와 F1 score가 95%을 상회하며 상당히 정확해졌다.

      `random Forest`가 아닌 다른 알고리즘 모델을 사용하면 더욱 정확한 결과를 도출할 수 있다고 판단하여 실행해보았다.

<br/>

2. 여러 알고리즘 학습 모델 사용

   다음은 위에서 설명한 네 가지 모델을 코드로 구현한 모습이다.

   ```python
   # Logistic Regresstion
   from sklearn.linear_model import LogisticRegression
   def lgs_train(train_vec,train_y):
       lgs = LogisticRegression(solver='lbfgs', max_iter=1000)
       lgs.fit(train_vec,train_y)
       return lgs

   # Decision Tree
   from sklearn import tree
   def dt_train(train_vec,train_y):
       dt = tree.DecisionTreeClassifier()
       dt.fit(train_vec,train_y)
       return dt

   # Linear SVM
   from sklearn.svm import LinearSVC
   def svm_train(train_vec,train_y):
       svm = LinearSVC(C=1)
       svm.fit(train_vec,train_y)
       return svm

   # Random Forest
   from sklearn.ensemble import RandomForestClassifier
   def rf_train(train_vec,train_y):
       rf = RandomForestClassifier(200)
       rf.fit(train_vec,train_y)
       return rf
   ```

   결과는 다음과 같았다.

   |          | Logistic Regresstion | Random Forest      | Decision Tree      | Linear SVM      |
   | -------- | -------------------- | ------------------ | ------------------ | --------------- |
   | Accuracy | 0.9760910505199377   | 0.964873495455662  | 0.9662654548431999 | 0.9945959223777 |
   | F1 score | 0.9706473663047849   | 0.9582644226092032 | 0.9597262952101663 | 0.9933827956769 |

   위 알고리즘들의 threshold에 대한 ROC(Receiver Operating Characteristic: 분류 모델 성능 그래프) 는 다음과 같았다.

   ![](https://user-images.githubusercontent.com/28581806/140687402-ca370471-b93d-4552-b8ee-3f109f443744.png)

   SVM의 AUC(Area Under the Curve: ROC 곡선 아래의 영역)가 가장 크기 때문에 SVM 알고리즘을 통해 학습하는 방법이 가장 높은 정확도를 나타냈다. 이는 클래스 구별에 SVM의 성능이 훌륭하다는 것을 의미한다.

   설명은 다음과 같다.

   > SVM은 고차원 또는 무한차원공간에서 초평면 또는 초평면 집합을 구축하는 역할을 하는데, 일반적으로 마진이 클수록 분류기의 일반화 오류가 낮아지므로 모든 클래스의 가장 가까운 훈련 데이터 포인트까지 가장 중요한 거리를 가진 초평면에 의해 우수한 분리가 달성, 그런 초평면을 찾아주는것이 SVM이기에 AUC가 가장 크게 나온다고 생각한다.

   > 어떤 데이터들의 평균값을 내릴 때 편차를 줄이기 위해서는 평균이 아닌 중앙값이 더 정확한 데이터가 될때도 있다. SVM 알고리즘은 학습한 데이터들의 기준점을 선정할 때 무수히 많은 기준점들 중 편차를 최대한으로 줄일 수 있는 방법 즉, 두 데이터가 기준점과 최대한 멀게 기준점을 잡는 것(마진을 크게하는 것)이다. 또한 편차가 심한 데이터가 있을 땐 데이터를 구분하는 기준에 큰 영향을 주지 않도록 중앙값을 이용하는 것 또한 일반화 오류를 낮출 수 있는 방법일 것이다. 또한 저차원에서 보기에 기준점을 잡기 어려운 경우 커널트릭을 이용하여 다차원으로 끌어올려준 후 기준점을 잡아주는 방법(초평면을 생성하는)을 이용하기 때문에 데이터들의 기준점을 보다 명확하게 잡게 된다.

   ```



   모델에 따른 AUC 결과는 다음과 같다.

   | 모델명                 | AUC      |
   | ---------------------- | -------- |
   | LogisticRegression     | 0.974117 |
   | RandomForestClassifier | 0.967980 |
   | DecisionTreeClassifier | 0.968537 |
   | LinearSVC              | 0.993629 |


   ```
