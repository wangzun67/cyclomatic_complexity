## code format
代码使用black来做format，使用isort来做import管理

安装format工具：

```
pip3 install black
pip3 install isort
```

代码提交之前执行：

```
isort
black
```

## install dependency

```
pip3 install -r requirement.txt
```

## execute tests
```
python3 cyclomatic_complexity.py tests
```

## usage
folder：
```
python3 cyclomatic_complexity.py tests
```

file:
```
python3 cyclomatic_complexity.py test.py
```
