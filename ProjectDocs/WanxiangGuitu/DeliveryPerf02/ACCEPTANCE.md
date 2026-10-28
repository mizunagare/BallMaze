# PERF-02 逐项验收

本表PASS是受限验证交付项，不是性能达标。九个稳态窗口与五次能力/诊断进程均实际完成，历史失败不改写。详见REPORT及原始证据。

|ID|项目|结果|证据与限制|
|---|---|---|---|
|P2-01|PERF01固定SHA复审归档|PASS|Reviews原文及限定接受；审核方未独立Windows重跑|
|P2-02|冻结输入/保护用户文件|PASS|ReadOnlyAudit+source-protection，1152项未变；用户覆盖层只发哈希|
|P2-03|3份新Library非开发构建与类型边界|PASS|A/B0错116警告，C0错118警告；PE原件及类型重审，无Editor引用|
|P2-04|ABC/BCA/CAB各3独立窗口|PASS|matrix-results、boundary、实际OS退出回执；60秒/10秒预热，9窗口完整|
|P2-05|已知分配/零动作/线程/帧边界探针|PASS|3探针+2诊断共5进程，原始payload、worker完成、same/next/end帧数据|
|P2-06|可靠逐帧/逐线程GC Alloc字节|NOT_RUN|已知分配仍0，目标Recorder无效；UNAVAILABLE，不用内存增长替代|
|P2-07|FTM有效CPU/渲染/GPU子集|PASS|B/C原始timestamp和计时，缺失/非正/重复保留，不混指标|
|P2-08|GPU完整逐帧覆盖|UNRESOLVED|FTM及Recorder均有缺口，不能把子集当完整基准|
|P2-09|GPU Frame Time Recorder正值能力|PASS|TimeNanoseconds正值检查点子集；重复同帧/可能共享后端限制明确|
|P2-10|FrameTime.GPU可靠正值|NOT_RUN|句柄可用却未获可靠正值；0不等于无GPU工作|
|P2-11|C实际LUID及DXGI应用段用量/预算|PASS|原生D3D11设备LUID匹配，node0 HRESULT0，容量/预算/用量分列；不是整卡剩余显存|
|P2-12|PDH/WMI当前进程能力|PASS|两次定向诊断有实际LUID有效数据，所有错误/无效样本保留；不替换原C窗口时间序列|
|P2-13|A逐帧指标、A/B唯一LUID、整卡剩余显存|NOT_RUN|遵守A不添加逐帧采样器；名称/版本不是唯一实例证明，应用预算余量不是设备剩余容量|
|P2-14|完整工具/sidecar自身CPU因果分解|NOT_RUN|Player累计CPU和B/C部分自耗时有效，sidecar自身CPU未测量，不作因果差值|
|P2-15|最多3类警告源码语义复核|PASS|89关联诊断，91仍全部OPEN；不迁移API、不重存场景|
|P2-16|原始数据、失败、数学与无损重汇总|PASS|原始日志/帧、18892离群索引、最终7项分析测试、manifest及还原校验|
|P2-17|性能预算/原生U16/独立人工|NOT_RUN|无硬件预算/安全独立原生与人员，不拿截图/虚拟输入替代|
|P2-18|历史引擎根因关闭|UNRESOLVED|UNKNOWN/青色帧/Search/JobTempAlloc保持开放，无试探性生命周期修改|

18项：**11 PASS /0 FAIL /5 NOT_RUN /2 UNRESOLVED**。这里的0 FAIL不抹去工具准备/诊断失败，也不把14个进程成功等同于GC、GPU或发行验收全部通过。原始运行、指标和本表分别统计，交付后等待独立复审。
