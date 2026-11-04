# 纯发行可玩包与人工检查

最终纯发行路径见REPORT和Evidence/build-identities.json；使用最新LatestPureBuild4/Release，不使用包含NW/CP6/CPC测试驱动的测试包。默认正常启动仍进入标题；独立训练使用：

```powershell
& '<LatestPureBuild4>/Release/WanxiangGuitu.exe' -cp05-training -wanxiang-storage-root 'I:/WGCombat/<fresh-owned-playtest-root>'
```

使用全新、工程外合成目录，不指向真实存档。Esc释放鼠标，点击“训练装备架（临时）”；新武器先生成地面物品，不直接入包。靠近按当前交互键拾取（默认E），Tab打开背包，在双武器页选择主/副武器；默认V切换。技能面板选择两个独立技能之一，再用当前技能键（默认F）；所有提示读取当前绑定，本批不改键位。保留原四武器按钮和自由/辅助模式对照。

建议分别检查：双刃左右/交叉和真实翻滚反击、巨剑蓄势与地波、镰刀弧形与受墙阻挡牵引；四旧武器与两个法杖近距案例；暂停、切换、重开、死亡、库存和声音。记录操作者、构建SHA/文件SHA、键位、录像时间、输入与观察，不预填PASS。

本批没有真实操作者原生键鼠或独立试玩记录。自动化截图、受控API调用、AI攻击和WM_CLOSE均不等于这些验收。模型为原创简化分件、既有剪辑加程序化骨骼补充；左手握持、尾迹遮挡、音质和整体美术需要人工判断。
