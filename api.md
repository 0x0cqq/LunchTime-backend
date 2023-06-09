# API文档

- POST 请求参数以表单形式从前端发送
- GET 请求参数以Params形式从前端发送

## 一、登录相关

### 获取邮箱验证码
- POST: /api/verify_email
- Param:

```json
{
    "email":
}
```

- Response:
```json
{
    "status":  , //True or False
    "message": , //Error message
}
```

### 用户注册

- POST: /api/register
- Param:

```json
{
    "name":,
    "password":,
    "email":,
    "verfication":,
}
```

- Response
```json
{
    "status": ,  
    "message": , 
}
```

### 用户登录
- POST: /api/login
- Param:

```json
{
    "name":,
    "password":,
}
```

- Response
```json
{
    "status": ,  //True or False
    "message": , //Error message
}
```

## 二、帖子相关

### 按时间线/热度/评论/关注获取帖子
- GET: api/posts
- Param:
```json
{
    "user_name":,
    "type": , // 0->time 1->popularity 2->comment
    "target_user_name": , // empty means all users
    "filter": , // 0->no filter 1->following
}
```
- Response
```json
{
    "status": ,
    "message": ,
    "posts":[{
        "post_id": ,
        "user_name": ,
        "user_image": ,
        "create_time":,
        "tag":,
        "title":,
        "content":,
        "picture":[] , //其中为图片的url链接
		"is_video": ,
		"video": [], //其中为视频的url链接
        "location":,
        "love_count":,
        "comment_count":,
        "save_count":,
        "is_loved":,  //True or False
        "is_saved":,
        },
    ]
}
```
### 获取用户收藏的帖子
- GET: api/posts_saved
- Param:
```json
{
    "user_name":,
    "target_user_name": , 
}
```
- Response
```json
{
    "status": ,
    "message": ,
    "posts":[{
        "post_id": ,
        "user_name": ,
        "user_image": ,
        "create_time":,
        "tag":,
        "title":,
        "content":,
        "picture":[] , //其中为图片的url链接
		"is_video": ,
		"video": [], //其中为视频的url链接
        "location":,
        "love_count":,
        "comment_count":,
        "save_count":,
        "is_loved":,  //True or False
        "is_saved":,
        },
    ]
}
```


### 搜索帖子
- GET: api/search_post
- Param:
```json
{
    "user_name":,
    "keyword":,
    "field":, //'all', 'title', 'tag', 'content', 'username'
    "type":, //0->time 1->love 3-> comment
}
```
- Response
```json
{
    "status": ,
    "message": ,
    "posts":[{
        "post_id": ,
        "user_name": ,
        "user_image": ,
        "create_time":,
        "tag":,
        "title":,
        "content":,
        "picture":[] , //其中为图片的url链接
		"is_video": ,
		"video": [], //其中为视频的url链接
        "location":,
        "love_count":,
        "comment_count":,
        "save_count":,
        "is_loved":,  //True or False
        "is_saved":,
        },
    ]    
}
```

### 获取某个帖子的详细信息
- GET: api/post_detail
- Param:
```json
{
    "user_name":,
    "post_id": ,
}
```
- Response:
```json
{   
    "status":,
    "message":,
    "post":{
        "post_id": ,
        "user_name": ,
        "user_image": ,
        "create_time":,
        "tag":,
        "title":,
        "content":,
        "picture":[] , //其中为图片的url链接
		"is_video": ,
		"video": [], //其中为视频的url链接
        "location":,
        "love_count":,
        "comment_count":,
        "save_count":,
        "is_loved":,
        "is_saved":,
    }, 
    "comments":[{
        "user_name": ,
        "user_image": ,
        "content": ,
        "create_time":,},
    ]
}
```

### 发帖
- POST: api/post
- Param:
```json
{
    "user_name": ,
    "tag": , 
    "title": ,
    "content": ,
    "picture": [] ,
	"video": [],
    "location": ,
}
```
- Response:
```json
{
    "status":,
    "message":,
    "post_id":,
}
```

### 对帖子点赞/取消点赞
- POST: api/love_post
- Param:
```json
{
    "user_name":,
    "post_id":,
}
```
- Response:
```json
{
    "status": ,
    "message":,
    "result":, //result=1, 点赞成功; result=0, 取消点赞成功
}
```

### 对帖子评论
- POST: api/comment_post
- Param:
```json
{
    "user_name":,
    "post_id":,
    "comment":,
}
```
- Response:
```json
{
    "status": ,
    "message":,
}
```

### 对帖子收藏/取消收藏
- POST: api/save_post
- Param:
```json
{
    "user_name":,
    "post_id":,
}
```
- Response:
```json
{
    "status": ,
    "message":,
    "result":,
}
```

