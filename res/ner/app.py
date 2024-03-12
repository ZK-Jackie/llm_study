import hanlp
# load basic tokenizer
# tok = hanlp.load(hanlp.pretrained.tok.COARSE_ELECTRA_SMALL_ZH)
# load fine(another) tokenizer
# tok_fine = hanlp.load(hanlp.pretrained.tok.FINE_ELECTRA_SMALL_ZH)

# divide one sentence
# tok('晓美焰来到北京立方庭参观自然语义科技公司')
# divide multiple sentences
# tok_fine(['商品和服务。', '晓美焰来到北京立方庭参观自然语义科技公司'])
# divide passages
# HanLP = hanlp.pipeline()\
#    .append(hanlp.utils.rules.split_sentence) \
#    .append(tok)
# token_text: list = HanLP('量体裁衣，HanLP提供RESTful和native两种API。两者在语义上保持一致，在代码上坚持开源。')

HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_BASE_ZH)
result = HanLP(
    '根据《中华人民共和国社会保险法》、《中华人民共和国银行业监督管理法》、《中华人民共和国保险法》、《中华人民共和国证券投资基金法》等法律法规，经党中央、国务院同意，现就推动个人养老金发展提出以下意见',
    tasks=['ner/msra', 'dep']
)
print(result)
# doc = HanLP(['2021年HanLPv2.1为生产环境带来次世代最先进的多语种NLP技术。', '阿婆主来到北京立方庭参观自然语义科技公司。'], tasks='dep')


# dep(["2021年", "HanLPv2.1", "带来", "次", "世代", "最", "先进", "的", "多", "语种", "NLP", "技术", "。"], conll=False)
