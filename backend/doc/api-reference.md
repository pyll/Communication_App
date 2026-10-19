# Communication_App 后端接口说明

> 基于仓库 `pyll/Communication_App/backend` 的 `urls.py` 路由配置及部分 `views.py` 源码整理。
> 说明：`talk` 和 `friend` 模块的 `urls.py` 未能成功获取，相关接口信息可能不完整；`event` 和 `square` 模块的 `views.py` 未能成功获取，这些接口的详细参数和响应格式是基于路由配置推断的。

---

## 一、总览

后端采用 **Django + Django REST Framework** 的 `APIView` 风格实现。所有业务模块的路由均挂载在根路由之下：

| 模块 | 根路径 | 状态 |
|---|---|---|
| 用户 | `/user/` | 完整 |
| 动态 | `/event/` | 路由完整，视图细节部分缺失 |
| 广场 | `/square/` | 路由完整，视图细节部分缺失 |
| 资讯 | `/news/` | 完整 |
| 聊天 | `/talk/` | 路由文件未获取 |
| 好友 | `/friend/` | 路由文件未获取（但相关接口被 user 模块直接引用） |

**通用认证方式**：除 `user/register`、`user/login`、`user/test` 外，其余接口普遍需要携带 `token` **作为查询参数**（`?token=xxx`），后端通过 `UserToken.objects.get(token__exact=token).user` 解析当前用户。

**通用响应结构**：标准接口返回如下 JSON 格式：

```json
{
  "code": 200,
  "detail": "success",
  "info": []
}
```

`code` 为 `200` 表示成功，其他值表示异常；`detail` 存放提示信息；`info` 存放业务数据（列表或对象）。

---

## 二、用户模块（`/user/`）

### 1. 注册

| 项目 | 内容 |
|---|---|
| **路径** | `POST /user/register` |
| **认证** | 无需 token |
| **功能** | 用户注册，同时上传头像至七牛云并保存用户信息 |
| **请求参数**（JSON body） | `username`、`password`、`re_password`、`school`、`gender`、`avatar`（图片文件路径） |
| **成功响应** | `code: 200`，`detail: "success"` |
| **失败情况** | 用户名已存在（`code: 201`，`detail.username: "该用户名已被注册"`）；两次密码不一致（`code: 201`，`detail.password: "两次密码不一样"`） |

该视图继承自 `APIView`，设置了 `authentication_classes = []`，因此无需 token 即可调用。

### 2. 登录

| 项目 | 内容 |
|---|---|
| **路径** | `POST /user/login` |
| **认证** | 无需 token |
| **功能** | 校验用户名和密码，成功后生成 token 并返回用户信息 |
| **请求参数**（JSON body） | `username`、`password` |
| **成功响应** | `code: 200`，`info` 包含 `username`、`gender`、`school`、`token`、`avatar`、`birth`、`major` |
| **失败情况** | 用户不存在（`detail: "用户不存在"`）；密码不正确（`detail: "密码不正确"`） |

登录成功后，token 会通过 `UserToken.objects.update_or_create` 写入或更新。

### 3. 更新用户信息

| 项目 | 内容 |
|---|---|
| **路径** | `POST /user/update` |
| **认证** | 需要 token（查询参数） |
| **功能** | 更新当前用户的 `school`、`gender`、`username` |
| **请求参数**（查询参数） | `token` |
| **请求参数**（JSON body） | `school`、`gender`、`username` |
| **响应** | `code: 200`，`detail: "success"` |

### 4. 获取好友列表

| 项目 | 内容 |
|---|---|
| **路径** | `POST /user/getFriendList` |
| **认证** | 需要 token |
| **功能** | 返回当前用户的所有有效好友（`is_deleted != 1`） |
| **请求参数** | 查询参数 `token` |
| **响应** | `code: 200`，`info` 为好友对象列表（由 `FriendSerializer` 序列化） |

该接口直接使用了 `friend` 应用的 `Friend` 模型，说明好友关系数据由 user 模块直接操作。

### 5. 添加好友

