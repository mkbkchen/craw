import requests
import json
import csv
def login():
    url = "https://doss.donson.com.cn/prod-api/login"
    data={
        "password": "FORnwN+NrHqndIQtdqFrVcmomntlnNa/FBUtuhCSz73hBzjtBbszf41X4XTkgCTM7Plw29bEw6nC9P0V2T6YQMEN+HxKTOuzVLtgreQERmB56u/yEl4yw8orrF9mUSzuyiwfEasF1RKxWa0xhy1kclgNba2bxlIrY5la4LJnlwQ=",
        "username": "510329"
    }
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Content-Type":"application/json;charset=UTF-8"
    }
    res=requests.post(url=url,headers=headers,json=data)
    res=json.loads(res.text)
    token=res.get("token")
    return token



def get_data(pageNum,pageSize,token):
    url="https://doss.donson.com.cn/prod-api/finance/order/listVo?"
    params={
    "pageNum": pageNum,
    "pageSize": pageSize,
    "deptId": "12995",
    "deptName": "商业运营部",
    "params[isSalesOrder]": 1
    }
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Authorization":"Bearer "+token,
        "Content-Type":"application/json;charset=UTF-8"
    }
    res=requests.get(url=url,params=params,headers=headers)
    res=json.loads(res.text)
    return res


def get_inf(id,token):
    url="https://doss.donson.com.cn/prod-api/finance/order/orderDetail/{}".format(id)
    headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Authorization":"Bearer "+token,
    "Content-Type":"application/json;charset=UTF-8"
    }
    res=requests.get(url=url,headers=headers)
    res=json.loads(res.text)
    data=res.get("data")
    return data

    
#需要的字段
col_map={
			"客户名称":"businessName",
			"商机编码":"businessCode",
			"合同金额":"contractMoney",
			"订单金额":"orderAmount",
			"事业部":"secondDepartmentName",
            "业务类型":"businessType"
		}


# 查询字段确认对应的类型
bt_map = {
 "业务类型":{
    "Name":"businessType",
    "Map":{
        9:"营赛-服务",
        8:"营赛-产品"
    }
 }
}



def main():
    token=login()
    pageSize=10

    #获取全部的订单数
    total_page=get_data(1,1,token)["total"]
    print(total_page)
    total_pageNum=int(total_page/10)+1


    
    all_rows=[]
    #所有数据组成的列表（假如共56个数据，10个一组，共6组）
    for i in range(total_pageNum):
        res=get_data(i+1,10,token)
        # print(res.get("rows"))
        # print(i+1)
        all_rows.extend(res.get("rows"))

    #把businessTypet以字典形式加进去
    for col in all_rows:
        id=col.get("id")
        data= get_inf(id,token)
        col["businessType"]=data["businessType"]


    #得到最后的表格
    all_data=[]
    for col in all_rows:

        #得到一行数据
        row_data=[]
        for k,v in col_map.items():
            if k in bt_map:
                row_val=col.get(v,None) #得到网页的字段值
                map_val=bt_map.get(k)['Map'].get(row_val,None)#得到对应的字段值
                row_data.append(map_val)
            else:
                row_data.append(col.get(v,None))
        
        all_data.append(row_data)
    print(all_data)
    
    #写入到文件中
    with open('data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        head=[x for x in col_map.keys()]
        writer.writerow(head)
        for row  in all_data:
            writer.writerow(row)
        print("the end .")

if __name__ == "__main__":
    main()
​
