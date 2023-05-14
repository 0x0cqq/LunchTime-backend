# API文档
- 参数以表单形式从前端发送

## 一、用户相关

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

### 按时间线获取帖子
- GET: api/get_posts_by_time
- Param:
```json
{
    "user_name":
}
```
- Response
```json
{
    "status": ,
    "message": ,
    "posts":
        [{"post_id": ,
         "user_name": ,
         "create_time":,
         "tag":,
         "title":,
         "content":,
         "picture":[] , //其中为图片的url链接
         "location":,
         "love_count":,
         "comment_count":,
         "save_count":,},
        ]
}
```

### 按热度获取帖子
- GET: api/get_posts_by_popularity
- Param:
```json
{
    "user_name":
}
```
- Response
```json
{
    "status": ,
    "message": ,
    "posts":
        [{"post_id": ,
         "user_name": ,
         "create_time":,
         "tag":,
         "title":,
         "content":,
         "picture":[] , //其中为图片的url链接
         "location":,
         "love_count":,
         "comment_count":,
         "save_count":,},
        ]
}
```

### 按关注获取帖子
- GET: api/get_posts_by_attention
- Param:
```json
{
    "user_name":
}
```
- Response
```json
{
    "status": ,
    "message": ,
    "posts":
        [{"post_id": ,
         "user_name": ,
         "create_time":,
         "tag":,
         "title":,
         "content":,
         "picture":[] , //其中为图片的url链接
         "location":,
         "love_count":,
         "comment_count":,
         "save_count":,},
        ]
}
```

### 获取某个帖子的详细信息
- GET: api/get_post_detail
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
    "post_id": ,
    "user_name": ,
    "create_time":,
    "tag":,
    "title":,
    "content":,
    "picture":[] , //其中为图片的url链接
    "location":,
    "love_count":,
    "comment_count":,
    "save_count":,
    "comment":[{
        "user_name": ,
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