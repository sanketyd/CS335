class Node:
    #misc here is supposed to be tuple
    def __init__(self, place = None, val = None, is_var = True, Type = None, category = None, is_arr = False, arr_dims = [], misc = None):
        self.place = place
        self.val = val
        self.is_var = is_var
        self.Type = Type
        self.is_arr = is_arr
        self.arr_dims = arr_dims
        self.category = category
        self.misc = misc
