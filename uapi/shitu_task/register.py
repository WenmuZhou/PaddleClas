# Copyright (c) 2023 PaddlePaddle Authors. All Rights Reserved. 
#   
# Licensed under the Apache License, Version 2.0 (the "License");   
# you may not use this file except in compliance with the License.  
# You may obtain a copy of the License at   
#   
#     http://www.apache.org/licenses/LICENSE-2.0    
#   
# Unless required by applicable law or agreed to in writing, software   
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
# See the License for the specific language governing permissions and   
# limitations under the License.

import os.path as osp

from ..base.register import register_suite_info, register_model_info
from .model import ShiTuModel
from .runner import ShiTuRunner
from .config import ShiTuConfig

# XXX: Hard-code relative path of repo root dir
_file_path = osp.realpath(__file__)
REPO_ROOT_PATH = osp.abspath(osp.join(osp.dirname(_file_path), '..', '..'))

register_suite_info({
    'suite_name': 'ShiTu',
    'model': ShiTuModel,
    'runner': ShiTuRunner,
    'config': ShiTuConfig,
    'runner_root_path': REPO_ROOT_PATH
})

PPLCNetV2_base_ShiTu_CFG_PATH = osp.join(
    REPO_ROOT_PATH,
    'ppcls/configs/GeneralRecognitionV2/GeneralRecognitionV2_PPLCNetV2_base.yaml'
)

register_model_info({
    'model_name': 'PPLCNetV2_base_ShiTu',
    'suite': 'ShiTu',
    'config_path': PPLCNetV2_base_ShiTu_CFG_PATH,
    'auto_compression_config_path': PPLCNetV2_base_ShiTu_CFG_PATH,
    'supported_apis': ['train', 'export', 'infer', 'compression']
})