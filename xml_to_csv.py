import os
import sys
import glob
import pandas as pd
import xml.etree.ElementTree as ET

def find_mins(points):
    xmin, ymin = points[0]
    xmax, ymax = points[0]
    for x,y in points:
        if x < xmin:
            xmin = x
        if x > xmax:
            xmax = x
        
        if y < ymin:
            ymin = y
        if y > ymax:
            ymax = y

    return xmin, ymin, xmax, ymax

def xml_to_csv(path, mode):
    xml_list = []
    klasses = {'1': 'occupied', '0': 'empty'}
    for xml_file in glob.glob(path + '/*.xml'):
        print(f'Processing {xml_file}')
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for space in root.findall('./space'):
            space_id = space.attrib['id']
            filename = os.path.join('images',mode, os.path.splitext(xml_file)[-2].split('\\')[-1] + '.jpg')
            if 'occupied' not in space.attrib:
                continue

            klass = klasses[space.attrib['occupied']]
            w = space[0][1].attrib['w']
            h = space[0][1].attrib['h']
            contour = space[1]
            points = []
            for item in contour:
                points.append([item.attrib['x'],item.attrib['y']])
            xmin, ymin, xmax, ymax = find_mins(points)
            value = (space_id,
                     filename,
                     int(w),
                     int(h),
                     klass,
                     int(xmin),
                     int(ymin),
                     int(xmax),
                     int(ymax)
                     )
            xml_list.append(value)
    column_name = ['space_id', 'filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df
    

def main():
    mode = sys.argv[1]
    image_path = os.path.join(os.getcwd(), 'images' , mode)
    xml_df = xml_to_csv(image_path, mode)
    xml_df.to_csv(os.path.join('data',f'{mode}_labels.csv'), index=None)
    print('Successfully converted xml to csv.')


main()
