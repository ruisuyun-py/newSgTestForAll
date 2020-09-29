import time
import requests
import page.base_page as base
import interface.vip.vip_interface as vip_interface
import interface.product.product_interface as product_interface
import interface.inventory.inventory_interface as inventory_interface
import interface.setting.setting_interface as setting_interface


# 新建订单
def new_order(vip_name, sku_info, warehouse_name='主仓库', express_name='买家自提', shop_name='阿里测试店铺01', other={}):
    """
    vip_name:会员名
    sku_info:商品信息列表，商品信息字典，如下
    sku_info = [{'商家编码': '测试商品1-红色 XS', '数量': '2'}, ]
    other_info= {"卖家备注": "111"}
    return:order_info ，订单信息，包含订单id和订单编码
    格式：{'ID': '7495084473608831886', 'Code': 'TD200903013'}
    """
    vip_info = vip_interface.get_vip_info(vip_name)
    order = {
        "Id": "0",
        "Tid": "",
        "OrderType": 1,
        "DealDate": time.strftime('%Y-%m-%d %H:%M:%S'),
        "ShopId": setting_interface.get_shop_id(shop_name),
        "VipId": vip_info["data"]["Items"][0]["VipId"],
        "VipName": vip_info["data"]["Items"][0]["VipName"],
        "ExpressId": setting_interface.get_express_id(warehouse_name, express_name),
        "PostFee": 0,
        "WarehouseId": inventory_interface.get_inventory_id(warehouse_name),
        "ProvinceName": "上海",
        "CityName": "上海市",
        "DistrictName": "闵行区",
        "ReceiverName": vip_info["data"]["Items"][0]["ReceiverName"],
        "ReceiverPhone": vip_info["data"]["Items"][0]["ReceiverPhone"],
        "ReceiverMobile": vip_info["data"]["Items"][0]["ReceiverMobile"],
        "ReceiverRegionId": vip_info["data"]["Items"][0]["ReceiverRegionId"],
        "ReceiverZip": vip_info["data"]["Items"][0]["ReceiverZip"],
        "ReceiverAddress": vip_info["data"]["Items"][0]["ReceiverAddress"],
        "SellerMemo": "",
        "BuyerMemo": "",
        "Note": "",
        "SettlementMode": 0,
        "SalesManId": "0",
        "SalesManName": "",
        "SellerFlag": 0,
        "InvoiceTitle": "",
        "InvoiceNo": ""
    }
    if len(other) != 0:
        for k, v in other.items():
            if k == "卖家备注":
                order["SellerMemo"] = v
            elif k == "买家备注":
                order["BuyerMemo"] = v
            elif k == "便签":
                order["Note"] = v
            elif k == "运费":
                order["PostFee"] = v
            elif k == "旗帜":
                order["SellerFlag"] = v
    headers = {
        'Cookie': base.cookies
    }
    url_param = ''
    for k, v in order.items():
        url_param += f"'{k}':'{v}',"
    url = "http://gw.erp12345.com/api/Orders/AllOrder/AddOrder?order={" + url_param + "}"
    print(url)
    response = requests.get(url, headers=headers, )
    result = dict(response.json())
    print(f"订单创建结果{result}")
    start = result['data']['OrderCodeTid'].find("T")
    end = len(result['data']['OrderCodeTid'])
    order_info = {"ID": result['data']['Id'], "Code": result['data']['OrderCodeTid'][start: end]}
    # 添加订单主体完成，下面需要添加商品信息
    url_param = ''
    sku_info_list = []
    for i in sku_info:
        sku = {"SkuId": product_interface.get_sku_info(i["商家编码"])["data"]["Items"][0]["Id"], "Qty": i["数量"]}
        sku_info_list.append(sku)
    for sku in sku_info_list:
        url_param += '{'
        for k, v in sku.items():
            url_param += f"'{k}':'{v}',"
        url_param += '},'
    url = "http://gw.erp12345.com/api/Orders/AllOrder/AddOrderLine?orderId=" + order_info[
        "ID"] + "&skus=[" + url_param + "]"
    print(url)
    requests.get(url, headers=headers, )
    # 添加支付信息
    url = "http://gw.erp12345.com/api/Orders/AllOrder/FastAddOrderPayment?orderId=" + order_info["ID"] + ""
    requests.get(url, headers=headers)
    return order_info


