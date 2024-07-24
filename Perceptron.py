#Student name: Zaid Khan
#Assignment #: 3


import numpy as np
import csv

def read_data(file, has_labels=True):
    data = []
    with open(file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if has_labels:
                
                features = [float(x) for x in row[:-1]]
                label = row[-1].strip().lower()  
                data.append(features + [label])
            else:
                
                features = [float(x) for x in row]
                data.append(features)
    return data

train_data = read_data('hw-files/train.csv', has_labels=True)
test_data = read_data('hw-files/test.csv', has_labels=False)
test_with_truth_data = read_data('hw-files/test_with_truth.csv', has_labels=True)

def perceptron(data, learning_rate, max_epochs, initial_bias):
    w = np.zeros(len(data[0])-1)
    b = initial_bias
    for epoch in range(max_epochs):
        errors = 0
        for row in data:
            x = np.array(row[:-1], dtype='float')
            y = 1 if row[-1] == 'bright' else -1
            if y * (np.dot(w, x) + b) <= 0:
                w = w + learning_rate * y * x
                b = b + learning_rate * y
                errors += 1
        print(f"epoch {epoch+1}, errors: {errors}")  
        if errors == 0:
            print(f"Training converged after {epoch+1} epochs")
            break
    return w, b

def predict(data, w, b):
    predictions = []
    for row in data:
        x = np.array(row, dtype='float')
        if np.dot(w, x) + b > 0:
            predictions.append('bright')
        else:
            predictions.append('dim')
    return predictions

def evaluate(test_data, predictions):
    results = []
    for row, prediction in zip(test_data, predictions):
        results.append(f"{','.join(map(str, map(int, row)))}, {prediction}")
    return results

def calculate_confusion_matrix(test_with_truth_data, predictions):
    TP = TN = FP = FN = 0
    for row, prediction in zip(test_with_truth_data, predictions):
        true_label = row[-1]
        if true_label == 'bright' and prediction == 'bright':
            TP += 1
        elif true_label == 'bright' and prediction == 'dim':
            FN += 1
        elif true_label == 'dim' and prediction == 'bright':
            FP += 1
        elif true_label == 'dim' and prediction == 'dim':
            TN += 1
    return TP, TN, FP, FN

def run_experiment(initial_bias):
    learning_rate = 0.1
    max_epochs = 50
    print(f"\nRunning experiment with initial bias = {initial_bias}")
    w, b = perceptron(train_data, learning_rate, max_epochs, initial_bias)
    
    predictions = predict(test_data, w, b)
    results = evaluate(test_data, predictions)
    
    print("20 test samples evaluated, Result:")
    for result in results:
        print(result)
    
    TP, TN, FP, FN = calculate_confusion_matrix(test_with_truth_data, predictions)
    
    print('Confusion Matrix:')
    print(f'                Classified Positive  Classified Negative')
    print(f'Truth Positive  TP = {TP}            FN = {FN}')
    print(f'Truth Negative  FP = {FP}            TN = {TN}')
    
    accuracy = (TP + TN) / (TP + TN + FP + FN)
    print('Accuracy: ', f"{accuracy * 100:.2f}%")

def main():
    biases = [-1, 0, 1]
    for bias in biases:
        run_experiment(bias)

if __name__ == '__main__':
    main()
