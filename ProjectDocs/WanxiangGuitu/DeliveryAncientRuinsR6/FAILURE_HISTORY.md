# 失败历史

- R5 的首轮标题差异及六个场内机位严格像素失败均保留。R6 标题在扩大样本后也出现严格像素差异，另记本轮 FAIL。 [R5 失败历史](https://github.com/mizunagare/BallMaze/blob/f21f807fb39f38653d7d3a5d9a3e3371936fedbe/ProjectDocs/WanxiangGuitu/DeliveryAncientRuinsR5/FAILURE_HISTORY.md) · [R6 配对数据](Evidence/ComparisonFinal/metrics.json.gz)
- 首版阴影和后处理诊断依赖额外相机组件，实际没有该组件，进程虽然正常退出但无有效开关截图。保留首轮诊断，再用活动 Light 的真实阴影开关复测。后处理仍没有活动路径供开关对照。[首版诊断样本](Evidence/Frames-A-camp-smoke/) · [独立复测](Evidence/isolated.jsonl.gz)
- 区域解析首次遇到带换行的 UI 文本，修正了解析器，再用原始截图和区域清单重算。随后收紧阴影控制资格，排除了标题零光源样本。[首轮异常](Evidence/comparison-first-failure.log.gz) · [最后重算](Evidence/comparison-final.log.gz)
- 发行 GraphicsSettings 通用类型树解析未读完 864 字节，保留失败，后续只对有独立核验的 PSO 区段解码。[解码报告](Evidence/graphics-payload.json)
- 首次原生字符串读回用固定长度，多读到短字符串结尾外的填充值。根据短字符串长度标记修正，保留两包旧读回和新读回。没有在任何样本中改写内存中的 GraphicsSettings。[首次 A](Evidence/Frames-A-camp-native/native-readback.jsonl.gz) · [复测 A](Evidence/Frames-A-camp-native2/native-readback.jsonl.gz)
