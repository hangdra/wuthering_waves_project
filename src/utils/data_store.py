import cv2
import numpy as np


class DataStore:
    """单例数据存储类，支持存入和取出名称、图片和信息"""

    _instance = None
    _data = None  # 类属性，存储所有数据
    _out_img = None
    _name = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._data = []  # 初始化数据列表
            cls._name = None
            cls._out_img = []
        return cls._instance

    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def get_out_img(self):
        return self._out_img

    def add(self, image: np.ndarray, info: str):
        """
        存入数据

        参数:
            name: 名称 (str)
            image: 图片 (np.ndarray)
            info: 信息 (str)
        """
        self._data.append({
            'name': self._name,
            'image': image,
            'info': info
        })



    def get_all(self):
        """
        取出所有已放入的数据

        返回:
            list: 包含所有数据的列表，每个元素是字典 {'name': str, 'image': np.ndarray, 'info': str}
        """
        return self._data.copy()

    def clear(self):
        """清空所有数据"""
        self._data.clear()
        self._name = None
        self._out_img = []

    def count(self):
        """返回已存储的数据条数"""
        return len(self._data)

    def get_merged_img_and_show(self,show=True):
        img_combine_list = []
        max_h,max_w = 1440,3440
        area_max = max_h*max_w
        area_accumulate = 0
        print("len(self._data)",len(self._data))
        for i in range(0,len(self._data),1):
            _data_item = self._data[i]
            img_tmp = _data_item['image']
            ih,iw = img_tmp.shape[:2]
            area = ih*iw
            area_accumulate += area
            if area_accumulate > area_max*0.9:
                from src.utils.image_dealer import concat_images_grid_with_rects
                result, all_rects = concat_images_grid_with_rects(img_combine_list,max_width=max_w)
                self._out_img.append(result)
                print("_______________________________self._out_img",len(self._out_img))
                img_combine_list = []
                area_accumulate = 0
                if show:
                    cv2.imshow('result'+str(i), result)
                    while True:
                        key = cv2.waitKey(1) & 0xFF
                        if key == ord('q'):  # 按 'q' 键退出
                            break
                    cv2.destroyAllWindows()
            img_combine_list.append(img_tmp)
        #结束之后剩余的部分也要进来
        if len(img_combine_list)>0:
            from src.utils.image_dealer import concat_images_grid_with_rects
            result, all_rects = concat_images_grid_with_rects(img_combine_list, max_width=max_w)
            self._out_img.append(result)



# ============ 使用示例 ============

# 获取单例实例（全局唯一）
data_store = DataStore()