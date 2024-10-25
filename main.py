
from bad_smells_groups import BAD_SMELLS_GROUPS_DICT, get_bad_smells_classes_dict
from dict2xml import dict2xml
import glob
import json
import os


BAD_SMELLS_CLASSES_DICT = get_bad_smells_classes_dict()


JPG = '.jpg'
JSON = '.json'
XML = '.xml'

CONFORMANCE_LIST = 'conformanceList'
DATA = 'data'
ID = 'id'
NAME = 'name'
VIOLATION_LIST = 'violationList'


uis_hunter_path = 'I:\\datasets\\UIS-Hunter'
uis_hunter_xml_path = os.path.join(uis_hunter_path, 'xml')
raw_json_path = os.path.join(uis_hunter_path, 'raw_json')
gallery_file_path = os.path.join(uis_hunter_path, 'result', 'gallery.json')


def get_gallery_data(gallery_file_path):
    # Opening JSON file
    file = open(gallery_file_path, 'r')
    gallery_data = json.load(file)
    file.close()
    return gallery_data[DATA]


def get_uis_dataset_list(gallery_data, classes = BAD_SMELLS_CLASSES_DICT):
    uis_dataset_dict = {}

    for gallery_item in gallery_data:
        conformance_list = gallery_item[CONFORMANCE_LIST]
        violation_list = gallery_item[VIOLATION_LIST]
        name = gallery_item[NAME]
        class_id = BAD_SMELLS_GROUPS_DICT[name][0]
        class_name = BAD_SMELLS_GROUPS_DICT[name][1]

        for ui_id in violation_list:
            if ui_id in uis_dataset_dict:
                uis_dataset_dict[ui_id][class_id] = True
            else:
                classes_dict = classes.copy()
                classes_dict[class_id] = True
                uis_dataset_dict[ui_id] = classes_dict

    return uis_dataset_dict


def get_xmls_from_jsons(jsons_path = raw_json_path, xmls_path = uis_hunter_xml_path):
    xmls_saved = 0

    if not os.path.exists(xmls_path) or not os.path.isdir(xmls_path):
        os.mkdir(xmls_path)

    jsons_list = glob.glob(f'{jsons_path}{os.sep}*{JSON}')

    for json_file in jsons_list:
        f = open(json_file, encoding='utf-8')
        json_data = json.load(f)
        #print(f'type(json_data): {type(json_data)}')
        f.close()

        json_file_name = os.path.basename(json_file)
        file_name_no_ext = os.path.splitext(json_file_name)[0]
        xml_file_path = os.path.join(xmls_path, f'{file_name_no_ext}{XML}')

        xml_data = dict2xml(json_data)

        f = open(xml_file_path, "w", encoding='utf-8')
        f.write(xml_data)
        xmls_saved += 1
        f.close()

    return xmls_saved


if __name__ == '__main__':
    """
    gallery_data = get_gallery_data(gallery_file_path)
    #print(f'gallery_data:{os.linesep}{gallery_data}')
    uis_dataset_list = get_uis_dataset_list(gallery_data)
    print(f'len(uis_dataset_list): {len(uis_dataset_list)}')

    with open('uis_dataset.json', 'w') as f:
        json.dump(uis_dataset_list, f)
    """


    f = open('uis_dataset.json')

    # returns JSON object as a dictionary
    uis_dataset = json.load(f)
    f.close()

    print(f'len(uis_dataset): {len(uis_dataset)}')
    # 66261
    #xmls_saved = get_xmls_from_jsons()
    #print(f'xmls_saved: {xmls_saved}')

    
