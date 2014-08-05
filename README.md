# Image classification Restful service for WMTS #
为WMTS瓦片提供一个影像分类的Rest服务和一个应用的Demo

## Rest服务的功能 ##

1. 输入
   > 读取WMTS服务Url，以及需要分类的Bbox参数；
2. 输出
   > GeoJson格式的返回值。

## 分类处理的逻辑 ##

需要的技术手段及软件
* decaf 以及Pre-trained imagenet文件；
* scikit-learn SGDLinearclassifier 实现Online Learning minibatch
* Python Multiprocessing 实现并行处理 进程池等技术
* landze 抓取wmts瓦片
* python-geojson 
* restful-flask 基于flask的restful服务创建

需要注意的地方：

demo应用可以开发一个网站，但是必要性不大，可以通过Geojson转Shp与WMTS叠加展示。