| 项目 | 内容 |
|---|---|
| **路径** | `POST /user/addFriend` |
| **认证** | 需要 token |
| **功能** | 向指定用户发起好友请求，先写入 `FriendLog` 表 |
| **请求参数**（查询参数） | `token` |
| **请求参数**（JSON body） | `username`（目标用户名） |
| **响应** | `code: 200`，`detail: "success"` |

若此前已有请求记录，则重置 `is_agreed = 0`，重新发起请求。

### 6. 回应好友请求

| 项目 | 内容 |
|---|---|
| **路径** | `POST /user/responseAddFriend` |
| **认证** | 需要 token |
| **功能** | 同意好友请求，将 `FriendLog` 中的请求转为正式的 `Friend` 关系 |
| **请求参数**（查询参数） | `token` |
| **请求参数**（JSON body） | `username`（发起请求的用户名） |
| **响应** | `code: 200`，`detail: "success"` |

若好友关系已存在且未被删除，返回 `detail: "已建立此好友关系"`；若曾删除，则将 `is_deleted` 重置为 `0` 恢复关系。

### 7. 删除好友

| 项目 | 内容 |
|---|---|
| **路径** | `POST /user/deleteFriend` |
| **认证** | 需要 token |
| **功能** | 删除好友关系（软删除，将 `is_deleted` 置为 `1`） |
| **请求参数** | 查询参数 `token`；JSON body 中的 `username` |

### 8. 获取用户信息

| 项目 | 内容 |
|---|---|
| **路径** | `POST /user/getUserInfo` |
| **认证** | 需要 token |
| **功能** | 根据用户名获取指定用户的详细信息 |

### 9. 问卷

| 项目 | 内容 |
|---|---|
| **路径** | `POST /user/survey` |
| **认证** | 需要 token |
| **功能** | 提交或获取用户问卷数据 |

### 10. 测试接口

| 项目 | 内容 |
|---|---|
| **路径** | `POST /user/test` |
| **认证** | 无需 token |
| **功能** | 测试接口，回显请求数据 |
| **响应** | `{"detail": "我收到啦!!!!!!"}` |

> **注意**：`user/urls.py` 中 `verifyCode`（获取验证码）、`forgetPassword`（忘记密码）、`studentConfirm`（学生认证）三个路由在源码中被注释掉了，**未启用**。

---

## 三、动态模块（`/event/`）

### 1. 获取全部动态

| 项目 | 内容 |
|---|---|
| **路径** | `POST /event/getAllEvent` |
| **认证** | 需要 token |
| **功能** | 获取全部动态信息 |

### 2. 按分类获取动态

| 路径 | 功能 |
|---|---|
| `POST /event/getFoodEvent` | 获取“食”分类的动态 |
| `POST /event/getSportEvent` | 获取“行”（运动）分类的动态 |
| `POST /event/getStudyEvent` | 获取“学”分类的动态 |
| `POST /event/getPlayEvent` | 获取“乐”分类的动态 |

### 3. 发布动态

| 项目 | 内容 |
|---|---|
| **路径** | `POST /event/addEvent` |
| **认证** | 需要 token |
| **功能** | 用户发布一条新动态 |

### 4. 获取我的动态

| 项目 | 内容 |
|---|---|
| **路径** | `POST /event/getMyEvent` |
| **认证** | 需要 token |
| **功能** | 获取当前用户发布的动态列表 |

### 5. 删除我的动态

| 项目 | 内容 |
|---|---|
| **路径** | `POST /event/delMyEvent` |
| **认证** | 需要 token |
| **功能** | 删除当前用户发布的指定动态 |

以上动态模块的路由定义来自 `event/urls.py`，所有接口均使用 `APIView` 子类实现。由于 `event/views.py` 未能成功获取，详细的请求参数和响应字段未能在本文档中列出。

---

## 四、广场模块（`/square/`）

| 路径 | 方法 | 功能 |
|---|---|---|
| `POST /square/getAllSquare` | POST | 获取全部广场信息 |
| `POST /square/addSquare` | POST | 增加广场信息 |

