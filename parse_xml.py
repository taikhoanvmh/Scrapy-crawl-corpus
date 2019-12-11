# -*- coding: utf-8 -*-
#!/usr/bin/python

from xml.etree import ElementTree

class Parse_XML():

    name = "xml"

    def parse():
    	#Ham phan biet ENG va VN:
        def Check_ENG_VN(string):
        	INPUT = "ạảãàáâậầấẩẫăắằặẳẵóòọõỏôộổỗồốơờớợởỡéèẻẹẽêếềệểễúùụủũưựữửừứíìịỉĩýỳỷỵỹđẠẢÃÀÁÂẬẦẤẨẪĂẮẰẶẲẴÓÒỌÕỎÔỘỔỖỒỐƠỜỚỢỞỠÉÈẺẸẼÊẾỀỆỂỄÚÙỤỦŨƯỰỮỬỪỨÍÌỊỈĨÝỲỶỴỸĐ"
        	string = str(string)
        	for token in INPUT:
        		if string.find(token)!= -1 : return 1 
        	return 0

        #Mo file xml - input
        f_0 = open('data.xml','r')
        tree_0 = ElementTree.parse('data.xml')
        root_0 = tree_0.getroot()

        #Mo file xml - output
        f_1 = open('corpus.xml','w')
        root_1 = ElementTree.Element("Doc")

        #Loop file xml input to ouput
        list_text = root_0.findall('text')
        num = 1
        temp = 0
        for i in range(len(list_text)):
            if i == 0 : 
                continue
            if Check_ENG_VN(list_text[i].text) == 0:
                sentence = ElementTree.Element('Sent')
                sentence.set('id',str(num))
                num += 1
                Eng = ElementTree.SubElement(sentence, 'ENG')
                Vn = ElementTree.SubElement(sentence, 'VN')
                Eng.text = str(list_text[i].text) + '.'
                for j in range(temp + 1, i + 6):
                    if j > len(list_text) - 1: break
                    if Check_ENG_VN(list_text[j].text) == 1:
                        Vn.text = str(list_text[j].text) + '.'
                        temp = j
                        break
                root_1.append(sentence)
        tree = ElementTree.ElementTree(root_1)		
        tree.write('corpus.xml')


    parse()

    	

