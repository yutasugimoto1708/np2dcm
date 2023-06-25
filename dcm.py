import os 
from glob import glob
import numpy as np
import random
import datetime
from PIL import Image
import pydicom
from pydicom.dataset import Dataset
from pydicom.uid import generate_uid
from dammy_dcm import Dammy

class Dcm(Dammy):
    # shape(D,H,W)を想定 
    def __init__(self):
        super().__init__()
        self.today, self.age = self._today_and_age() 
    
    def _today_and_age(self):
        t_delta = datetime.timedelta(hours=9)
        JST = datetime.timezone(t_delta, 'JST')
        now = datetime.datetime.now(JST)
        today = now.strftime('%Y%m%d')
        birth_date = datetime.datetime(2000, 12, 8) 
        age = now.year - birth_date.year
        if (now.month, now.day) < (birth_date.month, birth_date.day):
            age -= 1
        return today, age 

    def _get_dtype_max_min(self, array):
        if np.issubdtype(array.dtype, np.integer):
            info = np.iinfo(array.dtype)
        elif np.issubdtype(array.dtype, np.floating):
            info = np.finfo(array.dtype)
        else:
            raise ValueError("Unsupported data type.")
        return info.max, info.min 

    def _ch_dtype(self, array, dtype):
        """
        ダイナミックレンジを考慮しながらdtypeを変えるメソッド
        (配列の最大、最小値を変化後のdtypeの最大値、最小値としてスケールを変える)
        """
        # ダイナミックレンジを計算
        min_val = np.min(array)
        max_val = np.max(array)
        dynamic_range = max_val - min_val
        if dynamic_range == 0: return array.astype(dtype)
        # dtypeに基づいて値の範囲を調整
        normalized_array = (array - min_val) / dynamic_range
        # dtypeの最大値と最小値を取得
        if np.issubdtype(dtype, np.floating):
            dtype_min = np.finfo(dtype).min
            dtype_max = np.finfo(dtype).max
        else:
            dtype_min = np.iinfo(dtype).min
            dtype_max = np.iinfo(dtype).max
        scaled_array = normalized_array * (dtype_max - dtype_min) + dtype_min
        return scaled_array.astype(dtype)

    def overlay(self, bottom, top, alpha =0.3):
        """
        画像を薄く重ねるメソッド
        入力のshapeはD,H,W
        出力のdtypeはuint8となる
        """
        assert bottom.shape == top.shape, "The two data shapes are different."
        D = bottom.shape[0]
        bottom = self._ch_dtype(bottom, dtype = np.uint8)
        top = self._ch_dtype(top, dtype = np.uint8)
        overlay_list = []
        for i in range(D): 
            # bottom
            bottom_pixel_array = bottom[i,:,:]
            bottom_pil = Image.fromarray(bottom_pixel_array).convert("RGB")
            # top
            top_pixel_array = top[i,:,:]
            nonzero_indices = np.nonzero(top_pixel_array)
            top_pixel_array_rgb = np.zeros((top_pixel_array.shape[0], top_pixel_array.shape[1], 3), dtype=np.uint8)    
            red, green, blue = 100, 200, 100
            top_pixel_array_rgb[nonzero_indices] = [red, green, blue]
            top_pil = Image.fromarray(top_pixel_array_rgb)
            # overlay
            overlay_pil = Image.blend(bottom_pil, top_pil, alpha)# アルファ値（透明度）
            overlay_pixel_array = np.array(overlay_pil)
            overlay_list.append(overlay_pixel_array)
        overlay = np.stack(overlay_list, axis=0)
        return overlay

    def np2dcm(self, np_dic, case = "Dammy", savedir = "."):
        """
        配列からdicomファイルを作成する
        np.dic : 入力(辞書型で) 症例内のすべての処理画像を{"処理画像名":array(D,H,W)}で格納
        case : 症例名 
        """
        today, age =self._today_and_age() 
        caseUID = pydicom.uid.generate_uid()
        for i, (key, array) in enumerate(np_dic.items()): # per key
            assert np.issubdtype(array.dtype, np.integer), "dtype only integer"
            if array.ndim == 2:
                np.expand_dims(array,axis=0)
            assert array.ndim >= 3 , "Cannnot use this method array dim is 1"
            bit = array.dtype.itemsize * 8
            is_signed = self._is_negative_possible(array.dtype)
            keyUID = pydicom.uid.generate_uid()
            os.makedirs(os.path.join(savedir, case, key),exist_ok=True)
            D = array.shape[0]
            dmax, dmin = self._get_dtype_max_min(array)
            for j in range(D): # per slice
                # case統一,case毎に異なる値、基本的にcase名と同一とする
                ds = self.ds 
                ds.PatientName = f"{case}"
                ds.PatientID = f"{case}"
                ds.PatientBirthDate = f"20001208"  # 形式は"YYYYMMDD"
                ds.PatientSex = "M" # "F"は女性、"M"は男性
                ds.PatientAge = f"0{age}Y"
                # case統一
                ds.StudyInstanceUID = caseUID
                ds.StudyDate =  today  #形式は"YYYYMMDD"
                # 処理画像毎異なる値
                ds.SeriesNumber = f"{i+1:04}"
                ds.SeriesInstanceUID = keyUID
                ds.SeriesDescription = key
                # 処理スライス毎異なる値
                ds.PixelData = array[-(j+1),:,:].tobytes()
                ds.InstanceNumber = f"{j+1}"
                ds.ImagePositionPatient = ['0', '0', f'{j}']
                ds.SOPInstanceUID = pydicom.uid.generate_uid()
                ds.WindowWidth = array.max() - array.min()
                ds.WindowCenter = array.max() - array.min()//2 
                ds.BitsAllocated = bit 
                ds.BitsStored = bit
                ds.HighBit = bit - 1
                ds.PixelRepresentation = is_signed
                if array.ndim == 4: 
                    # RGB専用の変更点
                    ds.PhotometricInterpretation = 'RGB'
                    ds.SamplesPerPixel = 3
                    ds.add_new(0x00280006, 'US', 0)
                    ds.Rows, ds.Columns, _ = array[-(j+1),:,:].shape
                else:
                    ds.Rows, ds.Columns = array[-(j+1),:,:].shape
                ds.save_as(os.path.join(savedir, case, key, f"IMG{j+1:04}.dcm"))

    def _is_negative_possible(self, dtype):
        if np.issubdtype(dtype, np.signedinteger) or np.issubdtype(dtype, np.floating):
            return 1
        else:
            return 0

if __name__ == "__main__":
    test = Dcm() 
    print("today ==>", test.today, "age ==>", test.age, "random6num ==>", test.random6num)
    print(test.ds)