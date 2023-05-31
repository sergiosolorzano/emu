import os

filepath = '/home/sergio/Simple_Selfgen/example.py'

filename = os.path.basename(filepath)
path_without_filename = os.path.dirname(filepath)

print('Filename:', filename)
print('Path without filename:', path_without_filename)
