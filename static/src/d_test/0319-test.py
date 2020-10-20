# import random
#
#
# def split(full_list, shuffle=False, ratio=0.2):
#     n_total = len(full_list)
#     offset = int(n_total * ratio)
#     if n_total == 0 or offset < 1:
#         return [], full_list
#     if shuffle:
#         random.shuffle(full_list)
#     sublist_1 = full_list[:offset]
#     sublist_2 = full_list[offset:]
#     return sublist_1, sublist_2
#
#
# if __name__ == "__main__":
#     li = (1, 2)
#     sublist_1, sublist_2 = split(li, shuffle=False, ratio=0.9)
#
#     print(sublist_1, len(sublist_1))
#     print(sublist_2, len(sublist_2))
# import numpy as np
# # np.random.seed(0)
# p = np.array([0.2, 0.8])
# print(p)
# print(p.ravel())
# for i in range(50):
#     index = np.random.choice([1, 2], p=p.ravel())
#     print(index, i)


# def aa():
#     return 1
#
#
# def bb():
#     for i in range(10):
#         return i
#     return None
#
#
# a = aa()
# print(a)
# b = bb()
# print(b)