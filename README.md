# thinkphp
thinkphp ci cd


think php
基于Github/k8s/ArgoCD。流程分为 3 个阶段，实现代码 push到Github后自动部署到K8s。

关键组件
- K8s  ArgoCD
- Github  Actions / Packages

CI CD　部署流程
  - 开发提交代码到指定Github分支 
  - Github  Actions 使用Dockerfile 打包镜相到 Github Packages
  - ArgoCD 监听 Github 仓库根目录下 k8s/depoly.yaml 文件 自动拉取 部署到K8s 集群
  
实现代码管理 构建 部署 全部流程自动化