# 获取订单信息
def get_order_info_by_fuzzy(fuzzy_keywords, required_information_list):
    """
    fuzzy_keywords:模糊搜索的关键字
    required_information_list：需要的信息名称,比如：[info_name1, info_name2, info_name3]
    return:[{"info_name1": "value", "info_name2": "value", "info_name3": "value",}]
    """
    """
    原始信息：
    {data: {Items: [{WaitApproveMaxId: "7495029146578322338",…}], TotalCount: 1}, code: 1, message: null}
    code: 1
        data: {Items: [{WaitApproveMaxId: "7495029146578322338",…}], TotalCount: 1}
            Items: [{WaitApproveMaxId: "7495029146578322338",…}]
                0: {WaitApproveMaxId: "7495029146578322338",…}
                    Approved: false
                    BuyerMemo: ""
                    Code: "TD200727007"
                    DeliveryCompleted: false
                    DispatchCompleted: false
                    EncriptReceiverMobile: "$176$CkuuVaTZ5CdQYgSEVM/phA==$1$"
                    EncriptReceiverName: "~xNPw4a7Nc5bLCphunyYZjQ==~1~"
                    EncriptReceiverPhone: null
                    ExceptionMessage: "其他ERP已发货"
                    ExceptionType: 1048576
                    ExpressId: "7494440373939341490"
                    ExpressName: "邮政小包电子面单"
                    ExpressNo: null
                    Id: "7495029146578322338"
                    ImBackGroundImgUrl: "https://amos.alicdn.com/online.aw?v=2&uid=t_1479214728795_0&site=cntaobao&s=2&charset=utf-8"
                    ImUrl: "https://amos.alicdn.com/getcid.aw?v=3&site=cntaobao&groupid=0&s=1&fromid=&uid=t_1479214728795_0&status=1&charset=utf-8"
                    InvoiceNo: null
                    InvoiceTitle: null
                    IsCod: false
                    IsEnd: false
                    LackType: 4
                    Note: "{来源:WAP,WAP}"
                    OrderCodeTid: "1146084768821949721<br/>[全缺]TD200727007"
                    OrderCount: 4
                    OrderStatus: "其他ERP已发货"
                    OrderTypeName: "销售订单"
                    PayDate: "2020-07-27 18:24:55"
                    PayDays: 29
                    Platform: 1
                    PostFee: 0
                    ProHtml: "<span class="good-box"><span class="label">1</span><img src="https://img.alicdn.com/bao/uploaded/i2/2462224143/O1CN01Bpi9Ny1gTXTt4cGoS_!!2462224143.jpg_30x30.jpg" title="07080932-黑 43-46 43-46" /></span><span class="good-box"><span class="label">1</span><img src="https://img.alicdn.com/bao/uploaded/i2/2462224143/O1CN01Bpi9Ny1gTXTt4cGoS_!!2462224143.jpg_30x30.jpg" title="07080932-蓝 35-38 35-38" /></span><span class="good-box"><span class="label">1</span><img src="https://img.alicdn.com/bao/uploaded/i2/2462224143/O1CN01Bpi9Ny1gTXTt4cGoS_!!2462224143.jpg_30x30.jpg" title="07080932-红 31-34 31-34" /></span>"
                    ProList: [{Id: "7495029146578322338",…}, {Id: "7495029146578322338",…}, {Id: "7495029146578322338",…}]
                    ReceiverAddress: "上海 上海市 闵行区 浦江镇永杰路439弄永康城浦晨雅苑1号楼401"
                    ReceiverMobile: "17673647529"
                    ReceiverName: "郭习浪"
                    ReceiverPhone: null
                    ReceiverRegionId: "1234668550602865521"
                    RecordDate: "2020-07-27 18:25:48"
                    SellerFlag: 1
                    SellerMemo: "天下无敌  建单人：售后专用 - 建单时间：07/28 - 物流单号：568888544 -天下无敌共退1件;(货品信息:【07080932-蓝 35-蓝色 35—38*1】)|2020-07-28 17:12:48退货退款-ERP对接入仓自动退（淘宝）.195307080932-蓝 35-381.00  建单人：售后专用 - 建单时间：07/28 - 物流单号：568888544 -天下无敌共退1件;(货品信息:【07080932-蓝 35-蓝色 35—38*1】);共换1件(货品信息:【07080932-蓝 X-蓝色 XL*1】) （收）07080932-蓝 35-蓝色 3538*1（换）07080932-蓝 X-蓝色 XL*1"
                    ShopId: "7494677199308457149"
                    ShopName: "巨淘气"
                    SortKey: "1_[07080932-黑 43-46 43-46][07080932-红 31-34 31-34][07080932-蓝 35-38 35-38]"
                    SourceType: 1
                    StatusType: 4
                    SumAmount: 3
                    SumDeliveriedQty: 0
                    SumDiscountAmount: 0
                    SumDispatchedQty: 0
                    SumQty: 3
                    Tid: "1146084768821949721"
                    TradeOnlineUrl: "https://trade.taobao.com/trade/detail/trade_item_detail.htm?bizOrderId=1146084768821949721"
                    TradeStatus: 8
                    Type: 1
                    UnPaidAmount: 0
                    VipName: "t_1479214728795_0"
                    WaitApproveMaxId: "7495029146578322338"
                    WarehouseId: "162573418911628622"
                    WarehouseName: "主仓库"
                    Weight: 0
        TotalCount: 1
    message: null
    """
    url_params = {
        "Fuzzy": fuzzy_keywords,
        'ModelTypeName': 'ErpWeb.Domain.ViewModels.Orders.AllOrderVmv',
    }
    url = "http://gw.erp12345.com/api/Orders/AllOrder/QueryPage?"
    for k, v in url_params.items():
        url += f"{k}={v}&"
    headers = {
        'Cookie': base.cookies
    }
    response = requests.get(url, headers=headers)
    result = dict(response.json())
    information_mapping = {
        "是否审核": "Approved",
        "买家备注": "BuyerMemo",
        "订单编码": "Code",
        "是否发货": "DeliveryCompleted",
        "是否配货完成": "DispatchCompleted",
        "加密收货人电话": "EncriptReceiverMobile",
        "加密收货人姓名": "EncriptReceiverName",
        "加密收货人手机": "EncriptReceiverPhone",
        "异常消息": "ExceptionMessage",
        "快递": "ExpressName",
        "快递单号": "ExpressNo",
        "ID": "Id",
        "发票编号": "InvoiceNo",
        "发票抬头": "InvoiceTitle",
        "是否锁定": "IsCod",
        "是否终结": "IsEnd",
        "便签": "Note",
        "订单数": "OrderCount",
        "订单状态": "OrderStatus",
        "订单类型": "OrderTypeName",
        "付款时间": "PayDate",
        "付款天数": "PayDays",
        "运费": "PostFee",
        "商品信息": "ProList",
        "收货地址": "ReceiverAddress",
        "电话": "ReceiverMobile",
        "收货人": "ReceiverName",
        "手机": "ReceiverPhone",
        "创建时间": "RecordDate",
        "旗帜": "SellerFlag",
        "卖家备注": "SellerMemo",
        "店铺": "ShopName",
        "总金额": "SumAmount",
        "总发货数": "SumDeliveriedQty",
        "总优惠金额": "SumDiscountAmount",
        "总未配货数": "SumDispatchedQty",
        "商品数量": "SumQty",
        "平台单号": "Tid",
        "未付金额": "UnPaidAmount",
        "会员名": "VipName",
        "仓库": "WarehouseName",
        "重量": "Weight",
    }
    information_list = []
    for k in result["data"]["Items"]:
        info_dict = {}
        for i in required_information_list:
            info_code = information_mapping[i]
            info_dict[i] = k[info_code]
        information_list.append(info_dict)
    return information_list


