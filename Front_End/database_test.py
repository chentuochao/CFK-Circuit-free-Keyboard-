'''database.py 的使用实例'''
import database


sentences = database.get_sentences()
rare_dict = database.generate_rare_dict(sentences)
print(database.package_give_sentence(sentences,rare_dict))
