# CCF 第七版目录中适合「自动驾驶 / VRU / 智能骑行」的期刊与会议

> 依据：附件《第七版中国计算机学会推荐国际学术会议和期刊目录（正式版）》（2026-03-31 发布，2026 年 4 月 9 日勘误更新）。
> 本报告由该 PDF 全文（72 页）解析后逐条核对得出，共解析 681 条条目（10 个领域 × 期刊/会议 × A/B/C）。

## 0. 先说三个关键事实

1. **CCF 目录里没有「自动驾驶 / 交通 / 人因」独立领域**。10 个领域是：体系结构、网络、信息安全、软件工程、数据库、理论、图形学与多媒体、人工智能、人机交互与普适计算、交叉/综合/新兴。
2. **全目录里名称直接对口的只有 2 个**：
   - **TITS** — *IEEE Transactions on Intelligent Transportation Systems*：**交叉/综合/新兴 · 期刊 · B**
   - **JATS** — *ACM Journal on Autonomous Transportation Systems*：**人工智能 · 期刊 · C**
   全目录中 "Vehicle / Vehicular / Automotive / Pedestrian / Cycl / Bicycle" 出现次数均为 **0**。
3. 因此正确策略是：**按「子问题」拆开，投到对应领域的成熟 venue**，而不是找「自动驾驶专属刊」。
4. **本领域真正的「主场」venue 大多不在 CCF 目录内**（见第 4 节），这是该方向投稿必须知道的现实。

---

## 1. 结论速览：最值得投的 CCF venue 短名单

| # | Venue | CCF 领域/类别 | 类型 | 最匹配的子问题 |
|---|-------|--------------|------|----------------|
| 1 | **TITS** | 交叉/综合/新兴 **B** | 期刊 | 自动驾驶系统、VRU 安全、骑行安全与交通感知（最对口） |
| 2 | **CVPR / ICCV** | 人工智能 **A** | 会议 | 感知、VRU 检测/跟踪、轨迹预测、端到端驾驶 |
| 3 | **ECCV** | 人工智能 **B** | 会议 | 同上（次选，门槛略低） |
| 4 | **NeurIPS / ICML / ICLR** | 人工智能 **A** | 会议 | 预测、规划、决策、强化学习、世界模型 |
| 5 | **AAAI / IJCAI** | 人工智能 **A / B** | 会议 | 规划、推理、多智能体交互 |
| 6 | **ICRA** | 人工智能 **B** | 会议 | 机器人化自动驾驶、自行车/电动车动力学与控制、交互 |
| 7 | **IROS** | 人工智能 **C** | 会议 | 同上（更易中，产出快） |
| 8 | **TR**（IEEE Trans. Robotics） | 交叉/综合/新兴 **B** | 期刊 | 机器人规划/控制长文 |
| 9 | **TASAE**（IEEE Trans. Automation Science & Engineering） | 交叉/综合/新兴 **B** | 期刊 | 自动化系统、调度、协同 |
| 10 | **CHI / UbiComp / UIST** | 人机交互 **A** | 会议 | 骑行交互、AR-HUD、众包感知、活动识别 |
| 11 | **IEEE VR / ISMAR** | 图形学多媒体 **A / B** | 会议 | 骑行/驾驶模拟器、XR 抬头显示 |
| 12 | **TPAMI / IJCV / TIP / TMM / TVCG** | 人工智能 A / 图形 A | 期刊 | 感知、多模态、可视化长文 |
| 13 | **JSAC / TMC / INFOCOM / MobiCom** | 网络 **A** | 期刊/会议 | V2X、车联网、边缘协同 |
| 14 | **RTSS / EMSOFT / RTAS / DAC** | 交叉 A / 体系结构 A·B | 会议 | 车载实时系统、ADAS 计算平台 |
| 15 | **SIGKDD / SIGSPATIAL / RecSys** | 数据库 A / 交叉 C / 数据库 B | 会议 | 共享单车调度、骑行路径与需求预测 |

---

## 2. 按子问题映射（含 CCF 类别与等级）

### 2.1 感知：VRU 检测 / 分割 / 3D 检测 / 多模态融合
- **会议 A**：CVPR、ICCV、ACM MM、NeurIPS、ICML、ICLR、AAAI
- **会议 B**：ECCV、ICME、ICASSP、ICMR
- **会议 C**：ACCV、BMVC、ICPR、ICIP、3DV、MMM、PRCV
- **期刊 A**：TPAMI、IJCV、TIP、TMM、TVCG
- **期刊 B**：CVIU、Pattern Recognition、TCSVT、TOMM、TAP
- **期刊 C**：IVC、Machine Vision and Applications、JVCIR、Signal Processing: Image Communication

