from django.shortcuts import render
import requests
import datetime
import json
# Create your views here.


# 进入首页
def index(request):
    return render(request, 'index.html')


# 获取aqi数据
def draw(request):
    url = 'http://dockerj.top:8000/aqi/service'
    city = request.GET.get('city')
    data = {
        'city': city,
    }
    response = requests.get(url=url, params=data)
    # print(response.url)
    # 如果请求成功，则提取数值返回图表页面，否则返回出错页
    if response.status_code == 200:
        response = response.json()
        # 判断该城市是否存在，如存在，则渲染模版
        if response['code'] == 0:
            time = datetime.datetime.now().strftime('%Y-%m-%d')
            # print(time)
            # pprint.pprint(response)
            attr = ['PM2.5','PM10', 'SO2','NO2','O3']
            v1 = []
            arr = list(response['data'].values())
            del arr[-2]
            for value in arr:
                if value !='暂无':
                    v1.append(value[:-5])
                else:
                    v1.append('0')
            #获取建议
            advice = response['advice']
            # print(advice)
            # 获取未来15日空气质量指数
            aqi = response["未来15天空气质量指数"]
            print(aqi)
            #构建echarts数据
            aqi_data = []
            L = len(attr)
            for i in range(L):
                aqi_data.append(dict(value=v1[i], name=attr[i]))
            # print(aqi_data)
            return render(request, 'result.html', {
                'data': json.dumps({'aqi_data': aqi_data, 'city': city,'time': time,'attr': attr, 'datalist': v1,'aqi':aqi}),
                'city': city,
                'advice':advice
            })
        else:
            return render(request, 'notfound.html')
    else:
        return render(request, 'error.html')

