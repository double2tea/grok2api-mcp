# Git Commit Guide

## 🚀 Pre-commit Hook 已启用

每次 `git commit` 时会自动运行以下检查：

### ✅ **通过检查**
- 合并冲突标记
- 敏感信息泄露
- JavaScript/TypeScript语法
- 文件大小检查

### ⚠️ **警告（不阻止提交）**
- console.log/debugger代码
- TODO/FIXME注释
- 大文件（>1MB）
- 空文件

## 📝 **提交命令**

```bash
# 正常提交
git commit -m "Your commit message"

# 跳过检查（不推荐）
git commit --no-verify -m "Skip pre-commit"

# 分阶段提交
git add .
git commit -m "Add new feature"
```

## 🔧 **扩展钩子**

钩子位于：`.git/hooks/pre-commit`

**可添加的检查**：
- ESLint代码检查
- Prettier格式化
- 单元测试
- 类型检查（TypeScript）
- 安全扫描

## 🎯 **最佳实践**

1. **处理警告**：定期清理TODO/FIXME
2. **避免敏感信息**：使用环境变量
3. **保持文件小**：>1MB使用Git LFS
4. **移除调试代码**：生产环境不提交调试代码

## ❌ **阻止提交的情况**

- 合并冲突标记未解决
- 硬编码密码/API密钥
- JavaScript语法错误

## 💡 **提示**

- 警告可以忽略，但建议处理
- 错误必须修复才能提交
- 使用 `--no-verify` 紧急跳过（谨慎使用）