> 行人/骑行者检测、遮挡与小目标、夜间与恶劣天气、事件相机，标准去处就是 CVPR/ICCV/ECCV + TIP/TMM/TCSVT。

### 2.2 预测与规划决策：轨迹预测、行为意图、交互、强化学习
- **会议 A**：NeurIPS、ICML、ICLR、AAAI、CVPR、ICCV、WWW
- **会议 B**：IJCAI、ECCV、ICAPS（规划）、AAMAS（多智能体）、UAI
- **会议 C**：AISTATS、ICTAI、SMC、DAI
- **期刊**：TITS (B)、TR (B)、TASAE (B)、JATS (C)、TNNLS (B)、IEEE Trans. Cybernetics (B)、PR (B)、EAAI/KBS/Neurocomputing (C)

> 弱势道路使用者（行人、骑行者）轨迹预测与「车—人/车—骑」交互建模，最常用组合：CVPR/ICCV/NeurIPS + TITS。

### 2.3 机器人化驾驶与骑行载具控制（含 e-bike、自行车动力学）
- **ICRA**（人工智能 B）、**IROS**（人工智能 C）、**TR**（交叉 B）、**TASAE**（交叉 B）
- 多机/多智能体协同：**AAMAS**（人工智能 B，会议/期刊双列）、**IJCAI**（B）
- 期刊补充：TNNLS (B)、IEEE Trans. Cybernetics (B)、EAAI (C)

### 2.4 模拟器 / 数字孪生 / XR 抬头显示（骑行 AR-HUD、驾驶模拟）
- **会议 A**：**IEEE VR**、ACM MM、SIGGRAPH、IEEE VIS、UIST
- **会议 B**：**ISMAR**、SCA（动画）、I3D、ICME
- **会议 C**：**VRST**、**CASAXR**、**ICXR**、CGI、PacificVis、CAD/Graphics、AVI
- **期刊 A**：TVCG、TIP、TMM；**期刊 B**：CVMJ、CGF、CAD；**期刊 C**：TVC、C&G、VRIH、CAVW、VI

> 骑行模拟器、AR 风挡/头盔 HUD、驾驶工效学可视化 → IEEE VR / ISMAR / VRST + TVCG。

### 2.5 HCI 与人因：骑行者/驾驶员状态、可穿戴、众包感知
- **会议 A**：**CHI**、**UbiComp**、**UIST**、**CSCW**
- **会议 B**：**MobileHCI**、**PERCOM**、**IUI**、**ICWSM**、GROUP、ISS
- **会议 C**：**DIS**、**ICMI**（多模态）、**ASSETS**（无障碍，含残障骑行者）、INTERACT、MobiQuitous、UIC、AVI
- **期刊 A**：**TOCHI**、IJHCS
- **期刊 B**：**IEEE Trans. Human-Machine Systems**（驾驶员/骑行者人因最对口）、**IEEE TSMC: Systems**、CSCW、HCI、UMUAI、**CCF TPCI**、IJHCI
- **期刊 C**：PUC、**PMC**（Pervasive and Mobile Computing）、PACMHCI、THRI、BIT

> 骑行活动识别、手机/手表传感、众包路况、外卖骑手行为 → UbiComp / PERCOM / MobileHCI / PMC / THMS。

### 2.6 车联网 / V2X / 边缘计算
- **期刊 A**：**JSAC**、**TMC**、**TON**
- **期刊 B**：TCOM、TWC、TOSN、TOIT、CN、TOMM
- **期刊 C**：**IOT**（IEEE IoT Journal）、**TIOT**（ACM TIoT）、Ad Hoc Networks、TNSM、JNCA、MONET、PPNA、WCMC、Wireless Networks
- **会议 A**：**INFOCOM**、**MobiCom**、**NSDI**、SIGCOMM
- **会议 B**：**SenSys**、**MobiSys**、**SECON**、**IPSN**、**MobiHoc**、ICNP、CoNEXT、IWQoS
- **会议 C**：GLOBECOM、ICC、WCNC、**WoWMoM**、**MSN**、**MASS**、MSWiM、LCN