# 获取订单的商品明细详情
def get_order_product_detail(order_id, required_information_list):
    """
    order_id:该订单的id
    required_information_list:比如：["商家编码", "商品名称", "规格名称", "平台商家编码", "平台规格名称", "平台商品ID", ]
    return:[{"商家编码":"value", "": "", "": "", "": "", "": "", "": "", "": "",},.....]
    """
    """
    原始数据
    {data: {SumQty: 3, ProductAmount: 3, ExceptionItems: [],…}, code: 1, message: null}
    code: 1
        data: {SumQty: 3, ProductAmount: 3, ExceptionItems: [], Lines: [],…}
            ExceptionItems: []
                Lines: [{Id: "7495029146578322340", ProductId: "7495033536907314668", SkuId: "7495003057839669914",…},…]
                    0: {Id: "7495029146578322340", ProductId: "7495033536907314668", SkuId: "7495003057839669914",…}
                    1: {Id: "7495029146578322341", ProductId: "7495033536907314668", SkuId: "7495003057822892485",…}
                    2: {Id: "7495029146578322342", ProductId: "7495033536907314668", SkuId: "7495003057806115286",…}
                        Amount: 1
                        CanDispatchQty: -6
                        ComboQty: 0
                        DeliveriedQty: 0
                        DeliveryCompleted: false
                        DispatchedQty: 0
                        ExceptionTypeMessage: null
                        HeaderId: "0"
                        Id: "7495029146578322342"
                        IsCombo: false
                        IsGift: false
                        Oid: "1146084768824949721"
                        OnlineStatus: "交易完成"
                        OnlineUrl: "https://item.taobao.com/item.htm?id=610510713972"
                        OriginPrice: 1
                        PicUrl: "https://img.alicdn.com/bao/uploaded/i2/2462224143/O1CN01Bpi9Ny1gTXTt4cGoS_!!2462224143.jpg"
                        PlatProductCode: "200615192123"
                        PlatProductId: "610510713972"
                        PlatProductName: "测试专用 勿拍，不发货"
                        PlatSkuCode: "07080932-红 31-34"
                        PlatSkuId: "4555424594867"
                        PlatSkuName: "红色 31-34"
                        ProductCategoryId: "0"
                        ProductCode: "07080932"
                        ProductId: "7495033536907314668"
                        ProductName: "07080932"
                        Qty: 1
                        SkuCode: "07080932-红 31-34 31-34"
                        SkuId: "7495003057806115286"
                        SkuName: "红色 31-34"
                        SkuWeight: 0
                        SupplierId: "0"
                        ThumbnailUrl: "https://img.alicdn.com/bao/uploaded/i2/2462224143/O1CN01Bpi9Ny1gTXTt4cGoS_!!2462224143.jpg_30x30.jpg"
                        Tid: null
            ProductAmount: 3
            SumQty: 3
    message: null
    """
    url_params = {
        "orderId": order_id,
    }
    url = "http://gw.erp12345.com/api/Orders/AllOrder/GetOrderLines?"
    for k, v in url_params.items():
        url += f"{k}={v}&"
    headers = {
        'Cookie': base.cookies
    }
    response = requests.get(url, headers=headers)
    result = dict(response.json())
    information_mapping = {
        "总金额": "Amount",
        "可配货库存": "CanDispatchQty",
        "配货数量": "DispatchedQty",
        "是否套餐": "IsCombo",
        "是否赠品": "IsGift",
        "平台单号": "Oid",
        "线上状态": "OnlineStatus",
        "原始单价": "OriginPrice",
        "平台货号": "PlatProductCode",
        "平台商品ID": "PlatProductId",
        "平台商品名称": "PlatProductName",
        "平台商家编码": "PlatSkuCode",
        "平台规格ID": "PlatSkuId",
        "平台规格名称": "PlatSkuName",
        "货号": "ProductCode",
        "商品名称": "ProductName",
        "数量": "Qty",
        "商家编码": "SkuCode",
        "商品ID": "SkuId",
        "规格名称": "SkuName",
        "商品重量": "SkuWeight",
        "供应商ID": "SupplierId",
    }
    information_list = []
    for k in result["data"]["Lines"]:
        info_dict = {}
        for i in required_information_list:
            info_code = information_mapping[i]
            info_dict[i] = k[info_code]
        information_list.append(info_dict)
    return information_list


