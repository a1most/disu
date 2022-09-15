# disu
包含crt.sh、fullhunt、fofa、360quake、fofa、hunter、virustotal、zoomeye的获取子域名的集成工具。

说明：
除crt.sh外，其他平台需要在config.ini中配置api。

使用：python3 disu.py -d baidu.com

![1663206603508](https://user-images.githubusercontent.com/34560797/190294393-a1cd12ca-9877-4c09-bb42-dfe0fd8e73bd.png)

以上是在未配置api的情况下出现的情况。

正常配置出现的情况如下：

![image](https://user-images.githubusercontent.com/34560797/190296639-b58b4223-f315-46c6-ad07-b6c77ff74fe1.png)


最终生成的文件结果如下：

![image](https://user-images.githubusercontent.com/34560797/190296926-b6e62f2c-77ec-454e-950d-6c5a82a04a67.png)


目前实现的功能：
1、从各平台获取子域名信息。
2、去重并检测子域名存活性，保存到output目录下。
3、保存到test.db数据库文件。

后续将实现：
1、提升检测子域名存活的速度。
2、加入更多平台，欢迎提意见。

喜欢记得三连。




