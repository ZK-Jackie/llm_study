>  **实践 -> prompt -> prompt + llm实践 -> langchain + RAG 学习 -> 微调** + agent开发

## 一、微调简介

### 1. 什么是微调？

大语言模型的微调（Fine-tuning）是一种常用的**深度学习技术**。

在训练大语言模型时，通常会——

使用大量的数据预训练一个模型 -> **使用特定的**任务数据对模型进行微调。

### 2. 为什么要微调？

- 模型参数量大，重新训练成本高
- Prompt Engineering优缺点明显，需要微调来解决
  - P.E.优点：简单、高效
  - P.E.缺点：Prompt容易变得很长，推理成本高
- 当Prompt Engineering无法满足需求时

使用微调，可以利用预训练模型学习到的通用特征，而不需要从头开始训练模型，节省成本。

在微调过程中，模型的大部分层（通常是前面的层）的权重会被冻结，只有最后几层（通常是全连接层）的权重会被更新。这是因为前面的层通常负责学习通用的特征，而后面的层则负责学习特定任务的特征。

### 3. 微调的一版步骤

1. 选择一个预训练模型。
2. 冻结模型的大部分层，只让最后几层可以更新权重。
3. 使用特定任务的数据训练模型。
4. 评估模型的性能。

## 二、如何对大模型进行微调

从参数规模的角度看——

- 全量微调FFT(Full Fine Tuning)
  - 基本原理：用特定的数据，对大模型进行训练
  - 缺点：
    - 训练的成本会比较高（微调参数约等于预训练参数）
    - 灾难性遗忘 Catastrophic Forgetting（模型的某一领域拔高了，另一领域可能会下降）
- 轻量微调（高效微调）PEFT(Parameter-Efficient Fine-Tuning)【主流方案】
  - 解决FFT的问题

从训练数据的来源、以及训练的方法的角度看——

- 监督式微调SFT(Supervised Fine-Tuning)
- 基于人类反馈的强化学习微调RLHF(Reinforcement Learning with Human Feedback)
- 基于AI反馈的强化学习微调RLAIF(Reinforcement Learning with AI Feedback)

下面将只对当前热门常用的方案进行简要介绍：

### 1. PEFT微调方案

#### （1）Prompt Tuning

目标：基座模型(Foundation Model)的**参数不变**，为每个特定任务，训练一个少量参数的小模型，在具体执行特定任务的时候**按需调用**。

基本原理：在输入序列之前，增加一些特定长度的特殊Token，以增大生成期望序列的概率

#### （2）Prefix Tuning

目标：（类似于Prompt Tuning）

基本原理：在不改变大模型的前提下，在Prompt上下文中添加适当的条件，引导大模型有更加出色的表现

#### （3）LoRA

基本原理：线性代数

#### （4）QLoRA

基本原理：线性代数


### 2. RLHF

基本原理：通过让人对不同的模型输出进行排序或评分来收集人类反馈，从而提供奖励信号（reward signal）。收集到的奖励标签（reward labels）可以用来训练奖励模型（reward model），进而反过来指导LLM（Language Model）适应人类的喜好。

奖励模型本身是通过监督学习（supervised learning）来学习的（通常使用预训练的LLM作为基础模型）。