# 门店开单
def new_pos_oder(vip_name, sku_info):
    """
    由于需要打开页面才能读取到NewId,所以必须使用try catch 包裹
    vip_name ：会员名称
    sku_info:商品信息列表，商品信息字典，如下
sku_info = [
        {'SkuCode': '测试商品1-红色 XS', 'Qty': '2', 'Price': "100"},
        {'SkuCode': '测试商品1-红色 S', 'Qty': '2', 'Price': "100"},
        {'SkuCode': '测试商品1-红色 M', 'Qty': '2', 'Price': "100"},
    ]
    """
    with base.operate_page("订单", "门店收银", "门店收银框架") as e:
        vip_info = vip_interface.get_vip_info(vip_name)
        js = " return model.NewId;"
        new_id = base.driver.execute_script(js)
        url = "http://gw.erp12345.com/api/Pos/Pos/SingleSettle?dto={"
        dto = {
            "VipId": vip_info["data"]["Items"][0]["VipId"],
            "ShopId": "7494440358269421036",
            "WarehouseId": "162573418911628622",
            "SalesManId": "7494505976142234005",
            "SalesManName": "测试",
            "ReceiverPhone": vip_info["data"]["Items"][0]["ReceiverPhone"],
            "ReceiverMobile": vip_info["data"]["Items"][0]["ReceiverMobile"],
            "ReceiverZip": vip_info["data"]["Items"][0]["ReceiverZip"],
            "ReceiverRegionId": vip_info["data"]["Items"][0]["ReceiverRegionId"],
            "ReceiverName": vip_info["data"]["Items"][0]["ReceiverName"],
            "ReceiverAddress": vip_info["data"]["Items"][0]["ReceiverAddress"],
            "SumQty": 2,
            "SumRefundQty": 0,
            "SumAmount": 200,
            "Memo": "",
            "PayType": "2341617839082309572",
            "PaidAmount": 200,
            "DiscountAmount": 0,
            "PlatformPayCode": "",
            "PayAccount": "",
            "OrderCode": "",
            "NewId": f"{new_id}"
        }
        for k, v in dto.items():
            url += f'"{k}":"{v}",'
        # 用于存储商品信息
        lines = []
        line = {}
        for sku in sku_info:
            sku_id = product_interface.get_sku_info(sku["SkuCode"])["data"]["Items"][0]["Id"]
            line["Id"] = sku_id
            line["Qty"] = sku["Qty"]
            line["Price"] = sku["Price"]
            line["VipPrice"] = vip_interface.get_sku_price_by_vip_id(vip_name, sku["SkuCode"])
            actual_amount = int(line["Price"]) * int(line["Qty"])
            line["ActualAmount"] = actual_amount
            discount = int(line["Price"]) / int(line["VipPrice"])
            line["Discount"] = discount
            lines.append(dict(line))
        url += "Lines:["
        for s in lines:
            url += "{"
            for k, v in s.items():
                url += f"'{k}':'{v}',"
            url += "},"
        url += "]}"
        headers = {
            'cookie': base.cookies
        }
        response = requests.post(url, headers=headers)
        result = dict(response.json())
        return result


# 审核订单
def approve_order(order_id):
    """
    order_id:订单ID
    """
    url = "http://gw.erp12345.com/api/Orders/AllOrder/ApproveSalesOrder?"
    params = {
        "orderIds": order_id,
        "isForcedNonCheckDispatched": "false"
    }
    for k, v in params.items():
        url += f"{k}={v}&"
    headers = {
        'Cookie': base.cookies
    }
    # print(url)
    response = requests.get(url, headers=headers)
    result = dict(response.json())
    return result
