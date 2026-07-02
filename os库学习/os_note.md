# 目录操作
### 1.获取当前目录
```python

current_path = os.getcwd()  # 获取当前工作目录的绝对路径
print(current_path)

current_path = os.getcwdb() # 获取当前工作目录的绝对路径（值以Unicode编码返回）
print(current_path)

current_path = os.curdir    # 获取当前工作目录，以.表示
print(current_path)

current_path = os.pardir    # # 获取当前工作目录，以..表示
print(current_path)
```
### 2.创建目录
```python
# 注意window路径分隔符是\，linux或macos是/
current_path = os.getcwd()  # 获取当前工作目录的绝对路径
print(current_path)

# 在当前目录下创建单层目录
os.mkdir(current_path + "/test")	
# 如果目标目录已存在，则抛出异常：FileExistsError: [Errno 17] File exists

# 在当前目录下创建多层目录
os.makedirs(current_path + "/test/d1/d2") 
# 如果目标目录已存在，则抛出异常：FileExistsError: [Errno 17] File exists


```
### 3.删除目录
```python
# 注意window路径分隔符是\，linux或macos是/
current_path = os.getcwd()  # 获取当前工作目录的绝对路径
print(current_path)


# 在当前目录下删除单层目录
os.rmdir(current_path + "/test")	
# 如果目标目录不存在，会抛出异常：FileNotFoundError: [Errno 2] No such file or directory
# 如果目标目录不是单层目录或目录中存在文件，会抛出异常：OSError: [Errno 66] Directory not empty

# 在当前目录下删除多层目录
os.removedirs(current_path + "/test/d1/d2")
# 注意，如果指定删除的目录不为空或还有更深的目录，如d2目录下还有d3目录，则会抛出异常：OSError: [Errno 66] Directory not empty


```
### 4.重命名目录
```python


# 将新创建的目录重命名
os.rename(current_path + "/test", current_path + "/test_dir")

```
### 5.获取目录下所有的一级内容
```python
# 获取指定路径下所有的文件、目录内容，但不包含目录中的子文件
dirs = os.listdir(current_path)
print(dirs)	# ['demo.py', 'test1', 'test2']
```
### 6.判断目录是否存在
```python
# 注意window路径分隔符是\，linux或macos是/
current_path = os.getcwd()  # 获取当前工作目录的绝对路径
print(current_path)

print(os.path.exists(current_path)) # True
print(os.path.exists(current_path + "/test1")) # 目标目录不存在，返回False

os.mkdir(current_path + "/test1")
print(os.path.exists(current_path + "/test1")) # 目标目录创建后存在，返回True

```
### 7.判断是否是目录
```python
# 注意window路径分隔符是\，linux或macos是/
current_path = os.getcwd()  # 获取当前工作目录的绝对路径
print(current_path)

print(os.path.isdir(current_path))  # True
print(__file__)  # 当前python文件的绝对路径，current_path + demo.py
print(os.path.isdir(__file__))  # False

```
# 文件操作
### 1.创建文件
```python
# 注意window路径分隔符是\，linux或macos是/
current_path = os.getcwd()  # 获取当前工作目录的绝对路径
print(current_path)

# os.O_RDONLY   以只读的方式打开
# os.O_WRONLY   以只写的方式打开
# os.O_RDWR     以读写的方式打开
# os.O_NONBLOCK 打开时不堵塞
# os.O_APPEND 以追加的方式打开
# os.O_CREAT  创建或打开文件
# os.O_TRUNC  打开一个文件并截断它的长度为零

# 在当前工作目录中新建一个文件，demo.txt
demo_file_path = current_path + "/demo.txt"
print(demo_file_path)
# os.open() 需要三个参数，path需要打开或创建的文件路径，flags文件打开的模式，mode新创建文件的权限模式
# flags参数值对应上述说明选择，mode参数值默认是0o666，表示计算机内用户、组、其他三种身份都有读写的权限
# 创建或打开文件
fd = os.open(path=demo_file_path, flags=os.O_RDWR | os.O_CREAT, mode=0o666)
# 向文件内写入数据
os.write(fd, "Hello World".encode())
# 关闭文件
os.close(fd)

```
### 2.删除文件
```python
demo_file_path = current_path + "/demo.txt"
print(demo_file_path)

os.remove(demo_file_path)	# 删除文件

```
### 3.文件时间
```python
os.path.getatime(path)	# 1611364716.8618789
# 返回path对应文件或目录上一次访问时间，a表示access 访问
os.path.getmtime(path)
# 返回path对应文件或目录最近一次的修改时间，m表示modify 修改
os.path.getctime(path)
# 返回对应文件或目录的创建时间，c表示create 创建

time.ctime(os.path.getctime(path)
# 'Sat Jan 23 09:18:36 2021'

```
# 路径操作
### 1.路径拼接
```python
import os

current_path = os.getcwd()  # 获取当前工作目录的绝对路径
print(current_path)  # /Users/xxxx/PythonWorkspace/第20课：Python标准库初探

test_dir1 = "test1"
test_dir2 = "test2"
file_name = "demo.txt"
path = os.path.join(current_path, test_dir1, test_dir2, file_name)
print(path)  # /Users/xxxx/PythonWorkspace/第20课：Python标准库初探/test1/test2/demo.txt
```
### 2.路径分裂
```python
# 引用1.3.1的path变量值
paths = os.path.split(path)
print(paths)    # 将路径和最后一层文件或目录分裂成元祖
# ('/Users/xxxx/PythonWorkspace/第20课：Python标准库初探/test1/test2', 'demo.txt')
```
### 3.获取路径最后目录或文件名称
```python
# 引用1.3.1的path变量值
name = os.path.basename(path)
print(name) # demo.txt

```
### 4.获取文件名称的后缀
```python
# 引用1.3.1的path变量值
suffix = os.path.splitext(path)
print(suffix)  # ('/Users/xxxx/PythonWorkspace/第20课：Python标准库初探/test1/test2/demo', '.txt')

# 注意，如果path不是文件路径，而是目录路径则没有后缀，元祖的第二位元素则是空值

```
### 5.获取父级目录
```python
# 引用1.3.1的path变量值
dirname_1 = os.path.dirname(path)
print(dirname_1)  # /Users/xxxx/PythonWorkspace/第20课：Python标准库初探/test1/test2
dirname_2 = os.path.dirname(dirname_1)
print(dirname_2)  # /Users/xxxx/PythonWorkspace/第20课：Python标准库初探/test1

```
### 6.获取绝对路径
```python
# 引用1.3.1的path变量值
abspath = os.path.abspath(path)
print(abspath)  # /Users/xxxx/PythonWorkspace/第20课：Python标准库初探/test1/test2/demo.txt


```
# 环境变量操作
# 进程操作
