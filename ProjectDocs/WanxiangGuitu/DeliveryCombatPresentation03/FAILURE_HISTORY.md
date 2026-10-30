
首轮Before的剑几何断言误用了.85 slab；完整源码Contact对剑传PositiveInfinity，只有矛应用width。该4条错误假设失败保留，不归因产品。修订夹具使用真实类型宽度，并检查整个特效寿命（原剑弧末期越出真实方向锥），新增矛主段实际长度检查。数值读取现有SpearReach=3.1，不使用过期3.8假设；产品未改。另有一次只读查找误认为AdventureWeaponVisual独立文件，实际武器挂点代码在AdventureCombat.RefreshWeapon，未据此认定资源不存在。

后续保守审计：新弓释放Swing、新法杖启动Cast与同cue的.035秒限流存在高攻速启动抢占释放声的风险；不改限流或攻速，改为远程启动只保留聚能/原射击片段，现有音色留给真实释放。单独VisualCueBefore/After记录真实动作接受后soundReady，不通过调冷却制造通过。旧版所有构建/运行保留为中间变体，最终版重新验证与构建。

## 执行与历史边界

- 首次只读挂点搜索误认为AdventureWeaponVisual独立文件，另一次旧保存数据名AdventureData.cs不存在；实际挂点在AdventureCombat.RefreshWeapon，实际定义按源码清单定位。查找失败不是产品缺失结论。
- Runtime固定检查点工具的第一次嵌套PowerShell文本替换解析exit1，未写文件；literal Python修订后执行，原错误说明保留ToolFailures/runtime-patch-parser-error.txt。
- Before原201PASS/22FAIL/2UNRESOLVED；其中剑slab假设错误的失败不归因产品。Before2改用剑Infinity/矛slab并检查整个寿命与真实主段长度，205PASS/22FAIL/2UNRESOLVED。After相同输入227PASS/0FAIL/2UNRESOLVED。
- Extended271、Final279分别独立通过，装备色保守分支及生命周期扩展不冒充此前执行。VisualBefore等旧截图版本exit1保留；16张文件存在不代表旧断言通过。
- VisualCueBefore 74PASS/4FAIL，确认为启动已占用真实释放cue的.035秒限流状态；未声称默认攻速发生丢声。没有修改攻速/限流，只把远程声音留给真实释放。VisualCueAfter78PASS。
- 最终Final2与Runtime2各291PASS/0FAIL/2UNRESOLVED，中间Runtime279/2和两个中间构建均单独留存。最终验收192警告/纯发行96警告原文完整，不去重为更低数字、不视为警告已解决。
- 全部UNRESOLVED近距法杖样本不被6m成功覆盖；没有改CombatAim。Search/JobTempAlloc日志根因另索引，原UNKNOWN/C15/青色帧等历史失败不动，人工/原生仍NOT_RUN。

最后样式检查报告CombatFeedback.cs一个EOF空行；保留最终已测试/构建源码原字节，不为了样式重写冻结输入。原style-check.txt保留，未把该样式检查写PASS。它不是功能断言，发布SHA/范围/链接检查独立通过。
