class F1ScoreCounter:
    def __init__(self):
        self.true_positive = 0
        self.false_positive = 0
        self.true_negative = 0
        self.false_negative = 0

    def update(self, is_face_detected, is_face_present):
        if is_face_detected and is_face_present:
            self.true_positive += 1
        elif is_face_detected and not is_face_present:
            self.false_positive += 1
        elif not is_face_detected and is_face_present:
            self.false_negative += 1
        else:
            self.true_negative += 1

    def calculate_f1_score(self):
        try:
            precision = self.true_positive / (self.true_positive + self.false_positive)
            recall = self.true_positive / (self.true_positive + self.false_negative)
            f1_score = 2 * (precision * recall) / (precision + recall)
            return f1_score
        except ZeroDivisionError:
            return 0.0

    def reset(self):
        self.true_positive = 0
        self.false_positive = 0
        self.true_negative = 0
        self.false_negative = 0