> V2V/V2I/V2P（车—弱势道路使用者通信）、协同感知、路侧单元边缘推理 → INFOCOM/MobiCom/JSAC/TMC + SenSys/IPSN。

### 2.7 车载计算平台 / 实时与嵌入式 / 功能安全
- **会议 A**：**RTSS**（交叉）、**DAC**（体系结构）
- **会议 B**：**EMSOFT**（交叉）、**RTAS**（体系结构）、LCTES（软件工程）
- **会议 C**：ASP-DAC、CASES、FPL、FCCM、ASAP、MASCOTS
- **期刊**：**TCAD** (A)、TODAES (B)、TECS (B)、JSA (B)、TVLSI (B)、**RTS**（Real-Time Systems，C）、**TCPS**（ACM Trans. Cyber-Physical Systems，交叉 C）

> ADAS 域控、实时调度、端侧推理部署 → RTSS/RTAS/EMSOFT/DAC；CPS 视角 → TCPS。

### 2.8 安全、隐私、鲁棒性（对抗攻击、传感器欺骗）
- **会议 A**：**CCS**、**S&P**
- **会议 C**：**WiSec**（无线与移动安全）、AsiaCCS、TrustCom、SOUPS（可用隐私/安全）、PETS、SecureComm、ICICS
- **期刊 B/C**：TOPS (B)、SCN (C)、IJISP (C)

> 自动驾驶感知的对抗样本、V2X 认证与隐私、骑行者轨迹隐私 → S&P/CCS/WiSec/PETS。

### 2.9 数据挖掘与空间数据：共享单车、骑行路径、需求预测
- **会议 A**：**SIGKDD**、**WWW**、SIGMOD、VLDB、ICDE
- **会议 B**：**RecSys**、ECML-PKDD、CIDR、ISWC
- **会议 C**：**SIGSPATIAL**、**COSIT**（空间信息理论）、PAKDD、IEEE BigData、SMC
- **期刊 B**：TKDD、WWW Journal、TITS；**期刊 C**：**TIST**（ACM Trans. Intelligent Systems and Technology）、TBD（IEEE Trans. Big Data）、TORS

> 共享单车调度与再平衡、骑行需求预测、骑行路径推荐、轨迹挖掘 → SIGKDD/RecSys/SIGSPATIAL/TIST。

### 2.10 交叉/综合与「兜底」期刊
- **SCIS**（Science China Information Sciences，交叉 A）
- **Proc. IEEE**（交叉 A）、**JCST**（交叉 B）、**FCS**（交叉 B）、**The Computer Journal**（交叉 B）
- **TITS**（交叉 B）、**JATS**（人工智能 C）、**EITEE / FITEE**（交叉 C）
- **IEEE BigData**（交叉 C）、**SMC**（交叉 C）

---

## 3. 三个主题的具体建议

### 3.1 自动驾驶（Autonomous Driving）
| 方向 | 首选（含等级） |
|------|----------------|
| 感知 / 端到端 | CVPR·ICCV (A)、ECCV (B)、TPAMI·IJCV·TIP·TMM (A) |
| 预测 / 规划 / 决策 | NeurIPS·ICML·ICLR·AAAI (A)、IJCAI (B)、ICAPS (B)、TITS (B) |
| 机器人化驾驶 | ICRA (B)、IROS (C)、TR (B)、TASAE (B) |
| V2X | INFOCOM·MobiCom·JSAC·TMC (A)、SenSys·IPSN (B)、IOT (C) |
| 车载计算 | RTSS (A)、RTAS·EMSOFT (B)、DAC (A)、TCAD (A)、TECS (B)、RTS (C) |
| 仿真 / XR | IEEE VR (A)、ISMAR (B)、VRST (C)、TVCG (A) |
| 安全 | S&P·CCS (A)、WiSec (C) |

### 3.2 VRU（弱势道路使用者：行人、骑行者、电动自行车、摩托车）
| 方向 | 首选（含等级） |
|------|----------------|
| VRU 检测 / 姿态 / 跟踪 | CVPR·ICCV (A)、ECCV (B)、3DV (C)、TIP·TMM·TVCG (A)、TCSVT (B) |
| 意图 / 轨迹预测 | CVPR·ICCV·NeurIPS (A)、ECCV·IJCAI (B)、TITS (B) |
| 车—人交互 / 安全 | TITS (B)、TR (B)、IEEE THMS (B)、IEEE TSMC (B)、SMC (C) |
| 可穿戴/众包感知 | UbiComp (A)、PERCOM (B)、PUC·PMC (C)、TMC (A) |
| 无障碍与包容设计 | ASSETS (C)、CHI (A)、DIS (C) |
| 社会/行为研究 | CHI·CSCW (A)、ICWSM (B)、PACMHCI (C) |
| VRU 隐私 | PETS·SOUPS (C)、S&P (A) |

