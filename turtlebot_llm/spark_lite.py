# coding:utf-8
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

#星火认知大模型Spark Max的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_URL = 'wss://spark-api.xf-yun.com/v4.0/chat'
#星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
SPARKAI_APP_ID = ''
SPARKAI_API_SECRET = ''
SPARKAI_API_KEY = ''
#星火认知大模型Spark Max的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_DOMAIN = '4.0Ultra'

spark = ChatSparkLLM(
        spark_api_url=SPARKAI_URL,
        spark_app_id=SPARKAI_APP_ID,
        spark_api_key=SPARKAI_API_KEY,
        spark_api_secret=SPARKAI_API_SECRET,
        spark_llm_domain=SPARKAI_DOMAIN,
        streaming=False,
    )

def spark_lite(input):
    messages = [ChatMessage(role="system", content=
                            '''
                            只可调用以下这些方法(不要重新定义这些方法,不需要重新定义类),根据以下需求生成对应的Python代码段(必须使用self前缀!!!),控制移动机器人按照指定的动作执行(只需要输出控制代码段!!只需要输出控制代码段!!只需要输出控制代码段!!): self.forward(x) #机器人前进x米; self.backward(x) #机器人后退x米: self.left(x) #机器人左转x度; self.right(x) #机器人右转x度: self.stop() #机器人停下。  
                            示例1:
                            输入: 前进5米, 左转90度, 再后退3米, 最后停下。
                            输出：
                            ```python
                            self.forward(5) 
                            self.left(90) 
                            self.backward(3) 
                            self.stop()
                            ```
                            示例2:
                            输入: 走一个边长为0.5米的等边三角形。
                            输出：
                            ```python
                            self.forward(0.5) 
                            self.left(120) 
                            self.forward(0.5) 
                            self.left(120)
                            self.forward(0.5) 
                            self.stop()
                            ```
                            '''),
                ChatMessage(role="user",content=input)]
    handler = ChunkPrintHandler()
    a = spark.generate([messages], callbacks=[handler])
    print(a.flatten()[0].generations[0][0].text)
    return a.flatten()[0].generations[0][0].text

if __name__ == '__main__':
    print(spark_lite('走一个边长为1米的正方形'))