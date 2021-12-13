def ensemble_test_result(X, models):
    test_predict = []
    predicts = []
    for model in models:
        prob = [result for _, result in model.predict_proba(X)]
        predicts.append(prob)

    predict = np.mean(predicts, axis=0)
    predict = [1 if x >= 0.5 else 0 for x in predict]

    with open("predict.csv", "w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["file", "predict"])
        for a in range(10000):
            wr.writerow([os.path.splitext(l_test[a])[0], predict[a]])

    print(predict)
