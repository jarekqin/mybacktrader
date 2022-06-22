from xml.dom.minidom import Document

# main template
MAIN_NAME = 'ZSIM'
MAIN_ATTRIB = {'id': 'combo', 'path': 'you see', 'test': 'test1'}
# main template
MAIN_MODULE_NAME = 'Alphas'
MAIN_MODULE_ATTRIB = {'id': 'alphas', 'path': 'you see3', 'test': 'test3'}

# main operation template
MAIN_OPERATION_NAME = 'Operations'
MAIN_OPERATION_ATTRIB = {'id': 'operations', 'path': 'you see2', 'test': 'test2'}

# sub module template
SUB_MODULE_NAME = ['sub1', 'sub2', 'sub3']
SUB_MODULE_ATTRIB = [
    {'id': 'alpha', 'name': '1', 'test': 'test1'},
    {'id': 'alpha', 'name': '2', 'test': 'test2'},
    {'id': 'alpha', 'name': '3', 'test': 'test3'}
]
#sub operation template
SUB_OPEARTION_NAME = ['op1', 'op2', 'op3']
SUB_OPEARTION_ATTRIB = [
    {'id': 'sub_op1', 'name': 'opo1', 'test1': 'test1'},
    {'id': 'sub_op2', 'name': 'opo2', 'test2': 'test2'},
    {'id': 'sub_op3', 'name': 'opo3', 'test3': 'test3'}
]

class XMLTools(object):
    def __init__(self, local_xml_path=None, save_xml_path=None):
        self.local_xml_path = local_xml_path
        self.save_xml_path = save_xml_path
        self.doc_generator = Document()

    def create_modules(self, name, **kwargs):
        if name not in [None, ''] and len(kwargs) > 0:
            self.root = self.doc_generator.createElement(name)
            for k, v in kwargs.items():
                self.root.setAttribute(k, v)
            self.doc_generator.appendChild(self.root)
        else:
            raise ValueError('name and kwargs variable cannot be emapty!')

    def create_sub_module(self,parent_node,module_name, parent_name=None,**kwargs):
        if len(module_name)>0 and len(kwargs) > 0:
            sub_main_module = self.doc_generator.createElement(module_name)
            for k,v in kwargs.items():
                sub_main_module.setAttribute(k,v)
            if parent_name in [None,'']:
                parent_node.appendChild(sub_main_module)
            else:
                parent_node.getElementsByTagName(parent_name)[0].appendChild(sub_main_module)
        else:
            raise ValueError('name and kwargs variable cannot be emapty!')


    def main(self):
        if self.local_xml_path in [None, '']:
            self.create_modules(MAIN_NAME,**MAIN_ATTRIB)
            self.create_sub_module(self.root,MAIN_MODULE_NAME, **MAIN_MODULE_ATTRIB)
            self.create_sub_module(self.root,MAIN_OPERATION_NAME, **MAIN_OPERATION_ATTRIB)
            for sub_module,sub_module_attrib in zip(SUB_MODULE_NAME,SUB_MODULE_ATTRIB):
                self.create_sub_module(self.root,sub_module, MAIN_MODULE_NAME,**sub_module_attrib)
            for sub_operation,sub_operation_attrib in zip(SUB_OPEARTION_NAME,SUB_OPEARTION_ATTRIB):
                self.create_sub_module(self.root,sub_operation,MAIN_OPERATION_NAME, **sub_operation_attrib)

        fp = open(self.save_xml_path, 'w')
        fp.write(self.doc_generator.toprettyxml(indent=''))


if __name__ == '__main__':
    test_model = XMLTools(save_xml_path='./test.xml')
    test_model.main()
