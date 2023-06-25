import os 
from glob import glob
import numpy as np
import random
import datetime
from PIL import Image
import pydicom
from pydicom.dataset import Dataset
from pydicom.uid import generate_uid

class Dammy:
    def __init__(self):
        # ファイルメタ情報
        file_meta = pydicom.Dataset()
        file_meta.FileMetaInformationGroupLength = 196
        file_meta.FileMetaInformationVersion = b'\x00\x01'
        file_meta.MediaStorageSOPClassUID = "1.2.840.10008.5.1.4.1.1.4"  # MR Image Storage
        file_meta.MediaStorageSOPInstanceUID = "1.3.6.1.4.1.14519.5.2.1.1078.3273.178181433764864049172821167580"
        file_meta.TransferSyntaxUID = "1.2.840.10008.1.2.1"  # Explicit VR Little Endian
        file_meta.ImplementationClassUID = "1.2.40.0.13.1.1.1"
        file_meta.ImplementationVersionName = "dcm4che-1.4.35"
        # データセット
        ds = pydicom.dcmread(pydicom.filebase.DicomBytesIO(b"\x00"*16*8 + b"DICM" + b'\x02\x00\x00\x00'))
        ds.file_meta = file_meta
        ds.add_new([0x0009, 0x0010], 'LO', 'GEMS_IDEN_01')
        ds.add_new([0x0009, 0x1002], 'SH', 'rgmr')
        ds.add_new([0x0009, 0x1004], 'SH', 'SIGNA')
        ds.add_new([0x0009, 0x10e3], 'UI', '1.3.6.1.4.1.14519.5.2.1.1078.3273.122565008753391586789739557548')

        ds.SpecificCharacterSet = "ISO_IR 100"
        ds.ImageType = ["ORIGINAL", "PRIMARY", "OTHER"]
        ds.SOPClassUID = "1.2.840.10008.5.1.4.1.1.4"  # MR Image Storage
        ds.SOPInstanceUID = "1.3.6.1.4.1.14519.5.2.1.1078.3273.178181433764864049172821167580"
        ds.StudyDate = "20030324"
        ds.SeriesDate = "20030324"
        ds.AcquisitionDate = "20030324"
        ds.ContentDate = "20030324"
        ds.StudyTime = "112250.000000"
        ds.SeriesTime = "112823"
        ds.AcquisitionTime = "112823"
        ds.ContentTime = "112823"
        ds.AccessionNumber = "1418862270511534"
        ds.Modality = "MR"
        ds.Manufacturer = "GE MEDICAL SYSTEMS"
        ds.ReferringPhysicianName = ""
        ds.StudyDescription = "MR ABDOMEN NONENHANCED & ENHANCED=AB"
        ds.SeriesDescription = "AX SSFSE TE 70"
        ds.ManufacturerModelName = "DISCOVERY MR450"
        ds.PatientName = "dammy"
        ds.PatientID = "dammy"
        ds.PatientBirthDate = ""
        ds.PatientSex = "F"
        ds.PatientAge = "061Y"
        ds.PatientWeight = None
        ds.AdditionalPatientHistory = ""
        ds.ClinicalTrialTimePointID = "-62"
        ds.ClinicalTrialTimePointDescription = "Days offset from diagnosis"
        ds.PatientIdentityRemoved = "YES"
        ds.DeidentificationMethod = ['Per DICOM PS 3.15 AnnexE. Details in 0012,0064', 'Per DICOM PS 3.15 AnnexE. Details in 0012,0064']

        # De-identification Method Code Sequence
        deidentification_sequence = []
        code_values = ['113100', '113106', '113108', '113109', '113111', '113100', '113101', '113104', '113105', '113107', '113108', '113109', '113111']
        for code_value in code_values:
            item = pydicom.Dataset()
            item.CodeValue = code_value
            item.CodingSchemeDesignator = 'DCM'
            item.CodeMeaning = 'Some Code Meaning'  # 実際のコードの意味.
            deidentification_sequence.append(item)
            ds.DeidentificationMethodCodeSequence = deidentification_sequence
        # Set the values of the DICOM tags
        ds.add_new((0x0013, 0x0010), 'LO', 'dam')
        ds.add_new((0x0013, 0x1010), 'LO', 'dam')
        ds.add_new((0x0013, 0x1013), 'LO', '10000000')
        ds.add_new((0x0018, 0x0015), 'CS', 'PANCREAS')
        ds.add_new((0x0018, 0x0020), 'CS', 'SE')
        ds.add_new((0x0018, 0x0021), 'CS', 'SK')
        ds.add_new((0x0018, 0x0022), 'CS', ['FAST_GEMS', 'FC_SLICE_AX_GEMS', 'FC', 'EDR_GEMS', 'SS_GEMS', 'FILTERED_GEMS', 'ACC_GEMS', 'PFP'])
        ds.add_new((0x0018, 0x0023), 'CS', '2D')
        ds.add_new((0x0018, 0x0025), 'CS', 'N')
        ds.add_new((0x0018, 0x0050), 'DS', '6.0')
        ds.add_new((0x0018, 0x0080), 'DS', '1200.0')
        ds.add_new((0x0018, 0x0081), 'DS', '69.44')
        ds.add_new((0x0018, 0x0083), 'DS', '0.578947')
        ds.add_new((0x0018, 0x0084), 'DS', '63.862145')
        ds.add_new((0x0018, 0x0085), 'SH', '1H')
        ds.add_new((0x0018, 0x0086), 'IS', '1')
        ds.add_new((0x0018, 0x0087), 'DS', '1.5')
        ds.add_new((0x0018, 0x0088), 'DS', '6.0')
        ds.add_new((0x0018, 0x0091), 'IS', '1')
        ds.add_new((0x0018, 0x0093), 'DS', '57.8947')
        ds.add_new((0x0018, 0x0094), 'DS', '100.0')
        ds.add_new((0x0018, 0x0095), 'DS', '195.312')
        ds.add_new((0x0018, 0x1020), 'LO', ['25', 'LX', 'MR Software release:DV25.0_R01_1451.a'])
        ds.add_new((0x0018, 0x1088), 'IS', '0')
        ds.add_new((0x0018, 0x1090), 'IS', '0')
        ds.add_new((0x0018, 0x1094), 'IS', '0')
        ds.add_new((0x0018, 0x1100), 'DS', '320.0')
        ds.add_new((0x0018, 0x1250), 'SH', 'HD BodyUpper')
        ds.AcquisitionMatrix = [256, 0, 0, 224]
        ds.InPlanePhaseEncodingDirection = 'COL'
        ds.FlipAngle = '90.0'
        ds.VariableFlipAngleFlag = 'N'
        ds.SAR = '1.22821'
        ds.PatientPosition = 'FFS'
        ds.add_new((0x0019, 0x0010), 'LO', 'GEMS_ACQU_01')
        ds.add_new((0x0019, 0x100f), 'DS', '1238.300049')
        ds.add_new((0x0019, 0x1011), 'SS', 0)
        ds.add_new((0x0019, 0x1012), 'SS', 19)
        ds.add_new((0x0019, 0x1017), 'SS', 16)
        ds.add_new((0x0019, 0x1018), 'LO', 'S')
        ds.add_new((0x0019, 0x1019), 'DS', '53.2989')
        ds.add_new((0x0019, 0x101a), 'LO', 'I')
        ds.add_new((0x0019, 0x101b), 'DS', '-144.701')
        ds.add_new((0x0019, 0x101e), 'DS', '320.0')
        ds.add_new((0x0019, 0x105a), 'FL', 40093064.0)
        ds.add_new((0x0019, 0x107d), 'DS', '0.0')
        ds.add_new((0x0019, 0x107e), 'SS', 1)
        ds.add_new((0x0019, 0x107f), 'DS', '0.0')
        ds.add_new((0x0019, 0x1081), 'SS', 1)
        ds.add_new((0x0019, 0x1084), 'DS', '2.456429')
        ds.add_new((0x0019, 0x1087), 'DS', '0.0')
        ds.add_new((0x0019, 0x1088), 'SS', 0)
        ds.add_new((0x0019, 0x108a), 'SS', 8)
        ds.add_new((0x0019, 0x108b), 'SS', 30)
        ds.add_new((0x0019, 0x108d), 'DS', '0.0')
        ds.add_new((0x0019, 0x108f), 'SS', 0)
        ds.add_new((0x0019, 0x1090), 'SS', 17)
        ds.add_new((0x0019, 0x1091), 'DS', '20046532.0')
        ds.add_new((0x0019, 0x1092), 'SL', 0)
        ds.add_new((0x0019, 0x1093), 'DS', '638621450.0')
        ds.add_new((0x0019, 0x1094), 'SS', 184)
        ds.add_new((0x0019, 0x1095), 'SS', 8)
        ds.add_new((0x0019, 0x1096), 'SS', 30)
        ds.add_new((0x0019, 0x1097), 'SL', 40966)
        ds.add_new((0x0019, 0x109b), 'SS', 1)
        ds.add_new((0x0019, 0x109c), 'LO', 'ssfse')
        ds.add_new((0x0019, 0x109d), 'DT', '20070223185404')
        ds.add_new((0x0019, 0x109e), 'LO', 'SSFSE')
        ds.add_new((0x0019, 0x109f), 'SS', 3)
        ds.add_new((0x0019, 0x10a0), 'SS', 0)
        ds.add_new((0x0019, 0x10a1), 'SS', 0)
        ds.add_new((0x0019, 0x10a2), 'SL', 45582)
        ds.add_new((0x0019, 0x10a3), 'UL', 0)
        ds.add_new((0x0019, 0x10a4), 'SS', 0)
        ds.add_new((0x0019, 0x10be), 'DS', '0.0')
        ds.add_new((0x0019, 0x10c0), 'SS', 0)
        ds.add_new((0x0019, 0x10c2), 'SS', 9990)
        ds.add_new((0x0019, 0x10c3), 'SS', 9990)
        ds.add_new((0x0019, 0x10c4), 'SS', 9990)
        ds.add_new((0x0019, 0x10c5), 'SS', 9990)
        ds.add_new((0x0019, 0x10c6), 'SS', 9990)
        ds.add_new((0x0019, 0x10c7), 'SS', 9990)
        ds.add_new((0x0019, 0x10c8), 'SS', 0)
        ds.add_new((0x0019, 0x10c9), 'SS', 0)
        ds.add_new((0x0019, 0x10ca), 'SS', 0)
        ds.add_new((0x0019, 0x10cb), 'SS', 0)
        ds.add_new((0x0019, 0x10cc), 'SS', 0)
        ds.add_new((0x0019, 0x10cd), 'SS', 0)
        ds.add_new((0x0019, 0x10ce), 'SS', 2)
        ds.add_new((0x0019, 0x10cf), 'SS', 0)
        ds.add_new((0x0019, 0x10d2), 'SS', 0)
        ds.add_new((0x0019, 0x10d3), 'SH', '')
        ds.add_new((0x0019, 0x10d5), 'SS', 2)
        ds.add_new((0x0019, 0x10d7), 'SS', 0)
        ds.add_new([0x0019, 0x10d8], 'SS', 0)
        ds.add_new([0x0019, 0x10d9], 'DS', '0.0')
        ds.add_new([0x0019, 0x10e2], 'DS', '0.0')
        ds.add_new([0x0019, 0x10f2], 'SS', 0)
        ds.add_new([0x0019, 0x10f9], 'DS', '184.0')
        ds.add_new([0x0020, 0x000d], 'UI', '1.3.6.1.4.1.14519.5.2.1.1078.3273.133725899522537665602741713326')
        ds.add_new([0x0020, 0x000e], 'UI', '1.3.6.1.4.1.14519.5.2.1.1078.3273.189259952711431159887727981967')
        ds.add_new([0x0020, 0x0010], 'SH', '')
        ds.add_new([0x0020, 0x0011], 'IS', '8')
        ds.add_new([0x0020, 0x0012], 'IS', '1')
        ds.add_new([0x0020, 0x0013], 'IS', '15')
        ds.add_new([0x0020, 0x0032], 'DS', [-161.78, -153.863, -30.7011])
        ds.ImageOrientationPatient = [1, -0, 0, -0, 1, 0]
        ds.FrameOfReferenceUID = "1.3.6.1.4.1.14519.5.2.1.1078.3273.210199795815576245591551798364"
        ds.Laterality = ''
        ds.ImagesInAcquisition = '34'
        ds.PositionReferenceIndicator = ''
        ds.SliceLocation = '-30.70111084'
        ds.StackID = '1'
        ds.InStackPositionNumber = 15
        ds.add_new((0x0021, 0x0010), 'LO', 'GEMS_RELA_01')
        ds.add_new((0x0021, 0x1036), 'SS', 17)
        ds.add_new((0x0021, 0x104f), 'SS', 34)
        ds.add_new((0x0021, 0x1050), 'SS', 0)
        ds.add_new((0x0021, 0x1051), 'DS', '0.0')
        ds.add_new((0x0021, 0x1052), 'DS', '0.0')
        ds.add_new((0x0021, 0x1053), 'DS', '0.0')
        ds.add_new((0x0021, 0x1056), 'SL', 0)
        ds.add_new((0x0021, 0x1057), 'SL', 0)
        ds.add_new((0x0021, 0x1058), 'SL', 0)
        ds.add_new((0x0021, 0x1059), 'SL', 0)
        ds.add_new((0x0021, 0x105a), 'SL', 0)
        ds.add_new((0x0021, 0x105b), 'DS', '0.0')
        ds.add_new((0x0021, 0x105c), 'DS', '0.0')
        ds.add_new((0x0021, 0x105d), 'DS', '0.0')
        ds.add_new((0x0021, 0x105e), 'DS', '0.0')
        ds.add_new((0x0021, 0x105f), 'DS', '0.0')
        ds.add_new((0x0021, 0x1081), 'DS', '0.0')
        ds.add_new((0x0021, 0x1082), 'DS', '0.0')
        ds.add_new((0x0021, 0x1083), 'DS', '0.0')
        ds.add_new((0x0021, 0x1084), 'DS', '0.0')
        ds.add_new((0x0023, 0x0010), 'LO', 'GEMS_STDY_01')
        ds.add_new((0x0023, 0x1074), 'SL', 0)
        ds.add_new((0x0023, 0x107d), 'SS', 0)
        ds.add_new((0x0025, 0x0010), 'LO', 'GEMS_SERS_01')
        ds.add_new((0x0025, 0x1006), 'SS', 19)
        ds.add_new((0x0025, 0x1007), 'SL', 34)
        ds.add_new([0x0025, 0x1010], 'SL', 0)
        ds.add_new([0x0025, 0x1011], 'SS', 2)
        ds.add_new([0x0025, 0x1014], 'SL', 0)
        ds.add_new([0x0025, 0x1017], 'SL', 0)
        ds.add_new([0x0025, 0x1018], 'SL', 0)
        ds.add_new([0x0025, 0x1019], 'SL', 34)
        ds.add_new([0x0027, 0x0010], 'LO', 'GEMS_IMAG_01')
        ds.add_new([0x0027, 0x1010], 'SS', 0)
        ds.add_new([0x0027, 0x1030], 'SH', '')
        ds.add_new([0x0027, 0x1031], 'SS', 1)
        ds.add_new([0x0027, 0x1032], 'SS', 19)
        ds.add_new([0x0027, 0x1033], 'UL', 1107298312)
        ds.add_new([0x0027, 0x1035], 'SS', 16)
        ds.add_new([0x0027, 0x1040], 'SH', 'I')
        ds.add_new([0x0027, 0x1041], 'FL', -30.70111083984375)
        ds.add_new([0x0027, 0x1060], 'FL', 256.0)
        ds.add_new([0x0027, 0x1061], 'FL', 224.0)
        ds.add_new([0x0027, 0x1062], 'FL', 0.5789473652839661)
        ds.add_new([0x0028, 0x0002], 'US', 1)
        ds.add_new([0x0028, 0x0004], 'CS', 'MONOCHROME2')
        ds.add_new([0x0028, 0x0010], 'US', 512)
        ds.add_new([0x0028, 0x0011], 'US', 512)
        ds.add_new([0x0028, 0x0030], 'DS', [0.625, 0.625])
        ds.add_new([0x0028, 0x0100], 'US', 16)
        ds.add_new([0x0028, 0x0101], 'US', 16)
        ds.add_new([0x0028, 0x0102], 'US', 15)
        ds.add_new([0x0028, 0x0103], 'US', 1)
        ds.add_new([0x0028, 0x0106], 'SS', 0)
        ds.add_new([0x0028, 0x0107], 'SS', 1789)
        ds.add_new([0x0028, 0x0303], 'CS', 'MODIFIED')
        ds.add_new([0x0028, 0x1050], 'DS', '894.0')
        ds.add_new([0x0028, 0x1051], 'DS', '1789.0')
        ds.add_new([0x0029, 0x0010], 'LO', 'GEMS_IMPS_01')
        ds.add_new([0x0029, 0x1015], 'SL', 0)
        ds.add_new([0x0029, 0x1016], 'SL', 0)
        ds.add_new([0x0029, 0x1017], 'SL', 0)
        ds.add_new([0x0029, 0x1018], 'SL', 0)
        ds.add_new([0x0029, 0x1026], 'SS', 2)
        ds.add_new([0x0029, 0x1034], 'SL', 16384)
        ds.add_new([0x0029, 0x1035], 'SL', 0)
        ds.add_new([0x0031, 0x0010], 'LO', 'MITRA LINKED ATTRIBUTES 1.0')
        ds.add_new([0x0031, 0x0011], 'LO', 'AGFA EPR PROCEDURE CODE')
        ds.add_new([0x0031, 0x0012], 'LO', 'AGFA PACS Archive Mirroring 1.0')
        ds.add_new([0x0032, 0x000a], 'CS', 'READ')
        ds.add_new([0x0032, 0x000c], 'CS', 'NORMAL')
        ds.add_new([0x0032, 0x1030], 'LO', '')
        ds.add_new([0x0032, 0x4000], 'LT', '')
        ds.add_new([0x0033, 0x0010], 'LO', 'MITRA OBJECT UTF8 ATTRIBUTES 1.0')
        ds.add_new([0x0040, 0x0244], 'DA', '20030324')
        ds.add_new([0x0040, 0x0245], 'TM', '111316')
        ds.add_new([0x0040, 0x0254], 'LO', '')
        ds.add_new([0x0043, 0x0010], 'LO', 'GEMS_PARM_01')
        ds.add_new([0x0043, 0x0011], 'LO', 'dcm4che/archive')
        ds.add_new([0x0043, 0x1001], 'SS', 4)
        ds.add_new([0x0043, 0x1002], 'SS', 3)
        ds.add_new([0x0043, 0x1003], 'SS', 0)
        ds.add_new([0x0043, 0x1004], 'SS', 12)
        ds.add_new([0x0043, 0x1006], 'SS', 0)
        ds.add_new([0x0043, 0x1007], 'SS', 0)
        ds.add_new([0x0043, 0x1008], 'SS', 0)
        ds.add_new([0x0043, 0x1009], 'SS', 0)
        ds.add_new([0x0043, 0x100a], 'SS', 1)
        ds.add_new([0x0043, 0x100b], 'DS', '0.0')
        ds.add_new([0x0043, 0x100c], 'DS', '100.0')
        ds.add_new([0x0043, 0x100d], 'DS', '98.446892')
        ds.add_new([0x0043, 0x100e], 'DS', '0.0')
        ds.add_new([0x0043, 0x1010], 'US', 0)
        ds.add_new([0x0043, 0x101c], 'SS', 0)
        ds.add_new([0x0043, 0x101d], 'SS', 0)
        ds.add_new([0x0043, 0x102c], 'SS', 0)
        ds.add_new([0x0043, 0x102d], 'SH', 'p+')
        ds.add_new([0x0043, 0x102e], 'SH', '')
        ds.add_new([0x0043, 0x102f], 'SS', 0)
        ds.add_new([0x0043, 0x1032], 'SS', 2)
        ds.add_new([0x0043, 0x1033], 'FL', 0.0)
        ds.add_new([0x0043, 0x1034], 'IS', '0')
        ds.add_new([0x0043, 0x1035], 'UL', 0)
        ds.add_new([0x0043, 0x1036], 'UL', 0)
        ds.add_new([0x0043, 0x1037], 'UL', 0)
        ds.add_new([0x0043, 0x1038], 'FL', [0.0] * 24)
        ds.add_new([0x0043, 0x1039], 'IS', [0, 33, 0, 0])
        ds.add_new([0x0043, 0x107d], 'US', 0)
        ds.add_new([0x0043, 0x1081], 'LO', 'C-GE_HDx BodyUpper')
        ds.add_new([0x0043, 0x1083], 'DS', [0.678571, 1])
        ds.add_new([0x0043, 0x1084], 'LO', ['10000', '7', '5', '1', 'asset', 'YES', 'ASSET'])
        ds.add_new([0x0043, 0x1088], 'UI', '1.3.6.1.4.1.14519.5.2.1.1078.3273.158970295102526298673099587660')
        ds.add_new([0x0043, 0x1089], 'LO', ['FDA', 'IEC_FIRST_LEVEL', 'IEC_FIRST_LEVEL'])
        ds.add_new([0x0043, 0x108a], 'CS', 'COL')
        ds.add_new([0x0043, 0x1090], 'LO', ['WHOLE_BODY_6_MIN', 'LOCAL_PEAK_6_MIN', 'PARTIAL_BODY_6MIN'])
        ds.add_new([0x0043, 0x1091], 'DS', [1.228, 2.45643, 1.22821])
        ds.add_new([0x0043, 0x1095], 'LO', 'TG/s5,CF/s7,AS/s7')
        ds.add_new([0x0043, 0x1096], 'CS', 'PRODUCT')
        ds.add_new([0x0043, 0x1097], 'LO', ['5', '1', '1.5 0.2 0.2 2 128 0.2 1.25', '1.5 0.2 0.2 2 128 0.2 1.25', '1.5 0.2 0.2 2 128 0.2 1.25', '100', '0', '0', 'rev=1;a=75;b=2;c=32;d=8;e=3;f=2;g=1;h=0'])
        ds.add_new([0x0043, 0x1098], 'UI', '1.3.6.1.4.1.14519.5.2.1.1078.3273.158970295102526298673099587660')
        ds.add_new([0x0043, 0x109a], 'IS', '1')
        ds.add_new([0x7fd9, 0x0010], 'LO', 'agfa/preservedItems')
        ds.is_little_endian = True 
        ds.is_implicit_VR = False 

        array = np.zeros((512, 512), dtype ="int16")
        array[100:300, 100:300] = 1000
        ds.PixelData = array.tobytes()
        self.ds = ds
        
if __name__ == "__main__":
    x = Dammy()
    print(x.ds)
