class TAC:
    def __init__(self):
        self.code_list = []
        self.label_count = 0

    def emit(self, dest, src1, src2, op):
        self.code_list.append([dest, src1, src2, op])

    def new_label(self):
        self.label_count += 1
        return "label_" + str(self.label_count)
