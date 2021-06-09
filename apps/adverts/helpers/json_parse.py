# from json import JSONEncoder
#
#
# class StringParse(JSONEncoder):
#     def default(self, o):
#         try:
#             iterable = o.split(sep='\r\n')
#         except TypeError:
#             pass
#         else:
#             return iterable
#         # Let the base class default method raise the TypeError
#         return iterable
