# JobTempAlloc 原生退出调查

## 真实对照

所有构建使用Unity6000.6.5f1，`-diag-job-temp-memory-leak-validation`；NativeLeakDetection=EnabledWithStackTrace。BuildEmpty2仅相机空Scene；BuildTerrain2仅四块保存地形；BuildAudit2/3包含独立运行驱动和完整自有场景。三组修正后 Profile 显式场景列表均经 BuildProfile.scenes 断言。项目仍安装同一个MapMagic包，不能称“卸载插件后也复现”。

| 对照 | 活动MapMagicObject（构建前） | Build结果 | JobTempAlloc退出诊断 |
|---|---:|---|---|
| BuildEmpty2 | 0 | 成功，0错0警告 | 15条分配记录，均含ShaderCompilation::CompileVariantJob |
| BuildTerrain2 | 0 | 成功，0错0警告 | 同样15条 |
| BuildAudit2 | 0 | 成功，0错13警告 | 同样15条 |
| BuildAudit3 | 0 | 成功，0错13警告 | 同样15条 |
| EditorPlay1（不构建） | 运行时生成后正常销毁 | exit0 | 此次退出未见该警告 |

BuildReport 的warning数量不包含所有原生退出日志，不能以0 warning抹去 JobTempAlloc。

## 栈与数量

空场景正确对照的五种分配：504、582、152、64、64字节（共1366B），同一地址在age1、2、3重复报告，共15条；不是15个不同泄漏。记录为frameIndex=0、lifetime=15、state=OK。具体路径分别经过 CompileVariantJob、LoadVariantFromData、LoadSerializedSubProgramFromCache、LoadParametersFromData、ReadParametersSplit、ReadResourcesSplit 和Unity job worker。

[全部提取栈及原日志行号](Evidence/job-stacks.json)。日志中的原生堆十六进制载荷未公开，原始文件完整保留在本机，原SHA在manifest；每个警告、分配头及调用栈均保留。不得从内存转储字节猜测资产所有权。

## 归因边界

已定位：本轮三种构建的可见残余分配栈属于原生 Shader Variant 编译/缓存加载路径；空Scene不需要活动Terrain、NavMesh、MapMagic生成任务或运行时自有NativeArray即可触发。自有TempJob控制每轮执行Schedule→Complete→Dispose，独立断言通过。

尚未定位：为什么这些原生分配在Editor构建退出阶段仍未释放，以及是否只为退出顺序/编译缓存。没有Unity引擎源码级释放证据，不能宣称已修复或断言供应商完全无关。JobTempAlloc总体继续UNRESOLVED。

未做：修改引擎/供应商源码、关闭检查或改变Job生命周期来隐藏警告。上轮与本轮首次错误场景构建的日志均保留，但错误场景对照不计作正确实验控制。后续若需引擎缺陷报告，应携带Empty2最小栈和版本/图形API资料；本轮没有向外部发送工程或用户数据。
