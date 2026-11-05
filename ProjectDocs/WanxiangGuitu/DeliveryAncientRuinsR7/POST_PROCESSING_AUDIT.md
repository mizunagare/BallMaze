# 后处理开关实测

两份纯发行包按冻结清单逐文件校验，各自的无探针副本实际启动到标题并正常退出。场景取证使用两套发行包的隔离副本，只追加探针程序集和两个加载注册。原包、产品程序集、渲染资源、Prefab、Scene 和 GraphicsSettings 均未改动。[完整性核查](Evidence/Audit/protection.json) · [纯包启动证据](Evidence/INDEX.md)

各机位先保留原生相机，再于进程内临时添加 URP 相机数据和同一全局 ColorAdjustments Volume。曝光固定 +2 EV，依次关闭、开启、再关闭，其他控制条件相同。关回后移除临时对象。原生和关闭时的着色器阶段集合相同，开启后两包均新增两个实际提交的组合，再关闭后恢复原集合。[Unity Color Adjustments](https://docs.unity3d.com/6000.6/Documentation/Manual/urp/Post-Processing-Color-Adjustments.html) · [开关与画面原始数据](Evidence/Audit/gpu-and-post.json.gz)

| 机位 | 开 vs 关 RGB MAE，A/B 各两轮范围 | 关 vs 再关 MAE 上限（约） |
| --- | ---: | ---: |
| 标题 | 38.654–38.655 | 0.001 |
| 营地 | 48.968–48.969 | 0.017 |
| 遗迹入口 | 53.649–53.652 | 0.025 |
| 石柱广场 | 53.513–53.514 | 0.017 |
| 机关走廊 | 50.484–50.485 | 0.031 |
| 地下祭坛 | 47.292–47.293 | 0.057 |
| Boss 大厅 | 52.209–52.246 | 0.056 |

RGB MAE 单位为 0–255 的通道值。开态 A/B 的最大全帧 MAE 约 0.0892，远小于开关自身的视觉差异。截图和实际绘制都支持两包的曝光控制响应一致。包内日志仍记录 Gaussian/Bokeh Depth of Field 和 Panini Projection shader 不支持或被裁剪。本轮开关 PASS 限于测试过的曝光流程，其他效果未验收。[A/B 开关对照图](Evidence/Audit/post-contact-sheet.png) · [逐状态跨包像素数据](Evidence/Audit/post-cross-package.json)
