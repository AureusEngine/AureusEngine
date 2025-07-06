class UserSession:
    def __init__(self, user_id):
        self.user_id = user_id
        self.session_results = []
        self.pattern_history = []
        self.predictions = []
        self.feedback = []

    def add_result(self, result):
        self.session_results.append(result)

    def add_prediction(self, prediction):
        self.predictions.append(prediction)

    def add_feedback(self, feedback):
        self.feedback.append(feedback)

    def reset_session(self):
        self.session_results = []
        self.predictions = []
        self.feedback = []