## 三、通知相关
### 获取评论/点赞/聊天通知列表
- GET: api/notice
- Param:
```json
{
    "user_name":,
    "type":, // 1->评论 2->点赞 3->聊天
}
```
- Response
```json
{
    "notice_list":[
        {
            "user_name":,
            "user_image":, //用户头像，目前还不支持
            "create_time":,
            "content":, //评论的内容
            "post_id":, //帖子id
            "picture":, //帖子的第一张图片
            "is_read":,
        },
    ],
    "status":,
    "message":,
}
```

### 已读评论/点赞通知
- POST: api/read_notice
- Param:
```json
{
    "user_name":,           // the user who send this message
    "target_user_name":,
    "type":,                // "comment", "love",
    "create_time":,         // if type == "comment"
    "post_id":,
}
```
- Response:
```json
{
    "status":,
    "message":,
}
```

## 四、用户相关
### 获取用户信息
- GET: api/user_info
- Param:
```json
{
    "user_name":,
    "target_user_name":,
}
```
- Response:
```json
{   
    "user_info":{
        "user_name":,
        "user_image":,
        "user_description":,
        "follow_count":,
        "fans_count":,
        "is_following":,
        "is_hating":,
    },
    "status":,
    "message":,
}
```

### 修改用户名称
- POST: api/modify_user_name
- Param:
```json
{
    "original_user_name": ,
    "new_user_name": ,
}
```

- Response
```json
{
    "status":,
    "message":,
}
```

### 修改用户简介
- POST: api/modify_user_description
- Param:
```json
{
    "user_name": ,
    "new_user_description":,
}
```

- Response
```json
{
    "status":,
    "message":,
}
```

### 修改用户头像
- POST: api/modify_user_image
- Param:
```json
{
    "user_name":,
    "image":,
}
```
- Response:
```json
{
    "status":,
    "message":,
}
```

### 修改用户密码
- POST: api/modify_user_password
- Param:
```json
{
    "user_name":,
    "old_password":,
    "new_password":,
}
```
- Response:
```json
{
    "status":,
    "message":,
}
```

### 关注/取消关注
- POST: api/attention
- Param:
```json
{
    "user_name":,
    "target_user_name":
}
```
- Response
```json
{
    "result":, //result=1, 关注成功; result=0, 取消关注成功
    "status":,
    "message":,
}
```

### 拉黑/取消拉黑
- POST: api/hate
- Param:
```json
{
    "user_name":,
    "target_user_name":
}
```
- Response
```json
{
    "result":,
    "status":,
    "message":,
}
```

### 获取关注/粉丝/黑名单列表
- GET: api/attention_list
- Param:
```json
{
    "user_name":,
    "type":, //0->关注列表 1->粉丝列表 2->黑名单列表
}
```
- Response
```json
{
    "user_list":[
        {
            "user_name":,
            "user_image":,
            "user_description":,
            "follow_cnt":,
            "fans_cnt":,
            "isFollowing":,
            "isHating":,
        },
    ],
    "status":,
    "message":,
}
```

## 五、聊天相关

### 聊天列表 (/api/chats)

#### GET

* Params:
    * `user_name`: 用户名
* Response:

```json
{
    "status": true | false,
    "message": "错误信息" | null,
    "chat_list": [{
        "user_name" : "用户名",
        "user_avatar": "头像 URL" ,
        "content": "最近的消息",
        "timestamp": "时间戳",
        "unread_num": "未读消息数", 
    }] | null
}
```

#### POST

* Parmas:
    * `user_name`: "查看消息的用户"
    * `target_user_name`: "该用户的聊天对象"
* Response:

```json
{
    "status": true | false,
    "message": "错误信息" | null,
}
```

    
## 六、实时聊天

通过 websocket 来实现消息的实时收发

### Websocket URL

`ws://BASE_URL/ws/chat`

URL params:

* `sender_name` 发送者的用户名
* `receiver_name` 接收者的用户名

### 消息格式

> 采用 JSON 序列化成为字符形式发送

发送信息（客户端 -> 服务器）：

* `user_name: string`: 发送者的用户名
* `content: string `: 消息的内容

接收消息（服务器 -> 客户端）:

* `user_name: string`: 发送者的用户名
* `user_avatar: string`: 发送者的头像
* `content: string`: 消息内容
* `timestamp: int`: 消息发送的时间戳

## 七、实时通知

在后台开启长 Websocket 连接来获取后端的通知信息的及时更新

### URL

`ws://BASE_URL/ws/notice`

URL params:

* `user_name: string`: 需要请求的用户名
