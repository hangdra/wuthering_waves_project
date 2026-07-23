import cv2
import numpy as np
from dataclasses import dataclass
from typing import Literal, Tuple
import warnings

from src.utils.image_dealer import IconPosition, get_search_are_by_default, get_sub_image_from_image
from src.utils.read_write_image_from_filesys import imread_chinese


def equal_probability_gaussian(a, b, sigma=0.15):
    """
    高斯核概率函数

    参数：
        sigma: 标准差，控制"多近算接近"

    P(equal) = exp(-(a-b)² / (2*sigma²))
    """
    diff_sq = (a - b) ** 2
    return np.exp(-diff_sq / (2 * sigma ** 2))

@dataclass
class MatchResult:
    matched: Literal['a', 'b', 'none']
    confidence: float  # 0-1
    yellow_score: float  # 黄色像素占比（排除白区后）
    structure_score: float  # 外围结构差异分数
    details: str


class ImageMatcher:

    def __init__(self, img_a: np.ndarray, img_b: np.ndarray):
        self.img_a = self._validate(img_a, "img_a")
        self.img_b = self._validate(img_b, "img_b")

        self.template_h, self.template_w = self.img_a.shape[:2]

        if self.img_b.shape[:2] != (self.template_h, self.template_w):
            self.img_b = cv2.resize(self.img_b, (self.template_w, self.template_h))

        self.white_mask = self._extract_white_mask(self.img_a)
        self.focus_mask = cv2.bitwise_not(self.white_mask)

        # cv2.imshow('white_mask', self.white_mask)
        # cv2.imshow('focus_mask', self.focus_mask)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # 关键检查：focus_mask 是否有效
        self.white_pixels = cv2.countNonZero(self.white_mask)
        self.focus_pixels = cv2.countNonZero(self.focus_mask)
        if self.focus_pixels == 0:
            raise ValueError("模板图提取失败：未检测到非白色外围区域，请检查模板图是否包含非白色区域")

        self.a_features = self._extract_features(self.img_a, 'a')
        self.b_features = self._extract_features(self.img_b, 'b')

        cv2.imwrite("debug_white_mask.png", self.white_mask)
        cv2.imwrite("debug_focus_mask.png", self.focus_mask)
        print(f"图尺寸: {self.template_w}x{self.template_h}")
        print(f"白色像素: {cv2.countNonZero(self.white_mask)}")
        print(f"关注像素: {self.focus_pixels}")

    @staticmethod
    def _validate(img, name):
        if not isinstance(img, np.ndarray):
            raise TypeError(f"{name} 必须是 numpy.ndarray")
        if img.dtype != np.uint8:
            raise TypeError(f"{name} 必须是 uint8")
        if len(img.shape) != 3 or img.shape[2] != 3:
            raise ValueError(f"{name} 必须是 3 通道 BGR 图像")
        return img

    def _extract_white_mask(self, img: np.ndarray) -> np.ndarray:
        """
        提取中间白色区域掩码。
        假设白色区域是连通的大面积高亮区域。
        """
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 高阈值提取纯白/近白区域
        _, white = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)


        # 找最大连通域（假设中间白色是最大的白色区域）
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(white, connectivity=8)

        # 排除背景（label 0），找面积最大的白色连通域
        if num_labels <= 1:
            # 没有白色区域，退而求其次：用亮度自适应
            white = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY, 51, -10)
            return white

        # 找最大面积（跳过背景 label 0）
        largest_label = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
        mask = np.zeros_like(gray)
        mask[labels == largest_label] = 255

        # 轻微膨胀，确保边缘过渡区也被排除
        # kernel = np.ones((21, 21), np.uint8)
        # mask = cv2.dilate(mask, kernel, iterations=1)

        return mask

    def _extract_features(self, img: np.ndarray, label: str) -> dict:
        if img.shape[:2] != (self.template_h, self.template_w):
            img = cv2.resize(img, (self.template_w, self.template_h))

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        yellow_lower = np.array([24, 150, 98])
        yellow_upper = np.array([28, 221, 255])
        yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)

        if yellow_mask.shape != self.focus_mask.shape:
            yellow_mask = cv2.resize(yellow_mask, (self.template_w, self.template_h),
                                     interpolation=cv2.INTER_NEAREST)

        print("yellow_mask.shape", yellow_mask.shape,"self.focus_mask.shape", self.focus_mask.shape)
        yellow_mask = cv2.bitwise_and(yellow_mask, self.focus_mask)
        yellow_pixels = cv2.countNonZero(yellow_mask)
        # 使用 self.white_pixels 计算黄色占白色比例
        yellow_ratio = yellow_pixels / self.white_pixels if self.white_pixels > 0 else 0

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        masked_gray = cv2.bitwise_and(gray, self.focus_mask)
        edges = cv2.Canny(masked_gray, 50, 150)

        masked_img = cv2.bitwise_and(img, img, mask=self.focus_mask)
        mean_color = cv2.mean(masked_img, mask=self.focus_mask)[:3]

        return {
            'yellow_ratio': yellow_ratio,
            'yellow_mask': yellow_mask,
            'edges': edges,
            'mean_color': np.array(mean_color),
            'label': label
        }

    def match(self, img_c: np.ndarray) -> MatchResult:
        img_c = self._validate(img_c, "img_c")

        if img_c.shape[:2] != (self.template_h, self.template_w):
            img_c = cv2.resize(img_c, (self.template_w, self.template_h))

        c_features = self._extract_features(img_c, 'c')

        # 检查 C 的 focus 区域是否有效
        c_focus_pixels = cv2.countNonZero(self.focus_mask)  # 和模板一样
        if c_focus_pixels == 0:
            return MatchResult(
                matched='none',
                confidence=0.0,
                yellow_score=0.0,
                structure_score=0.0,
                details="输入图无有效外围区域"
            )

        yellow_a = self.a_features['yellow_ratio']
        yellow_b = self.b_features['yellow_ratio']
        yellow_c = c_features['yellow_ratio']

        print("yellow_a", yellow_a,"yellow_b", yellow_b,"yellow_c", yellow_c)
        yellow_gap_ab = abs(yellow_a - yellow_b)
        yellow_gap_cb = abs(yellow_c - yellow_b)

        equal_yellow_pro = equal_probability_gaussian(yellow_gap_ab,yellow_gap_cb)
        print("equal_yellow_pro", equal_yellow_pro,"yellow_gap_ab",yellow_gap_ab,"yellow_gap_cb",yellow_gap_cb)

        yellow_threshold = 0.7

        # if yellow_gap_cb/yellow_gap_ab
        is_yellow_detected = equal_yellow_pro > yellow_threshold

        def edge_similarity(edges1, edges2, dilate_kernel=2):
            """
            带膨胀的边缘 IoU，容忍 dilate_kernel//2 像素的位移
            """
            if dilate_kernel > 1:
                kernel = np.ones((dilate_kernel, dilate_kernel), np.uint8)
                edges1_d = cv2.dilate(edges1, kernel, iterations=1)
                edges2_d = cv2.dilate(edges2, kernel, iterations=1)
            else:
                edges1_d, edges2_d = edges1, edges2

            intersection = cv2.countNonZero(cv2.bitwise_and(edges1_d, edges2_d))
            union_area = cv2.countNonZero(cv2.bitwise_or(edges1_d, edges2_d))

            if union_area == 0:
                return 1.0 if cv2.countNonZero(edges1) == cv2.countNonZero(edges2) else 0.0
            return intersection / union_area

        edge_sim_ca = edge_similarity(c_features['edges'], self.a_features['edges'])
        edge_sim_cb = edge_similarity(c_features['edges'], self.b_features['edges'])

        # color_dist_ca = np.linalg.norm(c_features['mean_color'] - self.a_features['mean_color'])
        color_dist_cb = np.linalg.norm(c_features['mean_color'] - self.b_features['mean_color'])
        # color_sim_ca = 1 - min(color_dist_ca / 300, 1)#有黄圈 无用了
        # sqrt(255**2+255**2+255**2) = 441.7   300/441.7=0.68
        color_sim_cb = 1 - min(color_dist_cb / 300, 1)

        if is_yellow_detected:#跟a更像
            confidence = min(equal_yellow_pro, 1.0) if yellow_a > 0 else 0.5
            #如果边缘跟b更像
            if edge_sim_cb > edge_sim_ca + 0.3:
                confidence *= 0.5
            return MatchResult(
                matched='lock_on',
                confidence=round(confidence, 3),
                yellow_score=round(equal_yellow_pro, 4),
                structure_score=round(edge_sim_ca, 3),
                details=f"检测到黄色特征({yellow_c:.3f} > {yellow_threshold:.3f})"
            )
        else:
            # 安全计算边缘密度
            c_edge_count = cv2.countNonZero(c_features['edges'])
            b_edge_count = cv2.countNonZero(self.b_features['edges'])

            c_edge_density = c_edge_count / self.focus_pixels if self.focus_pixels > 0 else 0
            b_edge_density = b_edge_count / self.focus_pixels if self.focus_pixels > 0 else 0

            structure_score = edge_sim_cb
            print("edge_sim_cb",edge_sim_cb,"c_edge_density",c_edge_density,"b_edge_density",b_edge_density)

            if structure_score > 0.7 and c_edge_density > b_edge_density * 0.7:
                confidence = structure_score * 0.8 + color_sim_cb * 0.2
                return MatchResult(
                    matched='lock_off',
                    confidence=round(min(confidence, 1.0), 3),
                    yellow_score=round(equal_yellow_pro, 4),
                    structure_score=round(structure_score, 3),
                    details=f"无黄色，结构与B相似({structure_score:.3f})"
                )
            else:
                confidence = 1 - max(structure_score * 0.8 + color_sim_cb * 0.2, equal_yellow_pro)
                return MatchResult(
                    matched='none',
                    confidence=round(min(max(confidence, 0.5), 1.0), 3),
                    yellow_score=round(equal_yellow_pro, 4),
                    structure_score=round(structure_score, 3),
                    details=f"无黄色且结构与B不匹配({structure_score:.3f})"
                )


