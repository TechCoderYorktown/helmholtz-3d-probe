class RunHistory:

    def __init__(self):
        self.runs = []

    def start_new_run(self):
        self.runs.append([])

    def add_sample(self, row):

        if not self.runs:
            self.start_new_run()

        self.runs[-1].append(row)

    def current_run(self):

        if not self.runs:
            return []

        return self.runs[-1]

    def all_runs(self):
        return self.runs

    def clear(self):
        self.runs.clear()