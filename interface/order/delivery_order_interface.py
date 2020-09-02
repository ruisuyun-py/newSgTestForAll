import time
import requests
import page.base_page as base


# 获取已出库包裹主表信息
def get_delivery_order_info(query_params_dict, return_info_list):
    """
    query_params_dict:查询信息字典{"模糊搜索": "1", "出库时间": "2020-08-28 00:00:00,2020-08-29 00:00:00", "": "", "": "", "": "", "": "", }
    return_info_list：需要返回的信息列表,如：["物流单号", "会员名称", ]
    """
    """
    return:
    {"data":
        { "Items":
            [
                {"Id":"7495067250655756700","OrderType":8,"OrderTypeName":"[门店]",
                "WarehouseName":"主仓库","ExpressName":"买家自提","Code":"DO200823007","ExpressNo":"DO200823007","PlatCode":null,
                "ProductQuantity":2,"PickCount":0,"PayDate":"2020-08-23 01:18:43","ExpressPrintDate":"2020-08-23 01:18:44",
                "DeliverySendDate":"2020-08-23 01:18:44","TranStatusModifyDate":null,"ScanDate":null,"IsPlatDelivery":false,
                "IsPrintExpress":true,"IsWeight":false,"IsScan":false,"IsTrans":false,"IsSplit":false,"ShopName":"测试门店1",
                "VipName":"20200823011805","Note":null,"ConsigneeName":"7495067250018222081","Weight":0.0,"WeightQty":0.0,
                "SumAmount":200.0,"ConsigneeAdress":"7495067250018222081","DeliverySendUser":"测试","ScanUser":null,
                "WeightUser":null,"PackageUser":null,"PlatDeliveryDate":null,"TranStatusName":"未知状态","ExpressCost":0.0,
                "BatchCode":null,"PackageMemo":null,"Platform":0,"EncriptReceiverMobile":null,"EncriptReceiverPhone":null,
                "EncriptReceiverName":null},
            ]
        ,"TotalCount":2393
        },
    "code":1,
    "message":null
    }
    """
    # 信息对照表,方便通过显示名称获取数据库字段名称
    info_map = {
        "ID": "Id",
        "订单类型": "OrderType",
        "订单类型名称": "OrderTypeName",
        "仓库": "WarehouseName",
        "快递": "ExpressName",
        "发货单号": "Code",
        "物流单号": "ExpressNo",
        "平台单号": "PlatCode",
        "商品数量": "ProductQuantity",
        "点货数量": "PickCount",
        "付款时间": "PayDate",
        "面单打印时间": "ExpressPrintDate",
        "出库时间": "DeliverySendDate",
        "物流更新时间": "TranStatusModifyDate",
        "扫描时间": "ScanDate",
        "物流单打印": "IsPrintExpress",
        "称重状态": "IsWeight",
        "扫描状态": "IsScan",
        "装车状态": "IsTrans",
        "是否拆包": "IsSplit",
        "店铺": "ShopName",
        "会员名称": "VipName",
        "便签": "Note",
        "收货人": "ConsigneeName",
        "理论重量": "Weight",
        "称重重量": "WeightQty",
        "总金额": "SumAmount",
        "地址": "ConsigneeAdress",
        "出库人": "DeliverySendUser",
        "扫描人": "ScanUser",
        "称重人": "WeightUser",
        "打包人": "PackageUser",
        "平台发货日期": "PlatDeliveryDate",
        "物流状态": "TranStatusName",
        "物流成本": "ExpressCost",
        "打印批次号": "BatchCode",
        "包裹备注": "PackageMemo",
        "平台": "Platform",
        "加密电话": "EncriptReceiverMobile",
        "加密手机": "EncriptReceiverPhone",
        "加密收货人": "EncriptReceiverName",
        "拣货批次号": "WaveCode",
        "店铺ID": "ShopId",
        "快递ID": "ExpressId",
        "仓库ID": "WarehouseId",
        "模糊搜索": "Fuzzy",
        "审核时间": "ApprovedDate",
        "商家编码": "SkuCode",
        "卖家备注": "SellerMemo",
        "包裹状态": "TranStatus",
        # 特指物流单
        "打印次数": "ExpressPrintQty",
    }
    params = {
        'ModelTypeName': 'ErpWeb.Domain.ViewModels.Deliverys.DeliveryOrderQueryVmv',
    }
    for k, v in query_params_dict.items():
        params[info_map[k]] = v
    url = "http://gw.erp12345.com/api/Deliverys/DeliveryOrderQuery/QueryPage?"
    for k, v in params.items():
        url += f"{k}={v}&"
    headers = {
        'Cookie': base.cookies
    }
    response = requests.get(url, headers=headers)
    result = dict(response.json())
    return_info = []
    for i in result["data"]["Items"]:
        info = {}
        for j in return_info_list:
            info[j] = i[info_map[j]]
        return_info.append(info)
    return return_info