# ========== 使用示例 ==========
import os

from src.utils.tools import get_root_dir, get_config_dir_from_root, get_template_img_dir_from_root
Root_dir = get_root_dir(__file__)
Config_dir = get_config_dir_from_root()
Img_dir = get_template_img_dir_from_root()
if __name__ == "__main__":
    # 加载模板
    img_a = imread_chinese("src/assets/images/enemy_lock.png")[0:20,0:20]  # 有黄色圈
    img_b = imread_chinese("src/assets/images/enemy_lock.png")[0:20,20:40] # 无黄色圈
    # cv2.imshow("a", img_a)
    # cv2.imshow("b", img_b)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


    # 初始化匹配器
    matcher = ImageMatcher(img_a, img_b)

    # 测试各种 C
    output_dir = "src/tests/images/auto/"
    test_cases = ["mc_lock_enemy_4_True.png","mc_lock_enemy_5_False.png","mc_lock_enemy_6_False.png"]
    new_cases = []
    for filename in os.listdir(Root_dir / output_dir):
        # if len(filename.split("_")[0]) == 3 and filename.startswith("mc"):
        if filename.startswith("mc"):
            new_cases.append(filename)
    print(new_cases)
    for filename in new_cases:
        img_c = imread_chinese(f"{output_dir}{filename}")
        tar_window_h, tar_window_w = img_c.shape[:2]
        tem_window_w, tem_window_h = 1600, 900
        l = {"template_window_width": 1600, "template_window_height": 900,
             "template_area_list": [{"x": 1198, "y": 801, "skill_no": 4}, {"x": 1118, "y": 801, "skill_no": 5},
                                    {"x": 1038, "y": 801, "skill_no": 6}], "template_width": 20, "template_height": 20}
        target_v = int(filename.split("_")[3])
        for i in l['template_area_list']:
            if i["skill_no"] == target_v:
                tem_target_x, tem_target_y = i["x"], i["y"]
        tem_w = l["template_width"]
        tem_h = l["template_height"]
        position_group = IconPosition.RIGHT_BOTTOM
        print("tar_window_w:", tar_window_w, "tar_window_h:", tar_window_h, "tem_window_w:", tem_window_w,
              "tem_window_h:", tem_window_h, "tem_target_x:", tem_target_x, "tem_target_y:", tem_target_y, "tem_w:",
              tem_w, "tem_h:", tem_h)
        roi_x_fix, roi_y_fix, roi_w_fix, roi_h_fix = get_search_are_by_default(tar_window_w, tar_window_h, tem_window_w,
                                                                               tem_window_h, tem_target_x, tem_target_y,
                                                                               tem_w, tem_h, position_group,
                                                                               w_variance=1,
                                                                               h_variance=1)

        target_img_sub = get_sub_image_from_image(img_c, roi_x_fix, roi_y_fix, roi_w_fix, roi_h_fix)

        # cv2.imshow("target_img_sub", target_img_sub)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        result = matcher.match(target_img_sub)
        print(f"\n{filename}:")
        print(f"  匹配结果: {result.matched} (置信度: {result.confidence})")
        print(f"  黄色分数: {result.yellow_score}")
        print(f"  结构分数: {result.structure_score}")
        print(f"  详情: {result.details}")