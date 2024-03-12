from langchain.indexes import GraphIndexCreator
from langchain.llms.base import LLM
from LLM.InternLM import InternLM


class GraphCreator(GraphIndexCreator):

    def __init__(self, llm: LLM):
        GraphIndexCreator.__init__(self)
        self.llm = llm


graph_creator = GraphCreator(llm=InternLM('/root/Shanghai_AI_Laboratory/internlm-chat-7b'))
print(graph_creator.from_text(
    '对中西部地区、老工业基地、新疆生产建设兵团和在京中央国家机关及所属事业单位所需资金，中央财政予以适当补助。').get_triples())
