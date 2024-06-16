# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : test_xpath.py
@Project            : S001_bilibili_API
@CreateTime         : 2024/6/16 17:03
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2024/6/16 17:03 
@Version            : 1.0
@Description         : None
"""
src = """
<table id="table1" cellspacing="0px">
  <tr>
    <th>编号</th>
    <th>姓名</th>
    <th>年龄</th>
  </tr>
  <tr>
    <td>1</td>
    <td>张三</td>
    <td>11</td>
  </tr>
  <tr>
    <td>2</td>
    <td>李四</td>
    <td>12</td>
  </tr>
  <tr>
    <td>3</td>
    <td>王五</td>
    <td>13</td>
  </tr>
  <tr>
    <td>4</td>
    <td>马六</td>
    <td>14</td>
  </tr>
</table>
"""

from lxml import etree

content = etree.HTML(src)
print(type(content))

trs = content.xpath('//table[@id="table1"]/tr')[1:]
print(type(trs))

for row in trs:
    print(type(row))
    id = row.xpath('./td[1]/text()')[0]
    name = row.xpath('./td[2]/text()')[0]
    age = row.xpath('./td[3]/text()')[0]
    print(id, name, age)
