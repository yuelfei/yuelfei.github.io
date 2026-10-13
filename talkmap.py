

# # Leaflet cluster map of talk locations
#
# (c) 2016-2017 R. Stuart Geiger, released under the MIT license
#
# Run this from the _talks/ directory, which contains .md files of all your talks. 
# This scrapes the location YAML field from each .md file, geolocates it with
# geopy/Nominatim, and uses the getorg library to output data, HTML,
# and Javascript for a standalone cluster map.
#
# Requires: glob, getorg, geopy

'''
是一个“生成演讲地点地图”的脚本。它的作用不是展示文章内容，而是把你在各篇 talk 里写的地点，整理成一张地图。

它具体做了什么
扫描 _talks 目录下的所有 Markdown 文件
找每篇文章里的 location 字段
用 geopy + Nominatim 把“地点名”转成经纬度
把这些地点收集到一个字典里
最后调用 getorg 生成一个聚类地图页面，输出到 talkmap/ 目录

'''

import glob
import getorg
from geopy import Nominatim

g = glob.glob("*.md")


geocoder = Nominatim()
location_dict = {}
location = ""
permalink = ""
title = ""


for file in g:
    with open(file, 'r') as f:
        lines = f.read()
        if lines.find('location: "') > 1:
            loc_start = lines.find('location: "') + 11
            lines_trim = lines[loc_start:]
            loc_end = lines_trim.find('"')
            location = lines_trim[:loc_end]
                            
           
        location_dict[location] = geocoder.geocode(location)
        print(location, "\n", location_dict[location])


m = getorg.orgmap.create_map_obj()
getorg.orgmap.output_html_cluster_map(location_dict, folder_name="../talkmap", hashed_usernames=False)




