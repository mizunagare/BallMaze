# 失败与未运行记录

1. 本次首次prepare退出1：`Tree membership differs`。初实现将完整合成集合与旧发布目录子集比较，子集未包含bak和entry.lock，但原始发布的storage-after.json已经记录这两项。原始stderr/stdout见Evidence/Preparation/initial-failure.*。重复一次仅为捕获原始输出，没有创建包或操作玩家档。
2. 最小工具修复：使用该已发布运行时清单规范化Windows路径、核对完整4文件SHA，不忽略多余文件，不修改历史原始证据。随后prepare成功、14项工具自测通过。
3. PowerShell启动器仅静态解析，尚未实际人工执行；其窗口启动、退出与恢复全过程NOT_RUN，不以语法通过代替。
4. 历史C15 FAIL和30秒超时根因UNRESOLVED原样保留。R1新WM_CLOSE样本不是旧失败根因结论。D3D12、青色帧、Search、JobTempAlloc、旧Editor阻塞不在本次重复运行。