### 3.3 智能骑行（Smart Cycling / 智能骑行）
| 方向 | 首选（含等级） |
|------|----------------|
| 骑行活动识别 / 穿戴与手机传感 | UbiComp (A)、PERCOM (B)、SenSys·IPSN (B)、PUC·PMC (C)、CCF TPCI (B) |
| 骑行 AR-HUD / 导航 / 交互 | IEEE VR (A)、ISMAR (B)、UIST·CHI (A)、MobileHCI (B)、VRST (C)、AVI (C) |
| 共享单车 / 需求与路径推荐 | SIGKDD (A)、RecSys (B)、SIGSPATIAL (C)、TIST (C)、SIGMOD·VLDB (A) |
| 电动自行车 / 自行车动力学与控制 | ICRA (B)、IROS (C)、TR (B)、TASAE (B) |
| 骑行安全分析与事故建模 | TITS (B)、SMC (C)、IEEE BigData (C)、TBD (C) |
| 骑行健康与体能 | JBHI (C)、ACM HEALTH (C)、PUC (C) |
| 骑行众包 / 交通流监测 | SenSys (B)、TMC (A)、TOSN (B)、IOT (C) |

---

## 4. 重要提醒：本领域「主场」venue 大多不在 CCF 目录内

以下都是自动驾驶 / VRU / 骑行研究的常规发表地，但**第七版目录中均未收录**（已逐词核对为 0 次出现）：

- **会议**：IEEE IV（Intelligent Vehicles Symposium）、IEEE ITSC（Intelligent Transportation Systems Conference）、**AutomotiveUI**、CoRL（Conference on Robot Learning）、RSS（Robotics: Science and Systems）、IEEE ICVES、IEEE ICUS、TRB Annual Meeting
- **期刊**：**IEEE T-IV**（Trans. Intelligent Vehicles）、**IEEE TVT**（Trans. Vehicular Technology）、IEEE ITS Magazine（magazine，按 CCF 规则明确不收）、**Transportation Research Part C**、**Accident Analysis & Prevention**、IEEE RA-L、IEEE Sensors Journal、CoRL Proceedings、IMWUT（Proc. ACM Interactive, Mobile, Wearable and Ubiquitous Technologies）

> 注意：CCF 官方声明中明确「magazine（杂志）未纳入推荐期刊列表」，因此 *IEEE Intelligent Transportation Systems Magazine* 之类即使影响因子高也不在目录内。
> 另外 CCF 强调目录**不作为学术评价依据**；若所在单位/导师以 CCF 等级考核，请优先从本文第 1 节短名单中选择。

---

## 5. 投稿组合建议（面向 CCF 考核 + 领域影响力兼顾）

1. **主线长文 → 领域主场**：把最完整的系统/数据/评测投 TITS(B)、T-IV、TR-C 或 IV/ITSC，建立领域可见度。
2. **方法创新 → CCF 高等级**：把感知新方法投 CVPR/ICCV/ECCV，预测规划投 NeurIPS/ICML/ICLR/AAAI，HCI 投 CHI/UbiComp/UIST。
3. **保底与快速产出**：IROS(C)、ACCV/BMVC/ICPR/ICIP(C)、VRST/ICXR(C)、SMC(C)、IEEE BigData(C)、JATS(C)。
4. **系统与工程**：车端实时/部署投 RTSS/RTAS/EMSOFT/DAC/TECS；通信投 INFOCOM/MobiCom/SenSys/IPSN。
5. **跨学科叙事**（骑行政策/人因/交通安全）：THMS(B)、TSMC(B)、TITS(B)、CHI(A)、SMC(C)。

---

## 附：数据来源与产物

- 原文 PDF：`第七版中国计算机学会推荐国际学术会议和期刊目录（正式版）.pdf`（72 页，CCF 2026-03-31 发布）
- 官方公告：<https://www.ccf.org.cn/Academic_Evaluation/By_category/2026-03-31/870181.shtml>
- 解析产物：`.ccf/ccf7.txt`（PDF 全文文本）、`.ccf/ccf7.json`（681 条结构化条目）
