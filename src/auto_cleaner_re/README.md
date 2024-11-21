# MCDR AutoCleanerRe
复活的扫地大妈

## 用法
开箱即用。

## 命令
```
  !!acr: 显示帮助信息
  !!acr status: 显示扫地机状态信息
  !!acr enable: 启动扫地机
  !!acr disable: 关闭扫地机
  !!acr ignore_player_items <true/false>: 启用/关闭 清扫时忽略因玩家死亡而掉落的物品
  !!acr ignore_distance <ignore_distance>: 设置忽略半径
  !!acr set_interval <interval_sec>: 设置清扫间隔，单位：秒 最低45
```

## 依赖项
无

## 局限性
玩家死亡时掉落的物品与玩家之间并没有联系，无法做到精确关联。本插件的做法是玩家死亡半径内的物品打上标签，使用`/kill @e[type=item,tag=!player_death]`来反匹配不含标签的掉落物

## 配置说明

| 配置项                | 含义                                   | 默认值 | 备注               |
| --------------------- | -------------------------------------- | ------ | ------------------ |
| `enabled`             | 启用/关闭扫地机                        | `true` |                    |
| `permission`          | 使用命令`!!acr`需要的权限              | `2`    | HELPER级别         |
| `ignore_player_items` | 是否在清扫时忽略因玩家死亡而掉落的物品 | `true` |                    |
| `ignore_distance`     | 玩家掉落物品忽略半径                   | `5`    | 欧氏距离           |
| `clean_interval_sec`  | 清扫间隔                               | `300`  | 以秒为单位，最低45 |

## 鸣谢
 - https://github.com/Forgot-Dream/MCDR-AutoCleaner
 - https://github.com/TISUnion/AutoPluginReloader