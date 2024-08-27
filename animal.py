import requests
import json
import base64

flora_api = {}  # 顾名思义,FloraBot的API,载入(若插件已设为禁用则不载入)后会赋值上


def occupying_function(*values):  # 该函数仅用于占位,并没有任何意义
    pass


send_msg = occupying_function


def init():  # 插件初始化函数,在载入(若插件已设为禁用则不载入)或启用插件时会调用一次,API可能没有那么快更新,可等待,无传入参数
    global send_msg
    #print(flora_api)
    send_msg = flora_api.get("SendMsg")
    print("FloraBot插件模板 加载成功")


def api_update_event():  # 在API更新时会调用一次(若插件已设为禁用则不调用),可及时获得最新的API内容,无传入参数
    #print(flora_api)
    return


def event(data: dict):  # 事件函数,FloraBot每收到一个事件都会调用这个函数(若插件已设为禁用则不调用),传入原消息JSON参数
    print(data)
    uid = data.get("user_id")  # 事件对象QQ号
    gid = data.get("group_id")  # 事件对象群号
    mid = data.get("message_id")  # 消息ID
    msg = data.get("raw_message")  # 消息内容
    try:
        global ws_client
        global ws_server
        send_address = data.get("SendAddress")
        ws_client = send_address.get("WebSocketClient")
        ws_server = send_address.get("WebSocketServer")
    except:
        ws_server=None
        ws_client=None
        pass
    if msg is not None:
        msg = msg.replace("&#91;", "[").replace("&#93;", "]").replace("&amp;", "&").replace("&#44;", ",")  # 消息需要将URL编码替换到正确内容
        #print(uid, gid, mid, msg)
        if msg == "#随机猫猫":
            req_data=requests.get("https://api.thecatapi.com/v1/images/search")
            req_data=req_data.json()
            #print(req_data)
            send_compatible(msg=f"[CQ:at,qq={uid}]\n[CQ:image,file={req_data[0].get('url')}]",uid=uid,gid=gid)
        if msg == "#随机狗狗":
            req_data=requests.get("https://api.thedogapi.com/v1/images/search")
            req_data=req_data.json()
            #print(req_data)
            send_compatible(msg=f"[CQ:at,qq={uid}]\n[CQ:image,file={req_data[0].get('url')}]",uid=uid,gid=gid)
        if msg == "#随机狐狐":
            req_data=req_data.json()
            #print(req_data)
            send_compatible(msg=f"[CQ:at,qq={uid}]\n[CQ:image,file={req_data['image']}]\n{req_data['link']}",uid=uid,gid=gid)
        if msg == "#随机鸭鸭":
            req_data=requests.get("https://random-d.uk/api/random")
            req_data=req_data.json()
            #print(req_data)
            send_compatible(msg=f"[CQ:at,qq={uid}]\n[CQ:image,file={req_data['url']}]",uid=uid,gid=gid)


def send_compatible(msg:str,gid:str|int,uid: str|int,mid:str|int =None):  #兼容性函数,用于兼容旧版本API(请直接调用本函数)
    if flora_api.get("FloraVersion") == 'v1.01': #旧版本API
        send_msg(msg=msg,gid=gid,uid=uid,mid=mid)
    else:
        send_type=flora_api.get("ConnectionType")
        send_address=flora_api.get("FrameworkAddress")
        send_msg(msg=msg,gid=gid,uid=uid,mid=mid,send_type=send_type,ws_client=ws_client,ws_server=ws_server)