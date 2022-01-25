# import requests
# import base64
# with open('./static/test/identification_1.mp4', 'rb') as f:
#     video = base64.b64encode(f.read()).decode('ascii')
#
# data = {
#     'video_id': '132456',
#     'video': video,
#     'action_type': '抱膝提踵',
#     'function_type': '0',
#     'time_limit': ''
# }
# url = 'http://localhost:5000/process'
# requests.post(url, json=data)

import matplotlib.pyplot as plt

point = []


plt.plot(point)
plt.show()
print()
