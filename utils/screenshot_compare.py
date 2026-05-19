import os
from PIL import Image
from pixelmatch.contrib.PIL import pixelmatch

class ScreenshotComparator:
    
    """截图对比工具"""
    def __init__(self, baseline_dir='baseline_screenshots', diff_dir='diff_screenshots'):
        self.baseline_dir = baseline_dir
        self.diff_dir = diff_dir
        os.makedirs(self.baseline_dir, exist_ok=True)
        os.makedirs(self.diff_dir, exist_ok=True)

    def save_baseline(self, page, name:str):
        """保存基准截图"""
        path = os.path.join(self.baseline_dir, f'{name}.png')
        page.screenshot(path=path)
        print(f"✅ 基准截图已保存: {path}")
        return path

    def compare(self, page, name:str, threshold:float=0.1) -> bool:
        """对比当前页面与基准截图
        
        Args:
            page: Playwright 页面对象
            name: 截图名称
            threshold: 差异阈值（0-1），超过此值认为不一致
        
        Returns:
            True: 一致, False: 不一致
            """
        baseline_path = os.path.join(self.baseline_dir, f'{name}.png')
        if not os.path.exists(baseline_path):
            raise FileNotFoundError(f"基准截图不存在: {baseline_path}，请先保存基准截图")
        
        # 截取当前页面
        current_path = os.path.join(self.diff_dir, f'{name}_current.png')
        page.screenshot(path=current_path)
        # 对比两张图片
        baseline_img = Image.open(baseline_path)
        current_img = Image.open(current_path)

        # 确保尺寸一致
        if baseline_img.size != current_img.size:
            current_img = current_img.resize(baseline_img.size)

        # 计算差异（pixelmatch 需要 RGBA 模式）
        diff_img = Image.new('RGBA', baseline_img.size)
        diff_pixels = pixelmatch(
            baseline_img.convert('RGBA'),
            current_img.convert('RGBA'),
            diff_img,
            threshold=threshold
        )

        # 保存差异图
        diff_path = os.path.join(self.diff_dir, f'{name}_diff.png')
        diff_img.save(diff_path)
        total_pixels = baseline_img.width * baseline_img.height
        diff_percent = (diff_pixels / total_pixels) * 100

        print(f"📊 差异像素: {diff_pixels} / {total_pixels} ({diff_percent:.2f}%)")
        
        if diff_pixels == 0:
            print(f"✅ 截图一致: {name}")
            return True
        else:
            print(f"❌ 截图不一致: {name}，差异图保存至: {diff_path}")
            return False
        