广场模块的路由定义在 `square/urls.py` 中，仅包含以上两个接口。由于 `square/views.py` 未能成功获取，具体的请求参数和响应格式无法进一步说明。

---

## 五、资讯模块（`/news/`）

资讯模块的接口统一以 `POST` 方式调用，根据不同的兴趣类别返回对应的资讯列表。大多数接口的核心逻辑是 `News.objects.filter(type__exact=<数字>)` 后序列化返回。

| 路径 | 功能 | 对应 `type` 值（如有） |
|---|---|---|
| `POST /news/getLike` | 根据当前用户 `like` 字段（逗号分隔的兴趣 ID）返回个性化推荐资讯 | 动态匹配 |
| `POST /news/getFruit` | 获取“水果”类资讯 | `5` |
| `POST /news/getHotpot` | 获取“火锅”类资讯 | `6` |
| `POST /news/getMilktea` | 获取“奶茶”类资讯 | `7` |
| `POST /news/getMeal` | 获取“三餐”类资讯 | `8` |
| `POST /news/getBall` | 获取“球类”类资讯 | `9` |
| `POST /news/getRun` | 获取“跑步”类资讯 | `10` |
| `POST /news/getSwim` | 获取“游泳”类资讯 | `11` |
| `POST /news/getYoga` | 获取“瑜伽”类资讯 | `12` |
| `POST /news/getEnglish` | 获取“英语”类资讯 | — |
| `POST /news/getHandwriting` | 获取“书法”类资讯 | — |
| `POST /news/getDraw` | 获取“绘画”类资讯 | — |
| `POST /news/getRead` | 获取“读书”类资讯 | — |
| `POST /news/getSing` | 获取“唱K”类资讯 | — |
| `POST /news/getFilm` | 获取“电影”类资讯 | — |
| `POST /news/getChess` | 获取“下棋”类资讯 | — |
| `POST /news/getHomeparty` | 获取“轰趴”类资讯 | — |

`getLike` 接口需要 token，会从 `UserToken` 中解析当前用户，读取 `user.like` 字段并按兴趣类型逐类查询资讯；其余分类接口通常不需要 token，直接按 `type` 过滤返回。

---

## 六、聊天模块（`/talk/`）与好友模块（`/friend/`）

### 聊天模块（`/talk/`）

根路由 `backend03/urls.py` 中已注册 `url('talk/', include('talk.urls'))`，说明聊天模块存在且已挂载。但 `talk/urls.py` 在本次抓取中未能成功获取，因此**具体接口路径和功能暂无法列出**。

### 好友模块（`/friend/`）

根路由中**没有** `friend` 的 `include`，但 `friend` 应用被 `user` 模块直接引用：`user/views.py` 中 `from friend.models import Friend, FriendLog`，并且 `getFriendList`、`addFriend`、`responseAddFriend`、`deleteFriend` 等好友相关接口全部放在 `/user/` 路径下。因此，好友功能在路由层面是通过 **`/user/` 模块对外暴露的**，`friend` 应用只提供了模型层支持。

---

## 七、补充说明

1. **请求方法**：绝大多数接口在视图层实现为 `def post(self, request)`，因此即使路由路径看起来像资源路径，实际调用时也应使用 **POST** 方法。
2. **Token 传递**：token 普遍通过 **URL 查询参数** 传递（如 `/user/getFriendList?token=xxxx`），而不是 `Authorization` 请求头。
3. **头像存储**：用户头像通过七牛云 Python SDK 上传至 `privatebucket` 空间，返回的是带有效期的私有下载链接。
4. **未启用接口**：`verifyCode`、`forgetPassword`、`studentConfirm` 在 `user/urls.py` 中被注释，当前版本不可用。
5. **缺失文件说明**：`talk/urls.py`、`friend/urls.py`、`event/views.py`、`square/views.py` 在本次分析中未能成功获取，如果你需要这几个模块的完整接口细节，建议直接在仓库中打开对应文件查看。